from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_FIXTURE = Path("examples/workloads/kora-methodology-fixture-check-slice-v0.json")
ALLOWED_CHECK_TYPES = {
    "exact_string",
    "exact_number",
    "exact_list",
    "exact_object",
    "required_keys",
    "field_schema",
}
ALLOWED_STATUSES = {"checked", "skipped"}
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
JSON_TYPE_NAMES = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "list": list,
    "object": dict,
}


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("fixture root must be an object")
    return data


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


def _validate_expected_keys(item: dict[str, Any], item_id: str) -> None:
    expected_keys = item.get("expected_keys")
    if not isinstance(expected_keys, list) or not expected_keys:
        raise ValueError(f"{item_id} expected_keys must be a non-empty list")
    if not all(isinstance(key, str) and key.strip() for key in expected_keys):
        raise ValueError(f"{item_id} expected_keys must contain non-empty strings")
    if not isinstance(item["observed_output"], dict):
        raise ValueError(f"{item_id} observed_output must be an object for required_keys")


def _validate_expected_schema(item: dict[str, Any], item_id: str) -> None:
    expected_schema = item.get("expected_schema")
    if not isinstance(expected_schema, dict) or not expected_schema:
        raise ValueError(f"{item_id} expected_schema must be a non-empty object")
    unknown_types = sorted(
        type_name
        for type_name in expected_schema.values()
        if not isinstance(type_name, str) or type_name not in JSON_TYPE_NAMES
    )
    if unknown_types:
        raise ValueError(f"{item_id} expected_schema contains unsupported types: {unknown_types}")
    if not isinstance(item["observed_output"], dict):
        raise ValueError(f"{item_id} observed_output must be an object for field_schema")


def _validate_checked_item(item: dict[str, Any], item_id: str) -> None:
    missing = REQUIRED_CHECKED_FIELDS - set(item)
    if missing:
        raise ValueError(f"{item_id} missing checked fields: {sorted(missing)}")
    check_type = item["check_type"]
    if check_type not in ALLOWED_CHECK_TYPES:
        raise ValueError(f"{item_id} check_type is not allowed: {check_type}")

    if check_type.startswith("exact_") and "expected_output" not in item:
        raise ValueError(f"{item_id} expected_output is required for {check_type}")
    if check_type == "exact_string" and not isinstance(item["expected_output"], str):
        raise ValueError(f"{item_id} expected_output must be a string")
    if check_type == "exact_number" and not _is_number(item["expected_output"]):
        raise ValueError(f"{item_id} expected_output must be a number")
    if check_type == "exact_list" and not isinstance(item["expected_output"], list):
        raise ValueError(f"{item_id} expected_output must be a list")
    if check_type == "exact_object" and not isinstance(item["expected_output"], dict):
        raise ValueError(f"{item_id} expected_output must be an object")
    if check_type == "required_keys":
        _validate_expected_keys(item, item_id)
    if check_type == "field_schema":
        _validate_expected_schema(item, item_id)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _field_matches_type(value: Any, type_name: str) -> bool:
    if type_name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "number":
        return _is_number(value)
    return isinstance(value, JSON_TYPE_NAMES[type_name])


def _check_item(item: dict[str, Any]) -> tuple[bool, str | None]:
    check_type = item["check_type"]
    observed = item["observed_output"]

    if check_type in {"exact_string", "exact_number", "exact_list", "exact_object"}:
        if observed == item["expected_output"]:
            return True, None
        return False, "observed_output did not exactly match expected_output"

    if check_type == "required_keys":
        missing_keys = [key for key in item["expected_keys"] if key not in observed]
        if not missing_keys:
            return True, None
        return False, f"observed_output missing required keys: {missing_keys}"

    if check_type == "field_schema":
        for field, type_name in item["expected_schema"].items():
            if field not in observed:
                return False, f"observed_output missing schema field: {field}"
            if not _field_matches_type(observed[field], type_name):
                return False, f"observed_output field {field} did not match type {type_name}"
        return True, None

    raise ValueError(f"unsupported check_type: {check_type}")


def evaluate_methodology_fixture_checks(path: Path = DEFAULT_FIXTURE) -> dict[str, Any]:
    data = _load_json(path)
    if data.get("schema_version") != "kora_methodology_fixture_check_slice_v0":
        raise ValueError("unsupported schema_version")
    if data.get("public_safe") is not True:
        raise ValueError("fixture public_safe must be true")
    if data.get("claim_scope") != "fixture_only":
        raise ValueError("fixture claim_scope must be fixture_only")

    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if not 12 <= len(items) <= 20:
        raise ValueError("items must contain between 12 and 20 entries")

    seen_ids: set[str] = set()
    status_counts: Counter[str] = Counter()
    check_type_counts: Counter[str] = Counter()
    failures: list[dict[str, Any]] = []

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"item {index} must be an object")
        item_id = _validate_common_item(item, index, seen_ids)
        status = item["status"]
        status_counts[status] += 1

        if status == "checked":
            _validate_checked_item(item, item_id)
            check_type_counts[item["check_type"]] += 1
            passed, reason = _check_item(item)
            if not passed:
                failures.append(
                    {
                        "id": item_id,
                        "check_type": item["check_type"],
                        "reason": reason,
                        "expected": item.get("expected_output", item.get("expected_keys", item.get("expected_schema"))),
                        "observed": item["observed_output"],
                    }
                )
        elif not item.get("skip_reason"):
            raise ValueError(f"{item_id} skip_reason is required for skipped items")

    checked_items = status_counts["checked"]
    failed_checks = len(failures)
    passed_checks = checked_items - failed_checks
    ok = failed_checks == 0

    return {
        "ok": ok,
        "fixture": str(path),
        "claim_scope": "fixture_only",
        "public_safe": True,
        "total_items": len(items),
        "checked_items": checked_items,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "skipped_items": status_counts["skipped"],
        "check_type_counts": {key: check_type_counts[key] for key in sorted(check_type_counts)},
        "failures": failures,
        "non_claims": [
            "does_not_call_providers",
            "does_not_run_model_inference",
            "does_not_execute_h100_gpu_cuda_server_remote_work",
            "does_not_execute_semantic_judging",
            "does_not_include_human_review_results",
            "does_not_prove_output_quality",
            "does_not_prove_broader_workload_representativeness",
            "does_not_validate_production_readiness",
            "does_not_prove_cost_reduction",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate deterministic methodology-aligned fixture checks for a small public-safe KORA fixture."
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Path to the methodology-aligned fixture-check slice.",
    )
    args = parser.parse_args(argv)

    try:
        summary = evaluate_methodology_fixture_checks(args.fixture)
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2, sort_keys=True))
        return 2

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
