"""End-to-end, non-executing Hero planning and evidence events."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from kora.hero_contracts import (
    ExecutionPlan,
    HardwareProfile,
    HeroEvent,
    ModelResourceProfile,
    RuntimeCapability,
    StrictContract,
    WorkloadRequirements,
)
from kora.hero_feasibility import build_execution_plan
from kora.hero_runtime_registry import (
    build_runtime_capabilities,
    default_adapter_priority,
)


class HeroPlanningBundle(StrictContract):
    """Profiles, decisions, and replayable events produced without execution."""

    schema_version: Literal["hero.planning-bundle.v1"] = "hero.planning-bundle.v1"
    hardware_profile_id: str = Field(min_length=1)
    model_resource_profile_id: str = Field(min_length=1)
    capabilities: list[RuntimeCapability] = Field(min_length=1)
    plan: ExecutionPlan
    events: list[HeroEvent] = Field(min_length=1)
    evidence_digest: str
    claim_boundary: str = Field(min_length=1)

    @model_validator(mode="after")
    def _references_are_consistent(self) -> HeroPlanningBundle:
        if self.plan.hardware_profile_id != self.hardware_profile_id:
            raise ValueError("plan and bundle hardware profile IDs differ")
        if self.plan.model_resource_profile_id != self.model_resource_profile_id:
            raise ValueError("plan and bundle model profile IDs differ")
        capability_ids = [capability.adapter_id for capability in self.capabilities]
        if len(capability_ids) != len(set(capability_ids)):
            raise ValueError("runtime capability IDs must be unique")
        if {candidate.adapter_id for candidate in self.plan.candidates} != set(
            capability_ids
        ):
            raise ValueError("plan candidates must match registered capabilities")
        if [event.sequence for event in self.events] != list(range(len(self.events))):
            raise ValueError("planning event sequences must be contiguous from zero")
        if len({event.run_id for event in self.events}) != 1:
            raise ValueError("planning events must share one run ID")
        if any(event.event_type.startswith("task.") for event in self.events):
            raise ValueError("planning bundles cannot contain task execution events")
        if len(self.evidence_digest) != 64 or any(
            character not in "0123456789abcdef" for character in self.evidence_digest
        ):
            raise ValueError("evidence_digest must be lowercase SHA-256")
        sealed = [
            event for event in self.events if event.event_type == "evidence.sealed"
        ]
        if len(sealed) != 1 or sealed[0].payload.get("sha256") != self.evidence_digest:
            raise ValueError("planning bundle requires one matching sealed digest")
        return self


def _evidence_level(
    hardware: HardwareProfile,
    model: ModelResourceProfile,
) -> Literal["fixture", "observed"]:
    if "fixture" in {hardware.evidence_level, model.evidence_level}:
        return "fixture"
    return "observed"


def _evidence_refs(
    hardware: HardwareProfile,
    model: ModelResourceProfile,
) -> tuple[str, ...]:
    refs = [
        f"profile:hardware:{hardware.profile_id}",
        f"profile:model:{model.profile_id}",
        *hardware.evidence_refs,
    ]
    refs.extend(
        domain.evidence_ref
        for domain in hardware.memory_domains
        if domain.evidence_ref is not None
    )
    if model.tensor_inventory_ref is not None:
        refs.append(model.tensor_inventory_ref)
    return tuple(dict.fromkeys(refs))


def _planning_digest(
    *,
    hardware: HardwareProfile,
    model: ModelResourceProfile,
    workload: WorkloadRequirements,
    capabilities: list[RuntimeCapability],
    plan: ExecutionPlan,
) -> str:
    payload = {
        "hardware": hardware.model_dump(mode="json"),
        "model": model.model_dump(mode="json"),
        "workload": workload.model_dump(mode="json"),
        "capabilities": [
            capability.model_dump(mode="json") for capability in capabilities
        ],
        "plan": plan.model_dump(mode="json"),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _event(
    *,
    run_id: str,
    sequence: int,
    occurred_at: datetime,
    event_type: str,
    phase: str,
    status: str,
    evidence_level: str,
    evidence_refs: tuple[str, ...],
    payload: dict[str, object],
) -> HeroEvent:
    return HeroEvent(
        event_id=f"{run_id}:{sequence:04d}",
        run_id=run_id,
        sequence=sequence,
        occurred_at=occurred_at,
        event_type=event_type,
        phase=phase,
        status=status,
        source="kora.hero_planner",
        evidence_level=evidence_level,
        evidence_refs=evidence_refs,
        payload=payload,
    )


def build_hero_planning_bundle(
    *,
    run_id: str,
    plan_id: str,
    occurred_at: datetime,
    hardware: HardwareProfile,
    model: ModelResourceProfile,
    workload: WorkloadRequirements,
) -> HeroPlanningBundle:
    """Create capabilities, a deterministic plan, and evidence-linked events."""

    capabilities = build_runtime_capabilities(hardware)
    priority = default_adapter_priority(
        hardware,
        artifact_format=model.artifact_format,
    )
    plan = build_execution_plan(
        plan_id=plan_id,
        hardware=hardware,
        model=model,
        workload=workload,
        capabilities=capabilities,
        adapter_priority=priority,
    )
    digest = _planning_digest(
        hardware=hardware,
        model=model,
        workload=workload,
        capabilities=capabilities,
        plan=plan,
    )
    level = _evidence_level(hardware, model)
    input_refs = _evidence_refs(hardware, model)
    sealed_refs = (*input_refs, f"sha256:{digest}")
    events = [
        _event(
            run_id=run_id,
            sequence=0,
            occurred_at=occurred_at,
            event_type="run.started",
            phase="intake",
            status="running",
            evidence_level=level,
            evidence_refs=input_refs,
            payload={
                "execution_performed": False,
                "provider_calls_performed": 0,
            },
        ),
        _event(
            run_id=run_id,
            sequence=1,
            occurred_at=occurred_at,
            event_type="workload.analyzed",
            phase="analyze",
            status="completed",
            evidence_level=level,
            evidence_refs=input_refs,
            payload={
                "hardware_profile_id": hardware.profile_id,
                "model_resource_profile_id": model.profile_id,
                "workload_class": workload.workload_class,
            },
        ),
        _event(
            run_id=run_id,
            sequence=2,
            occurred_at=occurred_at,
            event_type="runtime.capabilities.registered",
            phase="plan",
            status="completed",
            evidence_level=level,
            evidence_refs=input_refs,
            payload={
                "adapters": [
                    {
                        "adapter_id": capability.adapter_id,
                        "detected": capability.detected,
                    }
                    for capability in capabilities
                ]
            },
        ),
        _event(
            run_id=run_id,
            sequence=3,
            occurred_at=occurred_at,
            event_type="execution.plan.created",
            phase="plan",
            status="completed",
            evidence_level=level,
            evidence_refs=input_refs,
            payload={
                "plan_id": plan.plan_id,
                "selected_adapter_id": plan.selected_adapter_id,
                "executor_class": plan.executor_class,
                "candidate_decisions": [
                    decision.model_dump(mode="json") for decision in plan.candidates
                ],
                "runtime_started": False,
            },
        ),
        _event(
            run_id=run_id,
            sequence=4,
            occurred_at=occurred_at,
            event_type="evidence.sealed",
            phase="plan",
            status="completed",
            evidence_level=level,
            evidence_refs=sealed_refs,
            payload={
                "sha256": digest,
                "claim_scope": "planning_only",
            },
        ),
    ]
    return HeroPlanningBundle(
        hardware_profile_id=hardware.profile_id,
        model_resource_profile_id=model.profile_id,
        capabilities=capabilities,
        plan=plan,
        events=events,
        evidence_digest=digest,
        claim_boundary=(
            "Planning evidence only. No runtime was started and no model output, "
            "performance, service quality, or larger-than-VRAM execution was measured."
        ),
    )


def write_planning_evidence(
    output_path: str | os.PathLike[str],
    *,
    bundle: HeroPlanningBundle,
) -> Path:
    """Atomically write a human-auditable planning bundle."""

    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.tmp")
    temporary.write_text(
        json.dumps(bundle.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, target)
    return target


__all__ = [
    "HeroPlanningBundle",
    "build_hero_planning_bundle",
    "write_planning_evidence",
]
