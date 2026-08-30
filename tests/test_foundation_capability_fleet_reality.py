from __future__ import annotations

import json
from dataclasses import replace

import pytest

from kora.foundation.capability_graph import build_capability_graph
from kora.foundation.device_inventory import collect_device_inventory
from kora.foundation.fleet_inventory import build_fleet, load_fleet
from kora.foundation.reality_matrix import SCHEMA_VERSION, RealityObservation


def _inventory(label: str):
    return collect_device_inventory(
        executor=lambda command: None,
        which=lambda command: None,
        node_name=label,
        os_name="Darwin",
        os_version="26.0",
        architecture="arm64",
    )


def test_capability_graph_keeps_detected_facts_separate_from_measurements() -> None:
    graph = build_capability_graph(_inventory("node-a"))
    data = graph.to_dict()
    facts = data["compute"] + data["accelerators"] + data["runtime_candidates"] + data["transport_candidates"]
    assert {fact["evidence_state"] for fact in facts} == {"DETECTED"}
    assert "performance" in data["evidence_boundary"]
    assert "metrics" not in json.dumps(data)


def test_fleet_is_deterministic_and_rejects_duplicate_labels(tmp_path) -> None:
    first, second = _inventory("z-node"), _inventory("a-node")
    fleet = build_fleet([first, second])
    assert [node.node_label for node in fleet.nodes] == ["a-node", "z-node"]
    assert fleet.node_count == 2

    with pytest.raises(ValueError, match="duplicate"):
        build_fleet([first, replace(first, node_name="Z-NODE")])

    path = tmp_path / "bad.json"
    path.write_text('{"schema_version": "wrong"}', encoding="utf-8")
    with pytest.raises(ValueError, match="schema_version"):
        load_fleet([path])


def test_reality_observation_enforces_evidence_state_separation() -> None:
    planned = RealityObservation(
        schema_version=SCHEMA_VERSION,
        observation_id="planned-tcp",
        node_labels=("node-a", "node-b"),
        runtime="unknown",
        hardware="mixed-mac",
        transport="tcp",
        topology="independent_workers",
        evidence_state="PLANNED",
        metrics={},
        source=None,
        notes="future experiment",
    )
    assert planned.to_dict()["evidence_state"] == "PLANNED"

    with pytest.raises(ValueError, match="MEASURED"):
        replace(planned, metrics={"tokens_per_second": 1.0})
    with pytest.raises(ValueError, match="source"):
        replace(planned, evidence_state="MEASURED", metrics={"tokens_per_second": 1.0})

    measured = replace(
        planned,
        evidence_state="MEASURED",
        metrics={"latency_seconds": 1.25},
        source="local-experiment.json",
    )
    assert measured.metrics["latency_seconds"] == 1.25
