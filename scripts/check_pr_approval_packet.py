from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_FIELDS: tuple[str, ...] = (
    "decision needed",
    "risk level",
    "final status classification",
    "changed files",
    "validation summary",
    "repair attempts",
    "failures encountered",
    "self-review summary",
    "claim-boundary audit",
    "forbidden-action audit",
    "uncertainty notes",
    "workflow recommendation",
    "albert action options",
)
VALID_FINAL_STATUSES = {"merge-ready", "needs-r1", "needs-cto-review", "blocked"}
VALID_RISK_LEVELS = {"low", "medium", "high"}
REQUIRED_ACTION_OPTIONS = ("Merge", "Request R1", "Stop", "CTO Review")


def _label_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?im)^\s*(?:[-*]\s*)?{re.escape(label)}\s*:\s*(.+?)\s*$")


def _field_value(text: str, label: str) -> str | None:
    match = _label_pattern(label).search(text)
    if match is None:
        return None
    return match.group(1).strip()


def _normalized_token(value: str) -> str:
    return value.strip().strip("` .").lower()


def validate_packet(text: str, require_merge_ready: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    fields: dict[str, str] = {}

    for field in REQUIRED_FIELDS:
        value = _field_value(text, field)
        if value is None:
            errors.append(f"missing required field: {field}")
        elif not value:
            errors.append(f"empty required field: {field}")
        else:
            fields[field] = value

    risk_value = _normalized_token(fields.get("risk level", ""))
    if risk_value and risk_value not in VALID_RISK_LEVELS:
        errors.append(f"invalid risk level: {fields['risk level']}")

    status_value = _normalized_token(fields.get("final status classification", ""))
    if status_value and status_value not in VALID_FINAL_STATUSES:
        errors.append(f"invalid final status classification: {fields['final status classification']}")
    if require_merge_ready and status_value and status_value != "merge-ready":
        errors.append("--require-merge-ready requires final status classification: merge-ready")

    action_value = fields.get("albert action options", "")
    for option in REQUIRED_ACTION_OPTIONS:
        if option.lower() not in action_value.lower():
            errors.append(f"missing Albert action option: {option}")

    return {
        "ok": not errors,
        "errors": errors,
        "fields_present": sorted(fields),
        "risk_level": risk_value or None,
        "final_status_classification": status_value or None,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check a KORA PR approval packet in a Markdown file."
    )
    parser.add_argument("path", type=Path, help="Markdown file containing an approval packet.")
    parser.add_argument("--json-out", type=Path, help="Optional path for JSON check output.")
    parser.add_argument(
        "--require-merge-ready",
        action="store_true",
        help="Require final status classification to be merge-ready.",
    )
    return parser.parse_args(argv)


def write_json(result: dict[str, Any], json_out: Path | None) -> None:
    if json_out is not None:
        json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        text = args.path.read_text(encoding="utf-8")
    except OSError as exc:
        result = {"ok": False, "errors": [f"could not read file: {exc}"]}
        write_json(result, args.json_out)
        print(f"FAIL: {result['errors'][0]}")
        return 1

    result = validate_packet(text, require_merge_ready=args.require_merge_ready)
    write_json(result, args.json_out)

    if not result["ok"]:
        for error in result["errors"]:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {args.path} contains a complete KORA approval packet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
