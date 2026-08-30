from __future__ import annotations

import hashlib
import json

import pytest

from kora.foundation.measurement_contract import (
    MANIFEST_SCHEMA_VERSION,
    PLAN_SCHEMA_VERSION,
    MeasurementArtifactManifest,
    MeasurementPlan,
    build_measured_observation,
    verify_artifact,
)


def _plan_data(**updates):
    data = {
        "schema_version": PLAN_SCHEMA_VERSION,
        "plan_id": "synthetic-plan-a",
        "node_labels": ["synthetic-node-a"],
        "runtime": "synthetic-runtime-label",
        "hardware": "synthetic-hardware-label",
        "transport": "none",
        "topology": "single-node",
        "metrics": [
            {"name": "synthetic_latency", "unit": "milliseconds", "method": "fixture value"},
            {"name": "synthetic_rate", "unit": "tokens_per_second", "method": "fixture value"},
        ],
        "repetitions": 2,
        "warmup_runs": 0,
        "run_count": 3,
        "workload_label": "synthetic-workload-label",
        "model_label": None,
        "preconditions": ["fixture-only test"],
        "notes": "No benchmark is executed.",
        "evidence_state": "PLANNED",
    }
    data.update(updates)
    return data


def _manifest_data(digest: str, **updates):
    data = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "artifact_id": "synthetic-artifact-a",
        "plan_id": "synthetic-plan-a",
        "artifact_path": "fixtures/synthetic-result.json",
        "sha256": digest,
        "collector_id": "synthetic-fixture-writer",
        "collector_version": "0",
        "timestamp": "2026-08-30T00:00:00Z",
        "local_only": True,
        "notes": "Provenance metadata only.",
    }
    data.update(updates)
    return data


def test_plan_is_strict_planned_and_deterministic() -> None:
    data = _plan_data(metrics=list(reversed(_plan_data()["metrics"])))
    first = MeasurementPlan.from_dict(data)
    second = MeasurementPlan.from_dict(json.loads(json.dumps(data)))
    assert first.to_dict() == second.to_dict()
    assert [item["name"] for item in first.to_dict()["metrics"]] == [
        "synthetic_latency", "synthetic_rate"
    ]
    assert first.evidence_state == "PLANNED"


@pytest.mark.parametrize(
    ("updates", "message"),
    [
        ({"plan_id": " "}, "plan_id"),
        ({"metrics": []}, "at least one metric"),
        ({"metrics": [{"name": "value", "unit": "watts", "method": "fixture"}]}, "unit"),
        (
            {"metrics": [
                {"name": "Value", "unit": "count", "method": "fixture"},
                {"name": "value", "unit": "count", "method": "fixture"},
            ]},
            "duplicate metric",
        ),
        ({"repetitions": 0}, "positive integer"),
        ({"repetitions": True}, "positive integer"),
        ({"warmup_runs": -1}, "nonnegative integer"),
        ({"run_count": 0}, "positive integer"),
        ({"evidence_state": "MEASURED"}, "remain PLANNED"),
    ],
)
def test_plan_rejects_malformed_inputs(updates, message) -> None:
    with pytest.raises(ValueError, match=message):
        MeasurementPlan.from_dict(_plan_data(**updates))


def test_plan_rejects_unknown_or_missing_fields() -> None:
    with pytest.raises(ValueError, match="unexpected"):
        MeasurementPlan.from_dict({**_plan_data(), "result": 1})
    data = _plan_data()
    del data["runtime"]
    with pytest.raises(ValueError, match="missing"):
        MeasurementPlan.from_dict(data)


@pytest.mark.parametrize(
    ("updates", "message"),
    [
        ({"sha256": "abc"}, "sha256"),
        ({"sha256": "A" * 64}, "sha256"),
        ({"artifact_path": "/tmp/result.json"}, "relative POSIX"),
        ({"artifact_path": "../result.json"}, "path segments"),
        ({"artifact_path": "nested/../result.json"}, "path segments"),
        ({"artifact_path": "C:\\result.json"}, "relative POSIX"),
        ({"local_only": False}, "local_only"),
    ],
)
def test_manifest_rejects_invalid_integrity_and_paths(updates, message) -> None:
    with pytest.raises(ValueError, match=message):
        MeasurementArtifactManifest.from_dict(_manifest_data("0" * 64, **updates))


def test_manifest_rejects_raw_or_sensitive_payload_fields() -> None:
    for field in ("raw_prompt", "user_document", "mac", "serial", "uuid", "credential"):
        with pytest.raises(ValueError, match="unexpected artifact manifest fields"):
            MeasurementArtifactManifest.from_dict(
                {**_manifest_data("0" * 64), field: "must-not-be-stored"}
            )


def test_verification_and_measured_observation_require_matching_provenance(tmp_path) -> None:
    artifact = tmp_path / "fixtures" / "synthetic-result.json"
    artifact.parent.mkdir()
    artifact.write_text('{"synthetic_fixture": true}\n', encoding="utf-8")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    plan = MeasurementPlan.from_dict(_plan_data())
    manifest = MeasurementArtifactManifest.from_dict(_manifest_data(digest))

    assert verify_artifact(plan, manifest, tmp_path) == artifact.resolve()
    observation = build_measured_observation(
        plan,
        manifest,
        tmp_path,
        observation_id="synthetic-observation-a",
        metrics={"synthetic_rate": 2.0, "synthetic_latency": 1.0},
        notes="Synthetic contract test only.",
    )
    assert observation.evidence_state == "MEASURED"
    assert list(observation.metrics) == ["synthetic_latency", "synthetic_rate"]
    assert observation.source == "fixtures/synthetic-result.json"

    mismatched_plan = MeasurementArtifactManifest.from_dict(_manifest_data(digest, plan_id="other"))
    with pytest.raises(ValueError, match="plan_id"):
        verify_artifact(plan, mismatched_plan, tmp_path)
    mismatched_hash = MeasurementArtifactManifest.from_dict(_manifest_data("0" * 64))
    with pytest.raises(ValueError, match="SHA-256"):
        verify_artifact(plan, mismatched_hash, tmp_path)
    artifact.unlink()
    with pytest.raises(ValueError, match="missing"):
        verify_artifact(plan, manifest, tmp_path)


def test_measured_observation_requires_exact_explicit_numeric_metrics(tmp_path) -> None:
    artifact = tmp_path / "fixtures" / "synthetic-result.json"
    artifact.parent.mkdir()
    artifact.write_bytes(b"fixture")
    plan = MeasurementPlan.from_dict(_plan_data())
    manifest = MeasurementArtifactManifest.from_dict(
        _manifest_data(hashlib.sha256(artifact.read_bytes()).hexdigest())
    )
    with pytest.raises(ValueError, match="exactly match"):
        build_measured_observation(
            plan, manifest, tmp_path, observation_id="obs", metrics={"synthetic_latency": 1.0}
        )
    with pytest.raises(ValueError, match="finite numbers"):
        build_measured_observation(
            plan,
            manifest,
            tmp_path,
            observation_id="obs",
            metrics={"synthetic_latency": 1.0, "synthetic_rate": True},
        )
