from __future__ import annotations

from datetime import datetime, timezone

import pytest

from kora.hero_contracts import HeroEvent
from kora.hero_replay import HeroReplayError, replay_hero_events


NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)


def event(
    sequence: int,
    event_type: str,
    *,
    phase: str,
    status: str,
    task_id: str | None = None,
    executor_class: str | None = None,
    adapter_id: str | None = None,
    payload: dict | None = None,
) -> HeroEvent:
    return HeroEvent(
        event_id=f"event-{sequence}",
        run_id="run-hero-1",
        sequence=sequence,
        occurred_at=NOW,
        event_type=event_type,
        phase=phase,
        status=status,
        source="fixture",
        evidence_level="fixture",
        task_id=task_id,
        executor_class=executor_class,
        adapter_id=adapter_id,
        payload=payload or {},
    )


def accepted_stream() -> list[HeroEvent]:
    return [
        event(0, "run.started", phase="intake", status="running"),
        event(
            1,
            "task.created",
            phase="decompose",
            status="created",
            task_id="facts",
            payload={"label": "Check facts", "purpose": "Extract bounded facts", "dependencies": []},
        ),
        event(2, "task.ready", phase="plan", status="ready", task_id="facts"),
        event(
            3,
            "task.routed",
            phase="plan",
            status="ready",
            task_id="facts",
            executor_class="deterministic",
        ),
        event(
            4,
            "task.started",
            phase="execute",
            status="running",
            task_id="facts",
            executor_class="deterministic",
            adapter_id="deterministic_core",
        ),
        event(5, "task.completed", phase="execute", status="completed", task_id="facts"),
        event(
            6,
            "task.created",
            phase="decompose",
            status="created",
            task_id="draft",
            payload={
                "label": "Draft answer",
                "purpose": "Create a bounded answer",
                "dependencies": ["facts"],
            },
        ),
        event(7, "task.ready", phase="plan", status="ready", task_id="draft"),
        event(
            8,
            "task.routed",
            phase="plan",
            status="ready",
            task_id="draft",
            executor_class="local_ai",
        ),
        event(
            9,
            "task.started",
            phase="execute",
            status="running",
            task_id="draft",
            executor_class="local_ai",
            adapter_id="mlx_lm",
        ),
        event(10, "task.completed", phase="execute", status="completed", task_id="draft"),
        event(11, "merge.started", phase="merge", status="running"),
        event(12, "merge.completed", phase="merge", status="completed"),
        event(13, "verification.started", phase="verify", status="running"),
        event(14, "verification.passed", phase="verify", status="verified"),
        event(15, "run.completed", phase="complete", status="completed"),
    ]


def test_replay_reconstructs_an_accepted_multi_executor_run() -> None:
    state = replay_hero_events(accepted_stream())

    assert state.run_state == "completed"
    assert state.accepted_outcome is True
    assert state.merge_state == "completed"
    assert state.verification_state == "passed"
    assert state.tasks["facts"].executor_class == "deterministic"
    assert state.tasks["draft"].executor_class == "local_ai"
    assert state.last_sequence == 15


def test_replay_is_deterministic() -> None:
    first = replay_hero_events(accepted_stream()).model_dump(mode="json")
    second = replay_hero_events(
        [item.model_dump(mode="json") for item in accepted_stream()]
    ).model_dump(mode="json")

    assert first == second


def test_replay_rejects_sequence_gaps() -> None:
    stream = accepted_stream()
    stream[5] = stream[5].model_copy(update={"sequence": 6, "event_id": "gap"})

    with pytest.raises(HeroReplayError, match="expected sequence 5"):
        replay_hero_events(stream)


def test_replay_rejects_completion_before_verification() -> None:
    stream = accepted_stream()[:13]
    stream.append(event(13, "run.completed", phase="complete", status="completed"))

    with pytest.raises(HeroReplayError, match="verification.passed"):
        replay_hero_events(stream)


def test_replay_preserves_unknown_events_for_forward_compatibility() -> None:
    stream = accepted_stream()
    stream.insert(
        1,
        event(1, "extension.visual_hint", phase="analyze", status="completed"),
    )
    stream = [
        item.model_copy(update={"sequence": index, "event_id": f"event-{index}"})
        for index, item in enumerate(stream)
    ]

    state = replay_hero_events(stream)

    assert state.unhandled_event_ids == ["event-1"]
    assert state.run_state == "completed"
