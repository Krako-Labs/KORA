from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Any

import pytest

from kora import executor as executor_module
from kora.adapters.base import BaseAdapter
from kora.adapters.llama_cpp_local import LlamaCppLocalAdapter, LlamaCppLocalRuntimeError
from kora.executor import _AdapterRegistry, run_graph
from kora.task_ir import TaskGraph, normalize_graph, validate_graph


def _env(tmp_path: Path) -> dict[str, str]:
    binary = tmp_path / "llama-cli"
    binary.write_text("", encoding="utf-8")
    binary.chmod(0o755)
    model = tmp_path / "model.gguf"
    model.write_text("fixture", encoding="utf-8")
    return {"KORA_LLAMA_CPP_BIN": str(binary), "KORA_LLAMA_CPP_MODEL": str(model)}


@pytest.mark.parametrize("missing", ["KORA_LLAMA_CPP_BIN", "KORA_LLAMA_CPP_MODEL"])
def test_adapter_fails_closed_when_required_config_missing(tmp_path: Path, missing: str) -> None:
    environ = _env(tmp_path)
    del environ[missing]
    with pytest.raises(LlamaCppLocalRuntimeError, match="no download or provider fallback"):
        LlamaCppLocalAdapter(environ=environ).run(
            task_id="llm", input={"question": "synthetic"}, budget={}, output_schema={}
        )


def test_adapter_parses_subprocess_output_and_forces_offline(tmp_path: Path) -> None:
    calls: list[dict[str, Any]] = []

    def runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append({"command": command, **kwargs})
        timings = """
llama_perf_context_print:        load time =      100.00 ms
llama_perf_context_print: prompt eval time =       20.00 ms /    4 tokens
llama_perf_context_print:        eval time =       30.00 ms /    3 runs   ( 10.00 ms per token, 100.00 tokens per second )
"""
        return subprocess.CompletedProcess(command, 0, "generated answer\n", timings)

    result = LlamaCppLocalAdapter(environ=_env(tmp_path), runner=runner).run(
        task_id="llm", input={"question": "synthetic"}, budget={"max_tokens": 500}, output_schema={}
    )
    assert result["output"]["answer"] == "generated answer"
    assert result["usage"] == {"time_ms": 150, "tokens_in": 4, "tokens_out": 3}
    assert result["meta"]["runtime"] == "llama.cpp"
    assert result["meta"]["remote_provider_calls"] == 0
    assert calls[0]["env"]["NO_PROXY"] == "*"
    assert calls[0]["command"][calls[0]["command"].index("--predict") + 1] == "128"


def test_adapter_rejects_missing_performance_timings(tmp_path: Path) -> None:
    def runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 0, "answer", "no timings")

    with pytest.raises(LlamaCppLocalRuntimeError, match="required performance timings"):
        LlamaCppLocalAdapter(environ=_env(tmp_path), runner=runner).run(
            task_id="llm", input={"question": "synthetic"}, budget={}, output_schema={}
        )


def _graph(text: str) -> TaskGraph:
    return TaskGraph.model_validate({
        "graph_id": "task008-unit", "version": "0.1", "root": "answer",
        "defaults": {"budget": {"max_time_ms": 5000, "max_tokens": 32, "max_retries": 0}},
        "tasks": [
            {"id": "route", "type": "det.route", "in": {"text": text}, "run": {"kind": "det", "spec": {
                "handler": "classify_by_rules", "args": {"scenario_id": "task008", "routes": [{
                    "route_id": "support.hours", "keywords": ["support hours"],
                    "output": {"answer": "Support is open 09:00-17:00."}
                }]}}}},
            {"id": "answer", "type": "llm.answer", "deps": ["route"], "run": {"kind": "llm", "spec": {
                "adapter": "llama_cpp_local", "input": {"question": text, "skip_if": {
                    "path": "$.route_kind", "equals": "deterministic"}},
                "output_schema": {"type": "object", "required": ["status", "task_id", "answer"]}}},
             "policy": {"on_fail": "fail"}}
        ]})


def test_registry_recognizes_llama_cpp_local() -> None:
    assert isinstance(_AdapterRegistry.get("llama_cpp_local"), LlamaCppLocalAdapter)


def test_deterministic_route_skips_adapter_invocation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KORA_LLAMA_CPP_BIN", raising=False)
    graph = normalize_graph(_graph("What are the support hours?"))
    validate_graph(graph)
    result = run_graph(graph)
    assert result["ok"] is True
    assert result["outputs"]["answer"]["skipped"] is True


def test_model_needed_path_calls_injected_adapter_once() -> None:
    class FakeAdapter(BaseAdapter):
        calls = 0
        def run(self, *, task_id: str, input: dict[str, Any], budget: dict[str, Any], output_schema: dict[str, Any]) -> dict[str, Any]:
            del input, budget, output_schema
            type(self).calls += 1
            return {"ok": True, "output": {"status": "ok", "task_id": task_id, "answer": "local"},
                    "usage": {"time_ms": 1, "tokens_in": 2, "tokens_out": 3},
                    "meta": {"adapter": "llama_cpp_local", "model_calls": 1}}

    old = executor_module._AdapterRegistry.providers["llama_cpp_local"]
    executor_module._AdapterRegistry.providers["llama_cpp_local"] = FakeAdapter
    try:
        graph = normalize_graph(_graph("Suggest a fictional moon name."))
        validate_graph(graph)
        result = run_graph(graph)
    finally:
        executor_module._AdapterRegistry.providers["llama_cpp_local"] = old
    assert result["ok"] is True
    assert result["outputs"]["route"]["route_kind"] == "provider_required"
    assert result["outputs"]["answer"]["answer"] == "local"
    assert FakeAdapter.calls == 1
