from __future__ import annotations

from kora.route_selectivity_metrics import (
    RouteDecision,
    RouteRequest,
    evaluate_items,
    krk_dry_run_policy,
    route_request_from_item,
)


def _item(
    request_id: str,
    *,
    metadata: dict,
    expected_route: str,
    acceptable_routes: list[str] | None = None,
    disallowed_routes: list[str] | None = None,
) -> dict:
    return {
        "request_id": request_id,
        "workload_profile": "test-profile",
        "workload_class": "test-class",
        "router_visible_metadata": metadata,
        "oracle_labels": {
            "expected_route": expected_route,
            "acceptable_routes": acceptable_routes or [expected_route],
            "disallowed_routes": disallowed_routes or [],
            "oracle_reason": "test oracle",
        },
    }


def test_route_request_excludes_oracle_labels() -> None:
    item = _item(
        "req-1",
        metadata={
            "input_size": "small",
            "batch_size": 1,
            "request_modality": "text",
            "cache_key_available": False,
            "latency_sensitivity": "high",
            "privacy_preference": "local",
            "estimated_complexity": "low",
            "compute_weight": 1,
        },
        expected_route="deterministic",
    )

    request = route_request_from_item(item)

    assert isinstance(request, RouteRequest)
    assert not hasattr(request, "oracle_labels")
    assert "oracle_labels" not in request.router_visible_metadata


def test_krk_dry_run_policy_uses_visible_metadata() -> None:
    request = RouteRequest(
        request_id="req-1",
        workload_profile="test",
        workload_class="known-template",
        router_visible_metadata={
            "input_size": "small",
            "batch_size": 1,
            "request_modality": "text",
            "cache_key_available": False,
            "latency_sensitivity": "high",
            "privacy_preference": "local",
            "estimated_complexity": "low",
            "compute_weight": 1,
        },
    )

    decision = krk_dry_run_policy(request)

    assert decision.selected_route == "deterministic"
    assert decision.policy_id == "KRK"
    assert decision.policy_version == "krk_dry_run_v0"


def test_evaluate_items_computes_route_metrics() -> None:
    items = [
        _item(
            "det",
            metadata={
                "input_size": "small",
                "batch_size": 1,
                "request_modality": "text",
                "cache_key_available": False,
                "latency_sensitivity": "high",
                "privacy_preference": "local",
                "estimated_complexity": "low",
                "compute_weight": 1,
            },
            expected_route="deterministic",
            disallowed_routes=["GPU"],
        ),
        _item(
            "gpu",
            metadata={
                "input_size": "large",
                "batch_size": 32,
                "request_modality": "text",
                "cache_key_available": False,
                "latency_sensitivity": "medium",
                "privacy_preference": "local_or_sanitized",
                "estimated_complexity": "high",
                "compute_weight": 9,
            },
            expected_route="GPU",
            disallowed_routes=["cache"],
        ),
        _item(
            "fallback",
            metadata={
                "input_size": "unknown",
                "batch_size": 0,
                "request_modality": "unknown",
                "cache_key_available": False,
                "latency_sensitivity": "low",
                "privacy_preference": "restricted",
                "estimated_complexity": "unknown",
                "compute_weight": 1,
            },
            expected_route="fallback",
            disallowed_routes=["provider", "GPU"],
        ),
    ]

    result = evaluate_items(items, profile_id="test-profile", policy=krk_dry_run_policy)

    assert result["total_requests"] == 3
    assert result["route_counts"]["deterministic"] == 1
    assert result["route_counts"]["GPU"] == 1
    assert result["route_counts"]["fallback"] == 1
    assert result["metrics"]["exact_route_accuracy"] == 1.0
    assert result["metrics"]["acceptable_route_rate"] == 1.0
    assert result["metrics"]["unsafe_misroute_rate"] == 0.0
    assert result["metrics"]["gpu_false_positive_count"] == 0
    assert result["metrics"]["gpu_false_negative_count"] == 0
    assert result["metrics"]["safety_fallback_rate"] == 1 / 3
    assert result["metrics"]["compute_weighted_gpu_demand"] == 9 / 11


def test_evaluate_items_detects_gpu_false_positive_and_negative() -> None:
    items = [
        _item(
            "false-positive",
            metadata={
                "input_size": "small",
                "batch_size": 1,
                "request_modality": "text",
                "cache_key_available": False,
                "latency_sensitivity": "high",
                "privacy_preference": "local",
                "estimated_complexity": "low",
                "compute_weight": 1,
            },
            expected_route="deterministic",
            disallowed_routes=["GPU"],
        ),
        _item(
            "false-negative",
            metadata={
                "input_size": "small",
                "batch_size": 1,
                "request_modality": "text",
                "cache_key_available": False,
                "latency_sensitivity": "high",
                "privacy_preference": "local",
                "estimated_complexity": "low",
                "compute_weight": 1,
            },
            expected_route="GPU",
            acceptable_routes=["GPU"],
            disallowed_routes=["deterministic"],
        ),
    ]

    def policy(request: RouteRequest) -> RouteDecision:
        if request.request_id == "false-positive":
            return RouteDecision("GPU", "test", "v0", "forced GPU")
        return RouteDecision("deterministic", "test", "v0", "forced deterministic")

    result = evaluate_items(items, profile_id="test-profile", policy=policy)

    assert result["metrics"]["gpu_false_positive_count"] == 1
    assert result["metrics"]["gpu_false_negative_count"] == 1
    assert result["metrics"]["unsafe_misroute_rate"] == 1.0


def test_cache_hit_correctness_rate_is_null_without_cache_routes() -> None:
    items = [
        _item(
            "det",
            metadata={
                "input_size": "small",
                "batch_size": 1,
                "request_modality": "text",
                "cache_key_available": False,
                "latency_sensitivity": "high",
                "privacy_preference": "local",
                "estimated_complexity": "low",
                "compute_weight": 1,
            },
            expected_route="deterministic",
        )
    ]

    result = evaluate_items(items, profile_id="test-profile", policy=krk_dry_run_policy)

    assert result["metrics"]["cache_hit_correctness_rate"] is None
