"""Run the bounded Specul.AI editorial workload through explicit KORA policies."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
from dataclasses import replace
from pathlib import Path
from typing import Any

from kora.adapters.openai_adapter import OpenAIAdapter, openai_api_key_configured
from kora.adapters.openai_compatible_local import OpenAICompatibleLocalAdapter
from kora.solution.contracts import canonical_json_bytes
from kora.solution.economics import (
    EconomicsNode,
    ExecutionPolicy,
    WorkloadEconomicsRunner,
)

MAX_SOURCES = 8
MAX_WORKLOAD_BYTES = 64 * 1024


def _object_schema(properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


STRING_ARRAY = {"type": "array", "items": {"type": "string"}}
SOURCE_IDS = {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1}

NODES = (
    EconomicsNode(
        "research",
        "Extract one to three concise evidence items per supplied source. Preserve source-defined terms, definitions, decision boundaries, workflow steps, approval scope, and measurement cadence when materially present. Prefer distinct evidence facets rather than repeating one summary. Preserve source IDs exactly. Each point must be at most 45 words and each limitation at most 25 words. Do not invent facts or source IDs, and do not expand an abbreviation unless a supplied source explicitly defines it.",
        "frontier",
        max_tokens=1800,
        output_schema=_object_schema(
            {
                "evidence": {
                    "type": "array",
                    "items": _object_schema(
                        {
                            "source_id": {"type": "string", "minLength": 1},
                            "point": {"type": "string", "minLength": 1, "maxLength": 420},
                            "limitation": {"type": "string", "maxLength": 240},
                        },
                        ["source_id", "point", "limitation"],
                    ),
                    "minItems": 1,
                    "maxItems": 24,
                },
                "source_ids": SOURCE_IDS,
            },
            ["evidence", "source_ids"],
        ),
    ),
    EconomicsNode(
        "synthesis",
        "Using only the brief and research evidence, synthesize a bounded thesis and outline. Preserve source-defined domain terms and their meanings, explicit decision/approval boundaries, workflow sequences, and measurement cadence when present; do not flatten them into generic categories. Preserve undefined source terminology exactly and never infer acronym expansions. Copy source IDs exactly from research evidence.",
        "frontier",
        ("research",),
        max_tokens=3500,
        output_schema=_object_schema(
            {
                "thesis": {"type": "string", "minLength": 1},
                "outline": {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 2},
                "source_ids": SOURCE_IDS,
            },
            ["thesis", "outline", "source_ids"],
        ),
    ),
    EconomicsNode(
        "draft",
        "Write the canonical long-form article as the strongest complete reasoning artifact for this brief. Ground it only in supplied research and synthesis. Preserve source-defined domain terms and their meanings, material operational details, decision/approval boundaries, and measurement cadence represented in the evidence. Preserve source provenance, preserve undefined source terminology exactly, never infer acronym expansions, and do not invent facts. Honor quality_contract while preserving depth without expanding into an exhaustive report.",
        "frontier",
        ("research", "synthesis"),
        max_tokens=5000,
        output_schema=_object_schema(
            {
                "title": {"type": "string", "minLength": 8},
                "article": {"type": "string", "minLength": 500},
                "claim_source_ids": SOURCE_IDS,
            },
            ["title", "article", "claim_source_ids"],
        ),
    ),
    EconomicsNode(
        "claim_review",
        "Check the draft against research evidence. Treat inferred expansions of undefined source acronyms as unsupported. Return at most 8 concise grounded claims and at most 8 concise unsupported claims; each item must be at most 35 words. Preserve source IDs exactly and do not rewrite the article.",
        "routine",
        ("research", "draft"),
        max_tokens=2500,
        output_schema=_object_schema(
            {
                "grounded_claims": {"type": "array", "items": {"type": "string", "maxLength": 320}, "maxItems": 8},
                "unsupported_claims": {"type": "array", "items": {"type": "string", "maxLength": 320}, "maxItems": 8},
                "source_ids": SOURCE_IDS,
            },
            ["grounded_claims", "unsupported_claims", "source_ids"],
        ),
    ),
    EconomicsNode(
        "editorial_review",
        "Review the draft for reader value, structure, clarity, overclaiming, and unsupported terminology expansion. Return at most 6 concise actionable findings; each finding must be at most 35 words. Do not rewrite the article.",
        "frontier",
        ("draft",),
        max_tokens=2500,
        output_schema=_object_schema(
            {
                "verdict": {"type": "string", "minLength": 1},
                "findings": {"type": "array", "items": {"type": "string", "maxLength": 320}, "maxItems": 6},
            },
            ["verdict", "findings"],
        ),
    ),
    EconomicsNode(
        "revision",
        "Revise the draft into a canonical long-form final article while preserving evidence boundaries. Resolve the reviews without collapsing the argument into a summary. Preserve undefined source terminology exactly, never infer acronym expansions, copy claim source IDs from the draft, and do not invent facts.",
        "frontier",
        ("draft", "claim_review", "editorial_review"),
        max_tokens=5000,
        output_schema=_object_schema(
            {
                "title": {"type": "string", "minLength": 8},
                "article": {"type": "string", "minLength": 500},
                "claim_source_ids": SOURCE_IDS,
                "resolved_findings": STRING_ARRAY,
            },
            ["title", "article", "claim_source_ids", "resolved_findings"],
        ),
    ),
    EconomicsNode(
        "quality_repair",
        "Produce the final canonical long-form article from the revised article. quality_contract is mandatory: the returned article MUST stay within both min/max article character and word ranges, should aim near the supplied targets, and MUST finish with a complete concluding sentence. Preserve undefined source terminology exactly and never infer acronym expansions. IMPORTANT: when the revision exceeds a maximum, deliberately compress it to roughly 90 percent of that maximum rather than landing on the boundary. Remove repetition and secondary implementation detail first. If too short, clarify only already-grounded material. Do not add facts. Preserve claim source IDs.",
        "frontier",
        ("revision", "research", "claim_review", "editorial_review"),
        max_tokens=5000,
        output_schema=_object_schema(
            {
                "title": {"type": "string", "minLength": 8},
                "article": {"type": "string", "minLength": 500},
                "claim_source_ids": SOURCE_IDS,
                "resolved_findings": STRING_ARRAY,
            },
            ["title", "article", "claim_source_ids", "resolved_findings"],
        ),
    ),
)

def nodes_for(workload: dict[str, Any]) -> tuple[EconomicsNode, ...]:
    """Bind provenance fields to source IDs declared by this workload."""
    allowed = sorted(source["id"] for source in workload["sources"])
    bound: list[EconomicsNode] = []
    for node in NODES:
        schema = copy.deepcopy(node.output_schema)
        if not isinstance(schema, dict):
            bound.append(node)
            continue
        properties = schema.get("properties")
        if not isinstance(properties, dict):
            bound.append(node)
            continue
        if node.id == "research":
            evidence = properties["evidence"]["items"]["properties"]
            evidence["source_id"]["enum"] = allowed
            properties["source_ids"]["items"]["enum"] = allowed
        elif node.id == "synthesis":
            properties["source_ids"]["items"]["enum"] = allowed
        elif node.id in {"draft", "revision", "quality_repair"}:
            properties["claim_source_ids"]["items"]["enum"] = allowed
        elif node.id == "claim_review":
            properties["source_ids"]["items"]["enum"] = allowed
        bound.append(replace(node, output_schema=schema))
    return tuple(bound)


POLICIES = {
    "frontier-baseline": ExecutionPolicy(
        "frontier-baseline",
        {"routine": "frontier", "frontier": "frontier"},
        exact_reuse=False,
        context_mode="full",
    ),
    "kora-auto": ExecutionPolicy(
        "kora-auto",
        {"routine": "frontier", "frontier": "frontier"},
        exact_reuse=True,
        context_mode="brief+deps",
    ),
    "kora-local-first": ExecutionPolicy(
        "kora-local-first",
        {"routine": "local", "frontier": "frontier"},
        exact_reuse=True,
        context_mode="brief+deps",
        fallback_routes={"routine": "frontier"},
    ),
    "kora-quality-auto": ExecutionPolicy(
        "kora-quality-auto",
        {"routine": "frontier", "frontier": "frontier"},
        exact_reuse=True,
        context_mode="brief+deps",
        full_context_nodes=("draft",),
    ),
    "local-control": ExecutionPolicy(
        "local-control",
        {"routine": "local", "frontier": "local"},
        exact_reuse=True,
        context_mode="brief+deps",
    ),
    "local-control-no-reuse": ExecutionPolicy(
        "local-control-no-reuse",
        {"routine": "local", "frontier": "local"},
        exact_reuse=False,
        context_mode="brief+deps",
    ),
}


def load_workload(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if len(raw) > MAX_WORKLOAD_BYTES:
        raise ValueError("workload exceeds the bounded byte limit")
    payload = json.loads(raw)
    if not isinstance(payload, dict) or not isinstance(payload.get("brief"), dict):
        raise TypeError("workload requires an object brief")
    sources = payload.get("sources")
    if not isinstance(sources, list) or not 1 <= len(sources) <= MAX_SOURCES:
        raise ValueError("workload requires one through eight sources")
    ids: list[str] = []
    for source in sources:
        if not isinstance(source, dict):
            raise TypeError("each source must be an object")
        source_id = source.get("id")
        text = source.get("text")
        if not isinstance(source_id, str) or not source_id.strip():
            raise ValueError("each source requires a non-empty id")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("each source requires non-empty text")
        ids.append(source_id)
    if len(set(ids)) != len(ids):
        raise ValueError("source ids must be unique")
    return payload


def adapters_for(policy_name: str) -> dict[str, Any]:
    needs_local = policy_name in {"local-control", "local-control-no-reuse", "kora-local-first"}
    needs_frontier = policy_name in {"frontier-baseline", "kora-auto", "kora-local-first", "kora-quality-auto"}
    local_reuse = policy_name in {"local-control", "kora-local-first"}
    frontier_reuse = policy_name in {"kora-auto", "kora-local-first", "kora-quality-auto"}

    if local_reuse and not os.getenv("KORA_LOCAL_OPENAI_RUNTIME_ID", "").strip():
        raise RuntimeError(
            "KORA_LOCAL_OPENAI_RUNTIME_ID is required when local exact reuse is enabled"
        )
    if needs_frontier and not openai_api_key_configured():
        raise RuntimeError(
            "an OpenAI credential is required: OPENAI_API_KEY or KORA_OPENAI_API_KEY_FILE"
        )
    frontier_model = os.getenv("KORA_OPENAI_MODEL", "").strip() if needs_frontier else ""
    if needs_frontier and not frontier_model:
        raise RuntimeError(
            "KORA_OPENAI_MODEL must explicitly name the frontier model for this comparison"
        )
    if frontier_reuse and not os.getenv("KORA_OPENAI_CACHE_ID", "").strip():
        raise RuntimeError(
            "KORA_OPENAI_CACHE_ID is required when frontier exact reuse is enabled"
        )

    adapters: dict[str, Any] = {}
    if needs_local:
        adapters["local"] = OpenAICompatibleLocalAdapter()
    if needs_frontier:
        adapters["frontier"] = OpenAIAdapter(model=frontier_model)
    return adapters


def evaluate_quality(result: dict[str, Any], workload: dict[str, Any]) -> dict[str, Any]:
    """Apply bounded deterministic final-output checks declared by the workload."""
    output = result.get("output")
    output = output if isinstance(output, dict) else {}
    brief = workload.get("brief")
    brief = brief if isinstance(brief, dict) else {}
    floor = brief.get("quality_floor")
    floor = floor if isinstance(floor, dict) else {}
    article = output.get("article")
    article = article if isinstance(article, str) else ""
    article_chars = len(article)
    article_words = len(re.findall(r"\b\w+[\w'-]*\b", article))
    min_chars = floor.get("min_article_chars", 0)
    max_chars = floor.get("max_article_chars", 0)
    min_words = floor.get("min_article_words", 0)
    max_words = floor.get("max_article_words", 0)
    target_chars = floor.get("target_article_chars", 0)
    target_words = floor.get("target_article_words", 0)
    for name, value in (
        ("min_article_chars", min_chars),
        ("max_article_chars", max_chars),
        ("min_article_words", min_words),
        ("max_article_words", max_words),
        ("target_article_chars", target_chars),
        ("target_article_words", target_words),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"brief.quality_floor.{name} must be a non-negative integer")
    if max_chars and max_chars < min_chars:
        raise ValueError("brief.quality_floor.max_article_chars must be at least min_article_chars")
    if max_words and max_words < min_words:
        raise ValueError("brief.quality_floor.max_article_words must be at least min_article_words")
    required_ids = floor.get("required_source_ids", [])
    if not isinstance(required_ids, list) or any(not isinstance(x, str) or not x for x in required_ids):
        raise ValueError("brief.quality_floor.required_source_ids must be a string array")
    actual_ids = output.get("claim_source_ids")
    actual_ids = actual_ids if isinstance(actual_ids, list) else []
    ending_body = re.sub(r"(?:\s*\[S[^\]]+\])+$", "", article.rstrip()).rstrip()
    complete_ending = bool(ending_body) and ending_body[-1] in '.!?…”’"'
    checks = {
        "article_min_chars": article_chars >= min_chars,
        "article_max_chars": max_chars == 0 or article_chars <= max_chars,
        "article_min_words": article_words >= min_words,
        "article_max_words": max_words == 0 or article_words <= max_words,
        "complete_ending": complete_ending,
        "required_source_ids": set(required_ids) <= set(actual_ids),
        "resolved_findings_present": isinstance(output.get("resolved_findings"), list),
    }
    return {
        "pass": all(checks.values()),
        "checks": checks,
        "article_chars": article_chars,
        "article_words": article_words,
        "min_article_chars": min_chars,
        "max_article_chars": max_chars,
        "min_article_words": min_words,
        "max_article_words": max_words,
        "target_article_chars": target_chars,
        "target_article_words": target_words,
    }


def public_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": result["schema_version"],
        "policy": result["policy"],
        "workload_digest": result["workload_digest"],
        "output_digest": hashlib.sha256(canonical_json_bytes(result["output"])).hexdigest(),
        "model_calls": result["model_calls"],
        "tokens_in": result["tokens_in"],
        "tokens_out": result["tokens_out"],
        "exact_reuse_hits": result["exact_reuse_hits"],
        "escalations": result.get("escalations", 0),
        "total_time_ms": result["total_time_ms"],
        "quality_pass": bool((result.get("quality") or {}).get("pass", False)),
        "article_chars": int((result.get("quality") or {}).get("article_chars", 0)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--policy", choices=sorted(POLICIES), required=True)
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    workload = load_workload(args.workload)
    policy = POLICIES[args.policy]
    runner = WorkloadEconomicsRunner(
        nodes=nodes_for(workload),
        adapters=adapters_for(args.policy),
        cache_directory=args.cache_dir if policy.exact_reuse else None,
    )
    result = runner.run(workload=workload, policy=policy)
    result["quality"] = evaluate_quality(result, workload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_json_bytes(result))
    print(json.dumps(public_summary(result), indent=2))
    return 0 if result["quality"]["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
