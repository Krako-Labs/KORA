"""Standalone conformance runner for bounded KORA Solution Packages."""

from __future__ import annotations

import json
import tempfile
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .contracts import (
    CONFORMANCE_CASE_SCHEMA,
    CONFORMANCE_REPORT_SCHEMA,
    SolutionContractError,
    load_json_object,
    validate_contract_instance,
)
from .host import LocalSolutionHost, SolutionHostError
from .validator import SolutionValidationError

CONFORMANCE_CASES_DIRECTORY = Path("conformance") / "cases"


class SolutionConformanceError(ValueError):
    """A bounded conformance setup failure that occurs before case execution."""

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = " ".join(detail.split())[:512]
        super().__init__(self.detail)

    def to_dict(self) -> dict[str, Any]:
        return {"status": "error", "error": {"code": self.code, "detail": self.detail}}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _load_cases(package: Path) -> list[dict[str, Any]]:
    cases_root = package / CONFORMANCE_CASES_DIRECTORY
    if cases_root.is_symlink() or not cases_root.is_dir():
        raise SolutionConformanceError(
            "conformance_cases_missing",
            "package must contain a regular conformance/cases directory",
        )

    entries = sorted(cases_root.iterdir(), key=lambda item: item.name)
    if not entries:
        raise SolutionConformanceError("conformance_cases_missing", "package has no conformance cases")

    manifest = load_json_object(package / "solution.json")
    integrity_files = set(manifest["integrity"]["files"])
    cases: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in entries:
        if path.is_symlink() or not path.is_file() or path.suffix != ".json":
            raise SolutionConformanceError(
                "invalid_conformance_case",
                "conformance/cases may contain regular JSON files only",
            )
        relative = path.relative_to(package).as_posix()
        if relative not in integrity_files:
            raise SolutionConformanceError(
                "conformance_case_not_integrity_bound",
                f"conformance case is absent from integrity.files: {path.name}",
            )
        try:
            payload = load_json_object(path)
            validate_contract_instance(CONFORMANCE_CASE_SCHEMA, payload)
        except (OSError, TypeError, ValueError, json.JSONDecodeError, SolutionContractError) as exc:
            raise SolutionConformanceError(
                "invalid_conformance_case",
                f"conformance case failed schema validation: {path.name}",
            ) from exc
        case_id = payload["case_id"]
        if case_id in seen:
            raise SolutionConformanceError(
                "duplicate_conformance_case",
                f"duplicate conformance case id: {case_id}",
            )
        seen.add(case_id)
        cases.append(payload)
    return cases


def _check(name: str, passed: bool) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed)}


def _case_result(
    case: dict[str, Any],
    returned_result: dict[str, Any],
    result: dict[str, Any],
    status: dict[str, Any],
    receipt: dict[str, Any],
) -> dict[str, Any]:
    expected = case["expected"]
    error = result["error"]
    error_code = None if error is None else error["code"]
    history = [entry["state"] for entry in status["history"]]
    runtime_identity = receipt["runtime_resolution"]
    activity = result["activity"]
    checks = [
        _check("solution_identity", result["solution"] == receipt["solution"]),
        _check("runtime_identity", result["runtime"] == runtime_identity),
        _check("lifecycle_state", result["lifecycle_state"] == expected["lifecycle_state"]),
        _check("validation", result["validation"] == expected["validation"]),
        _check("output", result["output"] == expected["output"]),
        _check("error_code", error_code == expected["error_code"]),
        _check(
            "capabilities_executed",
            activity["capabilities_executed"] == expected["capabilities_executed"],
        ),
        _check("lifecycle_history", history == expected["lifecycle_history"]),
        _check(
            "persisted_result",
            returned_result == result and result["run_id"] == status["run_id"],
        ),
        _check("evidence_reference", result["evidence_reference"] == status["evidence_reference"]),
        _check(
            "forbidden_activity_absent",
            activity["network_accessed"] is False
            and activity["model_inference_performed"] is False
            and activity["gpu_execution_performed"] is False
            and status["activity"]["network_accessed"] is False
            and status["activity"]["model_inference_performed"] is False
            and status["activity"]["gpu_execution_performed"] is False,
        ),
    ]
    passed = all(check["passed"] for check in checks)
    return {
        "case_id": case["case_id"],
        "status": "passed" if passed else "failed",
        "run_id": result["run_id"],
        "lifecycle_state": result["lifecycle_state"],
        "status_reference": status["evidence_reference"],
        "result_reference": f"runs/{result['run_id']}/result.json",
        "checks": checks,
    }


def run_solution_conformance(
    package_root: str | Path,
    *,
    clock: Callable[[], str] | None = None,
) -> dict[str, Any]:
    """Validate, install, and execute declared cases in a fresh isolated Host store."""

    now = clock or _utc_now
    started_at = now()
    package = Path(package_root).expanduser()
    try:
        if package.is_symlink():
            raise SolutionConformanceError(
                "invalid_package", "package root must not be a symbolic link"
            )
        package = package.resolve(strict=True)
        with tempfile.TemporaryDirectory(prefix="kora-conformance-") as temporary:
            host = LocalSolutionHost(temporary, clock=now)
            validation = host.validate(package)
            receipt = host.install(package)
            installed_package = (
                host.installed_root
                / receipt["solution"]["id"]
                / receipt["solution"]["version"]
                / "package"
            )
            cases = _load_cases(installed_package)
            digest = receipt["package_digest"]

            case_results: list[dict[str, Any]] = []
            execution_performed = False
            for case in cases:
                result = host.run(
                    receipt["solution"]["id"],
                    case["input"],
                    version=receipt["solution"]["version"],
                    approvals=case["approvals"],
                )
                persisted_result = host.result(result["run_id"])
                status = host.status(result["run_id"])
                execution_performed = (
                    execution_performed or persisted_result["activity"]["execution_performed"]
                )
                case_results.append(
                    _case_result(case, result, persisted_result, status, receipt)
                )
    except SolutionConformanceError:
        raise
    except FileNotFoundError as exc:
        raise SolutionConformanceError("package_not_found", "package directory was not found") from exc
    except SolutionValidationError as exc:
        codes = ",".join(sorted({issue.code for issue in exc.issues}))
        raise SolutionConformanceError(
            "package_validation_failed",
            f"Solution Package validation failed ({codes})",
        ) from exc
    except SolutionHostError as exc:
        raise SolutionConformanceError(exc.code, exc.detail) from exc
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SolutionConformanceError(
            "conformance_failed", "conformance execution failed closed"
        ) from exc

    passed_count = sum(item["status"] == "passed" for item in case_results)
    report = {
        "schema_version": "kora.solution.conformance-report/v0alpha1",
        "protocol_version": validation["api_version"],
        "package": {
            "id": receipt["solution"]["id"],
            "version": receipt["solution"]["version"],
            "digest": digest,
        },
        "runtime": dict(receipt["runtime_resolution"]),
        "status": "passed" if passed_count == len(case_results) else "failed",
        "summary": {
            "total": len(case_results),
            "passed": passed_count,
            "failed": len(case_results) - passed_count,
        },
        "cases": case_results,
        "activity": {
            "execution_performed": execution_performed,
            "network_accessed": False,
            "model_inference_performed": False,
            "gpu_execution_performed": False,
        },
        "timestamps": {"started_at": started_at, "finished_at": now()},
    }
    validate_contract_instance(CONFORMANCE_REPORT_SCHEMA, report)
    return report


__all__ = [
    "CONFORMANCE_CASES_DIRECTORY",
    "SolutionConformanceError",
    "run_solution_conformance",
]
