from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from kora.hero_contracts import (
    AcceleratorProfile,
    CandidateDecision,
    ExecutionPlan,
    HardwareProfile,
    HeroEvent,
    MemoryDomain,
    ModelResourceProfile,
)


NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)


def test_hardware_profile_rejects_unknown_accelerator_memory_domain() -> None:
    with pytest.raises(ValidationError, match="unknown memory domain"):
        HardwareProfile(
            profile_id="host-1",
            captured_at=NOW,
            platform="linux",
            architecture="x86_64",
            memory_domains=[
                MemoryDomain(
                    domain_id="ram",
                    kind="system",
                    total_bytes=32 * 1024**3,
                    source="os",
                )
            ],
            accelerators=[
                AcceleratorProfile(
                    accelerator_id="gpu-0",
                    vendor="nvidia",
                    product="candidate",
                    memory_domain_id="vram-0",
                )
            ],
            evidence_level="fixture",
        )


def test_verified_model_profile_requires_tensor_inventory() -> None:
    with pytest.raises(ValidationError, match="tensor_inventory_ref"):
        ModelResourceProfile(
            profile_id="model-profile-1",
            model_id="model",
            artifact_id="artifact",
            artifact_format="gguf",
            quantization="Q4_K_M",
            artifact_bytes=20,
            model_weight_bytes=16,
            sha256="a" * 64,
            source_revision="revision",
            evidence_level="verified",
        )


def test_execution_plan_selects_only_a_feasible_non_rejected_candidate() -> None:
    plan = ExecutionPlan(
        plan_id="plan-1",
        hardware_profile_id="host-1",
        model_resource_profile_id="model-1",
        workload_class="source_bounded_brief",
        executor_class="local_ai",
        selected_adapter_id="llama_cpp",
        candidates=[
            CandidateDecision(
                adapter_id="llama_cpp",
                feasibility="yes",
                reason_codes=["hybrid_memory_supported"],
                estimated_peak_bytes={"system": 24},
                rejected=False,
            ),
            CandidateDecision(
                adapter_id="mlx_lm",
                feasibility="no",
                reason_codes=["platform_unsupported"],
                rejected=True,
            ),
        ],
        constraints=["no_network", "quality_gate_required"],
        explanation=["llama.cpp is the only feasible local candidate in this fixture"],
        evidence_level="fixture",
    )

    assert plan.selected_adapter_id == "llama_cpp"

    with pytest.raises(ValidationError, match="feasible non-rejected"):
        plan.model_copy(update={"selected_adapter_id": "mlx_lm"}).model_validate(
            plan.model_copy(update={"selected_adapter_id": "mlx_lm"}).model_dump()
        )


def test_hero_event_is_immutable_and_task_start_requires_adapter() -> None:
    event = HeroEvent(
        event_id="event-0",
        run_id="run-1",
        sequence=0,
        occurred_at=NOW,
        event_type="run.started",
        phase="intake",
        status="running",
        source="test",
        evidence_level="fixture",
    )

    with pytest.raises(ValidationError):
        event.sequence = 1

    with pytest.raises(ValidationError, match="adapter_id"):
        HeroEvent(
            event_id="event-1",
            run_id="run-1",
            sequence=1,
            occurred_at=NOW,
            event_type="task.started",
            phase="execute",
            status="running",
            source="test",
            evidence_level="fixture",
            task_id="task-1",
            executor_class="local_ai",
        )
