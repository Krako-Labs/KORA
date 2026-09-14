from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

from kora.hero_contracts import HeroEvent
from kora.hero_event_log import HeroEventLog
from kora.studio_hero_live import (
    LIVE_EVIDENCE_ENV,
    StudioLiveEvidenceError,
    live_evidence_payload,
    load_live_evidence,
)
from kora.studio_server import create_studio_request_handler


def _event(
    run_id,
    sequence,
    event_type,
    phase,
    status,
    *,
    task_id=None,
    executor_class=None,
    adapter_id=None,
    payload=None,
):
    return HeroEvent(
        event_id=f"{run_id}:{sequence:04d}",
        run_id=run_id,
        sequence=sequence,
        occurred_at=datetime(2026, 9, 14, tzinfo=timezone.utc),
        event_type=event_type,
        phase=phase,
        status=status,
        source="test.live",
        evidence_level="observed",
        task_id=task_id,
        attempt=1 if task_id else None,
        executor_class=executor_class,
        adapter_id=adapter_id,
        payload=payload or {},
    )


def _evidence():
    run_id = "hero-live-test"
    log = HeroEventLog(run_id)
    events = [
        _event(run_id, 0, "run.started", "intake", "running"),
        _event(
            run_id,
            1,
            "task.created",
            "decompose",
            "created",
            task_id="draft",
            payload={"label": "Draft", "purpose": "Test", "dependencies": []},
        ),
        _event(run_id, 2, "task.ready", "execute", "ready", task_id="draft"),
        _event(
            run_id,
            3,
            "task.routed",
            "plan",
            "ready",
            task_id="draft",
            executor_class="local_ai",
            adapter_id="llama.cpp",
        ),
        _event(
            run_id,
            4,
            "task.started",
            "execute",
            "running",
            task_id="draft",
            executor_class="local_ai",
            adapter_id="llama.cpp",
        ),
        _event(
            run_id,
            5,
            "task.completed",
            "execute",
            "completed",
            task_id="draft",
            executor_class="local_ai",
            adapter_id="llama.cpp",
        ),
        _event(run_id, 6, "merge.started", "merge", "running"),
        _event(run_id, 7, "merge.completed", "merge", "completed"),
        _event(run_id, 8, "verification.started", "verify", "running"),
        _event(run_id, 9, "verification.passed", "verify", "completed"),
        _event(run_id, 10, "run.completed", "complete", "completed"),
    ]
    log.extend(events)
    return {
        "schema_version": "hero.live-execution-evidence.v1",
        "run_id": run_id,
        "recorded_at": "2026-09-14T10:00:00+00:00",
        "evidence_level": "observed",
        "claim_boundary": "One bounded local execution; semantic quality not measured.",
        "planning_digest": "0" * 64,
        "runtime_identity": {"network": "loopback", "runtime_version": "test"},
        "effective_config": {"max_output_tokens": 256},
        "output": {"headline": "test"},
        "usage": [{"tokens_in": 10, "tokens_out": 5}],
        "cleanup": {"cleanup_success": True},
        "actual_execution": {
            "runtime_starts": 1,
            "model_calls": 1,
            "provider_calls": 0,
            "live_window_ms": 1000,
        },
        "verification": {
            "accepted_outcome": True,
            "semantic_non_regression": "not_measured",
        },
        "A_workload_control": {"local_model_draft": "completed"},
        "B_local_execution": {
            "execution_performed": True,
            "semantic_quality_measured": False,
        },
        "event_log": log.snapshot(),
    }


def _write(tmp_path, payload=None):
    target = tmp_path / "live.json"
    target.write_text(json.dumps(payload or _evidence()))
    return target


def test_unconfigured_view_is_disabled_without_discovery():
    payload = live_evidence_payload(environ={})
    assert payload["available"] is False
    assert payload["status"] == "not_configured"


def test_valid_live_evidence_is_projected_without_its_host_path(tmp_path):
    target = _write(tmp_path)
    loaded = load_live_evidence(target)
    assert loaded["verification"]["accepted_outcome"] is True
    view = live_evidence_payload(environ={LIVE_EVIDENCE_ENV: str(target)})
    assert view["available"] is True
    assert view["status"] == "objective_pass"
    assert view["actual_execution"]["provider_calls"] == 0
    assert str(target) not in json.dumps(view)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value["actual_execution"].update(provider_calls=1),
        lambda value: value["actual_execution"].update(model_calls=4),
        lambda value: value["usage"][0].update(tokens_out=257),
        lambda value: value["runtime_identity"].update(network="remote"),
        lambda value: value["verification"].update(semantic_non_regression="pass"),
        lambda value: value["cleanup"].update(cleanup_success=False),
    ],
)
def test_contract_violations_fail_closed(tmp_path, mutate):
    payload = _evidence()
    mutate(payload)
    with pytest.raises(StudioLiveEvidenceError):
        load_live_evidence(_write(tmp_path, payload))


def test_symlink_is_rejected(tmp_path):
    target = _write(tmp_path)
    link = tmp_path / "link.json"
    link.symlink_to(target)
    with pytest.raises(StudioLiveEvidenceError, match="non-symlink"):
        load_live_evidence(link)


@pytest.fixture
def server(monkeypatch, tmp_path):
    target = _write(tmp_path)
    monkeypatch.setenv(LIVE_EVIDENCE_ENV, str(target))

    def no_probe():
        raise AssertionError("read-only live route must not probe the host")

    instance = ThreadingHTTPServer(
        ("127.0.0.1", 0), create_studio_request_handler(no_probe)
    )
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{instance.server_port}"
    instance.shutdown()
    instance.server_close()
    thread.join()


def test_http_live_page_asset_and_evidence_route(server):
    with urlopen(server + "/hero/live") as response:
        html = response.read().decode()
        assert "LOCAL EVIDENCE" in html
        assert "read-only" in html
    with urlopen(server + "/hero-assets/hero-live.js") as response:
        assert "application/javascript" in response.headers["Content-Type"]
        assert b"/api/hero/live" in response.read()
    with urlopen(server + "/api/hero/live") as response:
        payload = json.load(response)
    assert payload["available"] is True
    assert payload["actual_execution"]["model_calls"] == 1


def test_invalid_configured_evidence_returns_422(monkeypatch, tmp_path):
    target = tmp_path / "invalid.json"
    target.write_text("{}")
    monkeypatch.setenv(LIVE_EVIDENCE_ENV, str(target))
    instance = ThreadingHTTPServer(
        ("127.0.0.1", 0), create_studio_request_handler(dict)
    )
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    try:
        with pytest.raises(HTTPError) as raised:
            urlopen(f"http://127.0.0.1:{instance.server_port}/api/hero/live")
        assert raised.value.code == 422
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join()
