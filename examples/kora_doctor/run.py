"""Offline KORA Doctor example."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from kora.executor import run_graph
from kora.task_ir import TaskGraph, normalize_graph, validate_graph

EXAMPLE_DIR = Path(__file__).resolve().parent
DEFAULT_WORKLOAD = EXAMPLE_DIR / "workload.json"
WORKLOADS_DIR = EXAMPLE_DIR / "workloads"
CLAIM_BOUNDARY = (
    "In these offline sample workloads, KORA Doctor identifies deterministic candidates "
    "and provider-needed candidates without making provider calls. "
    "It does not claim production diagnostic accuracy, automatic cost reduction, "
    "real API-cost proof, benchmark superiority, broad workload superiority, or "
    "production proxy readiness."
)


def load_workload(path: Path = DEFAULT_WORKLOAD) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sample_workload_paths(workloads_root: Path | None = None) -> list[Path]:
    root = workloads_root or EXAMPLE_DIR
    default_workload = root / "workload.json"
    workloads_dir = root / "workloads"
    paths = [default_workload]
    if workloads_dir.exists():
        paths.extend(sorted(workloads_dir.glob("*.json")))
    return paths


def _task_text(item: dict[str, Any]) -> str:
    return f"{item.get('title', '')} {item.get('description', '')}"


def _doctor_graph(workload: dict[str, Any], item: dict[str, Any]) -> TaskGraph:
    return TaskGraph.model_validate(
        {
            "graph_id": f"kora-doctor-{item['id']}",
            "version": "0.1",
            "root": "doctor_inspect",
            "defaults": {"budget": {"max_time_ms": 1500, "max_tokens": 300, "max_retries": 0}},
            "tasks": [
                {
                    "id": "doctor_inspect",
                    "type": "det.doctor.inspect_task",
                    "deps": [],
                    "in": {"text": _task_text(item)},
                    "run": {
                        "kind": "det",
                        "spec": {
                            "handler": "doctor_inspect_task",
                            "args": {
                                "deterministic_rules": workload["deterministic_rules"],
                                "provider_needed_rules": workload["provider_needed_rules"],
                            },
                        },
                    },
                    "policy": {"on_fail": "fail"},
                    "tags": ["kora-doctor", "offline-example"],
                }
            ],
        }
    )


def _run_doctor_task(workload: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    graph = normalize_graph(_doctor_graph(workload, item))
    validate_graph(graph)
    result = run_graph(graph)
    if not result.get("ok"):
        raise RuntimeError(str(result.get("error")))
    final = result.get("final")
    if not isinstance(final, dict):
        raise RuntimeError("doctor graph did not return an object")
    inspected = dict(final)
    inspected.update(
        {
            "id": item["id"],
            "title": item["title"],
            "description": item["description"],
            "kora_graph_id": result["graph_id"],
            "kora_event_count": len(result.get("events", [])),
        }
    )
    return inspected


def build_doctor_summary(
    workload_path: Path = DEFAULT_WORKLOAD,
    *,
    json_out: Path | None = None,
) -> dict[str, Any]:
    workload = load_workload(workload_path)
    tasks = workload["tasks"]
    inspections = [_run_doctor_task(workload, item) for item in tasks]
    deterministic_candidates = sum(
        1 for item in inspections if item["route_kind"] == "deterministic_candidate"
    )
    provider_needed_candidates = sum(
        1 for item in inspections if item["route_kind"] == "provider_needed_candidate"
    )
    provider_calls = sum(int(item["provider_calls"]) for item in inspections)
    expected_match_count = sum(
        1
        for expected, actual in zip(tasks, inspections, strict=True)
        if expected["expected_route_kind"] == actual["route_kind"]
        and expected["expected_suggested_handler"] == actual["suggested_handler"]
    )
    suggested_handlers = sorted(
        {
            str(item["suggested_handler"])
            for item in inspections
            if item.get("suggested_handler")
        }
    )
    fallback_reasons = []
    for item in inspections:
        reason = item.get("provider_needed_reason")
        if reason and reason not in fallback_reasons:
            fallback_reasons.append(str(reason))

    summary: dict[str, Any] = {
        "ok": expected_match_count == len(tasks) and provider_calls == 0,
        "mode": "kora_doctor_example",
        "workload_path": str(workload_path),
        "workload_id": workload["workload_id"],
        "privacy_class": workload["privacy_class"],
        "total_tasks": len(tasks),
        "deterministic_candidates": deterministic_candidates,
        "provider_needed_candidates": provider_needed_candidates,
        "avoided_provider_invocations": deterministic_candidates,
        "provider_calls_actually_made": provider_calls,
        "expected_match_count": expected_match_count,
        "suggested_deterministic_handlers": suggested_handlers,
        "provider_model_fallback_recommended_for": fallback_reasons,
        "inspections": inspections,
        "next_step_recommendations": [
            "Promote deterministic candidates into explicit KORA handlers or rules.",
            "Add cache keys for repeat lookups before provider fallback.",
            "Keep provider-needed candidates separated from deterministic handlers.",
            "Add fixtures and expected counters before expanding this example to real project data.",
        ],
        "safe_example_claim": (
            "In these offline sample workloads, KORA Doctor identifies deterministic candidates "
            "and provider-needed candidates without making provider calls."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def build_aggregate_summary(
    workloads_root: Path | None = None,
    *,
    json_out: Path | None = None,
) -> dict[str, Any]:
    workload_summaries = [build_doctor_summary(path) for path in sample_workload_paths(workloads_root)]
    total_tasks = sum(item["total_tasks"] for item in workload_summaries)
    deterministic_candidates = sum(item["deterministic_candidates"] for item in workload_summaries)
    provider_needed_candidates = sum(item["provider_needed_candidates"] for item in workload_summaries)
    provider_calls = sum(item["provider_calls_actually_made"] for item in workload_summaries)
    suggested_handlers = sorted(
        {
            handler
            for item in workload_summaries
            for handler in item["suggested_deterministic_handlers"]
        }
    )
    fallback_reasons: list[str] = []
    for item in workload_summaries:
        for reason in item["provider_model_fallback_recommended_for"]:
            if reason not in fallback_reasons:
                fallback_reasons.append(reason)
    inspections = [
        dict(inspection, workload_id=item["workload_id"])
        for item in workload_summaries
        for inspection in item["inspections"]
    ]
    summary: dict[str, Any] = {
        "ok": all(item["ok"] for item in workload_summaries) and provider_calls == 0,
        "mode": "kora_doctor_report_pack",
        "workloads_root": str(workloads_root or EXAMPLE_DIR),
        "workload_count": len(workload_summaries),
        "workload_ids": [item["workload_id"] for item in workload_summaries],
        "total_tasks": total_tasks,
        "deterministic_candidates": deterministic_candidates,
        "provider_needed_candidates": provider_needed_candidates,
        "avoided_provider_invocations": deterministic_candidates,
        "provider_calls_actually_made": provider_calls,
        "suggested_deterministic_handlers": suggested_handlers,
        "provider_model_fallback_recommended_for": fallback_reasons,
        "workload_summaries": workload_summaries,
        "inspections": inspections,
        "next_step_recommendations": [
            "Promote deterministic candidates into explicit KORA handlers or rules.",
            "Add cache keys for repeat lookups before provider fallback.",
            "Keep provider-needed candidates separated from deterministic handlers.",
            "Use the README refresh proposal before rewriting top-level positioning.",
        ],
        "safe_example_claim": (
            "In these offline sample workloads, KORA Doctor identifies deterministic candidates "
            "and provider-needed candidates without making provider calls."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def render_text_report(summary: dict[str, Any]) -> str:
    title = "KORA Doctor Report Pack" if summary["mode"] == "kora_doctor_report_pack" else "KORA Doctor Example"
    lines = [
        title,
        "",
        f"Workload: {summary['workload_id']}" if summary["mode"] != "kora_doctor_report_pack" else f"Workloads: {summary['workload_count']}",
        f"Total tasks: {summary['total_tasks']}",
        f"Deterministic candidates: {summary['deterministic_candidates']}",
        f"Provider-needed candidates: {summary['provider_needed_candidates']}",
        "Suggested deterministic handlers:",
    ]
    for handler in summary["suggested_deterministic_handlers"]:
        lines.append(f"- {handler}")
    lines.append("")
    lines.append("Provider/model fallback recommended for:")
    for reason in summary["provider_model_fallback_recommended_for"]:
        lines.append(f"- {reason}")
    lines.extend(
        [
            "",
            f"Avoided simulated provider/model invocations: {summary['avoided_provider_invocations']}",
            f"Provider calls actually made: {summary['provider_calls_actually_made']}",
        "",
        ]
    )
    if summary["mode"] == "kora_doctor_report_pack":
        lines.extend(
            [
                "Workload counters:",
            ]
        )
        for item in summary["workload_summaries"]:
            lines.append(
                "- {workload}: total={total}, deterministic={det}, provider_needed={provider}, provider_calls={calls}".format(
                    workload=item["workload_id"],
                    total=item["total_tasks"],
                    det=item["deterministic_candidates"],
                    provider=item["provider_needed_candidates"],
                    calls=item["provider_calls_actually_made"],
                )
            )
        lines.append("")
    lines.extend(
        [
            "Route rationale:",
        ]
    )
    for item in summary["inspections"]:
        lines.append(
            "- {id}: {route} via {selected} - {rationale}".format(
                id=item["id"],
                route=item["route_kind"],
                selected=item["selected_route"],
                rationale=item["route_rationale"],
            )
        )
    lines.extend(["", "Next-step recommendations:"])
    for recommendation in summary["next_step_recommendations"]:
        lines.append(f"- {recommendation}")
    lines.extend(["", "Claim boundary:", summary["claim_boundary"]])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workload", default=str(DEFAULT_WORKLOAD), help="sample workload JSON path")
    parser.add_argument("--all", action="store_true", help="run all bundled sample workloads")
    parser.add_argument("--json-out", help="optional output path for structured JSON")
    parser.add_argument("--report-md", help="optional output path for the text report")
    args = parser.parse_args()

    if args.all:
        summary = build_aggregate_summary(json_out=Path(args.json_out) if args.json_out else None)
    else:
        summary = build_doctor_summary(
            Path(args.workload),
            json_out=Path(args.json_out) if args.json_out else None,
        )
    report = render_text_report(summary)
    if args.report_md:
        report_path = Path(args.report_md)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
    print(report, end="")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
