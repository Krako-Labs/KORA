"""Persistent, append-only storage for verified measured observations.

The registry stores normalized observations and provenance references only. It
does not store or parse raw measurement artifacts and does not verify their
measurement correctness.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from .measurement_contract import MANIFEST_SCHEMA_VERSION, MeasurementArtifactManifest, MeasurementPlan
from .reality_matrix import RealityObservation, RealityRegistry, build_reality_registry

SCHEMA_VERSION = "kora_foundation_verified_evidence_registry_v0"
RECORD_SCHEMA_VERSION = "kora_foundation_verified_evidence_record_v0"
STABLE_ORDER_KEY = "observation.observation_id.casefold(), observation.observation_id"
CLAIM_BOUNDARY = (
    "This registry preserves supplied verified-artifact lineage; it does not store raw artifacts, "
    "validate measurement correctness, or prove performance, scaling, savings, or production readiness."
)


def _non_empty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


@dataclass(frozen=True)
class EvidenceLineage:
    plan_id: str
    artifact_id: str
    manifest_schema_version: str
    artifact_path: str
    manifest_sha256: str

    def __post_init__(self) -> None:
        _non_empty(self.plan_id, "plan_id")
        _non_empty(self.artifact_id, "artifact_id")
        if self.manifest_schema_version != MANIFEST_SCHEMA_VERSION:
            raise ValueError(f"expected manifest_schema_version {MANIFEST_SCHEMA_VERSION!r}")
        _non_empty(self.artifact_path, "artifact_path")
        if len(self.manifest_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.manifest_sha256
        ):
            raise ValueError("manifest_sha256 must be 64 lowercase hexadecimal characters")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EvidenceLineage:
        required = {
            "plan_id", "artifact_id", "manifest_schema_version", "artifact_path", "manifest_sha256"
        }
        if not isinstance(data, dict):
            raise ValueError("lineage must be a JSON object")
        missing = sorted(required - data.keys())
        unexpected = sorted(data.keys() - required)
        if missing:
            raise ValueError(f"missing lineage fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"unexpected lineage fields: {', '.join(unexpected)}")
        return cls(**data)


@dataclass(frozen=True)
class VerifiedEvidenceRecord:
    schema_version: str
    revision: int
    observation: RealityObservation
    lineage: EvidenceLineage

    def __post_init__(self) -> None:
        if self.schema_version != RECORD_SCHEMA_VERSION:
            raise ValueError(f"expected record schema_version {RECORD_SCHEMA_VERSION!r}")
        if self.revision != 1:
            raise ValueError("append-only v0 records must have revision 1")
        if self.observation.evidence_state != "MEASURED":
            raise ValueError("persisted evidence observation must be MEASURED")
        if self.observation.source != self.lineage.artifact_path:
            raise ValueError("observation source conflicts with lineage artifact_path")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_verified(
        cls,
        observation: RealityObservation,
        plan: MeasurementPlan,
        manifest: MeasurementArtifactManifest,
    ) -> VerifiedEvidenceRecord:
        """Construct lineage after the caller's verified-observation construction step."""

        if manifest.plan_id != plan.plan_id:
            raise ValueError("artifact manifest plan_id does not match measurement plan")
        return cls(
            schema_version=RECORD_SCHEMA_VERSION,
            revision=1,
            observation=observation,
            lineage=EvidenceLineage(
                plan_id=plan.plan_id,
                artifact_id=manifest.artifact_id,
                manifest_schema_version=manifest.schema_version,
                artifact_path=manifest.artifact_path,
                manifest_sha256=manifest.sha256,
            ),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VerifiedEvidenceRecord:
        required = {"schema_version", "revision", "observation", "lineage"}
        if not isinstance(data, dict):
            raise ValueError("evidence record must be a JSON object")
        missing = sorted(required - data.keys())
        unexpected = sorted(data.keys() - required)
        if missing:
            raise ValueError(f"missing evidence record fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"unexpected evidence record fields: {', '.join(unexpected)}")
        return cls(
            schema_version=data["schema_version"],
            revision=data["revision"],
            observation=RealityObservation.from_dict(data["observation"]),
            lineage=EvidenceLineage.from_dict(data["lineage"]),
        )


@dataclass(frozen=True)
class VerifiedEvidenceRegistry:
    schema_version: str
    records: tuple[VerifiedEvidenceRecord, ...]
    record_count: int
    stable_order_key: str
    claim_boundary: str

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"expected schema_version {SCHEMA_VERSION!r}")
        if self.record_count != len(self.records):
            raise ValueError("record_count does not match records")
        if self.stable_order_key != STABLE_ORDER_KEY:
            raise ValueError("unexpected stable_order_key")
        if self.claim_boundary != CLAIM_BOUNDARY:
            raise ValueError("unexpected claim_boundary")
        _validate_records(self.records)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_reality_registry(self) -> RealityRegistry:
        if not self.records:
            raise ValueError("cannot reconstruct a RealityRegistry from an empty evidence registry")
        return build_reality_registry(record.observation for record in self.records)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VerifiedEvidenceRegistry:
        required = {"schema_version", "records", "record_count", "stable_order_key", "claim_boundary"}
        if not isinstance(data, dict):
            raise ValueError("evidence registry must be a JSON object")
        missing = sorted(required - data.keys())
        unexpected = sorted(data.keys() - required)
        if missing:
            raise ValueError(f"missing evidence registry fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"unexpected evidence registry fields: {', '.join(unexpected)}")
        if not isinstance(data["records"], list):
            raise ValueError("records must be a JSON array")
        return cls(
            schema_version=data["schema_version"],
            records=tuple(VerifiedEvidenceRecord.from_dict(item) for item in data["records"]),
            record_count=data["record_count"],
            stable_order_key=data["stable_order_key"],
            claim_boundary=data["claim_boundary"],
        )


def _record_key(record: VerifiedEvidenceRecord) -> tuple[str, str]:
    identifier = record.observation.observation_id
    return identifier.casefold(), identifier


def _validate_records(records: Iterable[VerifiedEvidenceRecord]) -> None:
    observation_ids: set[str] = set()
    artifact_owners: dict[str, VerifiedEvidenceRecord] = {}
    for record in records:
        observation_id = record.observation.observation_id
        if observation_id in observation_ids:
            raise ValueError(f"duplicate observation_id is not allowed: {observation_id}")
        observation_ids.add(observation_id)
        prior = artifact_owners.get(record.lineage.artifact_id)
        if prior is not None:
            raise ValueError(
                f"artifact_id reuse is not allowed: {record.lineage.artifact_id} "
                f"({prior.observation.observation_id}, {observation_id})"
            )
        artifact_owners[record.lineage.artifact_id] = record
    if tuple(sorted(records, key=_record_key)) != tuple(records):
        raise ValueError("records are not in stable deterministic order")


def empty_evidence_registry() -> VerifiedEvidenceRegistry:
    return VerifiedEvidenceRegistry(SCHEMA_VERSION, (), 0, STABLE_ORDER_KEY, CLAIM_BOUNDARY)


def append_evidence(
    registry: VerifiedEvidenceRegistry, record: VerifiedEvidenceRecord
) -> tuple[VerifiedEvidenceRegistry, str]:
    """Append a new record, or return ``unchanged`` for exact re-ingestion."""

    for existing in registry.records:
        if existing.observation.observation_id == record.observation.observation_id:
            if existing == record:
                return registry, "unchanged"
            raise ValueError(f"conflicting duplicate observation_id: {record.observation.observation_id}")
        if existing.lineage.artifact_id == record.lineage.artifact_id:
            raise ValueError(
                f"artifact_id is already assigned to observation "
                f"{existing.observation.observation_id}: {record.lineage.artifact_id}"
            )
    records = tuple(sorted((*registry.records, record), key=_record_key))
    return VerifiedEvidenceRegistry(SCHEMA_VERSION, records, len(records), STABLE_ORDER_KEY, CLAIM_BOUNDARY), "appended"


def load_evidence_registry(path: str | Path) -> VerifiedEvidenceRegistry:
    registry_path = Path(path)
    try:
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load evidence registry {registry_path}: {exc}") from exc
    try:
        return VerifiedEvidenceRegistry.from_dict(payload)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid evidence registry {registry_path}: {exc}") from exc


def load_evidence_record(path: str | Path) -> VerifiedEvidenceRecord:
    record_path = Path(path)
    try:
        payload = json.loads(record_path.read_text(encoding="utf-8"))
        return VerifiedEvidenceRecord.from_dict(payload)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ValueError(f"cannot load evidence record {record_path}: {exc}") from exc


def serialize_evidence_registry(registry: VerifiedEvidenceRegistry) -> str:
    return json.dumps(registry.to_dict(), indent=2, sort_keys=True, allow_nan=False) + "\n"


def save_evidence_registry(registry: VerifiedEvidenceRegistry, path: str | Path) -> None:
    """Atomically replace a registry using a temporary file in its directory."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix=f".{destination.name}.", suffix=".tmp", delete=False,
        ) as temporary:
            temporary_name = temporary.name
            temporary.write(serialize_evidence_registry(registry))
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, destination)
        temporary_name = None
    finally:
        if temporary_name is not None:
            try:
                Path(temporary_name).unlink()
            except FileNotFoundError:
                pass
