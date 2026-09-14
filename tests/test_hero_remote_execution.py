from datetime import datetime, timedelta, timezone

import pytest

from kora.hero_live_execution import LiveExecutionError, LiveServiceRequest, _digest
from kora.hero_remote_execution import (
    FileIdentity,
    RemoteConfig,
    VllmController,
    run_remote_execution,
    validate_lease,
)
from kora.hero_replay import replay_hero_events


def config(**changes):
    values = {
        "approval_id": "test-approval",
        "lease_id": "test-lease",
        "project": "test-project",
        "unit": "test-unit.service",
        "lease_tool": "/test/lease.py",
        "model_dir": "/test/model",
        "model_id": "qwen-test",
        "revision": "test-revision",
        "files": [
            {"name": "model.safetensors", "size": 61_000_000_000, "sha256": "a" * 64}
        ],
        "runtime_files": {"/test/python": "b" * 64},
        "runtime_versions": {"vllm": "test"},
        "python_path": "/test/python",
    }
    values.update(changes)
    return RemoteConfig(**values)


def service():
    return LiveServiceRequest(
        request_id="test-request",
        facts=("Owned hardware.", "Loopback endpoint.", "Bounded checks."),
        approved_fragment="Evidence before claims.",
        allowed_headlines=("Private AI",),
        allowed_audiences=("Teams",),
        allowed_promises=("Bounded execution.",),
        approved_proof_points=(
            "Owned hardware.",
            "Loopback endpoint.",
            "Bounded checks.",
        ),
        required_caveats=("Semantics not measured.", "Production not measured."),
        prohibited_claims=("quality proven",),
    )


def output():
    return {
        "headline": "Private AI",
        "audience": "Teams",
        "promise": "Bounded execution.",
        "proof_points": ["Owned hardware.", "Loopback endpoint.", "Bounded checks."],
        "caveats": ["Semantics not measured.", "Production not measured."],
    }


def response(value=None, finish="stop", tokens=92):
    import json

    return {
        "model": "qwen-test",
        "choices": [
            {
                "finish_reason": finish,
                "message": {"content": json.dumps(value or output())},
            }
        ],
        "usage": {"prompt_tokens": 364, "completion_tokens": tokens},
    }


def status(cfg=None):
    cfg = cfg or config()
    now = datetime.now(timezone.utc)
    return {
        "lease": {
            "lease_id": cfg.lease_id,
            "project": cfg.project,
            "unit": cfg.unit,
            "expected_end": (now + timedelta(minutes=25)).isoformat(),
        },
        "overdue": False,
        "observed": {"sampled_at": now.isoformat(), "processes": []},
    }


class FakeController:
    def __init__(self, responses=None, *, cleanup=True, probe_error=None):
        self.responses = responses if responses is not None else [response()]
        self.cleanup = cleanup
        self.probe_error = probe_error
        self.calls = self.stops = 0

    def probe(self):
        if self.probe_error:
            raise LiveExecutionError(self.probe_error)
        cfg = config()
        return {
            "model_manifest_digest": _digest([e.model_dump() for e in cfg.files]),
            "runtime_digest": "b" * 64,
            "gpu_bytes": 80 * 1024**3,
            "gpu_uuid": "test-gpu",
            "gpu_name": "NVIDIA H100",
            "runtime_versions": {"vllm": "test"},
        }

    def start(self, cancelled):
        if cancelled():
            raise LiveExecutionError("cancelled")

    def call(self, service):
        self.calls += 1
        value = self.responses.pop(0)
        if isinstance(value, Exception):
            raise value
        return value

    def stop(self):
        self.stops += 1
        return {
            "owned_process_stopped": self.cleanup,
            "runtime_started": True,
            "borrowed_service_restoration": "pending_supervisor",
        }


def execute(controller=None, **kwargs):
    return run_remote_execution(
        config(),
        service(),
        controller or FakeController(),
        evidence_level="fixture",
        **kwargs,
    )


def test_success_requires_real_counts_and_keeps_restoration_pending():
    c = FakeController()
    result = execute(c)
    assert result["verification"]["objective_pass"] is True
    assert result["verification"]["service_restoration"] == "pending_supervisor"
    assert result["privacy_mode"] == "private_network"
    assert result["actual_execution"]["owned_remote_model_calls"] == 1
    assert result["actual_execution"]["commercial_provider_calls"] == 0
    assert result["output"] == output()
    assert replay_hero_events(result["event_log"]["events"]).accepted_outcome
    assert c.stops == 1


@pytest.mark.parametrize(
    "field,value",
    [
        ("max_calls", 3),
        ("max_calls", True),
        ("max_tokens", 257),
        ("max_tokens", False),
        ("request_timeout_s", 301),
        ("execution_window_s", 1201),
        ("restoration_reserve_s", 599),
        ("port", 80),
        ("unit", "x.service;id"),
        ("context_tokens", 8192),
    ],
)
def test_budget_and_unit_rejection(field, value):
    with pytest.raises(ValueError):
        config(**{field: value})


@pytest.mark.parametrize("name", ["../model", "/tmp/model", "x/y", ".", "..", ""])
def test_manifest_rejects_path_traversal(name):
    with pytest.raises(ValueError):
        FileIdentity(name=name, size=1, sha256="a" * 64)


def test_duplicate_model_files_rejected():
    cfg = config()
    with pytest.raises(ValueError):
        config(files=[cfg.files[0], cfg.files[0]])


@pytest.mark.parametrize(
    "change", ["foreign", "expired", "stale", "future", "process", "none"]
)
def test_lease_guard_rejects_unsafe_status(change):
    s = status()
    if change == "foreign":
        s["lease"]["lease_id"] = "another"
    if change == "expired":
        s["lease"]["expected_end"] = (
            datetime.now(timezone.utc) + timedelta(minutes=9)
        ).isoformat()
    if change == "stale":
        s["observed"]["sampled_at"] = (
            datetime.now(timezone.utc) - timedelta(seconds=31)
        ).isoformat()
    if change == "future":
        s["observed"]["sampled_at"] = (
            datetime.now(timezone.utc) + timedelta(minutes=1)
        ).isoformat()
    if change == "process":
        s["observed"]["processes"] = [{"service": "other.service"}]
    if change == "none":
        s["lease"] = None
    with pytest.raises(LiveExecutionError):
        validate_lease(config(), s)


def test_exact_lease_accepted_and_clear_guard_rejects_existing_process():
    s = status()
    validate_lease(config(), s)
    s["observed"]["processes"] = [{"service": config().unit}]
    validate_lease(config(), s)
    with pytest.raises(LiveExecutionError):
        validate_lease(config(), s, require_clear=True)


def test_truncation_retry_retains_both_token_samples():
    c = FakeController([response(finish="length", tokens=256), response()])
    result = execute(c)
    assert result["verification"]["objective_pass"]
    assert result["actual_execution"]["owned_remote_model_calls"] == 2
    assert [x["tokens_out"] for x in result["attempts"]] == [256, 92]
    assert (
        sum(e["event_type"] == "run.replanned" for e in result["event_log"]["events"])
        == 1
    )


@pytest.mark.parametrize(
    "kind",
    [
        "truncated",
        "malformed",
        "unsupported",
        "timeout",
        "tokens",
        "cleanup",
        "identity",
    ],
)
def test_failure_retained_and_no_automatic_fallback(kind):
    if kind == "truncated":
        c = FakeController([response(finish="length"), response(finish="length")])
    elif kind == "malformed":
        c = FakeController([response({"bad": "shape"}), response({"bad": "shape"})])
    elif kind == "unsupported":
        c = FakeController([response({**output(), "promise": "Unapproved"})])
    elif kind == "timeout":
        c = FakeController([TimeoutError()])
    elif kind == "tokens":
        c = FakeController([response(tokens=257)])
    elif kind == "cleanup":
        c = FakeController(cleanup=False)
    else:
        c = FakeController(probe_error="model_identity_mismatch")
    r = execute(c)
    assert not r["verification"]["objective_pass"]
    assert not replay_hero_events(r["event_log"]["events"]).accepted_outcome
    assert c.stops == 1
    assert c.calls <= (2 if kind in {"truncated", "malformed"} else 1)


def test_cancel_before_call_and_after_response():
    c = FakeController()
    r = execute(c, cancelled=lambda: True)
    assert c.calls == 0 and r["verification"]["failure_code"] == "cancelled"
    c = FakeController()
    r = execute(c, cancelled=lambda: c.calls > 0)
    assert c.calls == 1 and r["verification"]["failure_code"] == "cancelled"
    assert not r["verification"]["objective_pass"]


def test_launch_has_loopback_offline_bounded_arguments():
    cmd = config().command()
    assert cmd[cmd.index("--host") + 1] == "127.0.0.1"
    assert cmd[cmd.index("--max-num-seqs") + 1] == "1"
    assert cmd[cmd.index("--max-model-len") + 1] == "4096"


def test_model_hash_drift_fails_before_process_start(tmp_path):
    f = tmp_path / "model.safetensors"
    f.write_bytes(b"bad")
    cfg = config(
        model_dir=str(tmp_path), files=[{"name": f.name, "size": 3, "sha256": "a" * 64}]
    )
    c = VllmController(cfg, tmp_path / "runtime.log")
    with pytest.raises(LiveExecutionError, match="model_identity"):
        c.probe()
    assert c.process is None


def test_launch_pins_native_sampler_and_offline_network_environment():
    env = config().launch_environment()
    assert env["VLLM_USE_FLASHINFER_SAMPLER"] == "0"
    assert env["HF_HUB_OFFLINE"] == "1"
    assert env["VLLM_HOST_IP"] == "127.0.0.1"


def test_decoder_compatibility_preserves_independent_uniqueness_validation():
    from kora.hero_live_execution import LiveDraft, _validate_draft
    from kora.hero_remote_execution import decoder_schema

    s = service()
    schema = decoder_schema(s)
    assert "uniqueItems" not in schema["properties"]["proof_points"]
    assert schema["properties"]["proof_points"]["items"]["enum"] == list(
        s.approved_proof_points
    )
    duplicate = output()
    duplicate["proof_points"][1] = duplicate["proof_points"][0]
    assert _validate_draft(LiveDraft.model_validate(duplicate), s)
