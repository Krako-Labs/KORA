from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.run_bounded_local_validation import PROFILES, REPORT_SCHEMA


ALLOWED_STATUSES = {"passed", "failed", "skipped/dry-run"}
ROOT_FIELDS = ("repository_root", "repo_root")
RETURN_CODE_FIELDS = ("return_code", "returnCode")
COMMAND_FIELDS = ("command", "argv")


def _first_present(data: dict[str, Any], fields: tuple[str, ...]) -> Any:
    for field in fields:
        if field in data:
            return data[field]
    return None


def _approved_commands(profile: str) -> list[list[str]]:
    return [list(step.argv) for step in PROFILES[profile]]


def _load_report(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"report not found: {path}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return None, ["report root must be a JSON object"]
    return data, []


def verify_report(report: dict[str, Any], profile: str, allow_failed: bool = False) -> list[str]:
    errors: list[str] = []

    if profile not in PROFILES:
        errors.append(f"unsupported profile: {profile}")
        return errors

    required_fields = ("profile", "final_status", "steps")
    for field in required_fields:
        if field not in report:
            errors.append(f"missing top-level field: {field}")

    if _first_present(report, ROOT_FIELDS) is None:
        errors.append("missing top-level field: repository_root or repo_root")

    if errors:
        return errors

    if report["profile"] != profile:
        errors.append(f"profile mismatch: expected {profile}, got {report['profile']}")

    schema = report.get("report_schema")
    if schema is not None and schema != REPORT_SCHEMA:
        errors.append(f"unsupported report_schema: {schema}")

    steps = report["steps"]
    if not isinstance(steps, list):
        errors.append("steps must be a list")
        return errors

    approved_commands = _approved_commands(profile)
    if len(steps) != len(approved_commands):
        errors.append(f"step count mismatch: expected {len(approved_commands)}, got {len(steps)}")
        return errors

    saw_failed_step = False
    saw_non_dry_run_step = False
    for index, (step, approved_command) in enumerate(zip(steps, approved_commands), 1):
        if not isinstance(step, dict):
            errors.append(f"step {index} must be an object")
            continue

        for field in ("name", "status"):
            if field not in step:
                errors.append(f"step {index} missing field: {field}")

        command = _first_present(step, COMMAND_FIELDS)
        if command is None:
            errors.append(f"step {index} missing field: command or argv")
        elif command != approved_command:
            errors.append(f"step {index} command mismatch: expected {approved_command}, got {command}")
        elif not isinstance(command, list) or not all(isinstance(part, str) for part in command):
            errors.append(f"step {index} command must be an argv list of strings")

        if _first_present(step, RETURN_CODE_FIELDS) is None and not any(
            field in step for field in RETURN_CODE_FIELDS
        ):
            errors.append(f"step {index} missing field: return_code or returnCode")

        status = step.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"step {index} invalid status: {status}")
        if status == "failed":
            saw_failed_step = True
        if status != "skipped/dry-run":
            saw_non_dry_run_step = True

    final_status = report["final_status"]
    if final_status not in {"passed", "failed", "dry-run"}:
        errors.append(f"invalid final_status: {final_status}")

    is_failed_report = final_status == "failed" or saw_failed_step
    is_dry_run_report = final_status == "dry-run" or not saw_non_dry_run_step
    if is_dry_run_report and any(step.get("status") != "skipped/dry-run" for step in steps if isinstance(step, dict)):
        errors.append("dry-run reports must mark all steps skipped/dry-run")

    if is_failed_report and not allow_failed:
        errors.append("report contains failed validation; rerun with --allow-failed to accept structure only")

    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify a bounded local validation JSON report.")
    parser.add_argument("report", type=Path, help="Path to a JSON report from run_bounded_local_validation.py.")
    parser.add_argument("--profile", required=True, help="Expected approved validation profile.")
    parser.add_argument(
        "--allow-failed",
        action="store_true",
        help="Accept structurally valid reports that contain failed validation steps.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report, load_errors = _load_report(args.report)
    if load_errors:
        for error in load_errors:
            print(f"failed: {error}")
        return 2

    assert report is not None
    errors = verify_report(report, args.profile, allow_failed=args.allow_failed)
    if errors:
        print(f"failed: {args.report} profile={args.profile}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"passed: {args.report} profile={args.profile} steps={len(report['steps'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
