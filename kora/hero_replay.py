"""Deterministic replay reducer for KORA Hero event streams."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from kora.hero_contracts import ExecutorClass, HeroEvent


class HeroReplayError(ValueError):
    """An ordered Hero event stream violated a state or evidence invariant."""


class HeroTaskProjection(BaseModel):
    """UI-safe task state reconstructed only from events."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    label: str
    purpose: str
    dependencies: list[str] = Field(default_factory=list)
    state: str = "created"
    attempt: int = 1
    executor_class: ExecutorClass | None = None
    adapter_id: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)


class HeroRunProjection(BaseModel):
    """Complete replay projection for one Hero run."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    run_state: str = "idle"
    last_sequence: int = -1
    tasks: dict[str, HeroTaskProjection] = Field(default_factory=dict)
    merge_state: str = "not_started"
    verification_state: str = "not_started"
    accepted_outcome: bool = False
    event_ids: list[str] = Field(default_factory=list)
    unhandled_event_ids: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)


_KNOWN_NON_STATE_EVENTS = {
    "workload.analyzed",
    "graph.created",
    "runtime.capabilities.registered",
    "execution.plan.created",
    "task.progress",
    "telemetry.sampled",
    "evidence.sealed",
}


def _require_task(state: HeroRunProjection, event: HeroEvent) -> HeroTaskProjection:
    task_id = event.task_id
    if task_id is None or task_id not in state.tasks:
        raise HeroReplayError(f"{event.event_type} references an unknown task")
    return state.tasks[task_id]


def _task_created(state: HeroRunProjection, event: HeroEvent) -> None:
    assert event.task_id is not None
    if event.task_id in state.tasks:
        raise HeroReplayError(f"duplicate task.created for {event.task_id!r}")
    label = event.payload.get("label")
    purpose = event.payload.get("purpose")
    dependencies = event.payload.get("dependencies", [])
    if not isinstance(label, str) or not label.strip():
        raise HeroReplayError("task.created payload requires a non-empty label")
    if not isinstance(purpose, str) or not purpose.strip():
        raise HeroReplayError("task.created payload requires a non-empty purpose")
    if not isinstance(dependencies, list) or not all(
        isinstance(dependency, str) and dependency for dependency in dependencies
    ):
        raise HeroReplayError("task.created dependencies must be a list of task IDs")
    missing = [dependency for dependency in dependencies if dependency not in state.tasks]
    if missing:
        raise HeroReplayError(f"task.created references dependencies not yet declared: {missing}")
    state.tasks[event.task_id] = HeroTaskProjection(
        task_id=event.task_id,
        label=label,
        purpose=purpose,
        dependencies=list(dependencies),
        attempt=event.attempt or 1,
        evidence_refs=list(event.evidence_refs),
    )


def _apply_task_event(state: HeroRunProjection, event: HeroEvent) -> None:
    if event.event_type == "task.created":
        _task_created(state, event)
        return
    task = _require_task(state, event)

    if event.event_type == "task.ready":
        if task.state not in {"created", "failed"}:
            raise HeroReplayError(f"task.ready is invalid from {task.state!r}")
        if any(state.tasks[dependency].state not in {"completed", "verified"} for dependency in task.dependencies):
            raise HeroReplayError("task.ready requires completed dependencies")
        task.state = "ready"
        task.attempt = event.attempt or task.attempt
    elif event.event_type == "task.routed":
        if task.state != "ready":
            raise HeroReplayError(f"task.routed is invalid from {task.state!r}")
        task.executor_class = event.executor_class
        task.adapter_id = event.adapter_id
    elif event.event_type == "task.started":
        if task.state != "ready" or task.executor_class is None:
            raise HeroReplayError("task.started requires a ready, routed task")
        if event.executor_class != task.executor_class:
            raise HeroReplayError("task.started executor differs from task.routed")
        task.state = "running"
        task.adapter_id = event.adapter_id
        task.attempt = event.attempt or task.attempt
    elif event.event_type == "task.completed":
        if task.state != "running":
            raise HeroReplayError(f"task.completed is invalid from {task.state!r}")
        task.state = "completed"
    elif event.event_type == "task.verified":
        if task.state != "completed":
            raise HeroReplayError(f"task.verified is invalid from {task.state!r}")
        task.state = "verified"
    elif event.event_type == "task.failed":
        if task.state != "running":
            raise HeroReplayError(f"task.failed is invalid from {task.state!r}")
        task.state = "failed"
    elif event.event_type == "task.progress":
        if task.state != "running":
            raise HeroReplayError("task.progress requires a running task")
    else:
        state.unhandled_event_ids.append(event.event_id)
        return

    for evidence_ref in event.evidence_refs:
        if evidence_ref not in task.evidence_refs:
            task.evidence_refs.append(evidence_ref)


def apply_hero_event(state: HeroRunProjection | None, event: HeroEvent) -> HeroRunProjection:
    """Apply one event, rejecting gaps, duplicates and illegal transitions."""

    if state is None:
        if event.sequence != 0 or event.event_type != "run.started":
            raise HeroReplayError("the first event must be run.started with sequence 0")
        state = HeroRunProjection(run_id=event.run_id)
    if event.run_id != state.run_id:
        raise HeroReplayError("an event stream cannot mix run IDs")
    if event.sequence != state.last_sequence + 1:
        raise HeroReplayError(
            f"expected sequence {state.last_sequence + 1}, received {event.sequence}"
        )
    if event.event_id in state.event_ids:
        raise HeroReplayError(f"duplicate event ID {event.event_id!r}")

    if event.event_type == "run.started":
        if state.last_sequence != -1:
            raise HeroReplayError("run.started can occur only once")
        state.run_state = "running"
    elif event.event_type.startswith("task."):
        _apply_task_event(state, event)
    elif event.event_type == "merge.started":
        if not state.tasks:
            raise HeroReplayError("merge.started requires at least one task")
        incomplete = [
            task.task_id
            for task in state.tasks.values()
            if task.state not in {"completed", "verified"}
        ]
        if incomplete:
            raise HeroReplayError(f"merge.started has incomplete tasks: {incomplete}")
        if state.merge_state != "not_started":
            raise HeroReplayError("merge.started can occur only once")
        state.merge_state = "running"
        state.run_state = "merging"
    elif event.event_type == "merge.completed":
        if state.merge_state != "running":
            raise HeroReplayError("merge.completed requires merge.started")
        state.merge_state = "completed"
    elif event.event_type == "verification.started":
        if state.merge_state != "completed":
            raise HeroReplayError("verification.started requires merge.completed")
        state.verification_state = "running"
        state.run_state = "verifying"
    elif event.event_type == "verification.passed":
        if state.verification_state != "running":
            raise HeroReplayError("verification.passed requires verification.started")
        state.verification_state = "passed"
    elif event.event_type == "verification.failed":
        if state.verification_state != "running":
            raise HeroReplayError("verification.failed requires verification.started")
        state.verification_state = "failed"
        state.run_state = "failed"
    elif event.event_type == "run.replanned":
        if state.run_state not in {"running", "failed", "verifying"}:
            raise HeroReplayError(f"run.replanned is invalid from {state.run_state!r}")
        state.run_state = "replanning"
    elif event.event_type == "run.escalated":
        if state.run_state not in {"running", "failed", "replanning", "verifying"}:
            raise HeroReplayError(f"run.escalated is invalid from {state.run_state!r}")
        state.run_state = "escalated"
    elif event.event_type == "run.completed":
        if state.verification_state != "passed":
            raise HeroReplayError("run.completed requires verification.passed")
        state.run_state = "completed"
        state.accepted_outcome = True
    elif event.event_type == "run.failed":
        state.run_state = "failed"
        state.accepted_outcome = False
    elif event.event_type not in _KNOWN_NON_STATE_EVENTS:
        state.unhandled_event_ids.append(event.event_id)

    state.last_sequence = event.sequence
    state.event_ids.append(event.event_id)
    for evidence_ref in event.evidence_refs:
        if evidence_ref not in state.evidence_refs:
            state.evidence_refs.append(evidence_ref)
    return state


def replay_hero_events(events: list[HeroEvent | dict[str, Any]]) -> HeroRunProjection:
    """Reconstruct a run projection from an ordered event list."""

    if not events:
        raise HeroReplayError("cannot replay an empty event stream")
    state: HeroRunProjection | None = None
    for raw_event in events:
        event = raw_event if isinstance(raw_event, HeroEvent) else HeroEvent.model_validate(raw_event)
        state = apply_hero_event(state, event)
    assert state is not None
    return state


__all__ = [
    "HeroReplayError",
    "HeroRunProjection",
    "HeroTaskProjection",
    "apply_hero_event",
    "replay_hero_events",
]
