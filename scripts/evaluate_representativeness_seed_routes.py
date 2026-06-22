from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_representativeness_seed import ALLOWED_ROUTES, DEFAULT_FIXTURE, validate_seed


LOCAL_ROUTE_CANDIDATES = ("cpu", "deterministic", "retrieval_needed", "tool_needed")
PROVIDER_MODEL_CANDIDATES = ("gpu", "provider_needed")
CACHE_REUSE_CANDIDATES = ("cache",)
FALLBACK_CONTROL_CANDIDATES = ("fallback",)


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("fixture root must be an object")
    return data


def evaluate_routes(path: Path = DEFAULT_FIXTURE) -> dict[str, Any]:
    validation_summary = validate_seed(path)
    data = _load_json(path)
    items = data["items"]

    route_counts = Counter(item.get("expected_route") for item in items)
    category_counts = Counter(item.get("category") for item in items)
    unsupported_or_missing = sum(
        1 for item in items if item.get("expected_route") not in ALLOWED_ROUTES
    )

    def count_routes(routes: tuple[str, ...]) -> int:
        return sum(route_counts[route] for route in routes)

    return {
        "ok": True,
        "fixture": str(path),
        "validation": {
            "shape_validated": validation_summary["ok"],
            "claim_scope": validation_summary["claim_scope"],
            "public_safe": validation_summary["public_safe"],
        },
        "total_seed_items": len(items),
        "route_counts": {
            route: route_counts[route]
            for route in sorted(ALLOWED_ROUTES)
            if route_counts[route]
        },
        "route_group_counts": {
            "cache_reuse_candidates": count_routes(CACHE_REUSE_CANDIDATES),
            "deterministic_local_route_candidates": count_routes(LOCAL_ROUTE_CANDIDATES),
            "fallback_control_candidates": count_routes(FALLBACK_CONTROL_CANDIDATES),
            "provider_model_candidates": count_routes(PROVIDER_MODEL_CANDIDATES),
        },
        "workload_category_counts": {
            category: category_counts[category] for category in sorted(category_counts)
        },
        "unsupported_unknown_missing_route_metadata_count": unsupported_or_missing,
        "non_claims": [
            "does_not_call_providers",
            "does_not_execute_h100_or_gpu_workloads",
            "does_not_run_model_inference",
            "does_not_prove_output_quality",
            "does_not_prove_broader_workload_representativeness",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate aggregate route counters for the KORA representativeness seed fixture."
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Path to the representativeness seed fixture.",
    )
    args = parser.parse_args(argv)

    summary = evaluate_routes(args.fixture)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
