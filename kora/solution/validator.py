"""Offline, fail-closed validation for KORA Solution Protocol v0 packages."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from kora.task_ir import TaskGraph, normalize_graph, validate_graph

from .reference_runtime import DOCUMENT_PDF_CAPABILITIES, REFERENCE_CAPABILITIES

SUPPORTED_API_VERSION = "kora.dev/v0alpha1"
DEFAULT_REFERENCE_CAPABILITIES = REFERENCE_CAPABILITIES | DOCUMENT_PDF_CAPABILITIES
MANIFEST_NAME = "solution.json"
SCHEMA_NAME = "solution-manifest.schema.json"


@dataclass(frozen=True, order=True)
class SolutionValidationIssue:
    """A stable, machine-readable package validation issue."""

    code: str
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


class SolutionValidationError(ValueError):
    """Raised when a Solution Package fails one or more validation gates."""

    def __init__(self, issues: Iterable[SolutionValidationIssue]):
        ordered = tuple(sorted(issues))
        if not ordered:
            raise ValueError("SolutionValidationError requires at least one issue")
        self.issues = ordered
        super().__init__("; ".join(f"{issue.code}: {issue.message}" for issue in ordered))

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": "invalid",
            "issues": [issue.to_dict() for issue in self.issues],
        }


def _issue(code: str, message: str, path: str = "") -> SolutionValidationError:
    return SolutionValidationError([SolutionValidationIssue(code=code, message=message, path=path)])


def _load_json(path: Path, *, code: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise _issue(code, f"required file not found: {path.name}", str(path)) from exc
    except IsADirectoryError as exc:
        raise _issue(code, f"expected a file: {path.name}", str(path)) from exc
    except UnicodeDecodeError as exc:
        raise _issue(code, f"file is not valid UTF-8: {path.name}", str(path)) from exc
    except json.JSONDecodeError as exc:
        raise _issue(
            code,
            f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
            str(path),
        ) from exc


def _resolve_package_file(root: Path, relative: str, *, code: str) -> Path:
    rel_path = Path(relative)
    if rel_path.is_absolute() or ".." in rel_path.parts:
        raise _issue(code, f"path must stay within the package: {relative}", relative)

    unresolved = root / rel_path
    if unresolved.is_symlink():
        raise _issue(code, f"symbolic links are not allowed in validated package files: {relative}", relative)

    try:
        resolved = unresolved.resolve(strict=True)
    except FileNotFoundError as exc:
        raise _issue(code, f"required package file not found: {relative}", relative) from exc

    if not resolved.is_relative_to(root):
        raise _issue(code, f"path resolves outside the package: {relative}", relative)
    if not resolved.is_file():
        raise _issue(code, f"expected a regular file: {relative}", relative)
    return resolved


def _manifest_schema() -> dict[str, Any]:
    path = Path(__file__).with_name("schemas") / SCHEMA_NAME
    payload = _load_json(path, code="internal_schema_error")
    if not isinstance(payload, dict):
        raise _issue("internal_schema_error", "bundled manifest schema must be a JSON object", str(path))
    return payload


def _validate_manifest_shape(manifest: Any) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        raise _issue("manifest_schema_error", "solution.json must contain a JSON object", MANIFEST_NAME)

    api_version = manifest.get("apiVersion")
    if isinstance(api_version, str) and api_version != SUPPORTED_API_VERSION:
        raise _issue(
            "unsupported_protocol_version",
            f"supported apiVersion is {SUPPORTED_API_VERSION}; received {api_version}",
            "apiVersion",
        )

    validator = Draft202012Validator(_manifest_schema())
    issues = []
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path)
        issues.append(
            SolutionValidationIssue(
                code="manifest_schema_error",
                message=error.message,
                path=location,
            )
        )
    if issues:
        raise SolutionValidationError(issues)
    return manifest


def _external_schema_references(payload: Any) -> list[str]:
    locations: list[str] = []

    def visit(value: Any, location: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_location = f"{location}.{key}"
                if (
                    key in {"$ref", "$dynamicRef", "$recursiveRef"}
                    and isinstance(child, str)
                    and not child.startswith("#")
                ):
                    locations.append(child_location)
                visit(child, child_location)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{location}[{index}]")

    visit(payload, "$")
    return sorted(locations)


def _validate_json_schema(path: Path, *, label: str) -> None:
    payload = _load_json(path, code="referenced_schema_error")
    if not isinstance(payload, dict):
        raise _issue("referenced_schema_error", f"{label} schema must be a JSON object", str(path))
    try:
        Draft202012Validator.check_schema(payload)
    except SchemaError as exc:
        raise _issue("referenced_schema_error", f"invalid {label} JSON Schema: {exc.message}", str(path)) from exc
    if _external_schema_references(payload):
        raise _issue(
            "referenced_schema_error",
            f"{label} schema contains external references; offline schemas may use fragment references only",
            str(path),
        )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_integrity(root: Path, manifest: dict[str, Any]) -> list[str]:
    integrity = manifest["integrity"]
    expected_files: dict[str, str] = integrity["files"]
    referenced = {
        manifest["inputs"]["schema"],
        manifest["graph"]["source"],
        manifest["outputs"]["schema"],
    }
    missing = sorted(referenced - set(expected_files))
    if missing:
        raise SolutionValidationError(
            SolutionValidationIssue(
                code="integrity_reference_missing",
                message=f"referenced file is absent from integrity.files: {relative}",
                path=relative,
            )
            for relative in missing
        )

    issues: list[SolutionValidationIssue] = []
    verified: list[str] = []
    for relative, expected in sorted(expected_files.items()):
        try:
            path = _resolve_package_file(root, relative, code="integrity_file_error")
        except SolutionValidationError as exc:
            issues.extend(exc.issues)
            continue
        actual = _sha256(path)
        if actual != expected:
            issues.append(
                SolutionValidationIssue(
                    code="integrity_mismatch",
                    message=f"SHA-256 mismatch for {relative}",
                    path=relative,
                )
            )
        else:
            verified.append(relative)
    if issues:
        raise SolutionValidationError(issues)
    return verified


def _validate_graph_and_policy(
    graph_path: Path,
    manifest: dict[str, Any],
    *,
    available_capabilities: frozenset[str],
) -> tuple[list[str], list[str]]:
    payload = _load_json(graph_path, code="task_graph_error")
    try:
        graph = normalize_graph(TaskGraph.model_validate(payload))
        validate_graph(graph)
    except (ValueError, TypeError) as exc:
        raise _issue("task_graph_error", str(exc), manifest["graph"]["source"]) from exc

    declared = set(manifest["requires"]["capabilities"])
    used: set[str] = set()
    effects: set[str] = set()
    for task in graph.tasks:
        if task.run.kind == "det":
            used.add(task.run.spec.handler)
        else:
            used.add(task.run.spec.adapter)
        effects.update(
            tag.removeprefix("side_effect:")
            for tag in task.tags
            if tag.startswith("side_effect:") and tag != "side_effect:"
        )

    issues: list[SolutionValidationIssue] = []
    for capability in sorted(used - declared):
        issues.append(
            SolutionValidationIssue(
                code="undeclared_capability",
                message=f"Task Graph uses undeclared capability: {capability}",
                path="requires.capabilities",
            )
        )
    for capability in sorted(declared - available_capabilities):
        issues.append(
            SolutionValidationIssue(
                code="missing_capability",
                message=f"Host does not provide required capability: {capability}",
                path="requires.capabilities",
            )
        )

    policy = manifest["policy"]
    declared_effects = set(policy["sideEffects"])
    approvals = set(policy["approvals"])
    for effect in sorted(effects - declared_effects):
        issues.append(
            SolutionValidationIssue(
                code="undeclared_side_effect",
                message=f"Task Graph uses undeclared side effect: {effect}",
                path="policy.sideEffects",
            )
        )
    for effect in sorted(declared_effects - approvals):
        issues.append(
            SolutionValidationIssue(
                code="missing_approval",
                message=f"side effect requires explicit approval declaration: {effect}",
                path="policy.approvals",
            )
        )
    if policy["network"] == "allowed" and "network.access" not in approvals:
        issues.append(
            SolutionValidationIssue(
                code="missing_approval",
                message="network access requires network.access approval",
                path="policy.approvals",
            )
        )
    if issues:
        raise SolutionValidationError(issues)
    return sorted(declared), sorted(used)


def validate_solution_package(
    package_root: str | Path,
    *,
    available_capabilities: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Validate a Solution Package without executing it or accessing the network."""

    root = Path(package_root).expanduser()
    try:
        root = root.resolve(strict=True)
    except FileNotFoundError as exc:
        raise _issue("package_not_found", f"package directory not found: {package_root}", str(package_root)) from exc
    if not root.is_dir():
        raise _issue("package_not_directory", f"package root is not a directory: {package_root}", str(root))

    manifest_path = root / MANIFEST_NAME
    if manifest_path.is_symlink():
        raise _issue("manifest_file_error", "solution.json must not be a symbolic link", MANIFEST_NAME)
    manifest = _validate_manifest_shape(_load_json(manifest_path, code="manifest_file_error"))

    verified_files = _validate_integrity(root, manifest)

    input_schema_path = _resolve_package_file(
        root,
        manifest["inputs"]["schema"],
        code="referenced_schema_error",
    )
    output_schema_path = _resolve_package_file(
        root,
        manifest["outputs"]["schema"],
        code="referenced_schema_error",
    )
    graph_path = _resolve_package_file(
        root,
        manifest["graph"]["source"],
        code="task_graph_error",
    )
    _validate_json_schema(input_schema_path, label="input")
    _validate_json_schema(output_schema_path, label="output")

    capabilities = frozenset(
        DEFAULT_REFERENCE_CAPABILITIES
        if available_capabilities is None
        else available_capabilities
    )
    declared, used = _validate_graph_and_policy(
        graph_path,
        manifest,
        available_capabilities=capabilities,
    )

    return {
        "status": "valid",
        "api_version": manifest["apiVersion"],
        "solution_id": manifest["metadata"]["id"],
        "solution_version": manifest["metadata"]["version"],
        "declared_capabilities": declared,
        "used_capabilities": used,
        "verified_files": verified_files,
        "execution_performed": False,
        "network_accessed": False,
    }
