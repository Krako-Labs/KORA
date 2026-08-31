from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from kora.solution import SolutionValidationError, validate_solution_package


REPO_ROOT = Path(__file__).resolve().parents[1]
HELLO_SOLUTION = REPO_ROOT / "examples" / "solutions" / "hello-solution"


def _copy_solution(tmp_path: Path) -> Path:
    target = tmp_path / "solution"
    shutil.copytree(HELLO_SOLUTION, target)
    return target


def _load_manifest(package: Path) -> dict:
    return json.loads((package / "solution.json").read_text(encoding="utf-8"))


def _write_manifest(package: Path, manifest: dict) -> None:
    (package / "solution.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_graph_and_refresh_digest(package: Path, graph: dict) -> None:
    graph_path = package / "graph" / "workflow.json"
    graph_path.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = _load_manifest(package)
    manifest["integrity"]["files"]["graph/workflow.json"] = hashlib.sha256(
        graph_path.read_bytes()
    ).hexdigest()
    _write_manifest(package, manifest)


def _codes(exc: SolutionValidationError) -> set[str]:
    return {issue.code for issue in exc.issues}


def test_hello_solution_validates_offline() -> None:
    result = validate_solution_package(HELLO_SOLUTION)

    assert result["status"] == "valid"
    assert result["solution_id"] == "example.hello"
    assert result["declared_capabilities"] == ["det.echo"]
    assert result["execution_performed"] is False
    assert result["network_accessed"] is False
    assert result["verified_files"] == [
        "graph/workflow.json",
        "schemas/input.schema.json",
        "schemas/output.schema.json",
    ]


def test_unsupported_protocol_version_fails_before_execution(tmp_path: Path) -> None:
    package = _copy_solution(tmp_path)
    manifest = _load_manifest(package)
    manifest["apiVersion"] = "kora.dev/v1"
    _write_manifest(package, manifest)

    with pytest.raises(SolutionValidationError) as captured:
        validate_solution_package(package)

    assert _codes(captured.value) == {"unsupported_protocol_version"}


def test_tampered_file_fails_integrity(tmp_path: Path) -> None:
    package = _copy_solution(tmp_path)
    graph_path = package / "graph" / "workflow.json"
    graph_path.write_text(graph_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    with pytest.raises(SolutionValidationError) as captured:
        validate_solution_package(package)

    assert "integrity_mismatch" in _codes(captured.value)


def test_cycle_fails_graph_validation_after_valid_integrity(tmp_path: Path) -> None:
    package = _copy_solution(tmp_path)
    graph = json.loads((package / "graph" / "workflow.json").read_text(encoding="utf-8"))
    graph["tasks"][0]["deps"] = ["hello"]
    _write_graph_and_refresh_digest(package, graph)

    with pytest.raises(SolutionValidationError) as captured:
        validate_solution_package(package)

    assert _codes(captured.value) == {"task_graph_error"}
    assert "cycle" in str(captured.value).lower()


def test_undeclared_capability_fails_closed(tmp_path: Path) -> None:
    package = _copy_solution(tmp_path)
    graph = json.loads((package / "graph" / "workflow.json").read_text(encoding="utf-8"))
    graph["tasks"][0]["run"]["spec"]["handler"] = "text.normalize"
    _write_graph_and_refresh_digest(package, graph)

    with pytest.raises(SolutionValidationError) as captured:
        validate_solution_package(package)

    assert "undeclared_capability" in _codes(captured.value)


def test_missing_host_capability_fails_closed() -> None:
    with pytest.raises(SolutionValidationError) as captured:
        validate_solution_package(HELLO_SOLUTION, available_capabilities=set())

    assert _codes(captured.value) == {"missing_capability"}


def test_side_effect_requires_declaration_and_approval(tmp_path: Path) -> None:
    package = _copy_solution(tmp_path)
    graph = json.loads((package / "graph" / "workflow.json").read_text(encoding="utf-8"))
    graph["tasks"][0]["tags"] = ["side_effect:artifact.write"]
    _write_graph_and_refresh_digest(package, graph)

    with pytest.raises(SolutionValidationError) as captured:
        validate_solution_package(package)

    assert _codes(captured.value) == {"undeclared_side_effect"}


def test_parent_traversal_path_is_rejected_by_manifest_schema(tmp_path: Path) -> None:
    package = _copy_solution(tmp_path)
    manifest = _load_manifest(package)
    manifest["inputs"]["schema"] = "../outside.json"
    _write_manifest(package, manifest)

    with pytest.raises(SolutionValidationError) as captured:
        validate_solution_package(package)

    assert _codes(captured.value) == {"manifest_schema_error"}
