from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.verify_bounded_local_validation_report import APPROVED_COMMANDS, SUPPORTED_PROFILE, load_report


CATEGORY_BY_COMMAND: dict[tuple[str, ...], str] = {
    ("python3", "scripts/evaluate_fixture_quality_checks.py"): "fixture_quality_failure",
    ("python3", "-m", "pytest", "tests/test_fixture_quality_checks.py"): "fixture_quality_failure",
    (
        "python3",
        "-m",
        "pytest",
        "tests/test_representativeness_seed.py",
        "tests/test_representativeness_route_only_evaluator.py",
    ): "representativeness_failure",
    ("python3", "scripts/check_markdown_links_goal082b.py"): "markdown_link_failure",
    ("git", "diff", "--check"): "diff_check_failure",
    ("python3", "-m", "pytest"): "full_pytest_failure",
}


def _summary(
    *,
    profile: str | None,
    final_status: str | None,
    category: str,
    failing_step: str | None = None,
    failing_command: list[str] | None = None,
    failing_return_code: int | None = None,
    summary: str,
) -> dict[str, Any]:
    return {
        "category": category,
        "failing_command": failing_command,
        "failing_return_code": failing_return_code,
        "failing_step": failing_step,
        "final_status": final_status,
        "profile": profile,
        "summary": summary,
    }


def classify_report(report: dict[str, Any], expected_profile: str) -> tuple[int, dict[str, Any]]:
    profile = report.get("profile")
    final_status = report.get("final_status")

    if expected_profile != SUPPORTED_PROFILE or profile != expected_profile:
        return 1, _summary(
            profile=profile if isinstance(profile, str) else None,
            final_status=final_status if isinstance(final_status, str) else None,
            category="unsupported_profile",
            summary=f"unsupported or mismatched profile; expected {expected_profile}",
        )

    steps = report.get("steps")
    if not isinstance(steps, list):
        return 1, _summary(
            profile=profile,
            final_status=final_status if isinstance(final_status, str) else None,
            category="malformed_report",
            summary="steps must be a list",
        )

    if final_status == "dry-run":
        return 0, _summary(
            profile=profile,
            final_status=final_status,
            category="dry_run_only",
            summary="bounded validation report is a dry-run; no commands were executed by the runner",
        )

    failing_step: dict[str, Any] | None = None
    for step in steps:
        if not isinstance(step, dict):
            return 1, _summary(
                profile=profile,
                final_status=final_status if isinstance(final_status, str) else None,
                category="malformed_report",
                summary="step records must be objects",
            )
        return_code = step.get("return_code")
        status = step.get("status")
        if status == "failed" or (isinstance(return_code, int) and return_code != 0):
            failing_step = step
            break

    if final_status == "passed" and failing_step is None:
        return 0, _summary(
            profile=profile,
            final_status=final_status,
            category="all_passed",
            summary="all bounded validation steps passed",
        )

    if final_status not in {"passed", "failed", "dry-run"}:
        return 1, _summary(
            profile=profile,
            final_status=final_status if isinstance(final_status, str) else None,
            category="malformed_report",
            summary=f"invalid final_status: {final_status}",
        )

    if failing_step is None:
        return 1, _summary(
            profile=profile,
            final_status=final_status,
            category="malformed_report",
            summary="failed report did not include a failing step",
        )

    command = failing_step.get("command")
    if not isinstance(command, list) or not all(isinstance(part, str) for part in command):
        return 1, _summary(
            profile=profile,
            final_status=final_status,
            category="malformed_report",
            failing_step=failing_step.get("name") if isinstance(failing_step.get("name"), str) else None,
            summary="failing step command must be a list of strings",
        )

    category = CATEGORY_BY_COMMAND.get(tuple(command), "unknown_step_failure")
    return_code = failing_step.get("return_code")
    if not isinstance(return_code, int):
        return_code = None

    return 0, _summary(
        profile=profile,
        final_status=final_status,
        category=category,
        failing_step=failing_step.get("name") if isinstance(failing_step.get("name"), str) else None,
        failing_command=command,
        failing_return_code=return_code,
        summary=f"classified first failing bounded validation step as {category}",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify a bounded local validation report without executing report commands."
    )
    parser.add_argument("report", type=Path, help="Path to the JSON report to classify.")
    parser.add_argument("--profile", required=True, help="Expected approved validation profile.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report, load_errors = load_report(args.report)
    if report is None:
        print(
            json.dumps(
                _summary(
                    profile=args.profile,
                    final_status=None,
                    category="malformed_report",
                    summary="; ".join(load_errors),
                ),
                sort_keys=True,
            )
        )
        return 1

    exit_code, result = classify_report(report, args.profile)
    print(json.dumps(result, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
