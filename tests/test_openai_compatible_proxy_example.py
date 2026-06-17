from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def _load_module():
    script_path = Path("examples/openai_compatible_proxy/run.py")
    spec = importlib.util.spec_from_file_location("openai_compatible_proxy_run", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load openai proxy module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_openai_compatible_proxy_summary_matches_expected_counters() -> None:
    module = _load_module()
    expected = json.loads(
        Path("examples/openai_compatible_proxy/expected_counters.json").read_text(encoding="utf-8")
    )

    summary = module.build_proxy_summary()

    assert summary["ok"] is True
    for key, value in expected.items():
        assert summary[key] == value
    assert summary["expected_match_count"] == summary["total_requests"]


def test_openai_compatible_proxy_uses_kora_task_graph_path() -> None:
    module = _load_module()

    summary = module.build_proxy_summary()

    deterministic = [item for item in summary["results"] if item["route_kind"] == "deterministic"]
    provider_needed = [item for item in summary["results"] if item["route_kind"] == "provider_required"]
    cache_hits = [item for item in summary["results"] if item["route_kind"] == "cache_hit"]
    assert deterministic
    assert provider_needed
    assert cache_hits
    assert all(str(item["kora_graph_id"]).startswith("openai-compatible-proxy-") for item in deterministic)
    assert all(item["handler"] == "classify_by_rules" for item in deterministic)
    assert cache_hits[0]["handler"] == "cache_reuse"
    assert all(item["provider_calls"] == 0 for item in summary["results"])


def test_openai_compatible_proxy_report_contains_required_sections() -> None:
    module = _load_module()

    report = module.render_report(module.build_proxy_summary())

    assert "KORA OpenAI-Compatible Proxy Example" in report
    assert "Total requests: 6" in report
    assert "Deterministic handled: 3" in report
    assert "Cache hits: 1" in report
    assert "Provider-needed: 2" in report
    assert "Provider calls actually made: 0" in report
    assert "Claim boundary:" in report


def test_openai_compatible_proxy_cli_writes_outputs(tmp_path: Path) -> None:
    json_out = tmp_path / "proxy.json"
    report_md = tmp_path / "proxy.md"

    completed = subprocess.run(
        [
            sys.executable,
            "examples/openai_compatible_proxy/run.py",
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
    assert "KORA OpenAI-Compatible Proxy Example" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["mode"] == "openai_compatible_proxy_example"
    assert saved["total_requests"] == 6
    assert saved["provider_calls_actually_made"] == 0
    assert report_md.read_text(encoding="utf-8") == completed.stdout


def test_openai_compatible_proxy_appears_in_example_listing() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "kora", "examples", "list"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "openai_compatible_proxy: offline OpenAI-style proxy routing example" in completed.stdout
