from __future__ import annotations

import inspect

import pytest

from kora.hero_contracts import (
    HardwareProfile,
    HeroEvent,
    ModelResourceProfile,
    WorkloadRequirements,
)
from kora.hero_mock_execution import (
    MockExecutionBridgeError,
    build_mock_execution_bridge,
)
from kora.hero_planner import HeroPlanningBundle
from kora.hero_replay import replay_hero_events
from kora.studio_hero import build_studio_hero_fixture


def _inputs() -> dict:
    fixture = build_studio_hero_fixture("apple")
    return {
        "bundle": HeroPlanningBundle.model_validate(fixture["planning_bundle"]),
        "hardware": HardwareProfile.model_validate(fixture["hardware"]),
        "model": ModelResourceProfile.model_validate(fixture["model"]),
        "workload": WorkloadRequirements.model_validate(fixture["workload"]),
    }


def _events(fixture: dict) -> list[dict]:
    return [frame["event"] for frame in fixture["frames"]]


def test_success_joins_plan_config_adapter_and_task_in_one_canonical_log():
    fixture = build_studio_hero_fixture("apple")
    events = _events(fixture)
    types = [event["event_type"] for event in events]
    bundle = fixture["planning_bundle"]
    bridge = fixture["mock_execution_bridge"]

    assert events[:5] == [
        event.model_dump(mode="json")
        for event in HeroPlanningBundle.model_validate(bundle).events
    ]
    assert [event["sequence"] for event in events] == list(range(len(events)))
    assert len({event["event_id"] for event in events}) == len(events)
    assert types.index("graph.created") < types.index("task.started")
    local_started = next(
        event
        for event in events
        if event["event_type"] == "task.started" and event["task_id"] == "draft"
    )
    assert local_started["adapter_id"] == bundle["plan"]["selected_adapter_id"]
    assert local_started["payload"]["effective_config"] == bridge["effective_config"]
    assert (
        local_started["payload"]["effective_config_digest"]
        == bridge["effective_config_digest"]
    )

    adapter_events = [
        event for event in events if event["event_type"].startswith("adapter.")
    ]
    assert adapter_events
    assert all(event["task_id"] == "draft" for event in adapter_events)
    assert all(event["attempt"] == 1 for event in adapter_events)
    assert all(
        event["payload"]["task_event_bridge"]["planning_digest"]
        == bundle["evidence_digest"]
        for event in adapter_events
    )
    assert all(
        event["payload"]["task_event_bridge"]["effective_config_digest"]
        == bridge["effective_config_digest"]
        for event in adapter_events
    )


def test_mock_completion_remains_separate_from_fixture_service_acceptance():
    fixture = build_studio_hero_fixture("apple")
    final = fixture["frames"][-1]
    assert fixture["mock_execution_bridge"]["accepted_outcome"] is False
    assert fixture["mock_execution_bridge"]["service_acceptance"] == "not_measured"
    assert final["projection"]["accepted_outcome"] is True
    assert final["view"]["fixture_accepted_outcome"] is True
    assert final["view"]["mock_execution_bridge"]["accepted_outcome"] is False
    assert final["view"]["B_local_execution"]["execution_performed"] is False
    assert fixture["actual_execution"] == {
        "runtime_starts": 0,
        "model_calls": 0,
        "provider_calls": 0,
    }


@pytest.mark.parametrize(
    ("scenario", "adapter_failure"),
    [
        ("cancelled", "adapter.cancelled"),
        ("load-failed", "adapter.load.failed"),
        ("execute-failed", "adapter.execute.failed"),
        ("finish-failed", "adapter.finish.failed"),
    ],
)
def test_failure_and_cancel_paths_stop_before_merge_and_preserve_cleanup(
    scenario, adapter_failure
):
    fixture = build_studio_hero_fixture(scenario)
    events = _events(fixture)
    types = [event["event_type"] for event in events]
    final = fixture["frames"][-1]

    assert adapter_failure in types
    assert "adapter.cleaned" in types
    assert types.index(adapter_failure) < types.index("adapter.cleaned")
    assert "task.failed" in types
    assert "merge.started" not in types
    assert not any(kind.startswith("verification.") for kind in types)
    assert final["projection"]["run_state"] == "failed"
    assert final["projection"]["tasks"]["draft"]["state"] == "failed"
    assert final["view"]["fixture_accepted_outcome"] is False
    assert final["view"]["mock_execution_bridge"]["failures"]


def test_cleanup_failure_retry_is_visible_before_mock_task_completion():
    fixture = build_studio_hero_fixture("cleanup-retried")
    events = _events(fixture)
    types = [event["event_type"] for event in events]
    failed = types.index("adapter.cleanup.failed")
    cleaned = types.index("adapter.cleaned")
    completed = next(
        index
        for index, event in enumerate(events)
        if event["event_type"] == "task.completed" and event["task_id"] == "draft"
    )

    assert failed < cleaned < completed
    assert fixture["frames"][failed]["view"]["mock_execution_bridge"][
        "adapter_state"
    ] == "cleanup_failed"
    assert fixture["frames"][-1]["projection"]["run_state"] == "completed"
    assert fixture["frames"][-1]["view"]["fixture_accepted_outcome"] is True


def test_bounded_replan_preserves_first_attempt_and_reuses_exact_plan():
    fixture = build_studio_hero_fixture("replanned")
    events = _events(fixture)
    types = [event["event_type"] for event in events]
    failed = next(
        index
        for index, event in enumerate(events)
        if event["event_type"] == "task.failed" and event["task_id"] == "draft"
    )
    replanned = types.index("run.replanned")
    reaffirmed = types.index("execution.plan.reaffirmed")
    second_start = next(
        index
        for index, event in enumerate(events)
        if event["event_type"] == "task.started"
        and event["task_id"] == "draft"
        and event["attempt"] == 2
    )
    replan_event = events[replanned]
    reaffirmed_event = events[reaffirmed]

    assert failed < replanned < reaffirmed < second_start
    assert replan_event["payload"]["replan_strategy"] == "bounded_same_plan_retry"
    assert (
        replan_event["payload"]["planning_digest"]
        == fixture["planning_bundle"]["evidence_digest"]
    )
    assert (
        reaffirmed_event["payload"]["effective_config"]
        == fixture["planning_bundle"]["plan"]["effective_config"]
    )
    assert (
        reaffirmed_event["payload"]["effective_config_digest"]
        == fixture["mock_execution_bridge"]["effective_config_digest"]
    )
    assert fixture["frames"][-1]["projection"]["tasks"]["draft"]["attempt"] == 2
    assert fixture["frames"][-1]["projection"]["run_state"] == "completed"
    assert any(
        failure["reason_code"] == "mock_execute_failure"
        for failure in fixture["frames"][-1]["view"]["mock_execution_bridge"][
            "failures"
        ]
    )


@pytest.mark.parametrize("scenario", ["pc", "unknown"])
def test_unsupported_execution_is_rejected_before_graph_session_or_task_start(scenario):
    fixture = build_studio_hero_fixture(scenario)
    events = _events(fixture)
    types = [event["event_type"] for event in events]
    expected = "placement_unresolved" if scenario == "pc" else "no_selected_runtime"

    assert types == [
        "run.started",
        "workload.analyzed",
        "runtime.capabilities.registered",
        "execution.plan.created",
        "evidence.sealed",
        "run.failed",
    ]
    assert not any(kind.startswith("adapter.") for kind in types)
    assert not any(kind.startswith("task.") for kind in types)
    assert "graph.created" not in types
    assert events[-1]["payload"]["reason_code"] == expected
    assert events[-1]["payload"]["execution_gate"] == "before_graph_and_task_start"
    assert fixture["mock_execution_bridge"]["runtime_identity"] is None


@pytest.mark.parametrize("tamper", ["plan", "planning_event", "model"])
def test_identity_or_digest_tampering_fails_closed_before_returning_a_log(tamper):
    data = _inputs()
    if tamper == "plan":
        data["bundle"].plan.effective_config["context_tokens"] = 1
    elif tamper == "planning_event":
        data["bundle"].events[0].payload["execution_performed"] = True
    else:
        data["model"].sha256 = "b" * 64

    with pytest.raises(MockExecutionBridgeError, match="planning_evidence_mismatch"):
        build_mock_execution_bridge(**data)


def test_bridge_is_deterministic_and_every_prefix_replays():
    first = build_mock_execution_bridge(**_inputs(), scenario="replanned")
    second = build_mock_execution_bridge(**_inputs(), scenario="replanned")
    assert first == second
    events = first["events"]
    for index in range(len(events)):
        expected = first["log"]["events"][: index + 1]
        projection = replay_hero_events(
            [HeroEvent.model_validate(event) for event in expected]
        )
        assert projection.last_sequence == index


def test_module_has_no_executable_runtime_or_network_binding():
    import kora.hero_mock_execution as module

    source = inspect.getsource(module)
    forbidden = (
        "import subprocess",
        "from subprocess",
        "import requests",
        "from requests",
        "import urllib",
        "from urllib",
        "import socket",
        "from socket",
        "import torch",
        "from torch",
        "import transformers",
        "from transformers",
        "import mlx",
        "import llama_cpp",
        "import openai",
    )
    assert all(token not in source for token in forbidden)
