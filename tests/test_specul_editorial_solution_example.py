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
    monkeypatch.delenv("KORA_OPENAI_API_KEY_FILE", raising=False)
    with pytest.raises(RuntimeError, match="OpenAI credential"):
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
    monkeypatch.delenv("KORA_OPENAI_API_KEY_FILE", raising=False)
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
    monkeypatch.delenv("KORA_OPENAI_API_KEY_FILE", raising=False)
    monkeypatch.setenv("KORA_OPENAI_MODEL","frontier-test")
    monkeypatch.setenv("KORA_LOCAL_OPENAI_RUNTIME_ID","local-runtime-test")
    monkeypatch.delenv("KORA_OPENAI_CACHE_ID",raising=False)
    with pytest.raises(RuntimeError,match="CACHE_ID"):
        m.adapters_for("kora-local-first")


def test_local_first_policy_has_bounded_routine_frontier_fallback():
    m=module()
    policy=m.POLICIES["kora-local-first"]
    assert policy.routes=={"routine":"local","frontier":"frontier"}
    assert policy.fallback_routes=={"routine":"frontier"}


def test_quality_repair_is_frontier_and_routine_nodes_stay_local_candidates():
    m=module()
    tiers={node.id:node.tier for node in m.NODES}
    assert {k for k,v in tiers.items() if v=="routine"}=={"claim_review"}
    assert {k for k,v in tiers.items() if v=="frontier"}=={"research","synthesis","draft","editorial_review","revision","quality_repair"}


def test_quality_gate_requires_bounded_words_chars_and_complete_ending():
    m=module()
    workload={"brief":{"quality_floor":{
        "min_article_chars":100,"max_article_chars":1000,
        "min_article_words":10,"max_article_words":100,
        "target_article_chars":500,"target_article_words":50,
        "required_source_ids":["S1"],
    }},"sources":[{"id":"S1","text":"x"}]}
    good_article=("word "*20)+"finished."
    good={"output":{"article":good_article,"claim_source_ids":["S1"],"resolved_findings":[]}}
    assert m.evaluate_quality(good,workload)["pass"] is True
    broken={"output":{"article":good_article[:-1],"claim_source_ids":["S1"],"resolved_findings":[]}}
    q=m.evaluate_quality(broken,workload)
    assert q["pass"] is False
    assert q["checks"]["complete_ending"] is False


def test_frontier_node_budgets_are_task_specific():
    m=module()
    budgets={node.id:node.max_tokens for node in m.NODES}
    assert budgets["research"]==1800
    assert budgets["synthesis"]==3500
    assert budgets["draft"]==5000
    assert budgets["claim_review"]==2500
    assert budgets["editorial_review"]==2500
    assert budgets["revision"]==5000
    assert budgets["quality_repair"]==5000


def test_quality_auto_uses_frontier_for_all_semantic_tiers_with_compact_context():
    m=module()
    p=m.POLICIES["kora-quality-auto"]
    assert p.routes=={"routine":"frontier","frontier":"frontier"}
    assert p.context_mode=="brief+deps"
    assert p.full_context_nodes==("draft",)
    assert p.exact_reuse is True
    assert p.fallback_routes is None


def test_kora_auto_uses_frontier_semantics_with_compact_context_and_reuse():
    m=module()
    policy=m.POLICIES["kora-auto"]
    assert policy.routes=={"routine":"frontier","frontier":"frontier"}
    assert policy.exact_reuse is True
    assert policy.context_mode=="brief+deps"
    assert policy.fallback_routes is None


def test_research_contract_allows_richer_bounded_evidence_density():
    m=module()
    research=next(node for node in m.NODES if node.id=="research")
    evidence=research.output_schema["properties"]["evidence"]
    assert evidence["minItems"]==1
    assert evidence["maxItems"]==24
    assert research.max_tokens==1800
