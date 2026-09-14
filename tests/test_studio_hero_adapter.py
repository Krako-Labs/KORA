from __future__ import annotations

import json
import threading
from copy import deepcopy
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from kora.hero_replay import replay_hero_events
from kora.hero_runtime_adapter_v2 import MockScript
from kora.studio_hero import hero_sse
from kora.studio_hero_adapter import (
    SCENARIOS,
    AdapterReview,
    adapter_event_payload,
    build_adapter_review_fixture,
    review_inputs,
)
from kora.studio_server import create_studio_request_handler


def setup_review(scenario="success"):
    fixture = build_adapter_review_fixture(scenario)
    review = AdapterReview(
        review_inputs(scenario), MockScript.model_validate(fixture["mock_script"])
    )
    return fixture, review


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_canonical_mock_events_replay_incrementally_without_acceptance(scenario):
    fixture, review = setup_review(scenario)
    assert fixture == build_adapter_review_fixture(scenario)
    events = [f["event"] for f in fixture["frames"]]
    for i, event in enumerate(events):
        frame = review.append(event)
        assert frame == fixture["frames"][i]
        assert frame["projection"] == replay_hero_events(events[: i + 1]).model_dump(
            mode="json"
        )
        assert frame["view"]["accepted_outcome"] is False
        assert frame["projection"]["accepted_outcome"] is False
        assert frame["view"]["service_acceptance"] == "not_measured"
        assert frame["view"]["B_local_execution"]["execution_performed"] is False
        assert frame["view"]["A_workload_control"] == {
            "actual_model_calls": 0,
            "actual_provider_calls": 0,
        }
    assert fixture["frames"][-1]["view"]["mock_allocation_retained"] is False
    assert fixture["frames"][-1]["view"]["adapter_state"] == (
        "blocked" if scenario == "placement_unresolved" else "closed"
    )


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_all_cursors_and_sse_reconstruct_identical_frames(scenario):
    fixture = build_adapter_review_fixture(scenario)
    frames = fixture["frames"]
    for cursor in range(-1, fixture["event_count"]):
        payload = adapter_event_payload(scenario, cursor)
        assert frames[: cursor + 1] + payload["frames"] == frames
        decoded = [
            json.loads(line[6:])
            for line in hero_sse(payload).splitlines()
            if line.startswith("data: ") and line != "data: {}"
        ]
        assert decoded == payload["frames"]


def test_failure_cleanup_and_retry_remain_visible_and_do_not_mean_quality():
    fixture = build_adapter_review_fixture("cleanup_failed_then_retried")
    failed, closed = fixture["frames"][-2:]
    assert failed["view"]["adapter_state"] == "cleanup_failed"
    assert failed["view"]["mock_allocation_retained"] is True
    assert closed["view"]["adapter_state"] == "closed"
    assert closed["view"]["mock_outcome"] == "completed"
    assert closed["view"]["failures"] == failed["view"]["failures"]
    assert closed["view"]["accepted_outcome"] is False
    assert closed["view"]["telemetry"]["peak_host_bytes"] is None
    assert closed["view"]["telemetry"]["ttft_ms"] is None


def test_placement_rejection_does_not_construct_a_session(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("unresolved placement must not create a session")

    monkeypatch.setattr("kora.studio_hero_adapter.MockRuntimeSession", forbidden)
    fixture = build_adapter_review_fixture("placement_unresolved")
    view = fixture["frames"][-1]["view"]
    assert view["compatibility"]["reason_codes"] == ["placement_unresolved"]
    assert view["runtime_identity"] is None
    assert not any(
        f["event"]["event_type"].startswith("adapter.") for f in fixture["frames"]
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("runtime_started", True),
        ("actual_model_calls", 1),
        ("actual_model_calls", False),
        ("actual_provider_calls", 1),
        ("mode", "live"),
        ("state", "running"),
        ("mock_allocation_retained", False),
        ("extra", "unexpected"),
    ],
)
def test_tampered_known_payload_rejected_atomically(field, value):
    fixture, review = setup_review()
    for frame in fixture["frames"][:5]:
        review.append(frame["event"])
    before = review.log.snapshot()
    event = deepcopy(fixture["frames"][5]["event"])
    event["payload"][field] = value
    with pytest.raises(ValueError):
        review.append(event)
    assert review.log.snapshot() == before
    assert review.state == "new"
    assert review.append(fixture["frames"][5]["event"]) == fixture["frames"][5]


@pytest.mark.parametrize(
    "field,value",
    [
        ("effective_config_digest", "b" * 64),
        ("model_revision", "changed"),
        ("mock_script_digest", "c" * 64),
        ("runtime_version", "invented"),
    ],
)
def test_bound_identity_mutation_rejected(field, value):
    fixture, review = setup_review()
    for frame in fixture["frames"][:5]:
        review.append(frame["event"])
    event = deepcopy(fixture["frames"][5]["event"])
    event["payload"]["runtime_identity"][field] = value
    with pytest.raises(ValueError, match="identity or payload"):
        review.append(event)


@pytest.mark.parametrize(
    "mutation", ["gap", "duplicate", "mixed_run", "observed", "planning", "order"]
)
def test_sequence_evidence_planning_and_lifecycle_fail_closed(mutation):
    fixture, review = setup_review()
    events = [deepcopy(f["event"]) for f in fixture["frames"]]
    if mutation == "gap":
        events.pop(2)
    elif mutation == "duplicate":
        events.insert(2, events[1])
    elif mutation == "mixed_run":
        events[2]["run_id"] = "other"
    elif mutation == "observed":
        events[0]["evidence_level"] = "observed"
    elif mutation == "planning":
        events[3]["payload"]["runtime_started"] = True
    else:
        events[5]["event_type"] = "adapter.started"
    with pytest.raises(ValueError):
        for event in events:
            review.append(event)


def test_unknown_extension_retained_without_state_change():
    fixture, review = setup_review()
    for frame in fixture["frames"][:5]:
        review.append(frame["event"])
    unknown = deepcopy(fixture["frames"][5]["event"])
    unknown["event_type"] = "adapter.future_notice"
    unknown["payload"] = {"state": "completed", "accepted_outcome": True}
    frame = review.append(unknown)
    assert frame["view"]["adapter_state"] == "new"
    assert frame["view"]["accepted_outcome"] is False
    assert unknown["event_id"] in frame["projection"]["unhandled_event_ids"]
    assert frame["event"]["payload"] == unknown["payload"]


@pytest.mark.parametrize(
    "kind", ["task.completed", "verification.passed", "run.completed"]
)
def test_mock_review_cannot_promote_service_acceptance(kind):
    fixture, review = setup_review()
    for frame in fixture["frames"]:
        review.append(frame["event"])
    event = deepcopy(fixture["frames"][-1]["event"])
    event.update(
        sequence=10, event_id="forged-completion", event_type=kind, task_id="fake"
    )
    with pytest.raises(ValueError):
        review.append(event)
    assert review.log.projection.accepted_outcome is False


def test_returned_nested_state_cannot_mutate_projection():
    fixture, review = setup_review()
    for frame in fixture["frames"][:6]:
        last = review.append(frame["event"])
    last["view"]["runtime_identity"]["effective_config"]["changed"] = True
    last["projection"]["unhandled_event_ids"].clear()
    last["event"]["payload"]["runtime_identity"]["model_revision"] = "changed"
    assert review.append(fixture["frames"][6]["event"]) == fixture["frames"][6]


@pytest.mark.parametrize("cursor", [-2, 100, True, 1.5])
def test_invalid_cursor(cursor):
    with pytest.raises(ValueError):
        adapter_event_payload("success", cursor)


@pytest.fixture
def server():
    def no_probe():
        raise AssertionError("review must not probe the host")

    instance = ThreadingHTTPServer(
        ("127.0.0.1", 0), create_studio_request_handler(no_probe)
    )
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{instance.server_port}"
    instance.shutdown()
    instance.server_close()
    thread.join()


def test_review_http_csp_and_canonical_last_event_id(server):
    with urlopen(server + "/hero/adapter") as response:
        assert "script-src 'self'" in response.headers["Content-Security-Policy"]
        assert "MOCK FIXTURE REPLAY" in response.read().decode()
    with urlopen(server + "/api/hero/adapter/fixture") as response:
        fixture = json.load(response)
        assert "frames" not in fixture
        assert fixture["event_digest"]
    request = Request(server + "/api/hero/adapter/sse", headers={"Last-Event-ID": "8"})
    with urlopen(request) as response:
        data = response.read().decode()
        assert data.startswith("id: 9\nevent: hero\n")
    with urlopen(server + "/api/hero/adapter/events?after=9") as response:
        assert json.load(response)["frames"] == []


@pytest.mark.parametrize(
    "suffix",
    [
        "fixture?scenario=unknown",
        "events?after=-2",
        "events?after=10",
        "sse?after=nan",
    ],
)
def test_invalid_http_request(server, suffix):
    with pytest.raises(HTTPError) as error:
        urlopen(server + "/api/hero/adapter/" + suffix)
    assert error.value.code == 400
