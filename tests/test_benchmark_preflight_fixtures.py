import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "examples/benchmarks/three-environment"


def test_comparison_plan_preserves_native_baseline_and_claim_boundaries():
    plan = json.loads((ROOT / "comparison-plan.json").read_text())
    assert plan["status"] == "configuration-frozen-execution-unverified"
    assert plan["h100_primary"]["kora_execution_control"] is False
    assert plan["h100_controlled"]["artifact"] == "same-as-local"
    assert plan["cluster"]["memory_pooling"] is False
    assert plan["model"]["capacity_candidate"] is None
    artifact = plan["local"]["artifact"]
    assert len(artifact["sha256"]) == 64
    assert len(artifact["revision"]) == 40
    assert artifact["bytes"] == 18556685824
    assert plan["measurement"]["failed_runs_retained"] is True


def test_fixtures_are_unique_and_exact_expected_values_are_consistent():
    corpus = json.loads((ROOT / "workloads.json").read_text())
    assert len(corpus["cases"]) == 6
    assert len({item["id"] for item in corpus["cases"]}) == 6
    for item in corpus["cases"]:
        assert item["expected_model_output"]["category"] in {"billing", "access", "delivery"}
        data = item["structured_input"]
        expected = item["expected_deterministic_output"]
        assert expected == {"total": data["quantity"] * data["unit_price"], "currency": "KRW"}
    assert corpus["quality_gate"]["aggregate_required_pass_rate"] == 1.0
