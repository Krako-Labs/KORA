"""Guardrail regression tests for known over-routing cases.

Two target-workload cases must ESCALATE (the deterministic front door must
abstain and defer to the LLM), but the reference dispatcher routes them anyway:

  * rea-030 (reasoning): a damaged-gift request with no order number. The word
    "number" (from "order number") plus "help" made it match the support_phone
    FAQ, so it was answered with a phone number instead of escalating.
  * trp-030 (trap): a refund query whose payload carries days_since_delivery=-5,
    a physically impossible value. The policy evaluator accepted it and returned
    "eligible" instead of abstaining on the malformed input.

Both cases are labelled should_escalate=True in the canonical workload. The
positive class and escalate criterion here mirror run.py exactly:
    escalated == (not Decision.routed)

These tests are the fixed, named record of the over-routing. Before the
guardrails land they FAIL; after the range-check and FAQ-signal fixes they PASS.
Case data is loaded from the canonical workload rather than hard-coded so the
test can never drift from the shipped fixture.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kora.dispatcher import dispatch

_WORKLOAD = Path(__file__).resolve().parent.parent / "workloads" / "full.json"
_OVER_ROUTING_IDS = ("rea-030", "trp-030")


def _cases_by_id() -> dict[str, dict]:
    data = json.loads(_WORKLOAD.read_text(encoding="utf-8"))
    return {c["id"]: c for c in data["cases"]}


@pytest.fixture(scope="module")
def cases() -> dict[str, dict]:
    return _cases_by_id()


@pytest.mark.parametrize("case_id", _OVER_ROUTING_IDS)
def test_case_is_labelled_should_escalate(cases: dict[str, dict], case_id: str) -> None:
    """Guard the premise: these cases are escalate-positive in the fixture."""
    assert cases[case_id]["should_escalate"] is True


@pytest.mark.parametrize("case_id", _OVER_ROUTING_IDS)
def test_over_routing_case_escalates(cases: dict[str, dict], case_id: str) -> None:
    """The front door must abstain (escalate), not produce a deterministic answer."""
    case = cases[case_id]
    decision = dispatch(case["text"], case.get("payload"))
    escalated = not decision.routed
    assert escalated, (
        f"{case_id} was routed to {decision.handler!r} "
        f"(answer={decision.answer!r}) but must escalate"
    )
