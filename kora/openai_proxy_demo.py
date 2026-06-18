"""Reusable offline OpenAI-style proxy demo routing utilities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from kora.executor import run_graph
from kora.task_ir import TaskGraph, normalize_graph, validate_graph

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REQUESTS_PATH = REPO_ROOT / "examples" / "openai_compatible_proxy" / "requests.json"
DEFAULT_EXPECTED_COUNTERS_PATH = (
    REPO_ROOT / "examples" / "openai_compatible_proxy" / "expected_counters.json"
)
CLAIM_BOUNDARY = (
    "In this offline proxy demo, KORA routes deterministic or cacheable "
    "OpenAI-style sample requests without making provider calls and marks "
    "ambiguous/open-ended requests as provider-needed. It does not claim "
    "production proxy readiness, full OpenAI API compatibility, automatic cost "
    "reduction, real API-cost proof, benchmark superiority, or broad workload superiority."
)
SAFE_EXAMPLE_CLAIM = (
    "In this offline proxy demo, KORA routes deterministic or cacheable "
    "OpenAI-style sample requests without making provider calls and marks "
    "ambiguous/open-ended requests as provider-needed."
)


def load_requests(path: Path = DEFAULT_REQUESTS_PATH) -> dict[str, Any]:
    """Load an OpenAI-style request fixture."""
    return json.loads(path.read_text(encoding="utf-8"))


def message_text(request: dict[str, Any]) -> str:
    """Extract text from OpenAI-style chat message content."""
    messages = request.get("messages", [])
    if not isinstance(messages, list):
        return ""
    parts: list[str] = []
    for message in messages:
        if not isinstance(message, dict):
            continue
        content = message.get("content", "")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    parts.append(str(item["text"]))
    return " ".join(parts)


def request_cache_key(request: dict[str, Any]) -> str:
    """Return a stable cache key for an OpenAI-style request object."""
    canonical = json.dumps(request, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def classification_graph(config: dict[str, Any], request_id: str, text: str) -> TaskGraph:
    """Build the KORA TaskGraph used by the offline proxy demo."""
    return TaskGraph.model_validate(
        {
            "graph_id": f"openai-compatible-proxy-{request_id}",
            "version": "0.1",
            "root": "classify",
            "defaults": {"budget": {"max_time_ms": 1500, "max_tokens": 300, "max_retries": 0}},
            "tasks": [
                {
                    "id": "classify",
                    "type": "det.proxy.openai_compatible_classification",
                    "deps": [],
                    "in": {"text": text},
                    "run": {
                        "kind": "det",
                        "spec": {
                            "handler": "classify_by_rules",
                            "args": {
                                "scenario_id": "openai_compatible_proxy",
                                "routes": config["routes"],
                                "provider_required_route": config["provider_required_route"],
                            },
                        },
                    },
                    "policy": {"on_fail": "fail"},
                    "tags": ["openai-compatible-proxy", "offline-demo"],
                }
            ],
        }
    )


def run_kora_route(config: dict[str, Any], request_id: str, request: dict[str, Any]) -> dict[str, Any]:
    """Route one OpenAI-style request through KORA TaskGraph execution."""
    text = message_text(request)
    graph = normalize_graph(classification_graph(config, request_id, text))
    validate_graph(graph)
    result = run_graph(graph)
    if not result.get("ok"):
        raise RuntimeError(str(result.get("error")))
    final = result.get("final")
    if not isinstance(final, dict):
        raise RuntimeError("proxy graph did not return an object")
    routed = dict(final)
    routed.update(
        {
            "kora_graph_id": result["graph_id"],
            "kora_event_count": len(result.get("events", [])),
        }
    )
    return routed


def openai_style_response(request_id: str, route: dict[str, Any], source: str) -> dict[str, Any]:
    """Build a small OpenAI-style response envelope for demo output."""
    return {
        "id": f"chatcmpl-kora-{request_id}",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": json.dumps(
                        {
                            "source": source,
                            "route_kind": route["route_kind"],
                            "selected_route": route["selected_route"],
                            "classification_output": route.get("classification_output"),
                            "provider_needed_reason": route.get("provider_needed_reason"),
                        },
                        sort_keys=True,
                    ),
                },
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "provider_calls": 0,
    }


def build_proxy_summary(
    *,
    requests_path: Path = DEFAULT_REQUESTS_PATH,
    expected_counters_path: Path | None = DEFAULT_EXPECTED_COUNTERS_PATH,
    json_out: Path | None = None,
    mode: str = "openai_proxy_demo",
) -> dict[str, Any]:
    """Run the offline proxy demo and return structured evidence."""
    config = load_requests(requests_path)
    cache: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []

    for item in config["requests"]:
        request_id = str(item["id"])
        request = item["request"]
        cache_key = request_cache_key(request)

        if cache_key in cache:
            cached = cache[cache_key]
            route = dict(cached["route"])
            route.update(
                {
                    "route_kind": "cache_hit",
                    "selected_route": "proxy.cache.reuse",
                    "provider_needed_reason": None,
                }
            )
            handler = "cache_reuse"
            source = "cache"
            graph_id = cached["route"].get("kora_graph_id")
            event_count = 0
        else:
            route = run_kora_route(config, request_id, request)
            handler = (
                "classify_by_rules"
                if route["route_kind"] == "deterministic"
                else "provider_needed_fallback"
            )
            source = "kora_task_graph"
            graph_id = route.get("kora_graph_id")
            event_count = route.get("kora_event_count", 0)
            if route["route_kind"] == "deterministic":
                cache[cache_key] = {"route": route}

        proxy_response = openai_style_response(request_id, route, source)
        results.append(
            {
                "id": request_id,
                "openai_style_request": request,
                "request_text": message_text(request),
                "route_kind": route["route_kind"],
                "selected_route": route["selected_route"],
                "handler": handler,
                "classification_output": route.get("classification_output"),
                "provider_needed_reason": route.get("provider_needed_reason"),
                "provider_calls": 0,
                "cache_key": cache_key,
                "source": source,
                "kora_graph_id": graph_id,
                "kora_event_count": event_count,
                "openai_style_response": proxy_response,
                "expected_route_kind": item["expected_route_kind"],
                "expected_handler": item["expected_handler"],
            }
        )

    total_requests = len(results)
    deterministic_handled = sum(1 for item in results if item["route_kind"] == "deterministic")
    cache_hits = sum(1 for item in results if item["route_kind"] == "cache_hit")
    provider_needed = sum(1 for item in results if item["route_kind"] == "provider_required")
    provider_calls = sum(int(item["provider_calls"]) for item in results)
    expected_match_count = sum(
        1
        for item in results
        if item["route_kind"] == item["expected_route_kind"]
        and item["handler"] == item["expected_handler"]
    )
    avoided_provider_invocations = deterministic_handled + cache_hits
    counters = {
        "total_requests": total_requests,
        "deterministic_handled": deterministic_handled,
        "cache_hits": cache_hits,
        "provider_needed": provider_needed,
        "avoided_provider_invocations": avoided_provider_invocations,
        "provider_calls_actually_made": provider_calls,
    }
    expected_counters = (
        json.loads(expected_counters_path.read_text(encoding="utf-8"))
        if expected_counters_path is not None and expected_counters_path.exists()
        else counters
    )
    summary: dict[str, Any] = {
        "ok": counters == expected_counters and expected_match_count == total_requests,
        "mode": mode,
        **counters,
        "expected_match_count": expected_match_count,
        "results": results,
        "example_request": results[0],
        "safe_example_claim": SAFE_EXAMPLE_CLAIM,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def render_report(summary: dict[str, Any], *, title: str = "KORA OpenAI Proxy Demo") -> str:
    """Render the proxy summary as a concise CLI/example report."""
    example = summary["example_request"]
    lines = [
        title,
        "",
        f"Total requests: {summary['total_requests']}",
        f"Deterministic handled: {summary['deterministic_handled']}",
        f"Cache hits: {summary['cache_hits']}",
        f"Provider-needed: {summary['provider_needed']}",
        f"Avoided simulated provider/model invocations: {summary['avoided_provider_invocations']}",
        f"Provider calls actually made: {summary['provider_calls_actually_made']}",
        "",
        "Example request:",
        f"- OpenAI-style chat request: \"{example['request_text'].split(':', 1)[-1].strip()}\"",
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


def write_report(report: str, report_md: Path | None) -> None:
    """Write a rendered report when an output path is provided."""
    if report_md is None:
        return
    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_md.write_text(report, encoding="utf-8")
