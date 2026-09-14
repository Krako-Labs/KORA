"""Offline operations tests. All generated records here are synthetic test inputs."""
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest
from test_hero_hybrid_evidence import sources

from kora.hero_hybrid_evidence import ENV, combine_evidence
from kora.studio_festa import (
    LOCK_ENV,
    create_show_lock,
    fixture_replay,
    preflight,
    software_fingerprint,
)
from kora.studio_server import create_studio_request_handler


@pytest.fixture
def configured(tmp_path):
    record = tmp_path / "test-evidence.json"
    record.write_text(json.dumps(combine_evidence(*sources(observed=True))))
    package = tmp_path / "package"
    package.mkdir()
    (package / "source.py").write_text("pass\n")
    env = {ENV: str(record), LOCK_ENV: str(tmp_path / "lock.json")}
    lock = create_show_lock(env, package_root=package)
    (tmp_path / "lock.json").write_text(json.dumps(lock))
    return env, package


def test_fixture_is_stable_and_never_measured():
    first, second = fixture_replay(), fixture_replay()
    assert first["identity"] == second["identity"]
    assert first["new_model_calls"] == 0
    assert first["source_objective_pass"] is False
    assert first["source_model_calls"] is None
    assert all(f["event"]["evidence_level"] == "fixture" for f in first["frames"])


def test_preflight_binds_code_and_both_sources_without_new_execution(configured):
    env, package = configured
    value = preflight(env, package_root=package)
    assert value["ready"]
    assert value["checks"]["lock"] == "verified"
    assert value["retained"]["source_model_calls"] == {"mac": 1, "h100": 1}
    assert value["retained"]["frames"][-1]["projection"]["accepted_outcome"]
    assert value["new_model_calls"] == 0
    assert value["live_runtime_status"] == "not_checked"
    assert value["automatic_fallback"] is False
    assert env[ENV] not in json.dumps(value)
    frames = value["retained"]["frames"]
    assert [f["event"]["sequence"] for f in frames] == list(range(len(frames)))
    assert frames[0]["projection"]["tasks"] == {}
    assert len(frames[-1]["projection"]["tasks"]) == 3


@pytest.mark.parametrize("part", ["source", "evidence", "lock", "fixture", "schema", "extra", "boolean_calls"])
def test_show_lock_tampering_blocks_replay(configured, part):
    env, package = configured
    lock_path = Path(env[LOCK_ENV])
    lock = json.loads(lock_path.read_text())
    if part == "source":
        (package / "source.py").write_text("changed\n")
    elif part == "evidence":
        Path(env[ENV]).write_text("{}")
    elif part == "lock":
        lock["retained_sha256"] = "0" * 64
    elif part == "fixture":
        lock["fixture_sha256"] = "0" * 64
    elif part == "schema":
        lock["schema_version"] = "other"
    elif part == "boolean_calls":
        lock["new_model_calls"] = False
    else:
        lock["unexpected"] = True
    lock_path.write_text(json.dumps(lock))
    value = preflight(env, package_root=package)
    assert not value["ready"]
    assert value["retained"] is None
    assert value["fixture"]["mode"] == "fixture"
    assert value["automatic_fallback"] is False


@pytest.mark.parametrize("raw", ["{}", "[]", "null", "{", '"bad"', ""])
def test_malformed_evidence_and_lock_fail_closed(configured, raw):
    from pathlib import Path
    env, package = configured
    Path(env[ENV]).write_text(raw)
    Path(env[LOCK_ENV]).write_text(raw)
    result = preflight(env, package_root=package)
    assert not result["ready"]
    assert result["retained"] is None


def test_missing_source_and_lock_never_auto_fallback():
    result = preflight({})
    assert not result["ready"]
    assert result["checks"]["retained"] == "not_configured"
    assert result["checks"]["lock"] == "not_configured"
    assert result["automatic_fallback"] is False


def test_changed_valid_source_does_not_reuse_lock(configured):
    from pathlib import Path
    env, package = configured
    path = Path(env[ENV])
    original = path.read_bytes()
    data = json.loads(original)
    data["mac"]["recorded_at"] = "2026-09-15T00:00:00Z"
    data = combine_evidence(data["mac"], data["h100"], data["restoration"])
    path.write_text(json.dumps(data))
    result = preflight(env, package_root=package)
    assert result["checks"]["retained"] == "verified"
    assert result["checks"]["lock"] == "mismatch"
    assert not result["ready"]


def test_lock_symlink_rejected(configured):
    env, package = configured
    link = package.parent / "linked-lock"
    link.symlink_to(env[LOCK_ENV])
    env[LOCK_ENV] = str(link)
    assert preflight(env, package_root=package)["checks"]["lock"] == "rejected"


def test_package_identity_covers_assets_and_is_path_independent(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    for p in [a, b]:
        (p / "x.py").write_text("source")
        (p / "x.js").write_text("asset")
    assert software_fingerprint(a) == software_fingerprint(b)
    (b / "x.js").write_text("tampered")
    assert software_fingerprint(a) != software_fingerprint(b)


def test_failed_historical_restoration_cannot_lock(configured):
    from pathlib import Path
    env, package = configured
    path = Path(env[ENV])
    data = json.loads(path.read_text())
    data["restoration"]["restored_health"] = False
    data = combine_evidence(data["mac"], data["h100"], data["restoration"])
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        create_show_lock(env, package_root=package)
    assert preflight(env, package_root=package)["checks"]["retained"] == "objective_failed"


def test_http_preflight_assets_no_probes_no_mutations(monkeypatch, configured):
    from pathlib import Path
    env, _ = configured
    Path(env[LOCK_ENV]).write_text(json.dumps(create_show_lock(env)))
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    def no_probe():
        raise AssertionError("Festa must not probe runtimes")
    server = ThreadingHTTPServer(("127.0.0.1", 0), create_studio_request_handler(no_probe))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        for route in ["/hero/festa", "/hero-assets/hero-festa.js", "/hero-assets/hero-festa.css"]:
            with urlopen(base + route) as response:
                assert response.status == 200
                assert response.read()
        with urlopen(base + "/api/hero/festa") as response:
            assert json.load(response)["ready"]
        for route in ["/api/hero/festa?path=/private", "/api/hero/festa?mode=live"]:
            with pytest.raises(HTTPError) as error:
                urlopen(base + route)
            assert error.value.code == 400
        with pytest.raises(HTTPError) as error:
            urlopen(Request(base + "/api/hero/festa", data=b"{}", method="POST"))
        assert error.value.code in {404, 405}
    finally:
        server.shutdown(); server.server_close(); thread.join()


def test_running_server_rejects_changed_disk_software(monkeypatch, configured):
    import kora.studio_festa as module
    env, _ = configured
    Path(env[LOCK_ENV]).write_text(json.dumps(create_show_lock(env)))
    monkeypatch.setattr(module, "_STARTUP_SOFTWARE_SHA256", "0" * 64)
    value = preflight(env)
    assert not value["ready"]
    assert value["checks"]["software"] == "restart_required"
