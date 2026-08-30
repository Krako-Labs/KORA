from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any

import pytest

from kora import executor as executor_module
from kora.adapters.base import BaseAdapter
from kora.adapters.mlx_local import MLXLocalAdapter, MLXLocalRuntimeError
from kora.executor import _AdapterRegistry, run_graph
from kora.task_ir import TaskGraph, normalize_graph, validate_graph


def _env(tmp_path: Path) -> dict[str, str]:
    python = tmp_path / "python"
    python.write_text("", encoding="utf-8")
    model = tmp_path / "model"
    model.mkdir()
    hf_home = tmp_path / "hf"
    hf_home.mkdir()
    return {
        "KORA_MLX_PYTHON": str(python),
        "KORA_MLX_MODEL": str(model),
        "HF_HOME": str(hf_home),
    }


@pytest.mark.parametrize("missing", ["KORA_MLX_PYTHON", "KORA_MLX_MODEL", "HF_HOME"])
def test_mlx_adapter_fails_closed_when_required_config_missing(
    tmp_path: Path, missing: str
) -> None:
    environ = _env(tmp_path)
    del environ[missing]

    with pytest.raises(MLXLocalRuntimeError, match="no provider fallback"):
        MLXLocalAdapter(environ=environ).run(
            task_id="llm", input={"question": "synthetic"}, budget={}, output_schema={}
        )


def test_mlx_adapter_fails_closed_when_python_file_is_missing(tmp_path: Path) -> None:
    environ = _env(tmp_path)
    environ["KORA_MLX_PYTHON"] = str(tmp_path / "missing-python")

    with pytest.raises(MLXLocalRuntimeError, match="not an existing file"):
        MLXLocalAdapter(environ=environ).run(
            task_id="llm", input={"question": "synthetic"}, budget={}, output_schema={}
        )


def test_mlx_adapter_fails_closed_when_model_is_not_cached(tmp_path: Path) -> None:
    environ = _env(tmp_path)
    environ["KORA_MLX_MODEL"] = "example/missing-model"

    with pytest.raises(MLXLocalRuntimeError, match="offline cache"):
        MLXLocalAdapter(environ=environ).run(
            task_id="llm", input={"question": "synthetic"}, budget={}, output_schema={}
        )


def test_mlx_adapter_parses_one_worker_json_object_and_forces_offline(
    tmp_path: Path,
) -> None:
    calls: list[dict[str, Any]] = []

    def runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append({"command": command, **kwargs})
        response = {
            "ok": True,
            "output": {"status": "ok", "task_id": "llm", "answer": "generated"},
            "usage": {"time_ms": 10, "tokens_in": 4, "tokens_out": 1},
            "meta": {"adapter": "mlx_local", "model_calls": 1},
        }
        return subprocess.CompletedProcess(command, 0, json.dumps(response), "")

    result = MLXLocalAdapter(environ=_env(tmp_path), runner=runner).run(
        task_id="llm",
        input={"question": "synthetic"},
        budget={"max_tokens": 500},
        output_schema={},
    )

    assert result["output"]["answer"] == "generated"
    request = json.loads(calls[0]["input"])
    assert request["max_tokens"] == 128
    assert calls[0]["env"]["HF_HUB_OFFLINE"] == "1"
    assert calls[0]["env"]["TRANSFORMERS_OFFLINE"] == "1"


def test_mlx_adapter_rejects_invalid_worker_stdout(tmp_path: Path) -> None:
    def runner(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 0, "not-json", "")

    with pytest.raises(MLXLocalRuntimeError, match="valid JSON object"):
        MLXLocalAdapter(environ=_env(tmp_path), runner=runner).run(
            task_id="llm", input={"question": "synthetic"}, budget={}, output_schema={}
        )


def _graph(text: str) -> TaskGraph:
    return TaskGraph.model_validate(
        {
            "graph_id": "task007-unit",
            "version": "0.1",
            "root": "answer",
            "defaults": {"budget": {"max_time_ms": 5000, "max_tokens": 32, "max_retries": 0}},
            "tasks": [
                {
                    "id": "route",
                    "type": "det.route",
                    "in": {"text": text},
                    "run": {
                        "kind": "det",
                        "spec": {
                            "handler": "classify_by_rules",
                            "args": {
                                "scenario_id": "task007",
                                "routes": [
                                    {
                                        "route_id": "support.hours",
                                        "keywords": ["support hours"],
                                        "output": {"answer": "Support is open 09:00-17:00."},
                                    }
                                ],
                            },
                        },
                    },
                },
                {
                    "id": "answer",
                    "type": "llm.answer",
                    "deps": ["route"],
                    "run": {
                        "kind": "llm",
                        "spec": {
                            "adapter": "mlx_local",
                            "input": {
                                "question": text,
                                "skip_if": {"path": "$.route_kind", "equals": "deterministic"},
                            },
                            "output_schema": {
                                "type": "object",
                                "required": ["status", "task_id", "answer"],
                            },
                        },
                    },
                    "policy": {"on_fail": "fail"},
                },
            ],
        }
    )


def test_registry_recognizes_mlx_local() -> None:
    assert isinstance(_AdapterRegistry.get("mlx_local"), MLXLocalAdapter)


def test_deterministic_route_skips_mlx_adapter_invocation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KORA_MLX_PYTHON", raising=False)
    graph = normalize_graph(_graph("What are the support hours?"))
    validate_graph(graph)

    result = run_graph(graph)

    assert result["ok"] is True
    assert result["outputs"]["route"]["selected_route"] == "support.hours"
    assert result["outputs"]["answer"]["skipped"] is True


def test_model_needed_path_calls_injected_mlx_adapter_once() -> None:
    class FakeMLXAdapter(BaseAdapter):
        calls = 0

        def run(self, *, task_id: str, input: dict[str, Any], budget: dict[str, Any], output_schema: dict[str, Any]) -> dict[str, Any]:
            del input, budget, output_schema
            type(self).calls += 1
            return {
                "ok": True,
                "output": {"status": "ok", "task_id": task_id, "answer": "local generated answer"},
                "usage": {"time_ms": 1, "tokens_in": 2, "tokens_out": 3},
                "meta": {"adapter": "mlx_local", "model_calls": 1},
            }

    old = executor_module._AdapterRegistry.providers["mlx_local"]
    executor_module._AdapterRegistry.providers["mlx_local"] = FakeMLXAdapter
    try:
        graph = normalize_graph(_graph("Suggest a name for a fictional moon."))
        validate_graph(graph)
        result = run_graph(graph)
    finally:
        executor_module._AdapterRegistry.providers["mlx_local"] = old

    assert result["ok"] is True
    assert result["outputs"]["route"]["route_kind"] == "provider_required"
    assert result["outputs"]["answer"]["answer"] == "local generated answer"
    assert FakeMLXAdapter.calls == 1
