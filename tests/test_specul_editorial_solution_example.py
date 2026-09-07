import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
RUNNER = ROOT / "examples/solutions/specul-editorial-v1/run.py"


def module():
    spec = importlib.util.spec_from_file_location("specul_editorial_example", RUNNER)
    loaded = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(loaded)
    return loaded


def test_workload_loader_accepts_bounded_example():
    m = module()
    payload = m.load_workload(ROOT / "examples/solutions/specul-editorial-v1/workload.example.json")
    assert [item["id"] for item in payload["sources"]] == ["S1", "S2"]


def test_workload_loader_rejects_duplicate_source_ids(tmp_path):
    m = module()
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"brief": {}, "sources": [{"id": "S1", "text": "a"}, {"id": "S1", "text": "b"}]}))
    with pytest.raises(ValueError, match="unique"):
        m.load_workload(path)


def test_frontier_policy_fails_closed_without_byok(monkeypatch):
    m = module()
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        m.adapters_for("frontier-baseline")


def test_policy_contract_matches_public_template():
    m = module()
    template = json.loads((ROOT / "examples/solutions/specul-editorial-v1/workflow.json").read_text())
    assert [node.id for node in m.NODES] == [node["id"] for node in template["nodes"]]
    assert all(node.cacheable for node in m.NODES)
    assert all(node["cacheable"] for node in template["nodes"])


def test_nodes_bind_provenance_to_workload_source_ids():
    m=module()
    workload={"brief":{},"sources":[{"id":"S1","text":"a"},{"id":"S2","text":"b"}]}
    nodes={node.id:node for node in m.nodes_for(workload)}
    research=nodes["research"].output_schema["properties"]
    assert research["source_ids"]["items"]["enum"]==["S1","S2"]
    assert research["evidence"]["items"]["properties"]["source_id"]["enum"]==["S1","S2"]
    assert nodes["revision"].output_schema["properties"]["claim_source_ids"]["items"]["enum"]==["S1","S2"]


def test_frontier_policy_requires_explicit_model(monkeypatch):
    m=module()
    monkeypatch.setenv("OPENAI_API_KEY","test-only")
    monkeypatch.delenv("KORA_OPENAI_MODEL",raising=False)
    with pytest.raises(RuntimeError,match="KORA_OPENAI_MODEL"):
        m.adapters_for("frontier-baseline")


def test_local_exact_reuse_requires_runtime_identity(monkeypatch):
    m=module()
    monkeypatch.delenv("KORA_LOCAL_OPENAI_RUNTIME_ID",raising=False)
    with pytest.raises(RuntimeError,match="RUNTIME_ID"):
        m.adapters_for("local-control")


def test_local_first_requires_explicit_remote_cache_identity(monkeypatch):
    m=module()
    monkeypatch.setenv("OPENAI_API_KEY","test-only")
    monkeypatch.setenv("KORA_OPENAI_MODEL","frontier-test")
    monkeypatch.setenv("KORA_LOCAL_OPENAI_RUNTIME_ID","local-runtime-test")
    monkeypatch.delenv("KORA_OPENAI_CACHE_ID",raising=False)
    with pytest.raises(RuntimeError,match="CACHE_ID"):
        m.adapters_for("kora-local-first")
