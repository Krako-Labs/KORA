"""Offline RAG routing example using KORA task execution."""

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
CORPUS_PATH = EXAMPLE_DIR / "corpus.json"
QUERIES_PATH = EXAMPLE_DIR / "queries.json"
EXPECTED_COUNTERS_PATH = EXAMPLE_DIR / "expected_counters.json"
CLAIM_BOUNDARY = (
    "In this offline RAG-routing example, KORA routes sample queries across "
    "deterministic, cache, retrieval-needed, and provider-needed paths without "
    "making provider calls. It does not claim production RAG readiness, retrieval "
    "accuracy, automatic cost reduction, real API-cost proof, or benchmark superiority."
)


def load_corpus(path: Path = CORPUS_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_queries(path: Path = QUERIES_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _query_cache_key(query: str) -> str:
    normalized = " ".join(query.lower().strip().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _rag_graph(config: dict[str, Any], corpus: dict[str, Any], query_id: str, query: str) -> TaskGraph:
    return TaskGraph.model_validate(
        {
            "graph_id": f"rag-routing-{query_id}",
            "version": "0.1",
            "root": "route_query",
            "defaults": {"budget": {"max_time_ms": 1500, "max_tokens": 300, "max_retries": 0}},
            "tasks": [
                {
                    "id": "route_query",
                    "type": "det.rag.route_query",
                    "deps": [],
                    "in": {"query": query},
                    "run": {
                        "kind": "det",
                        "spec": {
                            "handler": "rag_route_query",
                            "args": {
                                "exact_answers": config["exact_answers"],
                                "retrieval_rules": config["retrieval_rules"],
                                "provider_needed_rules": config["provider_needed_rules"],
                                "corpus": corpus["documents"],
                            },
                        },
                    },
                    "policy": {"on_fail": "fail"},
                    "tags": ["rag-routing", "offline-example"],
                }
            ],
        }
    )


def _run_kora_rag_route(config: dict[str, Any], corpus: dict[str, Any], query_id: str, query: str) -> dict[str, Any]:
    graph = normalize_graph(_rag_graph(config, corpus, query_id, query))
    validate_graph(graph)
    result = run_graph(graph)
    if not result.get("ok"):
        raise RuntimeError(str(result.get("error")))
    final = result.get("final")
    if not isinstance(final, dict):
        raise RuntimeError("RAG routing graph did not return an object")
    routed = dict(final)
    routed.update(
        {
            "kora_graph_id": result["graph_id"],
            "kora_event_count": len(result.get("events", [])),
        }
    )
    return routed


def build_rag_summary(
    *,
    corpus_path: Path = CORPUS_PATH,
    queries_path: Path = QUERIES_PATH,
    json_out: Path | None = None,
) -> dict[str, Any]:
    corpus = load_corpus(corpus_path)
    config = load_queries(queries_path)
    cache: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []

    for item in config["queries"]:
        query_id = str(item["id"])
        query = str(item["query"])
        cache_key = _query_cache_key(query)

        if cache_key in cache:
            cached = cache[cache_key]
            route = dict(cached["route"])
            route.update(
                {
                    "route_kind": "cache_hit",
                    "selected_route": "rag.cache.reuse",
                    "handler": "cache_reuse",
                    "provider_needed_reason": None,
                }
            )
            source = "cache"
            graph_id = cached["route"].get("kora_graph_id")
            event_count = 0
        else:
            route = _run_kora_rag_route(config, corpus, query_id, query)
            source = "kora_task_graph"
            graph_id = route.get("kora_graph_id")
            event_count = int(route.get("kora_event_count", 0))
            if route["route_kind"] in {"deterministic_answer", "retrieval_needed"}:
                cache[cache_key] = {"route": route}

        results.append(
            {
                "id": query_id,
                "query": query,
                "route_kind": route["route_kind"],
                "selected_route": route["selected_route"],
                "handler": route["handler"],
                "answer": route.get("answer"),
                "retrieved_documents": route.get("retrieved_documents", []),
                "provider_needed_reason": route.get("provider_needed_reason"),
                "provider_calls": int(route.get("provider_calls", 0)),
                "cache_key": cache_key,
                "source": source,
                "kora_graph_id": graph_id,
                "kora_event_count": event_count,
                "expected_route_kind": item["expected_route_kind"],
                "expected_handler": item["expected_handler"],
            }
        )

    total_queries = len(results)
    deterministic_answered = sum(1 for item in results if item["route_kind"] == "deterministic_answer")
    cache_hits = sum(1 for item in results if item["route_kind"] == "cache_hit")
    retrieval_needed = sum(1 for item in results if item["route_kind"] == "retrieval_needed")
    provider_needed = sum(1 for item in results if item["route_kind"] == "provider_needed")
    provider_calls = sum(int(item["provider_calls"]) for item in results)
    expected_match_count = sum(
        1
        for item in results
        if item["route_kind"] == item["expected_route_kind"]
        and item["handler"] == item["expected_handler"]
    )
    counters = {
        "total_queries": total_queries,
        "deterministic_answered": deterministic_answered,
        "cache_hits": cache_hits,
        "retrieval_needed": retrieval_needed,
        "provider_needed": provider_needed,
        "avoided_provider_invocations": deterministic_answered + cache_hits,
        "provider_calls_actually_made": provider_calls,
    }
    expected_counters = json.loads(EXPECTED_COUNTERS_PATH.read_text(encoding="utf-8"))
    summary: dict[str, Any] = {
        "ok": counters == expected_counters and expected_match_count == total_queries,
        "mode": "rag_routing_example",
        **counters,
        "expected_match_count": expected_match_count,
        "corpus_id": corpus["corpus_id"],
        "query_set_id": config["query_set_id"],
        "results": results,
        "example_query": results[0],
        "safe_example_claim": (
            "In this offline RAG-routing example, KORA routes sample queries across "
            "deterministic, cache, retrieval-needed, and provider-needed paths without "
            "making provider calls."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def render_report(summary: dict[str, Any]) -> str:
    example = summary["example_query"]
    lines = [
        "KORA RAG Routing Example",
        "",
        f"Total queries: {summary['total_queries']}",
        f"Deterministic answered: {summary['deterministic_answered']}",
        f"Cache hits: {summary['cache_hits']}",
        f"Retrieval-needed: {summary['retrieval_needed']}",
        f"Provider-needed: {summary['provider_needed']}",
        f"Avoided simulated provider/model invocations: {summary['avoided_provider_invocations']}",
        f"Provider calls actually made: {summary['provider_calls_actually_made']}",
        "",
        "Example query:",
        f"- Input: \"{example['query']}\"",
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
    parser.add_argument("--corpus", default=str(CORPUS_PATH), help="offline document corpus JSON")
    parser.add_argument("--queries", default=str(QUERIES_PATH), help="RAG query fixture JSON")
    parser.add_argument("--json-out", help="optional path for structured JSON output")
    parser.add_argument("--report-md", help="optional path for rendered report output")
    args = parser.parse_args()

    summary = build_rag_summary(
        corpus_path=Path(args.corpus),
        queries_path=Path(args.queries),
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
