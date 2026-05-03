import json
from pathlib import Path

from experiments.run_benchmark import (
    load_workload,
    run_direct_baseline,
    run_dry_run,
    run_kora_controlled,
)


WORKLOAD_PATH = Path("experiments/workloads/deterministic_heavy_v0.json")


def test_workload_json_can_be_loaded() -> None:
    workload = load_workload(WORKLOAD_PATH)

    assert workload["name"] == "deterministic_heavy_v0"
    assert isinstance(workload["tasks"], list)
    assert len(workload["tasks"]) == 20


def test_dry_run_result_counts_workload(tmp_path: Path) -> None:
    output_path = tmp_path / "deterministic_heavy_v0.dry_run.json"

    result = run_dry_run(WORKLOAD_PATH, output_path)

    assert result["benchmark_name"] == "deterministic_heavy_v0"
    assert result["mode"] == "dry-run"
    assert result["total_tasks"] == 20
    assert result["requires_model_true"] == 4
    assert result["requires_model_false"] == 16
    assert set(result["category_counts"]) == {
        "arithmetic",
        "cache_lookup",
        "json_validation",
        "routing_decision",
        "schema_check",
        "string_normalization",
    }


def test_dry_run_writes_output_json(tmp_path: Path) -> None:
    output_path = tmp_path / "result.json"

    run_dry_run(WORKLOAD_PATH, output_path)

    assert output_path.exists()
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["status"] == "ok"
    assert saved["total_tasks"] == 20


def test_direct_baseline_result_counts_simulated_model_invocations(tmp_path: Path) -> None:
    output_path = tmp_path / "deterministic_heavy_v0.direct_baseline.json"

    result = run_direct_baseline(WORKLOAD_PATH, output_path)

    assert result["benchmark_name"] == "deterministic_heavy_v0"
    assert result["mode"] == "direct-baseline"
    assert result["total_tasks"] == 20
    assert result["simulated_model_invocations"] == 20
    assert result["deterministic_tasks_sent_to_model"] == 16
    assert result["fallback_candidate_tasks_sent_to_model"] == 4


def test_direct_baseline_writes_output_json(tmp_path: Path) -> None:
    output_path = tmp_path / "direct_baseline.json"

    run_direct_baseline(WORKLOAD_PATH, output_path)

    assert output_path.exists()
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["status"] == "ok"
    assert saved["mode"] == "direct-baseline"
    assert saved["simulated_model_invocations"] == 20


def test_kora_controlled_result_counts_avoided_model_invocations(tmp_path: Path) -> None:
    output_path = tmp_path / "deterministic_heavy_v0.kora_controlled.json"

    result = run_kora_controlled(WORKLOAD_PATH, output_path)

    assert result["benchmark_name"] == "deterministic_heavy_v0"
    assert result["mode"] == "kora-controlled"
    assert result["total_tasks"] == 20
    assert result["deterministic_resolutions"] == 16
    assert result["fallback_candidates"] == 4
    assert result["simulated_model_invocations"] == 4
    assert result["avoided_model_invocations_vs_direct_baseline"] == 16
    assert result["avoided_model_invocation_rate"] == 0.8


def test_kora_controlled_writes_output_json(tmp_path: Path) -> None:
    output_path = tmp_path / "kora_controlled.json"

    run_kora_controlled(WORKLOAD_PATH, output_path)

    assert output_path.exists()
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["status"] == "ok"
    assert saved["mode"] == "kora-controlled"
    assert saved["simulated_model_invocations"] == 4
