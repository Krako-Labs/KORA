from __future__ import annotations

from datetime import datetime, timezone

import pytest

from kora.adapters.openai_compatible_local import LocalOpenAICompatibleError
from kora.hero_contracts import (
    AcceleratorProfile,
    HardwareProfile,
    MemoryDomain,
    ModelResourceProfile,
    WorkloadRequirements,
)
from kora.hero_live_execution import (
    LIVE_DRAFT_SCHEMA,
    LiveExecutionConfig,
    LiveExecutionError,
    LiveServiceRequest,
    run_live_execution,
    write_live_evidence,
)
from kora.hero_planner import build_hero_planning_bundle
from kora.hero_replay import replay_hero_events

MODEL_SHA = "0" * 64
RUNTIME_SHA = "1" * 64


def service() -> LiveServiceRequest:
    return LiveServiceRequest(
        request_id="hero-s02-test",
        facts=(
            "The service runs on user-owned hardware.",
            "The endpoint is loopback-only.",
            "The result records objective checks.",
        ),
        approved_fragment="Private by default. Evidence before claims.",
        allowed_headlines=("Private AI, visible evidence",),
        allowed_audiences=("Teams operating AI on owned hardware",),
        allowed_promises=("Run one bounded local draft with traceable evidence.",),
        approved_proof_points=(
            "Runs on user-owned hardware.",
            "Uses a loopback-only endpoint.",
            "Records objective checks and cleanup.",
        ),
        required_caveats=(
            "Semantic quality was not measured.",
            "Production behavior was not measured.",
        ),
        prohibited_claims=("2x", "3x", "production proven"),
    )


def config(**updates) -> LiveExecutionConfig:
    values = {
        "endpoint": "http://127.0.0.1:8796",
        "model_name": "qwen-test",
        "runtime_id": "llama-test",
        "runtime_version": "build-test",
        "runtime_binary_sha256": RUNTIME_SHA,
        "model_artifact_sha256": MODEL_SHA,
        "max_output_tokens": 256,
        "max_model_calls": 2,
        "timeout_s": 30,
        "live_window_s": 1200,
    }
    values.update(updates)
    return LiveExecutionConfig(**values)


def inputs(*, model_sha: str = MODEL_SHA):
    hardware = HardwareProfile(
        profile_id="observed-mac",
        captured_at=datetime(2026, 9, 14, tzinfo=timezone.utc),
        platform="Darwin",
        architecture="arm64",
        memory_domains=[
            MemoryDomain(
                domain_id="unified:0",
                kind="unified",
                total_bytes=128 * 1024**3,
                source="sysctl.hw.memsize",
                evidence_ref="probe:sysctl.hw.memsize",
            )
        ],
        accelerators=[
            AcceleratorProfile(
                accelerator_id="gpu:0",
                vendor="Apple",
                product="Apple M3 Max",
                memory_domain_id="unified:0",
            )
        ],
        runtime_candidates=["llama.cpp"],
        evidence_level="observed",
        evidence_refs=["probe:physical_memory_bytes"],
    )
    model = ModelResourceProfile(
        profile_id="observed-model",
        model_id="qwen-test",
        artifact_id="qwen.gguf",
        artifact_format="gguf",
        quantization="Q4_K_M",
        artifact_bytes=18 * 1024**3,
        model_weight_bytes=18 * 1024**3,
        sha256=model_sha,
        source_revision="local-verified",
        evidence_level="observed",
        tensor_inventory_ref="sha256:" + "2" * 64,
        unknown_fields=["exact_tensor_weight_bytes"],
    )
    workload = WorkloadRequirements(
        workload_class="source_bounded_launch_brief",
        context_tokens=4096,
        max_output_tokens=256,
        estimated_kv_bytes=1024**3,
        runtime_reserve_bytes=4 * 1024**3,
        allow_network=False,
    )
    bundle = build_hero_planning_bundle(
        run_id="hero-s02-test-run",
        plan_id="hero-s02-test-plan",
        occurred_at=datetime(2026, 9, 14, tzinfo=timezone.utc),
        hardware=hardware,
        model=model,
        workload=workload,
    )
    assert bundle.plan.selected_adapter_id == "llama.cpp"
    return bundle, hardware, model, workload


def valid_output():
    return {
        "headline": "Private AI, visible evidence",
        "audience": "Teams operating AI on owned hardware",
        "promise": "Run one bounded local draft with traceable evidence.",
        "proof_points": [
            "Runs on user-owned hardware.",
            "Uses a loopback-only endpoint.",
            "Records objective checks and cleanup.",
        ],
        "caveats": [
            "Semantic quality was not measured.",
            "Production behavior was not measured.",
        ],
    }


class FakeController:
    def __init__(self, *, cleanup_success=True, fail_probe=None, fail_start=None):
        self.cleanup_success = cleanup_success
        self.fail_probe = fail_probe
        self.fail_start = fail_start
        self.stop_calls = 0

    def probe(self):
        if self.fail_probe:
            raise LiveExecutionError(self.fail_probe)
        return {
            "runtime_version": "build-test",
            "runtime_binary_sha256": RUNTIME_SHA,
            "model_artifact_sha256": MODEL_SHA,
            "network": "loopback",
        }

    def start(self):
        if self.fail_start:
            raise LiveExecutionError(self.fail_start)
        return {**self.probe(), "runtime_started": True, "runtime_starts": 1}

    def stop(self):
        self.stop_calls += 1
        return {
            "cleanup_success": self.cleanup_success,
            "runtime_was_started": True,
            "peak_process_rss_bytes": 123456,
            "rss_sample_count": 4,
            "rss_method": "fixture sampler",
        }


class FakeAdapter:
    def __init__(self, outcomes, *, tokens_out=30):
        self.outcomes = outcomes
        self.tokens_out = tokens_out

    def cache_identity(self):
        return {
            "endpoint": "http://127.0.0.1:8796",
            "model": "qwen-test",
            "runtime_id": "llama-test",
        }

    def run(self, **kwargs):
        schema = kwargs["output_schema"]
        assert schema["required"] == LIVE_DRAFT_SCHEMA["required"]
        assert schema["properties"]["headline"]["enum"] == [
            "Private AI, visible evidence"
        ]
        assert schema["properties"]["proof_points"]["uniqueItems"] is True
        assert kwargs["budget"]["max_tokens"] == 256
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return {
            "ok": True,
            "output": outcome,
            "usage": {
                "time_ms": 10,
                "tokens_in": 20,
                "tokens_out": self.tokens_out,
            },
            "meta": {
                "network": "loopback",
                "provider": "local",
                "remote_provider_calls": 0,
                "model_calls": 1,
            },
        }


def execute(
    outcomes, *, controller=None, cancelled=lambda: False, cfg=None, tokens_out=30
):
    bundle, hardware, model, workload = inputs()
    adapter = FakeAdapter(outcomes, tokens_out=tokens_out)
    result = run_live_execution(
        bundle=bundle,
        hardware=hardware,
        model=model,
        workload=workload,
        service=service(),
        config=cfg or config(),
        controller=controller or FakeController(),
        adapter_factory=lambda: adapter,
        cancelled=cancelled,
    )
    return result


def event_types(result):
    return [event["event_type"] for event in result["event_log"]["events"]]


def test_live_success_binds_output_usage_cleanup_and_replay():
    controller = FakeController()
    result = execute([valid_output()], controller=controller)
    assert result["verification"] == {
        "accepted_outcome": True,
        "service_acceptance": "objective_pass",
        "semantic_non_regression": "not_measured",
        "failure_code": None,
    }
    assert result["actual_execution"] == {
        "runtime_starts": 1,
        "model_calls": 1,
        "provider_calls": 0,
        "live_window_ms": result["actual_execution"]["live_window_ms"],
    }
    assert result["output"] == valid_output()
    assert result["cleanup"]["cleanup_success"] is True
    assert result["B_local_execution"]["peak_process_rss_bytes"] == 123456
    assert controller.stop_calls == 1
    projection = replay_hero_events(result["event_log"]["events"])
    assert projection.accepted_outcome is True
    assert projection.tasks["review"].state == "completed"
    assert "adapter.cleaned" in event_types(result)


def test_one_malformed_output_retries_same_plan_then_succeeds():
    result = execute(
        [
            LocalOpenAICompatibleError("local model returned invalid JSON output"),
            valid_output(),
        ]
    )
    assert result["actual_execution"]["model_calls"] == 2
    assert result["verification"]["accepted_outcome"] is True
    assert event_types(result).count("run.replanned") == 1
    draft_events = [
        event
        for event in result["event_log"]["events"]
        if event.get("task_id") == "draft" and event["event_type"] == "task.started"
    ]
    assert [event["attempt"] for event in draft_events] == [1, 2]


def test_retry_exhaustion_emits_escalation_and_stops():
    invalid = LocalOpenAICompatibleError("local model returned invalid JSON output")
    result = execute([invalid, invalid])
    assert result["verification"]["accepted_outcome"] is False
    assert result["verification"]["failure_code"] == "malformed_output"
    assert result["actual_execution"]["model_calls"] == 2
    assert event_types(result)[-3:] == [
        "escalation.required",
        "run.escalated",
        "adapter.cleaned",
    ]


@pytest.mark.parametrize(
    ("outcome", "code"),
    [
        (
            LocalOpenAICompatibleError(
                "local OpenAI-compatible request failed: TimeoutError"
            ),
            "runtime_request_failed",
        ),
        (
            {**valid_output(), "promise": "An unsupported promise."},
            "promise_not_supplied",
        ),
    ],
)
def test_timeout_and_unsupported_output_do_not_retry(outcome, code):
    result = execute([outcome])
    assert result["verification"]["failure_code"] == code
    assert result["actual_execution"]["model_calls"] == 1
    assert "run.replanned" not in event_types(result)


def test_cancellation_stops_before_model_call_and_cleans_up():
    result = execute([], cancelled=lambda: True)
    assert result["verification"]["failure_code"] == "cancelled"
    assert result["actual_execution"]["model_calls"] == 0
    assert result["cleanup"]["cleanup_success"] is True


def test_model_identity_mismatch_fails_before_runtime_start():
    bundle, hardware, model, workload = inputs(model_sha="3" * 64)
    result = run_live_execution(
        bundle=bundle,
        hardware=hardware,
        model=model,
        workload=workload,
        service=service(),
        config=config(),
        controller=FakeController(),
        adapter_factory=lambda: FakeAdapter([valid_output()]),
    )
    assert result["verification"]["failure_code"] == "live_plan_or_identity_mismatch"
    assert result["actual_execution"]["model_calls"] == 0
    assert result["actual_execution"]["runtime_starts"] == 0


def test_cleanup_failure_prevents_task_completion_and_acceptance():
    result = execute([valid_output()], controller=FakeController(cleanup_success=False))
    assert result["verification"]["failure_code"] == "cleanup_failed"
    assert result["verification"]["accepted_outcome"] is False
    assert "task.completed" not in [
        event["event_type"]
        for event in result["event_log"]["events"]
        if event.get("task_id") == "draft"
    ]


def test_reported_output_token_overrun_fails_closed_without_retry():
    result = execute([valid_output()], tokens_out=257)
    assert result["verification"]["failure_code"] == "output_token_budget_exceeded"
    assert result["verification"]["accepted_outcome"] is False
    assert result["actual_execution"]["model_calls"] == 1
    assert "run.replanned" not in event_types(result)


def test_probe_and_start_failures_are_retained_and_cleanup_runs():
    for code, controller in (
        (
            "runtime_identity_mismatch",
            FakeController(fail_probe="runtime_identity_mismatch"),
        ),
        (
            "runtime_readiness_timeout",
            FakeController(fail_start="runtime_readiness_timeout"),
        ),
    ):
        result = execute([valid_output()], controller=controller)
        assert result["verification"]["failure_code"] == code
        assert result["verification"]["accepted_outcome"] is False
        assert controller.stop_calls == 1


def test_config_rejects_remote_endpoint_and_budget_expansion():
    with pytest.raises(ValueError, match="loopback"):
        config(endpoint="https://example.com")
    with pytest.raises(ValueError):
        config(max_output_tokens=257)
    with pytest.raises(ValueError):
        config(max_model_calls=4)
    with pytest.raises(ValueError):
        config(live_window_s=1201)


def test_write_live_evidence_is_bounded_to_the_declared_schema(tmp_path):

    result = execute([valid_output()])
    target = write_live_evidence(tmp_path / "evidence.json", result)
    assert target.read_text().endswith("\n")
    with pytest.raises(LiveExecutionError, match="invalid_live_evidence_schema"):
        write_live_evidence(tmp_path / "bad.json", {"schema_version": "wrong"})
