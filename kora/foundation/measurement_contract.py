"""Pre-registration and provenance contracts for local Reality Matrix measurements.

These types describe intended measurements and local artifact integrity. They do
not run benchmarks, interpret artifacts, or establish that supplied measurements
are correct.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from .reality_matrix import SCHEMA_VERSION as OBSERVATION_SCHEMA_VERSION
from .reality_matrix import RealityObservation

PLAN_SCHEMA_VERSION = "kora_foundation_measurement_plan_v0"
MANIFEST_SCHEMA_VERSION = "kora_foundation_measurement_artifact_manifest_v0"
METRIC_UNITS = frozenset(
    {
        "bytes",
        "count",
        "gigabytes",
        "milliseconds",
        "percent",
        "ratio",
        "seconds",
        "tokens_per_second",
    }
)
PLAN_CLAIM_BOUNDARY = (
    "A PLANNED measurement plan pre-registers intended collection; it contains no benchmark result."
)
MANIFEST_CLAIM_BOUNDARY = (
    "A verified manifest proves local artifact provenance and integrity only, not correctness or performance."
)


def _non_empty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _integer(value: Any, field: str, *, minimum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        qualifier = "nonnegative" if minimum == 0 else "positive"
        raise ValueError(f"{field} must be a {qualifier} integer")
    return value


@dataclass(frozen=True)
class MetricSpec:
    name: str
    unit: str
    method: str

    def __post_init__(self) -> None:
        _non_empty(self.name, "metric name")
        if self.unit not in METRIC_UNITS:
            raise ValueError(f"unsupported metric unit {self.unit!r}")
        _non_empty(self.method, "metric method")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MetricSpec:
        if not isinstance(data, dict):
            raise ValueError("metric must be a JSON object")
        required = {"name", "unit", "method"}
        missing = sorted(required - data.keys())
        unexpected = sorted(data.keys() - required)
        if missing:
            raise ValueError(f"missing metric fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"unexpected metric fields: {', '.join(unexpected)}")
        return cls(**data)


@dataclass(frozen=True)
class MeasurementPlan:
    schema_version: str
    plan_id: str
    node_labels: tuple[str, ...]
    runtime: str
    hardware: str
    transport: str
    topology: str
    metrics: tuple[MetricSpec, ...]
    repetitions: int
    warmup_runs: int
    run_count: int
    workload_label: str | None
    model_label: str | None
    preconditions: tuple[str, ...]
    notes: str | None
    evidence_state: str = "PLANNED"
    claim_boundary: str = PLAN_CLAIM_BOUNDARY

    def __post_init__(self) -> None:
        if self.schema_version != PLAN_SCHEMA_VERSION:
            raise ValueError(f"expected schema_version {PLAN_SCHEMA_VERSION!r}")
        for field in ("plan_id", "runtime", "hardware", "transport", "topology"):
            _non_empty(getattr(self, field), field)
        if not isinstance(self.node_labels, tuple) or not self.node_labels:
            raise ValueError("at least one node label is required")
        if any(not isinstance(label, str) or not label.strip() for label in self.node_labels):
            raise ValueError("node labels must be non-empty strings")
        folded_labels = [label.casefold() for label in self.node_labels]
        if len(folded_labels) != len(set(folded_labels)):
            raise ValueError("duplicate node labels are not allowed")
        if not isinstance(self.metrics, tuple) or not self.metrics:
            raise ValueError("at least one metric is required")
        if any(not isinstance(metric, MetricSpec) for metric in self.metrics):
            raise ValueError("metrics must contain MetricSpec values")
        names = [metric.name.casefold() for metric in self.metrics]
        if len(names) != len(set(names)):
            raise ValueError("duplicate metric names are not allowed")
        if tuple(sorted(self.metrics, key=lambda item: (item.name.casefold(), item.name))) != self.metrics:
            raise ValueError("metrics must use deterministic name ordering")
        _integer(self.repetitions, "repetitions", minimum=1)
        _integer(self.warmup_runs, "warmup_runs", minimum=0)
        _integer(self.run_count, "run_count", minimum=1)
        for field in ("workload_label", "model_label"):
            value = getattr(self, field)
            if value is not None:
                _non_empty(value, field)
        if not isinstance(self.preconditions, tuple) or any(
            not isinstance(item, str) or not item.strip() for item in self.preconditions
        ):
            raise ValueError("preconditions must be non-empty strings")
        if self.notes is not None and not isinstance(self.notes, str):
            raise ValueError("notes must be null or a string")
        if self.evidence_state != "PLANNED":
            raise ValueError("measurement plan evidence_state must remain PLANNED")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MeasurementPlan:
        if not isinstance(data, dict):
            raise ValueError("measurement plan must be a JSON object")
        required = {
            "schema_version", "plan_id", "node_labels", "runtime", "hardware", "transport",
            "topology", "metrics", "repetitions", "warmup_runs", "run_count", "workload_label",
            "model_label", "preconditions", "notes", "evidence_state",
        }
        optional = {"claim_boundary"}
        missing = sorted(required - data.keys())
        unexpected = sorted(data.keys() - required - optional)
        if missing:
            raise ValueError(f"missing measurement plan fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"unexpected measurement plan fields: {', '.join(unexpected)}")
        for field in ("node_labels", "metrics", "preconditions"):
            if not isinstance(data[field], list):
                raise ValueError(f"{field} must be a JSON array")
        metrics = tuple(
            sorted(
                (MetricSpec.from_dict(item) for item in data["metrics"]),
                key=lambda item: (item.name.casefold(), item.name),
            )
        )
        try:
            return cls(
                **{
                    **data,
                    "node_labels": tuple(data["node_labels"]),
                    "metrics": metrics,
                    "preconditions": tuple(data["preconditions"]),
                }
            )
        except TypeError as exc:
            raise ValueError(f"malformed measurement plan: {exc}") from exc


@dataclass(frozen=True)
class MeasurementArtifactManifest:
    schema_version: str
    artifact_id: str
    plan_id: str
    artifact_path: str
    sha256: str
    collector_id: str
    collector_version: str | None
    timestamp: str
    local_only: bool
    notes: str | None
    claim_boundary: str = MANIFEST_CLAIM_BOUNDARY

    def __post_init__(self) -> None:
        if self.schema_version != MANIFEST_SCHEMA_VERSION:
            raise ValueError(f"expected schema_version {MANIFEST_SCHEMA_VERSION!r}")
        for field in ("artifact_id", "plan_id", "artifact_path", "collector_id", "timestamp"):
            _non_empty(getattr(self, field), field)
        path = PurePosixPath(self.artifact_path)
        windows_path = PureWindowsPath(self.artifact_path)
        if path.is_absolute() or windows_path.is_absolute() or "\\" in self.artifact_path:
            raise ValueError("artifact_path must be a relative POSIX path")
        if any(part in {"", ".", ".."} for part in path.parts):
            raise ValueError("artifact_path must not contain empty, current, or parent path segments")
        if len(self.sha256) != 64 or any(character not in "0123456789abcdef" for character in self.sha256):
            raise ValueError("sha256 must be 64 lowercase hexadecimal characters")
        if self.collector_version is not None:
            _non_empty(self.collector_version, "collector_version")
        if self.local_only is not True:
            raise ValueError("local_only must be true")
        if self.notes is not None and not isinstance(self.notes, str):
            raise ValueError("notes must be null or a string")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MeasurementArtifactManifest:
        if not isinstance(data, dict):
            raise ValueError("artifact manifest must be a JSON object")
        required = {
            "schema_version", "artifact_id", "plan_id", "artifact_path", "sha256",
            "collector_id", "collector_version", "timestamp", "local_only", "notes",
        }
        optional = {"claim_boundary"}
        missing = sorted(required - data.keys())
        unexpected = sorted(data.keys() - required - optional)
        if missing:
            raise ValueError(f"missing artifact manifest fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"unexpected artifact manifest fields: {', '.join(unexpected)}")
        try:
            return cls(**data)
        except TypeError as exc:
            raise ValueError(f"malformed artifact manifest: {exc}") from exc


def verify_artifact(
    plan: MeasurementPlan,
    manifest: MeasurementArtifactManifest,
    artifact_root: str | Path,
) -> Path:
    """Fail closed unless the manifest identifies the plan and exact local bytes."""

    if manifest.plan_id != plan.plan_id:
        raise ValueError("artifact manifest plan_id does not match measurement plan")
    root = Path(artifact_root).resolve()
    artifact = (root / manifest.artifact_path).resolve()
    try:
        artifact.relative_to(root)
    except ValueError as exc:
        raise ValueError("artifact path resolves outside artifact root") from exc
    if not artifact.is_file():
        raise ValueError(f"artifact file is missing: {manifest.artifact_path}")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if digest != manifest.sha256:
        raise ValueError("artifact SHA-256 does not match manifest")
    return artifact


def build_measured_observation(
    plan: MeasurementPlan,
    manifest: MeasurementArtifactManifest,
    artifact_root: str | Path,
    *,
    observation_id: str,
    metrics: dict[str, float],
    notes: str | None = None,
) -> RealityObservation:
    """Verify provenance, then construct a measured observation from explicit metrics."""

    verify_artifact(plan, manifest, artifact_root)
    ordered_metrics = validate_measured_metrics(plan, metrics)
    return RealityObservation(
        schema_version=OBSERVATION_SCHEMA_VERSION,
        observation_id=observation_id,
        node_labels=plan.node_labels,
        runtime=plan.runtime,
        hardware=plan.hardware,
        transport=plan.transport,
        topology=plan.topology,
        evidence_state="MEASURED",
        metrics=ordered_metrics,
        source=manifest.artifact_path,
        notes=notes,
    )


def validate_measured_metrics(
    plan: MeasurementPlan, metrics: dict[str, float]
) -> dict[str, float]:
    """Validate explicit values against a plan and return stable name ordering."""

    if not isinstance(metrics, dict) or not metrics:
        raise ValueError("explicit measured metrics are required")
    planned_names = {metric.name for metric in plan.metrics}
    if set(metrics) != planned_names:
        raise ValueError("measured metric names must exactly match the measurement plan")
    if any(
        not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value)
        for value in metrics.values()
    ):
        raise ValueError("measured metric values must be finite numbers (not booleans)")
    return {name: metrics[name] for name in sorted(metrics, key=lambda item: (item.casefold(), item))}
