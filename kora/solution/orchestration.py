"""Deterministic capability-tier recommendation for bounded task contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class CapabilityTier(IntEnum):
    """Provider-neutral execution capability classes, ordered by capability."""

    L0_DETERMINISTIC = 0
    L1_LOCAL_BOUNDED = 1
    L2_LOCAL_STRONG = 2
    L3_FRONTIER = 3
    L4_HIGHEST_REASONING = 4


@dataclass(frozen=True)
class TaskContract:
    """Bounded routing facts known before execution begins."""

    objective_verification: bool = False
    repetitive_or_inspection: bool = False
    bounded_implementation: bool = False
    complex_cross_component: bool = False
    architecture_or_ambiguous: bool = False
    high_risk: bool = False


@dataclass(frozen=True)
class TierRecommendation:
    """Stable tier decision plus a machine-readable reason code."""

    tier: CapabilityTier
    reason_code: str


def recommend_capability_tier(contract: TaskContract) -> TierRecommendation:
    """Recommend the lowest safe capability tier from explicit contract facts.

    High-risk or architecture/ambiguity flags dominate lower-tier hints. The
    function performs no I/O and names no model or provider.
    """

    if contract.high_risk:
        return TierRecommendation(CapabilityTier.L4_HIGHEST_REASONING, "high_risk")
    if contract.architecture_or_ambiguous:
        return TierRecommendation(
            CapabilityTier.L4_HIGHEST_REASONING,
            "architecture_or_ambiguous",
        )
    if contract.complex_cross_component:
        return TierRecommendation(CapabilityTier.L3_FRONTIER, "complex_cross_component")
    if contract.bounded_implementation:
        if contract.objective_verification:
            return TierRecommendation(
                CapabilityTier.L2_LOCAL_STRONG,
                "bounded_implementation_verified",
            )
        return TierRecommendation(
            CapabilityTier.L3_FRONTIER,
            "bounded_implementation_unverified",
        )
    if contract.repetitive_or_inspection:
        return TierRecommendation(CapabilityTier.L1_LOCAL_BOUNDED, "bounded_routine")
    if contract.objective_verification:
        return TierRecommendation(CapabilityTier.L0_DETERMINISTIC, "objective_deterministic")
    return TierRecommendation(CapabilityTier.L3_FRONTIER, "unverified_default")


__all__ = [
    "CapabilityTier",
    "TaskContract",
    "TierRecommendation",
    "recommend_capability_tier",
]
