import json
from pathlib import Path

from experiments.run_benchmark import load_workload, run_dry_run


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
