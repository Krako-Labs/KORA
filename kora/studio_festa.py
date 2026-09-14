"""Offline Festa operations: retained replay, explicit fixtures and build locks.

No runtime execution or service-health client is connected to this surface.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from kora.hero_contracts import HeroEvent
from kora.hero_hybrid_evidence import hybrid_payload, read_record
from kora.hero_replay import apply_hero_event
from kora.studio_hero import build_studio_hero_fixture

LOCK_ENV = "KORA_HERO_SHOW_LOCK_PATH"
LOCK_SCHEMA = "hero.show-build-lock.v1"
BOUNDARY = (
    "RETAINED EVIDENCE REPLAY — sequential Mac and separately measured H100. "
    "No new inference. Viewer recovery is not model execution or runtime recovery. "
    "Semantic quality, simultaneous execution, 2x/3x and physical 8GB are not established."
)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


def software_fingerprint(package_root=None):
    """Bind all package source, schemas and browser assets, without host paths."""
    root = Path(package_root) if package_root else Path(__file__).parent
    files = {}
    for path in sorted(root.rglob("*")):
        if path.suffix in {".py", ".html", ".css", ".js", ".json"}:
            if path.is_symlink() or not path.is_file():
                raise ValueError("package source must be a regular file")
            files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not files:
        raise ValueError("empty package source")
    return digest(files)


_STARTUP_SOFTWARE_SHA256 = software_fingerprint()


def fixture_replay():
    fixture = build_studio_hero_fixture("apple")
    frames = fixture["frames"]
    return {
        "mode": "fixture",
        "identity": digest(frames),
        "run_id": fixture["run_id"],
        "request": fixture["request"],
        "boundary": fixture["claim_boundary"],
        "frames": frames,
        "source_objective_pass": False,
        "new_model_calls": 0,
        "source_model_calls": None,
    }


def retained_replay(environ):
    view = hybrid_payload(environ)
    if not view["available"]:
        return None
    state = None
    frames = []
    answer = None
    for raw in view["event_log"]["events"]:
        event = HeroEvent.model_validate(raw)
        state = apply_hero_event(state, event)
        if event.event_type == "merge.completed":
            answer = event.payload.get("answer")
        frames.append({
            "event": raw,
            "projection": state.model_dump(mode="json"),
            "view": {"answer": answer},
        })
    return {
        "mode": "retained",
        "identity": digest(view),
        "run_id": view["run_id"],
        "request": "Prepare the supplied-value launch brief using the retained Mac draft and separately measured H100 draft, then verify their evidence.",
        "boundary": BOUNDARY,
        "frames": frames,
        "source_objective_pass": view["accepted_outcome"],
        "new_model_calls": 0,
        "source_model_calls": {"mac": view["mac"]["model_calls"], "h100": view["h100"]["model_calls"]},
        "source_dates": {"mac": view["mac"]["recorded_at"], "h100": view["h100"]["recorded_at"]},
        "source_digests": view["source_digests"],
        "source_restoration": view["restoration"],
        "source_usage": {"mac": view["mac"]["usage"], "h100": view["h100"]["usage"]},
    }


def create_show_lock(environ=None, *, package_root=None):
    values = os.environ if environ is None else environ
    replay = retained_replay(values)
    if replay is None or replay["source_objective_pass"] is not True:
        raise ValueError("accepted retained evidence required")
    return {
        "schema_version": LOCK_SCHEMA,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "software_sha256": software_fingerprint(package_root),
        "retained_sha256": replay["identity"],
        "fixture_sha256": fixture_replay()["identity"],
        "execution_mode": "retained_replay_only",
        "new_model_calls": 0,
    }


def preflight(environ=None, *, package_root=None):
    """Revalidate from disk on every request. Never automatically choose fallback."""
    values = os.environ if environ is None else environ
    fixture = fixture_replay()
    checks = {"fixture": "ready", "software": "unchecked", "retained": "unchecked", "lock": "not_configured"}
    replay = None
    software = None
    try:
        software = software_fingerprint(package_root)
        checks["software"] = (
            "verified" if package_root is not None or software == _STARTUP_SOFTWARE_SHA256
            else "restart_required"
        )
    except (OSError, ValueError):
        checks["software"] = "rejected"
    try:
        replay = retained_replay(values)
        checks["retained"] = (
            "not_configured" if replay is None else
            "verified" if replay["source_objective_pass"] else "objective_failed"
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError):
        checks["retained"] = "rejected"
    configured = values.get(LOCK_ENV, "").strip()
    if configured:
        try:
            lock = read_record(configured)
            expected_keys = {"schema_version", "created_at", "software_sha256", "retained_sha256", "fixture_sha256", "execution_mode", "new_model_calls"}
            if (
                set(lock) != expected_keys
                or lock["schema_version"] != LOCK_SCHEMA
                or not isinstance(lock["created_at"], str)
                or not lock["created_at"]
                or lock["execution_mode"] != "retained_replay_only"
                or type(lock["new_model_calls"]) is not int
                or lock["new_model_calls"] != 0
            ):
                raise ValueError("invalid show lock")
            checks["lock"] = "verified" if (
                software is not None
                and replay is not None
                and lock["software_sha256"] == software
                and lock["retained_sha256"] == replay["identity"]
                and lock["fixture_sha256"] == fixture["identity"]
            ) else "mismatch"
        except (OSError, ValueError, KeyError, TypeError):
            checks["lock"] = "rejected"
    ready = all(checks[k] == "verified" for k in ("software", "retained", "lock"))
    return {
        "schema_version": "hero.festa-preflight.v1",
        "ready": ready,
        "status": "retained_replay_ready" if ready else "blocked",
        "checks": checks,
        "software_sha256": software,
        "retained": replay if ready else None,
        "fixture": fixture,
        "automatic_fallback": False,
        "new_model_calls": 0,
        "live_runtime_status": "not_checked",
        "boundary": BOUNDARY,
    }
