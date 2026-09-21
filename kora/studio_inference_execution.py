"""Read-only Studio projection for observed Inference -> Execution evidence."""

from __future__ import annotations

import hashlib
import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

INFERENCE_EXECUTION_EVIDENCE_ENV = "KORA_INFERENCE_EXECUTION_EVIDENCE_PATH"
MAX_INFERENCE_EXECUTION_EVIDENCE_BYTES = 2 * 1024 * 1024
SCHEMA_VERSION = "kora.inference-execution-studio-evidence.v1"

_EVENT_STATES = {
    "model.intelligence.started": "MODEL INTELLIGENCE",
    "compile.observation.accepted": "OBSERVING REPEAT",
    "compile.candidate.created": "PATTERN / CANDIDATE",
    "compile.validation.started": "VALIDATING",
    "compile.candidate.activated": "VERIFIED / ACTIVATED",
    "compiled.execution.started": "KNOWN — KORA EXECUTION",
    "compiled.execution.completed": "MODEL CALLS 0",
    "run.paused.safely": "MODEL OFFLINE — TASK PAUSED SAFELY",
}
_ALLOWED_EVENT_NAMES = {
    "workload.classified",
    "model.intelligence.started",
    "model.intelligence.completed",
    "compile.observation.accepted",
    "compile.candidate.created",
    "compile.validation.started",
    "compile.validation.passed",
    "compile.validation.failed",
    "compile.candidate.activated",
    "compile.candidate.deactivated",
    "compiled.execution.started",
    "verification.started",
    "verification.passed",
    "verification.failed",
    "compiled.execution.completed",
    "run.paused.safely",
}


class StudioInferenceExecutionEvidenceError(ValueError):
    """Configured evidence violated the read-only Studio contract."""


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _reject_sensitive_payload(value: Any) -> None:
    blocked_keys = {
        "raw_request",
        "raw_response",
        "model_content",
        "token_file",
        "worker_token",
        "prompt",
        "system_prompt",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).casefold() in blocked_keys:
                raise StudioInferenceExecutionEvidenceError(
                    "scrubbed evidence contains a forbidden field"
                )
            _reject_sensitive_payload(item)
    elif isinstance(value, list):
        for item in value:
            _reject_sensitive_payload(item)
    elif isinstance(value, str):
        lowered = value.casefold()
        if (
            "/volumes/" in lowered
            or "/users/" in lowered
            or "worker.token" in lowered
        ):
            raise StudioInferenceExecutionEvidenceError(
                "scrubbed evidence contains a private local path"
            )


def _disabled() -> dict[str, Any]:
    return {
        "schema_version": "kora.inference-execution-studio-view.v1",
        "available": False,
        "status": "not_configured",
        "claim_boundary": (
            "No Inference -> Execution evidence path is configured. Studio only "
            "reads an explicitly supplied scrubbed evidence file and never starts "
            "a model, runtime, provider, compiler, or benchmark."
        ),
    }


def _bounded_nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise StudioInferenceExecutionEvidenceError(f"invalid {name}")
    return value


def _bounded_ms_list(value: Any, name: str) -> list[float]:
    if not isinstance(value, list) or len(value) > 10000:
        raise StudioInferenceExecutionEvidenceError(f"invalid {name}")
    result: list[float] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, (int, float)) or item < 0:
            raise StudioInferenceExecutionEvidenceError(f"invalid {name}")
        result.append(float(item))
    return result


def _project_states(events: list[dict[str, Any]]) -> list[str]:
    states: list[str] = []
    expected_sequence = 1
    for event in events:
        if not isinstance(event, dict):
            raise StudioInferenceExecutionEvidenceError("event must be an object")
        if set(event) != {"sequence", "name", "payload"}:
            raise StudioInferenceExecutionEvidenceError("event fields are invalid")
        sequence = event["sequence"]
        name = event["name"]
        payload = event["payload"]
        if sequence != expected_sequence:
            raise StudioInferenceExecutionEvidenceError("event sequence is not contiguous")
        expected_sequence += 1
        if name not in _ALLOWED_EVENT_NAMES or not isinstance(payload, dict):
            raise StudioInferenceExecutionEvidenceError("unsupported event")
        if name == "workload.classified":
            classification = payload.get("classification")
            if classification == "NEW":
                states.append("NEW")
            elif classification == "UNKNOWN":
                states.append("OOD / UNKNOWN — MODEL REQUIRED")
            elif classification != "KNOWN":
                raise StudioInferenceExecutionEvidenceError("invalid workload classification")
        elif name in _EVENT_STATES:
            states.append(_EVENT_STATES[name])
    return states


def load_inference_execution_evidence(
    path: str | os.PathLike[str],
) -> dict[str, Any]:
    """Load one scrubbed observed-evidence record without following symlinks."""

    target = Path(path).expanduser()
    if target.is_symlink() or not target.is_file():
        raise StudioInferenceExecutionEvidenceError(
            "evidence must be a regular non-symlink file"
        )
    size = target.stat().st_size
    if size <= 0 or size > MAX_INFERENCE_EXECUTION_EVIDENCE_BYTES:
        raise StudioInferenceExecutionEvidenceError("evidence size is outside the allowed bound")
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StudioInferenceExecutionEvidenceError(
            "evidence is not valid UTF-8 JSON"
        ) from exc
    if not isinstance(payload, dict):
        raise StudioInferenceExecutionEvidenceError("evidence must be a JSON object")
    _reject_sensitive_payload(payload)

    required = {
        "schema_version",
        "evidence_level",
        "recorded_at",
        "claim_boundary",
        "model_identity",
        "model_accounting",
        "candidate",
        "activation",
        "counters",
        "timings_ms",
        "events",
        "event_digest",
        "accepted",
    }
    if set(payload) != required:
        raise StudioInferenceExecutionEvidenceError("evidence fields are invalid")
    if payload["schema_version"] != SCHEMA_VERSION or payload["evidence_level"] != "observed":
        raise StudioInferenceExecutionEvidenceError("unsupported evidence schema or level")
    if not isinstance(payload["recorded_at"], str) or not payload["recorded_at"]:
        raise StudioInferenceExecutionEvidenceError("recorded_at is required")
    if not isinstance(payload["claim_boundary"], str) or not payload["claim_boundary"]:
        raise StudioInferenceExecutionEvidenceError("claim boundary is required")
    if payload["accepted"] is not True:
        raise StudioInferenceExecutionEvidenceError("only accepted observed evidence is displayable")

    model_identity = payload["model_identity"]
    if not isinstance(model_identity, dict):
        raise StudioInferenceExecutionEvidenceError("model identity is invalid")
    expected_identity = {
        "model_repository",
        "model_revision",
        "artifact_sha256",
        "runtime_commit",
        "quantization",
        "context_tokens",
        "concurrency",
        "prefix_cache",
        "thinking",
        "tokenizer_sha256",
        "template_sha256",
        "verification",
    }
    if set(model_identity) != expected_identity:
        raise StudioInferenceExecutionEvidenceError("model identity fields are invalid")
    if not all(isinstance(model_identity[key], str) and model_identity[key] for key in (
        "model_repository",
        "model_revision",
        "artifact_sha256",
        "runtime_commit",
        "quantization",
        "prefix_cache",
        "tokenizer_sha256",
        "template_sha256",
        "verification",
    )):
        raise StudioInferenceExecutionEvidenceError("model identity strings are invalid")
    _bounded_nonnegative_int(model_identity["context_tokens"], "context_tokens")
    _bounded_nonnegative_int(model_identity["concurrency"], "concurrency")
    if not isinstance(model_identity["thinking"], bool):
        raise StudioInferenceExecutionEvidenceError("thinking must be boolean")

    model_accounting = payload["model_accounting"]
    if not isinstance(model_accounting, dict) or set(model_accounting) != {
        "calls", "input_tokens", "output_tokens", "reasoning_tokens", "token_source"
    }:
        raise StudioInferenceExecutionEvidenceError("model accounting is invalid")
    calls = _bounded_nonnegative_int(model_accounting["calls"], "model calls")
    _bounded_nonnegative_int(model_accounting["input_tokens"], "input tokens")
    _bounded_nonnegative_int(model_accounting["output_tokens"], "output tokens")
    reasoning = model_accounting["reasoning_tokens"]
    if reasoning is not None:
        _bounded_nonnegative_int(reasoning, "reasoning tokens")
    if model_accounting["token_source"] != "engine-reported":
        raise StudioInferenceExecutionEvidenceError("token accounting must be engine-reported")

    candidate = payload["candidate"]
    if not isinstance(candidate, dict) or set(candidate) != {
        "digest", "automatic_from_live_observations", "deterministic_repeat_equal"
    }:
        raise StudioInferenceExecutionEvidenceError("candidate evidence is invalid")
    if (
        not isinstance(candidate["digest"], str)
        or len(candidate["digest"]) != 64
        or candidate["automatic_from_live_observations"] is not True
        or candidate["deterministic_repeat_equal"] is not True
    ):
        raise StudioInferenceExecutionEvidenceError("candidate acceptance is incomplete")

    activation = payload["activation"]
    if not isinstance(activation, dict) or set(activation) != {
        "passed", "raw_overlap_count", "normalized_overlap_count"
    }:
        raise StudioInferenceExecutionEvidenceError("activation evidence is invalid")
    if activation["passed"] is not True:
        raise StudioInferenceExecutionEvidenceError("candidate activation did not pass")
    if (
        _bounded_nonnegative_int(activation["raw_overlap_count"], "raw overlap") != 0
        or _bounded_nonnegative_int(
            activation["normalized_overlap_count"], "normalized overlap"
        )
        != 0
    ):
        raise StudioInferenceExecutionEvidenceError("activation overlap must be zero")

    counters = payload["counters"]
    required_counters = {
        "model_calls",
        "compiled_executions",
        "exact_reuse_hits",
        "unknown_or_ood_escalations",
        "safe_pauses",
        "ood_silent_deterministic_success",
    }
    if not isinstance(counters, dict) or set(counters) != required_counters:
        raise StudioInferenceExecutionEvidenceError("counter set is invalid")
    for key in required_counters:
        _bounded_nonnegative_int(counters[key], key)
    if counters["model_calls"] != calls:
        raise StudioInferenceExecutionEvidenceError("model call counters disagree")
    if counters["compiled_executions"] < 1:
        raise StudioInferenceExecutionEvidenceError("compiled execution proof is missing")
    if counters["exact_reuse_hits"] != 0:
        raise StudioInferenceExecutionEvidenceError("compiled proof used exact reuse")
    if counters["ood_silent_deterministic_success"] != 0:
        raise StudioInferenceExecutionEvidenceError("silent OOD success must be zero")

    timings = payload["timings_ms"]
    required_timings = {
        "model_intelligence",
        "candidate_generation",
        "candidate_validation",
        "compiled_execution",
        "verification",
        "end_to_end",
    }
    if not isinstance(timings, dict) or set(timings) != required_timings:
        raise StudioInferenceExecutionEvidenceError("timing set is invalid")
    for key in required_timings:
        _bounded_ms_list(timings[key], key)
    if not timings["model_intelligence"] or not timings["compiled_execution"]:
        raise StudioInferenceExecutionEvidenceError("required measured timings are missing")

    events = payload["events"]
    if not isinstance(events, list) or not events or len(events) > 10000:
        raise StudioInferenceExecutionEvidenceError("event list is invalid")
    projected = _project_states(events)
    required_states = {
        "NEW",
        "MODEL INTELLIGENCE",
        "OBSERVING REPEAT",
        "PATTERN / CANDIDATE",
        "VALIDATING",
        "VERIFIED / ACTIVATED",
        "KNOWN — KORA EXECUTION",
        "MODEL CALLS 0",
        "OOD / UNKNOWN — MODEL REQUIRED",
        "MODEL OFFLINE — TASK PAUSED SAFELY",
    }
    if not required_states.issubset(set(projected)):
        raise StudioInferenceExecutionEvidenceError("required Studio states are missing")
    event_digest = payload["event_digest"]
    if not isinstance(event_digest, str) or len(event_digest) != 64:
        raise StudioInferenceExecutionEvidenceError("event digest is invalid")
    actual_event_digest = hashlib.sha256(_canonical_json(events)).hexdigest()
    if event_digest != actual_event_digest:
        raise StudioInferenceExecutionEvidenceError("event digest does not match events")

    return deepcopy(payload)


def inference_execution_payload(
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return a path-free Studio view for one configured evidence record."""

    values = os.environ if environ is None else environ
    configured = values.get(INFERENCE_EXECUTION_EVIDENCE_ENV, "").strip()
    if not configured:
        return _disabled()
    evidence = load_inference_execution_evidence(configured)
    states = _project_states(evidence["events"])
    return {
        "schema_version": "kora.inference-execution-studio-view.v1",
        "available": True,
        "status": "objective_pass",
        "recorded_at": evidence["recorded_at"],
        "claim_boundary": evidence["claim_boundary"],
        "model_identity": evidence["model_identity"],
        "model_accounting": evidence["model_accounting"],
        "candidate": evidence["candidate"],
        "activation": evidence["activation"],
        "counters": evidence["counters"],
        "timings_ms": evidence["timings_ms"],
        "event_count": len(evidence["events"]),
        "event_digest": evidence["event_digest"],
        "studio_states": states,
    }


__all__ = [
    "INFERENCE_EXECUTION_EVIDENCE_ENV",
    "MAX_INFERENCE_EXECUTION_EVIDENCE_BYTES",
    "SCHEMA_VERSION",
    "StudioInferenceExecutionEvidenceError",
    "inference_execution_payload",
    "load_inference_execution_evidence",
]
