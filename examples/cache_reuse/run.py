"""Offline cache reuse example using KORA task execution."""

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
REQUESTS_PATH = EXAMPLE_DIR / "requests.json"
EXPECTED_COUNTERS_PATH = EXAMPLE_DIR / "expected_counters.json"
CLAIM_BOUNDARY = (
    "In this offline cache-reuse example, KORA routes repeated sample requests "
    "to cache hits without making provider calls and marks ambiguous/open-ended "
    "requests as provider-needed. It does not claim production cache correctness, "
    "automatic cost reduction, real API-cost proof, or benchmark superiority."
)


def load_requests(path: Path = REQUESTS_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _cache_key(item: dict[str, Any]) -> str:
    semantic_key = item.get("semantic_cache_key")
    if isinstance(semantic_key, str) and semantic_key.strip():
        normalized = " ".join(semantic_key.lower().strip().split())
    else:
        normalized = " ".join(str(item.get("text", "")).lower().strip().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _classification_graph(config: dict[str, Any], request_id: str, text: str) -> TaskGraph:
    return TaskGraph.model_validate(
        {
            "graph_id": f"cache-reuse-{request_id}",
            "version": "0.1",
            "root": "classify",
            "defaults": {"budget": {"max_time_ms": 1500, "max_tokens": 300, "max_retries": 0}},
            "tasks": [
                {
                    "id": "classify",
                    "type": "det.cache_reuse.classification",
                    "deps": [],
                    "in": {"text": text},
                    "run": {
                        "kind": "det",
                        "spec": {
                            "handler": "classify_by_rules",
                            "args": {
                                "scenario_id": "cache_reuse",
                                "routes": config["routes"],
                                "provider_required_route": config["provider_required_route"],
                            },
                        },
                    },
                    "policy": {"on_fail": "fail"},
                    "tags": ["cache-reuse", "offline-example"],
                }
            ],
        }
    )


def _run_kora_classification(config: dict[str, Any], request_id: str, text: str) -> dict[str, Any]:
    graph = normalize_graph(_classification_graph(config, request_id, text))
    validate_graph(graph)
    result = run_graph(graph)
    if not result.get("ok"):
        raise RuntimeError(str(result.get("error")))
    final = result.get("final")
    if not isinstance(final, dict):
        raise RuntimeError("cache reuse graph did not return an object")
    routed = dict(final)
    routed.update(
        {
            "kora_graph_id": result["graph_id"],
            "kora_event_count": len(result.get("events", [])),
        }
    )
    return routed


def build_cache_reuse_summary(
    *,
    requests_path: Path = REQUESTS_PATH,
    json_out: Path | None = None,
) -> dict[str, Any]:
    config = load_requests(requests_path)
    cache: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []

    for item in config["requests"]:
        request_id = str(item["id"])
        text = str(item["text"])
        cache_key = _cache_key(item)

        if cache_key in cache:
            cached = cache[cache_key]
            route = dict(cached["route"])
            route.update(
                {
                    "route_kind": "cache_hit",
                    "selected_route": "cache.reuse.hit",
                    "provider_needed_reason": None,
                }
            )
            handler = "cache_reuse"
            source = "cache"
            graph_id = cached["route"].get("kora_graph_id")
            event_count = 0
        else:
            route = _run_kora_classification(config, request_id, text)
            handler = (
                "classify_by_rules"
                if route["route_kind"] == "deterministic"
                else "provider_needed_fallback"
            )
            source = "kora_task_graph"
            graph_id = route.get("kora_graph_id")
            event_count = int(route.get("kora_event_count", 0))
            if route["route_kind"] == "deterministic":
                cache[cache_key] = {"route": route}

        results.append(
            {
                "id": request_id,
                "input": text,
                "semantic_cache_key": item.get("semantic_cache_key"),
                "cache_key": cache_key,
                "route_kind": route["route_kind"],
                "selected_route": route["selected_route"],
                "handler": handler,
                "classification_output": route.get("classification_output"),
                "provider_needed_reason": route.get("provider_needed_reason"),
                "provider_calls": int(route.get("provider_calls", 0)),
                "source": source,
                "kora_graph_id": graph_id,
                "kora_event_count": event_count,
                "expected_route_kind": item["expected_route_kind"],
                "expected_handler": item["expected_handler"],
            }
        )

    total_requests = len(results)
    first_time_deterministic_handled = sum(
        1 for item in results if item["route_kind"] == "deterministic"
    )
    cache_hits = sum(1 for item in results if item["route_kind"] == "cache_hit")
    provider_needed = sum(1 for item in results if item["route_kind"] == "provider_required")
    provider_calls = sum(int(item["provider_calls"]) for item in results)
    expected_match_count = sum(
        1
        for item in results
        if item["route_kind"] == item["expected_route_kind"]
        and item["handler"] == item["expected_handler"]
    )
    counters = {
        "total_requests": total_requests,
        "first_time_deterministic_handled": first_time_deterministic_handled,
        "cache_hits": cache_hits,
        "provider_needed": provider_needed,
        "avoided_provider_invocations": first_time_deterministic_handled + cache_hits,
        "provider_calls_actually_made": provider_calls,
    }
    expected_counters = json.loads(EXPECTED_COUNTERS_PATH.read_text(encoding="utf-8"))
    summary: dict[str, Any] = {
        "ok": counters == expected_counters and expected_match_count == total_requests,
        "mode": "cache_reuse_example",
        **counters,
        "expected_match_count": expected_match_count,
        "request_set_id": config["request_set_id"],
        "results": results,
        "example_request": results[0],
        "safe_example_claim": (
            "In this offline cache-reuse example, KORA routes repeated sample requests "
            "to cache hits without making provider calls and marks ambiguous/open-ended "
            "requests as provider-needed."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def render_report(summary: dict[str, Any]) -> str:
    example = summary["example_request"]
    lines = [
        "KORA Cache Reuse Example",
        "",
        f"Total requests: {summary['total_requests']}",
        f"First-time deterministic handled: {summary['first_time_deterministic_handled']}",
        f"Cache hits: {summary['cache_hits']}",
        f"Provider-needed: {summary['provider_needed']}",
        f"Avoided simulated provider/model invocations: {summary['avoided_provider_invocations']}",
        f"Provider calls actually made: {summary['provider_calls_actually_made']}",
        "",
        "Example request:",
        f"- Input: \"{example['input']}\"",
        f"- Route: {example['route_kind']}",
        f"- Handler: {example['handler']}",
        f"- Provider calls: {example['provider_calls']}",
        "",
        "Comparison surface:",
    ]
    for item in summary["results"]:
        lines.append(
            "- {id}: route={route}, handler={handler}, provider_calls={calls}, source={source}".format(
                id=item["id"],
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
    parser.add_argument("--requests", default=str(REQUESTS_PATH), help="offline cache request fixture JSON")
    parser.add_argument("--json-out", help="optional path for structured JSON output")
    parser.add_argument("--report-md", help="optional path for rendered report output")
    args = parser.parse_args()

    summary = build_cache_reuse_summary(
        requests_path=Path(args.requests),
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
