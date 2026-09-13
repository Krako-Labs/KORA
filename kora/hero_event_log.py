"""Ordered in-memory event log and SSE serializer for KORA Hero."""

from __future__ import annotations

import json
from collections.abc import Iterable
from copy import deepcopy
from typing import Any

from kora.hero_contracts import HeroEvent
from kora.hero_replay import HeroRunProjection, apply_hero_event


class HeroEventLog:
    """Append-only event log with atomic replay validation."""

    def __init__(self, run_id: str) -> None:
        if not run_id:
            raise ValueError("run_id must not be empty")
        self._run_id = run_id
        self._events: list[HeroEvent] = []
        self._projection: HeroRunProjection | None = None

    @property
    def run_id(self) -> str:
        return self._run_id

    @property
    def projection(self) -> HeroRunProjection | None:
        return self._projection.model_copy(deep=True) if self._projection else None

    def append(self, raw_event: HeroEvent | dict[str, Any]) -> HeroRunProjection:
        """Validate and append one event without partially mutating on failure."""

        event = (
            raw_event
            if isinstance(raw_event, HeroEvent)
            else HeroEvent.model_validate(raw_event)
        )
        if event.run_id != self._run_id:
            raise ValueError("event run_id does not match this log")
        candidate_state = (
            self._projection.model_copy(deep=True) if self._projection else None
        )
        next_state = apply_hero_event(candidate_state, event)
        self._events.append(event)
        self._projection = next_state
        return next_state.model_copy(deep=True)

    def extend(
        self, events: Iterable[HeroEvent | dict[str, Any]]
    ) -> HeroRunProjection:
        """Append a batch atomically after validating the complete candidate stream."""

        candidate_events = list(events)
        candidate_state = (
            self._projection.model_copy(deep=True) if self._projection else None
        )
        validated: list[HeroEvent] = []
        for raw_event in candidate_events:
            event = (
                raw_event
                if isinstance(raw_event, HeroEvent)
                else HeroEvent.model_validate(raw_event)
            )
            if event.run_id != self._run_id:
                raise ValueError("event run_id does not match this log")
            candidate_state = apply_hero_event(candidate_state, event)
            validated.append(event)
        if candidate_state is None:
            raise ValueError("cannot append an empty event batch")
        self._events.extend(validated)
        self._projection = candidate_state
        return candidate_state.model_copy(deep=True)

    def events_after(self, sequence: int | None = None) -> list[HeroEvent]:
        """Return immutable events after a reconnect cursor."""

        if sequence is None:
            return list(self._events)
        if sequence < -1:
            raise ValueError("sequence cursor must be -1 or greater")
        return [event for event in self._events if event.sequence > sequence]

    def snapshot(self) -> dict[str, Any]:
        """Return a JSON-ready event and projection snapshot."""

        return {
            "schema_version": "hero.event-log.v1",
            "run_id": self._run_id,
            "event_count": len(self._events),
            "events": [
                event.model_dump(mode="json", exclude_none=True)
                for event in self._events
            ],
            "projection": (
                self._projection.model_dump(mode="json")
                if self._projection is not None
                else None
            ),
        }

    def format_sse(self, *, after_sequence: int | None = None) -> str:
        """Serialize events using same-origin Server-Sent Events framing."""

        chunks = ["retry: 1500\n\n"]
        for event in self.events_after(after_sequence):
            data = json.dumps(
                event.model_dump(mode="json", exclude_none=True),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            chunks.append(
                f"id: {event.sequence}\n"
                f"event: hero_event\n"
                f"data: {data}\n\n"
            )
        return "".join(chunks)

    def clone(self) -> "HeroEventLog":
        """Return an isolated copy useful for evidence sealing and tests."""

        clone = HeroEventLog(self._run_id)
        clone._events = list(self._events)
        clone._projection = deepcopy(self._projection)
        return clone


__all__ = ["HeroEventLog"]
