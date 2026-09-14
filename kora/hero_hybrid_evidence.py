"""Validated read-only Mac/owned-GPU evidence composition; never executes."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path

from kora.hero_live_execution import (
    LiveDraft,
    LiveServiceRequest,
    _digest,
    _validate_draft,
)
from kora.hero_remote_execution import SCHEMA, RemoteEvents
from kora.hero_replay import replay_hero_events
from kora.studio_hero_live import load_live_evidence

ENV = "KORA_HERO_HYBRID_EVIDENCE_PATH"


def read_record(path):
    target = Path(path)
    if (
        target.is_symlink()
        or not target.is_file()
        or not 0 < target.stat().st_size <= 2 * 1024 * 1024
    ):
        raise ValueError("requires one bounded non-symlink evidence file")
    value = json.loads(target.read_text())
    if not isinstance(value, dict):
        raise TypeError("evidence must be an object")
    return value


def validate_remote(remote, *, allow_fixture=False):
    if (
        remote.get("schema_version") != SCHEMA
        or remote.get("evidence_level")
        not in ({"observed", "fixture"} if allow_fixture else {"observed"})
        or remote.get("privacy_mode") != "private_network"
        or remote.get("execution_location") != "owned_remote_gpu"
    ):
        raise ValueError("unsupported remote evidence boundary")
    service = LiveServiceRequest.model_validate(remote["request"])
    if remote["input_digest"] != _digest(service.model_dump(mode="json")):
        raise ValueError("request digest mismatch")
    accepted = remote["verification"]["objective_pass"]
    if (
        type(accepted) is not bool
        or remote["verification"]["semantic_quality"] != "not_measured"
    ):
        raise ValueError("invalid verification boundary")
    calls = remote["actual_execution"]["owned_remote_model_calls"]
    attempts = remote["attempts"]
    if (
        type(calls) is not int
        or not 0 <= calls <= 2
        or len(attempts) != calls
        or remote["actual_execution"]["commercial_provider_calls"] != 0
    ):
        raise ValueError("invalid call accounting")
    for i, sample in enumerate(attempts, 1):
        if sample["attempt"] != i:
            raise ValueError("attempt order mismatch")
        for key, maximum in [("tokens_in", 4096), ("tokens_out", 256)]:
            value = sample[key]
            if value is not None and (
                type(value) is not int or not 0 <= value <= maximum
            ):
                raise ValueError("token accounting invalid")
            if accepted and value is None:
                raise ValueError("accepted evidence needs complete usage")
    if accepted:
        if (
            calls < 1
            or remote["cleanup"].get("owned_process_stopped") is not True
            or remote["verification"]["failure_code"] is not None
            or remote["plan"]["selected_adapter_id"] != "vllm-owned"
            or attempts[-1]["status"] != "objective_pass"
        ):
            raise ValueError("accepted evidence lacks completed execution")
        draft = LiveDraft.model_validate(remote["output"])
        if _validate_draft(draft, service) or remote["output_digest"] != _digest(
            draft.model_dump(mode="json")
        ):
            raise ValueError("output grounding or digest mismatch")
    projection = replay_hero_events(remote["event_log"]["events"])
    if projection.accepted_outcome is not accepted:
        raise ValueError("remote replay disagrees")
    if remote["event_log"]["event_count"] != len(remote["event_log"]["events"]):
        raise ValueError("event count mismatch")
    return service


def combine_evidence(mac, remote, restoration, *, allow_fixture=False):
    service = validate_remote(remote, allow_fixture=allow_fixture)
    # The caller must load Mac records through the existing strict loader.
    if (
        mac.get("schema_version") != "hero.live-execution-evidence.v1"
        or mac.get("evidence_level") != "observed"
        or mac["verification"]["accepted_outcome"] is not True
        or mac["cleanup"]["cleanup_success"] is not True
        or mac["input_digest"] != remote["input_digest"]
    ):
        raise ValueError("Mac request or acceptance mismatch")
    if (
        mac["output_digest"] != _digest(mac["output"])
        or _validate_draft(LiveDraft.model_validate(mac["output"]), service)
        or not replay_hero_events(mac["event_log"]["events"]).accepted_outcome
    ):
        raise ValueError("Mac output or replay mismatch")
    actual = mac["actual_execution"]
    usage = mac["usage"]
    calls = actual["model_calls"]
    if (
        type(calls) is not int
        or not 1 <= calls <= 3
        or len(usage) != calls
        or actual["provider_calls"] != 0
        or mac["runtime_identity"].get("network") != "loopback"
        or mac["verification"]["semantic_non_regression"] != "not_measured"
        or mac["B_local_execution"]["semantic_quality_measured"] is not False
        or mac["B_local_execution"]["execution_performed"] is not True
        or any(
            type(x.get("tokens_out")) is not int or not 0 <= x["tokens_out"] <= 256
            for x in usage
        )
    ):
        raise ValueError("Mac accounting or boundary invalid")
    restored = (
        restoration.get("lease_id") == remote["lease_id"]
        and restoration.get("owned_unit_stopped") is True
        and restoration.get("restored_health") is True
        and restoration.get("restored_model") == "openai/gpt-oss-120b"
        and restoration.get("lease_released") is True
        and restoration.get("foreign_work_preserved") is True
    )
    accepted = remote["verification"]["objective_pass"] and restored
    refs = {
        "mac": _digest(mac),
        "h100": _digest(remote),
        "restoration": _digest(restoration),
    }
    log = RemoteEvents(
        "hero-s02-integrated-" + remote["run_id"],
        _digest(refs),
        "fixture" if remote["evidence_level"] == "fixture" else "observed",
    )
    log.emit("run.started", "intake", "running")
    log.emit(
        "graph.created",
        "decompose",
        "completed",
        payload={
            "mode": "retained_mac_plus_new_h100_evidence",
            "concurrent_execution_proven": False,
        },
    )
    for task, label in [
        ("mac", "Validated retained Mac output"),
        ("h100", "Retained owned H100 output"),
    ]:
        log.begin(task, label, executor="exact_reuse", adapter="retained_evidence")
        log.emit(
            "task.completed",
            "execute",
            "completed",
            task=task,
            payload={"evidence_digest": refs[task], "new_model_calls": 0},
        )
    log.begin("review", "Independent evidence and restoration review", ("mac", "h100"))
    if accepted:
        log.emit("task.completed", "execute", "completed", task="review")
        log.emit("merge.started", "merge", "running")
        log.emit(
            "merge.completed",
            "merge",
            "completed",
            payload={"answer": remote["output"]},
        )
        log.emit("verification.started", "verify", "running")
        log.emit("verification.passed", "verify", "completed")
        log.emit("run.completed", "complete", "completed")
    else:
        log.emit(
            "task.failed",
            "execute",
            "failed",
            task="review",
            payload={"reason_code": "remote_execution_or_restoration_failed"},
        )
        log.emit(
            "run.escalated",
            "escalate",
            "escalated",
            payload={"automatic_fallback": False},
        )
    return {
        "schema_version": "hero.hybrid-evidence.v1",
        "evidence_level": log.level,
        "run_id": log.log.run_id,
        "accepted_outcome": accepted,
        "source_digests": refs,
        "mac": deepcopy(mac),
        "h100": deepcopy(remote),
        "restoration": deepcopy(restoration),
        "event_log": log.log.snapshot(),
        "claim_boundary": "Retained Mac output and separately measured owned H100 output. Sequential evidence integration; simultaneous multi-device execution, semantic quality, production behavior and 2x/3x benefits are not established.",
    }


def load_hybrid_evidence(path):
    data = read_record(path)
    if data.get("schema_version") != "hero.hybrid-evidence.v1":
        raise ValueError("unknown integrated evidence")
    rebuilt = combine_evidence(data["mac"], data["h100"], data["restoration"])
    # Rebuilding emits fresh timestamps/run events, so compare all derived
    # acceptance, provenance and source fields and independently replay events.
    for key in (
        "accepted_outcome",
        "source_digests",
        "evidence_level",
        "run_id",
        "claim_boundary",
    ):
        if data.get(key) != rebuilt[key]:
            raise ValueError("derived evidence mismatch")
    actual_log, expected_log = data["event_log"], rebuilt["event_log"]
    for key in ("schema_version", "run_id", "event_count"):
        if actual_log.get(key) != expected_log[key]:
            raise ValueError("integrated log identity mismatch")
    # Only timestamps vary when rebuilding retained evidence. Bind every other
    # event field, including answers, task labels and provenance, to the sources.
    def stable_events(log):
        return [
            {key: value for key, value in event.items() if key != "occurred_at"}
            for event in log["events"]
        ]

    if _digest(stable_events(actual_log)) != _digest(stable_events(expected_log)):
        raise ValueError("integrated event/source mismatch")
    projection = replay_hero_events(actual_log["events"])
    if (
        projection.accepted_outcome is not data["accepted_outcome"]
        or actual_log.get("projection") != projection.model_dump(mode="json")
    ):
        raise ValueError("integrated replay projection mismatch")
    return data


def hybrid_payload(environ=None):
    configured = (os.environ if environ is None else environ).get(ENV, "").strip()
    if not configured:
        return {"available": False, "status": "not_configured"}
    data = load_hybrid_evidence(configured)
    mac, remote = data["mac"], data["h100"]
    return {
        "available": True,
        "run_id": data["run_id"],
        "accepted_outcome": data["accepted_outcome"],
        "claim_boundary": data["claim_boundary"],
        "source_digests": data["source_digests"],
        "mac": {
            "output": mac["output"],
            "recorded_at": mac["recorded_at"],
            "model_calls": mac["actual_execution"]["model_calls"],
            "usage": mac["usage"],
            "mode": "retained_observed",
        },
        "h100": {
            "output": remote["output"],
            "recorded_at": remote["recorded_at"],
            "model_calls": remote["actual_execution"]["owned_remote_model_calls"],
            "usage": remote["attempts"],
            "runtime_identity": remote["runtime_identity"],
            "plan": remote["plan"],
            "privacy_mode": "private_network",
        },
        "restoration": {
            k: data["restoration"].get(k)
            for k in [
                "owned_unit_stopped",
                "restored_health",
                "restored_model",
                "lease_released",
            ]
        },
        "event_log": data["event_log"],
        "semantic_quality": "not_measured",
        "commercial_provider_calls": 0,
    }


def compose_files(mac_path, remote_path, restoration_path, output_path):
    result = combine_evidence(
        load_live_evidence(mac_path),
        read_record(remote_path),
        read_record(restoration_path),
    )
    target = Path(output_path)
    if target.exists():
        raise ValueError("output already exists")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    )
    return result
