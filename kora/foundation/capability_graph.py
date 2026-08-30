"""Fact-only capability graph derived from a local device inventory."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .device_inventory import DeviceInventory

SCHEMA_VERSION = "kora_foundation_capability_graph_v0"
CLAIM_BOUNDARY = (
    "Detected facts are not benchmark evidence and do not prove compatibility, model fit, "
    "performance, routing benefit, scaling, savings, or production readiness."
)


@dataclass(frozen=True)
class CapabilityFact:
    name: str
    value: Any
    availability: str
    evidence_state: str = "DETECTED"


@dataclass(frozen=True)
class CapabilityGraph:
    schema_version: str
    node_label: str
    availability: str
    compute: tuple[CapabilityFact, ...]
    accelerators: tuple[CapabilityFact, ...]
    runtime_candidates: tuple[CapabilityFact, ...]
    transport_candidates: tuple[CapabilityFact, ...]
    evidence_boundary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _fact(name: str, value: Any, present: bool | None) -> CapabilityFact:
    availability = "unknown" if present is None else ("available" if present else "unavailable")
    return CapabilityFact(name=name, value=value, availability=availability)


def build_capability_graph(inventory: DeviceInventory) -> CapabilityGraph:
    """Normalize inventory facts without introducing placement heuristics."""

    compute = (
        _fact("architecture", inventory.architecture, inventory.architecture != "unknown"),
        _fact("chip_model", inventory.chip_model, inventory.chip_model != "unknown"),
        _fact("memory_gb", inventory.total_memory_gb, None if inventory.total_memory_gb is None else True),
        _fact("physical_cpu_cores", inventory.physical_cpu_cores, None if inventory.physical_cpu_cores is None else True),
        _fact("logical_cpu_cores", inventory.logical_cpu_cores, None if inventory.logical_cpu_cores is None else True),
    )
    accelerators = tuple(
        _fact(model, {"core_count": inventory.gpu_core_counts[index] or None}, True)
        for index, model in enumerate(inventory.gpu_models)
    )
    runtimes = tuple(_fact(item.name, {"command": item.command}, item.detected) for item in inventory.runtime_candidates)
    transports = tuple(
        _fact(
            item.name,
            {"devices": list(item.devices), "max_link_speed_gbps": item.max_link_speed_gbps},
            item.detected,
        )
        for item in inventory.transports
    )
    return CapabilityGraph(
        schema_version=SCHEMA_VERSION,
        node_label=inventory.node_name,
        availability="available" if inventory.inventory_status == "detected" else "unknown",
        compute=compute,
        accelerators=accelerators,
        runtime_candidates=runtimes,
        transport_candidates=transports,
        evidence_boundary=CLAIM_BOUNDARY,
    )
