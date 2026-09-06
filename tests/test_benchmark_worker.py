import threading

import pytest

from kora.benchmarks.three_system import Client, arithmetic, execute_case
from kora.benchmarks.worker import (
    VERSION,
    ModelBackend,
    Worker,
    WorkerError,
    digest,
    http_json,
    make_server,
)

TOKEN = "t" * 40


def request(worker, job="j1", value=None):
    value = value or {"quantity": 2, "unit_price": 5, "currency": "KRW"}
    return {
        "schema_version": VERSION,
        "boot_id": worker.boot_id,
        "job_id": job,
        "operation": "arithmetic",
        "input": value,
        "input_hash": digest(value),
    }


def test_duplicates_conflicts_and_new_jobs():
    calls = []

    def calculate(value):
        calls.append(value)
        return arithmetic(value)

    worker = Worker("test", TOKEN, {"arithmetic": calculate}, capacity=2)
    first = worker.execute(request(worker))
    assert first["model_calls_completed"] == 0
    assert worker.execute(request(worker))["duplicate_delivery"]
    assert len(calls) == 1
    changed = request(worker, value={"quantity": 3, "unit_price": 5, "currency": "KRW"})
    with pytest.raises(WorkerError, match="job-id-conflict"):
        worker.execute(changed)
    worker.execute(request(worker, "j2"))
    assert len(calls) == 2
    with pytest.raises(WorkerError, match="ledger-full"):
        worker.execute(request(worker, "j3"))


def test_restart_and_hash_fail_closed():
    worker = Worker("test", TOKEN, {"arithmetic": arithmetic})
    r = request(worker)
    r["input"]["quantity"] = 3
    with pytest.raises(WorkerError, match="input-hash-mismatch"):
        worker.execute(r)
    other = Worker("test", TOKEN, {"arithmetic": arithmetic})
    with pytest.raises(WorkerError, match="worker-incarnation-mismatch"):
        other.execute(request(worker))


def test_failure_retained_no_repeat_inference():
    calls = []

    def fail(value):
        calls.append(value)
        raise WorkerError("transport-outcome-unknown")

    worker = Worker("test", TOKEN, {"model": fail})
    r = request(worker)
    r["operation"] = "model"
    result = worker.execute(r)
    assert result["status"] == "failed"
    assert result["model_calls_completed"] == 0
    assert result["model_execution_outcome"] == "unknown-or-not-started"
    assert worker.execute(r)["duplicate_delivery"]
    assert len(calls) == 1
    r["job_id"] = "new"
    with pytest.raises(WorkerError, match="model-recovery-required"):
        worker.execute(r)


def test_inflight_duplicate_does_not_execute_twice():
    entered, release = threading.Event(), threading.Event()

    def slow(value):
        entered.set()
        release.wait(3)
        return arithmetic(value)

    worker = Worker("test", TOKEN, {"arithmetic": slow})
    thread = threading.Thread(target=lambda: worker.execute(request(worker)))
    thread.start()
    assert entered.wait(2)
    try:
        with pytest.raises(WorkerError, match="job-in-progress"):
            worker.execute(request(worker))
        with pytest.raises(WorkerError, match="worker-busy"):
            worker.execute(request(worker, "j2"))
    finally:
        release.set()
        thread.join()


def test_authenticated_loopback_transport():
    worker = Worker("test", TOKEN, {"arithmetic": arithmetic})
    server = make_server(worker)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = "http://127.0.0.1:" + str(server.server_port)
    try:
        with pytest.raises(WorkerError, match="http-401"):
            http_json(url + "/health")
        client = Client(url, TOKEN, "test")
        result = client.run(
            "j1", "arithmetic", {"quantity": 3, "unit_price": 7, "currency": "KRW"}
        )
        assert result["output"]["total"] == 21
        with pytest.raises(WorkerError, match="worker-identity-mismatch"):
            Client(url, TOKEN, "different")
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize(
    "url", ["http://example.com", "https://127.0.0.1", "http://user@127.0.0.1"]
)
def test_non_loopback_endpoints_rejected(url):
    with pytest.raises(WorkerError, match="loopback-or-ssh-tunnel-required"):
        http_json(url)


def test_h100_model_mismatch_before_completion(monkeypatch):
    import kora.benchmarks.worker as module

    calls = []

    def fake(url, *args, **kwargs):
        calls.append(url)
        return {"data": [{"id": "other-model"}]}

    monkeypatch.setattr(module, "http_json", fake)
    backend = ModelBackend("http://127.0.0.1:1", "pinned-model", {}, {})
    with pytest.raises(WorkerError, match="model-mismatch"):
        backend.generate({"system": "system", "text": "text"})
    assert len(calls) == 1 and calls[0].endswith("/v1/models")


def test_model_counts_and_malformed_usage(monkeypatch):
    import kora.benchmarks.worker as module

    response = {
        "choices": [
            {"message": {"content": '{"category":"billing"}'}, "finish_reason": "stop"}
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 6},
    }

    def fake(url, *args, **kwargs):
        return {"data": [{"id": "pinned"}]} if url.endswith("/models") else response

    monkeypatch.setattr(module, "http_json", fake)
    backend = ModelBackend("http://127.0.0.1:1", "pinned", {}, {"revision": "test"})
    assert backend.generate({"system": "s", "text": "t"})["completion_tokens"] == 6
    response["usage"]["completion_tokens"] = None
    with pytest.raises(WorkerError, match="missing-engine-token-counts"):
        backend.generate({"system": "s", "text": "t"})


@pytest.mark.parametrize("quantity", [True, -1, 1.1, "2", 10**10])
def test_arithmetic_bounds(quantity):
    with pytest.raises(WorkerError):
        arithmetic({"quantity": quantity, "unit_price": 2, "currency": "KRW"})


def test_failed_quality_keeps_generated_counts(monkeypatch):
    monkeypatch.setattr(ModelBackend, "health", lambda self: {})
    monkeypatch.setattr(
        ModelBackend,
        "generate",
        lambda self, p: {"text": "invalid json", "completion_tokens": 3},
    )
    fixture = {
        "id": "f",
        "text": "t",
        "structured_input": {},
        "expected_model_output": {"category": "billing"},
    }
    events = []
    result = execute_case(
        "h100",
        {
            "backend": {
                "url": "http://127.0.0.1:1",
                "model": "x",
                "generation": {},
                "identity": {},
            }
        },
        fixture,
        "s",
        "M",
        "r",
        events.append,
    )
    assert result["status"] == "failed" and not result["quality_pass"]
    assert result["completion_tokens"] == 3 and result["model_calls_completed"] == 1
    assert [e["sequence"] for e in events] == list(range(1, len(events) + 1))


def test_http_body_limit_and_invalid_framing():
    from http.client import HTTPConnection

    worker = Worker("test", TOKEN, {"arithmetic": arithmetic})
    server = make_server(worker)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for headers, expected in [
            ({"Content-Length": "65537"}, 413),
            ({"Transfer-Encoding": "chunked"}, 400),
        ]:
            connection = HTTPConnection("127.0.0.1", server.server_port, timeout=2)
            connection.request(
                "POST", "/jobs", headers={"Authorization": "Bearer " + TOKEN, **headers}
            )
            response = connection.getresponse()
            assert response.status == expected
            response.read()
            connection.close()
        assert not worker.jobs
    finally:
        server.shutdown()
        server.server_close()


def test_three_system_contract_with_explicit_mock_models(monkeypatch):
    output = {"text": '{"category":"billing"}', "completion_tokens": 6}
    monkeypatch.setattr(ModelBackend, "health", lambda self: {})
    monkeypatch.setattr(ModelBackend, "generate", lambda self, payload: dict(output))
    monkeypatch.setenv("TEST_WORKER_TOKEN", TOKEN)
    servers = []
    try:
        refs = {}
        for name in ("mp", "a", "b"):
            worker = Worker(
                name, TOKEN, {"arithmetic": arithmetic, "model": lambda p: dict(output)}
            )
            server = make_server(worker)
            servers.append(server)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            refs[name] = {
                "url": "http://127.0.0.1:" + str(server.server_port),
                "worker_id": name,
            }
        config = {
            "mp": {
                "token_env": "TEST_WORKER_TOKEN",
                "model_worker": refs["mp"],
                "deterministic_worker": refs["mp"],
            },
            "cluster": {
                "token_env": "TEST_WORKER_TOKEN",
                "model_worker": refs["a"],
                "deterministic_worker": refs["b"],
            },
            "h100": {
                "backend": {
                    "url": "http://127.0.0.1:1",
                    "model": "mock",
                    "generation": {},
                    "identity": {"mock": True},
                }
            },
        }
        fixture = {
            "id": "f",
            "text": "fixture",
            "structured_input": {"quantity": 2, "unit_price": 5, "currency": "KRW"},
            "expected_deterministic_output": {"total": 10, "currency": "KRW"},
            "expected_model_output": {"category": "billing"},
        }
        rows = [
            execute_case(
                name, config[name], fixture, "system", "W", name, lambda e: None
            )
            for name in ("mp", "cluster", "h100")
        ]
        assert all(row["quality_pass"] for row in rows)
        assert len({row["input_hash"] for row in rows}) == 1
        assert all(row["model_calls_completed"] == 1 for row in rows)
        assert rows[1]["cluster_cooperation_observed"]
        deterministic = execute_case(
            "cluster", config["cluster"], fixture, "system", "D", "d", lambda e: None
        )
        assert deterministic["model_calls_completed"] == 0
        assert not deterministic["cluster_cooperation_observed"]
    finally:
        for server in servers:
            server.shutdown()
            server.server_close()
