from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_FIXTURE = Path("examples/workloads/kora-representativeness-seed-v0.json")
ALLOWED_SCHEMA_VERSIONS = {
    "kora_representativeness_seed_v0",
    "kora_representativeness_slice_v1",
}
REQUIRED_ITEM_FIELDS = {
    "id",
    "category",
    "input",
    "expected_route",
    "rationale",
    "public_safe",
    "claim_scope",
}
ALLOWED_ROUTES = {
    "deterministic",
    "cache",
    "cpu",
    "retrieval_needed",
    "tool_needed",
    "provider_needed",
    "gpu",
    "fallback",
}


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("fixture root must be an object")
    return data


def validate_seed(path: Path = DEFAULT_FIXTURE) -> dict[str, Any]:
    data = _load_json(path)
    if data.get("schema_version") not in ALLOWED_SCHEMA_VERSIONS:
        raise ValueError("unsupported schema_version")
    if data.get("public_safe") is not True:
        raise ValueError("fixture public_safe must be true")
    if data.get("claim_scope") != "fixture_only":
        raise ValueError("fixture claim_scope must be fixture_only")

    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if not 30 <= len(items) <= 60:
        raise ValueError("items must contain between 30 and 60 entries")

    seen_ids: set[str] = set()
    route_counts = {route: 0 for route in sorted(ALLOWED_ROUTES)}
    category_counts: dict[str, int] = {}

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"item {index} must be an object")
        missing = REQUIRED_ITEM_FIELDS - set(item)
        if missing:
            raise ValueError(f"item {index} missing fields: {sorted(missing)}")

        item_id = item["id"]
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError(f"item {index} id must be a non-empty string")
        if item_id in seen_ids:
            raise ValueError(f"duplicate id: {item_id}")
        seen_ids.add(item_id)

        for field in ("category", "input", "rationale"):
            if not isinstance(item[field], str) or not item[field].strip():
                raise ValueError(f"{item_id} {field} must be a non-empty string")
        if item["expected_route"] not in ALLOWED_ROUTES:
            raise ValueError(f"{item_id} expected_route is not allowed: {item['expected_route']}")
        if item["public_safe"] is not True:
            raise ValueError(f"{item_id} public_safe must be true")
        if item["claim_scope"] != "fixture_only":
            raise ValueError(f"{item_id} claim_scope must be fixture_only")

        route_counts[item["expected_route"]] += 1
        category_counts[item["category"]] = category_counts.get(item["category"], 0) + 1

    return {
        "ok": True,
        "path": str(path),
        "item_count": len(items),
        "category_count": len(category_counts),
        "route_counts": {route: count for route, count in route_counts.items() if count},
        "claim_scope": "fixture_only",
        "public_safe": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the KORA representativeness seed fixture shape.")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Path to the representativeness seed fixture.",
    )
    args = parser.parse_args(argv)

    summary = validate_seed(args.fixture)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
