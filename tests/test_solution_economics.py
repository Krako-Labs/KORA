import pytest

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
    assert first["adapter_attempts"] == 3
    assert second["adapter_attempts"] == 1
    assert [event["adapter_attempts"] for event in second["events"]] == [0, 1, 0]
    assert sum(adapter.calls for adapter in r.adapters.values()) == 4


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


def test_route_policy_rollback_and_shared_dependency_replay(tmp_path):
    class PricingAdapter:
        def run(self, *, task_id, input, budget, output_schema):
            if task_id == "catalog":
                output = input["workload"]["catalog"]
            elif task_id == "quote":
                output = input["dependencies"]
            else:
                catalog = input["dependencies"]["catalog"]
                units = {"single": 1, "pair": 2, "triple": 3}[input["instruction"]]
                output = {"revision": catalog["revision"], "price": units * catalog["unit_price"]}
            return {"ok": True, "output": output}

    def replay(route_a_policy, revision, unit_price):
        nodes = (
            EconomicsNode("catalog", "read catalog", "routine"),
            EconomicsNode("route_a", route_a_policy, "routine", ("catalog",)),
            EconomicsNode("route_b", "pair", "routine", ("catalog",)),
            EconomicsNode("quote", "collect quotes", "routine", ("route_a", "route_b"), cacheable=False),
        )
        runner = WorkloadEconomicsRunner(
            nodes=nodes, adapters={"fixture": PricingAdapter()}, cache_directory=tmp_path
        )
        policy = ExecutionPolicy(
            "quotes", {"routine": "fixture"}, exact_reuse=True, context_mode="brief+deps"
        )
        # Only the upstream node sees the catalog directly.
        workload = {"brief": {}, "catalog": {"revision": revision, "unit_price": unit_price}}
        result = runner.run(workload=workload, policy=policy)
        reused = {event["node_id"] for event in result["events"] if event["reused"]}
        return result["output"], reused

    cold, hits = replay("single", "v1", 10)
    assert hits == set()
    assert cold == {
        "route_a": {"revision": "v1", "price": 10},
        "route_b": {"revision": "v1", "price": 20},
    }

    changed, hits = replay("triple", "v1", 10)
    assert hits == {"catalog", "route_b"}
    assert changed == {"route_a": {"revision": "v1", "price": 30}, "route_b": cold["route_b"]}

    rolled_back, hits = replay("single", "v1", 10)
    assert hits == {"catalog", "route_a", "route_b"}
    assert rolled_back == cold

    revised, hits = replay("single", "v2", 10)
    assert hits == set()
    assert revised == {
        "route_a": {"revision": "v2", "price": 10},
        "route_b": {"revision": "v2", "price": 20},
    }

    repriced, hits = replay("single", "v3", 12)
    assert hits == set()
    assert repriced == {
        "route_a": {"revision": "v3", "price": 12},
        "route_b": {"revision": "v3", "price": 24},
    }


def test_misspelled_full_context_node_is_rejected_before_dispatch_and_cache():
    import pytest

    class AmountAdapter(FakeAdapter):
        def run(self, *, task_id, input, budget, output_schema):
            self.calls += 1
            output = ({"constant": True} if task_id == "read"
                      else {"amount": input["workload"].get("order", {}).get("amount", 0)})
            return {"ok": True, "output": output}

    adapter = AmountAdapter("fixture")
    r = WorkloadEconomicsRunner(
        nodes=(EconomicsNode("read", "read constant", "routine"),
               EconomicsNode("explain", "include amount", "routine", ("read",))),
        adapters={"fixture": adapter},
    )
    def policy(names):
        return ExecutionPolicy("p", {"routine": "fixture"}, exact_reuse=True,
                               context_mode="brief+deps", full_context_nodes=names)

    valid = policy(("explain",))
    for amount in (5, 10):
        result = r.run(workload={"brief": {}, "order": {"amount": amount}}, policy=valid)
        assert result["output"] == {"amount": amount}
        assert result["exact_reuse_hits"] == 0
    warm_cache = dict(r.cache.memory)
    calls = adapter.calls
    for bad in (("exlpain",), ("explain", "missing"), "explain", (None,), ("",)):
        with pytest.raises(ValueError, match="full_context_nodes"):
            r.run(workload={"brief": {}, "order": {"amount": 5}}, policy=policy(bad))
        assert adapter.calls == calls
        assert r.cache.memory == warm_cache
    assert r.run(workload={"brief": {}, "order": {"amount": 5}}, policy=valid)["exact_reuse_hits"] == 2


def test_escalation_result_does_not_mask_primary_recovery():
    class RecoveryAdapter(FakeAdapter):
        def __init__(self, name, failure):
            super().__init__(name)
            self.failure = failure

        def cache_identity(self):
            return {"name": self.name}

        def run(self, *, task_id, input, budget, output_schema):
            self.calls += 1
            if self.failure == "exception":
                raise RuntimeError("temporary failure")
            if self.failure == "not_ok":
                return {"ok": False}
            return {"ok": True, "output": {"source": self.name}}

    for failure in ("exception", "not_ok"):
        primary = RecoveryAdapter("primary", failure)
        secondary = RecoveryAdapter("secondary", None)
        runner = WorkloadEconomicsRunner(
            nodes=(EconomicsNode("read", "read", "routine"),),
            adapters={"primary": primary, "secondary": secondary},
        )
        policy = ExecutionPolicy("p", {"routine": "primary"}, exact_reuse=True,
                                 fallback_routes={"routine": "secondary"})
        work = {"brief": {"id": "a"}}
        first = runner.run(workload=work, policy=policy)
        assert first["output"] == {"source": "secondary"}
        assert first["events"][0]["route"] == "secondary"
        assert first["escalations"] == 1
        assert first["adapter_attempts"] == first["events"][0]["adapter_attempts"] == 2
        assert first["model_calls"] == 1
        assert not runner.cache.memory

        primary.failure = None
        second = runner.run(workload=work, policy=policy)
        assert second["output"] == {"source": "primary"}
        assert second["events"][0]["route"] == "primary"
        assert second["exact_reuse_hits"] == 0
        assert primary.calls == 2 and secondary.calls == 1
        assert second["adapter_attempts"] == second["events"][0]["adapter_attempts"] == 1

        third = runner.run(workload=work, policy=policy)
        assert third["output"] == second["output"]
        assert third["exact_reuse_hits"] == 1
        assert third["adapter_attempts"] == third["events"][0]["adapter_attempts"] == 0
        assert primary.calls == 2 and secondary.calls == 1


def test_legacy_fallback_enabled_cache_key_is_not_reused(tmp_path):
    import hashlib
    from kora.solution.contracts import canonical_json_bytes

    node = EconomicsNode("read", "read", "routine")
    primary = FakeAdapter("primary")
    secondary = FakeAdapter("secondary")
    runner = WorkloadEconomicsRunner(
        nodes=(node,), adapters={"primary": primary, "secondary": secondary},
        cache_directory=tmp_path,
    )
    work = {"brief": {"topic": "a"}}
    payload = {"instruction": node.instruction, "quality_contract": {},
               "workload": work, "dependencies": {}}
    # The previous key had no result-source discriminator and could contain
    # either primary or fallback output.
    old_bound = {
        "node": {"id": node.id, "instruction": node.instruction, "tier": node.tier,
                 "deps": [], "max_tokens": node.max_tokens,
                 "output_schema": {"type": "object"}},
        "adapter": runner._adapter_identity("primary", primary),
        "fallback_adapter": runner._adapter_identity("secondary", secondary),
        "payload": payload,
    }
    old_key = hashlib.sha256(canonical_json_bytes(old_bound)).hexdigest()
    runner.cache.put(old_key, {"source": "unknown"})
    policy = ExecutionPolicy("p", {"routine": "primary"}, exact_reuse=True,
                             fallback_routes={"routine": "secondary"})
    result = runner.run(workload=work, policy=policy)
    assert result["exact_reuse_hits"] == 0
    assert result["output"] != {"source": "unknown"}
    assert primary.calls == 1 and secondary.calls == 0
    assert runner.run(workload=work, policy=policy)["exact_reuse_hits"] == 1


def test_compare_adapter_attempts_preserves_unknown_and_zero_baseline():
    base = {"model_calls": 7, "adapter_attempts": 11}
    other = {"model_calls": 7, "adapter_attempts": 7}
    result = compare_economics(base, other)
    assert result["baseline_adapter_attempts"] == 11
    assert result["kora_adapter_attempts"] == 7
    assert result["adapter_attempt_reduction_percent"] == 36.3636
    assert result["model_call_reduction_percent"] == 0.0
    assert compare_economics(base, {"adapter_attempts": 0})["adapter_attempt_reduction_percent"] == 100.0
    assert compare_economics({"adapter_attempts": 0}, other)["adapter_attempt_reduction_percent"] is None
    for invalid in (None, True, False, -1, 1.0, "7", [], {}):
        for left, right in ((base, {"adapter_attempts": invalid}), ({"adapter_attempts": invalid}, other)):
            assert compare_economics(left, right)["adapter_attempt_reduction_percent"] is None
    assert compare_economics(base, {})["kora_adapter_attempts"] is None
    assert compare_economics({}, other)["baseline_adapter_attempts"] is None
    assert compare_economics({}, {})["adapter_attempt_reduction_percent"] is None


def test_unrepresentable_adapter_attempt_percentage_preserves_raw_counters():
    large = 10**400
    result = compare_economics({"adapter_attempts": 1}, {"adapter_attempts": large})
    assert result["baseline_adapter_attempts"] == 1
    assert result["kora_adapter_attempts"] == large
    assert result["adapter_attempt_reduction_percent"] is None
    assert compare_economics({"adapter_attempts": large}, {"adapter_attempts": large * 2})[
        "adapter_attempt_reduction_percent"
    ] == -100.0


def test_deterministic_adapter_preserves_explicit_zero_model_calls():
    class DeterministicAdapter(FakeAdapter):
        def run(self, **kwargs):
            result = super().run(**kwargs)
            result["meta"]["model_calls"] = 0
            return result

    adapter = DeterministicAdapter("deterministic")
    r = WorkloadEconomicsRunner(
        nodes=(EconomicsNode("lookup", "read", "routine"),),
        adapters={"deterministic": adapter},
    )
    policy = ExecutionPolicy("test", {"routine": "deterministic"}, exact_reuse=True)
    first = r.run(workload={"brief": {}}, policy=policy)
    repeat = r.run(workload={"brief": {}}, policy=policy)
    assert first["adapter_attempts"] == 1
    assert first["model_calls"] == first["events"][0]["model_calls"] == 0
    assert repeat["adapter_attempts"] == repeat["model_calls"] == 0
    assert repeat["exact_reuse_hits"] == adapter.calls == 1


def test_legacy_absent_null_and_false_model_calls_keep_default():
    class LegacyAdapter(FakeAdapter):
        def __init__(self, value):
            super().__init__("legacy")
            self.value = value

        def run(self, **kwargs):
            result = super().run(**kwargs)
            if self.value == "absent":
                del result["meta"]["model_calls"]
            else:
                result["meta"]["model_calls"] = self.value
            return result

    for value in ("absent", None, False, 2):
        r = WorkloadEconomicsRunner(
            nodes=(EconomicsNode("lookup", "read", "routine"),),
            adapters={"legacy": LegacyAdapter(value)},
        )
        result = r.run(workload={}, policy=ExecutionPolicy("test", {"routine": "legacy"}))
        assert result["model_calls"] == (2 if value == 2 else 1)
        assert result["adapter_attempts"] == 1


def test_deterministic_fallback_reports_zero_model_calls_not_zero_attempts():
    class FailedAdapter(FakeAdapter):
        def run(self, **kwargs):
            self.calls += 1
            return {"ok": False}

    class DeterministicAdapter(FakeAdapter):
        def run(self, **kwargs):
            result = super().run(**kwargs)
            result["meta"]["model_calls"] = 0
            return result

    primary = FailedAdapter("primary")
    fallback = DeterministicAdapter("fallback")
    r = WorkloadEconomicsRunner(
        nodes=(EconomicsNode("lookup", "read", "routine"),),
        adapters={"primary": primary, "fallback": fallback},
    )
    policy = ExecutionPolicy(
        "test", {"routine": "primary"}, fallback_routes={"routine": "fallback"},
    )
    result = r.run(workload={}, policy=policy)
    assert result["adapter_attempts"] == 2
    assert result["model_calls"] == result["events"][0]["model_calls"] == 0
    assert primary.calls == fallback.calls == 1


def test_invalid_later_route_is_rejected_before_any_dispatch_or_cache_write():
    import pytest

    cases = (
        ({"routine": "local"}, None, "policy route"),
        ({"routine": "local", "frontier": "missing"}, None, "policy route"),
        ({"routine": "local", "frontier": "frontier"}, {"frontier": "missing"}, "policy fallback route"),
        ({"routine": "local", "frontier": "frontier"}, {"frontier": "frontier"}, "policy fallback route"),
    )
    for routes, fallback, message in cases:
        r = runner()
        valid = ExecutionPolicy("valid", {"routine": "local", "frontier": "frontier"}, exact_reuse=True)
        r.run(workload={"topic": "warm"}, policy=valid)
        before = sum(adapter.calls for adapter in r.adapters.values())
        cached = dict(r.cache.memory)
        for reuse in (False, True):
            invalid = ExecutionPolicy("invalid", routes, exact_reuse=reuse, fallback_routes=fallback)
            with pytest.raises(ValueError, match=message):
                r.run(workload={"topic": "cold"}, policy=invalid)
            assert sum(adapter.calls for adapter in r.adapters.values()) == before
            assert r.cache.memory == cached
        assert r.run(workload={"topic": "warm"}, policy=valid)["exact_reuse_hits"] == 2


@pytest.mark.parametrize("key,metric", [
    ("model_calls", "model_call_reduction_percent"),
    ("tokens_in", "input_token_reduction_percent"),
    ("tokens_out", "output_token_reduction_percent"),
])
def test_economics_reductions_require_observed_nonnegative_integer_counters(key, metric):
    assert compare_economics({key: 10}, {key: 0})[metric] == 100.0
    assert compare_economics({key: 10}, {key: 4})[metric] == 60.0
    assert compare_economics({key: 10}, {key: 20})[metric] == -100.0
    assert compare_economics({key: 0}, {key: 4})[metric] is None
    for invalid in ({}, *({key: value} for value in (None, True, False, -1, 1.5, "7", [], {}))):
        assert compare_economics({key: 10}, invalid)[metric] is None
        assert compare_economics(invalid, {key: 4})[metric] is None
    assert compare_economics({key: 1}, {key: 10**400})[metric] is None
    assert compare_economics({key: 10**400}, {key: 2 * 10**400})[metric] == -100.0


@pytest.mark.parametrize("reuse,cacheable", [(False, True), (True, False), (False, False)])
@pytest.mark.parametrize("primary_fails", [False, True])
def test_noncached_node_does_not_require_fallback_cache_identity(reuse, cacheable, primary_fails):
    class Fixture(FakeAdapter):
        def __init__(self, name, fail=False):
            super().__init__(name)
            self.fail = fail
            self.identity_calls = 0

        def cache_identity(self):
            self.identity_calls += 1
            raise RuntimeError("fixture cache identity unavailable")

        def run(self, **kwargs):
            self.calls += 1
            return {"ok": not self.fail, "output": {"source": self.name},
                    "meta": {"model_calls": 0}}

    primary = Fixture("primary", primary_fails)
    fallback = Fixture("fallback")
    r = WorkloadEconomicsRunner(
        nodes=(EconomicsNode("n", "read", "routine", cacheable=cacheable),),
        adapters={"primary": primary, "fallback": fallback},
    )
    policy = ExecutionPolicy("test", {"routine": "primary"}, exact_reuse=reuse,
                             fallback_routes={"routine": "fallback"})
    for _ in range(2):
        result = r.run(workload={}, policy=policy)
        assert result["output"] == {"source": "fallback" if primary_fails else "primary"}
        assert result["adapter_attempts"] == (2 if primary_fails else 1)
        assert result["model_calls"] == result["exact_reuse_hits"] == 0
    assert primary.calls == 2 and fallback.calls == (2 if primary_fails else 0)
    assert primary.identity_calls == fallback.identity_calls == 0
    assert not r.cache.memory


def test_cached_node_still_requires_fallback_identity_before_dispatch():
    class MissingIdentity(FakeAdapter):
        def cache_identity(self):
            raise RuntimeError("fixture cache identity unavailable")

    primary = FakeAdapter("primary")
    fallback = MissingIdentity("fallback")
    r = WorkloadEconomicsRunner(
        nodes=(EconomicsNode("n", "read", "routine"),),
        adapters={"primary": primary, "fallback": fallback},
    )
    with pytest.raises(RuntimeError, match="fixture cache identity unavailable"):
        r.run(workload={}, policy=ExecutionPolicy("test", {"routine": "primary"},
              exact_reuse=True, fallback_routes={"routine": "fallback"}))
    assert primary.calls == fallback.calls == 0
    assert not r.cache.memory


@pytest.mark.parametrize("persistent", [False, True])
@pytest.mark.parametrize("field", ["model_calls", "tokens_in", "tokens_out", "time_ms"])
def test_failed_receipt_does_not_publish_node_cache(tmp_path, persistent, field):
    class RecoveringAdapter(FakeAdapter):
        def run(self, **kwargs):
            result = super().run(**kwargs)
            result["output"]["attempt"] = self.calls
            if self.calls == 1:
                section = "meta" if field == "model_calls" else "usage"
                result[section][field] = "malformed"
            return result

    adapter = RecoveringAdapter("fixture")
    r = WorkloadEconomicsRunner(
        nodes=(EconomicsNode("n", "read", "routine"),),
        adapters={"fixture": adapter},
        cache_directory=tmp_path if persistent else None,
    )
    p = ExecutionPolicy("p", {"routine": "fixture"}, exact_reuse=True)
    with pytest.raises(ValueError):
        r.run(workload={}, policy=p)
    assert not r.cache.memory
    assert not list(tmp_path.glob("*.json"))

    retry = r.run(workload={}, policy=p)
    repeat = r.run(workload={}, policy=p)
    assert retry["output"]["attempt"] == repeat["output"]["attempt"] == 2
    assert retry["adapter_attempts"] == 1
    assert repeat["adapter_attempts"] == 0
    assert repeat["exact_reuse_hits"] == 1
    assert adapter.calls == 2


@pytest.mark.parametrize("field,value", [
    ("model_calls", 0.5), ("model_calls", -1), ("model_calls", True),
    ("tokens_in", 0.5), ("tokens_in", -1), ("tokens_out", True),
    ("cached_tokens_in", -1), ("cache_write_tokens_in", 0.5),
    ("reasoning_tokens_out", -1), ("time_ms", -1),
])
def test_invalid_explicit_economics_counters_fail_before_cache(field, value):
    class InvalidCounterAdapter(FakeAdapter):
        def run(self, **kwargs):
            result = super().run(**kwargs)
            result["meta" if field == "model_calls" else "usage"][field] = value
            return result

    adapter = InvalidCounterAdapter("fixture")
    r = WorkloadEconomicsRunner(nodes=(EconomicsNode("n", "read", "routine"),),
                                adapters={"fixture": adapter})
    p = ExecutionPolicy("p", {"routine": "fixture"}, exact_reuse=True)
    with pytest.raises(ValueError, match=field):
        r.run(workload={}, policy=p)
    assert not r.cache.memory
    assert adapter.calls == 1


@pytest.mark.parametrize('failure', ['raise', 'not_ok'])
@pytest.mark.parametrize('reuse', [False, True])
def test_fallback_receives_original_input_and_schema(failure, reuse):
    class Primary:
        def run(self, *, task_id, input, budget, output_schema):
            input['workload']['facts']['allowed'] = True
            output_schema['required'].clear()
            if failure == 'raise':
                raise RuntimeError('fixture failure')
            return {'ok': False}

    class Secondary:
        def run(self, *, task_id, input, budget, output_schema):
            assert output_schema['required'] == ['allowed']
            return {'ok': True, 'output': {'allowed': input['workload']['facts']['allowed']},
                    'meta': {'model_calls': 0}}

    schema = {'type': 'object', 'properties': {'allowed': {'type': 'boolean'}}, 'required': ['allowed']}
    workload = {'facts': {'allowed': False}}
    r = WorkloadEconomicsRunner(nodes=(EconomicsNode('n', 'read', 'routine', output_schema=schema),),
                                adapters={'p': Primary(), 's': Secondary()})
    result = r.run(workload=workload, policy=ExecutionPolicy('p', {'routine': 'p'},
                   exact_reuse=reuse, fallback_routes={'routine': 's'}))
    assert result['output'] == {'allowed': False}
    assert result['adapter_attempts'] == 2
    assert result['model_calls'] == 0
    assert result['exact_reuse_hits'] == 0
    assert not r.cache.memory
    assert workload['facts']['allowed'] is False
    assert schema['required'] == ['allowed']


def test_adapter_cannot_mutate_schema_used_for_validation():
    class MutatingAdapter:
        def run(self, *, task_id, input, budget, output_schema):
            output_schema['required'].clear()
            return {'ok': True, 'output': {}, 'meta': {'model_calls': 0}}

    schema = {'type': 'object', 'required': ['allowed']}
    r = WorkloadEconomicsRunner(nodes=(EconomicsNode('n', 'read', 'routine', output_schema=schema),),
                                adapters={'a': MutatingAdapter()})
    with pytest.raises(RuntimeError, match='output schema'):
        r.run(workload={}, policy=ExecutionPolicy('p', {'routine': 'a'}, exact_reuse=True))
    assert not r.cache.memory
    assert schema['required'] == ['allowed']


@pytest.mark.parametrize("failure", ["exception", "not_ok"])
@pytest.mark.parametrize("escalated_arm", ["baseline", "kora"])
def test_incomplete_failed_attempt_usage_cannot_support_reduction(failure, escalated_arm):
    class FailedAdapter(FakeAdapter):
        def run(self, **kwargs):
            self.calls += 1
            if failure == "exception":
                raise RuntimeError("fixture primary unavailable")
            return {"ok": False, "meta": {"model_calls": 1},
                    "usage": {"tokens_in": 10, "tokens_out": 4}}

    class SuccessfulFixtureAdapter(FakeAdapter):
        def run(self, **kwargs):
            result = super().run(**kwargs)
            count = 1 if escalated_arm == "baseline" else 0
            result["meta"]["model_calls"] = count
            result["usage"].update(tokens_in=count, tokens_out=count)
            return result

    nodes = (EconomicsNode("lookup", "read", "routine"),)
    direct = WorkloadEconomicsRunner(nodes=nodes, adapters={"a": FakeAdapter("a")})
    primary, fallback = FailedAdapter("primary"), SuccessfulFixtureAdapter("fallback")
    recovered = WorkloadEconomicsRunner(
        nodes=nodes, adapters={"p": primary, "f": fallback},
    )
    workload = {"topic": "same"}
    normal = direct.run(workload=workload, policy=ExecutionPolicy("direct", {"routine": "a"}))
    escalated = recovered.run(
        workload=workload,
        policy=ExecutionPolicy("recovered", {"routine": "p"}, fallback_routes={"routine": "f"}),
    )
    assert normal["output"] == escalated["output"]
    assert escalated["escalations"] == 1
    assert escalated["adapter_attempts"] == primary.calls + fallback.calls == 2
    assert escalated["model_calls"] == (1 if escalated_arm == "baseline" else 0)
    left, right = (escalated, normal) if escalated_arm == "baseline" else (normal, escalated)
    comparison = compare_economics(left, right)
    assert comparison["model_call_reduction_percent"] is None
    assert comparison["input_token_reduction_percent"] is None
    assert comparison["output_token_reduction_percent"] is None
    assert comparison["baseline_model_calls"] == left["model_calls"]
    assert comparison["kora_model_calls"] == right["model_calls"]
    assert comparison["adapter_attempt_reduction_percent"] == (
        50.0 if escalated_arm == "baseline" else -100.0
    )


@pytest.mark.parametrize("escalations", [None, -1, True, 0.5, "0"])
def test_invalid_explicit_escalation_metadata_cannot_support_reduction(escalations):
    left = {"model_calls": 10, "tokens_in": 10, "tokens_out": 10,
            "adapter_attempts": 10, "escalations": 0}
    right = {"model_calls": 5, "tokens_in": 5, "tokens_out": 5,
             "adapter_attempts": 5, "escalations": escalations}
    comparison = compare_economics(left, right)
    assert comparison["model_call_reduction_percent"] is None
    assert comparison["input_token_reduction_percent"] is None
    assert comparison["output_token_reduction_percent"] is None
    assert comparison["adapter_attempt_reduction_percent"] == 50.0


def test_explicit_no_escalations_preserves_comparison():
    left = {"model_calls": 10, "tokens_in": 10, "tokens_out": 10,
            "adapter_attempts": 10, "escalations": 0}
    right = {"model_calls": 0, "tokens_in": 0, "tokens_out": 0,
             "adapter_attempts": 5, "escalations": 0}
    comparison = compare_economics(left, right)
    assert comparison["model_call_reduction_percent"] == 100.0
    assert comparison["input_token_reduction_percent"] == 100.0
    assert comparison["output_token_reduction_percent"] == 100.0
    assert comparison["adapter_attempt_reduction_percent"] == 50.0
