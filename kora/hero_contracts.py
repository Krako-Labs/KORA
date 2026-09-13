"""Fail-closed data contracts for the KORA Hero execution path."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


EvidenceLevel = Literal["fixture", "observed", "verified"]
ExecutorClass = Literal["deterministic", "exact_reuse", "local_ai", "frontier_ai"]
MemoryDomainKind = Literal["dedicated_gpu", "system", "unified"]
Feasibility = Literal["yes", "no", "unknown"]
HeroPhase = Literal[
    "intake",
    "analyze",
    "decompose",
    "plan",
    "execute",
    "merge",
    "verify",
    "replan",
    "escalate",
    "complete",
    "fail",
]
HeroStatus = Literal[
    "created",
    "ready",
    "running",
    "completed",
    "verified",
    "failed",
    "skipped",
    "replanned",
    "escalated",
]


class StrictContract(BaseModel):
    """Base model that rejects undeclared contract fields."""

    model_config = ConfigDict(extra="forbid")


class MemoryDomain(StrictContract):
    """One physical memory domain reported by a profiler."""

    domain_id: str = Field(min_length=1)
    kind: MemoryDomainKind
    total_bytes: int = Field(gt=0)
    source: str = Field(min_length=1)
    evidence_ref: str | None = None


class AcceleratorProfile(StrictContract):
    """Locally observed accelerator identity without inferred capability."""

    accelerator_id: str = Field(min_length=1)
    vendor: str = Field(min_length=1)
    product: str = Field(min_length=1)
    memory_domain_id: str
    device_identifier: str | None = None
    driver_version: str | None = None


class HardwareProfile(StrictContract):
    """Hardware facts used by feasibility planning."""

    schema_version: Literal["hero.hardware.v1"] = "hero.hardware.v1"
    profile_id: str = Field(min_length=1)
    captured_at: datetime
    platform: str = Field(min_length=1)
    architecture: str = Field(min_length=1)
    memory_domains: list[MemoryDomain] = Field(min_length=1)
    accelerators: list[AcceleratorProfile] = Field(default_factory=list)
    runtime_candidates: list[str] = Field(default_factory=list)
    evidence_level: EvidenceLevel
    evidence_refs: list[str] = Field(default_factory=list)
    unknown_fields: list[str] = Field(default_factory=list)

    @field_validator("captured_at")
    @classmethod
    def _captured_at_is_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("captured_at must include a timezone")
        return value

    @model_validator(mode="after")
    def _references_known_memory_domains(self) -> "HardwareProfile":
        domain_ids = [domain.domain_id for domain in self.memory_domains]
        if len(domain_ids) != len(set(domain_ids)):
            raise ValueError("memory domain IDs must be unique")
        known = set(domain_ids)
        for accelerator in self.accelerators:
            if accelerator.memory_domain_id not in known:
                raise ValueError(
                    f"accelerator {accelerator.accelerator_id!r} references an unknown memory domain"
                )
        return self


class ModelResourceProfile(StrictContract):
    """Byte-based model artifact facts; estimates must not use evidence_level=verified."""

    schema_version: Literal["hero.model-resource.v1"] = "hero.model-resource.v1"
    profile_id: str = Field(min_length=1)
    model_id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    artifact_format: Literal["gguf", "safetensors", "mlx", "other"]
    quantization: str = Field(min_length=1)
    artifact_bytes: int = Field(gt=0)
    model_weight_bytes: int = Field(gt=0)
    sha256: str
    source_revision: str = Field(min_length=1)
    evidence_level: EvidenceLevel
    tensor_inventory_ref: str | None = None
    tokenizer_digest: str | None = None
    chat_template_digest: str | None = None
    unknown_fields: list[str] = Field(default_factory=list)

    @field_validator("sha256")
    @classmethod
    def _sha256_is_hex(cls, value: str) -> str:
        normalized = value.lower()
        if len(normalized) != 64 or any(character not in "0123456789abcdef" for character in normalized):
            raise ValueError("sha256 must be 64 lowercase hexadecimal characters")
        return normalized

    @model_validator(mode="after")
    def _weights_fit_inside_artifact(self) -> "ModelResourceProfile":
        if self.model_weight_bytes > self.artifact_bytes:
            raise ValueError("model_weight_bytes cannot exceed artifact_bytes")
        if self.evidence_level == "verified" and not self.tensor_inventory_ref:
            raise ValueError("verified model resource profiles require tensor_inventory_ref")
        return self


class RuntimeCapability(StrictContract):
    """Declared runtime capability; detection is distinct from execution proof."""

    schema_version: Literal["hero.runtime-capability.v1"] = "hero.runtime-capability.v1"
    adapter_id: str = Field(min_length=1)
    executor_class: ExecutorClass
    supported_platforms: list[str] = Field(min_length=1)
    supported_architectures: list[str] = Field(min_length=1)
    supported_artifact_formats: list[str] = Field(min_length=1)
    memory_modes: list[Literal["gpu_resident", "hybrid_cpu_gpu", "unified"]] = Field(
        min_length=1
    )
    detected: bool
    evidence_level: EvidenceLevel
    evidence_refs: list[str] = Field(default_factory=list)


class WorkloadRequirements(StrictContract):
    """Memory and service constraints supplied to feasibility planning."""

    schema_version: Literal["hero.workload-requirements.v1"] = (
        "hero.workload-requirements.v1"
    )
    workload_class: str = Field(min_length=1)
    context_tokens: int = Field(gt=0)
    max_output_tokens: int = Field(gt=0)
    concurrency: int = Field(default=1, gt=0)
    estimated_kv_bytes: int | None = Field(default=None, ge=0)
    runtime_reserve_bytes: int | None = Field(default=None, ge=0)
    minimum_free_system_bytes: int = Field(default=2 * 1024**3, ge=0)
    allow_network: bool = False


class CandidateDecision(StrictContract):
    """One adapter candidate and the planner's explicit decision."""

    adapter_id: str = Field(min_length=1)
    feasibility: Feasibility
    reason_codes: list[str] = Field(min_length=1)
    estimated_peak_bytes: dict[str, int] = Field(default_factory=dict)
    rejected: bool

    @field_validator("estimated_peak_bytes")
    @classmethod
    def _memory_estimates_are_non_negative(cls, value: dict[str, int]) -> dict[str, int]:
        if any(amount < 0 for amount in value.values()):
            raise ValueError("estimated peak bytes cannot be negative")
        return value

    @model_validator(mode="after")
    def _decision_is_consistent(self) -> "CandidateDecision":
        if self.feasibility == "no" and not self.rejected:
            raise ValueError("an infeasible candidate must be rejected")
        return self


class ExecutionPlan(StrictContract):
    """Auditable execution plan produced from frozen input profiles."""

    schema_version: Literal["hero.execution-plan.v1"] = "hero.execution-plan.v1"
    plan_id: str = Field(min_length=1)
    hardware_profile_id: str = Field(min_length=1)
    model_resource_profile_id: str = Field(min_length=1)
    workload_class: str = Field(min_length=1)
    executor_class: ExecutorClass
    selected_adapter_id: str | None
    candidates: list[CandidateDecision] = Field(min_length=1)
    constraints: list[str] = Field(min_length=1)
    explanation: list[str] = Field(min_length=1)
    effective_config: dict[str, Any] = Field(default_factory=dict)
    expert_overrides_required: bool = False
    evidence_level: EvidenceLevel

    @model_validator(mode="after")
    def _selected_candidate_is_supported(self) -> "ExecutionPlan":
        selectable = {
            candidate.adapter_id
            for candidate in self.candidates
            if candidate.feasibility == "yes" and not candidate.rejected
        }
        if self.selected_adapter_id is None:
            if selectable:
                raise ValueError("a feasible non-rejected candidate requires a selected adapter")
        elif self.selected_adapter_id not in selectable:
            raise ValueError("selected_adapter_id must identify a feasible non-rejected candidate")
        if self.expert_overrides_required and self.selected_adapter_id is not None:
            raise ValueError("normal-user plans cannot select a path that requires expert overrides")
        return self


class HeroEvent(StrictContract):
    """Immutable event envelope used by runtime, evidence and UI replay."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["hero.event.v1"] = "hero.event.v1"
    event_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    sequence: int = Field(ge=0)
    occurred_at: datetime
    event_type: str = Field(min_length=1)
    phase: HeroPhase
    status: HeroStatus
    source: str = Field(min_length=1)
    evidence_level: EvidenceLevel
    payload: dict[str, Any] = Field(default_factory=dict)
    task_id: str | None = None
    parent_task_id: str | None = None
    attempt: int | None = Field(default=None, ge=1)
    executor_class: ExecutorClass | None = None
    adapter_id: str | None = None
    evidence_refs: tuple[str, ...] = ()

    @field_validator("occurred_at")
    @classmethod
    def _occurred_at_is_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("occurred_at must include a timezone")
        return value

    @model_validator(mode="after")
    def _task_events_have_task_ids(self) -> "HeroEvent":
        if self.event_type.startswith("task.") and not self.task_id:
            raise ValueError("task events require task_id")
        if self.event_type == "task.routed" and not self.executor_class:
            raise ValueError("task.routed requires executor_class")
        if self.event_type == "task.started" and (not self.executor_class or not self.adapter_id):
            raise ValueError("task.started requires executor_class and adapter_id")
        return self


__all__ = [
    "AcceleratorProfile",
    "CandidateDecision",
    "EvidenceLevel",
    "ExecutionPlan",
    "ExecutorClass",
    "Feasibility",
    "HardwareProfile",
    "HeroEvent",
    "MemoryDomain",
    "ModelResourceProfile",
    "RuntimeCapability",
    "WorkloadRequirements",
]
