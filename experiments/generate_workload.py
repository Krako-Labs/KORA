from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Callable


DEFAULT_BENCHMARK_NAME = "deterministic_heavy_v1"
DEFAULT_COUNT = 100
DEFAULT_SEED = 42
VERSION = "1.0"

CATEGORIES = [
    "arithmetic",
    "string_normalization",
    "json_validation",
    "routing_decision",
    "cache_lookup",
    "schema_check",
    "date_normalization",
    "unit_conversion",
    "config_validation",
    "policy_rule_match",
]


def _fallback_output(reason: str) -> dict[str, Any]:
    return {
        "fallback_required": True,
        "reason": reason,
    }


def build_arithmetic_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    left = rng.randint(10, 250)
    right = rng.randint(1, 80)
    operation = rng.choice(["add", "subtract", "multiply"])
    result = {
        "add": left + right,
        "subtract": left - right,
        "multiply": left * right,
    }[operation]

    return {
        "id": f"arithmetic_{index:03d}",
        "category": "arithmetic",
        "input": {"left": left, "right": right, "operation": operation},
        "expected_path": "deterministic_arithmetic" if not requires_model else "fallback_candidate",
        "expected_output": result if not requires_model else _fallback_output("ambiguous arithmetic instruction"),
        "requires_model": requires_model,
        "notes": "Exact arithmetic case." if not requires_model else "Fallback candidate for ambiguous arithmetic wording.",
    }


def build_string_normalization_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    words = [" KORA ", "Benchmark", "  deterministic ", "CONTROLLED", " Result  "]
    selected = rng.sample(words, k=3)
    raw = "-".join(selected)
    normalized = " ".join(part.strip().lower() for part in selected)

    return {
        "id": f"string_normalization_{index:03d}",
        "category": "string_normalization",
        "input": {"text": raw, "normalization": "strip_lower_join_spaces"},
        "expected_path": "deterministic_string_normalization" if not requires_model else "fallback_candidate",
        "expected_output": normalized if not requires_model else _fallback_output("requires semantic rewrite beyond normalization"),
        "requires_model": requires_model,
        "notes": "Deterministic string normalization." if not requires_model else "Fallback candidate for semantic rewriting.",
    }


def build_json_validation_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    include_required = rng.choice([True, True, False])
    payload = {"id": f"item-{index}", "enabled": rng.choice([True, False])}
    if include_required:
        payload["kind"] = rng.choice(["alpha", "beta", "gamma"])
    expected = {"valid": include_required, "missing": [] if include_required else ["kind"]}

    return {
        "id": f"json_validation_{index:03d}",
        "category": "json_validation",
        "input": {"payload": payload, "required_fields": ["id", "kind", "enabled"]},
        "expected_path": "deterministic_json_validation" if not requires_model else "fallback_candidate",
        "expected_output": expected if not requires_model else _fallback_output("requires policy decision for invalid payload"),
        "requires_model": requires_model,
        "notes": "Structured JSON validation." if not requires_model else "Fallback candidate for invalid payload handling policy.",
    }


def build_routing_decision_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    priority = rng.choice(["low", "normal", "high"])
    kind = rng.choice(["billing", "support", "security"])
    route = "security_review" if kind == "security" or priority == "high" else f"{kind}_queue"

    return {
        "id": f"routing_decision_{index:03d}",
        "category": "routing_decision",
        "input": {"kind": kind, "priority": priority},
        "expected_path": "deterministic_routing" if not requires_model else "fallback_candidate",
        "expected_output": {"route": route} if not requires_model else _fallback_output("route requires incomplete policy context"),
        "requires_model": requires_model,
        "notes": "Rule-based routing decision." if not requires_model else "Fallback candidate for incomplete routing rules.",
    }


def build_cache_lookup_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    cache = {"alpha": "cached-alpha", "beta": "cached-beta", "gamma": "cached-gamma"}
    key = rng.choice(["alpha", "beta", "gamma", "missing"])
    expected = {"hit": key in cache, "value": cache.get(key)}

    return {
        "id": f"cache_lookup_{index:03d}",
        "category": "cache_lookup",
        "input": {"key": key, "namespace": "deterministic_heavy_v1"},
        "expected_path": "deterministic_cache_lookup" if not requires_model else "fallback_candidate",
        "expected_output": expected if not requires_model else _fallback_output("cache miss requires external answer"),
        "requires_model": requires_model,
        "notes": "Deterministic cache hit/miss lookup." if not requires_model else "Fallback candidate after cache miss.",
    }


def build_schema_check_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    status = rng.choice(["draft", "active", "archived", "invalid"])
    expected = {"valid": status in {"draft", "active", "archived"}, "field": "status"}

    return {
        "id": f"schema_check_{index:03d}",
        "category": "schema_check",
        "input": {"object": {"status": status}, "enum": ["draft", "active", "archived"]},
        "expected_path": "deterministic_schema_check" if not requires_model else "fallback_candidate",
        "expected_output": expected if not requires_model else _fallback_output("schema repair requires human or model judgment"),
        "requires_model": requires_model,
        "notes": "Enum schema check." if not requires_model else "Fallback candidate for schema repair.",
    }


def build_date_normalization_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    year = 2026
    month = rng.randint(1, 12)
    day = rng.randint(1, 28)
    raw = f"{month}/{day}/{year}"
    normalized = f"{year:04d}-{month:02d}-{day:02d}"

    return {
        "id": f"date_normalization_{index:03d}",
        "category": "date_normalization",
        "input": {"date": raw, "input_format": "M/D/YYYY", "output_format": "YYYY-MM-DD"},
        "expected_path": "deterministic_date_normalization" if not requires_model else "fallback_candidate",
        "expected_output": normalized if not requires_model else _fallback_output("date phrase is underspecified"),
        "requires_model": requires_model,
        "notes": "Exact date normalization." if not requires_model else "Fallback candidate for underspecified date phrase.",
    }


def build_unit_conversion_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    meters = rng.randint(1, 500)
    centimeters = meters * 100

    return {
        "id": f"unit_conversion_{index:03d}",
        "category": "unit_conversion",
        "input": {"value": meters, "from": "m", "to": "cm"},
        "expected_path": "deterministic_unit_conversion" if not requires_model else "fallback_candidate",
        "expected_output": {"value": centimeters, "unit": "cm"} if not requires_model else _fallback_output("unit target is ambiguous"),
        "requires_model": requires_model,
        "notes": "Exact metric unit conversion." if not requires_model else "Fallback candidate for ambiguous unit conversion.",
    }


def build_config_validation_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    retries = rng.randint(0, 5)
    timeout_ms = rng.choice([100, 500, 1000, 5000])
    expected = {"valid": 0 <= retries <= 3 and timeout_ms <= 3000}

    return {
        "id": f"config_validation_{index:03d}",
        "category": "config_validation",
        "input": {"config": {"retries": retries, "timeout_ms": timeout_ms}},
        "expected_path": "deterministic_config_validation" if not requires_model else "fallback_candidate",
        "expected_output": expected if not requires_model else _fallback_output("config recommendation requires tradeoff judgment"),
        "requires_model": requires_model,
        "notes": "Deterministic config bounds validation." if not requires_model else "Fallback candidate for config recommendation.",
    }


def build_policy_rule_match_task(index: int, rng: random.Random, requires_model: bool) -> dict[str, Any]:
    region = rng.choice(["us", "eu", "apac"])
    data_class = rng.choice(["public", "internal", "restricted"])
    allowed = not (region == "eu" and data_class == "restricted")

    return {
        "id": f"policy_rule_match_{index:03d}",
        "category": "policy_rule_match",
        "input": {"region": region, "data_class": data_class},
        "expected_path": "deterministic_policy_rule_match" if not requires_model else "fallback_candidate",
        "expected_output": {"allowed": allowed} if not requires_model else _fallback_output("policy text is incomplete"),
        "requires_model": requires_model,
        "notes": "Explicit policy table match." if not requires_model else "Fallback candidate for incomplete policy text.",
    }


BUILDERS: dict[str, Callable[[int, random.Random, bool], dict[str, Any]]] = {
    "arithmetic": build_arithmetic_task,
    "string_normalization": build_string_normalization_task,
    "json_validation": build_json_validation_task,
    "routing_decision": build_routing_decision_task,
    "cache_lookup": build_cache_lookup_task,
    "schema_check": build_schema_check_task,
    "date_normalization": build_date_normalization_task,
    "unit_conversion": build_unit_conversion_task,
    "config_validation": build_config_validation_task,
    "policy_rule_match": build_policy_rule_match_task,
}


def fallback_indices(count: int, rng: random.Random) -> set[int]:
    fallback_count = round(count * 0.2)
    return set(rng.sample(range(count), k=fallback_count))


def generate_workload(count: int = DEFAULT_COUNT, seed: int = DEFAULT_SEED, benchmark_name: str = DEFAULT_BENCHMARK_NAME) -> dict[str, Any]:
    if count < len(CATEGORIES):
        raise ValueError(f"count must be at least {len(CATEGORIES)} to include every category")

    rng = random.Random(seed)
    fallback_set = fallback_indices(count, rng)
    tasks = []

    for index in range(count):
        category = CATEGORIES[index % len(CATEGORIES)]
        task_rng = random.Random(f"{seed}:{index}:{category}")
        task = BUILDERS[category](index + 1, task_rng, index in fallback_set)
        tasks.append(task)

    return {
        "benchmark_name": benchmark_name,
        "name": benchmark_name,
        "version": VERSION,
        "generated_by": "experiments/generate_workload.py",
        "seed": seed,
        "task_count": count,
        "tasks": tasks,
    }


def write_workload(workload: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(workload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate deterministic-heavy KORA benchmark workloads.")
    parser.add_argument("--output", required=True, help="Path for generated workload JSON")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT, help="Number of tasks to generate")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Deterministic generation seed")
    parser.add_argument("--benchmark-name", default=DEFAULT_BENCHMARK_NAME, help="Benchmark name stored in workload metadata")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_path = Path(args.output)
    workload = generate_workload(count=args.count, seed=args.seed, benchmark_name=args.benchmark_name)
    write_workload(workload, output_path)
    print(
        json.dumps(
            {
                "benchmark_name": workload["benchmark_name"],
                "output": str(output_path),
                "seed": workload["seed"],
                "task_count": workload["task_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
