from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def _load_module():
    script_path = Path("examples/agent_workflow_optimization/run.py")
    spec = importlib.util.spec_from_file_location("agent_workflow_optimization_run", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load agent workflow optimization module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_agent_workflow_summary_matches_expected_counters() -> None:
    module = _load_module()
    expected = json.loads(
        Path("examples/agent_workflow_optimization/expected_counters.json").read_text(
            encoding="utf-8"
        )
    )

    summary = module.build_agent_workflow_summary()

    assert summary["ok"] is True
    for key, value in expected.items():
        assert summary[key] == value
    assert summary["expected_match_count"] == summary["total_workflow_steps"]
    assert summary["provider_calls_actually_made"] == 0


def test_agent_workflow_uses_kora_task_graph_and_cache_paths() -> None:
    module = _load_module()

    summary = module.build_agent_workflow_summary()

    deterministic = [item for item in summary["results"] if item["route_kind"] == "deterministic"]
    cache_hits = [item for item in summary["results"] if item["route_kind"] == "cache_hit"]
    tool_needed = [item for item in summary["results"] if item["route_kind"] == "tool_needed"]
    provider_needed = [item for item in summary["results"] if item["route_kind"] == "provider_needed"]
    assert len(deterministic) == 4
    assert len(cache_hits) == 2
    assert len(tool_needed) == 3
    assert len(provider_needed) == 3
    assert all(str(item["kora_graph_id"]).startswith("agent-workflow-") for item in deterministic)
    assert all(item["source"] == "kora_task_graph" for item in tool_needed)
    assert tool_needed[0]["tool_name"] == "local_account_lookup"
    assert cache_hits[0]["handler"] == "cache_reuse"
    assert all(item["provider_calls"] == 0 for item in summary["results"])


def test_agent_workflow_report_contains_required_sections() -> None:
    module = _load_module()

    report = module.render_report(module.build_agent_workflow_summary())

    assert "KORA Agent Workflow Optimization Example" in report
    assert "Total workflow steps: 12" in report
    assert "Deterministic steps: 4" in report
    assert "Cache hits: 2" in report
    assert "Tool-needed steps: 3" in report
    assert "Provider-needed steps: 3" in report
    assert "Provider calls actually made: 0" in report
    assert "Claim boundary:" in report


def test_agent_workflow_cli_writes_outputs(tmp_path: Path) -> None:
    json_out = tmp_path / "agent_workflow.json"
    report_md = tmp_path / "agent_workflow.md"

    completed = subprocess.run(
        [
            sys.executable,
            "examples/agent_workflow_optimization/run.py",
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
    assert "KORA Agent Workflow Optimization Example" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["mode"] == "agent_workflow_optimization_example"
    assert saved["workflow_count"] == 3
    assert saved["total_workflow_steps"] == 12
    assert saved["tool_needed_steps"] == 3
    assert saved["provider_calls_actually_made"] == 0
    assert report_md.read_text(encoding="utf-8") == completed.stdout


def test_agent_workflow_appears_in_example_listing() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "kora", "examples", "list"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "agent_workflow_optimization: offline agent workflow control example" in completed.stdout
