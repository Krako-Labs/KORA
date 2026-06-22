from __future__ import annotations

import json
import subprocess
import sys

from scripts.evaluate_representativeness_seed_routes import DEFAULT_FIXTURE, evaluate_routes


def test_route_only_evaluator_counts_seed_routes() -> None:
    summary = evaluate_routes(DEFAULT_FIXTURE)

    assert summary["ok"] is True
    assert summary["total_seed_items"] == 40
    assert summary["route_counts"] == {
        "cache": 6,
        "cpu": 5,
        "deterministic": 7,
        "fallback": 5,
        "gpu": 3,
        "provider_needed": 8,
        "retrieval_needed": 1,
        "tool_needed": 5,
    }
    assert summary["route_group_counts"] == {
        "cache_reuse_candidates": 6,
        "deterministic_local_route_candidates": 18,
        "fallback_control_candidates": 5,
        "provider_model_candidates": 11,
    }
    assert summary["unsupported_unknown_missing_route_metadata_count"] == 0


def test_route_only_evaluator_counts_workload_categories() -> None:
    summary = evaluate_routes(DEFAULT_FIXTURE)

    assert summary["workload_category_counts"] == {
        "agent_workflow_steps": 3,
        "cache_reuse_repeated_work": 2,
        "document_intake": 3,
        "gpu_candidate_batch": 3,
        "incident_alert_routing": 3,
        "issue_triage": 3,
        "mixed_operational_workflow": 3,
        "output_quality_methodology_seed": 2,
        "policy_safety_fallback": 2,
        "provider_needed_ambiguous_tasks": 2,
        "rag_query_routing": 3,
        "report_generation_control": 3,
        "support_ticket_classification": 3,
        "tool_needed_local_actions": 2,
        "validation_schema_check": 3,
    }


def test_route_only_evaluator_cli_outputs_deterministic_json() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_representativeness_seed_routes.py",
            "--fixture",
            str(DEFAULT_FIXTURE),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    summary = json.loads(completed.stdout)
    assert summary["total_seed_items"] == 40
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
    assert summary["validation"] == {
        "claim_scope": "fixture_only",
        "public_safe": True,
        "shape_validated": True,
    }
    assert "does_not_call_providers" in summary["non_claims"]
