from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from kora.openai_proxy_demo import (
    DEFAULT_REQUESTS_PATH,
    build_proxy_summary,
    message_text,
    request_cache_key,
)


def _run_kora(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("OPENAI_API_KEY", None)
    env.pop("ANTHROPIC_API_KEY", None)
    return subprocess.run(
        [sys.executable, "-m", "kora", *args],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def test_proxy_demo_module_matches_expected_counters() -> None:
    expected = json.loads(
        Path("examples/openai_compatible_proxy/expected_counters.json").read_text(encoding="utf-8")
    )

    summary = build_proxy_summary(requests_path=DEFAULT_REQUESTS_PATH)

    assert summary["ok"] is True
    for key, value in expected.items():
        assert summary[key] == value
    assert summary["mode"] == "openai_proxy_demo"
    assert summary["expected_match_count"] == summary["total_requests"]
    assert summary["provider_calls_actually_made"] == 0


def test_proxy_demo_module_uses_kora_graph_and_cache_paths() -> None:
    summary = build_proxy_summary(requests_path=DEFAULT_REQUESTS_PATH)

    deterministic = [item for item in summary["results"] if item["route_kind"] == "deterministic"]
    cache_hits = [item for item in summary["results"] if item["route_kind"] == "cache_hit"]
    provider_needed = [item for item in summary["results"] if item["route_kind"] == "provider_required"]

    assert len(deterministic) == 3
    assert len(cache_hits) == 1
    assert len(provider_needed) == 2
    assert all(item["source"] == "kora_task_graph" for item in deterministic)
    assert all(str(item["kora_graph_id"]).startswith("openai-compatible-proxy-") for item in deterministic)
    assert cache_hits[0]["source"] == "cache"
    assert cache_hits[0]["selected_route"] == "proxy.cache.reuse"
    assert all(item["handler"] == "provider_needed_fallback" for item in provider_needed)


def test_proxy_demo_module_extracts_chat_message_text_and_cache_key() -> None:
    request = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Classify only."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Classify this ticket:"},
                    {"type": "text", "text": "Customer was charged twice"},
                ],
            },
        ],
    }

    assert message_text(request) == "Classify only. Classify this ticket: Customer was charged twice"
    assert request_cache_key(request) == request_cache_key(dict(reversed(list(request.items()))))


def test_proxy_demo_cli_runs_and_writes_outputs(tmp_path: Path) -> None:
    json_out = tmp_path / "proxy_demo.json"
    report_md = tmp_path / "proxy_demo.md"

    completed = _run_kora(
        "proxy-demo",
        "examples/openai_compatible_proxy/requests.json",
        "--json-out",
        str(json_out),
        "--report-md",
        str(report_md),
    )

    assert completed.returncode == 0
    assert "KORA OpenAI Proxy Demo" in completed.stdout
    assert "Total requests: 6" in completed.stdout
    assert "Cache hits: 1" in completed.stdout
    assert "Provider calls actually made: 0" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["mode"] == "openai_proxy_demo_cli"
    assert saved["avoided_provider_invocations"] == 4
    assert saved["provider_calls_actually_made"] == 0
    assert report_md.read_text(encoding="utf-8") == completed.stdout


def test_proxy_demo_cli_missing_file_fails_cleanly() -> None:
    completed = _run_kora("proxy-demo", "/tmp/not-a-kora-proxy-fixture.json")

    assert completed.returncode == 2
    assert "KORA proxy demo request JSON not found" in completed.stderr
