from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from kora.solution import LocalSolutionHost, ReferenceRuntime, SolutionValidationError
from kora.solution.contracts import canonical_json_bytes, validate_contract_instance
from kora.solution.reference_runtime import RuntimeExecution

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples/solutions/typed-node-fixture"


class Normalize(ReferenceRuntime):
    runtime_id = "fixture.normalize"

    @property
    def capabilities(self):
        return frozenset({"text.normalize"})


class Echo(ReferenceRuntime):
    runtime_id = "fixture.echo"

    @property
    def capabilities(self):
        return frozenset({"det.echo"})


def package(tmp_path):
    p = tmp_path / "package"
    shutil.copytree(FIXTURE, p)
    return p


def refresh(p):
    manifest = json.loads((p / "solution.json").read_text())
    manifest["integrity"]["files"] = {
        f.relative_to(p).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
        for f in sorted(p.rglob("*"))
        if f.is_file() and f.name != "solution.json"
    }
    (p / "solution.json").write_bytes(canonical_json_bytes(manifest))


def change(p, filename, edit):
    path = p / filename
    value = json.loads(path.read_text())
    edit(value)
    path.write_bytes(canonical_json_bytes(value))
    refresh(p)


def run(host, p, payload=None, approvals=()):
    host.install(p)
    return host.run(
        "example.typed-node",
        payload or {"text": "  hello   world "},
        approvals=approvals,
    )


def evidence(host, result):
    value = json.loads(
        (host.runs_root / result["run_id"] / "node-evidence.json").read_text()
    )
    validate_contract_instance("node-evidence.schema.json", value)
    return value["nodes"]


def test_typed_output_crosses_two_runtime_boundaries_and_persists_identity(tmp_path):
    host = LocalSolutionHost(tmp_path / "store", runtimes=[Normalize(), Echo()])
    result = run(host, package(tmp_path))
    assert result["lifecycle_state"] == "succeeded"
    assert result["output"] == {"text": "hello world"}
    nodes = evidence(host, result)
    assert [n["runtime"]["id"] for n in nodes] == ["fixture.normalize", "fixture.echo"]
    assert all(
        n["state"] == "succeeded" and n["input_valid"] and n["output_valid"]
        for n in nodes
    )
    assert host.result(result["run_id"]) == result
    assert result["runtime"]["id"] == "kora.node-coordinator"
    assert not result["activity"]["model_inference_performed"]


def test_bound_dollar_string_remains_literal(tmp_path):
    host = LocalSolutionHost(tmp_path / "store", runtimes=[Normalize(), Echo()])
    result = run(host, package(tmp_path), {"text": "$.not_a_path"})
    assert result["output"] == {"text": "$.not_a_path"}


@pytest.mark.parametrize(
    "mode",
    [
        "nonancestor",
        "unknown_source",
        "external_schema",
        "wrong_version",
        "legacy_input",
        "overlap",
    ],
)
def test_invalid_node_contract_is_rejected_before_execution(tmp_path, mode):
    p = package(tmp_path)
    if mode == "legacy_input":
        change(
            p,
            "graph/workflow.json",
            lambda g: g["tasks"][0]["in"].update(text="$.text"),
        )
    else:

        def edit(plan):
            if mode == "nonancestor":
                plan["nodes"]["normalize"]["bindings"]["text"] = {
                    "source": "node",
                    "node": "echo",
                    "path": ["text"],
                }
            elif mode == "unknown_source":
                plan["nodes"]["echo"]["bindings"]["text"]["source"] = "auto"
            elif mode == "external_schema":
                plan["nodes"]["echo"]["input_schema"]["$ref"] = (
                    "https://invalid.example/schema"
                )
            elif mode == "wrong_version":
                plan["schema_version"] = "kora.node-execution/v99"
            else:
                plan["nodes"]["normalize"]["bindings"]["trim"] = {
                    "source": "input",
                    "path": ["text"],
                }

        change(p, "graph/execution.json", edit)
    host = LocalSolutionHost(tmp_path / "store", runtimes=[Normalize(), Echo()])
    with pytest.raises(SolutionValidationError):
        host.install(p)
    assert not list(host.runs_root.iterdir())


@pytest.mark.parametrize(
    "mode", ["missing", "input_type", "output_type", "exception", "wrong_evidence"]
)
def test_failed_node_never_invokes_downstream(tmp_path, mode):
    p = package(tmp_path)
    calls = []

    class Downstream(Echo):
        def execute(self, *args, **kwargs):
            calls.append("echo")
            return super().execute(*args, **kwargs)

    class Broken(Normalize):
        def execute(self, *args, **kwargs):
            if mode == "exception":
                raise RuntimeError("private details must not leak")
            if mode == "wrong_evidence":
                return RuntimeExecution(
                    output={"text": "ok"}, capabilities_executed=("det.echo",)
                )
            return super().execute(*args, **kwargs)

    if mode == "missing":
        change(
            p,
            "graph/execution.json",
            lambda q: q["nodes"]["normalize"]["bindings"]["text"].update(
                path=["absent"]
            ),
        )
    if mode == "input_type":
        change(
            p,
            "graph/execution.json",
            lambda q: q["nodes"]["normalize"]["input_schema"]["properties"][
                "text"
            ].update(type="integer"),
        )
    if mode == "output_type":
        change(
            p,
            "graph/execution.json",
            lambda q: q["nodes"]["normalize"]["output_schema"]["properties"][
                "text"
            ].update(type="integer"),
        )
    host = LocalSolutionHost(tmp_path / "store", runtimes=[Broken(), Downstream()])
    result = run(host, p)
    assert result["lifecycle_state"] == "failed"
    assert calls == []
    assert [n["state"] for n in evidence(host, result)] == ["failed", "skipped"]
    assert "private details" not in json.dumps(result)


def test_missing_approval_prevents_all_node_execution(tmp_path):
    p = package(tmp_path)
    change(p, "solution.json", lambda m: m["policy"].update(approvals=["human.review"]))
    host = LocalSolutionHost(tmp_path / "store", runtimes=[Normalize(), Echo()])
    result = run(host, p)
    assert result["error"]["code"] == "approval_required"
    assert not (host.runs_root / result["run_id"] / "node-evidence.json").exists()


def test_plan_integrity_cannot_be_omitted(tmp_path):
    p = package(tmp_path)
    m = json.loads((p / "solution.json").read_text())
    del m["integrity"]["files"]["graph/execution.json"]
    (p / "solution.json").write_bytes(canonical_json_bytes(m))
    with pytest.raises(SolutionValidationError):
        LocalSolutionHost(tmp_path / "store").install(p)


def test_installed_plan_tampering_rejected(tmp_path):
    p = package(tmp_path)
    host = LocalSolutionHost(tmp_path / "store", runtimes=[Normalize(), Echo()])
    host.install(p)
    installed = (
        host.installed_root / "example.typed-node/0.1.0/package/graph/execution.json"
    )
    installed.write_text("{}")
    result = host.run("example.typed-node", {"text": "hello"})
    assert result["error"]["code"] == "integrity_mismatch"


def test_ambiguity_in_later_node_prevents_install(tmp_path):
    from kora.solution import SolutionHostError

    class OtherEcho(Echo):
        runtime_id = "fixture.other"

    host = LocalSolutionHost(
        tmp_path / "store", runtimes=[Normalize(), Echo(), OtherEcho()]
    )
    with pytest.raises(SolutionHostError, match="same highest priority"):
        host.install(package(tmp_path))


def test_downstream_input_mismatch_keeps_upstream_success(tmp_path):
    p = package(tmp_path)
    change(
        p,
        "graph/execution.json",
        lambda q: q["nodes"]["echo"]["input_schema"]["properties"]["text"].update(
            type="integer"
        ),
    )
    calls = []

    class GuardedEcho(Echo):
        def execute(self, *args, **kwargs):
            calls.append(True)
            return super().execute(*args, **kwargs)

    host = LocalSolutionHost(tmp_path / "store", runtimes=[Normalize(), GuardedEcho()])
    result = run(host, p)
    assert result["lifecycle_state"] == "failed"
    assert calls == []
    assert [n["state"] for n in host.node_evidence(result["run_id"])["nodes"]] == [
        "succeeded",
        "failed",
    ]


def test_persisted_node_evidence_rejects_duplicate_ids(tmp_path):
    from kora.solution import SolutionHostError

    host = LocalSolutionHost(tmp_path / "store", runtimes=[Normalize(), Echo()])
    result = run(host, package(tmp_path))
    path = host.runs_root / result["run_id"] / "node-evidence.json"
    value = host.node_evidence(result["run_id"])
    value["nodes"][1]["node_id"] = value["nodes"][0]["node_id"]
    path.write_text(json.dumps(value))
    with pytest.raises(SolutionHostError, match="failed validation"):
        host.node_evidence(result["run_id"])


def test_registry_tampering_between_nodes_prevents_downstream(tmp_path):
    calls = []

    class Tamper(Normalize):
        def execute(self, *args, **kwargs):
            result = super().execute(*args, **kwargs)
            descriptor = (
                host.runtime_registry.root
                / "fixture.echo"
                / self.runtime_version
                / "runtime.json"
            )
            descriptor.write_text("{}")
            return result

    class GuardedEcho(Echo):
        def execute(self, *args, **kwargs):
            calls.append(True)
            return super().execute(*args, **kwargs)

    host = LocalSolutionHost(tmp_path / "store", runtimes=[Tamper(), GuardedEcho()])
    result = run(host, package(tmp_path))
    assert result["lifecycle_state"] == "failed"
    assert calls == []
    assert [n["state"] for n in host.node_evidence(result["run_id"])["nodes"]] == [
        "succeeded",
        "failed",
    ]
