"""Bounded CUDA execution harness for KRK-selected GPU fixture items."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kora.matrix_evaluator import load_matrix, repo_commit
from kora.route_selectivity_metrics import POLICIES, route_request_from_item, validate_matrix_item

CLAIM_LEVEL_MEASURED = "bounded_h100_execution_measured"
CLAIM_LEVEL_NOT_RUN = "h100_cuda_unavailable_not_run"
CLAIM_BOUNDARY = (
    "Bounded KRK-selected GPU fixture execution only. This output does not claim "
    "production savings, customer savings, infrastructure savings, H100 superiority, "
    "GPU superiority, broad workload superiority, production readiness, or provider replacement."
)
DEFAULT_TARGET_COUNT = 24
MAX_TARGET_COUNT = 50


@dataclass(frozen=True)
class BoundedOperation:
    request_id: str
    workload_profile: str
    workload_class: str
    compute_weight: float
    operation_index: int


def _compute_weight(item: dict[str, Any]) -> float:
    metadata = item.get("router_visible_metadata", {})
    if not isinstance(metadata, dict):
        return 1.0
    try:
        return max(float(metadata.get("compute_weight", 1)), 1.0)
    except (TypeError, ValueError):
        return 1.0


def collect_gpu_routed_items(matrix_paths: list[Path], *, policy_id: str = "KRK") -> list[dict[str, Any]]:
    try:
        policy = POLICIES[policy_id]
    except KeyError as exc:
        available = ", ".join(sorted(POLICIES))
        raise ValueError(f"unknown policy {policy_id!r}; available policies: {available}") from exc

    selected: list[dict[str, Any]] = []
    for matrix_path in matrix_paths:
        matrix = load_matrix(matrix_path)
        for item in matrix["items"]:
            validate_matrix_item(item)
            request = route_request_from_item(item)
            decision = policy(request)
            if decision.selected_route != "GPU":
                continue
            selected.append(
                {
                    "request_id": str(item["request_id"]),
                    "workload_profile": str(item["workload_profile"]),
                    "workload_class": str(item["workload_class"]),
                    "compute_weight": _compute_weight(item),
                    "selected_route": decision.selected_route,
                    "expected_route": str(item["oracle_labels"]["expected_route"]),
                }
            )
    return selected


def build_bounded_operations(
    gpu_items: list[dict[str, Any]],
    *,
    target_count: int = DEFAULT_TARGET_COUNT,
) -> list[BoundedOperation]:
    if target_count < 1 or target_count > MAX_TARGET_COUNT:
        raise ValueError(f"target_count must be between 1 and {MAX_TARGET_COUNT}")
    if not gpu_items:
        return []

    operations: list[BoundedOperation] = []
    for index in range(target_count):
        item = gpu_items[index % len(gpu_items)]
        operations.append(
            BoundedOperation(
                request_id=str(item["request_id"]),
                workload_profile=str(item["workload_profile"]),
                workload_class=str(item["workload_class"]),
                compute_weight=float(item["compute_weight"]),
                operation_index=index + 1,
            )
        )
    return operations


def _safe_device_class(device_name: str | None) -> str | None:
    if not device_name:
        return None
    lowered = device_name.lower()
    if "h100" in lowered:
        return "H100-class GPU"
    if "cuda" in lowered or "nvidia" in lowered:
        return "CUDA-capable GPU"
    return "GPU"


def _torch_status(torch_module: Any) -> dict[str, Any]:
    cuda_available = bool(torch_module.cuda.is_available())
    device_count = int(torch_module.cuda.device_count()) if cuda_available else 0
    device_name = torch_module.cuda.get_device_name(0) if cuda_available and device_count else None
    return {
        "torch_version": str(getattr(torch_module, "__version__", "unknown")),
        "torch_cuda_version": str(getattr(torch_module.version, "cuda", None)),
        "cuda_available": cuda_available,
        "cuda_device_count": device_count,
        "cuda_device_class": _safe_device_class(device_name),
    }


def _unavailable_result(
    *,
    matrix_paths: list[Path],
    fixture_count: int,
    gpu_items: list[dict[str, Any]],
    blocker: str,
    repo_commit_value: str | None,
) -> dict[str, Any]:
    return {
        "schema_version": "krk_h100_bounded_harness_v0",
        "claim_level": CLAIM_LEVEL_NOT_RUN,
        "run_status": "not_run",
        "blocker": blocker,
        "fixture_count": fixture_count,
        "gpu_routed_count": len(gpu_items),
        "operation_count": 0,
        "success_count": 0,
        "failure_count": 0,
        "runtime_seconds": 0.0,
        "throughput_requests_per_second": 0.0,
        "throughput_compute_weight_per_second": 0.0,
        "memory": {
            "peak_bounded_allocation_mb": 0.0,
            "cuda_context_before_mb": None,
            "cuda_context_after_mb": None,
        },
        "cuda": {
            "cuda_available": False,
            "cuda_device_count": 0,
            "cuda_device_class": None,
        },
        "source": {
            "matrix_files": [path.as_posix() for path in matrix_paths],
            "policy_id": "KRK",
            "subset_source": "public_krk_matrix_gpu_routed_items",
        },
        "reproducibility": {
            "repo_commit": repo_commit_value if repo_commit_value is not None else repo_commit(),
        },
        "public_boundary": {
            "raw_logs_committed": False,
            "private_infrastructure_details_committed": False,
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def execute_bounded_h100(
    matrix_paths: list[Path],
    *,
    target_count: int = DEFAULT_TARGET_COUNT,
    repo_commit_value: str | None = None,
    torch_module: Any | None = None,
) -> dict[str, Any]:
    fixture_count = sum(len(load_matrix(path)["items"]) for path in matrix_paths)
    gpu_items = collect_gpu_routed_items(matrix_paths)
    operations = build_bounded_operations(gpu_items, target_count=target_count)

    if not operations:
        return _unavailable_result(
            matrix_paths=matrix_paths,
            fixture_count=fixture_count,
            gpu_items=gpu_items,
            blocker="No KRK-selected GPU-routed fixture items were available.",
            repo_commit_value=repo_commit_value,
        )

    if torch_module is None:
        try:
            import torch as torch_module  # type: ignore[no-redef]
        except Exception as exc:  # noqa: BLE001 - structured no-CUDA/no-torch result.
            return _unavailable_result(
                matrix_paths=matrix_paths,
                fixture_count=fixture_count,
                gpu_items=gpu_items,
                blocker=f"Torch import failed: {type(exc).__name__}",
                repo_commit_value=repo_commit_value,
            )

    status = _torch_status(torch_module)
    if not status["cuda_available"]:
        result = _unavailable_result(
            matrix_paths=matrix_paths,
            fixture_count=fixture_count,
            gpu_items=gpu_items,
            blocker="CUDA is not available in this Python/Torch runtime.",
            repo_commit_value=repo_commit_value,
        )
        result["cuda"].update(status)
        return result

    device = torch_module.device("cuda")
    torch_module.cuda.synchronize()
    torch_module.cuda.reset_peak_memory_stats()
    context_before_mb = torch_module.cuda.memory_reserved() / (1024 * 1024)
    start = time.perf_counter()
    total_compute_weight = 0.0

    for operation in operations:
        total_compute_weight += operation.compute_weight
        elements = int(min(2_097_152, max(262_144, operation.compute_weight * 131_072)))
        iterations = int(min(32, max(4, operation.compute_weight)))
        tensor = torch_module.full((elements,), 0.5, device=device)
        for _ in range(iterations):
            tensor = tensor.mul(1.0001).add(0.0001)
        _ = float(tensor.mean().item())
        torch_module.cuda.synchronize()
        del tensor

    torch_module.cuda.synchronize()
    runtime_seconds = time.perf_counter() - start
    peak_allocation_mb = torch_module.cuda.max_memory_allocated() / (1024 * 1024)
    context_after_mb = torch_module.cuda.memory_reserved() / (1024 * 1024)
    operation_count = len(operations)

    return {
        "schema_version": "krk_h100_bounded_harness_v0",
        "claim_level": CLAIM_LEVEL_MEASURED,
        "run_status": "measured",
        "fixture_count": fixture_count,
        "gpu_routed_count": len(gpu_items),
        "operation_count": operation_count,
        "success_count": operation_count,
        "failure_count": 0,
        "runtime_seconds": round(runtime_seconds, 6),
        "throughput_requests_per_second": round(operation_count / runtime_seconds, 6) if runtime_seconds else 0.0,
        "throughput_compute_weight_per_second": (
            round(total_compute_weight / runtime_seconds, 6) if runtime_seconds else 0.0
        ),
        "memory": {
            "peak_bounded_allocation_mb": round(peak_allocation_mb, 3),
            "cuda_context_before_mb": round(context_before_mb, 3),
            "cuda_context_after_mb": round(context_after_mb, 3),
        },
        "cuda": status,
        "source": {
            "matrix_files": [path.as_posix() for path in matrix_paths],
            "policy_id": "KRK",
            "subset_source": "public_krk_matrix_gpu_routed_items",
        },
        "reproducibility": {
            "repo_commit": repo_commit_value if repo_commit_value is not None else repo_commit(),
            "target_count": target_count,
        },
        "public_boundary": {
            "raw_logs_committed": False,
            "private_infrastructure_details_committed": False,
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def render_markdown_summary(result: dict[str, Any]) -> str:
    lines = [
        "# KRK H100 Bounded Harness Summary v0",
        "",
        "Status: public-safe bounded H100 harness summary.",
        "",
        "This summary is generated by the repo-owned bounded H100 harness. It records aggregate metrics only and excludes raw runtime logs and private infrastructure details.",
        "",
        "## Run Summary",
        "",
        f"- run status: `{result['run_status']}`",
        f"- claim level: `{result['claim_level']}`",
        f"- fixture count: `{result['fixture_count']}`",
        f"- GPU-routed fixture count: `{result['gpu_routed_count']}`",
        f"- operation count: `{result['operation_count']}`",
        f"- success count: `{result['success_count']}`",
        f"- failure count: `{result['failure_count']}`",
        f"- runtime seconds: `{result['runtime_seconds']}`",
        f"- requests/sec: `{result['throughput_requests_per_second']}`",
        f"- compute-weight/sec: `{result['throughput_compute_weight_per_second']}`",
        "",
        "## CUDA Summary",
        "",
        f"- CUDA available: `{str(result['cuda']['cuda_available']).lower()}`",
        f"- CUDA device count: `{result['cuda']['cuda_device_count']}`",
        f"- CUDA device class: `{result['cuda']['cuda_device_class']}`",
        "",
        "## Memory Summary",
        "",
        f"- peak bounded allocation MB: `{result['memory']['peak_bounded_allocation_mb']}`",
        f"- CUDA context before MB: `{result['memory']['cuda_context_before_mb']}`",
        f"- CUDA context after MB: `{result['memory']['cuda_context_after_mb']}`",
        "",
    ]
    if result["run_status"] != "measured":
        lines.extend(["## Blocker", "", str(result.get("blocker", "not measured")), ""])
    lines.extend(["## Claim Boundary", "", CLAIM_BOUNDARY, ""])
    return "\n".join(lines)


def write_outputs(result: dict[str, Any], *, json_out: Path, md_out: Path) -> None:
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_out.write_text(render_markdown_summary(result), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run bounded KRK H100 fixture execution when CUDA is available.")
    parser.add_argument("--matrix", action="append", required=True, help="KRK matrix JSON fixture path")
    parser.add_argument("--target-count", type=int, default=DEFAULT_TARGET_COUNT, help="bounded operation count, max 50")
    parser.add_argument("--json-out", required=True, help="output path for JSON summary")
    parser.add_argument("--md-out", required=True, help="output path for Markdown summary")
    parser.add_argument("--repo-commit", help="override repo commit metadata")
    args = parser.parse_args(argv)

    result = execute_bounded_h100(
        [Path(path) for path in args.matrix],
        target_count=args.target_count,
        repo_commit_value=args.repo_commit,
    )
    write_outputs(result, json_out=Path(args.json_out), md_out=Path(args.md_out))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
