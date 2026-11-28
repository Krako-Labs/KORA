"""Offline maintenance replay: cache identity is part of the policy contract."""
from copy import deepcopy
import json
from statistics import median
from time import perf_counter_ns

from examples.document_policy_reuse.run import BASE, Fixture, Manual, NODES
from kora.solution.economics import ExecutionPolicy, WorkloadEconomicsRunner


class PolicyFixture(Fixture):
    """One shared synthetic policy change, used by every comparison arm."""

    def __init__(self):
        super().__init__()
        self.revised = False

    def run(self, *, task_id, input, budget, output_schema):
        result = super().run(
            task_id=task_id, input=input, budget=budget, output_schema=output_schema
        )
        # Revised policy: permit redacted restricted documents only for staff
        # with a live grant and explicit redaction permission.
        if self.revised and task_id == "authorize":
            brief = input["workload"]["brief"]
            classification = input["dependencies"]["classify"]["classification"]
            if (
                result["output"]["action"] == "deny"
                and classification == "restricted"
                and brief["granted"]
                and brief["role"] == "staff"
                and brief["redaction_allowed"]
                and brief["as_of"] <= brief["expires"]
            ):
                result["output"]["action"] = "redact"
        return result


# Expected answers are authored separately from the implementation.
# The first case is affected by the new policy; the others are controls.
CASES = (
    ("staff", "restricted", {}, "deny", "redact"),
    ("guest", "restricted", {}, "deny", "deny"),
    ("staff", "restricted", {"redaction_allowed": False}, "deny", "deny"),
    ("staff", "restricted", {"as_of": "2026-11-30"}, "refresh", "refresh"),
    ("staff", "restricted", {"granted": False}, "deny", "deny"),
    ("guest", "internal", {}, "redact", "redact"),
)

# Deliberate invalidation fault is isolated to this synthetic experiment.
# Never use the unchanged-version stage as an authorization mechanism.
STAGES = (
    ("baseline", False, "v1"),
    ("baseline_repeat", False, "v1"),
    ("missing_version_bump", True, "v1"),
    ("version_bump", True, "v2"),
    ("revised_repeat", True, "v2"),
    ("rollback", False, "v3"),
    ("rollback_repeat", False, "v3"),
)


def run(rounds=10):
    if type(rounds) is not int or rounds < 1:
        raise ValueError("rounds must be a positive integer")
    arms = ("direct", "manual", "kora")
    totals = {
        arm: {
            stage: {
                "requests": 0, "matches": 0, "expected_faults": 0,
                "dispatches": 0, "hits": 0, "latencies_us": [],
            }
            for stage, _, _ in STAGES
        }
        for arm in arms
    }
    for round_id in range(rounds):
        # Rotate order to reduce systematic measurement bias.
        for arm in arms[round_id % len(arms):] + arms[:round_id % len(arms)]:
            adapter = PolicyFixture()
            runner = WorkloadEconomicsRunner(nodes=NODES, adapters={"fixture": adapter})
            policy = ExecutionPolicy(
                arm, {"routine": "fixture"},
                exact_reuse=arm == "kora", context_mode="brief+deps",
            )
            manual = Manual(adapter)
            for stage, revised, version in STAGES:
                adapter.revised = revised
                adapter.version = version
                record = totals[arm][stage]
                for index, (role, classification, overrides, before, after) in enumerate(CASES):
                    work = {
                        "document": {"id": f"doc-{index}", "classification": classification},
                        "brief": dict(BASE, **dict(overrides, role=role)),
                    }
                    expected = after if revised else before
                    calls = sum(adapter.calls.values())
                    started = perf_counter_ns()
                    if arm == "manual":
                        output, hits = manual.run(deepcopy(work))
                    else:
                        result = runner.run(workload=deepcopy(work), policy=policy)
                        output = result["output"]
                        hits = [event["reused"] for event in result["events"]]
                        assert result["model_calls"] == 0
                        assert result["adapter_attempts"] == sum(adapter.calls.values()) - calls
                    elapsed = (perf_counter_ns() - started) / 1000
                    dispatches = sum(adapter.calls.values()) - calls
                    assert dispatches + sum(hits) == len(NODES)
                    intentional_fault = stage == "missing_version_bump" and arm != "direct" and before != after
                    # Fault detector must identify the actual stale answer.
                    assert output == {"notice": before if intentional_fault else expected}, (arm, stage, index, output)
                    record["requests"] += 1
                    record["matches"] += output == {"notice": expected}
                    record["expected_faults"] += intentional_fault
                    record["dispatches"] += dispatches
                    record["hits"] += sum(hits)
                    record["latencies_us"].append(elapsed)
    for arm in arms:
        for stage, record in totals[arm].items():
            record["p50_us"] = median(record.pop("latencies_us"))
            assert record["matches"] + record["expected_faults"] == record["requests"]
    return {
        "scope": "authored synthetic policy maintenance replay, no actual document access or model calls",
        "rounds": rounds,
        "cases_per_stage": len(CASES),
        "model_calls": 0,
        "arms": totals,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
