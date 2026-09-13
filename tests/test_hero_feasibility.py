from __future__ import annotations

from datetime import datetime, timezone

from kora.hero_contracts import (
    AcceleratorProfile,
    HardwareProfile,
    MemoryDomain,
    ModelResourceProfile,
    RuntimeCapability,
    WorkloadRequirements,
)
from kora.hero_feasibility import build_execution_plan, evaluate_candidate


NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)
GIB = 1024**3


def model() -> ModelResourceProfile:
    return ModelResourceProfile(
        profile_id="model-profile",
        model_id="candidate",
        artifact_id="candidate-q4",
        artifact_format="gguf",
        quantization="Q4_K_M",
        artifact_bytes=20 * GIB,
        model_weight_bytes=18 * GIB,
        sha256="b" * 64,
        source_revision="fixture-revision",
        evidence_level="fixture",
    )


def pc() -> HardwareProfile:
    return HardwareProfile(
        profile_id="pc",
        captured_at=NOW,
        platform="linux",
        architecture="x86_64",
        memory_domains=[
            MemoryDomain(
                domain_id="ram",
                kind="system",
                total_bytes=32 * GIB,
                source="fixture",
            ),
            MemoryDomain(
                domain_id="vram",
                kind="dedicated_gpu",
                total_bytes=8 * GIB,
                source="fixture",
            ),
        ],
        accelerators=[
            AcceleratorProfile(
                accelerator_id="gpu",
                vendor="nvidia",
                product="fixture",
                memory_domain_id="vram",
            )
        ],
        runtime_candidates=["llama_cpp"],
        evidence_level="fixture",
    )


def workload(*, complete_estimates: bool = True) -> WorkloadRequirements:
    return WorkloadRequirements(
        workload_class="source_bounded_brief",
        context_tokens=4096,
        max_output_tokens=768,
        estimated_kv_bytes=1 * GIB if complete_estimates else None,
        runtime_reserve_bytes=2 * GIB if complete_estimates else None,
    )


def llama_cpp() -> RuntimeCapability:
    return RuntimeCapability(
        adapter_id="llama_cpp",
        executor_class="local_ai",
        supported_platforms=["linux", "darwin", "windows"],
        supported_architectures=["x86_64", "arm64"],
        supported_artifact_formats=["gguf"],
        memory_modes=["gpu_resident", "hybrid_cpu_gpu"],
        detected=True,
        evidence_level="fixture",
    )


def test_hybrid_candidate_can_be_planned_without_claiming_gpu_resident_fit() -> None:
    decision = evaluate_candidate(llama_cpp(), pc(), model(), workload())

    assert decision.feasibility == "yes"
    assert decision.reason_codes == [
        "hybrid_host_capacity_satisfied",
        "placement_requires_runtime_plan",
    ]
    assert decision.estimated_peak_bytes == {"system": 21 * GIB}


def test_unknown_runtime_overhead_fails_closed() -> None:
    decision = evaluate_candidate(
        llama_cpp(),
        pc(),
        model(),
        workload(complete_estimates=False),
    )

    assert decision.feasibility == "unknown"
    assert decision.rejected is True
    assert decision.reason_codes == ["kv_or_runtime_reserve_unknown"]


def test_missing_runtime_is_not_selected() -> None:
    capability = llama_cpp().model_copy(update={"detected": False})
    plan = build_execution_plan(
        plan_id="plan",
        hardware=pc(),
        model=model(),
        workload=workload(),
        capabilities=[capability],
        adapter_priority=["llama_cpp"],
    )

    assert plan.selected_adapter_id is None
    assert plan.candidates[0].reason_codes == ["runtime_not_detected"]
    assert plan.expert_overrides_required is False


def test_priority_selection_is_deterministic() -> None:
    challenger = llama_cpp().model_copy(update={"adapter_id": "challenger"})
    arguments = {
        "plan_id": "plan",
        "hardware": pc(),
        "model": model(),
        "workload": workload(),
        "capabilities": [challenger, llama_cpp()],
        "adapter_priority": ["llama_cpp", "challenger"],
    }

    first = build_execution_plan(**arguments)
    second = build_execution_plan(**arguments)

    assert first.model_dump(mode="json") == second.model_dump(mode="json")
    assert first.selected_adapter_id == "llama_cpp"
    assert "execution must be measured separately" in first.explanation[-1]


def test_network_disallowed_rejects_frontier_candidate() -> None:
    frontier = RuntimeCapability(
        adapter_id="frontier",
        executor_class="frontier_ai",
        supported_platforms=["*"],
        supported_architectures=["*"],
        supported_artifact_formats=["gguf"],
        memory_modes=["hybrid_cpu_gpu"],
        detected=True,
        evidence_level="fixture",
    )

    decision = evaluate_candidate(frontier, pc(), model(), workload())

    assert decision.feasibility == "no"
    assert decision.reason_codes == ["network_disallowed"]


def test_gpu_resident_only_candidate_rejects_oversized_artifact() -> None:
    resident = llama_cpp().model_copy(update={"memory_modes": ["gpu_resident"]})

    decision = evaluate_candidate(resident, pc(), model(), workload())

    assert decision.feasibility == "no"
    assert decision.reason_codes == ["dedicated_gpu_capacity_insufficient"]
    assert decision.estimated_peak_bytes["dedicated_gpu"] == 21 * GIB
