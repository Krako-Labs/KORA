import json
from pathlib import Path

from experiments.generate_workload import CATEGORIES, generate_workload, write_workload


REQUIRED_TASK_FIELDS = {
    "id",
    "category",
    "input",
    "expected_path",
    "expected_output",
    "requires_model",
    "notes",
}


def test_generator_can_create_workload_file(tmp_path: Path) -> None:
    output_path = tmp_path / "deterministic_heavy_v1_100.json"
    workload = generate_workload(count=100, seed=42, benchmark_name="deterministic_heavy_v1")

    write_workload(workload, output_path)

    assert output_path.exists()
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["benchmark_name"] == "deterministic_heavy_v1"
    assert saved["name"] == "deterministic_heavy_v1"
    assert saved["seed"] == 42
    assert saved["task_count"] == 100


def test_generated_workload_has_100_tasks() -> None:
    workload = generate_workload(count=100, seed=42, benchmark_name="deterministic_heavy_v1")

    assert len(workload["tasks"]) == 100
    assert workload["task_count"] == 100


def test_generated_workload_is_reproducible_with_same_seed() -> None:
    first = generate_workload(count=100, seed=42, benchmark_name="deterministic_heavy_v1")
    second = generate_workload(count=100, seed=42, benchmark_name="deterministic_heavy_v1")

    assert first == second


def test_generated_workload_contains_all_expected_categories() -> None:
    workload = generate_workload(count=100, seed=42, benchmark_name="deterministic_heavy_v1")
    categories = {task["category"] for task in workload["tasks"]}

    assert categories == set(CATEGORIES)


def test_generated_workload_has_expected_model_requirement_split() -> None:
    workload = generate_workload(count=100, seed=42, benchmark_name="deterministic_heavy_v1")
    deterministic_count = sum(task["requires_model"] is False for task in workload["tasks"])
    fallback_count = sum(task["requires_model"] is True for task in workload["tasks"])

    assert deterministic_count == 80
    assert fallback_count == 20


def test_every_generated_task_has_required_schema_fields() -> None:
    workload = generate_workload(count=100, seed=42, benchmark_name="deterministic_heavy_v1")

    for task in workload["tasks"]:
        assert set(task) == REQUIRED_TASK_FIELDS
        assert isinstance(task["id"], str)
        assert isinstance(task["category"], str)
        assert isinstance(task["input"], dict)
        assert isinstance(task["expected_path"], str)
        assert isinstance(task["requires_model"], bool)
        assert isinstance(task["notes"], str)


def test_deterministic_tasks_have_expected_output_values() -> None:
    workload = generate_workload(count=100, seed=42, benchmark_name="deterministic_heavy_v1")

    for task in workload["tasks"]:
        if task["requires_model"] is False:
            assert task["expected_output"] is not None
            assert task["expected_output"] != {}
