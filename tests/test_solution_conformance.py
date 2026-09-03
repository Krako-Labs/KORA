from __future__ import annotations

import hashlib
import json
import shutil
import socket
from pathlib import Path
from typing import Any

import pytest

from kora.cli import main
from kora.solution import (
    CONFORMANCE_REPORT_SCHEMA,
    SolutionConformanceError,
    run_solution_conformance,
    scaffold_solution,
    validate_contract_instance,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
HELLO_SOLUTION = REPO_ROOT / "examples" / "solutions" / "hello-solution"
DOCUMENT_SOLUTION = REPO_ROOT / "examples" / "solutions" / "document-transform-fixture"
GENERATED_SOLUTION = REPO_ROOT / "examples" / "solutions" / "generated-echo-fixture"


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _copy_scaffold(tmp_path: Path) -> Path:
    package = tmp_path / "package"
    scaffold_solution("example.negative", package)
    return package


def _refresh_integrity(package: Path) -> None:
    manifest_path = package / "solution.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative in manifest["integrity"]["files"]:
        manifest["integrity"]["files"][relative] = hashlib.sha256(
            (package / relative).read_bytes()
        ).hexdigest()
    _write_json(manifest_path, manifest)


@pytest.mark.parametrize(
    "package",
    [HELLO_SOLUTION, DOCUMENT_SOLUTION, GENERATED_SOLUTION],
    ids=["hello", "document-transform", "generated"],
)
def test_reference_packages_share_conformance_entrypoint(package: Path) -> None:
    report = run_solution_conformance(package)

    assert report["status"] == "passed"
    assert report["protocol_version"] == "kora.dev/v0alpha1"
    assert report["runtime"]["id"] == "kora.reference"
    assert report["summary"]["failed"] == 0
    assert report["activity"] == {
        "execution_performed": True,
        "network_accessed": False,
        "model_inference_performed": False,
        "gpu_execution_performed": False,
    }
    validate_contract_instance(CONFORMANCE_REPORT_SCHEMA, report)


def test_expectation_mismatch_returns_valid_failed_report(tmp_path: Path) -> None:
    package = _copy_scaffold(tmp_path)
    case_path = package / "conformance" / "cases" / "echo-success.json"
    case = json.loads(case_path.read_text(encoding="utf-8"))
    case["expected"]["output"] = {"message": "different"}
    _write_json(case_path, case)
    _refresh_integrity(package)

    report = run_solution_conformance(package)

    assert report["status"] == "failed"
    assert report["summary"] == {"total": 1, "passed": 0, "failed": 1}
    checks = {item["name"]: item["passed"] for item in report["cases"][0]["checks"]}
    assert checks["output"] is False
    validate_contract_instance(CONFORMANCE_REPORT_SCHEMA, report)


@pytest.mark.parametrize("mutation", ["invalid_input", "invalid_output"])
def test_runtime_contract_rejections_fail_conformance(
    tmp_path: Path,
    mutation: str,
) -> None:
    package = _copy_scaffold(tmp_path)
    if mutation == "invalid_input":
        case_path = package / "conformance" / "cases" / "echo-success.json"
        case = json.loads(case_path.read_text(encoding="utf-8"))
        case["input"] = {"wrong": "field"}
        _write_json(case_path, case)
    else:
        schema_path = package / "schemas" / "output.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["required"] = ["other"]
        schema["properties"] = {"other": {"type": "string"}}
        _write_json(schema_path, schema)
    _refresh_integrity(package)

    report = run_solution_conformance(package)

    assert report["status"] == "failed"
    assert report["cases"][0]["lifecycle_state"] == "failed"
    checks = {item["name"]: item["passed"] for item in report["cases"][0]["checks"]}
    assert checks["lifecycle_state"] is False


def test_declared_expected_input_failure_can_conform(tmp_path: Path) -> None:
    package = _copy_scaffold(tmp_path)
    case_path = package / "conformance" / "cases" / "echo-success.json"
    case = json.loads(case_path.read_text(encoding="utf-8"))
    case["case_id"] = "invalid-input"
    case["input"] = {"wrong": "field"}
    case["expected"] = {
        "lifecycle_state": "failed",
        "validation": {"input": "invalid", "output": "not_run"},
        "output": None,
        "error_code": "input_validation_failed",
        "capabilities_executed": [],
        "lifecycle_history": ["created", "validating", "failed"],
    }
    _write_json(case_path, case)
    _refresh_integrity(package)

    report = run_solution_conformance(package)

    assert report["status"] == "passed"
    assert report["activity"]["execution_performed"] is False


def test_conformance_case_passes_explicit_approval_grant(tmp_path: Path) -> None:
    package = _copy_scaffold(tmp_path)
    graph_path = package / "graph" / "workflow.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["tasks"][0]["in"] = {}
    graph["tasks"][0]["run"]["spec"] = {
        "handler": "approval.require",
        "args": {"approval": "fixture.approved"},
    }
    graph["tasks"][0]["tags"] = ["side_effect:fixture.approved"]
    _write_json(graph_path, graph)

    output_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["approval", "approved"],
        "properties": {
            "approval": {"const": "fixture.approved"},
            "approved": {"const": True},
        },
    }
    _write_json(package / "schemas" / "output.schema.json", output_schema)

    manifest_path = package / "solution.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["requires"]["capabilities"] = ["approval.require"]
    manifest["policy"]["sideEffects"] = ["fixture.approved"]
    manifest["policy"]["approvals"] = ["fixture.approved"]
    _write_json(manifest_path, manifest)

    case_path = package / "conformance" / "cases" / "echo-success.json"
    case = json.loads(case_path.read_text(encoding="utf-8"))
    case["approvals"] = ["fixture.approved"]
    case["expected"]["output"] = {
        "approval": "fixture.approved",
        "approved": True,
    }
    case["expected"]["capabilities_executed"] = ["approval.require"]
    _write_json(case_path, case)
    _refresh_integrity(package)

    report = run_solution_conformance(package)

    assert report["status"] == "passed"


def test_deliberate_runtime_failure_can_be_an_expected_case(tmp_path: Path) -> None:
    package = _copy_scaffold(tmp_path)
    graph_path = package / "graph" / "workflow.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["tasks"][0]["in"] = {}
    graph["tasks"][0]["run"]["spec"] = {"handler": "fixture.fail", "args": {}}
    _write_json(graph_path, graph)

    manifest_path = package / "solution.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["requires"]["capabilities"] = ["fixture.fail"]
    _write_json(manifest_path, manifest)

    case_path = package / "conformance" / "cases" / "echo-success.json"
    case = json.loads(case_path.read_text(encoding="utf-8"))
    case["case_id"] = "deliberate-failure"
    case["expected"] = {
        "lifecycle_state": "failed",
        "validation": {"input": "valid", "output": "not_run"},
        "output": None,
        "error_code": "deliberate_failure",
        "capabilities_executed": [],
        "lifecycle_history": ["created", "validating", "running", "failed"],
    }
    _write_json(case_path, case)
    _refresh_integrity(package)

    report = run_solution_conformance(package)

    assert report["status"] == "passed"
    assert report["cases"][0]["lifecycle_state"] == "failed"


@pytest.mark.parametrize(
    ("mutation", "expected_detail"),
    [
        ("tamper", "integrity_mismatch"),
        ("missing_capability", "missing_capability"),
        ("undeclared_side_effect", "undeclared_side_effect"),
    ],
)
def test_negative_package_matrix_fails_closed(
    tmp_path: Path,
    mutation: str,
    expected_detail: str,
) -> None:
    package = _copy_scaffold(tmp_path)
    graph_path = package / "graph" / "workflow.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    manifest_path = package / "solution.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if mutation == "tamper":
        graph_path.write_bytes(graph_path.read_bytes() + b"\n")
    elif mutation == "missing_capability":
        graph["tasks"][0]["run"]["spec"]["handler"] = "missing.capability"
        manifest["requires"]["capabilities"] = ["missing.capability"]
        _write_json(graph_path, graph)
        _write_json(manifest_path, manifest)
        _refresh_integrity(package)
    else:
        graph["tasks"][0]["tags"] = ["side_effect:local.file.write"]
        _write_json(graph_path, graph)
        _refresh_integrity(package)

    with pytest.raises(SolutionConformanceError) as captured:
        run_solution_conformance(package)

    assert captured.value.code == "package_validation_failed"
    assert expected_detail in captured.value.detail


def test_malformed_or_unbound_case_is_rejected(
    tmp_path: Path,
) -> None:
    malformed = _copy_scaffold(tmp_path)
    case_path = malformed / "conformance" / "cases" / "echo-success.json"
    _write_json(case_path, {"case_id": "incomplete"})
    _refresh_integrity(malformed)
    with pytest.raises(SolutionConformanceError) as captured:
        run_solution_conformance(malformed)
    assert captured.value.code == "invalid_conformance_case"

    unbound = tmp_path / "unbound"
    shutil.copytree(GENERATED_SOLUTION, unbound)
    manifest_path = unbound / "solution.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    del manifest["integrity"]["files"]["conformance/cases/echo-success.json"]
    _write_json(manifest_path, manifest)
    with pytest.raises(SolutionConformanceError) as captured:
        run_solution_conformance(unbound)
    assert captured.value.code == "conformance_case_not_integrity_bound"


def test_conformance_attempts_no_network(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    package = _copy_scaffold(tmp_path)

    def deny_socket(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "socket", deny_socket)
    report = run_solution_conformance(package)

    assert report["status"] == "passed"
    assert report["activity"]["network_accessed"] is False


def test_conform_cli_failed_report_uses_exit_one(tmp_path: Path, capsys) -> None:
    package = _copy_scaffold(tmp_path)
    case_path = package / "conformance" / "cases" / "echo-success.json"
    case = json.loads(case_path.read_text(encoding="utf-8"))
    case["expected"]["output"] = {"message": "not-the-runtime-output"}
    _write_json(case_path, case)
    _refresh_integrity(package)

    assert main(["solution", "conform", str(package), "--json"]) == 1
    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert captured.err == ""
    assert report["status"] == "failed"
