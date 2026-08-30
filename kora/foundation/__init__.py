"""KORA Foundation primitives."""

from .device_inventory import DeviceInventory, collect_device_inventory, render_device_inventory_text
from .capability_graph import CapabilityGraph, build_capability_graph
from .fleet_inventory import FleetInventory, build_fleet, load_fleet
from .measurement_contract import (
    METRIC_UNITS,
    MeasurementArtifactManifest,
    MeasurementPlan,
    MetricSpec,
    build_measured_observation,
    validate_measured_metrics,
    verify_artifact,
)
from .evidence_registry import (
    EvidenceLineage,
    VerifiedEvidenceRecord,
    VerifiedEvidenceRegistry,
    append_evidence,
    empty_evidence_registry,
    load_evidence_record,
    load_evidence_registry,
    save_evidence_registry,
    serialize_evidence_registry,
)
from .measurement_package import (
    MeasurementPackage,
    assemble_verified_evidence,
    load_measurement_package,
    serialize_verified_evidence,
)
from .reality_matrix import (
    RealityObservation,
    RealityRegistry,
    build_reality_registry,
    load_reality_registry,
    render_reality_registry_text,
)

__all__ = [
    "CapabilityGraph", "DeviceInventory", "FleetInventory", "MeasurementArtifactManifest",
    "MeasurementPackage", "MeasurementPlan", "MetricSpec", "RealityObservation", "RealityRegistry", "METRIC_UNITS",
    "EvidenceLineage", "VerifiedEvidenceRecord", "VerifiedEvidenceRegistry",
    "append_evidence", "empty_evidence_registry", "load_evidence_record",
    "load_evidence_registry", "save_evidence_registry", "serialize_evidence_registry",
    "assemble_verified_evidence", "load_measurement_package", "serialize_verified_evidence",
    "build_measured_observation", "validate_measured_metrics", "verify_artifact",
    "build_capability_graph", "build_fleet", "build_reality_registry", "collect_device_inventory",
    "load_fleet", "load_reality_registry", "render_device_inventory_text",
    "render_reality_registry_text",
]
