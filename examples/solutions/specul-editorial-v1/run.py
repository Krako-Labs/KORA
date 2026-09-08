"""Run the bounded Specul.AI editorial workload through explicit KORA policies."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
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
        "Extract exactly one concise evidence item per supplied source. Preserve source IDs exactly. Each point must be at most 45 words and each limitation at most 25 words. Do not invent facts or source IDs.",
        "routine",
        max_tokens=420,
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
                    "maxItems": 8,
                },
                "source_ids": SOURCE_IDS,
            },
            ["evidence", "source_ids"],
        ),
    ),
    EconomicsNode(
        "synthesis",
        "Using only the brief and research evidence, synthesize a bounded thesis and outline. Copy source IDs exactly from research evidence.",
        "frontier",
        ("research",),
        max_tokens=500,
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
        "Write a reader-facing English canonical draft grounded only in the supplied research and synthesis. Preserve source provenance; do not invent facts.",
        "frontier",
        ("research", "synthesis"),
        max_tokens=1600,
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
        "Check the draft against research evidence. Separate grounded from unsupported claims and preserve source IDs exactly.",
        "routine",
        ("research", "draft"),
        max_tokens=700,
        output_schema=_object_schema(
            {
                "grounded_claims": STRING_ARRAY,
                "unsupported_claims": STRING_ARRAY,
                "source_ids": SOURCE_IDS,
            },
            ["grounded_claims", "unsupported_claims", "source_ids"],
        ),
    ),
    EconomicsNode(
        "editorial_review",
        "Review the draft for reader value, structure, clarity, and overclaiming. Return concise actionable findings.",
        "routine",
        ("draft",),
        max_tokens=600,
        output_schema=_object_schema(
            {
                "verdict": {"type": "string", "minLength": 1},
                "findings": STRING_ARRAY,
            },
            ["verdict", "findings"],
        ),
    ),
    EconomicsNode(
        "revision",
        "Revise the draft using claim and editorial review while preserving evidence boundaries. Copy claim source IDs from the draft; do not invent facts.",
        "frontier",
        ("draft", "claim_review", "editorial_review"),
        max_tokens=1800,
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
    """Bind every provenance field to source IDs declared by this workload."""
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
        elif node.id in {"draft", "revision"}:
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
    "kora-local-first": ExecutionPolicy(
        "kora-local-first",
        {"routine": "local", "frontier": "frontier"},
        exact_reuse=True,
        context_mode="brief+deps",
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
    needs_frontier = policy_name in {"frontier-baseline", "kora-local-first"}
    local_reuse = policy_name in {"local-control", "kora-local-first"}
    frontier_reuse = policy_name == "kora-local-first"

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
        "total_time_ms": result["total_time_ms"],
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
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_json_bytes(result))
    print(json.dumps(public_summary(result), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
