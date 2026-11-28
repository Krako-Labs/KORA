import pytest

from examples.document_policy_reuse.declared_identity import DeclaredPolicy
from examples.document_policy_reuse.maintenance import CASES
from examples.document_policy_reuse.run import BASE, Manual, NODES
from kora.solution.economics import ExecutionPolicy, WorkloadEconomicsRunner


@pytest.mark.parametrize("arm", ["manual", "kora"])
def test_declared_identity_change_and_rollback(arm):
    adapter = DeclaredPolicy()
    manual = Manual(adapter)
    runner = WorkloadEconomicsRunner(nodes=NODES, adapters={"fixture": adapter})
    policy = ExecutionPolicy(
        arm, {"routine": "fixture"}, exact_reuse=True, context_mode="brief+deps"
    )
    original_identity = adapter.cache_identity()
    phases = [
        (False, "v1", True),
        (False, "v1", False),
        (True, "v1", True),
        (True, "v1", False),
        (False, "v1", False),
        (False, "v2", True),
    ]
    for revised, version, should_dispatch in phases:
        adapter.revised = revised
        adapter.version = version
        before_phase = sum(adapter.calls.values())
        for index, (role, classification, overrides, before, after) in enumerate(CASES):
            work = {
                "document": {"id": f"doc-{index}", "classification": classification},
                "brief": dict(BASE, **dict(overrides, role=role)),
            }
            before_call = sum(adapter.calls.values())
            if arm == "manual":
                output, hits = manual.run(work)
            else:
                result = runner.run(workload=work, policy=policy)
                output = result["output"]
                hits = [event["reused"] for event in result["events"]]
                assert result["model_calls"] == 0
                assert result["adapter_attempts"] == sum(adapter.calls.values()) - before_call
            assert output == {"notice": after if revised else before}
            assert sum(adapter.calls.values()) - before_call + sum(hits) == len(NODES)
        assert (sum(adapter.calls.values()) > before_phase) == should_dispatch
        identity = adapter.cache_identity()
        if version == "v1":
            assert (identity == original_identity) == (not revised)
        else:
            assert identity != original_identity
