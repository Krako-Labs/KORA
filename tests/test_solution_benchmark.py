from pathlib import Path

import pytest

from kora.solution import LocalSolutionHost
from kora.solution.benchmark import collect_local_runs

FIXTURE = Path(__file__).resolve().parents[1] / "examples/solutions/typed-node-fixture"


def test_measured_fixture_has_real_runs_and_no_synthetic_token_rate(tmp_path):
    host = LocalSolutionHost(tmp_path / "store")
    report = collect_local_runs(
        host,
        FIXTURE,
        {"text": " hello   world "},
        {"text": "hello world"},
        repetitions=2,
    )
    assert len({sample["run_id"] for sample in report["samples"]}) == 2
    for sample in report["samples"]:
        assert sample["quality_pass"]
        assert sample["deterministic_nodes_completed"] == 2
        assert sample["elapsed_ms"] >= 0
        assert sample["generated_tokens"] is None
        assert sample["ttft_ms"] is None
        assert sample["model_calls"] == sample["exact_reuse_hits"] == 0
        assert host.result(sample["run_id"])["output"] == {"text": "hello world"}


def test_wrong_expected_output_does_not_count_as_quality_success(tmp_path):
    report = collect_local_runs(
        LocalSolutionHost(tmp_path),
        FIXTURE,
        {"text": "hello"},
        {"text": "wrong"},
        repetitions=1,
    )
    assert report["samples"][0]["status"] == "succeeded"
    assert not report["samples"][0]["quality_pass"]


@pytest.mark.parametrize("count", [0, 101, True, 1.5])
def test_invalid_repetition_count_is_rejected(tmp_path, count):
    with pytest.raises(ValueError):
        collect_local_runs(
            LocalSolutionHost(tmp_path), FIXTURE, {}, {}, repetitions=count
        )
