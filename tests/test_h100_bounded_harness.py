from __future__ import annotations

import json
from pathlib import Path

from kora.h100_bounded_harness import (
    CLAIM_BOUNDARY,
    CLAIM_LEVEL_NOT_RUN,
    build_bounded_operations,
    collect_gpu_routed_items,
    execute_bounded_h100,
    main,
    render_markdown_summary,
)


MATRIX_PATHS = [
    Path("examples/workloads/krk-mixed-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-cache-heavy-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-adversarial-routing-matrix-alpha.json"),
]


class _NoCuda:
    def is_available(self) -> bool:
        return False

    def device_count(self) -> int:
        return 0


class _NoCudaTorch:
    __version__ = "test"

    class version:
        cuda = None

    cuda = _NoCuda()


def test_collect_gpu_routed_items_uses_public_matrix_policy() -> None:
    items = collect_gpu_routed_items(MATRIX_PATHS)

    assert [item["request_id"] for item in items] == ["mixed-004", "gpu-001", "gpu-002", "cache-003"]
    assert all(item["selected_route"] == "GPU" for item in items)


def test_build_bounded_operations_repeats_public_gpu_subset() -> None:
    items = collect_gpu_routed_items(MATRIX_PATHS)
    operations = build_bounded_operations(items, target_count=8)

    assert len(operations) == 8
    assert operations[0].request_id == "mixed-004"
    assert operations[4].request_id == "mixed-004"


def test_execute_bounded_h100_no_cuda_returns_not_run_result() -> None:
    result = execute_bounded_h100(
        MATRIX_PATHS,
        target_count=8,
        repo_commit_value="test-commit",
        torch_module=_NoCudaTorch(),
    )

    assert result["schema_version"] == "krk_h100_bounded_harness_v0"
    assert result["claim_level"] == CLAIM_LEVEL_NOT_RUN
    assert result["run_status"] == "not_run"
    assert result["fixture_count"] == 18
    assert result["gpu_routed_count"] == 4
    assert result["operation_count"] == 0
    assert result["cuda"]["cuda_available"] is False
    assert result["public_boundary"]["raw_logs_committed"] is False
    assert "private" not in json.dumps(result["source"]).lower()


def test_render_markdown_summary_preserves_claim_boundary() -> None:
    result = execute_bounded_h100(
        MATRIX_PATHS,
        target_count=8,
        repo_commit_value="test-commit",
        torch_module=_NoCudaTorch(),
    )
    markdown = render_markdown_summary(result)

    assert "# KRK H100 Bounded Harness Summary v0" in markdown
    assert "run status: `not_run`" in markdown
    assert CLAIM_BOUNDARY in markdown
    assert "production savings" in markdown


def test_h100_bounded_cli_writes_json_and_markdown(tmp_path: Path) -> None:
    json_out = tmp_path / "h100.json"
    md_out = tmp_path / "h100.md"
    argv: list[str] = []
    for matrix_path in MATRIX_PATHS:
        argv.extend(["--matrix", str(matrix_path)])
    argv.extend([
        "--target-count",
        "8",
        "--json-out",
        str(json_out),
        "--md-out",
        str(md_out),
        "--repo-commit",
        "test-commit",
    ])

    exit_code = main(argv)

    assert exit_code == 0
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    markdown = md_out.read_text(encoding="utf-8")
    assert saved["schema_version"] == "krk_h100_bounded_harness_v0"
    assert saved["gpu_routed_count"] == 4
    assert "# KRK H100 Bounded Harness Summary v0" in markdown
