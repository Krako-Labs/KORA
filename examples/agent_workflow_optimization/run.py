"""Offline agent workflow optimization example using KORA task execution."""

from __future__ import annotations

import argparse
import hashlib
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
WORKFLOWS_PATH = EXAMPLE_DIR / "workflows.json"
EXPECTED_COUNTERS_PATH = EXAMPLE_DIR / "expected_counters.json"
CLAIM_BOUNDARY = (
    "In this offline agent-workflow example, KORA routes sample workflow steps "
    "across deterministic, cache, tool-needed, and provider-needed paths without "
    "making provider calls. It does not claim production agent readiness, "
    "autonomous agent reliability, automatic cost reduction, real API-cost proof, "
    "or benchmark superiority."
)


def load_workflows(path: Path = WORKFLOWS_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _step_cache_key(workflow_id: str, step: dict[str, Any]) -> str:
    canonical = json.dumps(
        {
            "workflow_id": workflow_id,
            "description": step.get("description", ""),
            "step_type": step.get("step_type", ""),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _agent_step_graph(config: dict[str, Any], workflow: dict[str, Any], step: dict[str, Any]) -> TaskGraph:
    step_payload = dict(step)
    step_payload["workflow_id"] = workflow["id"]
    return TaskGraph.model_validate(
        {
            "graph_id": f"agent-workflow-{workflow['id']}-{step['id']}",
            "version": "0.1",
            "root": "route_step",
            "defaults": {"budget": {"max_time_ms": 1500, "max_tokens": 300, "max_retries": 0}},
            "tasks": [
                {
                    "id": "route_step",
                    "type": "det.agent.route_step",
                    "deps": [],
                    "in": {"step": step_payload},
                    "run": {
                        "kind": "det",
                        "spec": {
                            "handler": "agent_route_step",
                            "args": {
                                "workflow_id": workflow["id"],
                                "deterministic_handlers": config["deterministic_handlers"],
                                "tool_handlers": config["tool_handlers"],
                                "provider_needed_types": config["provider_needed_types"],
                            },
                        },
                    },
                    "policy": {"on_fail": "fail"},
                    "tags": ["agent-workflow-optimization", "offline-example", workflow["id"]],
                }
            ],
        }
    )


def _run_kora_agent_step(config: dict[str, Any], workflow: dict[str, Any], step: dict[str, Any]) -> dict[str, Any]:
    graph = normalize_graph(_agent_step_graph(config, workflow, step))
    validate_graph(graph)
    result = run_graph(graph)
    if not result.get("ok"):
        raise RuntimeError(str(result.get("error")))
    final = result.get("final")
    if not isinstance(final, dict):
        raise RuntimeError("agent workflow graph did not return an object")
    routed = dict(final)
    routed.update(
        {
            "kora_graph_id": result["graph_id"],
            "kora_event_count": len(result.get("events", [])),
        }
    )
    return routed


def build_agent_workflow_summary(
    *,
    workflows_path: Path = WORKFLOWS_PATH,
    json_out: Path | None = None,
) -> dict[str, Any]:
    config = load_workflows(workflows_path)
    cache: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []

    for workflow in config["workflows"]:
        workflow_id = str(workflow["id"])
        for step in workflow["steps"]:
            step_id = str(step["id"])
            cache_key = _step_cache_key(workflow_id, step)

            if cache_key in cache:
                cached = cache[cache_key]
                route = dict(cached["route"])
                route.update(
                    {
                        "route_kind": "cache_hit",
                        "selected_route": "agent.cache.reuse",
                        "handler": "cache_reuse",
                        "provider_needed_reason": None,
                    }
                )
                source = "cache"
                graph_id = cached["route"].get("kora_graph_id")
                event_count = 0
            else:
                route = _run_kora_agent_step(config, workflow, step)
                source = "kora_task_graph"
                graph_id = route.get("kora_graph_id")
                event_count = int(route.get("kora_event_count", 0))
                if route["route_kind"] == "deterministic":
                    cache[cache_key] = {"route": route}

            results.append(
                {
                    "workflow_id": workflow_id,
                    "workflow_label": workflow["label"],
                    "id": step_id,
                    "description": step["description"],
                    "step_type": step["step_type"],
                    "route_kind": route["route_kind"],
                    "selected_route": route["selected_route"],
                    "handler": route["handler"],
                    "step_output": route.get("step_output"),
                    "tool_name": route.get("tool_name"),
                    "provider_needed_reason": route.get("provider_needed_reason"),
                    "provider_calls": int(route.get("provider_calls", 0)),
                    "cache_key": cache_key,
                    "source": source,
                    "kora_graph_id": graph_id,
                    "kora_event_count": event_count,
                    "expected_route_kind": step["expected_route_kind"],
                    "expected_handler": step["expected_handler"],
                }
            )

    total_workflow_steps = len(results)
    deterministic_steps = sum(1 for item in results if item["route_kind"] == "deterministic")
    cache_hits = sum(1 for item in results if item["route_kind"] == "cache_hit")
    tool_needed_steps = sum(1 for item in results if item["route_kind"] == "tool_needed")
    provider_needed_steps = sum(1 for item in results if item["route_kind"] == "provider_needed")
    provider_calls = sum(int(item["provider_calls"]) for item in results)
    expected_match_count = sum(
        1
        for item in results
        if item["route_kind"] == item["expected_route_kind"]
        and item["handler"] == item["expected_handler"]
    )
    counters = {
        "total_workflow_steps": total_workflow_steps,
        "deterministic_steps": deterministic_steps,
        "cache_hits": cache_hits,
        "tool_needed_steps": tool_needed_steps,
        "provider_needed_steps": provider_needed_steps,
        "avoided_provider_invocations": deterministic_steps + cache_hits,
        "provider_calls_actually_made": provider_calls,
    }
    expected_counters = json.loads(EXPECTED_COUNTERS_PATH.read_text(encoding="utf-8"))
    summary: dict[str, Any] = {
        "ok": counters == expected_counters and expected_match_count == total_workflow_steps,
        "mode": "agent_workflow_optimization_example",
        **counters,
        "expected_match_count": expected_match_count,
        "workflow_set_id": config["workflow_set_id"],
        "workflow_count": len(config["workflows"]),
        "results": results,
        "example_step": results[0],
        "safe_example_claim": (
            "In this offline agent-workflow example, KORA routes sample workflow steps "
            "across deterministic, cache, tool-needed, and provider-needed paths without "
            "making provider calls."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def render_report(summary: dict[str, Any]) -> str:
    example = summary["example_step"]
    lines = [
        "KORA Agent Workflow Optimization Example",
        "",
        f"Total workflow steps: {summary['total_workflow_steps']}",
        f"Deterministic steps: {summary['deterministic_steps']}",
        f"Cache hits: {summary['cache_hits']}",
        f"Tool-needed steps: {summary['tool_needed_steps']}",
        f"Provider-needed steps: {summary['provider_needed_steps']}",
        f"Avoided simulated provider/model invocations: {summary['avoided_provider_invocations']}",
        f"Provider calls actually made: {summary['provider_calls_actually_made']}",
        "",
        "Example step:",
        f"- Workflow: {example['workflow_label']}",
        f"- Step: \"{example['description']}\"",
        f"- Route: {example['route_kind']}",
        f"- Handler: {example['handler']}",
        f"- Provider calls: {example['provider_calls']}",
        "",
        "Comparison surface:",
    ]
    for item in summary["results"]:
        lines.append(
            "- {id}: workflow={workflow}, route={route}, handler={handler}, provider_calls={calls}, source={source}".format(
                id=item["id"],
                workflow=item["workflow_id"],
                route=item["route_kind"],
                handler=item["handler"],
                calls=item["provider_calls"],
                source=item["source"],
            )
        )
    lines.extend(["", "Claim boundary:", summary["claim_boundary"]])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflows", default=str(WORKFLOWS_PATH), help="offline agent workflow fixture JSON")
    parser.add_argument("--json-out", help="optional path for structured JSON output")
    parser.add_argument("--report-md", help="optional path for rendered report output")
    args = parser.parse_args()

    summary = build_agent_workflow_summary(
        workflows_path=Path(args.workflows),
        json_out=Path(args.json_out) if args.json_out else None,
    )
    report = render_report(summary)
    if args.report_md:
        report_path = Path(args.report_md)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
    print(report, end="")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
