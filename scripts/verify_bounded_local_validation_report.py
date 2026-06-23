from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.run_bounded_local_validation import PROFILES, REPORT_SCHEMA


SUPPORTED_PROFILE = "kora-local-core"
ALLOWED_STATUSES = {"passed", "failed", "skipped/dry-run"}
REQUIRED_TOP_LEVEL_FIELDS = {"profile", "final_status", "steps"}


def _approved_commands(profile: str) -> list[list[str]]:
    return [list(step.argv) for step in PROFILES[profile]]


def _step_command(step: dict[str, Any]) -> list[str] | None:
    command = step.get("command", step.get("argv"))
    if isinstance(command, list) and all(isinstance(part, str) for part in command):
        return command
    if isinstance(command, str):
        try:
            return shlex.split(command)
        except ValueError:
            return None
    return None


def _return_code(step: dict[str, Any]) -> int | None | object:
    for key in ("return_code", "returnCode", "returncode"):
        if key in step:
            value = step[key]
            if value is None or isinstance(value, int):
                return value
            return object()
    return object()


def _validate_report(report: Any, expected_profile: str, allow_failed: bool) -> list[str]:
    errors: list[str] = []

    if not isinstance(report, dict):
        return ["report must be a JSON object"]

    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(report))
    if missing:
        errors.append(f"missing top-level field(s): {', '.join(missing)}")

    if "repo_root" not in report and "repository_root" not in report:
        errors.append("missing top-level field: repo_root or repository_root")

    schema = report.get("report_schema")
    if schema is not None and schema != REPORT_SCHEMA:
        errors.append(f"unsupported report_schema: {schema}")

    profile = report.get("profile")
    if profile != expected_profile:
        errors.append(f"profile mismatch: expected {expected_profile}, found {profile}")
    if expected_profile != SUPPORTED_PROFILE:
        errors.append(f"unsupported profile: {expected_profile}")
    if profile not in PROFILES:
        errors.append(f"report profile is unsupported: {profile}")

    final_status = report.get("final_status")
    if final_status not in {"passed", "failed", "dry-run"}:
        errors.append(f"invalid final_status: {final_status}")

    steps = report.get("steps")
    if not isinstance(steps, list):
        errors.append("steps must be a list")
        steps = []

    expected_commands = _approved_commands(SUPPORTED_PROFILE)
    actual_commands: list[list[str]] = []
    step_statuses: list[str] = []

    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"step {index + 1} must be an object")
            continue

        for field in ("name", "status"):
            if field not in step:
                errors.append(f"step {index + 1} missing field: {field}")

        command = _step_command(step)
        if command is None:
            errors.append(f"step {index + 1} missing valid command or argv")
        else:
            actual_commands.append(command)

        return_code = _return_code(step)
        if not (return_code is None or isinstance(return_code, int)):
            errors.append(f"step {index + 1} missing valid return_code")

        status = step.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"step {index + 1} has invalid status: {status}")
        else:
            step_statuses.append(status)

    if final_status == "failed":
        expected_prefix = expected_commands[: len(actual_commands)]
        if not actual_commands or actual_commands != expected_prefix:
            errors.append(
                "failed report step command list does not match an approved kora-local-core command prefix"
            )
    elif actual_commands != expected_commands:
        errors.append("step command list does not match approved kora-local-core command list")

    if final_status == "failed" and not allow_failed:
        errors.append("failed report requires --allow-failed")

    if final_status == "dry-run":
        if steps and any(status != "skipped/dry-run" for status in step_statuses):
            errors.append("dry-run report steps must all be skipped/dry-run")
    elif final_status == "passed":
        if steps and any(status != "passed" for status in step_statuses):
            errors.append("passed report steps must all be passed")
    elif final_status == "failed":
        if steps and "failed" not in step_statuses:
            errors.append("failed report must include at least one failed step")

    return errors


def verify_report(report_path: Path, expected_profile: str, allow_failed: bool) -> tuple[bool, list[str]]:
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, [f"malformed JSON: {exc.msg}"]
    except OSError as exc:
        return False, [f"could not read report: {exc}"]

    errors = _validate_report(report, expected_profile, allow_failed)
    return not errors, errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a bounded local validation JSON report without executing its commands."
    )
    parser.add_argument("report", type=Path, help="Path to a JSON report from run_bounded_local_validation.py.")
    parser.add_argument("--profile", required=True, help="Expected approved validation profile.")
    parser.add_argument(
        "--allow-failed",
        action="store_true",
        help="Treat structurally valid failed reports as acceptable.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ok, errors = verify_report(args.report, args.profile, args.allow_failed)
    if ok:
        print(f"PASS bounded local validation report verified: profile={args.profile}")
        return 0

    print(f"FAIL bounded local validation report rejected: profile={args.profile}")
    for error in errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
