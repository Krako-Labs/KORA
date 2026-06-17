import os, sys
import json
import pytest
from kora.executor import run_graph
from kora.task_ir import TaskGraph

# Helper to build a minimal deterministic graph using correct task_ir schema
def make_simple_graph():
    return TaskGraph.model_validate({
        "graph_id": "simple-graph",
        "version": "0.1",
        "root": "t1",
        "defaults": {
            "budget": {
                "max_time_ms": 1000,
                "max_tokens": 100,
                "max_retries": 0,
            }
        },
        "tasks": [
            {
                "id": "t1",
                "type": "det.echo",
                "deps": [],
                "in": {},
                "run": {
                    "kind": "det",
                    "spec": {
                        "handler": "echo",
                        "args": {"message": "hello"}
                    }
                },
                "verify": None,
                "policy": {"on_fail": "fail"},
                "tags": []
            }
        ]
    })

def test_fallback_to_python_when_rust_missing():
    # Ensure environment variable not set and rust module absent
    os.environ.pop('KORA_USE_RUST', None)
    graph = make_simple_graph()
    result = run_graph(graph)
    assert result["ok"] is True
    assert result["final"]["message"] == "hello"

def test_rust_path_success(monkeypatch):
    # Simulate rust module returning matching output
    class DummyRust:
        @staticmethod
        def run_graph(_):
            return json.dumps({"t1": {"status": "ok", "task_id": "t1", "message": "hello"}})
    monkeypatch.setitem(os.environ, 'KORA_USE_RUST', '1')
    monkeypatch.setitem(sys.modules, 'kora_rust', DummyRust)
    graph = make_simple_graph()
    result = run_graph(graph)
    assert result["ok"] is True
    assert result["final"]["message"] == "hello"
    assert "overall_total_s" in result["stage_timings"]

def test_rust_path_error_timeout_propagation(monkeypatch):
    class BadRust:
        @staticmethod
        def run_graph(_):
            raise ValueError("Execution failed: Task 't1' timed out (max_time_ms = 50 exceeded)")
    monkeypatch.setitem(os.environ, 'KORA_USE_RUST', '1')
    monkeypatch.setitem(sys.modules, 'kora_rust', BadRust)
    graph = make_simple_graph()
    result = run_graph(graph)
    assert result["ok"] is False
    assert result["error"]["error_type"] == "BUDGET_BREACH"
    assert result["error"]["stage"] == "BUDGET"
    assert result["error"]["budget_breached"] is True
    assert result["error"]["task_id"] == "t1"

def test_rust_path_error_verification_propagation(monkeypatch):
    class BadRust:
        @staticmethod
        def run_graph(_):
            raise ValueError("Execution failed: Verification failed for task 't1': schema mismatch")
    monkeypatch.setitem(os.environ, 'KORA_USE_RUST', '1')
    monkeypatch.setitem(sys.modules, 'kora_rust', BadRust)
    graph = make_simple_graph()
    result = run_graph(graph)
    assert result["ok"] is False
    assert result["error"]["error_type"] == "OUTPUT_SCHEMA_INVALID"
    assert result["error"]["stage"] == "VERIFY"
    assert result["error"]["task_id"] == "t1"
    assert "schema mismatch" in result["error"]["details"]

def test_rust_path_error_deterministic_propagation(monkeypatch):
    class BadRust:
        @staticmethod
        def run_graph(_):
            raise ValueError("Execution failed: Deterministic handler 't1' failed: missing arg")
    monkeypatch.setitem(os.environ, 'KORA_USE_RUST', '1')
    monkeypatch.setitem(sys.modules, 'kora_rust', BadRust)
    graph = make_simple_graph()
    result = run_graph(graph)
    assert result["ok"] is False
    assert result["error"]["error_type"] == "DETERMINISTIC_EXEC_FAILED"
    assert result["error"]["stage"] == "DETERMINISTIC"
    assert result["error"]["task_id"] == "t1"
    assert "missing arg" in result["error"]["details"]

def test_rust_path_error_llm_adapter_propagation(monkeypatch):
    class BadRust:
        @staticmethod
        def run_graph(_):
            raise ValueError("Execution failed: LLM adapter failed: API key invalid")
    monkeypatch.setitem(os.environ, 'KORA_USE_RUST', '1')
    monkeypatch.setitem(sys.modules, 'kora_rust', BadRust)
    graph = make_simple_graph()
    result = run_graph(graph)
    assert result["ok"] is False
    assert result["error"]["error_type"] == "ADAPTER_FAILED"
    assert result["error"]["stage"] == "ADAPTER"
    assert "API key invalid" in result["error"]["details"]

def test_rust_path_parity_with_python(monkeypatch):
    # Get Python result first
    os.environ.pop('KORA_USE_RUST', None)
    graph = make_simple_graph()
    py_result = run_graph(graph)

    # Set up Rust mock to return exact same output dictionary
    class MatchRust:
        @staticmethod
        def run_graph(_):
            return json.dumps(py_result["outputs"])
    
    monkeypatch.setitem(os.environ, 'KORA_USE_RUST', '1')
    monkeypatch.setitem(sys.modules, 'kora_rust', MatchRust)
    rust_result = run_graph(graph)

    # Assert contract parity
    assert rust_result["ok"] == py_result["ok"]
    assert rust_result["graph_id"] == py_result["graph_id"]
    assert rust_result["order"] == py_result["order"]
    assert rust_result["outputs"] == py_result["outputs"]
    assert rust_result["final"] == py_result["final"]
    assert "overall_total_s" in rust_result["stage_timings"]
    assert "overall_total_s" in py_result["stage_timings"]


def test_live_rust_executor_parity():
    try:
        import kora_rust
    except ImportError:
        pytest.skip("kora_rust is not compiled/installed in this environment")

    # Run simple graph with Python
    os.environ.pop('KORA_USE_RUST', None)
    graph = make_simple_graph()
    py_result = run_graph(graph)

    # Run simple graph with Rust
    os.environ['KORA_USE_RUST'] = '1'
    try:
        rust_result = run_graph(graph)
    finally:
        os.environ.pop('KORA_USE_RUST', None)

    # Verify parity of the full contract
    assert rust_result["ok"] is True
    assert py_result["ok"] is True
    assert rust_result["graph_id"] == py_result["graph_id"]
    assert rust_result["order"] == py_result["order"]
    assert rust_result["outputs"] == py_result["outputs"]
    assert rust_result["final"] == py_result["final"]
    assert len(rust_result["events"]) == len(py_result["events"])
    
    # Check events parity
    for re, pe in zip(rust_result["events"], py_result["events"]):
        assert re["task_id"] == pe["task_id"]
        assert re["status"] == pe["status"]
        assert re["stage"] == pe["stage"]

    assert "overall_total_s" in rust_result["stage_timings"]
    assert "det_total_s" in rust_result["stage_timings"]


def test_live_rust_executor_timeout_propagation():
    try:
        import kora_rust
    except ImportError:
        pytest.skip("kora_rust is not compiled/installed in this environment")

    graph = TaskGraph.model_validate({
        "graph_id": "timeout-graph",
        "version": "0.1",
        "root": "t1",
        "defaults": {
            "budget": {
                "max_time_ms": 20,  # 20ms budget
                "max_tokens": 100,
                "max_retries": 0,
            }
        },
        "tasks": [
            {
                "id": "t1",
                "type": "det.sleep",
                "deps": [],
                "in": {"ms": 100},  # sleeps 100ms
                "run": {
                    "kind": "det",
                    "spec": {
                        "handler": "sleep",
                        "args": {"ms": 100}
                    }
                },
                "verify": None,
                "policy": {"on_fail": "fail"},
                "tags": []
            }
        ]
    })

    os.environ['KORA_USE_RUST'] = '1'
    try:
        result = run_graph(graph)
    finally:
        os.environ.pop('KORA_USE_RUST', None)

    assert result["ok"] is False
    assert result["error"]["error_type"] == "BUDGET_BREACH"
    assert result["error"]["stage"] == "BUDGET"
    assert result["error"]["budget_breached"] is True
    assert result["error"]["task_id"] == "t1"
    assert "timed out" in result["error"]["details"]


def test_live_rust_executor_verification_fail_propagation():
    try:
        import kora_rust
    except ImportError:
        pytest.skip("kora_rust is not compiled/installed in this environment")

    graph = TaskGraph.model_validate({
        "graph_id": "verify-fail-graph",
        "version": "0.1",
        "root": "t1",
        "defaults": {
            "budget": {
                "max_time_ms": 1000,
                "max_tokens": 100,
                "max_retries": 0,
            }
        },
        "tasks": [
            {
                "id": "t1",
                "type": "det.echo",
                "deps": [],
                "in": {},
                "run": {
                    "kind": "det",
                    "spec": {
                        "handler": "echo",
                        "args": {"message": "hello"}
                    }
                },
                "verify": {
                    "schema": {
                        "type": "object",
                        "required": ["non_existent_field"]
                    },
                    "rules": []
                },
                "policy": {"on_fail": "fail"},
                "tags": []
            }
        ]
    })

    os.environ['KORA_USE_RUST'] = '1'
    try:
        result = run_graph(graph)
    finally:
        os.environ.pop('KORA_USE_RUST', None)

    assert result["ok"] is False
    assert result["error"]["error_type"] == "OUTPUT_SCHEMA_INVALID"
    assert result["error"]["stage"] == "VERIFY"
    assert result["error"]["task_id"] == "t1"
    assert "Schema validation failed" in result["error"]["details"]


def test_live_rust_executor_invalid_handler_propagation():
    try:
        import kora_rust
    except ImportError:
        pytest.skip("kora_rust is not compiled/installed in this environment")

    graph = TaskGraph.model_validate({
        "graph_id": "invalid-handler-graph",
        "version": "0.1",
        "root": "t1",
        "defaults": {
            "budget": {
                "max_time_ms": 1000,
                "max_tokens": 100,
                "max_retries": 0,
            }
        },
        "tasks": [
            {
                "id": "t1",
                "type": "det.non_existent",
                "deps": [],
                "in": {},
                "run": {
                    "kind": "det",
                    "spec": {
                        "handler": "non_existent",
                        "args": {}
                    }
                },
                "verify": None,
                "policy": {"on_fail": "fail"},
                "tags": []
            }
        ]
    })

    os.environ['KORA_USE_RUST'] = '1'
    try:
        result = run_graph(graph)
    finally:
        os.environ.pop('KORA_USE_RUST', None)

    assert result["ok"] is False
    assert result["error"]["error_type"] == "DETERMINISTIC_EXEC_FAILED"
    assert result["error"]["stage"] == "DETERMINISTIC"
    assert result["error"]["task_id"] == "t1"
    assert "Unknown deterministic handler" in result["error"]["details"]

