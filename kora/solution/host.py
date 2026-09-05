"""Bounded local KORA Host lifecycle for deterministic reference Solutions."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import uuid
from collections.abc import Callable, Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kora.task_ir import TaskGraph, normalize_graph, validate_graph

from .contracts import (
    RESULT_ENVELOPE_SCHEMA,
    RUNTIME_STATUS_SCHEMA,
    SolutionContractError,
    canonical_json_bytes,
    load_json_object,
    validate_contract_instance,
    validate_declared_instance,
)
from .reference_runtime import (
    ReferenceRuntime,
    ReferenceRuntimeError,
    default_reference_runtimes,
)
from .runtime_registry import (
    CapabilityRegistryError,
    CapabilityRuntime,
    LocalCapabilityRegistry,
    ResolvedRuntime,
)
from .validator import (
    SUPPORTED_API_VERSION,
    SolutionValidationError,
    validate_solution_package,
)

MAX_PACKAGE_FILES = 256
MAX_PACKAGE_BYTES = 16 * 1024 * 1024
RUN_ID_PATTERN = re.compile(r"^[a-f0-9]{32}$")
SOLUTION_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
VERSION_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?$"
)
RESULT_ERROR_CODES = frozenset(
    {
        "ambiguous_runtime",
        "approval_required",
        "deliberate_failure",
        "incompatible_runtime",
        "input_validation_failed",
        "integrity_mismatch",
        "missing_capability_runtime",
        "output_validation_failed",
        "package_validation_failed",
        "runtime_failure",
        "runtime_integrity_mismatch",
        "runtime_unavailable",
    }
)
TRANSITIONS = {
    "created": frozenset({"validating"}),
    "validating": frozenset({"running", "failed"}),
    "running": frozenset({"succeeded", "failed"}),
    "succeeded": frozenset(),
    "failed": frozenset(),
}


class SolutionHostError(RuntimeError):
    """A fail-closed Host operation error outside an initialized run."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = _bounded_detail(detail)
        super().__init__(self.detail)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": "error",
            "error": {"code": self.code, "detail": self.detail},
        }


def _bounded_detail(detail: str) -> str:
    rendered = " ".join(str(detail).split())
    if not rendered:
        rendered = "operation failed"
    return rendered[:512]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _package_files(root: Path) -> dict[str, str]:
    if root.is_symlink() or not root.is_dir():
        raise SolutionHostError("invalid_package", "package root must be a regular directory")

    files: dict[str, str] = {}
    total_bytes = 0
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise SolutionHostError("invalid_package", "symbolic links are not allowed in installed packages")
        if path.is_dir():
            continue
        if not path.is_file():
            raise SolutionHostError("invalid_package", "package entries must be regular files")
        relative = path.relative_to(root).as_posix()
        total_bytes += path.stat().st_size
        if len(files) >= MAX_PACKAGE_FILES or total_bytes > MAX_PACKAGE_BYTES:
            raise SolutionHostError("package_limit_exceeded", "package exceeds bounded install limits")
        files[relative] = _sha256(path)
    if "solution.json" not in files:
        raise SolutionHostError("invalid_package", "package is missing solution.json")
    return files


def _tree_digest(files: dict[str, str]) -> str:
    return hashlib.sha256(canonical_json_bytes(files)).hexdigest()


def _atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_bytes(canonical_json_bytes(payload))
    temporary.replace(path)


def _copy_package(source: Path, destination: Path, files: dict[str, str]) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for relative in files:
        source_path = source / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target)


class LocalSolutionHost:
    """Validate, install, run, and inspect deterministic local Solutions."""

    def __init__(
        self,
        store_root: str | Path,
        *,
        runtime: CapabilityRuntime | None = None,
        runtimes: Iterable[CapabilityRuntime] | None = None,
        clock: Callable[[], str] | None = None,
        run_id_factory: Callable[[], str] | None = None,
    ):
        self.store_root = Path(store_root).expanduser()
        self.store_root.mkdir(parents=True, exist_ok=True)
        if self.store_root.is_symlink() or not self.store_root.is_dir():
            raise SolutionHostError("invalid_store", "Host store root must be a regular directory")
        self.store_root = self.store_root.resolve()
        if runtime is not None and runtimes is not None:
            raise SolutionHostError("invalid_runtime_configuration", "use runtime or runtimes, not both")
        if runtimes is not None:
            configured_runtimes = tuple(runtimes)
        elif runtime is not None:
            configured_runtimes = (runtime,)
        else:
            configured_runtimes = default_reference_runtimes()
        if not configured_runtimes:
            raise SolutionHostError("invalid_runtime_configuration", "at least one runtime is required")
        self._clock = clock or _utc_now
        self._run_id_factory = run_id_factory or (lambda: uuid.uuid4().hex)
        self.installed_root = self._store_subdirectory("installed", create=True)
        self.runs_root = self._store_subdirectory("runs", create=True)
        self.runtimes_root = self._store_subdirectory("runtimes", create=True)
        try:
            self.runtime_registry = LocalCapabilityRegistry(self.runtimes_root)
            for configured_runtime in configured_runtimes:
                self.runtime_registry.register(configured_runtime)
        except CapabilityRegistryError as exc:
            raise SolutionHostError(exc.code, exc.detail) from exc

    def validate(self, package_root: str | Path) -> dict[str, Any]:
        report = validate_solution_package(
            package_root,
            available_capabilities=self._available_capabilities(),
        )
        package = Path(package_root).expanduser().resolve()
        manifest = load_json_object(package / "solution.json")
        if manifest["policy"]["network"] != "denied":
            raise SolutionHostError(
                "network_policy_not_supported",
                "bounded reference Host accepts only network-denied Solutions",
            )
        graph = TaskGraph.model_validate(load_json_object(package / manifest["graph"]["source"]))
        if any(task.run.kind != "det" for task in graph.tasks):
            raise SolutionHostError(
                "unsupported_runtime_task_kind",
                "bounded reference Host accepts only deterministic Task Graph nodes",
            )
        resolved = self._resolve_runtime(manifest, graph, package)
        report = dict(report)
        report["runtime_resolution"] = resolved.identity
        return report

    def install(self, package_root: str | Path) -> dict[str, Any]:
        source_candidate = Path(package_root).expanduser()
        if source_candidate.is_symlink():
            raise SolutionHostError("invalid_package", "package root must not be a symbolic link")
        source = source_candidate.resolve()
        report = self.validate(source)
        source_files = _package_files(source)
        source_digest = _tree_digest(source_files)
        solution_id = report["solution_id"]
        version = report["solution_version"]
        target = self._install_path(solution_id, version, create_parent=True)

        if target.exists():
            receipt = self._verify_install(target)
            if receipt["package_digest"] != source_digest:
                raise SolutionHostError(
                    "solution_already_installed",
                    "a different package is already installed for this Solution version",
                )
            return receipt

        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.parent / f".install-{uuid.uuid4().hex}"
        try:
            package_copy = temporary / "package"
            _copy_package(source, package_copy, source_files)
            copied_report = self.validate(package_copy)
            copied_files = _package_files(package_copy)
            if copied_files != source_files:
                raise SolutionHostError("integrity_mismatch", "installed package copy failed integrity verification")
            installed_at = self._clock()
            receipt = {
                "schema_version": "kora.solution.install/v0alpha1",
                "protocol_version": copied_report["api_version"],
                "solution": {"id": solution_id, "version": version},
                "runtime_resolution": copied_report["runtime_resolution"],
                "package_digest": source_digest,
                "files": copied_files,
                "installed_at": installed_at,
                "activity": {
                    "execution_performed": False,
                    "network_accessed": False,
                    "model_inference_performed": False,
                    "gpu_execution_performed": False,
                },
            }
            _atomic_write_json(temporary / "install.json", receipt)
            temporary.replace(target)
        except Exception:
            if temporary.exists():
                shutil.rmtree(temporary)
            raise
        return receipt

    def run(
        self,
        solution_id: str,
        input_payload: Any,
        *,
        version: str | None = None,
        approvals: Iterable[str] = (),
    ) -> dict[str, Any]:
        install_path = self._resolve_install(solution_id, version)
        resolved_version = install_path.name
        run_id = self._new_run_id()
        run_directory = self.runs_root / run_id
        run_directory.mkdir(parents=False, exist_ok=False)
        _atomic_write_json(run_directory / "input.json", input_payload)

        created_at = self._clock()
        evidence_reference = f"runs/{run_id}/status.json"
        status: dict[str, Any] = {
            "schema_version": "kora.solution.runtime-status/v0alpha1",
            "protocol_version": SUPPORTED_API_VERSION,
            "solution": {"id": solution_id, "version": resolved_version},
            "runtime": None,
            "run_id": run_id,
            "lifecycle_state": "created",
            "validation": {"input": "not_run", "output": "not_run"},
            "evidence_reference": evidence_reference,
            "error": None,
            "activity": {
                "execution_performed": False,
                "network_accessed": False,
                "model_inference_performed": False,
                "gpu_execution_performed": False,
                "capabilities_executed": [],
            },
            "timestamps": {
                "created_at": created_at,
                "started_at": None,
                "finished_at": None,
                "updated_at": created_at,
            },
            "history": [{"state": "created", "at": created_at}],
        }
        self._persist_status(run_directory, status)
        self._transition(run_directory, status, "validating")

        try:
            self._verify_install(install_path)
            package = install_path / "package"
            validate_solution_package(package, available_capabilities=self._available_capabilities())
            manifest = load_json_object(package / "solution.json")
            if manifest["metadata"] != {"id": solution_id, "version": resolved_version}:
                raise SolutionHostError("integrity_mismatch", "installed Solution identity changed")
            if manifest["policy"]["network"] != "denied":
                raise SolutionHostError(
                    "network_policy_not_supported",
                    "bounded reference Host accepts only network-denied Solutions",
                )
            graph_payload = load_json_object(package / manifest["graph"]["source"])
            graph = normalize_graph(TaskGraph.model_validate(graph_payload))
            validate_graph(graph)
            resolved_runtime = self._resolve_runtime(manifest, graph, package)
            status["runtime"] = resolved_runtime.identity
            self._persist_status(run_directory, status)

            input_schema = package / manifest["inputs"]["schema"]
            input_errors = validate_declared_instance(input_schema, input_payload)
            if input_errors:
                status["validation"]["input"] = "invalid"
                return self._finish_failure(
                    run_directory,
                    status,
                    code="input_validation_failed",
                    detail="input does not conform to the declared schema",
                )
            status["validation"]["input"] = "valid"

            required_approvals = frozenset(manifest["policy"]["approvals"])
            granted_approvals = frozenset(approvals)
            if not required_approvals <= granted_approvals:
                return self._finish_failure(
                    run_directory,
                    status,
                    code="approval_required",
                    detail="one or more declared approvals were not granted",
                )

            status["validation"]["output"] = "pending"
            status["activity"]["execution_performed"] = True
            self._transition(run_directory, status, "running")

            execution = resolved_runtime.runtime.execute(
                graph,
                input_payload,
                run_directory=run_directory,
                package_root=package,
                approvals=granted_approvals,
                declared_side_effects=manifest["policy"]["sideEffects"],
            )
            status["activity"]["capabilities_executed"] = list(execution.capabilities_executed)
            output_schema = package / manifest["outputs"]["schema"]
            output_errors = validate_declared_instance(output_schema, execution.output)
            if output_errors:
                status["validation"]["output"] = "invalid"
                return self._finish_failure(
                    run_directory,
                    status,
                    code="output_validation_failed",
                    detail="runtime output does not conform to the declared schema",
                )
            status["validation"]["output"] = "valid"
            return self._finish_success(run_directory, status, execution.output)

        except SolutionValidationError as exc:
            codes = {issue.code for issue in exc.issues}
            code = "integrity_mismatch" if "integrity_mismatch" in codes else "package_validation_failed"
            return self._finish_failure(
                run_directory,
                status,
                code=code,
                detail="installed package failed pre-execution validation",
            )
        except SolutionHostError as exc:
            code = exc.code if exc.code in RESULT_ERROR_CODES else "package_validation_failed"
            return self._finish_failure(
                run_directory,
                status,
                code=code,
                detail=exc.detail,
            )
        except ReferenceRuntimeError as exc:
            code = exc.code if exc.code in RESULT_ERROR_CODES else "runtime_failure"
            return self._finish_failure(
                run_directory,
                status,
                code=code,
                detail=exc.detail,
            )
        except Exception:  # noqa: BLE001 - initialized runs require a bounded envelope
            return self._finish_failure(
                run_directory,
                status,
                code="runtime_failure",
                detail="bounded reference runtime failed closed",
            )

    def status(self, run_id: str) -> dict[str, Any]:
        run_directory = self._run_path(run_id)
        path = run_directory / "status.json"
        if path.is_symlink() or not path.is_file():
            raise SolutionHostError("run_not_found", "runtime status was not found")
        try:
            payload = load_json_object(path)
            validate_contract_instance(RUNTIME_STATUS_SCHEMA, payload)
        except (OSError, TypeError, ValueError, SolutionContractError) as exc:
            raise SolutionHostError("invalid_runtime_status", "runtime status failed validation") from exc
        return payload

    def result(self, run_id: str) -> dict[str, Any]:
        run_directory = self._run_path(run_id)
        path = run_directory / "result.json"
        if path.is_symlink() or not path.is_file():
            raise SolutionHostError("result_not_found", "run result was not found")
        try:
            payload = load_json_object(path)
            validate_contract_instance(RESULT_ENVELOPE_SCHEMA, payload)
        except (OSError, TypeError, ValueError, SolutionContractError) as exc:
            raise SolutionHostError("invalid_result_envelope", "result envelope failed validation") from exc
        return payload

    def node_evidence(self, run_id: str) -> dict[str, Any]:
        """Read the optional versioned node trace for an initialized node run."""
        path = self._run_path(run_id) / "node-evidence.json"
        if path.is_symlink() or not path.is_file():
            raise SolutionHostError("node_evidence_not_found", "node evidence was not found")
        try:
            payload = load_json_object(path)
            validate_contract_instance("node-evidence.schema.json", payload)
            ids = [node["node_id"] for node in payload["nodes"]]
            if len(ids) != len(set(ids)):
                raise ValueError("duplicate node identities")
        except (OSError, TypeError, ValueError, SolutionContractError) as exc:
            raise SolutionHostError("invalid_node_evidence", "node evidence failed validation") from exc
        return payload

    def runtimes(self) -> dict[str, Any]:
        """Return integrity-verified local runtime registrations."""

        try:
            return self.runtime_registry.list()
        except CapabilityRegistryError as exc:
            raise SolutionHostError(exc.code, exc.detail) from exc

    def _available_capabilities(self) -> frozenset[str]:
        try:
            return self.runtime_registry.available_capabilities
        except CapabilityRegistryError as exc:
            raise SolutionHostError(exc.code, exc.detail) from exc

    def _resolve_runtime(
        self,
        manifest: dict[str, Any],
        graph: TaskGraph,
        package: Path,
    ) -> ResolvedRuntime:
        if "execution" in manifest["graph"]:
            from .node_execution import NodeCoordinator, load_node_plan

            try:
                plan = load_node_plan(package, manifest["graph"]["execution"], graph)
                return NodeCoordinator(plan, graph, self.runtime_registry).resolve()
            except CapabilityRegistryError as exc:
                raise SolutionHostError(exc.code, exc.detail) from exc

        required_capabilities = {
            task.run.spec.handler
            for task in graph.tasks
        }
        task_kinds = {task.run.kind for task in graph.tasks}
        try:
            return self.runtime_registry.resolve(
                required_capabilities,
                protocol_version=manifest["apiVersion"],
                task_kinds=task_kinds,
                allow_network=False,
                allow_model=False,
                allow_gpu=False,
            )
        except CapabilityRegistryError as exc:
            raise SolutionHostError(exc.code, exc.detail) from exc

    def _store_subdirectory(self, name: str, *, create: bool) -> Path:
        path = self.store_root / name
        if path.exists():
            if path.is_symlink() or not path.is_dir():
                raise SolutionHostError("invalid_store", "Host store contains an unsafe directory")
        elif create:
            path.mkdir()
        resolved = path.resolve(strict=False)
        if not resolved.is_relative_to(self.store_root):
            raise SolutionHostError("invalid_store", "Host store directory escaped its root")
        return resolved

    def _solution_root(self, solution_id: str, *, create: bool) -> Path:
        if not SOLUTION_ID_PATTERN.fullmatch(solution_id):
            raise SolutionHostError("invalid_solution_id", "Solution id is not valid")
        root = self.installed_root / solution_id
        if root.exists():
            if root.is_symlink() or not root.is_dir():
                raise SolutionHostError("invalid_store", "installed Solution directory is unsafe")
        elif create:
            root.mkdir()
        resolved = root.resolve(strict=False)
        if not resolved.is_relative_to(self.installed_root):
            raise SolutionHostError("invalid_store", "installed Solution directory escaped its root")
        return resolved

    def _install_path(self, solution_id: str, version: str, *, create_parent: bool = False) -> Path:
        if not VERSION_PATTERN.fullmatch(version):
            raise SolutionHostError("invalid_solution_version", "Solution version is not valid")
        root = self._solution_root(solution_id, create=create_parent)
        target = root / version
        if target.is_symlink():
            raise SolutionHostError("invalid_store", "installed Solution version is unsafe")
        resolved = target.resolve(strict=False)
        if not resolved.is_relative_to(self.installed_root):
            raise SolutionHostError("invalid_store", "installed Solution version escaped its root")
        return resolved

    def _resolve_install(self, solution_id: str, version: str | None) -> Path:
        if version is not None:
            target = self._install_path(solution_id, version)
            if target.is_symlink() or not target.is_dir():
                raise SolutionHostError("solution_not_installed", "requested Solution version is not installed")
            return target

        root = self._solution_root(solution_id, create=False)
        if root.is_symlink() or not root.is_dir():
            raise SolutionHostError("solution_not_installed", "requested Solution is not installed")
        versions = sorted(
            path
            for path in root.iterdir()
            if path.is_dir() and not path.is_symlink() and not path.name.startswith(".")
        )
        if not versions:
            raise SolutionHostError("solution_not_installed", "requested Solution is not installed")
        if len(versions) != 1:
            raise SolutionHostError("solution_version_required", "multiple installed versions require --version")
        return versions[0]

    def _verify_install(self, install_path: Path) -> dict[str, Any]:
        receipt_path = install_path / "install.json"
        package = install_path / "package"
        if (
            install_path.is_symlink()
            or receipt_path.is_symlink()
            or package.is_symlink()
            or not receipt_path.is_file()
            or not package.is_dir()
        ):
            raise SolutionHostError("integrity_mismatch", "installed Solution record is incomplete")
        try:
            receipt = load_json_object(receipt_path)
        except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise SolutionHostError("integrity_mismatch", "installed Solution receipt is invalid") from exc
        files = _package_files(package)
        if receipt.get("files") != files or receipt.get("package_digest") != _tree_digest(files):
            raise SolutionHostError("integrity_mismatch", "installed Solution package was modified")
        return receipt

    def _new_run_id(self) -> str:
        for _ in range(8):
            candidate = self._run_id_factory()
            if RUN_ID_PATTERN.fullmatch(candidate) and not (self.runs_root / candidate).exists():
                return candidate
        raise SolutionHostError("run_id_unavailable", "could not allocate a valid run id")

    def _run_path(self, run_id: str) -> Path:
        if not RUN_ID_PATTERN.fullmatch(run_id):
            raise SolutionHostError("invalid_run_id", "run id is not valid")
        path = self.runs_root / run_id
        if path.is_symlink() or not path.is_dir():
            raise SolutionHostError("run_not_found", "run was not found")
        return path

    def _persist_status(self, run_directory: Path, status: dict[str, Any]) -> None:
        validate_contract_instance(RUNTIME_STATUS_SCHEMA, status)
        _atomic_write_json(run_directory / "status.json", status)

    def _transition(
        self,
        run_directory: Path,
        status: dict[str, Any],
        state: str,
    ) -> None:
        current = status["lifecycle_state"]
        if state not in TRANSITIONS[current]:
            raise SolutionHostError(
                "invalid_lifecycle_transition",
                f"lifecycle transition {current} -> {state} is not allowed",
            )
        at = self._clock()
        status["lifecycle_state"] = state
        status["timestamps"]["updated_at"] = at
        if state == "running":
            status["timestamps"]["started_at"] = at
        if state in {"succeeded", "failed"}:
            status["timestamps"]["finished_at"] = at
        status["history"].append({"state": state, "at": at})
        self._persist_status(run_directory, status)

    def _finish_failure(
        self,
        run_directory: Path,
        status: dict[str, Any],
        *,
        code: str,
        detail: str,
    ) -> dict[str, Any]:
        if code not in RESULT_ERROR_CODES:
            code = "runtime_failure"
        if status["validation"]["input"] == "pending":
            status["validation"]["input"] = "not_run"
        if status["validation"]["output"] == "pending":
            status["validation"]["output"] = "not_run"
        status["error"] = {"code": code, "detail": _bounded_detail(detail)}
        self._transition(run_directory, status, "failed")
        result = self._result_from_status(status, output=None)
        validate_contract_instance(RESULT_ENVELOPE_SCHEMA, result)
        _atomic_write_json(run_directory / "result.json", result)
        return result

    def _finish_success(
        self,
        run_directory: Path,
        status: dict[str, Any],
        output: dict[str, Any],
    ) -> dict[str, Any]:
        self._transition(run_directory, status, "succeeded")
        result = self._result_from_status(status, output=output)
        validate_contract_instance(RESULT_ENVELOPE_SCHEMA, result)
        _atomic_write_json(run_directory / "result.json", result)
        return result

    @staticmethod
    def _result_from_status(
        status: dict[str, Any],
        *,
        output: dict[str, Any] | None,
    ) -> dict[str, Any]:
        return {
            "schema_version": "kora.solution.result/v0alpha1",
            "protocol_version": status["protocol_version"],
            "solution": dict(status["solution"]),
            "runtime": None if status["runtime"] is None else dict(status["runtime"]),
            "run_id": status["run_id"],
            "lifecycle_state": status["lifecycle_state"],
            "validation": dict(status["validation"]),
            "output": output,
            "evidence_reference": status["evidence_reference"],
            "error": None if status["error"] is None else dict(status["error"]),
            "activity": {
                "execution_performed": status["activity"]["execution_performed"],
                "network_accessed": False,
                "model_inference_performed": False,
                "gpu_execution_performed": False,
                "capabilities_executed": list(status["activity"]["capabilities_executed"]),
            },
            "timestamps": {
                "created_at": status["timestamps"]["created_at"],
                "started_at": status["timestamps"]["started_at"],
                "finished_at": status["timestamps"]["finished_at"],
            },
        }


__all__ = [
    "MAX_PACKAGE_BYTES",
    "MAX_PACKAGE_FILES",
    "RESULT_ERROR_CODES",
    "LocalSolutionHost",
    "SolutionHostError",
]
