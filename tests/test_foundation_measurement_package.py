from __future__ import annotations

import hashlib
import json

import pytest

from kora.cli import main
from kora.foundation.evidence_registry import (
    VerifiedEvidenceRecord,
    append_evidence,
    empty_evidence_registry,
)
from kora.foundation.measurement_contract import MANIFEST_SCHEMA_VERSION, PLAN_SCHEMA_VERSION
from kora.foundation.measurement_package import (
    SCHEMA_VERSION,
    MeasurementPackage,
    assemble_verified_evidence,
    serialize_verified_evidence,
)


def _plan_data(**updates):
    data = {
        "schema_version": PLAN_SCHEMA_VERSION,
        "plan_id": "fixture-plan-a",
        "node_labels": ["fixture-node"],
        "runtime": "fixture-runtime",
        "hardware": "fixture-hardware",
        "transport": "none",
        "topology": "single-node",
        "metrics": [
            {"name": "fixture_latency", "unit": "milliseconds", "method": "fixture"},
            {"name": "fixture_rate", "unit": "tokens_per_second", "method": "fixture"},
        ],
        "repetitions": 1,
        "warmup_runs": 0,
        "run_count": 1,
        "workload_label": "fixture-only",
        "model_label": None,
        "preconditions": ["synthetic fixture only"],
        "notes": None,
        "evidence_state": "PLANNED",
    }
    data.update(updates)
    return data


def _manifest_data(digest: str, **updates):
    data = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "artifact_id": "fixture-artifact-a",
        "plan_id": "fixture-plan-a",
        "artifact_path": "fixtures/result.json",
        "sha256": digest,
        "collector_id": "fixture-writer",
        "collector_version": "0",
        "timestamp": "2026-08-30T00:00:00Z",
        "local_only": True,
        "notes": None,
    }
    data.update(updates)
    return data


def _package_data(digest: str, **updates):
    data = {
        "schema_version": SCHEMA_VERSION,
        "package_id": "fixture-package-a",
        "measurement_plan": _plan_data(),
        "artifact_manifest": _manifest_data(digest),
        "metrics": {"fixture_rate": 2.0, "fixture_latency": 1.0},
        "observation_id": "fixture-observation-a",
        "notes": "Synthetic contract test only.",
    }
    data.update(updates)
    return data


def _fixture(tmp_path):
    artifact = tmp_path / "fixtures" / "result.json"
    artifact.parent.mkdir()
    artifact.write_text('{"synthetic_fixture":true}\n', encoding="utf-8")
    return artifact, hashlib.sha256(artifact.read_bytes()).hexdigest()


def test_package_shape_ids_plan_state_and_deterministic_round_trip(tmp_path) -> None:
    _, digest = _fixture(tmp_path)
    package = MeasurementPackage.from_dict(_package_data(digest))
    assert package.measurement_plan.evidence_state == "PLANNED"
    assert list(package.metrics) == ["fixture_latency", "fixture_rate"]
    assert MeasurementPackage.from_dict(package.to_dict()).to_dict() == package.to_dict()
    assert list(package.to_dict()) == [
        "schema_version", "package_id", "measurement_plan", "artifact_manifest",
        "metrics", "observation_id", "notes",
    ]
    for field in ("package_id", "observation_id"):
        with pytest.raises(ValueError, match=field):
            MeasurementPackage.from_dict(_package_data(digest, **{field: " "}))
    with pytest.raises(ValueError, match="unexpected measurement package fields"):
        MeasurementPackage.from_dict({**_package_data(digest), "raw_payload": "forbidden"})


@pytest.mark.parametrize(
    "metrics,message",
    [
        ({"fixture_latency": 1.0}, "missing"),
        ({"fixture_latency": 1.0, "fixture_rate": 2.0, "extra": 3.0}, "unexpected"),
        ({"fixture_latency": True, "fixture_rate": 2.0}, "finite numbers"),
        ({"fixture_latency": float("inf"), "fixture_rate": 2.0}, "finite numbers"),
        ({"fixture_latency": float("nan"), "fixture_rate": 2.0}, "finite numbers"),
    ],
)
def test_package_requires_exact_finite_non_bool_metrics(tmp_path, metrics, message) -> None:
    _, digest = _fixture(tmp_path)
    with pytest.raises(ValueError, match=message):
        MeasurementPackage.from_dict(_package_data(digest, metrics=metrics))


def test_package_rejects_lineage_mismatch_sensitive_fields_and_absolute_paths(tmp_path) -> None:
    _, digest = _fixture(tmp_path)
    mismatch = _package_data(digest)
    mismatch["artifact_manifest"] = _manifest_data(digest, plan_id="other-plan")
    with pytest.raises(ValueError, match="plan_id"):
        MeasurementPackage.from_dict(mismatch)
    for field in ("raw_prompt", "user_document", "secret", "mac", "serial", "uuid", "credential"):
        with pytest.raises(ValueError, match="unexpected measurement package fields"):
            MeasurementPackage.from_dict({**_package_data(digest), field: "forbidden"})
    absolute = _package_data(digest)
    absolute["artifact_manifest"] = _manifest_data(digest, artifact_path="/tmp/result.json")
    with pytest.raises(ValueError, match="relative POSIX"):
        MeasurementPackage.from_dict(absolute)


def test_assembly_reuses_hash_and_path_escape_checks_and_registry_accepts_record(tmp_path) -> None:
    artifact, digest = _fixture(tmp_path)
    package = MeasurementPackage.from_dict(_package_data(digest))
    record = assemble_verified_evidence(package, tmp_path)
    assert record.observation.evidence_state == "MEASURED"
    assert record.observation.observation_id == package.observation_id
    assert VerifiedEvidenceRecord.from_dict(json.loads(serialize_verified_evidence(record))) == record
    registry, status = append_evidence(empty_evidence_registry(), record)
    assert status == "appended"
    assert registry.record_count == 1

    artifact.write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="SHA-256"):
        assemble_verified_evidence(package, tmp_path)

    outside = tmp_path.parent / f"{tmp_path.name}-outside.json"
    outside.write_text("outside", encoding="utf-8")
    artifact.unlink()
    artifact.symlink_to(outside)
    escaped_digest = hashlib.sha256(outside.read_bytes()).hexdigest()
    escaped = MeasurementPackage.from_dict(_package_data(escaped_digest))
    with pytest.raises(ValueError, match="outside artifact root"):
        assemble_verified_evidence(escaped, tmp_path)


def test_verified_record_serialization_and_cli_are_deterministic(tmp_path, capsys) -> None:
    _, digest = _fixture(tmp_path)
    package_data = _package_data(digest)
    package_path = tmp_path / "package.json"
    package_path.write_text(json.dumps(package_data), encoding="utf-8")
    package = MeasurementPackage.from_dict(package_data)
    expected = serialize_verified_evidence(assemble_verified_evidence(package, tmp_path))
    assert expected == serialize_verified_evidence(assemble_verified_evidence(package, tmp_path))

    assert main(["system", "package", "assemble", str(package_path), str(tmp_path)]) == 0
    assert capsys.readouterr().out == expected

    output = tmp_path / "nested" / "record.json"
    assert main([
        "system", "package", "assemble", str(package_path), str(tmp_path),
        "--json-out", str(output),
    ]) == 0
    assert output.read_text(encoding="utf-8") == expected
    assert "Verified evidence record saved" in capsys.readouterr().out
