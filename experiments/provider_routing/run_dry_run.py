from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


EXPECTED_PROVIDER_KINDS = {
    "deterministic",
    "cache",
    "local_small_model",
    "local_h100_model",
    "aws_model",
    "azure_model",
    "openai_api",
    "claude_api",
    "gemini_api",
}

ALLOWED_PROVIDER_STATUSES = {"ready_dry_run", "planned_blocked"}
DEFAULT_CONFIG_PATH = Path(__file__).with_name("config.example.yaml")


class ProviderRoutingConfigError(ValueError):
    """Raised when the dry-run provider routing config is unsafe or malformed."""


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    """Load the JSON-compatible YAML example without adding a YAML dependency."""
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProviderRoutingConfigError(
            "config.example.yaml must remain JSON-compatible YAML for dependency-free dry runs"
        ) from exc

    if not isinstance(config, dict):
        raise ProviderRoutingConfigError("provider routing config must be an object")
    return config


def validate_provider_config(config: dict[str, Any]) -> dict[str, Any]:
    if config.get("dry_run_only") is not True:
        raise ProviderRoutingConfigError("dry_run_only must be true")
    if config.get("synthetic_results_only") is not True:
        raise ProviderRoutingConfigError("synthetic_results_only must be true")
    if config.get("real_provider_calls_enabled") is not False:
        raise ProviderRoutingConfigError("real_provider_calls_enabled must be false")

    providers = config.get("providers")
    if not isinstance(providers, list):
        raise ProviderRoutingConfigError("providers must be a list")

    seen_ids: set[str] = set()
    seen_kinds: set[str] = set()
    for index, provider in enumerate(providers):
        if not isinstance(provider, dict):
            raise ProviderRoutingConfigError(f"provider at index {index} must be an object")

        provider_id = provider.get("id")
        kind = provider.get("kind")
        status = provider.get("status")
        if not isinstance(provider_id, str) or not provider_id:
            raise ProviderRoutingConfigError(f"provider at index {index} must have a non-empty id")
        if provider_id in seen_ids:
            raise ProviderRoutingConfigError(f"duplicate provider id: {provider_id}")
        if kind not in EXPECTED_PROVIDER_KINDS:
            raise ProviderRoutingConfigError(f"unsupported provider kind for {provider_id}: {kind}")
        if status not in ALLOWED_PROVIDER_STATUSES:
            raise ProviderRoutingConfigError(f"unsupported status for {provider_id}: {status}")
        if provider.get("endpoint") is not None:
            raise ProviderRoutingConfigError(f"{provider_id} must not define an active endpoint")
        if provider.get("credential_ref") != "PLACEHOLDER_ONLY":
            raise ProviderRoutingConfigError(f"{provider_id} credential_ref must be PLACEHOLDER_ONLY")

        seen_ids.add(provider_id)
        seen_kinds.add(kind)

    missing = sorted(EXPECTED_PROVIDER_KINDS - seen_kinds)
    if missing:
        raise ProviderRoutingConfigError(f"missing provider kinds: {', '.join(missing)}")

    tasks = config.get("synthetic_tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ProviderRoutingConfigError("synthetic_tasks must be a non-empty list")
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise ProviderRoutingConfigError(f"synthetic task at index {index} must be an object")
        task_id = task.get("id")
        route_hint = task.get("route_hint")
        if not isinstance(task_id, str) or not task_id:
            raise ProviderRoutingConfigError(f"synthetic task at index {index} must have a non-empty id")
        if route_hint not in EXPECTED_PROVIDER_KINDS:
            raise ProviderRoutingConfigError(f"synthetic task {task_id} has unsupported route_hint: {route_hint}")

    return {
        "provider_count": len(providers),
        "provider_kinds": sorted(seen_kinds),
        "synthetic_task_count": len(tasks),
    }


def simulate_routing(config: dict[str, Any]) -> dict[str, Any]:
    validation = validate_provider_config(config)
    providers_by_kind = {provider["kind"]: provider for provider in config["providers"]}

    routed_tasks = []
    provider_counts: Counter[str] = Counter()
    blocked_real_execution_count = 0
    for task in config["synthetic_tasks"]:
        route_hint = task["route_hint"]
        provider = providers_by_kind[route_hint]
        dry_run_status = "synthetic_route_ready"
        if provider["status"] == "planned_blocked":
            dry_run_status = "synthetic_route_blocked_for_real_execution"
            blocked_real_execution_count += 1

        provider_counts[provider["id"]] += 1
        routed_tasks.append(
            {
                "task_id": task["id"],
                "selected_provider": provider["id"],
                "provider_kind": provider["kind"],
                "provider_status": provider["status"],
                "dry_run_status": dry_run_status,
                "real_call_attempted": False,
            }
        )

    return {
        "name": config.get("name", "ai_champion_provider_routing_dry_run"),
        "status": "ok",
        "mode": "dry-run",
        "dry_run_only": True,
        "synthetic_results_only": True,
        "real_provider_calls_enabled": False,
        "real_network_calls_attempted": False,
        "real_gpu_calls_attempted": False,
        "validation": validation,
        "summary": {
            "synthetic_tasks": len(routed_tasks),
            "providers_used": dict(sorted(provider_counts.items())),
            "blocked_real_execution_routes": blocked_real_execution_count,
        },
        "routed_tasks": routed_tasks,
        "claim_boundary": "Synthetic dry-run routing only; no real GPU, API, cost, latency, quality, energy, or production benchmark result.",
    }


def write_summary(summary: dict[str, Any], output_path: Path | None) -> None:
    if output_path is None:
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the AI Champion provider routing dry-run harness.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to JSON-compatible YAML config. Defaults to config.example.yaml.",
    )
    parser.add_argument("--output", type=Path, help="Optional path for the dry-run JSON summary.")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    summary = simulate_routing(config)
    write_summary(summary, args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
