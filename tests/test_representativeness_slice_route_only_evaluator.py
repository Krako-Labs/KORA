from __future__ import annotations

import json
import subprocess
import sys

from scripts.evaluate_representativeness_slice_routes import DEFAULT_FIXTURE, evaluate_routes
from scripts.validate_representativeness_seed import ALLOWED_ROUTES, validate_seed


def test_slice_fixture_loads_and_is_public_safe() -> None:
    summary = validate_seed(DEFAULT_FIXTURE)

    assert summary["ok"] is True
    assert summary["item_count"] == 40
    assert summary["category_count"] == 12
    assert summary["public_safe"] is True
    assert summary["claim_scope"] == "fixture_only"
    assert set(summary["route_counts"]) == ALLOWED_ROUTES


def test_slice_fixture_item_ids_are_unique_and_route_labels_are_accepted() -> None:
    fixture = json.loads(DEFAULT_FIXTURE.read_text(encoding="utf-8"))

    ids = [item["id"] for item in fixture["items"]]
    routes = {item["expected_route"] for item in fixture["items"]}

    assert len(ids) == len(set(ids))
    assert routes == ALLOWED_ROUTES
    assert all(item["id"].startswith("rep-slice-v1-") for item in fixture["items"])
    assert all(item["public_safe"] is True for item in fixture["items"])
    assert all(item["claim_scope"] == "fixture_only" for item in fixture["items"])


def test_slice_route_only_evaluator_counters_are_stable() -> None:
    summary = evaluate_routes(DEFAULT_FIXTURE)

    assert summary["ok"] is True
    assert summary["total_slice_items"] == 40
    assert summary["route_counts"] == {
        "cache": 7,
        "cpu": 6,
        "deterministic": 5,
        "fallback": 4,
        "gpu": 3,
        "provider_needed": 4,
        "retrieval_needed": 5,
        "tool_needed": 6,
    }
    assert summary["route_group_counts"] == {
        "cache_reuse_candidates": 7,
        "deterministic_local_route_candidates": 22,
        "fallback_control_candidates": 4,
        "provider_model_candidates": 7,
    }
    assert summary["unsupported_unknown_missing_route_metadata_count"] == 0


def test_slice_route_only_evaluator_counts_workload_categories() -> None:
    summary = evaluate_routes(DEFAULT_FIXTURE)

    assert summary["workload_category_counts"] == {
        "cache_reuse_candidates": 3,
        "cpu_local_transforms": 3,
        "document_intake_normalization": 4,
        "gpu_candidate_batch_labels": 3,
        "local_policy_checks": 4,
        "multi_step_app_workflow": 4,
        "provider_needed_ambiguous_tasks": 3,
        "report_generation_control": 2,
        "retrieval_needed_candidates": 3,
        "retry_fallback_control": 4,
        "schema_validation": 4,
        "tool_needed_local_actions": 3,
    }


def test_slice_evaluator_output_remains_route_only() -> None:
    summary = evaluate_routes(DEFAULT_FIXTURE)

    assert "does_not_call_providers" in summary["non_claims"]
    assert "does_not_run_model_inference" in summary["non_claims"]
    assert "does_not_prove_output_quality" in summary["non_claims"]
    assert "does_not_prove_broader_workload_representativeness" in summary["non_claims"]
    assert "does_not_prove_production_readiness" in summary["non_claims"]
    assert "quality_score" not in summary
    assert "semantic_judgment" not in summary
    assert "human_grade" not in summary


def test_slice_route_only_evaluator_cli_outputs_deterministic_json() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_representativeness_slice_routes.py",
            "--fixture",
            str(DEFAULT_FIXTURE),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    summary = json.loads(completed.stdout)
    assert summary["total_slice_items"] == 40
    assert list(summary["route_counts"]) == [
        "cache",
        "cpu",
        "deterministic",
        "fallback",
        "gpu",
        "provider_needed",
        "retrieval_needed",
        "tool_needed",
    ]
    assert summary["unsupported_unknown_missing_route_metadata_count"] == 0
