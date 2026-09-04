from __future__ import annotations

import hashlib
import json
import shutil
import socket
from pathlib import Path
from typing import Any

import pytest

from kora.solution import (
    CONFORMANCE_REPORT_SCHEMA,
    RESULT_ENVELOPE_SCHEMA,
    RUNTIME_STATUS_SCHEMA,
    LocalSolutionHost,
    ReferenceRuntime,
    SolutionValidationError,
    document_pdf_runtime_available,
    run_solution_conformance,
    validate_contract_instance,
    validate_solution_package,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_SOLUTION = (
    REPO_ROOT / "examples" / "solutions" / "research-foundry-reference"
)
SOLUTION_ID = "example.research-foundry-reference"
QUERY = {"query": "deterministic routing", "top_k": 3}
APPROVALS = ["local.file.write"]


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _refresh_integrity(package: Path) -> None:
    manifest_path = package / "solution.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative in manifest["integrity"]["files"]:
        manifest["integrity"]["files"][relative] = hashlib.sha256(
            (package / relative).read_bytes()
        ).hexdigest()
    _write_json(manifest_path, manifest)


def _expected_query_output() -> dict[str, Any]:
    case = json.loads(
        (
            RESEARCH_SOLUTION
            / "conformance"
            / "cases"
            / "query-success.json"
        ).read_text(encoding="utf-8")
    )
    return case["expected"]["output"]


def test_research_foundry_solution_uses_same_host_lifecycle_and_repeats(
    tmp_path: Path,
) -> None:
    assert document_pdf_runtime_available() is True
    validation = validate_solution_package(RESEARCH_SOLUTION)
    assert validation["status"] == "valid"
    assert validation["declared_capabilities"] == [
        "document.pdf.lexical-query"
    ]

    host = LocalSolutionHost(tmp_path / "host")
    receipt = host.install(RESEARCH_SOLUTION)
    assert receipt["solution"] == {"id": SOLUTION_ID, "version": "0.1.0"}
    assert receipt["runtime_resolution"]["id"] == "kora.document-pdf-reference"
    assert receipt["activity"] == {
        "execution_performed": False,
        "network_accessed": False,
        "model_inference_performed": False,
        "gpu_execution_performed": False,
    }

    first = host.run(SOLUTION_ID, QUERY, approvals=APPROVALS)
    second = host.run(SOLUTION_ID, QUERY, approvals=APPROVALS)

    assert first["output"] == second["output"] == _expected_query_output()
    assert first["activity"] == {
        "execution_performed": True,
        "network_accessed": False,
        "model_inference_performed": False,
        "gpu_execution_performed": False,
        "capabilities_executed": ["document.pdf.lexical-query"],
    }
    status = host.status(first["run_id"])
    persisted = host.result(first["run_id"])
    assert [entry["state"] for entry in status["history"]] == [
        "created",
        "validating",
        "running",
        "succeeded",
    ]
    assert persisted == first
    state = (
        host.store_root
        / "runs"
        / first["run_id"]
        / "workspace"
        / "research-state"
        / "research-foundry.sqlite3"
    )
    assert state.is_file()
    validate_contract_instance(RUNTIME_STATUS_SCHEMA, status)
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, persisted)


def test_research_foundry_conformance_is_integrity_bound_and_offline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def deny_socket(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "socket", deny_socket)
    report = run_solution_conformance(RESEARCH_SOLUTION)

    assert report["status"] == "passed"
    assert report["summary"] == {"total": 4, "passed": 4, "failed": 0}
    assert report["runtime"]["id"] == "kora.document-pdf-reference"
    assert {case["case_id"] for case in report["cases"]} == {
        "invalid-input",
        "missing-approval",
        "no-hit",
        "query-success",
    }
    assert report["activity"] == {
        "execution_performed": True,
        "network_accessed": False,
        "model_inference_performed": False,
        "gpu_execution_performed": False,
    }
    validate_contract_instance(CONFORMANCE_REPORT_SCHEMA, report)


def test_research_foundry_missing_approval_returns_machine_readable_failure(
    tmp_path: Path,
) -> None:
    host = LocalSolutionHost(tmp_path / "host")
    host.install(RESEARCH_SOLUTION)

    result = host.run(SOLUTION_ID, QUERY)

    assert result["lifecycle_state"] == "failed"
    assert result["validation"] == {"input": "valid", "output": "not_run"}
    assert result["error"]["code"] == "approval_required"
    assert result["activity"]["execution_performed"] is False
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, result)


def test_research_foundry_installed_asset_tampering_fails_before_execution(
    tmp_path: Path,
) -> None:
    host = LocalSolutionHost(tmp_path / "host")
    host.install(RESEARCH_SOLUTION)
    installed_pdf = (
        host.store_root
        / "installed"
        / SOLUTION_ID
        / "0.1.0"
        / "package"
        / "assets"
        / "corpus"
        / "reference.pdf"
    )
    installed_pdf.write_bytes(installed_pdf.read_bytes() + b"\n")

    result = host.run(SOLUTION_ID, QUERY, approvals=APPROVALS)

    assert result["lifecycle_state"] == "failed"
    assert result["error"]["code"] == "integrity_mismatch"
    assert result["activity"]["execution_performed"] is False
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, result)


def test_research_foundry_package_path_escape_fails_closed(tmp_path: Path) -> None:
    package = tmp_path / "package"
    shutil.copytree(RESEARCH_SOLUTION, package)
    graph_path = package / "graph" / "workflow.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["tasks"][0]["run"]["spec"]["args"]["corpus"] = "../outside"
    _write_json(graph_path, graph)
    _refresh_integrity(package)

    host = LocalSolutionHost(tmp_path / "host")
    host.install(package)
    result = host.run(SOLUTION_ID, QUERY, approvals=APPROVALS)

    assert result["lifecycle_state"] == "failed"
    assert result["error"] == {
        "code": "runtime_failure",
        "detail": "package asset path must remain inside the installed package",
    }
    assert result["activity"]["execution_performed"] is True
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, result)


def test_research_foundry_requires_the_optional_document_runtime(
    tmp_path: Path,
) -> None:
    host = LocalSolutionHost(tmp_path / "host", runtime=ReferenceRuntime())

    with pytest.raises(SolutionValidationError) as captured:
        host.install(RESEARCH_SOLUTION)

    assert {issue.code for issue in captured.value.issues} == {
        "missing_capability"
    }
