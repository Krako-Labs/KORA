from kora.solution.economics import (
    EconomicsNode,
    ExecutionPolicy,
    WorkloadEconomicsRunner,
    compare_economics,
)


class FakeAdapter:
    def __init__(self,name): self.name=name; self.calls=0
    def run(self,*,task_id,input,budget,output_schema):
        self.calls+=1
        return {"ok":True,"output":{"task":task_id,"value":input["workload"].get("topic"),"deps":sorted(input["dependencies"])},"usage":{"time_ms":2,"tokens_in":10,"tokens_out":4},"meta":{"provider":self.name,"model":self.name,"model_calls":1}}


def runner():
    return WorkloadEconomicsRunner(nodes=(
        EconomicsNode("research","extract bounded evidence","routine"),
        EconomicsNode("draft","draft from evidence","frontier",("research",),cacheable=False),
        EconomicsNode("review","review the draft","routine",("draft",)),
    ),adapters={"local":FakeAdapter("local"),"frontier":FakeAdapter("frontier")})


def test_exact_repeat_reuses_cacheable_nodes_but_not_uncacheable_draft():
    r=runner(); p=ExecutionPolicy("kora",{"routine":"local","frontier":"frontier"},exact_reuse=True)
    first=r.run(workload={"topic":"a"},policy=p); second=r.run(workload={"topic":"a"},policy=p)
    assert first["model_calls"]==3
    assert second["model_calls"]==1
    assert second["exact_reuse_hits"]==2


def test_changed_input_invalidates_exact_reuse():
    r=runner(); p=ExecutionPolicy("kora",{"routine":"local","frontier":"frontier"},exact_reuse=True)
    r.run(workload={"topic":"a"},policy=p); changed=r.run(workload={"topic":"b"},policy=p)
    assert changed["model_calls"]==3
    assert changed["exact_reuse_hits"]==0


def test_compare_is_arithmetic_not_claim_language():
    a={"policy":"baseline","model_calls":10,"tokens_in":100,"tokens_out":50}
    b={"policy":"kora","model_calls":5,"tokens_in":60,"tokens_out":30,"exact_reuse_hits":2}
    c=compare_economics(a,b)
    assert c["model_call_reduction_percent"]==50.0
    assert c["input_token_reduction_percent"]==40.0


def test_brief_plus_deps_reduces_downstream_context_without_changing_first_node():
    class SizeAdapter(FakeAdapter):
        def run(self,*,task_id,input,budget,output_schema):
            import json
            self.calls+=1
            size=len(json.dumps(input,sort_keys=True))
            return {"ok":True,"output":{"task":task_id,"size":size},"usage":{"time_ms":1,"tokens_in":size,"tokens_out":1},"meta":{"provider":self.name,"model":self.name,"model_calls":1}}
    nodes=(EconomicsNode("research","r","routine"),EconomicsNode("draft","d","frontier",("research",),cacheable=False))
    workload={"brief":{"topic":"x"},"sources":[{"text":"z"*1000}]}
    full=WorkloadEconomicsRunner(nodes=nodes,adapters={"a":SizeAdapter("a")}).run(workload=workload,policy=ExecutionPolicy("full",{"routine":"a","frontier":"a"},context_mode="full"))
    compact=WorkloadEconomicsRunner(nodes=nodes,adapters={"a":SizeAdapter("a")}).run(workload=workload,policy=ExecutionPolicy("compact",{"routine":"a","frontier":"a"},context_mode="brief+deps"))
    assert compact["tokens_in"] < full["tokens_in"]


def test_invalid_adapter_output_fails_closed_before_cache():
    class BadAdapter(FakeAdapter):
        def run(self,*,task_id,input,budget,output_schema):
            return {"ok":True,"output":{"wrong":1},"usage":{"time_ms":1,"tokens_in":1,"tokens_out":1},"meta":{"provider":"bad","model":"bad","model_calls":1}}
    schema={"type":"object","properties":{"answer":{"type":"string"}},"required":["answer"],"additionalProperties":False}
    r=WorkloadEconomicsRunner(nodes=(EconomicsNode("n","x","routine",output_schema=schema),),adapters={"bad":BadAdapter("bad")})
    import pytest
    with pytest.raises(RuntimeError,match="output schema failed closed"):
        r.run(workload={"brief":{}},policy=ExecutionPolicy("p",{"routine":"bad","frontier":"bad"},exact_reuse=True))
    assert r.cache.memory == {}


def test_model_identity_change_invalidates_exact_reuse():
    class IdentityAdapter(FakeAdapter):
        def cache_identity(self):
            return {"model": self.name}
    a=IdentityAdapter("model-a")
    r=WorkloadEconomicsRunner(nodes=(EconomicsNode("n","x","routine"),),adapters={"local":a})
    policy=ExecutionPolicy("p",{"routine":"local","frontier":"local"},exact_reuse=True)
    first=r.run(workload={"brief":{"x":1}},policy=policy)
    assert first["model_calls"]==1
    r.adapters["local"]=IdentityAdapter("model-b")
    second=r.run(workload={"brief":{"x":1}},policy=policy)
    assert second["model_calls"]==1
    assert second["exact_reuse_hits"]==0


def test_output_contract_change_invalidates_exact_reuse():
    adapter=FakeAdapter("same")
    node=EconomicsNode("n","x","routine")
    r=WorkloadEconomicsRunner(nodes=(node,),adapters={"local":adapter})
    policy=ExecutionPolicy("p",{"routine":"local","frontier":"local"},exact_reuse=True)
    r.run(workload={"brief":{"x":1}},policy=policy)
    changed=EconomicsNode("n","x","routine",max_tokens=513)
    r.nodes=(changed,)
    second=r.run(workload={"brief":{"x":1}},policy=policy)
    assert second["model_calls"]==1
    assert second["exact_reuse_hits"]==0


def test_persistent_exact_reuse_survives_runner_restart(tmp_path):
    node=EconomicsNode("n","x","routine")
    policy=ExecutionPolicy("p",{"routine":"local","frontier":"local"},exact_reuse=True)
    first_adapter=FakeAdapter("same")
    first=WorkloadEconomicsRunner(nodes=(node,),adapters={"local":first_adapter},cache_directory=tmp_path)
    a=first.run(workload={"brief":{"x":1}},policy=policy)
    assert a["model_calls"]==1
    second_adapter=FakeAdapter("same")
    second=WorkloadEconomicsRunner(nodes=(node,),adapters={"local":second_adapter},cache_directory=tmp_path)
    b=second.run(workload={"brief":{"x":1}},policy=policy)
    assert b["model_calls"]==0
    assert b["exact_reuse_hits"]==1
    assert second_adapter.calls==0


def test_corrupt_persistent_entry_is_not_reused(tmp_path):
    node=EconomicsNode("n","x","routine")
    policy=ExecutionPolicy("p",{"routine":"local","frontier":"local"},exact_reuse=True)
    first=WorkloadEconomicsRunner(nodes=(node,),adapters={"local":FakeAdapter("same")},cache_directory=tmp_path)
    first.run(workload={"brief":{"x":1}},policy=policy)
    path=next(tmp_path.glob("*.json"))
    path.write_text('{"schema_version":"kora.exact-result/v1","key":"bad"}')
    adapter=FakeAdapter("same")
    second=WorkloadEconomicsRunner(nodes=(node,),adapters={"local":adapter},cache_directory=tmp_path)
    result=second.run(workload={"brief":{"x":1}},policy=policy)
    assert result["model_calls"]==1
    assert result["exact_reuse_hits"]==0


def test_openai_cache_identity_requires_explicit_cache_id(monkeypatch):
    from kora.adapters.openai_adapter import OpenAIAdapter
    monkeypatch.delenv("KORA_OPENAI_CACHE_ID",raising=False)
    adapter=OpenAIAdapter(model="frontier-test")
    import pytest
    with pytest.raises(RuntimeError,match="CACHE_ID"):
        adapter.cache_identity()
    monkeypatch.setenv("KORA_OPENAI_CACHE_ID","frontier-test-snapshot")
    assert adapter.cache_identity()["cache_id"]=="frontier-test-snapshot"


def test_openai_api_key_file_configuration(tmp_path, monkeypatch):
    from kora.adapters.openai_adapter import (
        _openai_api_key_from_environment,
        openai_api_key_configured,
    )
    key_file=tmp_path/"openai.key"
    key_file.write_text("test-key-value")
    env={"KORA_OPENAI_API_KEY_FILE":str(key_file)}
    assert openai_api_key_configured(env) is True
    assert _openai_api_key_from_environment(env)=="test-key-value"


def test_openai_api_key_sources_are_mutually_exclusive(tmp_path):
    import pytest

    from kora.adapters.openai_adapter import _openai_api_key_from_environment
    key_file=tmp_path/"openai.key"
    key_file.write_text("file-key")
    with pytest.raises(ValueError,match="either"):
        _openai_api_key_from_environment({
            "OPENAI_API_KEY":"direct-key",
            "KORA_OPENAI_API_KEY_FILE":str(key_file),
        })


def test_local_failure_escalates_to_frontier_and_records_event():
    class FailingAdapter(FakeAdapter):
        def cache_identity(self):
            return {"model": "local-fail"}
        def run(self,*,task_id,input,budget,output_schema):
            self.calls+=1
            raise RuntimeError("bounded local failure")
    class FrontierAdapter(FakeAdapter):
        def cache_identity(self):
            return {"model": "frontier-ok"}
    local=FailingAdapter("local")
    frontier=FrontierAdapter("frontier")
    r=WorkloadEconomicsRunner(
        nodes=(EconomicsNode("n","x","routine"),),
        adapters={"local":local,"frontier":frontier},
    )
    policy=ExecutionPolicy(
        "local-first",
        {"routine":"local","frontier":"frontier"},
        fallback_routes={"routine":"frontier"},
    )
    result=r.run(workload={"brief":{}},policy=policy)
    assert local.calls==1
    assert frontier.calls==1
    assert result["escalations"]==1
    assert result["events"][0]["route"]=="frontier"
    assert result["events"][0]["escalated"] is True
    assert result["events"][0]["primary_error_class"]=="RuntimeError"


def test_fallback_identity_change_invalidates_exact_reuse():
    class IdentityAdapter(FakeAdapter):
        def cache_identity(self):
            return {"model": self.name}
    node=EconomicsNode("n","x","routine")
    local=IdentityAdapter("local-v1")
    r=WorkloadEconomicsRunner(
        nodes=(node,),
        adapters={"local":local,"frontier":IdentityAdapter("frontier-v1")},
    )
    policy=ExecutionPolicy(
        "p",
        {"routine":"local","frontier":"frontier"},
        exact_reuse=True,
        fallback_routes={"routine":"frontier"},
    )
    first=r.run(workload={"brief":{"x":1}},policy=policy)
    assert first["model_calls"]==1
    r.adapters["frontier"]=IdentityAdapter("frontier-v2")
    second=r.run(workload={"brief":{"x":1}},policy=policy)
    assert second["model_calls"]==1
    assert second["exact_reuse_hits"]==0


def test_fallback_enabled_persistent_repeat_reuses_without_model_calls(tmp_path):
    class IdentityAdapter(FakeAdapter):
        def cache_identity(self):
            return {"model": self.name}
    node=EconomicsNode("n","x","routine")
    policy=ExecutionPolicy(
        "p",
        {"routine":"local","frontier":"frontier"},
        exact_reuse=True,
        fallback_routes={"routine":"frontier"},
    )
    first=WorkloadEconomicsRunner(
        nodes=(node,),
        adapters={"local":IdentityAdapter("local"),"frontier":IdentityAdapter("frontier")},
        cache_directory=tmp_path,
    )
    assert first.run(workload={"brief":{"x":1}},policy=policy)["model_calls"]==1
    second_local=IdentityAdapter("local")
    second_frontier=IdentityAdapter("frontier")
    second=WorkloadEconomicsRunner(
        nodes=(node,),
        adapters={"local":second_local,"frontier":second_frontier},
        cache_directory=tmp_path,
    )
    result=second.run(workload={"brief":{"x":1}},policy=policy)
    assert result["model_calls"]==0
    assert result["exact_reuse_hits"]==1
    assert second_local.calls==0
    assert second_frontier.calls==0


def test_openai_strict_structured_parser_rejects_incomplete_json():
    import pytest

    from kora.adapters.openai_adapter import OpenAIAdapter
    assert OpenAIAdapter._parse_structured_text_output('{"ok":true}')=={"ok":True}
    with pytest.raises(ValueError,match="invalid or incomplete"):
        OpenAIAdapter._parse_structured_text_output('{"ok":')


def test_openai_cache_identity_binds_contract_and_prompt_cache_mode(monkeypatch):
    from kora.adapters.openai_adapter import OpenAIAdapter
    monkeypatch.setenv("KORA_OPENAI_CACHE_ID","snapshot-test")
    monkeypatch.setenv("KORA_OPENAI_DISABLE_PROMPT_CACHE","1")
    identity=OpenAIAdapter(model="frontier-test").cache_identity()
    assert identity["contract_version"]=="openai-responses/v2-strict-structured"
    assert identity["provider_prompt_cache_disabled"] is True


def test_selective_full_context_node_keeps_sources_only_where_declared():
    class InspectAdapter(FakeAdapter):
        def __init__(self,name): super().__init__(name); self.seen={}
        def run(self,*,task_id,input,budget,output_schema):
            self.seen[task_id]=input["workload"]
            return super().run(task_id=task_id,input=input,budget=budget,output_schema=output_schema)
    a=InspectAdapter("a")
    nodes=(
        EconomicsNode("research","r","routine"),
        EconomicsNode("draft","d","frontier",("research",)),
        EconomicsNode("review","v","frontier",("draft",)),
    )
    r=WorkloadEconomicsRunner(nodes=nodes,adapters={"a":a})
    p=ExecutionPolicy("p",{"routine":"a","frontier":"a"},context_mode="brief+deps",full_context_nodes=("draft",))
    r.run(workload={"brief":{"x":1},"sources":[{"text":"evidence"}]},policy=p)
    assert "sources" in a.seen["research"]
    assert "sources" in a.seen["draft"]
    assert "sources" not in a.seen["review"]
