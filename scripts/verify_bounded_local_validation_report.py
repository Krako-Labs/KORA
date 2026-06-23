from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.run_bounded_local_validation import PROFILES


SUPPORTED_PROFILE = "kora-local-core"
ALLOWED_FINAL_STATUSES = {"passed", "failed", "dry-run"}
ALLOWED_STEP_STATUSES = {"passed", "failed", "skipped/dry-run"}
REQUIRED_TOP_LEVEL_FIELDS = {"profile", "final_status", "steps"}
REQUIRED_STEP_FIELDS = {"name", "command", "return_code", "status"}

APPROVED_COMMANDS: dict[str, list[list[str]]] = {
    profile: [list(step.argv) for step in steps]
    for profile, steps in PROFILES.items()
}


def load_report(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON: {exc}"]
    except OSError as exc:
        return None, [f"could not read report: {exc}"]

    if not isinstance(data, dict):
        return None, ["report must be a JSON object"]
    return data, []


def _step_command(step: dict[str, Any]) -> list[str] | None:
    command = step.get("command")
    if isinstance(command, list) and all(isinstance(part, str) for part in command):
        return list(command)
    return None


def _step_return_code(step: dict[str, Any]) -> int | None | str:
    value = step.get("return_code")
    if value is None or isinstance(value, int):
        return value
    return "invalid"


def _expected_command_prefix_length(final_status: str, step_statuses: list[str]) -> int:
    if final_status in {"passed", "dry-run"}:
        return len(step_statuses)
    if "failed" in step_statuses:
        return step_statuses.index("failed") + 1
    return len(step_statuses)


def validate_report(report: dict[str, Any], expected_profile: str, allow_failed: bool = False) -> list[str]:
    errors: list[str] = []

    if expected_profile != SUPPORTED_PROFILE:
        errors.append(f"unsupported expected profile: {expected_profile}")
        return errors

    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(report))
    errors.extend(f"missing top-level field: {field}" for field in missing)

    profile = report.get("profile")
    if profile != expected_profile:
        errors.append(f"profile mismatch: expected {expected_profile}, got {profile}")

    final_status = report.get("final_status")
    if final_status not in ALLOWED_FINAL_STATUSES:
        errors.append(f"invalid final_status: {final_status}")

    report_root = report.get("repo_root", report.get("repository_root"))
    if report_root is None:
        errors.append("missing top-level field: repo_root or repository_root")
    elif not isinstance(report_root, str):
        errors.append("repo_root must be a string")
    else:
        try:
            if Path(report_root).resolve() != REPO_ROOT.resolve():
                errors.append(f"repo_root mismatch: expected {REPO_ROOT}, got {report_root}")
        except OSError as exc:
            errors.append(f"repo_root could not be resolved: {exc}")

    steps = report.get("steps")
    if not isinstance(steps, list):
        errors.append("steps must be a list")
        return errors

    expected_commands = APPROVED_COMMANDS.get(expected_profile, [])
    step_statuses: list[str] = []
    observed_commands: list[list[str]] = []

    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"step {index} must be an object")
            continue

        missing_step = sorted(REQUIRED_STEP_FIELDS - set(step))
        errors.extend(f"step {index} missing field: {field}" for field in missing_step)

        status = step.get("status")
        if status not in ALLOWED_STEP_STATUSES:
            errors.append(f"step {index} invalid status: {status}")
        elif isinstance(status, str):
            step_statuses.append(status)

        command = _step_command(step)
        if command is None:
            errors.append(f"step {index} command must be a list of strings")
        else:
            observed_commands.append(command)

        return_code = _step_return_code(step)
        if return_code == "invalid":
            errors.append(f"step {index} return_code must be an integer or null")

        if status == "passed" and return_code != 0:
            errors.append(f"step {index} passed status requires return_code 0")
        if status == "failed" and (not isinstance(return_code, int) or return_code == 0):
            errors.append(f"step {index} failed status requires nonzero return_code")
        if status == "skipped/dry-run" and return_code is not None:
            errors.append(f"step {index} skipped/dry-run status requires null return_code")

    if final_status in {"passed", "dry-run"} and len(observed_commands) != len(expected_commands):
        errors.append(
            f"{final_status} report must contain all approved steps: "
            f"expected {len(expected_commands)}, got {len(observed_commands)}"
        )

    if final_status == "failed" and len(observed_commands) > len(expected_commands):
        errors.append(
            f"failed report has too many steps: expected at most {len(expected_commands)}, got {len(observed_commands)}"
        )

    prefix_length = _expected_command_prefix_length(str(final_status), step_statuses)
    expected_prefix = expected_commands[:prefix_length]
    observed_prefix = observed_commands[:prefix_length]
    if observed_prefix != expected_prefix:
        errors.append("step commands do not match the approved command list")

    if final_status == "passed" and step_statuses and any(status != "passed" for status in step_statuses):
        errors.append("passed report steps must all be passed")
    if final_status == "dry-run" and step_statuses and any(status != "skipped/dry-run" for status in step_statuses):
        errors.append("dry-run report steps must all be skipped/dry-run")
    if final_status == "failed" and "failed" not in step_statuses:
        errors.append("failed report must include a failed step")
    if final_status == "failed" and not allow_failed:
        errors.append("failed report requires --allow-failed")

    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a bounded local validation JSON report without executing report commands."
    )
    parser.add_argument("report", type=Path, help="Path to the JSON report to verify.")
    parser.add_argument("--profile", required=True, help="Expected approved validation profile.")
    parser.add_argument(
        "--allow-failed",
        action="store_true",
        help="Treat structurally valid failed reports as accepted.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report, load_errors = load_report(args.report)
    if report is None:
        for error in load_errors:
            print(f"FAIL: {error}")
        return 1

    errors = validate_report(report, args.profile, allow_failed=args.allow_failed)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {args.report} matches {args.profile} bounded validation report contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
