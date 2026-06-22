from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_SCHEMA = "kora.bounded_local_validation.v1"


@dataclass(frozen=True)
class ValidationStep:
    name: str
    argv: list[str]


PROFILES: dict[str, list[ValidationStep]] = {
    "kora-local-core": [
        ValidationStep(
            name="fixture quality check evaluator",
            argv=["python3", "scripts/evaluate_fixture_quality_checks.py"],
        ),
        ValidationStep(
            name="fixture quality check tests",
            argv=["python3", "-m", "pytest", "tests/test_fixture_quality_checks.py"],
        ),
        ValidationStep(
            name="representativeness tests",
            argv=[
                "python3",
                "-m",
                "pytest",
                "tests/test_representativeness_seed.py",
                "tests/test_representativeness_route_only_evaluator.py",
            ],
        ),
        ValidationStep(
            name="markdown link check",
            argv=["python3", "scripts/check_markdown_links_goal082b.py"],
        ),
        ValidationStep(
            name="git whitespace check",
            argv=["git", "diff", "--check"],
        ),
        ValidationStep(
            name="full pytest suite",
            argv=["python3", "-m", "pytest"],
        ),
    ],
}


def _step_record(step: ValidationStep, return_code: int | None, status: str) -> dict[str, Any]:
    return {
        "name": step.name,
        "command": list(step.argv),
        "return_code": return_code,
        "status": status,
    }


def build_report(profile: str, dry_run: bool = False) -> tuple[int, dict[str, Any]]:
    if profile not in PROFILES:
        return 2, {
            "report_schema": REPORT_SCHEMA,
            "profile": profile,
            "final_status": "failed",
            "error": f"unknown profile: {profile}",
            "supported_profiles": sorted(PROFILES),
            "steps": [],
        }

    steps = PROFILES[profile]
    if dry_run:
        return 0, {
            "report_schema": REPORT_SCHEMA,
            "profile": profile,
            "final_status": "dry-run",
            "repo_root": str(REPO_ROOT),
            "steps": [_step_record(step, None, "skipped/dry-run") for step in steps],
        }

    records: list[dict[str, Any]] = []
    exit_code = 0
    final_status = "passed"

    for step in steps:
        completed = subprocess.run(
            step.argv,
            cwd=REPO_ROOT,
            shell=False,
            check=False,
        )
        status = "passed" if completed.returncode == 0 else "failed"
        records.append(_step_record(step, completed.returncode, status))
        if completed.returncode != 0:
            exit_code = completed.returncode
            final_status = "failed"
            break

    return exit_code, {
        "report_schema": REPORT_SCHEMA,
        "profile": profile,
        "final_status": final_status,
        "repo_root": str(REPO_ROOT),
        "steps": records,
    }


def render_text_summary(report: dict[str, Any]) -> str:
    lines = [
        f"profile: {report['profile']}",
        f"final_status: {report['final_status']}",
    ]
    if "error" in report:
        lines.append(f"error: {report['error']}")
    for step in report["steps"]:
        return_code = "not-run" if step["return_code"] is None else str(step["return_code"])
        lines.append(f"- {step['status']}: {step['name']} ({return_code})")
    return "\n".join(lines)


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Bounded Local Validation Report",
        "",
        f"- profile: `{report['profile']}`",
        f"- final_status: `{report['final_status']}`",
        f"- repo_root: `{report.get('repo_root', REPO_ROOT)}`",
        "",
        "## Steps",
        "",
        "| Step | Status | Return code | Command |",
        "| --- | --- | --- | --- |",
    ]
    for step in report["steps"]:
        return_code = "" if step["return_code"] is None else str(step["return_code"])
        command = " ".join(step["command"])
        lines.append(f"| {step['name']} | `{step['status']}` | `{return_code}` | `{command}` |")
    if "error" in report:
        lines.extend(["", f"Error: `{report['error']}`"])
    return "\n".join(lines) + "\n"


def write_reports(report: dict[str, Any], json_out: Path | None, md_out: Path | None) -> None:
    if json_out is not None:
        json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if md_out is not None:
        md_out.write_text(render_markdown_report(report), encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run approved bounded local KORA validation profiles."
    )
    parser.add_argument("--profile", required=True, help="Approved validation profile to run.")
    parser.add_argument("--dry-run", action="store_true", help="Report planned steps without executing commands.")
    parser.add_argument("--json-out", type=Path, help="Optional path for a structured JSON report.")
    parser.add_argument("--md-out", type=Path, help="Optional path for a Markdown report.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    exit_code, report = build_report(args.profile, dry_run=args.dry_run)
    write_reports(report, args.json_out, args.md_out)

    if args.json_out is None and args.md_out is None:
        print(render_text_summary(report))
    elif exit_code != 0:
        print(render_text_summary(report))

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
