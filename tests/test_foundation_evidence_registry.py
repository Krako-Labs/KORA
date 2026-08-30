from __future__ import annotations

import json
from dataclasses import replace

import pytest

from kora.cli import main
from kora.foundation import evidence_registry as evidence_registry_module
from kora.foundation.evidence_registry import (
    EvidenceLineage,
    VerifiedEvidenceRecord,
    append_evidence,
    empty_evidence_registry,
    load_evidence_registry,
    save_evidence_registry,
    serialize_evidence_registry,
)
from kora.foundation.measurement_contract import MANIFEST_SCHEMA_VERSION
from kora.foundation.reality_matrix import SCHEMA_VERSION as OBSERVATION_SCHEMA_VERSION
from kora.foundation.reality_matrix import RealityObservation


def _record(observation_id: str = "obs-a", artifact_id: str = "artifact-a", **lineage_updates):
    observation = RealityObservation(
        schema_version=OBSERVATION_SCHEMA_VERSION,
        observation_id=observation_id,
        node_labels=("synthetic-node",),
        runtime="synthetic-runtime",
        hardware="synthetic-hardware",
        transport="none",
        topology="single_node",
        evidence_state="MEASURED",
        metrics={"synthetic_value": 1.0},
        source="fixtures/synthetic-result.json",
        notes="synthetic contract test only",
    )
    lineage = {
        "plan_id": "plan-a",
        "artifact_id": artifact_id,
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "artifact_path": observation.source,
        "manifest_sha256": "a" * 64,
    }
    lineage.update(lineage_updates)
    return VerifiedEvidenceRecord(
        schema_version="kora_foundation_verified_evidence_record_v0",
        revision=1,
        observation=observation,
        lineage=EvidenceLineage(**lineage),
    )


def test_append_is_deterministic_and_exactly_idempotent() -> None:
    registry, status = append_evidence(empty_evidence_registry(), _record("z", "artifact-z"))
    assert status == "appended"
    registry, _ = append_evidence(registry, _record("A", "artifact-a"))
    assert [record.observation.observation_id for record in registry.records] == ["A", "z"]
    before = serialize_evidence_registry(registry)
    registry, status = append_evidence(registry, _record("A", "artifact-a"))
    assert status == "unchanged"
    assert serialize_evidence_registry(registry) == before
    assert serialize_evidence_registry(registry) == serialize_evidence_registry(registry)


def test_duplicate_and_conflicting_lineage_are_rejected() -> None:
    registry, _ = append_evidence(empty_evidence_registry(), _record())
    conflicting_observation = replace(_record(), observation=replace(_record().observation, metrics={"synthetic_value": 2.0}))
    with pytest.raises(ValueError, match="conflicting duplicate observation_id"):
        append_evidence(registry, conflicting_observation)
    with pytest.raises(ValueError, match="artifact_id is already assigned"):
        append_evidence(registry, _record("obs-b", "artifact-a"))
    with pytest.raises(ValueError, match="source conflicts"):
        replace(_record(), lineage=replace(_record().lineage, artifact_path="different.json"))


def test_strict_loading_rejects_malformed_registry_and_raw_payload(tmp_path) -> None:
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="missing evidence registry fields"):
        load_evidence_registry(malformed)

    registry, _ = append_evidence(empty_evidence_registry(), _record())
    payload = registry.to_dict()
    payload["records"][0]["raw_payload"] = {"prompt": "must not persist"}
    malformed.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="unexpected evidence record fields"):
        load_evidence_registry(malformed)
    assert "raw_payload" not in serialize_evidence_registry(registry)
    assert "prompt" not in serialize_evidence_registry(registry)


def test_atomic_save_round_trip_and_no_temporary_file(tmp_path) -> None:
    destination = tmp_path / "nested" / "evidence.json"
    registry, _ = append_evidence(empty_evidence_registry(), _record())
    save_evidence_registry(registry, destination)
    assert load_evidence_registry(destination) == registry
    assert destination.read_text(encoding="utf-8") == serialize_evidence_registry(registry)
    assert list(destination.parent.glob(f".{destination.name}.*.tmp")) == []


def test_failed_atomic_replace_preserves_existing_registry(tmp_path, monkeypatch) -> None:
    destination = tmp_path / "evidence.json"
    registry, _ = append_evidence(empty_evidence_registry(), _record())
    save_evidence_registry(registry, destination)
    original = destination.read_bytes()
    updated, _ = append_evidence(registry, _record("obs-b", "artifact-b"))

    def fail_replace(source, target):
        raise OSError("synthetic replace failure")

    monkeypatch.setattr(evidence_registry_module.os, "replace", fail_replace)
    with pytest.raises(OSError, match="synthetic replace failure"):
        save_evidence_registry(updated, destination)
    assert destination.read_bytes() == original
    assert list(destination.parent.glob(f".{destination.name}.*.tmp")) == []


def test_evidence_cli_ingest_idempotency_validate_and_conflict(tmp_path, capsys) -> None:
    registry_path = tmp_path / "evidence.json"
    record_path = tmp_path / "record.json"
    record_path.write_text(json.dumps(_record().to_dict()), encoding="utf-8")

    assert main(["system", "evidence", "ingest", str(registry_path), str(record_path), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "appended"
    original = registry_path.read_bytes()
    assert main(["system", "evidence", "ingest", str(registry_path), str(record_path), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "unchanged"
    assert registry_path.read_bytes() == original
    assert main(["system", "evidence", "validate", str(registry_path), "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == {"record_count": 1, "status": "valid"}

    conflict_path = tmp_path / "conflict.json"
    conflict_path.write_text(json.dumps(_record("obs-b", "artifact-a").to_dict()), encoding="utf-8")
    with pytest.raises(SystemExit, match="2"):
        main(["system", "evidence", "ingest", str(registry_path), str(conflict_path)])
    assert "artifact_id is already assigned" in capsys.readouterr().err
