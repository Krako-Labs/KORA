from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


VALID_FINAL_STATUSES = {"merge-ready", "needs-r1", "needs-cto-review", "blocked"}
VALID_RISK_LEVELS = {"low", "medium", "high"}
CLAIM_BOUNDARY_TERMS = (
    "claim-boundary audit",
    "claim boundary",
    "claim boundaries",
    "does not prove output quality",
    "no output-quality proof",
)
FORBIDDEN_ACTION_TERMS = (
    "forbidden-action audit",
    "forbidden actions",
    "no provider calls",
    "no report-command execution",
    "no release",
)


def _read(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except OSError as exc:
        return None, f"could not read {path}: {exc}"


def _group_id_from_path(path: Path) -> str | None:
    match = re.search(r"group(\d+)", path.name, re.IGNORECASE)
    if match is None:
        return None
    return f"Group {int(match.group(1))}"


def _first_pr_url(text: str) -> str | None:
    match = re.search(r"https://github\.com/Krako-Labs/KORA/pull/\d+", text)
    return match.group(0) if match else None


def _first_branch(text: str) -> str | None:
    patterns = (
        r"(?im)^\s*-\s*branch:\s*`([^`]+)`",
        r"(?im)^\s*-\s*active verification branch:\s*`([^`]+)`",
        r"(?im)^\s*-\s*branch pushed to:\s*`origin/([^`]+)`",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


def _group_context(text: str, group_id: str | None) -> str:
    if group_id is None:
        return text

    lines = text.splitlines()
    selected: list[str] = []
    group_lower = group_id.lower()
    for index, line in enumerate(lines):
        if group_lower not in line.lower():
            continue
        start = max(0, index - 3)
        end = min(len(lines), index + 9)
        selected.extend(lines[start:end])
        selected.append("")

    return "\n".join(selected) if selected else ""


def _field_value(text: str, label: str) -> str | None:
    match = re.search(rf"(?im)^\s*(?:[-*]\s*)?{re.escape(label)}\s*:\s*(.+?)\s*$", text)
    if not match:
        return None
    return match.group(1).strip().strip("`")


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def validate_consistency(report_path: Path, breadcrumb_paths: list[Path]) -> dict[str, Any]:
    errors: list[str] = []
    report_text, read_error = _read(report_path)
    if read_error is not None:
        return {"ok": False, "errors": [read_error]}
    assert report_text is not None

    group_id = _group_id_from_path(report_path)
    if group_id and group_id.lower() not in report_text.lower():
        errors.append(f"report missing id: {group_id}")

    report_pr = _first_pr_url(report_text)
    if report_pr is None:
        errors.append("report missing PR URL")

    report_branch = _first_branch(report_text)
    if report_branch is None:
        errors.append("report missing branch")

    risk_level = _field_value(report_text, "risk level")
    if risk_level is None or risk_level.lower() not in VALID_RISK_LEVELS:
        errors.append("report missing valid risk level")

    final_status = _field_value(report_text, "final status classification")
    if final_status is None or final_status.lower() not in VALID_FINAL_STATUSES:
        errors.append("report missing valid final status classification")

    if "validation" not in report_text.lower() or "passed" not in report_text.lower():
        errors.append("report missing validation results language")

    if not _contains_any(report_text, CLAIM_BOUNDARY_TERMS):
        errors.append("report missing claim-boundary language")

    if not _contains_any(report_text, FORBIDDEN_ACTION_TERMS):
        errors.append("report missing forbidden-action language")

    breadcrumb_summaries: list[dict[str, str | None]] = []
    for path in breadcrumb_paths:
        text, error = _read(path)
        if error is not None:
            errors.append(error)
            continue
        assert text is not None
        compare_text = _group_context(text, group_id)
        summary = {
            "path": str(path),
            "pr_url": _first_pr_url(compare_text),
            "branch": _first_branch(compare_text),
        }
        breadcrumb_summaries.append(summary)

        if group_id and group_id.lower() not in text.lower():
            errors.append(f"{path} missing id: {group_id}")
        if report_pr and summary["pr_url"] and summary["pr_url"] != report_pr:
            errors.append(f"{path} PR URL mismatch: expected {report_pr}, got {summary['pr_url']}")
        if report_branch and summary["branch"] and summary["branch"] != report_branch:
            errors.append(
                f"{path} branch mismatch: expected {report_branch}, got {summary['branch']}"
            )

    return {
        "ok": not errors,
        "errors": errors,
        "report": str(report_path),
        "breadcrumbs": breadcrumb_summaries,
        "group_id": group_id,
        "pr_url": report_pr,
        "branch": report_branch,
        "risk_level": risk_level.lower() if risk_level else None,
        "final_status_classification": final_status.lower() if final_status else None,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check literal consistency between a KORA report and breadcrumb files."
    )
    parser.add_argument("report", type=Path, help="Primary report Markdown file.")
    parser.add_argument(
        "--breadcrumb",
        action="append",
        type=Path,
        default=[],
        help="Optional breadcrumb Markdown file to compare.",
    )
    parser.add_argument("--json-out", type=Path, help="Optional path for JSON check output.")
    return parser.parse_args(argv)


def write_json(result: dict[str, Any], json_out: Path | None) -> None:
    if json_out is not None:
        json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = validate_consistency(args.report, args.breadcrumb)
    write_json(result, args.json_out)

    if not result["ok"]:
        for error in result["errors"]:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {args.report} is consistent with {len(args.breadcrumb)} breadcrumb file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
