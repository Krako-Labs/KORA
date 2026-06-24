from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_TAIL_LIMIT = 2000


@dataclass(frozen=True)
class SmokeCommand:
    label: str
    argv: list[str]


SMOKE_PROFILES: dict[str, list[SmokeCommand]] = {
    "first-run-cli-core": [
        SmokeCommand(
            label="kora doctor single workload",
            argv=[
                "python3",
                "-m",
                "kora",
                "doctor",
                "examples/kora_doctor/customer_support_workload.json",
            ],
        ),
        SmokeCommand(
            label="kora doctor aggregate workloads",
            argv=["python3", "-m", "kora", "doctor", "--all", "examples/kora_doctor/"],
        ),
        SmokeCommand(
            label="kora proxy demo",
            argv=[
                "python3",
                "-m",
                "kora",
                "proxy-demo",
                "examples/openai_compatible_proxy/requests.json",
            ],
        ),
        SmokeCommand(
            label="deterministic classification example",
            argv=["python3", "examples/deterministic_classification/run.py"],
        ),
        SmokeCommand(
            label="cache reuse example",
            argv=["python3", "examples/cache_reuse/run.py"],
        ),
        SmokeCommand(
            label="rag routing example",
            argv=["python3", "examples/rag_routing/run.py"],
        ),
        SmokeCommand(
            label="agent workflow optimization example",
            argv=["python3", "examples/agent_workflow_optimization/run.py"],
        ),
    ],
}


Runner = Callable[..., subprocess.CompletedProcess[str]]


def _tail_text(value: str | None) -> str:
    if not value:
        return ""
    if len(value) <= OUTPUT_TAIL_LIMIT:
        return value
    return value[-OUTPUT_TAIL_LIMIT:]


def _command_record(
    command: SmokeCommand,
    status: str,
    return_code: int | None,
    elapsed_seconds: float,
    stdout: str = "",
    stderr: str = "",
) -> dict[str, Any]:
    return {
        "label": command.label,
        "argv": list(command.argv),
        "status": status,
        "return_code": return_code,
        "elapsed_seconds": round(elapsed_seconds, 3),
        "stdout_tail": _tail_text(stdout),
        "stderr_tail": _tail_text(stderr),
    }


def _summary(records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    planned = sum(1 for record in records if record["status"] == "planned")
    passed = sum(1 for record in records if record["status"] == "passed")
    failed = sum(1 for record in records if record["status"] == "failed")
    if failed:
        final_status = "failed"
    elif planned:
        final_status = "planned"
    else:
        final_status = "passed"
    return {
        "total_commands": len(records),
        "planned_commands": planned,
        "passed_commands": passed,
        "failed_commands": failed,
        "final_status": final_status,
    }


def build_report(
    profile: str,
    *,
    dry_run: bool = False,
    continue_on_failure: bool = False,
    runner: Runner = subprocess.run,
    clock: Callable[[], float] = time.perf_counter,
) -> tuple[int, dict[str, Any]]:
    if profile not in SMOKE_PROFILES:
        report = {
            "profile": profile,
            "repo_root": str(REPO_ROOT),
            "final_status": "failed",
            "summary": {
                "total_commands": 0,
                "planned_commands": 0,
                "passed_commands": 0,
                "failed_commands": 0,
                "final_status": "failed",
            },
            "error": f"unknown profile: {profile}",
            "supported_profiles": sorted(SMOKE_PROFILES),
            "commands": [],
        }
        return 2, report

    records: list[dict[str, Any]] = []
    exit_code = 0
    for command in SMOKE_PROFILES[profile]:
        if dry_run:
            records.append(_command_record(command, "planned", None, 0.0))
            continue

        start = clock()
        completed = runner(
            command.argv,
            cwd=REPO_ROOT,
            shell=False,
            check=False,
            text=True,
            capture_output=True,
        )
        elapsed = clock() - start
        status = "passed" if completed.returncode == 0 else "failed"
        records.append(
            _command_record(
                command,
                status,
                completed.returncode,
                elapsed,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )
        )
        if completed.returncode != 0:
            exit_code = completed.returncode
            if not continue_on_failure:
                break

    summary = _summary(records)
    report = {
        "profile": profile,
        "repo_root": str(REPO_ROOT),
        "final_status": summary["final_status"],
        "summary": summary,
        "commands": records,
    }
    return exit_code, report


def render_text_summary(report: dict[str, Any]) -> str:
    lines = [
        f"profile: {report['profile']}",
        f"final_status: {report['final_status']}",
    ]
    if "error" in report:
        lines.append(f"error: {report['error']}")
    for command in report["commands"]:
        return_code = "not-run" if command["return_code"] is None else str(command["return_code"])
        lines.append(f"- {command['status']}: {command['label']} ({return_code})")
    return "\n".join(lines)


def render_markdown_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# First-Run CLI Smoke Report",
        "",
        f"- profile: `{report['profile']}`",
        f"- final_status: `{report['final_status']}`",
        f"- repo_root: `{report['repo_root']}`",
        f"- total_commands: `{summary['total_commands']}`",
        f"- planned_commands: `{summary['planned_commands']}`",
        f"- passed_commands: `{summary['passed_commands']}`",
        f"- failed_commands: `{summary['failed_commands']}`",
        "",
        "## Commands",
        "",
        "| Label | Status | Return code | Elapsed seconds | Command |",
        "| --- | --- | --- | --- | --- |",
    ]
    for command in report["commands"]:
        return_code = "" if command["return_code"] is None else str(command["return_code"])
        argv = " ".join(command["argv"])
        lines.append(
            f"| {command['label']} | `{command['status']}` | `{return_code}` | "
            f"`{command['elapsed_seconds']}` | `{argv}` |"
        )
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
        description="Run approved local first-run KORA CLI smoke checks."
    )
    parser.add_argument(
        "--profile",
        default="first-run-cli-core",
        help="Approved smoke profile to run. Defaults to first-run-cli-core.",
    )
    parser.add_argument("--dry-run", action="store_true", help="List planned commands without executing them.")
    parser.add_argument(
        "--continue-on-failure",
        action="store_true",
        help="Continue running remaining smoke commands after a failed command.",
    )
    parser.add_argument("--json-out", type=Path, help="Optional path for a structured JSON report.")
    parser.add_argument("--md-out", type=Path, help="Optional path for a Markdown report.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    exit_code, report = build_report(
        args.profile,
        dry_run=args.dry_run,
        continue_on_failure=args.continue_on_failure,
    )
    write_reports(report, args.json_out, args.md_out)

    if args.json_out is None and args.md_out is None:
        print(render_text_summary(report))
    elif exit_code != 0:
        print(render_text_summary(report))

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
