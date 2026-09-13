from __future__ import annotations

from datetime import datetime, timezone
import json

import pytest

from kora.hero_contracts import HeroEvent
from kora.hero_event_log import HeroEventLog
from kora.hero_replay import HeroReplayError


NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)


def event(sequence: int, event_type: str, *, status: str, phase: str) -> HeroEvent:
    return HeroEvent(
        event_id=f"event-{sequence}",
        run_id="run-1",
        sequence=sequence,
        occurred_at=NOW,
        event_type=event_type,
        phase=phase,
        status=status,
        source="test",
        evidence_level="fixture",
    )


def test_event_log_rejects_a_bad_batch_atomically() -> None:
    log = HeroEventLog("run-1")
    log.append(event(0, "run.started", status="running", phase="intake"))

    with pytest.raises(HeroReplayError, match="expected sequence 2"):
        log.extend(
            [
                event(1, "workload.analyzed", status="completed", phase="analyze"),
                event(3, "graph.created", status="completed", phase="decompose"),
            ]
        )

    assert log.snapshot()["event_count"] == 1
    assert log.projection is not None
    assert log.projection.last_sequence == 0


def test_event_log_reconnect_cursor_returns_only_newer_events() -> None:
    log = HeroEventLog("run-1")
    log.extend(
        [
            event(0, "run.started", status="running", phase="intake"),
            event(1, "workload.analyzed", status="completed", phase="analyze"),
            event(2, "graph.created", status="completed", phase="decompose"),
        ]
    )

    assert [item.sequence for item in log.events_after(0)] == [1, 2]
    assert [item.sequence for item in log.events_after(2)] == []


def test_sse_uses_ordered_ids_named_events_and_canonical_json() -> None:
    log = HeroEventLog("run-1")
    log.extend(
        [
            event(0, "run.started", status="running", phase="intake"),
            event(1, "workload.analyzed", status="completed", phase="analyze"),
        ]
    )

    stream = log.format_sse(after_sequence=0)

    assert stream.startswith("retry: 1500\n\n")
    assert "id: 0\n" not in stream
    assert "id: 1\nevent: hero_event\ndata: " in stream
    payload_line = next(
        line.removeprefix("data: ")
        for line in stream.splitlines()
        if line.startswith("data: ")
    )
    payload = json.loads(payload_line)
    assert payload["sequence"] == 1
    assert payload["event_type"] == "workload.analyzed"


def test_projection_and_snapshot_are_defensive_copies() -> None:
    log = HeroEventLog("run-1")
    log.append(event(0, "run.started", status="running", phase="intake"))

    projection = log.projection
    assert projection is not None
    projection.run_state = "failed"

    assert log.projection is not None
    assert log.projection.run_state == "running"
    assert log.snapshot()["projection"]["run_state"] == "running"
