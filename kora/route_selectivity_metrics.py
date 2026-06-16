"""KRK dry-run route-selectivity metrics."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Callable

ROUTES = ("deterministic", "cache", "CPU", "provider", "GPU", "fallback")
FALLBACK_CLASSES = (
    "safety_fallback",
    "failure_fallback",
    "validation_fallback",
    "unknown_fallback",
)
CLAIM_BOUNDARY = (
    "Dry-run route-selectivity evidence only. This output does not claim production "
    "savings, customer savings, infrastructure savings, GPU superiority, broad workload "
    "superiority, provider replacement, production readiness, or formal validation."
)


@dataclass(frozen=True)
class RouteRequest:
    """Router-visible request passed to route policies."""

    request_id: str
    workload_profile: str
    workload_class: str
    router_visible_metadata: dict[str, Any]


@dataclass(frozen=True)
class RouteDecision:
    """Route policy output."""

    selected_route: str
    policy_id: str
    policy_version: str
    decision_reason: str
    fallback_classification: str | None = None


RoutePolicy = Callable[[RouteRequest], RouteDecision]


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _metadata_text(metadata: dict[str, Any], key: str) -> str:
    return str(metadata.get(key, "")).strip()


def _is_restricted(metadata: dict[str, Any]) -> bool:
    privacy = _metadata_text(metadata, "privacy_preference")
    return privacy in {"restricted"}


def _is_malformed(metadata: dict[str, Any]) -> bool:
    return (
        _as_int(metadata.get("batch_size"), default=0) <= 0
        or _metadata_text(metadata, "input_size") == "unknown"
        or _metadata_text(metadata, "request_modality") == "unknown"
    )


def _is_gpu_suitable(metadata: dict[str, Any]) -> bool:
    return (
        _metadata_text(metadata, "estimated_complexity") == "high"
        and _metadata_text(metadata, "input_size") == "large"
        and _as_int(metadata.get("batch_size"), default=1) >= 16
        and _metadata_text(metadata, "privacy_preference") in {"local_or_sanitized"}
    )


def _fallback_classification(metadata: dict[str, Any]) -> str:
    if _is_restricted(metadata) or _is_malformed(metadata):
        return "safety_fallback"
    return "unknown_fallback"


def all_gpu_policy(request: RouteRequest) -> RouteDecision:
    return RouteDecision(
        selected_route="GPU",
        policy_id="all_gpu",
        policy_version="all_gpu_v0",
        decision_reason="Baseline policy routes every item to GPU.",
    )


def static_heuristic_policy(request: RouteRequest) -> RouteDecision:
    metadata = request.router_visible_metadata
    if _is_restricted(metadata) or _is_malformed(metadata):
        return RouteDecision(
            selected_route="fallback",
            policy_id="static_heuristic",
            policy_version="static_heuristic_v0",
            decision_reason="Restricted or malformed visible metadata requires fallback.",
            fallback_classification=_fallback_classification(metadata),
        )
    if bool(metadata.get("cache_key_available")) and _metadata_text(metadata, "privacy_preference") == "local":
        return RouteDecision(
            selected_route="cache",
            policy_id="static_heuristic",
            policy_version="static_heuristic_v0",
            decision_reason="Visible cache key and local preference select cache.",
        )
    if _metadata_text(metadata, "estimated_complexity") == "low" and _metadata_text(metadata, "input_size") == "small":
        return RouteDecision(
            selected_route="deterministic",
            policy_id="static_heuristic",
            policy_version="static_heuristic_v0",
            decision_reason="Small low-complexity request selects deterministic route.",
        )
    if _is_gpu_suitable(metadata):
        return RouteDecision(
            selected_route="GPU",
            policy_id="static_heuristic",
            policy_version="static_heuristic_v0",
            decision_reason="Large high-complexity local-or-sanitized request selects GPU.",
        )
    if _metadata_text(metadata, "privacy_preference") == "provider_allowed":
        return RouteDecision(
            selected_route="provider",
            policy_id="static_heuristic",
            policy_version="static_heuristic_v0",
            decision_reason="Provider-allowed request selects provider.",
        )
    return RouteDecision(
        selected_route="CPU",
        policy_id="static_heuristic",
        policy_version="static_heuristic_v0",
        decision_reason="Default visible-metadata route selects CPU.",
    )


def provider_first_with_gpu_fallback_policy(request: RouteRequest) -> RouteDecision:
    metadata = request.router_visible_metadata
    if _is_restricted(metadata) or _is_malformed(metadata):
        return RouteDecision(
            selected_route="fallback",
            policy_id="provider_first_with_gpu_fallback",
            policy_version="provider_first_with_gpu_fallback_v0",
            decision_reason="Restricted or malformed visible metadata requires fallback.",
            fallback_classification=_fallback_classification(metadata),
        )
    if _metadata_text(metadata, "privacy_preference") == "provider_allowed":
        return RouteDecision(
            selected_route="provider",
            policy_id="provider_first_with_gpu_fallback",
            policy_version="provider_first_with_gpu_fallback_v0",
            decision_reason="Provider-allowed request selects provider first.",
        )
    if _is_gpu_suitable(metadata):
        return RouteDecision(
            selected_route="GPU",
            policy_id="provider_first_with_gpu_fallback",
            policy_version="provider_first_with_gpu_fallback_v0",
            decision_reason="High-complexity local-or-sanitized request falls back to GPU.",
        )
    if bool(metadata.get("cache_key_available")):
        return RouteDecision(
            selected_route="cache",
            policy_id="provider_first_with_gpu_fallback",
            policy_version="provider_first_with_gpu_fallback_v0",
            decision_reason="Visible cache key selects cache when provider is not allowed.",
        )
    return RouteDecision(
        selected_route="CPU",
        policy_id="provider_first_with_gpu_fallback",
        policy_version="provider_first_with_gpu_fallback_v0",
        decision_reason="Default visible-metadata route selects CPU.",
    )


def krk_dry_run_policy(request: RouteRequest) -> RouteDecision:
    decision = static_heuristic_policy(request)
    return RouteDecision(
        selected_route=decision.selected_route,
        policy_id="KRK",
        policy_version="krk_dry_run_v0",
        decision_reason=f"KRK dry-run visible-metadata policy: {decision.decision_reason}",
        fallback_classification=decision.fallback_classification,
    )


POLICIES: dict[str, RoutePolicy] = {
    "all_gpu": all_gpu_policy,
    "static_heuristic": static_heuristic_policy,
    "provider_first_with_gpu_fallback": provider_first_with_gpu_fallback_policy,
    "KRK": krk_dry_run_policy,
}


def route_request_from_item(item: dict[str, Any]) -> RouteRequest:
    """Build router input without exposing oracle labels."""

    metadata = item.get("router_visible_metadata")
    if not isinstance(metadata, dict):
        raise ValueError("item missing router_visible_metadata object")
    return RouteRequest(
        request_id=str(item.get("request_id", "")),
        workload_profile=str(item.get("workload_profile", "")),
        workload_class=str(item.get("workload_class", "")),
        router_visible_metadata=dict(metadata),
    )


def validate_matrix_item(item: dict[str, Any]) -> None:
    for field in ("request_id", "workload_profile", "workload_class"):
        if field not in item:
            raise ValueError(f"matrix item missing {field}")
    if not isinstance(item.get("router_visible_metadata"), dict):
        raise ValueError("matrix item missing router_visible_metadata object")
    oracle = item.get("oracle_labels")
    if not isinstance(oracle, dict):
        raise ValueError("matrix item missing oracle_labels object")
    for field in ("expected_route", "acceptable_routes", "disallowed_routes", "oracle_reason"):
        if field not in oracle:
            raise ValueError(f"oracle_labels missing {field}")
    expected = oracle["expected_route"]
    acceptable = oracle["acceptable_routes"]
    disallowed = oracle["disallowed_routes"]
    if expected not in ROUTES:
        raise ValueError(f"unsupported expected_route: {expected}")
    if not isinstance(acceptable, list) or expected not in acceptable:
        raise ValueError("acceptable_routes must be a list containing expected_route")
    if not isinstance(disallowed, list):
        raise ValueError("disallowed_routes must be a list")


def _rate(count: int, total: int) -> float:
    return count / total if total else 0.0


def _compute_weight(item: dict[str, Any]) -> float:
    metadata = item.get("router_visible_metadata")
    if not isinstance(metadata, dict):
        return 0.0
    value = metadata.get("compute_weight", 1)
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def evaluate_items(
    items: list[dict[str, Any]],
    *,
    profile_id: str,
    policy: RoutePolicy,
) -> dict[str, Any]:
    total = len(items)
    route_counts: Counter[str] = Counter({route: 0 for route in ROUTES})
    fallback_counts: Counter[str] = Counter({kind: 0 for kind in FALLBACK_CLASSES})
    exact_matches = 0
    acceptable_matches = 0
    unsafe_misroutes = 0
    gpu_false_positive_count = 0
    gpu_false_negative_count = 0
    cache_selected = 0
    cache_correct = 0
    errors: list[dict[str, str]] = []
    item_results: list[dict[str, Any]] = []
    total_compute_weight = 0.0
    gpu_compute_weight = 0.0
    policy_id = ""
    policy_version = ""

    for item in items:
        request_id = str(item.get("request_id", ""))
        try:
            validate_matrix_item(item)
            route_request = route_request_from_item(item)
            decision = policy(route_request)
            if decision.selected_route not in ROUTES:
                raise ValueError(f"unsupported selected_route: {decision.selected_route}")
            policy_id = decision.policy_id
            policy_version = decision.policy_version
            oracle = item["oracle_labels"]
            expected_route = str(oracle["expected_route"])
            acceptable_routes = [str(route) for route in oracle["acceptable_routes"]]
            disallowed_routes = [str(route) for route in oracle["disallowed_routes"]]
            selected = decision.selected_route
            route_counts[selected] += 1
            exact = selected == expected_route
            acceptable = selected in acceptable_routes
            unsafe = selected in disallowed_routes
            exact_matches += int(exact)
            acceptable_matches += int(acceptable)
            unsafe_misroutes += int(unsafe)
            gpu_false_positive_count += int(selected == "GPU" and "GPU" not in acceptable_routes)
            gpu_false_negative_count += int(expected_route == "GPU" and selected != "GPU")
            if selected == "cache":
                cache_selected += 1
                metadata = route_request.router_visible_metadata
                cache_correct += int(bool(metadata.get("cache_key_available")) and "cache" in acceptable_routes)
            fallback_classification = decision.fallback_classification
            if selected == "fallback":
                fallback_classification = fallback_classification or "unknown_fallback"
                if fallback_classification not in FALLBACK_CLASSES:
                    fallback_classification = "unknown_fallback"
                fallback_counts[fallback_classification] += 1
            weight = _compute_weight(item)
            total_compute_weight += weight
            if selected == "GPU":
                gpu_compute_weight += weight
            item_results.append(
                {
                    "request_id": request_id,
                    "selected_route": selected,
                    "expected_route": expected_route,
                    "acceptable": acceptable,
                    "unsafe_misroute": unsafe,
                    "decision_reason": decision.decision_reason,
                    "fallback_classification": fallback_classification,
                    "error": None,
                }
            )
        except Exception as exc:  # noqa: BLE001 - surfaced as item-level dry-run error.
            errors.append({"request_id": request_id, "error": str(exc)})
            item_results.append(
                {
                    "request_id": request_id,
                    "selected_route": None,
                    "expected_route": None,
                    "acceptable": False,
                    "unsafe_misroute": False,
                    "decision_reason": None,
                    "fallback_classification": None,
                    "error": str(exc),
                }
            )

    error_count = len(errors)
    metrics = {
        "exact_route_accuracy": _rate(exact_matches, total),
        "acceptable_route_rate": _rate(acceptable_matches, total),
        "unsafe_misroute_rate": _rate(unsafe_misroutes, total),
        "gpu_false_positive_count": gpu_false_positive_count,
        "gpu_false_negative_count": gpu_false_negative_count,
        "cache_hit_correctness_rate": (
            cache_correct / cache_selected if cache_selected else None
        ),
        "safety_fallback_rate": _rate(fallback_counts["safety_fallback"], total),
        "failure_fallback_rate": _rate(fallback_counts["failure_fallback"], total),
        "error_count": error_count,
        "error_percentage": _rate(error_count, total),
        "compute_weighted_gpu_demand": (
            gpu_compute_weight / total_compute_weight if total_compute_weight else None
        ),
        "compute_weight_formula_version": "cwgd_v0",
    }
    return {
        "schema_version": "krk_route_metrics_v0",
        "profile_id": profile_id,
        "policy_id": policy_id,
        "policy_version": policy_version,
        "total_requests": total,
        "route_counts": dict(route_counts),
        "metrics": metrics,
        "fallback_counts": dict(fallback_counts),
        "items": item_results,
        "errors": errors,
        "claim_level": "dry_run_route_selectivity",
        "claim_boundary": CLAIM_BOUNDARY,
    }
