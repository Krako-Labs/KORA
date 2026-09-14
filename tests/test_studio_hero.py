from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from kora.hero_contracts import HeroEvent
from kora.hero_planner import HeroPlanningBundle
from kora.hero_replay import HeroReplayError, replay_hero_events
from kora.studio_hero import (
    SCENARIOS,
    build_studio_hero_fixture,
    hero_event_payload,
    hero_sse,
    project_studio_hero_events,
)
from kora.studio_server import create_studio_request_handler


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_fixture_uses_canonical_bundle_and_every_prefix_matches_replay(scenario):
    fixture = build_studio_hero_fixture(scenario)
    bundle = HeroPlanningBundle.model_validate(fixture["planning_bundle"])
    frames = fixture["frames"]
    events = [HeroEvent.model_validate(frame["event"]) for frame in frames]
    assert events[:5] == bundle.events
    assert fixture == build_studio_hero_fixture(scenario)
    for i, frame in enumerate(frames):
        assert frame["projection"] == replay_hero_events(events[: i + 1]).model_dump(
            mode="json"
        )
        assert frame["event"]["evidence_level"] == "fixture"
        assert frame["view"]["B_local_execution"]["execution_performed"] is False
    assert fixture["actual_execution"] == {
        "runtime_starts": 0,
        "model_calls": 0,
        "provider_calls": 0,
    }


@pytest.mark.parametrize(
    ("scenario", "adapter"),
    [("apple", "mlx-lm"), ("pc", "llama.cpp"), ("unknown", None)],
)
def test_planning_selection_and_all_four_reason_codes(scenario, adapter):
    fixture = build_studio_hero_fixture(scenario)
    plan = fixture["planning_bundle"]["plan"]
    assert plan["selected_adapter_id"] == adapter
    assert {item["adapter_id"] for item in plan["candidates"]} == {
        "mlx-lm",
        "llama.cpp",
        "freetoken",
        "ktransformers",
    }
    assert all(item["reason_codes"] for item in plan["candidates"])
    if scenario == "unknown":
        assert all(item["rejected"] for item in plan["candidates"])
        assert fixture["frames"][-1]["projection"]["tasks"] == {}
        assert fixture["frames"][-1]["view"]["fixture_accepted_outcome"] is False


def test_quality_failure_never_becomes_accepted_despite_completed_tasks():
    fixture = build_studio_hero_fixture("quality-failed")
    frame = fixture["frames"][-1]
    assert all(
        task["state"] == "completed" for task in frame["projection"]["tasks"].values()
    )
    assert frame["projection"]["merge_state"] == "completed"
    assert frame["view"]["structural_acceptance"] == "fixture_pass"
    assert frame["view"]["service_acceptance"] == "fixture_fail"
    assert frame["view"]["fixture_accepted_outcome"] is False
    assert not any(
        item["view"]["fixture_accepted_outcome"] for item in fixture["frames"]
    )


def test_final_acceptance_requires_service_gate_not_only_reducer_completion():
    events = [
        HeroEvent.model_validate(f["event"])
        for f in build_studio_hero_fixture()["frames"]
    ]
    passed = next(
        i for i, event in enumerate(events) if event.event_type == "verification.passed"
    )
    events[passed] = events[passed].model_copy(
        update={"payload": {"structural_acceptance": "fixture_pass"}}
    )
    assert replay_hero_events(events).accepted_outcome is True
    assert (
        project_studio_hero_events(events)[-1]["view"]["fixture_accepted_outcome"]
        is False
    )


def test_no_early_candidates_answer_or_acceptance_and_a_b_are_separate():
    frames = build_studio_hero_fixture()["frames"]
    for frame in frames[:3]:
        assert not frame["view"]["candidates_visible"]
    for frame in frames[:-1]:
        assert not frame["view"]["fixture_accepted_outcome"]
    merge_index = next(
        i
        for i, frame in enumerate(frames)
        if frame["event"]["event_type"] == "merge.completed"
    )
    assert all(not frame["view"]["answer"] for frame in frames[:merge_index])
    assert frames[-1]["view"]["fixture_accepted_outcome"]
    assert frames[-1]["view"]["A_workload_control"]["fixture_completed_tasks"] == {
        "deterministic": 1,
        "exact_reuse": 1,
        "local_ai": 1,
        "frontier_ai": 1,
    }
    assert frames[-1]["view"]["B_local_execution"]["latency_ms"] is None


def test_fixture_projection_rejects_observed_events_and_event_gaps():
    events = [
        HeroEvent.model_validate(f["event"])
        for f in build_studio_hero_fixture()["frames"]
    ]
    with pytest.raises(ValueError, match="non-fixture"):
        project_studio_hero_events(
            [events[0].model_copy(update={"evidence_level": "observed"})]
        )
    with pytest.raises(HeroReplayError, match="expected sequence"):
        project_studio_hero_events([events[0], events[2]])


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_recovery_suffix_reconstructs_every_exact_frame(scenario):
    frames = build_studio_hero_fixture(scenario)["frames"]
    for cursor in range(-1, len(frames)):
        suffix = hero_event_payload(scenario, cursor)["frames"]
        assert frames[: cursor + 1] + suffix == frames
    sse = hero_sse(hero_event_payload(scenario, 2))
    decoded = [
        json.loads(line[6:])
        for line in sse.splitlines()
        if line.startswith("data: ") and line != "data: {}"
    ]
    assert decoded == frames[3:]


@pytest.fixture
def hero_server():
    def no_probe():
        raise AssertionError("Hero route must not probe the real host")

    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), create_studio_request_handler(no_probe)
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    server.server_close()
    thread.join()


def test_http_hero_assets_metadata_events_and_last_event_id(hero_server):
    with urlopen(hero_server + "/hero") as response:
        assert "script-src 'self'" in response.headers["Content-Security-Policy"]
        html = response.read().decode()
    assert (
        "FIXTURE PLAYBACK" in html
        and "THIS COMPUTER" in html
        and "MODEL FOOTPRINT" in html
    )
    for name, content_type in [
        ("hero.css", "text/css"),
        ("hero.js", "application/javascript"),
    ]:
        with urlopen(hero_server + "/hero-assets/" + name) as response:
            assert content_type in response.headers["Content-Type"]
            assert response.read()
    with urlopen(hero_server + "/api/hero/fixture") as response:
        fixture = json.load(response)
        assert "frames" not in fixture
    request = Request(hero_server + "/api/hero/sse", headers={"Last-Event-ID": "29"})
    with urlopen(request) as response:
        assert response.read().decode().startswith("id: 30\nevent: hero\n")


@pytest.mark.parametrize(
    "path",
    [
        "/api/hero/fixture?scenario=arbitrary",
        "/api/hero/events?after=-2",
        "/api/hero/events?after=31",
        "/api/hero/sse?after=nan",
    ],
)
def test_invalid_scenario_and_cursor_fail_closed(hero_server, path):
    with pytest.raises(HTTPError) as error:
        urlopen(hero_server + path)
    assert error.value.code == 400
