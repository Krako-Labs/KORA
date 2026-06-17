"""Deterministic classification example pack using KORA task execution."""

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
DATASETS_DIR = EXAMPLE_DIR / "datasets"
DEFAULT_SCENARIO = "support_ticket_routing"
CLAIM_BOUNDARY = (
    "This example pack uses synthetic classification records to show deterministic routing "
    "and explicit provider-needed fallback surfaces. It does not claim production cost "
    "reduction, real API-cost proof, benchmark superiority, broad workload superiority, "
    "or production validation."
)


def load_dataset(path: Path | None = None) -> dict[str, Any]:
    dataset_path = path or DATASETS_DIR / f"{DEFAULT_SCENARIO}.json"
    return json.loads(dataset_path.read_text(encoding="utf-8"))


def load_scenario_datasets(
    *,
    scenario: str = "all",
    datasets_dir: Path = DATASETS_DIR,
) -> list[dict[str, Any]]:
    paths = sorted(datasets_dir.glob("*.json"))
    datasets = [load_dataset(path) for path in paths]
    if scenario == "all":
        return datasets
    selected = [dataset for dataset in datasets if dataset["scenario_id"] == scenario]
    if not selected:
        available = ", ".join(dataset["scenario_id"] for dataset in datasets)
        raise ValueError(f"unknown scenario {scenario!r}; available: {available}")
    return selected


def _item_text(item: dict[str, Any]) -> str:
    return f"{item.get('subject', '')} {item.get('body', '')}"


def _classification_graph(scenario: dict[str, Any], item: dict[str, Any]) -> TaskGraph:
    scenario_id = str(scenario["scenario_id"])
    item_id = str(item["id"])
    return TaskGraph.model_validate(
        {
            "graph_id": f"deterministic-classification-{scenario_id}-{item_id}",
            "version": "0.1",
            "root": "classify",
            "defaults": {"budget": {"max_time_ms": 1500, "max_tokens": 300, "max_retries": 0}},
            "tasks": [
                {
                    "id": "classify",
                    "type": f"det.classification.{scenario_id}",
                    "deps": [],
                    "in": {"text": _item_text(item)},
                    "run": {
                        "kind": "det",
                        "spec": {
                            "handler": "classify_by_rules",
                            "args": {
                                "scenario_id": scenario_id,
                                "routes": scenario["routes"],
                                "provider_required_route": scenario["provider_required_route"],
                            },
                        },
                    },
                    "policy": {"on_fail": "fail"},
                    "tags": ["deterministic-classification", scenario_id],
                }
            ],
        }
    )


def _run_kora_classification(scenario: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    graph = normalize_graph(_classification_graph(scenario, item))
    validate_graph(graph)
    result = run_graph(graph)
    if not result.get("ok"):
        raise RuntimeError(str(result.get("error")))
    final = result.get("final")
    if not isinstance(final, dict):
        raise RuntimeError("classification graph did not return an object")
    classification = dict(final)
    classification.update(
        {
            "scenario_id": scenario["scenario_id"],
            "scenario_label": scenario["scenario_label"],
            "id": item["id"],
            "input": {
                "id": item["id"],
                "subject": item["subject"],
                "body": item["body"],
            },
            "kora_graph_id": result["graph_id"],
            "kora_event_count": len(result.get("events", [])),
        }
    )
    return classification


def _category(result: dict[str, Any]) -> str | None:
    output = result.get("classification_output")
    if not isinstance(output, dict):
        return None
    category = output.get("category")
    return str(category) if category is not None else None


def run_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    items = scenario["items"]
    results = [_run_kora_classification(scenario, item) for item in items]
    deterministic_routes = sum(1 for result in results if result["route_kind"] == "deterministic")
    provider_needed_routes = sum(1 for result in results if result["route_kind"] == "provider_required")
    provider_calls = sum(int(result["provider_calls"]) for result in results)
    expected_match_count = sum(
        1
        for item, result in zip(items, results, strict=True)
        if item["expected_route"] == result["route_kind"]
        and (item["expected_category"] is None or item["expected_category"] == _category(result))
    )
    comparison = [
        {
            "scenario_id": result["scenario_id"],
            "id": result["id"],
            "input_subject": result["input"]["subject"],
            "route_kind": result["route_kind"],
            "selected_route": result["selected_route"],
            "classification_category": _category(result),
            "provider_call_performed": False,
            "provider_needed_reason": result["provider_needed_reason"],
        }
        for result in results
    ]
    return {
        "ok": expected_match_count == len(items) and provider_calls == 0,
        "scenario_id": scenario["scenario_id"],
        "scenario_label": scenario["scenario_label"],
        "privacy_class": scenario["privacy_class"],
        "total_tasks": len(items),
        "deterministic_routes": deterministic_routes,
        "provider_needed_routes": provider_needed_routes,
        "avoided_provider_invocations": deterministic_routes,
        "provider_calls": provider_calls,
        "expected_match_count": expected_match_count,
        "results": results,
        "comparison": comparison,
    }


def build_pack_summary(
    *,
    scenario: str = "all",
    json_out: Path | None = None,
) -> dict[str, Any]:
    scenario_summaries = [run_scenario(dataset) for dataset in load_scenario_datasets(scenario=scenario)]
    total_tasks = sum(item["total_tasks"] for item in scenario_summaries)
    deterministic_routes = sum(item["deterministic_routes"] for item in scenario_summaries)
    provider_needed_routes = sum(item["provider_needed_routes"] for item in scenario_summaries)
    provider_calls = sum(item["provider_calls"] for item in scenario_summaries)
    comparison = [row for item in scenario_summaries for row in item["comparison"]]
    summary: dict[str, Any] = {
        "ok": all(item["ok"] for item in scenario_summaries) and provider_calls == 0,
        "mode": "deterministic_classification_expansion_pack",
        "scenario": scenario,
        "scenario_count": len(scenario_summaries),
        "scenario_ids": [item["scenario_id"] for item in scenario_summaries],
        "total_tasks": total_tasks,
        "deterministic_routes": deterministic_routes,
        "provider_needed_routes": provider_needed_routes,
        "avoided_provider_invocations": deterministic_routes,
        "provider_calls": provider_calls,
        "provider_calls_actually_made": provider_calls,
        "scenario_summaries": scenario_summaries,
        "comparison": comparison,
        "aggregate_evidence_summary": {
            "total_tasks": total_tasks,
            "deterministic_routes": deterministic_routes,
            "provider_needed_routes": provider_needed_routes,
            "avoided_provider_invocations": deterministic_routes,
            "provider_calls_actually_made": provider_calls,
        },
        "safe_example_claim": (
            "In this example pack, KORA routes "
            f"{deterministic_routes} of {total_tasks} sample classification tasks to "
            "deterministic handlers, avoiding simulated provider/model invocation for "
            "those sample tasks."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "notes": [
            "Every classification item is executed through a KORA TaskGraph using the deterministic classify_by_rules handler.",
            "Provider-needed cases are labeled for fallback comparison, but no provider or model call is performed.",
            "Avoided provider invocations are simulated within this synthetic example pack only.",
        ],
    }
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def build_deterministic_classification_summary(
    *,
    scenario: str = DEFAULT_SCENARIO,
    json_out: Path | None = None,
) -> dict[str, Any]:
    """Compatibility wrapper for the original support-ticket example."""
    return build_pack_summary(scenario=scenario, json_out=json_out)


def render_report(summary: dict[str, Any]) -> str:
    evidence = summary["aggregate_evidence_summary"]
    lines = [
        "# Deterministic Classification Expansion Pack Report",
        "",
        summary["safe_example_claim"],
        "",
        "## Aggregate Evidence Summary",
        "",
        f"- Total tasks: `{evidence['total_tasks']}`",
        f"- Deterministic routes: `{evidence['deterministic_routes']}`",
        f"- Provider-needed routes: `{evidence['provider_needed_routes']}`",
        f"- Avoided provider invocations: `{evidence['avoided_provider_invocations']}`",
        f"- Provider calls actually made: `{evidence['provider_calls_actually_made']}`",
        "",
        "## Scenario Counters",
        "",
        "| Scenario | Total | Deterministic | Provider-needed | Provider calls |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for item in summary["scenario_summaries"]:
        lines.append(
            f"| `{item['scenario_id']}` | `{item['total_tasks']}` | "
            f"`{item['deterministic_routes']}` | `{item['provider_needed_routes']}` | "
            f"`{item['provider_calls']}` |"
        )
    lines.extend(
        [
            "",
            "## Comparison Surface",
            "",
            "| Scenario | Item | Route kind | Selected route | Classification | Provider call | Provider-needed reason |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in summary["comparison"]:
        lines.append(
            "| {scenario} | {id} | `{route_kind}` | `{route}` | `{category}` | `{provider_call}` | {reason} |".format(
                scenario=item["scenario_id"],
                id=item["id"],
                route_kind=item["route_kind"],
                route=item["selected_route"],
                category=item["classification_category"] or "",
                provider_call=str(item["provider_call_performed"]).lower(),
                reason=item["provider_needed_reason"] or "",
            )
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "- This is not production cost reduction evidence.",
            "- This is not real API-cost proof.",
            "- This is not benchmark superiority evidence.",
            "- This is not broad workload superiority evidence.",
            "- This is not production validation.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", default="all", help="scenario id to run, or all")
    parser.add_argument("--json-out", help="optional output path for structured JSON")
    parser.add_argument("--report-md", help="optional output path for markdown evidence report")
    args = parser.parse_args()

    summary = build_pack_summary(
        scenario=args.scenario,
        json_out=Path(args.json_out) if args.json_out else None,
    )
    if args.report_md:
        report_path = Path(args.report_md)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_report(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
