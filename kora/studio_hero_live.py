"""Read-only Studio projection for explicitly retained Hero live evidence."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

from kora.hero_replay import replay_hero_events

LIVE_EVIDENCE_ENV = "KORA_HERO_LIVE_EVIDENCE_PATH"
MAX_LIVE_EVIDENCE_BYTES = 2 * 1024 * 1024


class StudioLiveEvidenceError(ValueError):
    """A configured live evidence record failed the read-only boundary."""


def _disabled() -> dict[str, Any]:
    return {
        "schema_version": "hero.studio-live-view.v1",
        "available": False,
        "status": "not_configured",
        "claim_boundary": (
            "No live evidence path is configured. Studio never starts a runtime, "
            "loads a model, or calls a provider."
        ),
    }


def load_live_evidence(path: str | os.PathLike[str]) -> dict[str, Any]:
    """Load one bounded record without following symlinks or exposing its path."""

    target = Path(path).expanduser()
    if target.is_symlink() or not target.is_file():
        raise StudioLiveEvidenceError(
            "live evidence must be a regular non-symlink file"
        )
    if target.stat().st_size <= 0 or target.stat().st_size > MAX_LIVE_EVIDENCE_BYTES:
        raise StudioLiveEvidenceError("live evidence size is outside the allowed bound")
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StudioLiveEvidenceError("live evidence is not valid UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise StudioLiveEvidenceError("live evidence must be a JSON object")
    if (
        payload.get("schema_version") != "hero.live-execution-evidence.v1"
        or payload.get("evidence_level") != "observed"
    ):
        raise StudioLiveEvidenceError("unsupported live evidence schema or level")
    actual = payload.get("actual_execution")
    verification = payload.get("verification")
    cleanup = payload.get("cleanup")
    local = payload.get("B_local_execution")
    runtime = payload.get("runtime_identity")
    output = payload.get("output")
    usage = payload.get("usage")
    effective = payload.get("effective_config")
    event_log = payload.get("event_log")
    if not all(
        isinstance(item, dict)
        for item in (actual, verification, cleanup, local, runtime, event_log)
    ) or not isinstance(usage, list):
        raise StudioLiveEvidenceError("live evidence sections are incomplete")
    calls = actual.get("model_calls")
    max_output_tokens = (
        effective.get("max_output_tokens") if isinstance(effective, dict) else None
    )
    if (
        isinstance(calls, bool)
        or not isinstance(calls, int)
        or calls < 0
        or calls > 3
        or actual.get("provider_calls") != 0
        or runtime.get("network") != "loopback"
        or verification.get("semantic_non_regression") != "not_measured"
        or local.get("semantic_quality_measured") is not False
    ):
        raise StudioLiveEvidenceError(
            "live evidence violates the bounded claim contract"
        )
    if (
        not isinstance(effective, dict)
        or isinstance(max_output_tokens, bool)
        or not isinstance(max_output_tokens, int)
        or not 1 <= max_output_tokens <= 256
        or len(usage) != calls
        or any(
            not isinstance(sample, dict)
            or isinstance(sample.get("tokens_out"), bool)
            or not isinstance(sample.get("tokens_out"), int)
            or not 0 <= sample["tokens_out"] <= max_output_tokens
            for sample in usage
        )
    ):
        raise StudioLiveEvidenceError(
            "live evidence violates the output-token contract"
        )
    accepted = verification.get("accepted_outcome")
    if not isinstance(accepted, bool):
        raise StudioLiveEvidenceError("live acceptance must be boolean")
    if accepted and (
        output is None
        or calls < 1
        or cleanup.get("cleanup_success") is not True
        or local.get("execution_performed") is not True
    ):
        raise StudioLiveEvidenceError(
            "accepted live evidence lacks execution or cleanup"
        )
    events = event_log.get("events")
    if not isinstance(events, list) or not events:
        raise StudioLiveEvidenceError("live evidence event log is empty")
    projection = replay_hero_events(events)
    if projection.accepted_outcome is not accepted:
        raise StudioLiveEvidenceError("event replay and evidence acceptance differ")
    return deepcopy(payload)


def live_evidence_payload(
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return a Studio-safe view; never discovers evidence implicitly."""

    values = os.environ if environ is None else environ
    configured = values.get(LIVE_EVIDENCE_ENV, "").strip()
    if not configured:
        return _disabled()
    evidence = load_live_evidence(configured)
    return {
        "schema_version": "hero.studio-live-view.v1",
        "available": True,
        "status": (
            "objective_pass"
            if evidence["verification"]["accepted_outcome"]
            else "failed"
        ),
        "claim_boundary": evidence["claim_boundary"],
        "run_id": evidence["run_id"],
        "recorded_at": evidence["recorded_at"],
        "planning_digest": evidence["planning_digest"],
        "runtime_identity": evidence["runtime_identity"],
        "effective_config": evidence["effective_config"],
        "output": evidence["output"],
        "usage": evidence["usage"],
        "cleanup": evidence["cleanup"],
        "actual_execution": evidence["actual_execution"],
        "verification": evidence["verification"],
        "A_workload_control": evidence["A_workload_control"],
        "B_local_execution": evidence["B_local_execution"],
        "event_count": evidence["event_log"]["event_count"],
    }


__all__ = [
    "LIVE_EVIDENCE_ENV",
    "MAX_LIVE_EVIDENCE_BYTES",
    "StudioLiveEvidenceError",
    "live_evidence_payload",
    "load_live_evidence",
]
