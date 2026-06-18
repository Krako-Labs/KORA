from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def _load_module():
    script_path = Path("examples/cache_reuse/run.py")
    spec = importlib.util.spec_from_file_location("cache_reuse_run", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load cache reuse module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cache_reuse_summary_matches_expected_counters() -> None:
    module = _load_module()
    expected = json.loads(
        Path("examples/cache_reuse/expected_counters.json").read_text(encoding="utf-8")
    )

    summary = module.build_cache_reuse_summary()

    assert summary["ok"] is True
    for key, value in expected.items():
        assert summary[key] == value
    assert summary["expected_match_count"] == summary["total_requests"]
    assert summary["provider_calls_actually_made"] == 0


def test_cache_reuse_uses_kora_task_graph_and_cache_paths() -> None:
    module = _load_module()

    summary = module.build_cache_reuse_summary()

    deterministic = [item for item in summary["results"] if item["route_kind"] == "deterministic"]
    cache_hits = [item for item in summary["results"] if item["route_kind"] == "cache_hit"]
    provider_needed = [item for item in summary["results"] if item["route_kind"] == "provider_required"]
    assert len(deterministic) == 3
    assert len(cache_hits) == 2
    assert len(provider_needed) == 2
    assert all(str(item["kora_graph_id"]).startswith("cache-reuse-") for item in deterministic)
    assert all(item["source"] == "cache" for item in cache_hits)
    assert cache_hits[0]["handler"] == "cache_reuse"
    assert cache_hits[0]["cache_key"] == cache_hits[1]["cache_key"]
    assert all(item["provider_calls"] == 0 for item in summary["results"])


def test_cache_reuse_report_contains_required_sections() -> None:
    module = _load_module()

    report = module.render_report(module.build_cache_reuse_summary())

    assert "KORA Cache Reuse Example" in report
    assert "Total requests: 7" in report
    assert "First-time deterministic handled: 3" in report
    assert "Cache hits: 2" in report
    assert "Provider-needed: 2" in report
    assert "Provider calls actually made: 0" in report
    assert "Claim boundary:" in report


def test_cache_reuse_cli_writes_outputs(tmp_path: Path) -> None:
    json_out = tmp_path / "cache_reuse.json"
    report_md = tmp_path / "cache_reuse.md"

    completed = subprocess.run(
        [
            sys.executable,
            "examples/cache_reuse/run.py",
            "--json-out",
            str(json_out),
            "--report-md",
            str(report_md),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "KORA Cache Reuse Example" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["mode"] == "cache_reuse_example"
    assert saved["total_requests"] == 7
    assert saved["cache_hits"] == 2
    assert saved["provider_calls_actually_made"] == 0
    assert report_md.read_text(encoding="utf-8") == completed.stdout


def test_cache_reuse_appears_in_example_listing() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "kora", "examples", "list"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "cache_reuse: offline cache reuse routing example" in completed.stdout
