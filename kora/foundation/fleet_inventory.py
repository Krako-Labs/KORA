"""Deterministic, local-only fleet inventory aggregation."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from .capability_graph import CapabilityGraph, build_capability_graph
from .device_inventory import DeviceInventory

SCHEMA_VERSION = "kora_foundation_fleet_inventory_v0"


@dataclass(frozen=True)
class FleetNode:
    node_label: str
    inventory: DeviceInventory
    capabilities: CapabilityGraph


@dataclass(frozen=True)
class FleetInventory:
    schema_version: str
    nodes: tuple[FleetNode, ...]
    node_count: int
    evidence_state: str
    claim_boundary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_fleet(inventories: Iterable[DeviceInventory]) -> FleetInventory:
    items = sorted(inventories, key=lambda item: item.node_name.casefold())
    if not items:
        raise ValueError("at least one inventory is required")
    labels = [item.node_name for item in items]
    folded = [label.casefold() for label in labels]
    if len(folded) != len(set(folded)):
        raise ValueError("duplicate node labels are not allowed")
    nodes = tuple(FleetNode(item.node_name, item, build_capability_graph(item)) for item in items)
    return FleetInventory(
        schema_version=SCHEMA_VERSION,
        nodes=nodes,
        node_count=len(nodes),
        evidence_state="DETECTED",
        claim_boundary=(
            "This is a local aggregation of independently collected inventories, not evidence of "
            "connectivity, distributed execution, routing performance, or multi-node scaling."
        ),
    )


def load_fleet(paths: Iterable[str | Path]) -> FleetInventory:
    inventories: list[DeviceInventory] = []
    for path_value in paths:
        path = Path(path_value)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot load inventory {path}: {exc}") from exc
        inventories.append(DeviceInventory.from_dict(payload))
    return build_fleet(inventories)


def render_fleet_text(fleet: FleetInventory) -> str:
    lines = ["KORA Foundation Fleet Inventory", f"Nodes: {fleet.node_count}"]
    for node in fleet.nodes:
        inv = node.inventory
        lines.append(f"  - {node.node_label}: {inv.chip_model}, {inv.total_memory_gb or 'unknown'} GB, {node.capabilities.availability}")
    lines.extend((f"Evidence: {fleet.evidence_state}", f"Boundary: {fleet.claim_boundary}"))
    return "\n".join(lines) + "\n"
