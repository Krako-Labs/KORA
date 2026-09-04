"""Deterministic, offline reference capability runtime for Solution conformance."""

from __future__ import annotations

import importlib.util
import re
import sqlite3
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kora.research import ResearchFoundry, ResearchFoundryError
from kora.task_ir import Task, TaskGraph

REFERENCE_CAPABILITIES = frozenset(
    {
        "approval.require",
        "det.echo",
        "fixture.fail",
        "local.file.read",
        "local.file.write",
        "text.normalize",
    }
)
DOCUMENT_PDF_CAPABILITY = "document.pdf.lexical-query"
DOCUMENT_PDF_CAPABILITIES = frozenset({DOCUMENT_PDF_CAPABILITY})
MAX_LOCAL_FILE_BYTES = 1024 * 1024
MAX_PDF_FILES = 16
MAX_PDF_CORPUS_BYTES = 8 * 1024 * 1024


class ReferenceRuntimeError(RuntimeError):
    """A bounded runtime error safe for a machine-readable result envelope."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(detail)


@dataclass(frozen=True)
class RuntimeExecution:
    """Successful reference-runtime output and executed capability evidence."""

    output: dict[str, Any]
    capabilities_executed: tuple[str, ...]


def _resolve_json_path(payload: Any, expression: str) -> Any:
    if expression == "$":
        return payload
    if not expression.startswith("$."):
        return expression

    current = payload
    for part in expression[2:].split("."):
        if not part or not isinstance(current, dict) or part not in current:
            raise ReferenceRuntimeError(
                "runtime_failure",
                "task input mapping could not be resolved",
            )
        current = current[part]
    return current


def _resolve_value(value: Any, payload: dict[str, Any]) -> Any:
    if isinstance(value, str):
        return _resolve_json_path(payload, value)
    if isinstance(value, list):
        return [_resolve_value(item, payload) for item in value]
    if isinstance(value, dict):
        return {key: _resolve_value(item, payload) for key, item in value.items()}
    return value


def _topological_tasks(graph: TaskGraph) -> list[Task]:
    remaining = {task.id: task for task in graph.tasks}
    completed: set[str] = set()
    ordered: list[Task] = []
    while remaining:
        ready = sorted(
            (task for task in remaining.values() if set(task.deps) <= completed),
            key=lambda task: task.id,
        )
        if not ready:
            raise ReferenceRuntimeError("runtime_failure", "task graph cannot be scheduled")
        for task in ready:
            ordered.append(task)
            completed.add(task.id)
            del remaining[task.id]
    return ordered


def _normalize_text(params: dict[str, Any]) -> dict[str, Any]:
    text = params.get("text")
    if not isinstance(text, str):
        raise ReferenceRuntimeError("runtime_failure", "text.normalize requires string input")

    trim = params.get("trim", True)
    collapse_whitespace = params.get("collapse_whitespace", True)
    collapse_blank_lines = params.get("collapse_blank_lines", True)
    if not all(isinstance(value, bool) for value in (trim, collapse_whitespace, collapse_blank_lines)):
        raise ReferenceRuntimeError("runtime_failure", "text.normalize options must be booleans")

    normalized = unicodedata.normalize("NFKC", text).replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    if collapse_whitespace:
        lines = [re.sub(r"[^\S\n]+", " ", line) for line in lines]
    if trim:
        lines = [line.strip() for line in lines]
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
    if collapse_blank_lines:
        collapsed: list[str] = []
        for line in lines:
            if line or not collapsed or collapsed[-1]:
                collapsed.append(line)
        lines = collapsed
    return {"text": "\n".join(lines)}


def _workspace_path(workspace: Path, relative: Any, *, for_write: bool) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ReferenceRuntimeError("runtime_failure", "local file path must be a non-empty string")
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ReferenceRuntimeError("runtime_failure", "local file path must remain inside the run directory")

    current = workspace
    for part in rel.parts[:-1]:
        current = current / part
        if current.exists() and current.is_symlink():
            raise ReferenceRuntimeError("runtime_failure", "symbolic links are not allowed in run files")
    target = workspace / rel
    if target.exists() and target.is_symlink():
        raise ReferenceRuntimeError("runtime_failure", "symbolic links are not allowed in run files")

    resolved_workspace = workspace.resolve()
    resolved_target = target.resolve(strict=False)
    if not resolved_target.is_relative_to(resolved_workspace):
        raise ReferenceRuntimeError("runtime_failure", "local file path escaped the run directory")

    if for_write:
        resolved_target.parent.mkdir(parents=True, exist_ok=True)
    return resolved_target


def _write_local_file(
    workspace: Path,
    params: dict[str, Any],
    approvals: frozenset[str],
) -> dict[str, Any]:
    if "local.file.write" not in approvals:
        raise ReferenceRuntimeError("approval_required", "required approval was not granted")
    content = params.get("content")
    if not isinstance(content, str):
        raise ReferenceRuntimeError("runtime_failure", "local.file.write requires string content")
    encoded = content.encode("utf-8")
    if len(encoded) > MAX_LOCAL_FILE_BYTES:
        raise ReferenceRuntimeError("runtime_failure", "local file exceeds the bounded size limit")

    target = _workspace_path(workspace, params.get("path"), for_write=True)
    if target.exists() and not target.is_file():
        raise ReferenceRuntimeError("runtime_failure", "local file target must be a regular file")
    target.write_bytes(encoded)
    return {"path": str(Path(params["path"])), "bytes_written": len(encoded)}


def _read_local_file(workspace: Path, params: dict[str, Any]) -> dict[str, Any]:
    target = _workspace_path(workspace, params.get("path"), for_write=False)
    if not target.exists() or not target.is_file():
        raise ReferenceRuntimeError("runtime_failure", "local file was not found in the run directory")
    if target.stat().st_size > MAX_LOCAL_FILE_BYTES:
        raise ReferenceRuntimeError("runtime_failure", "local file exceeds the bounded size limit")
    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ReferenceRuntimeError("runtime_failure", "local file is not valid UTF-8") from exc
    return {"content": content}


def _package_directory(package_root: Path | None, relative: Any) -> Path:
    if package_root is None:
        raise ReferenceRuntimeError("runtime_failure", "package assets are unavailable")
    if not isinstance(relative, str) or not relative:
        raise ReferenceRuntimeError(
            "runtime_failure",
            "package asset path must be a non-empty string",
        )
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ReferenceRuntimeError(
            "runtime_failure",
            "package asset path must remain inside the installed package",
        )
    candidate = package_root / rel
    if candidate.is_symlink() or not candidate.is_dir():
        raise ReferenceRuntimeError(
            "runtime_failure",
            "package PDF corpus was not found",
        )
    resolved_root = package_root.resolve()
    resolved = candidate.resolve()
    if not resolved.is_relative_to(resolved_root):
        raise ReferenceRuntimeError(
            "runtime_failure",
            "package asset path escaped the installed package",
        )
    return resolved


def _document_pdf_lexical_query(
    workspace: Path,
    package_root: Path | None,
    params: dict[str, Any],
) -> dict[str, Any]:
    corpus = _package_directory(package_root, params.get("corpus"))
    pdfs = sorted(
        path
        for path in corpus.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    )
    if not pdfs or len(pdfs) > MAX_PDF_FILES:
        raise ReferenceRuntimeError(
            "runtime_failure",
            "package PDF corpus is empty or exceeds the bounded file limit",
        )
    if any(path.is_symlink() for path in pdfs):
        raise ReferenceRuntimeError(
            "runtime_failure",
            "package PDF corpus contains a symbolic link",
        )
    if sum(path.stat().st_size for path in pdfs) > MAX_PDF_CORPUS_BYTES:
        raise ReferenceRuntimeError(
            "runtime_failure",
            "package PDF corpus exceeds the bounded byte limit",
        )

    query = params.get("query")
    top_k = params.get("top_k", 5)
    if not isinstance(query, str) or not query.strip():
        raise ReferenceRuntimeError("runtime_failure", "lexical query must not be empty")
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 20:
        raise ReferenceRuntimeError(
            "runtime_failure",
            "top_k must be an integer from 1 to 20",
        )

    try:
        foundry = ResearchFoundry(workspace / "research-state")
        foundry.ingest(corpus)
        return foundry.query(query, top_k=top_k)
    except ResearchFoundryError as exc:
        raise ReferenceRuntimeError(
            "runtime_failure",
            "document PDF lexical query failed closed",
        ) from exc


def document_pdf_runtime_available() -> bool:
    """Return whether the optional local PDF and SQLite FTS5 dependencies exist."""

    if importlib.util.find_spec("pypdf") is None:
        return False
    try:
        with sqlite3.connect(":memory:") as connection:
            connection.execute("CREATE VIRTUAL TABLE capability_probe USING fts5(text)")
    except sqlite3.Error:
        return False
    return True


class ReferenceRuntime:
    """Execute only the bounded deterministic capabilities in this module."""

    runtime_id = "kora.reference"
    runtime_version = "0.1.0"
    priority = 100

    @property
    def capabilities(self) -> frozenset[str]:
        return REFERENCE_CAPABILITIES

    @property
    def descriptor(self) -> dict[str, Any]:
        """Return the validated static descriptor used by local resolution."""

        return {
            "schema_version": "kora.runtime.descriptor/v0alpha1",
            "runtime": {"id": self.runtime_id, "version": self.runtime_version},
            "protocol_versions": ["kora.dev/v0alpha1"],
            "capabilities": sorted(self.capabilities),
            "task_kinds": ["det"],
            "priority": self.priority,
            "execution": {
                "network_access": False,
                "model_inference": False,
                "gpu_execution": False,
            },
        }

    def execute(
        self,
        graph: TaskGraph,
        input_payload: dict[str, Any],
        *,
        run_directory: Path,
        package_root: Path | None = None,
        approvals: Iterable[str] = (),
        declared_side_effects: Iterable[str] = (),
    ) -> RuntimeExecution:
        workspace = run_directory / "workspace"
        workspace.mkdir(parents=True, exist_ok=False)
        granted = frozenset(approvals)
        declared = frozenset(declared_side_effects)
        outputs: dict[str, dict[str, Any]] = {}
        executed: list[str] = []

        for task in _topological_tasks(graph):
            if task.run.kind != "det":
                raise ReferenceRuntimeError(
                    "runtime_failure",
                    "reference runtime does not execute model-backed tasks",
                )
            capability = task.run.spec.handler
            if capability not in self.capabilities:
                raise ReferenceRuntimeError("runtime_failure", "required capability is unavailable")

            effects = {
                tag.removeprefix("side_effect:")
                for tag in task.tags
                if tag.startswith("side_effect:") and tag != "side_effect:"
            }
            if not effects <= declared:
                raise ReferenceRuntimeError("runtime_failure", "task requested an undeclared side effect")
            if not effects <= granted:
                raise ReferenceRuntimeError("approval_required", "required approval was not granted")

            dynamic = _resolve_value(task.in_, input_payload)
            if not isinstance(dynamic, dict):
                raise ReferenceRuntimeError("runtime_failure", "task input mapping must produce an object")
            params = dict(task.run.spec.args)
            if set(params) & set(dynamic):
                raise ReferenceRuntimeError("runtime_failure", "task input and static arguments overlap")
            params.update(dynamic)

            output = self._execute_capability(
                capability,
                params,
                workspace=workspace,
                approvals=granted,
                package_root=package_root,
            )
            if capability not in executed:
                executed.append(capability)
            outputs[task.id] = output

        root_output = outputs.get(graph.root)
        if not isinstance(root_output, dict):
            raise ReferenceRuntimeError("runtime_failure", "root task did not produce an object")
        return RuntimeExecution(output=root_output, capabilities_executed=tuple(executed))

    def _execute_capability(
        self,
        capability: str,
        params: dict[str, Any],
        *,
        workspace: Path,
        approvals: frozenset[str],
        package_root: Path | None,
    ) -> dict[str, Any]:
        if capability == "det.echo":
            return dict(params)
        if capability == "text.normalize":
            return _normalize_text(params)
        if capability == "local.file.write":
            return _write_local_file(workspace, params, approvals)
        if capability == "local.file.read":
            return _read_local_file(workspace, params)
        if capability == "fixture.fail":
            raise ReferenceRuntimeError(
                "deliberate_failure",
                "deliberate failure fixture invoked",
            )
        if capability == "approval.require":
            approval = params.get("approval")
            if not isinstance(approval, str) or not approval:
                raise ReferenceRuntimeError(
                    "runtime_failure",
                    "approval.require needs a named approval",
                )
            if approval not in approvals:
                raise ReferenceRuntimeError("approval_required", "required approval was not granted")
            return {"approval": approval, "approved": True}
        raise ReferenceRuntimeError("runtime_failure", "required capability is unavailable")


class DocumentPdfReferenceRuntime(ReferenceRuntime):
    """Optional bounded runtime for package-local text-layer PDF retrieval."""

    runtime_id = "kora.document-pdf-reference"
    runtime_version = "0.1.0"

    @property
    def capabilities(self) -> frozenset[str]:
        return DOCUMENT_PDF_CAPABILITIES

    def _execute_capability(
        self,
        capability: str,
        params: dict[str, Any],
        *,
        workspace: Path,
        approvals: frozenset[str],
        package_root: Path | None,
    ) -> dict[str, Any]:
        if capability == DOCUMENT_PDF_CAPABILITY:
            return _document_pdf_lexical_query(workspace, package_root, params)
        raise ReferenceRuntimeError("runtime_failure", "required capability is unavailable")


def default_reference_runtimes() -> tuple[ReferenceRuntime, ...]:
    """Return only reference runtimes whose local dependencies are available."""

    runtimes: list[ReferenceRuntime] = [ReferenceRuntime()]
    if document_pdf_runtime_available():
        runtimes.append(DocumentPdfReferenceRuntime())
    return tuple(runtimes)


__all__ = [
    "DOCUMENT_PDF_CAPABILITIES",
    "DOCUMENT_PDF_CAPABILITY",
    "MAX_LOCAL_FILE_BYTES",
    "MAX_PDF_CORPUS_BYTES",
    "MAX_PDF_FILES",
    "REFERENCE_CAPABILITIES",
    "DocumentPdfReferenceRuntime",
    "ReferenceRuntime",
    "ReferenceRuntimeError",
    "RuntimeExecution",
    "default_reference_runtimes",
    "document_pdf_runtime_available",
]
