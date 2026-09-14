"""Fixture-only adapter review using canonical mock sessions and Hero event replay."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from kora.hero_contracts import (
    HardwareProfile,
    HeroEvent,
    ModelResourceProfile,
    WorkloadRequirements,
)
from kora.hero_event_log import HeroEventLog
from kora.hero_planner import build_hero_planning_bundle
from kora.hero_runtime_adapter_v2 import (
    MockRuntimeSession,
    MockScript,
    MockTelemetry,
    adapter_descriptor,
    check_plan_compatibility,
)

SCENARIOS = (
    "success",
    "cancelled",
    "load_failed",
    "execute_failed",
    "finish_failed",
    "cleanup_failed_then_retried",
    "placement_unresolved",
)
NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)
GIB = 1024**3


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def review_inputs(scenario: str) -> dict[str, Any]:
    """Synthetic profiles only; no runtime discovery or artifact reads."""
    if scenario not in SCENARIOS:
        raise ValueError("unknown adapter review scenario")
    pc = scenario == "placement_unresolved"
    adapter = "llama.cpp" if pc else "mlx-lm"
    hardware = HardwareProfile(
        profile_id=f"adapter-review-hardware-{scenario}",
        captured_at=NOW,
        platform="linux" if pc else "darwin",
        architecture="x86_64" if pc else "arm64",
        memory_domains=[
            {
                "domain_id": "host",
                "kind": "system" if pc else "unified",
                "total_bytes": 32 * GIB,
                "source": "fixture",
            },
            *(
                [
                    {
                        "domain_id": "gpu",
                        "kind": "dedicated_gpu",
                        "total_bytes": 8 * GIB,
                        "source": "fixture",
                    }
                ]
                if pc
                else []
            ),
        ],
        runtime_candidates=[adapter],
        evidence_level="fixture",
    )
    model = ModelResourceProfile(
        profile_id=f"adapter-review-model-{scenario}",
        model_id="Synthetic review model",
        artifact_id="fixture-artifact",
        artifact_format="gguf" if pc else "safetensors",
        quantization="fixture-only",
        artifact_bytes=20 * GIB,
        model_weight_bytes=18 * GIB,
        sha256="a" * 64,
        source_revision="fixture-v1",
        evidence_level="fixture",
    )
    workload = WorkloadRequirements(
        workload_class="adapter_lifecycle_review",
        context_tokens=4096,
        max_output_tokens=64,
        estimated_kv_bytes=GIB,
        runtime_reserve_bytes=GIB,
        allow_network=False,
    )
    bundle = build_hero_planning_bundle(
        run_id=f"hero-adapter-review-{scenario}-v1",
        plan_id=f"review-plan-{scenario}",
        occurred_at=NOW,
        hardware=hardware,
        model=model,
        workload=workload,
    )
    return {
        "descriptor": adapter_descriptor(adapter, mode="mock"),
        "bundle": bundle,
        "hardware": hardware,
        "model": model,
        "workload": workload,
    }


class AdapterReview:
    """Atomic event projection; adapter state never promotes canonical acceptance.

    Inputs bind the complete plan and mock script. Known events must have exactly
    the expected identity, payload and legal lifecycle transition. Unknown extension
    events remain visible in the canonical log without updating adapter state.
    """

    def __init__(self, inputs: dict[str, Any], script: MockScript):
        self.inputs = deepcopy(inputs)
        self.script = MockScript.model_validate(script.model_dump(mode="json"))
        compatibility = check_plan_compatibility(**self.inputs)
        self.compatibility = compatibility
        self.identity = deepcopy(compatibility.runtime_identity)
        if self.identity is not None:
            self.identity["mock_script_digest"] = hashlib.sha256(
                _json(self.script.model_dump(mode="json")).encode()
            ).hexdigest()
        self.log = HeroEventLog(self.inputs["bundle"].events[0].run_id)
        self.state = "new" if compatibility.compatible else "blocked"
        self.outcome: str | None = None
        self.allocated = False
        self.telemetry: dict[str, Any] | None = None
        self.output: str | None = None
        self.failures: list[dict[str, Any]] = []

    def append(self, raw: HeroEvent | dict[str, Any]) -> dict[str, Any]:
        event = HeroEvent.model_validate(
            raw.model_dump(mode="json") if isinstance(raw, HeroEvent) else raw
        )
        if event.evidence_level != "fixture":
            raise ValueError("adapter review requires fixture events")
        # Work on copies: malformed events cannot damage the committed projection.
        candidate = deepcopy(self)
        candidate._apply(event)
        projection = candidate.log.append(event)
        self.__dict__.update(candidate.__dict__)
        planned = event.sequence >= len(self.inputs["bundle"].events) - 1
        view = {
            "adapter_state": self.state if planned else "awaiting_plan",
            "mock_outcome": self.outcome,
            "mock_allocation_retained": self.allocated,
            "runtime_identity": deepcopy(self.identity) if planned else None,
            "compatibility": self.compatibility.model_dump(mode="json")
            if planned
            else None,
            "telemetry": deepcopy(self.telemetry),
            "output": self.output,
            "failures": deepcopy(self.failures),
            "accepted_outcome": False,
            "service_acceptance": "not_measured",
            "semantic_non_regression": "not_measured",
            "A_workload_control": {"actual_model_calls": 0, "actual_provider_calls": 0},
            "B_local_execution": {
                "execution_performed": False,
                "physical_telemetry": None,
            },
        }
        return {
            "event": event.model_dump(mode="json"),
            "projection": projection.model_dump(mode="json"),
            "view": view,
        }

    def _apply(self, event: HeroEvent) -> None:
        planning = self.inputs["bundle"].events
        if event.sequence < len(planning):
            if _json(event.model_dump(mode="json")) != _json(
                planning[event.sequence].model_dump(mode="json")
            ):
                raise ValueError("planning event mismatch")
            return
        kind = event.event_type
        known = {
            "adapter.prepared",
            "adapter.started",
            "adapter.completed",
            "adapter.cancelled",
            "adapter.load.failed",
            "adapter.execute.failed",
            "adapter.finish.failed",
            "adapter.cleanup.failed",
            "adapter.cleaned",
            "telemetry.sampled",
        }
        if kind not in known:
            # Only future extensions may pass. Core task/run/verification events
            # cannot turn this review into an accepted service execution.
            if kind.startswith("adapter.") and event.task_id is None:
                return
            raise ValueError("unsupported event in adapter review")
        if self.identity is None:
            raise ValueError("blocked compatibility cannot emit lifecycle events")
        old = self.state
        # A scripted fault is mandatory on its first eligible operation.
        operation = {
            "adapter.prepared": "load",
            "adapter.started": "execute",
            "telemetry.sampled": "finish",
            "adapter.completed": "finish",
            "adapter.cleaned": "cleanup",
        }.get(kind)
        if (
            operation == self.script.fail_at
            and not self.failures
            and operation is not None
        ):
            raise ValueError("scripted failure was skipped")
        extra: dict[str, Any] = {}
        status = "completed"
        if kind == "adapter.prepared" and old == "new":
            self.state, self.allocated, status = "prepared", True, "ready"
        elif kind == "adapter.started" and old == "prepared":
            self.state, status = "running", "running"
        elif (
            kind == "telemetry.sampled" and old == "running" and self.telemetry is None
        ):
            self.telemetry = self.script.telemetry.model_dump(mode="json")
            extra["telemetry"] = self.telemetry
            status = "running"
        elif (
            kind == "adapter.completed"
            and old == "running"
            and self.telemetry is not None
        ):
            self.state, self.outcome, self.output = (
                "completed",
                "completed",
                self.script.output,
            )
            extra["output"] = self.output
        elif kind == "adapter.cancelled" and old in {"new", "prepared", "running"}:
            self.state, self.outcome, status = "cancelled", "cancelled", "failed"
            extra["reason_code"] = "mock_cancelled"
        elif kind in {
            "adapter.load.failed",
            "adapter.execute.failed",
            "adapter.finish.failed",
        }:
            operation = kind.split(".")[1]
            if (
                old
                != {"load": "new", "execute": "prepared", "finish": "running"}[
                    operation
                ]
            ):
                raise ValueError("illegal adapter failure order")
            if self.script.fail_at != operation or self.failures:
                raise ValueError("unscripted adapter failure")
            self.state, self.outcome, self.allocated, status = (
                "failed",
                "failed",
                True,
                "failed",
            )
            extra["reason_code"] = f"mock_{operation}_failure"
        elif kind == "adapter.cleanup.failed" and old in {
            "new",
            "prepared",
            "completed",
            "failed",
            "cancelled",
        }:
            if self.script.fail_at != "cleanup" or self.failures:
                raise ValueError("unscripted cleanup failure")
            self.state, status = "cleanup_failed", "failed"
            extra["reason_code"] = "mock_cleanup_failure"
        elif kind == "adapter.cleaned" and old in {
            "new",
            "prepared",
            "completed",
            "failed",
            "cancelled",
            "cleanup_failed",
        }:
            self.state, self.allocated = "closed", False
            extra["outcome"] = self.outcome
        else:
            raise ValueError("illegal adapter lifecycle order")
        expected_payload = {
            "mode": "mock",
            "runtime_identity": self.identity,
            "state": self.state,
            "mock_allocation_retained": self.allocated,
            "actual_model_calls": 0,
            "actual_provider_calls": 0,
            "runtime_started": False,
            **extra,
        }
        expected_refs = [
            f"sha256:{self.identity['planning_digest']}",
            f"sha256:{self.identity['descriptor_digest']}",
            f"sha256:{self.identity['model_artifact_sha256']}",
        ]
        if (
            _json(event.payload) != _json(expected_payload)
            or event.adapter_id != self.identity["adapter_id"]
            or event.executor_class != "local_ai"
            or event.source != "kora.hero_runtime_adapter_v2"
            or event.phase != "execute"
            or event.status != status
            or event.occurred_at != planning[-1].occurred_at
            or event.task_id is not None
            or event.parent_task_id is not None
            or event.attempt is not None
            or list(event.evidence_refs) != expected_refs
        ):
            raise ValueError("adapter identity or payload mismatch")
        if kind.endswith(".failed") or kind == "adapter.cancelled":
            self.failures.append(
                {
                    "sequence": event.sequence,
                    "event_type": kind,
                    "reason_code": extra["reason_code"],
                }
            )


def build_adapter_review_fixture(scenario: str = "success") -> dict[str, Any]:
    inputs = review_inputs(scenario)
    fail_at = {
        "load_failed": "load",
        "execute_failed": "execute",
        "finish_failed": "finish",
        "cleanup_failed_then_retried": "cleanup",
    }.get(scenario)
    script = MockScript(
        output="Supplied mock response. Service quality has not been measured.",
        telemetry=MockTelemetry(input_tokens=16, output_tokens=8),
        fail_at=fail_at,
    )
    review = AdapterReview(inputs, script)
    if review.compatibility.compatible:
        session = MockRuntimeSession(**inputs, script=script)
        session.load()
        if session.state == "prepared":
            session.execute()
        if session.state == "running":
            if scenario == "cancelled":
                session.cancel()
            else:
                session.finish()
        session.cleanup()
        if session.state == "cleanup_failed":
            session.cleanup()
        events = session.events_after()
    else:
        # No session or mock allocation is created for unresolved placement.
        events = inputs["bundle"].events
    frames = [review.append(event) for event in events]
    digest = hashlib.sha256(_json([f["event"] for f in frames]).encode()).hexdigest()
    return {
        "schema_version": "hero.studio-adapter-review.v1",
        "scenario": scenario,
        "run_id": events[0].run_id,
        "evidence_level": "fixture",
        "event_count": len(events),
        "event_digest": digest,
        "frames": frames,
        "mock_script": script.model_dump(mode="json"),
        "planning_bundle": inputs["bundle"].model_dump(mode="json"),
        "actual_execution": {
            "runtime_starts": 0,
            "model_calls": 0,
            "provider_calls": 0,
        },
        "claim_boundary": "Mock fixture replay only; no execution or service-quality evidence.",
    }


def adapter_event_payload(scenario: str, after: int = -1) -> dict[str, Any]:
    fixture = build_adapter_review_fixture(scenario)
    if type(after) is not int or after < -1 or after >= fixture["event_count"]:
        raise ValueError("invalid adapter event cursor")
    return {
        "run_id": fixture["run_id"],
        "evidence_level": "fixture",
        "frames": fixture["frames"][after + 1 :],
        "event_count": fixture["event_count"],
    }
