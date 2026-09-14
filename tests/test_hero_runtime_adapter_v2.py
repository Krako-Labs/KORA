from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from kora.hero_contracts import (
    HardwareProfile,
    ModelResourceProfile,
    WorkloadRequirements,
)
from kora.hero_planner import build_hero_planning_bundle
from kora.hero_replay import HeroReplayError, replay_hero_events
from kora.hero_runtime_adapter_v2 import (
    AdapterContractError,
    MockRuntimeSession,
    MockScript,
    MockTelemetry,
    adapter_descriptor,
    check_plan_compatibility,
)

NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)
GIB = 1024**3


def inputs(adapter_id="mlx-lm", *, hybrid=False, unknown=False):
    hardware = HardwareProfile(
        profile_id="fixture-hardware",
        captured_at=NOW,
        platform="linux" if hybrid else "darwin",
        architecture="x86_64" if hybrid else "arm64",
        memory_domains=(
            [
                {
                    "domain_id": "ram",
                    "kind": "system",
                    "total_bytes": 32 * GIB,
                    "source": "fixture",
                },
                {
                    "domain_id": "gpu",
                    "kind": "dedicated_gpu",
                    "total_bytes": 8 * GIB,
                    "source": "fixture",
                },
            ]
            if hybrid
            else [
                {
                    "domain_id": "unified",
                    "kind": "unified",
                    "total_bytes": 32 * GIB,
                    "source": "fixture",
                }
            ]
        ),
        runtime_candidates=[adapter_id],
        evidence_level="fixture",
    )
    model = ModelResourceProfile(
        profile_id="fixture-model",
        model_id="mock-model",
        artifact_id="mock-artifact",
        artifact_format="gguf" if adapter_id == "llama.cpp" else "safetensors",
        quantization="fixture",
        artifact_bytes=20 * GIB,
        model_weight_bytes=18 * GIB,
        sha256="a" * 64,
        source_revision="fixture-revision",
        evidence_level="fixture",
    )
    workload = WorkloadRequirements(
        workload_class="source_bounded_chat",
        context_tokens=4096,
        max_output_tokens=64,
        estimated_kv_bytes=None if unknown else GIB,
        runtime_reserve_bytes=GIB,
    )
    bundle = build_hero_planning_bundle(
        run_id="mock-run",
        plan_id="mock-plan",
        occurred_at=NOW,
        hardware=hardware,
        model=model,
        workload=workload,
    )
    return {
        "descriptor": adapter_descriptor(adapter_id, mode="mock"),
        "bundle": bundle,
        "hardware": hardware,
        "model": model,
        "workload": workload,
    }


def session(**kwargs):
    return MockRuntimeSession(**inputs(), **kwargs)


@pytest.mark.parametrize(
    "adapter_id", ["mlx-lm", "llama.cpp", "freetoken", "ktransformers"]
)
def test_default_bindings_are_inert_declarations(adapter_id):
    descriptor = adapter_descriptor(adapter_id)
    assert descriptor.mode == "inert"
    assert descriptor.capability.adapter_id == adapter_id
    assert descriptor.capability.detected is False
    assert "benchmark" in descriptor.unsupported
    assert "physical_telemetry" in descriptor.unsupported


@pytest.mark.parametrize(
    "adapter_id,mode",
    [
        ("mlx_local", "mock"),
        ("frontier_provider", "mock"),
        ("unknown", "mock"),
        ("mlx-lm", "live"),
        ("mlx-lm", "observed"),
    ],
)
def test_unknown_ids_and_live_modes_fail_closed(adapter_id, mode):
    with pytest.raises(AdapterContractError):
        adapter_descriptor(adapter_id, mode=mode)


@pytest.mark.parametrize("adapter_id", ["mlx-lm", "llama.cpp"])
def test_feasible_unified_plan_binds_exact_identity(adapter_id):
    data = inputs(adapter_id)
    result = check_plan_compatibility(**data)
    assert result.compatible
    assert not result.live_execution_allowed
    assert result.runtime_identity["model_artifact_sha256"] == "a" * 64
    assert result.runtime_identity["model_revision"] == "fixture-revision"
    assert result.runtime_identity["planning_digest"] == data["bundle"].evidence_digest
    assert result.runtime_identity["runtime_version"] is None
    assert result.runtime_identity["runtime_version_status"] == "not_probed"


@pytest.mark.parametrize(
    "case,reason",
    [
        ("inert", "inert_binding"),
        ("wrong_adapter", "selected_adapter_mismatch"),
        ("hybrid", "placement_unresolved"),
        ("unknown", "no_selected_runtime"),
        ("changed_model", "planning_evidence_mismatch"),
        ("changed_workload", "planning_evidence_mismatch"),
        ("changed_hardware", "planning_evidence_mismatch"),
        ("tampered_plan", "planning_evidence_mismatch"),
        ("tampered_capability", "planning_evidence_mismatch"),
        ("tampered_event", "planning_evidence_mismatch"),
        ("descriptor", "descriptor_mismatch"),
        ("network", "network_policy_unsupported"),
        ("observed", "fixture_inputs_required"),
    ],
)
def test_compatibility_rejects_unsafe_or_mismatched_binding(case, reason):
    data = (
        inputs("llama.cpp", hybrid=True)
        if case == "hybrid"
        else inputs(unknown=case == "unknown")
    )
    if case == "inert":
        data["descriptor"] = adapter_descriptor("mlx-lm")
    elif case == "wrong_adapter":
        data["descriptor"] = adapter_descriptor("llama.cpp", mode="mock")
    elif case == "changed_model":
        data["model"].sha256 = "b" * 64
    elif case == "changed_workload":
        data["workload"].context_tokens += 1
    elif case == "changed_hardware":
        data["hardware"].memory_domains[0].total_bytes += 1
    elif case == "tampered_plan":
        data["bundle"].plan.effective_config["command"] = "forbidden"
    elif case == "tampered_capability":
        data["bundle"].capabilities[0].supported_platforms.append("linux")
    elif case == "tampered_event":
        data["bundle"].events[0].payload["execution_performed"] = True
    elif case == "descriptor":
        data["descriptor"].capability.detected = True
    elif case in {"network", "observed"}:
        if case == "network":
            data["workload"].allow_network = True
        else:
            data["hardware"].evidence_level = "observed"
            data["model"].evidence_level = "observed"
        data["bundle"] = build_hero_planning_bundle(
            run_id="mock-run",
            plan_id="mock-plan",
            occurred_at=NOW,
            hardware=data["hardware"],
            model=data["model"],
            workload=data["workload"],
        )
    compatibility = check_plan_compatibility(**data)
    assert not compatibility.compatible
    assert reason in compatibility.reason_codes
    assert compatibility.runtime_identity is None
    with pytest.raises(AdapterContractError):
        MockRuntimeSession(**data)


def test_constructor_revalidates_bypassed_model_validation():
    data = inputs()
    data["model"] = data["model"].model_copy(update={"sha256": "invalid"})
    with pytest.raises(ValidationError):
        MockRuntimeSession(**data)


def test_success_keeps_acceptance_and_physical_measurements_unmeasured():
    adapter = session(script=MockScript(output="Fixture only"))
    assert adapter.probe()["host_probe_performed"] is False
    assert adapter.health()["live_ready"] is False
    adapter.load()
    assert adapter.state == "prepared"
    adapter.execute()
    assert adapter.state == "running"
    result = adapter.finish()
    assert result["output"] == "Fixture only"
    assert result["service_acceptance"] == "not_measured"
    assert result["semantic_non_regression"] == "not_measured"
    assert result["accepted_outcome"] is False
    assert result["telemetry"]["peak_gpu_bytes"] is None
    assert result["actual_model_calls"] == result["actual_provider_calls"] == 0
    assert result["runtime_started"] is False
    adapter.cleanup()
    assert adapter.state == "closed"
    assert not adapter.health()["mock_allocation_retained"]
    assert adapter.result() == result
    snapshot = adapter.snapshot()
    adapter.cleanup()
    assert adapter.snapshot() == snapshot


@pytest.mark.parametrize("stage", ["new", "prepared", "running"])
def test_cancellation_at_each_active_stage_prevents_late_output(stage):
    adapter = session()
    if stage in {"prepared", "running"}:
        adapter.load()
    if stage == "running":
        adapter.execute()
    adapter.cancel()
    snapshot = adapter.snapshot()
    adapter.cancel()
    assert adapter.snapshot() == snapshot
    for operation in [adapter.execute, adapter.finish, adapter.load, adapter.result]:
        with pytest.raises(AdapterContractError):
            operation()
    adapter.cleanup()
    assert adapter.state == "closed"
    assert adapter.snapshot()["outcome"] == "cancelled"
    assert not adapter.health()["mock_allocation_retained"]


@pytest.mark.parametrize("operation", ["load", "execute", "finish"])
def test_partial_failure_requires_cleanup_and_retains_failure(operation):
    adapter = session(script=MockScript(fail_at=operation))
    adapter.load()
    if operation in {"execute", "finish"}:
        adapter.execute()
    if operation == "finish":
        assert adapter.finish() is None
    assert adapter.state == "failed"
    assert adapter.health()["mock_allocation_retained"]
    with pytest.raises(AdapterContractError):
        adapter.execute()
    adapter.cleanup()
    assert adapter.snapshot()["outcome"] == "failed"
    assert not adapter.health()["mock_allocation_retained"]
    assert not replay_hero_events(adapter.events_after()).accepted_outcome


def test_cleanup_failure_is_visible_and_can_be_retried():
    adapter = session(script=MockScript(fail_at="cleanup"))
    adapter.load()
    adapter.cancel()
    adapter.cleanup()
    assert adapter.state == "cleanup_failed"
    assert adapter.health()["mock_allocation_retained"]
    with pytest.raises(AdapterContractError):
        adapter.load()
    adapter.cleanup()
    assert adapter.state == "closed"
    assert not adapter.health()["mock_allocation_retained"]
    events = adapter.events_after()
    assert events[-2].event_type == "adapter.cleanup.failed"
    assert events[-1].event_type == "adapter.cleaned"
    assert adapter.snapshot()["outcome"] == "cancelled"


@pytest.mark.parametrize("method", ["execute", "finish", "result"])
def test_invalid_order_is_atomic(method):
    adapter = session()
    before = adapter.snapshot()
    with pytest.raises(AdapterContractError):
        getattr(adapter, method)()
    assert adapter.snapshot() == before


def test_running_cleanup_requires_cancellation_and_closed_reuse_is_rejected():
    adapter = session()
    adapter.load()
    adapter.execute()
    before = adapter.snapshot()
    with pytest.raises(AdapterContractError):
        adapter.cleanup()
    assert adapter.snapshot() == before
    adapter.cancel()
    adapter.cleanup()
    for method in ["load", "execute", "finish", "cancel"]:
        with pytest.raises(AdapterContractError):
            getattr(adapter, method)()


@pytest.mark.parametrize(
    "field,value",
    [
        ("input_tokens", -1),
        ("output_tokens", True),
        ("peak_host_bytes", 1.5),
        ("peak_gpu_bytes", "42"),
        ("load_ms", float("nan")),
        ("ttft_ms", float("inf")),
        ("end_to_end_ms", -1.0),
        ("evidence_level", "observed"),
        ("unknown_metric", 1),
    ],
)
def test_telemetry_invalid_values_fail_closed(field, value):
    with pytest.raises(ValidationError):
        MockTelemetry(**{field: value})


def test_telemetry_is_scripted_not_interpolated():
    telemetry = MockTelemetry(
        output_tokens=0, peak_gpu_bytes=1234, load_ms=2.5, end_to_end_ms=8.0
    )
    adapter = session(script=MockScript(telemetry=telemetry))
    adapter.load()
    adapter.execute()
    result = adapter.finish()
    sampled = [e for e in adapter.events_after() if e.event_type == "telemetry.sampled"]
    assert len(sampled) == 1
    assert sampled[0].payload["telemetry"] == result["telemetry"]
    assert result["telemetry"]["input_tokens"] is None
    assert result["telemetry"]["output_tokens"] == 0
    assert sampled[0].evidence_level == "fixture"


def test_canonical_replay_reconnect_and_snapshot_isolation():
    adapter = session()
    adapter.load()
    prefix = adapter.events_after()
    cursor = prefix[-1].sequence
    adapter.execute()
    adapter.finish()
    adapter.cleanup()
    events = adapter.events_after()
    restored = replay_hero_events(prefix + adapter.events_after(cursor))
    assert restored == replay_hero_events(events)
    assert restored.model_dump(mode="json") == adapter.snapshot()["log"]["projection"]
    assert restored.accepted_outcome is False
    assert restored.verification_state == "not_started"
    assert restored.tasks == {}
    assert len(restored.unhandled_event_ids) == 4
    assert [e.sequence for e in events] == list(range(len(events)))
    assert len({e.event_id for e in events}) == len(events)
    with pytest.raises(HeroReplayError):
        replay_hero_events(events[:-2] + events[-1:])
    with pytest.raises(HeroReplayError):
        replay_hero_events(events + [events[-1]])
    events[-1].payload["runtime_identity"]["model_revision"] = "mutated"
    adapter.identity["effective_config"]["context_tokens"] = 1
    adapter.snapshot()["log"]["events"][0]["payload"]["execution_performed"] = True
    assert adapter.events_after()[-1].payload["runtime_identity"]["model_revision"] == (
        "fixture-revision"
    )
    assert adapter.identity["effective_config"]["context_tokens"] == 4096
    assert adapter.events_after()[0].payload["execution_performed"] is False


@pytest.mark.parametrize("cursor", [-2, 500, True, 1.5])
def test_invalid_reconnect_cursors_are_rejected(cursor):
    with pytest.raises(AdapterContractError):
        session().events_after(cursor)


@pytest.mark.parametrize("operation", ["benchmark", "calibration", "live_execution"])
def test_execution_extensions_are_explicitly_unsupported(operation):
    with pytest.raises(AdapterContractError, match="operation_unsupported"):
        session().unsupported(operation)


def test_model_and_process_calls_are_absent(monkeypatch):
    import builtins
    import socket
    import subprocess

    real_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        assert not name.startswith(
            ("mlx", "torch", "transformers", "llama_cpp", "kora.adapters.")
        ), name
        return real_import(name, *args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail("external execution attempted")

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(builtins, "open", forbidden)
    adapter = session()
    adapter.load()
    adapter.execute()
    adapter.finish()
    adapter.cleanup()
    assert adapter.state == "closed"


def test_identical_inputs_and_script_produce_identical_events():
    def run():
        adapter = session()
        adapter.load()
        adapter.execute()
        adapter.finish()
        adapter.cleanup()
        return adapter.snapshot()

    assert run() == run()
