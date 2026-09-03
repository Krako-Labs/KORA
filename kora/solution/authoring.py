"""Deterministic authoring helpers for KORA Solution Protocol packages."""

from __future__ import annotations

import hashlib
import re
import shutil
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .contracts import canonical_json_bytes

SOLUTION_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
VERSION_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?$"
)
MAX_AUTHORED_PACKAGE_FILES = 256
MAX_AUTHORED_PACKAGE_BYTES = 16 * 1024 * 1024
SCAFFOLD_SCHEMA_VERSION = "kora.solution.scaffold/v0alpha1"


class SolutionAuthoringError(ValueError):
    """A bounded authoring failure suitable for CLI output."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = " ".join(detail.split())[:512]
        super().__init__(self.detail)

    def to_dict(self) -> dict[str, Any]:
        return {"status": "error", "error": {"code": self.code, "detail": self.detail}}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(payload))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def integrity_file_digests(
    package_root: str | Path,
    relative_paths: Iterable[str],
) -> dict[str, str]:
    """Hash an explicit, package-confined set for manifest integrity.files."""

    root = Path(package_root).expanduser()
    if root.is_symlink() or not root.is_dir():
        raise SolutionAuthoringError("invalid_package", "package root must be a regular directory")
    root = root.resolve()
    paths = sorted(set(relative_paths))
    if not paths:
        raise SolutionAuthoringError(
            "invalid_integrity_path",
            "at least one integrity file is required",
        )
    if len(paths) > MAX_AUTHORED_PACKAGE_FILES:
        raise SolutionAuthoringError(
            "package_limit_exceeded",
            "integrity set exceeds bounded file limits",
        )
    files: dict[str, str] = {}
    total_bytes = 0
    for relative in paths:
        rel = Path(relative)
        if (
            not relative
            or relative == "solution.json"
            or rel.is_absolute()
            or ".." in rel.parts
        ):
            raise SolutionAuthoringError(
                "invalid_integrity_path",
                "integrity paths must be confined non-manifest package files",
            )
        candidate = root
        for part in rel.parts:
            candidate = candidate / part
            if candidate.is_symlink():
                raise SolutionAuthoringError(
                    "invalid_integrity_path",
                    "integrity paths must not contain symbolic links",
                )
        try:
            path = candidate.resolve(strict=True)
        except FileNotFoundError as exc:
            raise SolutionAuthoringError(
                "invalid_integrity_path",
                "integrity path does not name an existing file",
            ) from exc
        if not path.is_relative_to(root) or not path.is_file():
            raise SolutionAuthoringError(
                "invalid_integrity_path",
                "integrity path must name a regular package file",
            )
        total_bytes += path.stat().st_size
        if total_bytes > MAX_AUTHORED_PACKAGE_BYTES:
            raise SolutionAuthoringError(
                "package_limit_exceeded",
                "integrity set exceeds bounded byte limits",
            )
        files[rel.as_posix()] = _sha256(path)
    return files


def package_file_digests(package_root: str | Path) -> dict[str, str]:
    """Return a stable digest map for every regular package file."""

    root = Path(package_root).expanduser()
    if root.is_symlink() or not root.is_dir():
        raise SolutionAuthoringError("invalid_package", "package root must be a regular directory")
    root = root.resolve()
    files: dict[str, str] = {}
    total_bytes = 0
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise SolutionAuthoringError("invalid_package", "package files must not be symbolic links")
        if path.is_dir():
            continue
        if not path.is_file():
            raise SolutionAuthoringError("invalid_package", "package entries must be regular files")
        total_bytes += path.stat().st_size
        if (
            len(files) >= MAX_AUTHORED_PACKAGE_FILES
            or total_bytes > MAX_AUTHORED_PACKAGE_BYTES
        ):
            raise SolutionAuthoringError(
                "package_limit_exceeded",
                "package exceeds bounded digest limits",
            )
        files[path.relative_to(root).as_posix()] = _sha256(path)
    return files


def package_digest(package_root: str | Path) -> str:
    """Return a deterministic digest for the complete package tree."""

    return hashlib.sha256(canonical_json_bytes(package_file_digests(package_root))).hexdigest()


def _scaffold_payloads(solution_id: str) -> dict[str, bytes]:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["message"],
        "properties": {"message": {"type": "string"}},
    }
    graph = {
        "graph_id": solution_id,
        "version": "0.1",
        "root": "echo",
        "defaults": {
            "budget": {"max_time_ms": 1000, "max_tokens": 0, "max_retries": 0}
        },
        "tasks": [
            {
                "id": "echo",
                "type": "deterministic",
                "deps": [],
                "in": {"message": "$.message"},
                "run": {
                    "kind": "det",
                    "spec": {"handler": "det.echo", "args": {}},
                },
                "policy": {"on_fail": "fail"},
                "tags": [],
            }
        ],
    }
    case = {
        "schema_version": "kora.solution.conformance-case/v0alpha1",
        "case_id": "echo-success",
        "input": {"message": "Hello from a scaffolded Solution"},
        "approvals": [],
        "expected": {
            "lifecycle_state": "succeeded",
            "validation": {"input": "valid", "output": "valid"},
            "output": {"message": "Hello from a scaffolded Solution"},
            "error_code": None,
            "capabilities_executed": ["det.echo"],
            "lifecycle_history": ["created", "validating", "running", "succeeded"],
        },
    }
    readme = (
        f"# {solution_id}\n\n"
        "Deterministic offline KORA Solution scaffold using det.echo.\n\n"
        "Validate and conform this package with the KORA CLI.\n"
    ).encode()
    return {
        "README.md": readme,
        "conformance/cases/echo-success.json": canonical_json_bytes(case),
        "examples/input.json": canonical_json_bytes(case["input"]),
        "graph/workflow.json": canonical_json_bytes(graph),
        "schemas/input.schema.json": canonical_json_bytes(schema),
        "schemas/output.schema.json": canonical_json_bytes(schema),
    }


def scaffold_solution(
    solution_id: str,
    output: str | Path,
    *,
    version: str = "0.1.0",
) -> dict[str, Any]:
    """Create one deterministic, offline echo Solution Package."""

    if not SOLUTION_ID_PATTERN.fullmatch(solution_id) or not (3 <= len(solution_id) <= 128):
        raise SolutionAuthoringError("invalid_solution_id", "Solution id is not valid")
    if not VERSION_PATTERN.fullmatch(version):
        raise SolutionAuthoringError("invalid_solution_version", "Solution version is not valid")

    target = Path(output).expanduser()
    if target.exists() or target.is_symlink():
        raise SolutionAuthoringError("output_exists", "scaffold output path already exists")
    try:
        parent = target.parent.resolve(strict=True)
    except FileNotFoundError as exc:
        raise SolutionAuthoringError(
            "invalid_output_parent", "scaffold output parent does not exist"
        ) from exc
    if not parent.is_dir():
        raise SolutionAuthoringError("invalid_output_parent", "scaffold output parent is not a directory")
    target = parent / target.name
    created = False

    try:
        target.mkdir()
        created = True
        payloads = _scaffold_payloads(solution_id)
        for relative, content in sorted(payloads.items()):
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)

        integrity = integrity_file_digests(target, payloads)
        manifest = {
            "apiVersion": "kora.dev/v0alpha1",
            "kind": "Solution",
            "metadata": {"id": solution_id, "version": version},
            "requires": {"kora": ">=0.1.0a0,<0.2", "capabilities": ["det.echo"]},
            "inputs": {"schema": "schemas/input.schema.json"},
            "graph": {"source": "graph/workflow.json"},
            "outputs": {"schema": "schemas/output.schema.json"},
            "policy": {"network": "denied", "sideEffects": [], "approvals": []},
            "integrity": {"algorithm": "sha256", "files": integrity},
        }
        _write_json(target / "solution.json", manifest)
    except Exception:
        if created and target.exists() and target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        raise

    files = package_file_digests(target)
    return {
        "schema_version": SCAFFOLD_SCHEMA_VERSION,
        "status": "created",
        "solution": {"id": solution_id, "version": version},
        "package_digest": hashlib.sha256(canonical_json_bytes(files)).hexdigest(),
        "files": sorted(files),
        "activity": {
            "execution_performed": False,
            "network_accessed": False,
            "model_inference_performed": False,
            "gpu_execution_performed": False,
        },
    }


__all__ = [
    "MAX_AUTHORED_PACKAGE_BYTES",
    "MAX_AUTHORED_PACKAGE_FILES",
    "SCAFFOLD_SCHEMA_VERSION",
    "SolutionAuthoringError",
    "integrity_file_digests",
    "package_digest",
    "package_file_digests",
    "scaffold_solution",
]
