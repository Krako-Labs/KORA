from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_FIXTURE = Path("examples/workloads/kora-quality-check-seed-v0.json")
ALLOWED_CHECK_TYPES = {"exact", "schema", "structured_equivalent"}
ALLOWED_STATUSES = {"checked", "skipped", "gated"}
REQUIRED_COMMON_FIELDS = {
    "id",
    "category",
    "input",
    "status",
    "acceptance_criteria",
    "public_safe",
    "claim_scope",
}
REQUIRED_CHECKED_FIELDS = {"check_type", "observed_output"}


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("fixture root must be an object")
    return data


def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return sorted((_normalize(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, str):
        return value.strip()
    return value


def _validate_common_item(item: dict[str, Any], index: int, seen_ids: set[str]) -> str:
    missing = REQUIRED_COMMON_FIELDS - set(item)
    if missing:
        raise ValueError(f"item {index} missing fields: {sorted(missing)}")

    item_id = item["id"]
    if not isinstance(item_id, str) or not item_id.strip():
        raise ValueError(f"item {index} id must be a non-empty string")
    if item_id in seen_ids:
        raise ValueError(f"duplicate id: {item_id}")
    seen_ids.add(item_id)

    for field in ("category", "input", "acceptance_criteria"):
        if not isinstance(item[field], str) or not item[field].strip():
            raise ValueError(f"{item_id} {field} must be a non-empty string")
    if item["status"] not in ALLOWED_STATUSES:
        raise ValueError(f"{item_id} status is not allowed: {item['status']}")
    if item["public_safe"] is not True:
        raise ValueError(f"{item_id} public_safe must be true")
    if item["claim_scope"] != "fixture_only":
        raise ValueError(f"{item_id} claim_scope must be fixture_only")
    return item_id


def _validate_checked_item(item: dict[str, Any], item_id: str) -> None:
    missing = REQUIRED_CHECKED_FIELDS - set(item)
    if missing:
        raise ValueError(f"{item_id} missing checked fields: {sorted(missing)}")
    if item["check_type"] not in ALLOWED_CHECK_TYPES:
        raise ValueError(f"{item_id} check_type is not allowed: {item['check_type']}")

    check_type = item["check_type"]
    if check_type in {"exact", "structured_equivalent"} and "expected_output" not in item:
        raise ValueError(f"{item_id} expected_output is required for {check_type}")
    if check_type == "schema":
        expected_fields = item.get("expected_fields")
        if not isinstance(expected_fields, list) or not expected_fields:
            raise ValueError(f"{item_id} expected_fields must be a non-empty list")
        if not all(isinstance(field, str) and field.strip() for field in expected_fields):
            raise ValueError(f"{item_id} expected_fields must contain non-empty strings")
        if not isinstance(item["observed_output"], dict):
            raise ValueError(f"{item_id} observed_output must be an object for schema")


def _check_item(item: dict[str, Any]) -> bool:
    check_type = item["check_type"]
    if check_type == "exact":
        return item["observed_output"] == item["expected_output"]
    if check_type == "schema":
        observed = item["observed_output"]
        return all(field in observed for field in item["expected_fields"])
    if check_type == "structured_equivalent":
        return _normalize(item["observed_output"]) == _normalize(item["expected_output"])
    raise ValueError(f"unsupported check_type: {check_type}")


def evaluate_quality_checks(path: Path = DEFAULT_FIXTURE) -> dict[str, Any]:
    data = _load_json(path)
    if data.get("schema_version") != "kora_quality_check_seed_v0":
        raise ValueError("unsupported schema_version")
    if data.get("public_safe") is not True:
        raise ValueError("fixture public_safe must be true")
    if data.get("claim_scope") != "fixture_only":
        raise ValueError("fixture claim_scope must be fixture_only")

    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if not 5 <= len(items) <= 8:
        raise ValueError("items must contain between 5 and 8 entries")

    seen_ids: set[str] = set()
    status_counts: Counter[str] = Counter()
    check_type_counts: Counter[str] = Counter()
    passed_checks = 0
    failed_checks = 0

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"item {index} must be an object")
        item_id = _validate_common_item(item, index, seen_ids)
        status = item["status"]
        status_counts[status] += 1

        if status == "checked":
            _validate_checked_item(item, item_id)
            check_type_counts[item["check_type"]] += 1
            if _check_item(item):
                passed_checks += 1
            else:
                failed_checks += 1
        elif status == "skipped" and not item.get("skip_reason"):
            raise ValueError(f"{item_id} skip_reason is required for skipped items")
        elif status == "gated" and not item.get("gate_reason"):
            raise ValueError(f"{item_id} gate_reason is required for gated items")

    ok = failed_checks == 0
    return {
        "ok": ok,
        "fixture": str(path),
        "claim_scope": "fixture_only",
        "public_safe": True,
        "total_items": len(items),
        "checked_items": status_counts["checked"],
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "skipped_items": status_counts["skipped"],
        "gated_items": status_counts["gated"],
        "check_type_counts": {key: check_type_counts[key] for key in sorted(check_type_counts)},
        "non_claims": [
            "does_not_call_providers",
            "does_not_run_model_inference",
            "does_not_execute_h100_gpu_cuda_server_remote_work",
            "does_not_execute_semantic_judging",
            "does_not_include_human_review_results",
            "does_not_prove_output_quality",
            "does_not_prove_broader_workload_representativeness",
            "does_not_prove_production_readiness",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate deterministic fixture-only quality checks for a tiny public-safe KORA fixture."
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Path to the quality-check seed fixture.",
    )
    args = parser.parse_args(argv)

    try:
        summary = evaluate_quality_checks(args.fixture)
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2, sort_keys=True))
        return 2

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
