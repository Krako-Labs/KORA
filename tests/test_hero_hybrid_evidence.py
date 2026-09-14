import json

import pytest
from test_hero_remote_execution import execute, output, service
from test_studio_hero_live import _evidence

from kora.hero_hybrid_evidence import (
    ENV,
    combine_evidence,
    hybrid_payload,
    load_hybrid_evidence,
)
from kora.hero_live_execution import _digest
from kora.hero_replay import replay_hero_events


def sources(*, observed=False):
    mac = _evidence()
    mac.update(
        output=output(),
        output_digest=_digest(output()),
        input_digest=_digest(service().model_dump(mode="json")),
    )
    remote = execute()
    if observed:
        # Explicit synthetic input for loader tests only; never retained as live evidence.
        remote["evidence_level"] = "observed"
        for e in remote["event_log"]["events"]:
            e["evidence_level"] = "observed"
    receipt = {
        "lease_id": remote["lease_id"],
        "owned_unit_stopped": True,
        "restored_health": True,
        "restored_model": "openai/gpt-oss-120b",
        "lease_released": True,
        "foreign_work_preserved": True,
    }
    return mac, remote, receipt


def test_combined_replay_retains_separate_counts_and_source_hashes():
    mac, remote, receipt = sources()
    data = combine_evidence(mac, remote, receipt, allow_fixture=True)
    assert data["accepted_outcome"]
    assert data["source_digests"] == {
        "mac": _digest(mac),
        "h100": _digest(remote),
        "restoration": _digest(receipt),
    }
    assert replay_hero_events(data["event_log"]["events"]).accepted_outcome
    assert "simultaneous" in data["claim_boundary"]
    assert data["mac"]["actual_execution"]["model_calls"] == 1
    assert data["h100"]["actual_execution"]["owned_remote_model_calls"] == 1


def test_fixture_never_accepted_by_live_loader():
    with pytest.raises(ValueError, match="boundary"):
        combine_evidence(*sources())


@pytest.mark.parametrize(
    "field",
    [
        "owned_unit_stopped",
        "restored_health",
        "lease_released",
        "foreign_work_preserved",
        "lease_id",
        "restored_model",
    ],
)
def test_missing_or_mismatched_restoration_blocks_integration(field):
    mac, remote, receipt = sources()
    receipt[field] = False
    data = combine_evidence(mac, remote, receipt, allow_fixture=True)
    assert not data["accepted_outcome"]
    assert not replay_hero_events(data["event_log"]["events"]).accepted_outcome


@pytest.mark.parametrize(
    "mutation",
    [
        lambda m, r: m.update(input_digest="f" * 64),
        lambda m, r: m["output"].update(promise="unsupported"),
        lambda m, r: m["actual_execution"].update(provider_calls=1),
        lambda m, r: m["usage"][0].update(tokens_out=257),
        lambda m, r: r["actual_execution"].update(owned_remote_model_calls=3),
        lambda m, r: r["attempts"][0].update(tokens_out=None),
        lambda m, r: r["attempts"][0].update(tokens_out=True),
        lambda m, r: r["output"].update(headline="unsupported"),
        lambda m, r: r.update(output_digest="f" * 64),
        lambda m, r: r.update(privacy_mode="local_only"),
        lambda m, r: r["verification"].update(semantic_quality="passed"),
        lambda m, r: r["event_log"]["events"].pop(),
    ],
)
def test_tamper_rejected(mutation):
    mac, remote, receipt = sources()
    mutation(mac, remote)
    with pytest.raises((ValueError, KeyError)):
        combine_evidence(mac, remote, receipt, allow_fixture=True)


def test_read_only_payload_and_derived_fields(tmp_path):
    data = combine_evidence(*sources(observed=True))
    path = tmp_path / "hybrid.json"
    path.write_text(json.dumps(data))
    view = hybrid_payload({ENV: str(path)})
    assert view["available"] and view["accepted_outcome"]
    assert str(path) not in json.dumps(view)
    data["source_digests"]["mac"] = "f" * 64
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        load_hybrid_evidence(path)


def test_unconfigured_and_symlink_rejected(tmp_path):
    assert hybrid_payload({}) == {"available": False, "status": "not_configured"}
    path = tmp_path / "a.json"
    path.write_text("{}")
    link = tmp_path / "link.json"
    link.symlink_to(path)
    with pytest.raises(ValueError):
        load_hybrid_evidence(link)


@pytest.mark.parametrize("valid", [True, False])
def test_http_hybrid_routes_are_read_only_and_fail_closed(monkeypatch, tmp_path, valid):
    import threading
    from http.server import ThreadingHTTPServer
    from urllib.error import HTTPError
    from urllib.request import Request, urlopen

    from kora.studio_server import create_studio_request_handler

    target = tmp_path / "hybrid.json"
    target.write_text(
        json.dumps(combine_evidence(*sources(observed=True))) if valid else "{}"
    )
    monkeypatch.setenv(ENV, str(target))

    def no_probe():
        raise AssertionError("read-only route must not probe or execute")

    instance = ThreadingHTTPServer(
        ("127.0.0.1", 0), create_studio_request_handler(no_probe)
    )
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{instance.server_port}"
    try:
        with urlopen(base + "/hero/hybrid") as response:
            assert b"READ ONLY" in response.read()
        with urlopen(base + "/hero-assets/hero-hybrid.js") as response:
            assert b"/api/hero/hybrid" in response.read()
        with urlopen(base + "/hero-assets/hero-hybrid.css") as response:
            assert "text/css" in response.headers["Content-Type"]
        if valid:
            with urlopen(base + "/api/hero/hybrid") as response:
                assert json.load(response)["accepted_outcome"] is True
        else:
            with pytest.raises(HTTPError) as error:
                urlopen(base + "/api/hero/hybrid")
            assert error.value.code == 422
        with pytest.raises(HTTPError) as error:
            urlopen(Request(base + "/api/hero/hybrid", data=b"{}"))
        assert error.value.code == 405
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join()


@pytest.mark.parametrize(
    "mutation",
    ["answer", "source_digest", "evidence_ref", "evidence_level",
     "task_label", "log_run_id", "log_schema", "projection"],
)
def test_combined_loader_binds_replay_to_verified_sources(tmp_path, mutation):
    data = combine_evidence(*sources(observed=True))
    log = data["event_log"]
    if mutation == "answer":
        event = next(e for e in log["events"] if e["event_type"] == "merge.completed")
        event["payload"]["answer"] = {"headline": "Unrelated replay answer"}
    elif mutation == "source_digest":
        event = next(e for e in log["events"]
                     if e["event_type"] == "task.completed" and e["task_id"] == "mac")
        event["payload"]["evidence_digest"] = "f" * 64
    elif mutation == "evidence_ref":
        log["events"][0]["evidence_refs"] = ["sha256:" + "f" * 64]
    elif mutation == "evidence_level":
        for event in log["events"]:
            event["evidence_level"] = "fixture"
    elif mutation == "task_label":
        event = next(e for e in log["events"] if e["event_type"] == "task.created")
        event["payload"]["label"] = "Unrelated replay task"
    elif mutation == "log_run_id":
        log["run_id"] = "unrelated-run"
    elif mutation == "log_schema":
        log["schema_version"] = "unknown-log"
    else:
        log["projection"]["accepted_outcome"] = False
    path = tmp_path / "inconsistent-replay.json"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="mismatch"):
        load_hybrid_evidence(path)


def test_combined_loader_preserves_recorded_timestamps(tmp_path):
    data = combine_evidence(*sources(observed=True))
    path = tmp_path / "recorded.json"
    path.write_text(json.dumps(data))
    loaded = load_hybrid_evidence(path)
    assert loaded == data
