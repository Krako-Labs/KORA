from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def _load_module():
    script_path = Path("examples/rag_routing/run.py")
    spec = importlib.util.spec_from_file_location("rag_routing_run", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load RAG routing module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_rag_routing_summary_matches_expected_counters() -> None:
    module = _load_module()
    expected = json.loads(
        Path("examples/rag_routing/expected_counters.json").read_text(encoding="utf-8")
    )

    summary = module.build_rag_summary()

    assert summary["ok"] is True
    for key, value in expected.items():
        assert summary[key] == value
    assert summary["expected_match_count"] == summary["total_queries"]
    assert summary["provider_calls_actually_made"] == 0


def test_rag_routing_uses_kora_task_graph_and_cache_paths() -> None:
    module = _load_module()

    summary = module.build_rag_summary()

    deterministic = [item for item in summary["results"] if item["route_kind"] == "deterministic_answer"]
    retrieval = [item for item in summary["results"] if item["route_kind"] == "retrieval_needed"]
    cache_hits = [item for item in summary["results"] if item["route_kind"] == "cache_hit"]
    provider_needed = [item for item in summary["results"] if item["route_kind"] == "provider_needed"]
    assert len(deterministic) == 2
    assert len(retrieval) == 2
    assert len(cache_hits) == 1
    assert len(provider_needed) == 2
    assert all(str(item["kora_graph_id"]).startswith("rag-routing-") for item in deterministic)
    assert all(item["source"] == "kora_task_graph" for item in retrieval)
    assert retrieval[0]["retrieved_documents"][0]["id"] == "doc-security-retention"
    assert cache_hits[0]["handler"] == "cache_reuse"
    assert all(item["provider_calls"] == 0 for item in summary["results"])


def test_rag_routing_report_contains_required_sections() -> None:
    module = _load_module()

    report = module.render_report(module.build_rag_summary())

    assert "KORA RAG Routing Example" in report
    assert "Total queries: 7" in report
    assert "Deterministic answered: 2" in report
    assert "Cache hits: 1" in report
    assert "Retrieval-needed: 2" in report
    assert "Provider-needed: 2" in report
    assert "Provider calls actually made: 0" in report
    assert "Claim boundary:" in report


def test_rag_routing_cli_writes_outputs(tmp_path: Path) -> None:
    json_out = tmp_path / "rag.json"
    report_md = tmp_path / "rag.md"

    completed = subprocess.run(
        [
            sys.executable,
            "examples/rag_routing/run.py",
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
    assert "KORA RAG Routing Example" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["mode"] == "rag_routing_example"
    assert saved["total_queries"] == 7
    assert saved["retrieval_needed"] == 2
    assert saved["provider_calls_actually_made"] == 0
    assert report_md.read_text(encoding="utf-8") == completed.stdout


def test_rag_routing_appears_in_example_listing() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "kora", "examples", "list"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "rag_routing: offline RAG routing control example" in completed.stdout
