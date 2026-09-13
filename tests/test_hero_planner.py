from __future__ import annotations

import json
from datetime import datetime, timezone

from kora.hero_contracts import (
    AcceleratorProfile,
    HardwareProfile,
    MemoryDomain,
    ModelResourceProfile,
    WorkloadRequirements,
)
from kora.hero_planner import build_hero_planning_bundle, write_planning_evidence
from kora.hero_replay import replay_hero_events

NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)
GIB = 1024**3


def apple_profile() -> HardwareProfile:
    return HardwareProfile(
        profile_id="apple-profile",
        captured_at=NOW,
        platform="Darwin",
        architecture="arm64",
        memory_domains=[
            MemoryDomain(
                domain_id="unified:0",
                kind="unified",
                total_bytes=32 * GIB,
                source="fixture",
                evidence_ref="fixture:memory",
            )
        ],
        accelerators=[
            AcceleratorProfile(
                accelerator_id="gpu:0",
                vendor="Apple",
                product="Apple fixture",
                memory_domain_id="unified:0",
            )
        ],
        runtime_candidates=["mlx-lm", "llama.cpp"],
        evidence_level="fixture",
        evidence_refs=["fixture:hardware"],
    )


def pc_profile() -> HardwareProfile:
    return HardwareProfile(
        profile_id="pc-profile",
        captured_at=NOW,
        platform="linux",
        architecture="x86_64",
        memory_domains=[
            MemoryDomain(
                domain_id="system:0",
                kind="system",
                total_bytes=32 * GIB,
                source="fixture",
            ),
            MemoryDomain(
                domain_id="dedicated_gpu:0",
                kind="dedicated_gpu",
                total_bytes=8 * GIB,
                source="fixture",
            ),
        ],
        accelerators=[
            AcceleratorProfile(
                accelerator_id="gpu:0",
                vendor="NVIDIA",
                product="fixture",
                memory_domain_id="dedicated_gpu:0",
            )
        ],
        runtime_candidates=["llama.cpp"],
        evidence_level="fixture",
    )


def model(*, artifact_format: str = "gguf") -> ModelResourceProfile:
    return ModelResourceProfile(
        profile_id="model-profile",
        model_id="fixture-model",
        artifact_id="fixture-artifact",
        artifact_format=artifact_format,
        quantization="fixture-quantization",
        artifact_bytes=20 * GIB,
        model_weight_bytes=18 * GIB,
        sha256="a" * 64,
        source_revision="fixture-revision",
        evidence_level="fixture",
        tensor_inventory_ref="fixture:tensors",
    )


def workload(*, complete: bool = True) -> WorkloadRequirements:
    return WorkloadRequirements(
        workload_class="source_bounded_chat",
        context_tokens=4096,
        max_output_tokens=768,
        estimated_kv_bytes=1 * GIB if complete else None,
        runtime_reserve_bytes=2 * GIB if complete else None,
    )


def build(
    hardware: HardwareProfile,
    *,
    resource: ModelResourceProfile | None = None,
    requirements: WorkloadRequirements | None = None,
):
    return build_hero_planning_bundle(
        run_id="run-fixture",
        plan_id="plan-fixture",
        occurred_at=NOW,
        hardware=hardware,
        model=resource or model(),
        workload=requirements or workload(),
    )


def test_apple_bundle_selects_mlx_for_safetensors_without_execution() -> None:
    bundle = build(apple_profile(), resource=model(artifact_format="safetensors"))

    assert bundle.plan.selected_adapter_id == "mlx-lm"
    assert bundle.plan.executor_class == "local_ai"
    assert bundle.plan.constraints == [
        "no_runtime_started",
        "no_provider_fallback",
        "unknown_memory_overhead_fails_closed",
    ]
    plan_event = bundle.events[3]
    assert plan_event.event_type == "execution.plan.created"
    assert plan_event.payload["runtime_started"] is False
    assert plan_event.payload["selected_adapter_id"] == "mlx-lm"


def test_pc_bundle_selects_hybrid_llama_cpp_but_not_gpu_resident_claim() -> None:
    bundle = build(pc_profile())
    decision = next(
        item for item in bundle.plan.candidates if item.adapter_id == "llama.cpp"
    )

    assert bundle.plan.selected_adapter_id == "llama.cpp"
    assert decision.reason_codes == [
        "hybrid_host_capacity_satisfied",
        "placement_requires_runtime_plan",
    ]
    assert decision.estimated_peak_bytes == {"system": 21 * GIB}
    assert "execution must be measured separately" in bundle.plan.explanation[-1]


def test_unknown_overhead_fails_closed_and_remains_visible_in_event() -> None:
    bundle = build(pc_profile(), requirements=workload(complete=False))

    assert bundle.plan.selected_adapter_id is None
    assert all(item.rejected for item in bundle.plan.candidates)
    decisions = bundle.events[3].payload["candidate_decisions"]
    assert any(
        item["reason_codes"] == ["kv_or_runtime_reserve_unknown"]
        for item in decisions
    )


def test_planning_bundle_is_deterministic_for_frozen_inputs() -> None:
    first = build(pc_profile())
    second = build(pc_profile())

    assert first.model_dump(mode="json") == second.model_dump(mode="json")
    assert first.evidence_digest == second.evidence_digest


def test_planning_events_replay_without_unknown_or_execution_state() -> None:
    bundle = build(pc_profile())

    projection = replay_hero_events(bundle.events)

    assert projection.run_state == "running"
    assert projection.last_sequence == 4
    assert projection.unhandled_event_ids == []
    assert projection.accepted_outcome is False
    assert f"sha256:{bundle.evidence_digest}" in projection.evidence_refs


def test_events_link_profiles_inventory_and_sealed_digest() -> None:
    bundle = build(apple_profile(), resource=model(artifact_format="safetensors"))

    assert bundle.events[0].evidence_refs == (
        "profile:hardware:apple-profile",
        "profile:model:model-profile",
        "fixture:hardware",
        "fixture:memory",
        "fixture:tensors",
    )
    assert bundle.events[-1].evidence_refs[-1] == f"sha256:{bundle.evidence_digest}"


def test_evidence_writer_emits_human_readable_claim_bounded_json(tmp_path) -> None:
    bundle = build(pc_profile())
    target = tmp_path / "planning-evidence.json"

    returned = write_planning_evidence(target, bundle=bundle)
    payload = json.loads(target.read_text())

    assert returned == target
    assert payload["evidence_digest"] == bundle.evidence_digest
    assert payload["plan"]["selected_adapter_id"] == "llama.cpp"
    assert "Planning evidence only" in payload["claim_boundary"]
    assert list(tmp_path.glob(".*.tmp")) == []
