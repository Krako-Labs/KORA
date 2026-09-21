from __future__ import annotations

import hashlib
import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

from kora.studio_inference_execution import (
    INFERENCE_EXECUTION_EVIDENCE_ENV,
    StudioInferenceExecutionEvidenceError,
    inference_execution_payload,
    load_inference_execution_evidence,
)
from kora.studio_server import create_studio_request_handler


def _canonical_json(value):
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _events():
    names = [
        ("workload.classified", {"classification": "NEW"}),
        ("model.intelligence.started", {}),
        ("model.intelligence.completed", {}),
        ("compile.observation.accepted", {}),
        ("compile.candidate.created", {}),
        ("compile.validation.started", {}),
        ("compile.validation.passed", {}),
        ("compile.candidate.activated", {}),
        ("workload.classified", {"classification": "KNOWN"}),
        ("compiled.execution.started", {}),
        ("verification.started", {}),
        ("verification.passed", {}),
        ("compiled.execution.completed", {}),
        ("workload.classified", {"classification": "UNKNOWN"}),
        ("run.paused.safely", {}),
    ]
    return [
        {"sequence": index, "name": name, "payload": payload}
        for index, (name, payload) in enumerate(names, start=1)
    ]


def _evidence():
    events = _events()
    return {
        "schema_version": "kora.inference-execution-studio-evidence.v1",
        "evidence_level": "observed",
        "recorded_at": "2026-09-21T15:00:00+00:00",
        "claim_boundary": (
            "One bounded observed Inference -> Execution run. "
            "No production or broad speedup claim."
        ),
        "model_identity": {
            "model_repository": "Example/Model",
            "model_revision": "a" * 40,
            "artifact_sha256": "b" * 64,
            "runtime_commit": "c" * 40,
            "quantization": "Q4",
            "context_tokens": 4096,
            "concurrency": 1,
            "prefix_cache": "disabled",
            "thinking": False,
            "tokenizer_sha256": "d" * 64,
            "template_sha256": "e" * 64,
            "verification": "artifact-and-template-hash-verified",
        },
        "model_accounting": {
            "calls": 4,
            "input_tokens": 1000,
            "output_tokens": 400,
            "reasoning_tokens": None,
            "token_source": "engine-reported",
        },
        "candidate": {
            "digest": "f" * 64,
            "automatic_from_live_observations": True,
            "deterministic_repeat_equal": True,
        },
        "activation": {
            "passed": True,
            "raw_overlap_count": 0,
            "normalized_overlap_count": 0,
        },
        "counters": {
            "model_calls": 4,
            "compiled_executions": 3,
            "exact_reuse_hits": 0,
            "unknown_or_ood_escalations": 2,
            "safe_pauses": 1,
            "ood_silent_deterministic_success": 0,
        },
        "timings_ms": {
            "model_intelligence": [2000.0, 1900.0, 1950.0, 1920.0],
            "candidate_generation": [0.5],
            "candidate_validation": [1.0],
            "compiled_execution": [0.001, 0.0011, 0.0009],
            "verification": [0.0008, 0.0007, 0.0007],
            "end_to_end": [0.13, 0.12, 0.12],
        },
        "events": events,
        "event_digest": hashlib.sha256(_canonical_json(events)).hexdigest(),
        "accepted": True,
    }


def _write(tmp_path, payload=None):
    target = tmp_path / "inference-execution.json"
    target.write_text(json.dumps(payload or _evidence()))
    return target


def test_unconfigured_view_is_disabled_without_discovery():
    view = inference_execution_payload(environ={})
    assert view["available"] is False
    assert view["status"] == "not_configured"


def test_valid_evidence_loads_and_path_is_not_exposed(tmp_path):
    target = _write(tmp_path)
    loaded = load_inference_execution_evidence(target)
    assert loaded["accepted"] is True
    view = inference_execution_payload(
        environ={INFERENCE_EXECUTION_EVIDENCE_ENV: str(target)}
    )
    assert view["available"] is True
    assert view["status"] == "objective_pass"
    assert view["model_accounting"]["calls"] == 4
    assert view["counters"]["compiled_executions"] == 3
    assert view["counters"]["exact_reuse_hits"] == 0
    assert "KNOWN — KORA EXECUTION" in view["studio_states"]
    assert "OOD / UNKNOWN — MODEL REQUIRED" in view["studio_states"]
    assert view["event_timeline"][0] == {
        "sequence": 1,
        "event": "workload.classified",
        "state": "NEW",
    }
    assert any(item["state"] == "KNOWN" for item in view["event_timeline"])
    assert all(
        set(item) == {"sequence", "event", "state"} for item in view["event_timeline"]
    )
    assert "payload" not in json.dumps(view["event_timeline"])
    assert str(target) not in json.dumps(view)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value.update(accepted=False),
        lambda value: value["model_accounting"].update(token_source="estimated"),
        lambda value: value["candidate"].update(deterministic_repeat_equal=False),
        lambda value: value["activation"].update(raw_overlap_count=1),
        lambda value: value["counters"].update(exact_reuse_hits=1),
        lambda value: value["counters"].update(ood_silent_deterministic_success=1),
        lambda value: value["events"][0].update(sequence=2),
        lambda value: value["events"][0].update(name="unsupported.event"),
        lambda value: value.update(event_digest="0" * 64),
    ],
)
def test_contract_violations_fail_closed(tmp_path, mutate):
    payload = _evidence()
    mutate(payload)
    with pytest.raises(StudioInferenceExecutionEvidenceError):
        load_inference_execution_evidence(_write(tmp_path, payload))


def test_sensitive_raw_request_field_is_rejected(tmp_path):
    payload = _evidence()
    payload["events"][0]["payload"]["raw_request"] = "private text"
    payload["event_digest"] = hashlib.sha256(
        _canonical_json(payload["events"])
    ).hexdigest()
    with pytest.raises(
        StudioInferenceExecutionEvidenceError, match="forbidden field"
    ):
        load_inference_execution_evidence(_write(tmp_path, payload))


def test_private_local_path_is_rejected(tmp_path):
    payload = _evidence()
    payload["claim_boundary"] = "/Users/example/private"
    with pytest.raises(
        StudioInferenceExecutionEvidenceError, match="private local path"
    ):
        load_inference_execution_evidence(_write(tmp_path, payload))


def test_symlink_is_rejected(tmp_path):
    target = _write(tmp_path)
    link = tmp_path / "link.json"
    link.symlink_to(target)
    with pytest.raises(
        StudioInferenceExecutionEvidenceError, match="non-symlink"
    ):
        load_inference_execution_evidence(link)


@pytest.fixture
def server(monkeypatch, tmp_path):
    target = _write(tmp_path)
    monkeypatch.setenv(INFERENCE_EXECUTION_EVIDENCE_ENV, str(target))

    def no_probe():
        raise AssertionError("read-only evidence route must not probe the host")

    instance = ThreadingHTTPServer(
        ("127.0.0.1", 0), create_studio_request_handler(no_probe)
    )
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{instance.server_port}"
    instance.shutdown()
    instance.server_close()
    thread.join()


def test_http_page_asset_and_evidence_route(server):
    with urlopen(server + "/inference-execution") as response:
        html = response.read().decode()
        assert "INFERENCE → EXECUTION" in html
        assert "OBSERVED EVIDENCE · READ ONLY" in html
    with urlopen(server + "/hero-assets/inference-execution.js") as response:
        javascript = response.read()
        assert b"/api/inference-execution" in javascript
        assert b"replay-next" in javascript
        assert b"evidence-reload" in javascript
        assert b"setTimeout" not in javascript
        assert b"setInterval" not in javascript
    with urlopen(server + "/api/inference-execution") as response:
        payload = json.load(response)
    assert payload["available"] is True
    assert payload["model_accounting"]["calls"] == 4
    assert payload["counters"]["compiled_executions"] == 3
    assert payload["event_timeline"][-1] == {
        "sequence": 15,
        "event": "run.paused.safely",
        "state": "MODEL OFFLINE — TASK PAUSED SAFELY",
    }


def test_invalid_configured_evidence_returns_422(monkeypatch, tmp_path):
    target = tmp_path / "invalid.json"
    target.write_text("{}")
    monkeypatch.setenv(INFERENCE_EXECUTION_EVIDENCE_ENV, str(target))
    instance = ThreadingHTTPServer(
        ("127.0.0.1", 0), create_studio_request_handler(dict)
    )
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    try:
        with pytest.raises(HTTPError) as raised:
            urlopen(
                f"http://127.0.0.1:{instance.server_port}/api/inference-execution"
            )
        assert raised.value.code == 422
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join()
