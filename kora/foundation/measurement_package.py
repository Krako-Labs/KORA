"""Strict fixture-only assembly contract for verified local measurement evidence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .evidence_registry import VerifiedEvidenceRecord
from .measurement_contract import (
    MeasurementArtifactManifest,
    MeasurementPlan,
    build_measured_observation,
    validate_measured_metrics,
)

SCHEMA_VERSION = "kora_foundation_measurement_package_v0"


def _non_empty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _ordered_metrics(metrics: Any, plan: MeasurementPlan) -> dict[str, float]:
    if not isinstance(metrics, dict) or not metrics:
        raise ValueError("package metrics must be a non-empty JSON object")
    if any(not isinstance(name, str) or not name.strip() for name in metrics):
        raise ValueError("package metric names must be non-empty strings")
    planned_names = {metric.name for metric in plan.metrics}
    if set(metrics) != planned_names:
        missing = sorted(planned_names - set(metrics))
        unexpected = sorted(set(metrics) - planned_names)
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if unexpected:
            details.append(f"unexpected: {', '.join(unexpected)}")
        raise ValueError(
            "package metric names must exactly match the measurement plan"
            + (f" ({'; '.join(details)})" if details else "")
        )
    return validate_measured_metrics(plan, metrics)


@dataclass(frozen=True)
class MeasurementPackage:
    schema_version: str
    package_id: str
    measurement_plan: MeasurementPlan
    artifact_manifest: MeasurementArtifactManifest
    metrics: dict[str, float]
    observation_id: str
    notes: str | None = None

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"expected schema_version {SCHEMA_VERSION!r}")
        _non_empty(self.package_id, "package_id")
        _non_empty(self.observation_id, "observation_id")
        if not isinstance(self.measurement_plan, MeasurementPlan):
            raise ValueError("measurement_plan must be a MeasurementPlan")
        if not isinstance(self.artifact_manifest, MeasurementArtifactManifest):
            raise ValueError("artifact_manifest must be a MeasurementArtifactManifest")
        if self.artifact_manifest.plan_id != self.measurement_plan.plan_id:
            raise ValueError("artifact manifest plan_id does not match measurement plan")
        ordered = _ordered_metrics(self.metrics, self.measurement_plan)
        if self.metrics != ordered or list(self.metrics) != list(ordered):
            raise ValueError("package metrics must use deterministic name ordering")
        if self.notes is not None and not isinstance(self.notes, str):
            raise ValueError("notes must be null or a string")

    def to_dict(self) -> dict[str, Any]:
        plan = self.measurement_plan.to_dict()
        plan["node_labels"] = list(plan["node_labels"])
        plan["metrics"] = list(plan["metrics"])
        plan["preconditions"] = list(plan["preconditions"])
        return {
            "schema_version": self.schema_version,
            "package_id": self.package_id,
            "measurement_plan": plan,
            "artifact_manifest": self.artifact_manifest.to_dict(),
            "metrics": dict(self.metrics),
            "observation_id": self.observation_id,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MeasurementPackage:
        if not isinstance(data, dict):
            raise ValueError("measurement package must be a JSON object")
        required = {
            "schema_version", "package_id", "measurement_plan", "artifact_manifest",
            "metrics", "observation_id",
        }
        optional = {"notes"}
        missing = sorted(required - data.keys())
        unexpected = sorted(data.keys() - required - optional)
        if missing:
            raise ValueError(f"missing measurement package fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"unexpected measurement package fields: {', '.join(unexpected)}")
        plan = MeasurementPlan.from_dict(data["measurement_plan"])
        manifest = MeasurementArtifactManifest.from_dict(data["artifact_manifest"])
        metrics = _ordered_metrics(data["metrics"], plan)
        return cls(
            schema_version=data["schema_version"],
            package_id=data["package_id"],
            measurement_plan=plan,
            artifact_manifest=manifest,
            metrics=metrics,
            observation_id=data["observation_id"],
            notes=data.get("notes"),
        )


def assemble_verified_evidence(
    package: MeasurementPackage, artifact_root: str | Path
) -> VerifiedEvidenceRecord:
    """Verify the separate artifact and build the exact Task 004 record."""

    observation = build_measured_observation(
        package.measurement_plan,
        package.artifact_manifest,
        artifact_root,
        observation_id=package.observation_id,
        metrics=package.metrics,
        notes=package.notes,
    )
    return VerifiedEvidenceRecord.from_verified(
        observation, package.measurement_plan, package.artifact_manifest
    )


def load_measurement_package(path: str | Path) -> MeasurementPackage:
    package_path = Path(path)
    try:
        payload = json.loads(package_path.read_text(encoding="utf-8"))
        return MeasurementPackage.from_dict(payload)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ValueError(f"cannot load measurement package {package_path}: {exc}") from exc


def serialize_verified_evidence(record: VerifiedEvidenceRecord) -> str:
    return json.dumps(record.to_dict(), indent=2, sort_keys=True, allow_nan=False) + "\n"
