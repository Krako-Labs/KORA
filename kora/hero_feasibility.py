"""Deterministic, evidence-aware feasibility planning for KORA Hero runtimes."""

from __future__ import annotations

from collections.abc import Iterable

from kora.hero_contracts import (
    CandidateDecision,
    ExecutionPlan,
    HardwareProfile,
    MemoryDomain,
    ModelResourceProfile,
    RuntimeCapability,
    WorkloadRequirements,
)


def _domain(profile: HardwareProfile, kind: str) -> MemoryDomain | None:
    return next((item for item in profile.memory_domains if item.kind == kind), None)


def _static_rejections(
    capability: RuntimeCapability,
    hardware: HardwareProfile,
    model: ModelResourceProfile,
    workload: WorkloadRequirements,
) -> list[str]:
    reasons: list[str] = []
    platforms = {item.lower() for item in capability.supported_platforms}
    architectures = {item.lower() for item in capability.supported_architectures}
    if not capability.detected:
        reasons.append("runtime_not_detected")
    if "*" not in platforms and hardware.platform.lower() not in platforms:
        reasons.append("platform_unsupported")
    if "*" not in architectures and hardware.architecture.lower() not in architectures:
        reasons.append("architecture_unsupported")
    if model.artifact_format not in capability.supported_artifact_formats:
        reasons.append("artifact_format_unsupported")
    if capability.executor_class == "frontier_ai" and not workload.allow_network:
        reasons.append("network_disallowed")
    return reasons


def _required_bytes(
    model: ModelResourceProfile, workload: WorkloadRequirements
) -> int | None:
    if workload.estimated_kv_bytes is None or workload.runtime_reserve_bytes is None:
        return None
    return model.model_weight_bytes + workload.estimated_kv_bytes + workload.runtime_reserve_bytes


def _decision(
    adapter_id: str,
    feasibility: str,
    reason: str,
    *,
    estimated: dict[str, int] | None = None,
) -> CandidateDecision:
    return CandidateDecision(
        adapter_id=adapter_id,
        feasibility=feasibility,
        reason_codes=[reason],
        estimated_peak_bytes=estimated or {},
        rejected=feasibility != "yes",
    )


def _evaluate_gpu_resident(
    capability: RuntimeCapability,
    hardware: HardwareProfile,
    required_bytes: int | None,
) -> CandidateDecision:
    gpu = _domain(hardware, "dedicated_gpu")
    if gpu is None:
        return _decision(capability.adapter_id, "no", "dedicated_gpu_memory_missing")
    if required_bytes is None:
        return _decision(capability.adapter_id, "unknown", "kv_or_runtime_reserve_unknown")
    if required_bytes > gpu.total_bytes:
        return _decision(
            capability.adapter_id,
            "no",
            "dedicated_gpu_capacity_insufficient",
            estimated={"dedicated_gpu": required_bytes},
        )
    return _decision(
        capability.adapter_id,
        "yes",
        "gpu_resident_capacity_satisfied",
        estimated={"dedicated_gpu": required_bytes},
    )


def _evaluate_unified(
    capability: RuntimeCapability,
    hardware: HardwareProfile,
    required_bytes: int | None,
    workload: WorkloadRequirements,
) -> CandidateDecision:
    unified = _domain(hardware, "unified")
    if unified is None:
        return _decision(capability.adapter_id, "no", "unified_memory_missing")
    if required_bytes is None:
        return _decision(capability.adapter_id, "unknown", "kv_or_runtime_reserve_unknown")
    safe_capacity = unified.total_bytes - workload.minimum_free_system_bytes
    if required_bytes > safe_capacity:
        return _decision(
            capability.adapter_id,
            "no",
            "unified_memory_capacity_insufficient",
            estimated={"unified": required_bytes},
        )
    return _decision(
        capability.adapter_id,
        "yes",
        "unified_memory_capacity_satisfied",
        estimated={"unified": required_bytes},
    )


def _evaluate_hybrid(
    capability: RuntimeCapability,
    hardware: HardwareProfile,
    required_bytes: int | None,
    workload: WorkloadRequirements,
) -> CandidateDecision:
    system = _domain(hardware, "system")
    gpu = _domain(hardware, "dedicated_gpu")
    if system is None or gpu is None:
        return _decision(capability.adapter_id, "no", "hybrid_memory_domains_missing")
    if required_bytes is None:
        return _decision(capability.adapter_id, "unknown", "kv_or_runtime_reserve_unknown")
    safe_system_capacity = system.total_bytes - workload.minimum_free_system_bytes
    if required_bytes > safe_system_capacity:
        return _decision(
            capability.adapter_id,
            "no",
            "system_memory_capacity_insufficient",
            estimated={"system": required_bytes},
        )
    return CandidateDecision(
        adapter_id=capability.adapter_id,
        feasibility="yes",
        reason_codes=[
            "hybrid_host_capacity_satisfied",
            "placement_requires_runtime_plan",
        ],
        estimated_peak_bytes={"system": required_bytes},
        rejected=False,
    )


def evaluate_candidate(
    capability: RuntimeCapability,
    hardware: HardwareProfile,
    model: ModelResourceProfile,
    workload: WorkloadRequirements,
) -> CandidateDecision:
    """Evaluate one runtime without starting it or inferring unknown overhead."""

    static_rejections = _static_rejections(capability, hardware, model, workload)
    if static_rejections:
        return CandidateDecision(
            adapter_id=capability.adapter_id,
            feasibility="no",
            reason_codes=static_rejections,
            rejected=True,
        )

    required_bytes = _required_bytes(model, workload)
    decisions: list[CandidateDecision] = []
    if "unified" in capability.memory_modes:
        decisions.append(_evaluate_unified(capability, hardware, required_bytes, workload))
    if "hybrid_cpu_gpu" in capability.memory_modes:
        decisions.append(_evaluate_hybrid(capability, hardware, required_bytes, workload))
    if "gpu_resident" in capability.memory_modes:
        decisions.append(_evaluate_gpu_resident(capability, hardware, required_bytes))

    feasible = next((item for item in decisions if item.feasibility == "yes"), None)
    if feasible is not None:
        return feasible
    unknown = next((item for item in decisions if item.feasibility == "unknown"), None)
    if unknown is not None:
        return unknown
    if decisions:
        reasons = list(
            dict.fromkeys(reason for item in decisions for reason in item.reason_codes)
        )
        estimated_peak_bytes: dict[str, int] = {}
        for item in decisions:
            for domain, amount in item.estimated_peak_bytes.items():
                estimated_peak_bytes[domain] = max(
                    amount,
                    estimated_peak_bytes.get(domain, 0),
                )
        return CandidateDecision(
            adapter_id=capability.adapter_id,
            feasibility="no",
            reason_codes=reasons,
            estimated_peak_bytes=estimated_peak_bytes,
            rejected=True,
        )
    return _decision(capability.adapter_id, "no", "memory_mode_unsupported")


def build_execution_plan(
    *,
    plan_id: str,
    hardware: HardwareProfile,
    model: ModelResourceProfile,
    workload: WorkloadRequirements,
    capabilities: Iterable[RuntimeCapability],
    adapter_priority: list[str],
) -> ExecutionPlan:
    """Build a deterministic plan; unknown resource inputs fail closed."""

    capability_list = list(capabilities)
    decisions = [
        evaluate_candidate(capability, hardware, model, workload)
        for capability in capability_list
    ]
    decision_by_id = {decision.adapter_id: decision for decision in decisions}
    selected_adapter_id = next(
        (
            adapter_id
            for adapter_id in adapter_priority
            if adapter_id in decision_by_id
            and decision_by_id[adapter_id].feasibility == "yes"
            and not decision_by_id[adapter_id].rejected
        ),
        None,
    )
    selected_capability = next(
        (
            capability
            for capability in capability_list
            if capability.adapter_id == selected_adapter_id
        ),
        None,
    )
    if selected_adapter_id is None:
        explanation = [
            "No candidate has sufficient observed inputs and declared capability.",
            "The planner failed closed without starting a runtime.",
        ]
        executor_class = "local_ai"
    else:
        explanation = [
            f"Selected {selected_adapter_id} using the declared priority order.",
            "Selection proves planning feasibility only; execution must be measured separately.",
        ]
        assert selected_capability is not None
        executor_class = selected_capability.executor_class

    evidence_level = (
        "fixture"
        if "fixture" in {hardware.evidence_level, model.evidence_level}
        else "observed"
    )
    return ExecutionPlan(
        plan_id=plan_id,
        hardware_profile_id=hardware.profile_id,
        model_resource_profile_id=model.profile_id,
        workload_class=workload.workload_class,
        executor_class=executor_class,
        selected_adapter_id=selected_adapter_id,
        candidates=decisions,
        constraints=[
            "no_runtime_started",
            "no_provider_fallback",
            "unknown_memory_overhead_fails_closed",
        ],
        explanation=explanation,
        effective_config={
            "adapter_priority": adapter_priority,
            "context_tokens": workload.context_tokens,
            "max_output_tokens": workload.max_output_tokens,
            "concurrency": workload.concurrency,
        },
        evidence_level=evidence_level,
    )


__all__ = ["build_execution_plan", "evaluate_candidate"]
