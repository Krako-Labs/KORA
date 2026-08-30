"""Deterministic storage contracts for Reality Matrix evidence observations."""

from __future__ import annotations

import json
import math
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "kora_foundation_reality_observation_v0"
REGISTRY_SCHEMA_VERSION = "kora_foundation_reality_registry_v0"
EVIDENCE_STATES = frozenset({"DETECTED", "FACT", "MEASURED", "PLANNED", "UNKNOWN"})
CLAIM_BOUNDARY = (
    "The registry stores supplied evidence; it does not create benchmark evidence or prove "
    "performance, scaling, cost, savings, compatibility, or production readiness."
)


@dataclass(frozen=True)
class RealityObservation:
    schema_version: str
    observation_id: str
    node_labels: tuple[str, ...]
    runtime: str
    hardware: str
    transport: str
    topology: str
    evidence_state: str
    metrics: dict[str, float]
    source: str | None
    notes: str | None
    claim_boundary: str = "Only MEASURED observations with a source may contain performance metrics."

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"expected schema_version {SCHEMA_VERSION!r}")
        for field in ("observation_id", "runtime", "hardware", "transport", "topology"):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"observation field {field!r} must be a non-empty string")
        if not isinstance(self.node_labels, tuple) or not self.node_labels:
            raise ValueError("at least one node label is required")
        if any(not isinstance(label, str) or not label.strip() for label in self.node_labels):
            raise ValueError("node labels must be non-empty strings")
        folded_labels = [label.casefold() for label in self.node_labels]
        if len(folded_labels) != len(set(folded_labels)):
            raise ValueError("duplicate node labels are not allowed within an observation")
        if self.evidence_state not in EVIDENCE_STATES:
            raise ValueError(f"unsupported evidence_state {self.evidence_state!r}")
        if not isinstance(self.metrics, dict):
            raise ValueError("metrics must be an object")
        if any(not isinstance(name, str) or not name.strip() for name in self.metrics):
            raise ValueError("metric names must be non-empty strings")
        if self.metrics and self.evidence_state != "MEASURED":
            raise ValueError("performance metrics require MEASURED evidence")
        if self.evidence_state == "MEASURED" and (
            not self.metrics or not isinstance(self.source, str) or not self.source.strip()
        ):
            raise ValueError("MEASURED evidence requires metrics and a source")
        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(value)
            for value in self.metrics.values()
        ):
            raise ValueError("metric values must be finite numbers (not booleans)")
        if self.source is not None and (not isinstance(self.source, str) or not self.source.strip()):
            raise ValueError("source must be null or a non-empty string")
        if self.notes is not None and not isinstance(self.notes, str):
            raise ValueError("notes must be null or a string")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RealityObservation:
        """Strictly validate and load one JSON-ready observation object."""

        if not isinstance(data, dict):
            raise ValueError("observation must be a JSON object")
        required = {
            "schema_version", "observation_id", "node_labels", "runtime", "hardware",
            "transport", "topology", "evidence_state", "metrics", "source", "notes",
        }
        optional = {"claim_boundary"}
        missing = sorted(required - data.keys())
        unexpected = sorted(data.keys() - required - optional)
        if missing:
            raise ValueError(f"missing observation fields: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"unexpected observation fields: {', '.join(unexpected)}")
        if not isinstance(data["node_labels"], list):
            raise ValueError("node_labels must be a JSON array")
        try:
            return cls(**{**data, "node_labels": tuple(data["node_labels"])})
        except TypeError as exc:
            raise ValueError(f"malformed observation: {exc}") from exc


@dataclass(frozen=True)
class RealityRegistry:
    """A stable collection ordered by casefolded observation ID, then exact ID."""

    schema_version: str
    observations: tuple[RealityObservation, ...]
    observation_count: int
    summary: dict[str, dict[str, int]]
    stable_order_key: str
    claim_boundary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _counts(values: Iterable[str | int]) -> dict[str, int]:
    counts = Counter(str(value) for value in values)
    return {key: counts[key] for key in sorted(counts, key=lambda item: (item.casefold(), item))}


def build_reality_registry(observations: Iterable[RealityObservation]) -> RealityRegistry:
    """Collect observations without ranking or drawing performance conclusions."""

    items = sorted(observations, key=lambda item: (item.observation_id.casefold(), item.observation_id))
    if not items:
        raise ValueError("at least one reality observation is required")
    identifiers = [item.observation_id for item in items]
    if len(identifiers) != len(set(identifiers)):
        duplicates = sorted(identifier for identifier, count in Counter(identifiers).items() if count > 1)
        raise ValueError(f"duplicate observation IDs are not allowed: {', '.join(duplicates)}")
    summary = {
        "evidence_state": _counts(item.evidence_state for item in items),
        "runtime": _counts(item.runtime for item in items),
        "transport": _counts(item.transport for item in items),
        "topology": _counts(item.topology for item in items),
        "node_count": _counts(len(item.node_labels) for item in items),
    }
    return RealityRegistry(
        schema_version=REGISTRY_SCHEMA_VERSION,
        observations=tuple(items),
        observation_count=len(items),
        summary=summary,
        stable_order_key="observation_id.casefold(), observation_id",
        claim_boundary=CLAIM_BOUNDARY,
    )


def load_reality_registry(paths: Iterable[str | Path]) -> RealityRegistry:
    """Load one observation object from each supplied JSON file."""

    observations: list[RealityObservation] = []
    for path_value in paths:
        path = Path(path_value)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot load reality observation {path}: {exc}") from exc
        try:
            observations.append(RealityObservation.from_dict(payload))
        except ValueError as exc:
            raise ValueError(f"invalid reality observation {path}: {exc}") from exc
    return build_reality_registry(observations)


def render_reality_registry_text(registry: RealityRegistry) -> str:
    """Render an evidence-labelled, non-interpretive registry summary."""

    lines = ["KORA Foundation Reality Matrix Registry", f"Observations: {registry.observation_count}"]
    for observation in registry.observations:
        lines.append(
            f"  - {observation.observation_id} [{observation.evidence_state}]: "
            f"{observation.runtime} / {observation.transport} / {observation.topology} "
            f"({len(observation.node_labels)} node(s))"
        )
    lines.append("Evidence-state counts:")
    for state in sorted(EVIDENCE_STATES):
        lines.append(f"  - {state}: {registry.summary['evidence_state'].get(state, 0)}")
    lines.append(f"Boundary: {registry.claim_boundary}")
    return "\n".join(lines) + "\n"
