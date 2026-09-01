from __future__ import annotations

import hashlib
import json
import shutil
import socket
from pathlib import Path
from typing import Any

import pytest

from kora.solution import (
    REFERENCE_CAPABILITIES,
    RESULT_ENVELOPE_SCHEMA,
    RUNTIME_STATUS_SCHEMA,
    LocalSolutionHost,
    ReferenceRuntime,
    SolutionHostError,
    SolutionValidationError,
    validate_contract_instance,
    validate_solution_package,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
HELLO_SOLUTION = REPO_ROOT / "examples" / "solutions" / "hello-solution"
DOCUMENT_SOLUTION = REPO_ROOT / "examples" / "solutions" / "document-transform-fixture"


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _copy_solution(tmp_path: Path, source: Path = HELLO_SOLUTION) -> Path:
    target = tmp_path / f"solution-{len(list(tmp_path.iterdir()))}"
    shutil.copytree(source, target)
    return target


def _load_manifest(package: Path) -> dict[str, Any]:
    return json.loads((package / "solution.json").read_text(encoding="utf-8"))


def _refresh_integrity(package: Path) -> None:
    manifest = _load_manifest(package)
    for relative in manifest["integrity"]["files"]:
        manifest["integrity"]["files"][relative] = hashlib.sha256(
            (package / relative).read_bytes()
        ).hexdigest()
    _write_json(package / "solution.json", manifest)


def _object_schema(properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": properties,
    }


def _configure_single_task(
    package: Path,
    *,
    solution_id: str,
    capability: str,
    task_input: dict[str, Any],
    args: dict[str, Any] | None = None,
    effects: list[str] | None = None,
    approvals: list[str] | None = None,
    input_schema: dict[str, Any] | None = None,
    output_schema: dict[str, Any] | None = None,
) -> None:
    graph_path = package / "graph" / "workflow.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["graph_id"] = solution_id
    graph["root"] = "fixture"
    graph["tasks"] = [
        {
            "id": "fixture",
            "type": "deterministic",
            "deps": [],
            "in": task_input,
            "run": {
                "kind": "det",
                "spec": {
                    "handler": capability,
                    "args": args or {},
                },
            },
            "policy": {"on_fail": "fail"},
            "tags": [f"side_effect:{effect}" for effect in effects or []],
        }
    ]
    _write_json(graph_path, graph)

    if input_schema is not None:
        _write_json(package / "schemas" / "input.schema.json", input_schema)
    if output_schema is not None:
        _write_json(package / "schemas" / "output.schema.json", output_schema)

    manifest = _load_manifest(package)
    manifest["metadata"]["id"] = solution_id
    manifest["requires"]["capabilities"] = [capability]
    manifest["policy"]["sideEffects"] = effects or []
    manifest["policy"]["approvals"] = approvals or []
    _write_json(package / "solution.json", manifest)
    _refresh_integrity(package)


def _codes(exc: SolutionValidationError) -> set[str]:
    return {issue.code for issue in exc.issues}


def test_two_reference_solutions_share_protocol_and_install_without_core_changes(
    tmp_path: Path,
) -> None:
    hello_report = validate_solution_package(HELLO_SOLUTION)
    document_report = validate_solution_package(DOCUMENT_SOLUTION)
    assert hello_report["api_version"] == document_report["api_version"] == "kora.dev/v0alpha1"

    host = LocalSolutionHost(tmp_path / "host")
    hello_receipt = host.install(HELLO_SOLUTION)
    document_receipt = host.install(DOCUMENT_SOLUTION)

    assert hello_receipt["solution"] == {"id": "example.hello", "version": "0.1.0"}
    assert document_receipt["solution"] == {
        "id": "example.document-transform",
        "version": "0.1.0",
    }
    assert hello_receipt["activity"]["execution_performed"] is False
    assert document_receipt["activity"]["network_accessed"] is False


def test_deterministic_runs_persist_valid_result_and_lifecycle_contracts(
    tmp_path: Path,
) -> None:
    host = LocalSolutionHost(tmp_path / "host")
    host.install(HELLO_SOLUTION)
    host.install(DOCUMENT_SOLUTION)

    hello = host.run("example.hello", {"message": "Hello"})
    first = host.run(
        "example.document-transform",
        {"text": "  Alpha\r\n\r\n\r\n  Beta    value  "},
    )
    second = host.run(
        "example.document-transform",
        {"text": "  Alpha\r\n\r\n\r\n  Beta    value  "},
    )

    assert hello["output"] == {"message": "Hello"}
    assert first["output"] == second["output"] == {"text": "Alpha\n\nBeta value"}
    assert first["activity"] == {
        "execution_performed": True,
        "network_accessed": False,
        "model_inference_performed": False,
        "gpu_execution_performed": False,
        "capabilities_executed": ["text.normalize"],
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
    validate_contract_instance(RUNTIME_STATUS_SCHEMA, status)
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, persisted)


def test_invalid_input_fails_before_runtime_execution(tmp_path: Path) -> None:
    host = LocalSolutionHost(tmp_path / "host")
    host.install(DOCUMENT_SOLUTION)

    result = host.run("example.document-transform", {"wrong": "field"})

    assert result["lifecycle_state"] == "failed"
    assert result["validation"] == {"input": "invalid", "output": "not_run"}
    assert result["error"]["code"] == "input_validation_failed"
    assert result["activity"]["execution_performed"] is False
    status = host.status(result["run_id"])
    assert [entry["state"] for entry in status["history"]] == [
        "created",
        "validating",
        "failed",
    ]


def test_invalid_runtime_output_is_rejected_by_declared_schema(
    tmp_path: Path,
) -> None:
    package = _copy_solution(tmp_path)
    _configure_single_task(
        package,
        solution_id="example.invalid-output",
        capability="det.echo",
        task_input={"message": "$.message"},
        input_schema=_object_schema({"message": {"type": "string"}}, ["message"]),
        output_schema=_object_schema({"other": {"type": "string"}}, ["other"]),
    )
    host = LocalSolutionHost(tmp_path / "host")
    host.install(package)

    result = host.run("example.invalid-output", {"message": "value"})

    assert result["lifecycle_state"] == "failed"
    assert result["validation"] == {"input": "valid", "output": "invalid"}
    assert result["error"]["code"] == "output_validation_failed"
    assert result["activity"]["execution_performed"] is True
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, result)


def test_missing_runtime_capability_rejects_install(tmp_path: Path) -> None:
    class EchoOnlyRuntime(ReferenceRuntime):
        @property
        def capabilities(self) -> frozenset[str]:
            return frozenset({"det.echo"})

    host = LocalSolutionHost(tmp_path / "host", runtime=EchoOnlyRuntime())

    with pytest.raises(SolutionValidationError) as captured:
        host.install(DOCUMENT_SOLUTION)

    assert _codes(captured.value) == {"missing_capability"}


def test_undeclared_side_effect_rejects_install(tmp_path: Path) -> None:
    package = _copy_solution(tmp_path)
    graph_path = package / "graph" / "workflow.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["tasks"][0]["tags"] = ["side_effect:local.file.write"]
    _write_json(graph_path, graph)
    _refresh_integrity(package)

    with pytest.raises(SolutionValidationError) as captured:
        LocalSolutionHost(tmp_path / "host").install(package)

    assert _codes(captured.value) == {"undeclared_side_effect"}


def test_installed_package_tampering_fails_before_execution(tmp_path: Path) -> None:
    host = LocalSolutionHost(tmp_path / "host")
    host.install(HELLO_SOLUTION)
    graph = (
        host.store_root
        / "installed"
        / "example.hello"
        / "0.1.0"
        / "package"
        / "graph"
        / "workflow.json"
    )
    graph.write_bytes(graph.read_bytes() + b"\n")

    result = host.run("example.hello", {"message": "Hello"})

    assert result["lifecycle_state"] == "failed"
    assert result["validation"] == {"input": "not_run", "output": "not_run"}
    assert result["error"]["code"] == "integrity_mismatch"
    assert result["activity"]["execution_performed"] is False
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, result)


def test_deliberate_runtime_failure_produces_valid_result_envelope(
    tmp_path: Path,
) -> None:
    package = _copy_solution(tmp_path)
    _configure_single_task(
        package,
        solution_id="example.deliberate-failure",
        capability="fixture.fail",
        task_input={},
        input_schema=_object_schema({}, []),
        output_schema=_object_schema({}, []),
    )
    host = LocalSolutionHost(tmp_path / "host")
    host.install(package)

    result = host.run("example.deliberate-failure", {})

    assert result["lifecycle_state"] == "failed"
    assert result["validation"] == {"input": "valid", "output": "not_run"}
    assert result["error"] == {
        "code": "deliberate_failure",
        "detail": "deliberate failure fixture invoked",
    }
    assert result["activity"]["execution_performed"] is True
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, result)


def test_approval_required_fixture_fails_closed_then_runs_when_granted(
    tmp_path: Path,
) -> None:
    package = _copy_solution(tmp_path)
    approval = "fixture.approved"
    _configure_single_task(
        package,
        solution_id="example.approval-required",
        capability="approval.require",
        task_input={},
        args={"approval": approval},
        effects=[approval],
        approvals=[approval],
        input_schema=_object_schema({}, []),
        output_schema=_object_schema(
            {
                "approval": {"const": approval},
                "approved": {"const": True},
            },
            ["approval", "approved"],
        ),
    )
    host = LocalSolutionHost(tmp_path / "host")
    host.install(package)

    rejected = host.run("example.approval-required", {})
    accepted = host.run(
        "example.approval-required",
        {},
        approvals=[approval],
    )

    assert rejected["error"]["code"] == "approval_required"
    assert rejected["activity"]["execution_performed"] is False
    assert accepted["lifecycle_state"] == "succeeded"
    assert accepted["output"] == {"approval": approval, "approved": True}


def test_bounded_local_file_roundtrip_stays_inside_run_directory(
    tmp_path: Path,
) -> None:
    package = _copy_solution(tmp_path)
    solution_id = "example.file-roundtrip"
    input_schema = _object_schema(
        {
            "path": {"type": "string"},
            "content": {"type": "string"},
        },
        ["path", "content"],
    )
    output_schema = _object_schema({"content": {"type": "string"}}, ["content"])
    _write_json(package / "schemas" / "input.schema.json", input_schema)
    _write_json(package / "schemas" / "output.schema.json", output_schema)
    graph = {
        "graph_id": solution_id,
        "version": "0.1",
        "root": "read",
        "defaults": {
            "budget": {"max_time_ms": 1000, "max_tokens": 0, "max_retries": 0}
        },
        "tasks": [
            {
                "id": "write",
                "type": "deterministic",
                "deps": [],
                "in": {"path": "$.path", "content": "$.content"},
                "run": {
                    "kind": "det",
                    "spec": {"handler": "local.file.write", "args": {}},
                },
                "policy": {"on_fail": "fail"},
                "tags": ["side_effect:local.file.write"],
            },
            {
                "id": "read",
                "type": "deterministic",
                "deps": ["write"],
                "in": {"path": "$.path"},
                "run": {
                    "kind": "det",
                    "spec": {"handler": "local.file.read", "args": {}},
                },
                "policy": {"on_fail": "fail"},
                "tags": [],
            },
        ],
    }
    _write_json(package / "graph" / "workflow.json", graph)
    manifest = _load_manifest(package)
    manifest["metadata"]["id"] = solution_id
    manifest["requires"]["capabilities"] = ["local.file.read", "local.file.write"]
    manifest["policy"]["sideEffects"] = ["local.file.write"]
    manifest["policy"]["approvals"] = ["local.file.write"]
    _write_json(package / "solution.json", manifest)
    _refresh_integrity(package)

    host = LocalSolutionHost(tmp_path / "host")
    host.install(package)
    result = host.run(
        solution_id,
        {"path": "nested/note.txt", "content": "bounded content"},
        approvals=["local.file.write"],
    )

    assert result["lifecycle_state"] == "succeeded"
    assert result["output"] == {"content": "bounded content"}
    workspace_file = (
        host.store_root / "runs" / result["run_id"] / "workspace" / "nested" / "note.txt"
    )
    assert workspace_file.read_text(encoding="utf-8") == "bounded content"

    escaped = host.run(
        solution_id,
        {"path": "../escape.txt", "content": "blocked"},
        approvals=["local.file.write"],
    )
    assert escaped["lifecycle_state"] == "failed"
    assert escaped["error"]["code"] == "runtime_failure"
    assert not (host.store_root / "runs" / escaped["run_id"] / "escape.txt").exists()

    oversized = host.run(
        solution_id,
        {"path": "too-large.txt", "content": "x" * (1024 * 1024 + 1)},
        approvals=["local.file.write"],
    )
    assert oversized["lifecycle_state"] == "failed"
    assert oversized["error"]["code"] == "runtime_failure"
    assert not (
        host.store_root / "runs" / oversized["run_id"] / "workspace" / "too-large.txt"
    ).exists()


def test_reference_runtime_uses_no_network_model_or_gpu(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def deny_socket(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "socket", deny_socket)
    host = LocalSolutionHost(tmp_path / "host")
    host.install(DOCUMENT_SOLUTION)
    result = host.run("example.document-transform", {"text": "  Offline   text "})

    assert result["lifecycle_state"] == "succeeded"
    assert all(
        "network" not in capability
        and "model" not in capability
        and "gpu" not in capability
        for capability in REFERENCE_CAPABILITIES
    )
    assert result["activity"]["network_accessed"] is False
    assert result["activity"]["model_inference_performed"] is False
    assert result["activity"]["gpu_execution_performed"] is False


def test_corrupt_persisted_contracts_fail_closed(tmp_path: Path) -> None:
    host = LocalSolutionHost(tmp_path / "host")
    host.install(HELLO_SOLUTION)
    result = host.run("example.hello", {"message": "Hello"})
    run_directory = host.store_root / "runs" / result["run_id"]

    corrupt_result = json.loads((run_directory / "result.json").read_text(encoding="utf-8"))
    corrupt_result["activity"]["network_accessed"] = True
    _write_json(run_directory / "result.json", corrupt_result)
    with pytest.raises(SolutionHostError) as result_error:
        host.result(result["run_id"])
    assert result_error.value.code == "invalid_result_envelope"

    corrupt_status = json.loads((run_directory / "status.json").read_text(encoding="utf-8"))
    corrupt_status["activity"]["gpu_execution_performed"] = True
    _write_json(run_directory / "status.json", corrupt_status)
    with pytest.raises(SolutionHostError) as status_error:
        host.status(result["run_id"])
    assert status_error.value.code == "invalid_runtime_status"


def test_external_schema_reference_is_rejected_without_network(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    package = _copy_solution(tmp_path)
    _write_json(
        package / "schemas" / "input.schema.json",
        {"$ref": "https://example.invalid/external.schema.json"},
    )
    _refresh_integrity(package)

    def deny_socket(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "socket", deny_socket)
    with pytest.raises(SolutionValidationError) as captured:
        LocalSolutionHost(tmp_path / "host").install(package)

    assert _codes(captured.value) == {"referenced_schema_error"}


def test_host_rejects_symlinked_store_directories(tmp_path: Path) -> None:
    store = tmp_path / "host"
    outside = tmp_path / "outside"
    store.mkdir()
    outside.mkdir()
    (store / "runs").symlink_to(outside, target_is_directory=True)

    with pytest.raises(SolutionHostError) as captured:
        LocalSolutionHost(store)

    assert captured.value.code == "invalid_store"


def test_reference_host_rejects_model_task_even_with_capability_alias(
    tmp_path: Path,
) -> None:
    package = _copy_solution(tmp_path)
    graph_path = package / "graph" / "workflow.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["tasks"][0]["run"] = {
        "kind": "llm",
        "spec": {
            "adapter": "det.echo",
            "input": {},
            "output_schema": {"type": "object"},
        },
    }
    _write_json(graph_path, graph)
    _refresh_integrity(package)

    with pytest.raises(SolutionHostError) as captured:
        LocalSolutionHost(tmp_path / "host").install(package)

    assert captured.value.code == "unsupported_runtime_task_kind"


def test_reference_host_rejects_network_allowed_manifest(tmp_path: Path) -> None:
    package = _copy_solution(tmp_path)
    manifest = _load_manifest(package)
    manifest["policy"]["network"] = "allowed"
    manifest["policy"]["approvals"] = ["network.access"]
    _write_json(package / "solution.json", manifest)

    with pytest.raises(SolutionHostError) as captured:
        LocalSolutionHost(tmp_path / "host").install(package)

    assert captured.value.code == "network_policy_not_supported"
