"""Fixture-only bridge from a Hero plan to one canonical task/event stream.

No executable runtime, model, provider, subprocess, host probe, or network
client is imported or invoked here.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Literal

from kora.hero_contracts import (
    ExecutorClass,
    HardwareProfile,
    HeroEvent,
    HeroPhase,
    HeroStatus,
    ModelResourceProfile,
    WorkloadRequirements,
)
from kora.hero_event_log import HeroEventLog
from kora.hero_planner import HeroPlanningBundle
from kora.hero_runtime_adapter_v2 import (
    MockRuntimeSession,
    MockScript,
    MockTelemetry,
    adapter_descriptor,
    check_plan_compatibility,
)

MockExecutionScenario = Literal[
    "success",
    "quality_failed",
    "cancelled",
    "load_failed",
    "execute_failed",
    "finish_failed",
    "cleanup_failed_then_retried",
    "replanned",
]
MOCK_EXECUTION_SCENARIOS = (
    "success",
    "quality_failed",
    "cancelled",
    "load_failed",
    "execute_failed",
    "finish_failed",
    "cleanup_failed_then_retried",
    "replanned",
)


class MockExecutionBridgeError(ValueError):
    """Stable fail-closed error raised before a mock task can start."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class _Task:
    task_id: str
    label: str
    purpose: str
    dependencies: tuple[str, ...]
    executor_class: ExecutorClass
    adapter_id: str


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _tasks(selected_adapter_id: str) -> tuple[_Task, ...]:
    return (
        _Task(
            "facts",
            "Check supplied facts",
            "Apply the supplied structural rules.",
            (),
            "deterministic",
            "deterministic_core",
        ),
        _Task(
            "reuse",
            "Reuse approved brand notes",
            "Reuse an exact matching approved input.",
            (),
            "exact_reuse",
            "exact_reuse_store",
        ),
        _Task(
            "draft",
            "Draft the launch summary",
            "Combine checked facts with approved notes.",
            ("facts", "reuse"),
            "local_ai",
            selected_adapter_id,
        ),
        _Task(
            "review",
            "Independent review",
            "Apply the supplied fixture service gate without a provider call.",
            ("draft",),
            "frontier_ai",
            "frontier_provider_fixture",
        ),
    )


class _Bridge:
    def __init__(
        self,
        *,
        bundle: HeroPlanningBundle,
        hardware: HardwareProfile,
        model: ModelResourceProfile,
        workload: WorkloadRequirements,
        scenario: MockExecutionScenario,
    ) -> None:
        if scenario not in MOCK_EXECUTION_SCENARIOS:
            raise MockExecutionBridgeError("unknown_mock_execution_scenario")
        self.bundle = HeroPlanningBundle.model_validate(bundle.model_dump(mode="json"))
        self.hardware = HardwareProfile.model_validate(hardware.model_dump(mode="json"))
        self.model = ModelResourceProfile.model_validate(model.model_dump(mode="json"))
        self.workload = WorkloadRequirements.model_validate(
            workload.model_dump(mode="json")
        )
        self.scenario = scenario
        self.at = self.bundle.events[-1].occurred_at
        self.log = HeroEventLog(self.bundle.events[0].run_id)
        self.local_results: list[dict[str, Any]] = []
        self.runtime_identity: dict[str, Any] | None = None
        self.compatibility: dict[str, Any] | None = None

    def emit(
        self,
        event_type: str,
        phase: HeroPhase,
        status: HeroStatus,
        *,
        task_id: str | None = None,
        attempt: int | None = None,
        executor_class: ExecutorClass | None = None,
        adapter_id: str | None = None,
        evidence_refs: tuple[str, ...] = (),
        payload: dict[str, Any] | None = None,
    ) -> None:
        projection = self.log.projection
        sequence = 0 if projection is None else projection.last_sequence + 1
        self.log.append(
            HeroEvent(
                event_id=f"{self.log.run_id}:{sequence:04d}",
                run_id=self.log.run_id,
                sequence=sequence,
                occurred_at=self.at,
                event_type=event_type,
                phase=phase,
                status=status,
                source="kora.hero_mock_execution",
                evidence_level="fixture",
                task_id=task_id,
                attempt=attempt,
                executor_class=executor_class,
                adapter_id=adapter_id,
                evidence_refs=evidence_refs,
                payload={
                    "fixture_only": True,
                    "actual_model_calls": 0,
                    "actual_provider_calls": 0,
                    "runtime_started": False,
                    **(payload or {}),
                },
            )
        )

    def reject(self, reason_code: str) -> None:
        self.emit(
            "run.failed",
            "fail",
            "failed",
            evidence_refs=(f"sha256:{self.bundle.evidence_digest}",),
            payload={
                "reason": reason_code,
                "reason_code": reason_code,
                "execution_gate": "before_graph_and_task_start",
            },
        )

    def import_adapter_events(
        self, session: MockRuntimeSession, *, task_id: str, attempt: int
    ) -> None:
        for original in session.events_after(len(self.bundle.events) - 1):
            projection = self.log.projection
            assert projection is not None
            sequence = projection.last_sequence + 1
            payload = deepcopy(original.payload)
            payload["task_event_bridge"] = {
                "task_id": task_id,
                "attempt": attempt,
                "plan_id": self.bundle.plan.plan_id,
                "planning_digest": self.bundle.evidence_digest,
                "effective_config_digest": _digest(
                    self.bundle.plan.effective_config
                ),
            }
            self.log.append(
                original.model_copy(
                    update={
                        "event_id": f"{self.log.run_id}:{sequence:04d}",
                        "sequence": sequence,
                        "task_id": task_id,
                        "attempt": attempt,
                        "payload": payload,
                    },
                    deep=True,
                )
            )

    def task_started(self, task: _Task, *, attempt: int = 1) -> None:
        refs = (f"sha256:{self.bundle.evidence_digest}",)
        self.emit(
            "task.ready",
            "execute",
            "ready",
            task_id=task.task_id,
            attempt=attempt,
            evidence_refs=refs,
        )
        self.emit(
            "task.routed",
            "plan",
            "ready",
            task_id=task.task_id,
            attempt=attempt,
            executor_class=task.executor_class,
            adapter_id=task.adapter_id,
            evidence_refs=refs,
            payload={
                "plan_id": self.bundle.plan.plan_id,
                "selected_adapter_id": self.bundle.plan.selected_adapter_id,
            },
        )
        local = task.executor_class == "local_ai"
        self.emit(
            "task.started",
            "execute",
            "running",
            task_id=task.task_id,
            attempt=attempt,
            executor_class=task.executor_class,
            adapter_id=task.adapter_id,
            evidence_refs=refs,
            payload={
                "execution_mode": "mock" if local else "supplied_fixture",
                "effective_config": (
                    deepcopy(self.bundle.plan.effective_config) if local else None
                ),
                "effective_config_digest": (
                    _digest(self.bundle.plan.effective_config) if local else None
                ),
            },
        )

    def complete_supplied_task(self, task: _Task) -> None:
        self.task_started(task)
        self.emit(
            "task.completed",
            "execute",
            "completed",
            task_id=task.task_id,
            attempt=1,
            executor_class=task.executor_class,
            adapter_id=task.adapter_id,
            payload={"result": f"Illustrative output: {task.label}."},
        )

    def run_local_attempt(
        self,
        task: _Task,
        *,
        attempt: int,
        scenario: MockExecutionScenario,
    ) -> bool:
        fail_at = {
            "load_failed": "load",
            "execute_failed": "execute",
            "finish_failed": "finish",
            "cleanup_failed_then_retried": "cleanup",
        }.get(scenario)
        session = MockRuntimeSession(
            descriptor=adapter_descriptor(task.adapter_id, mode="mock"),
            bundle=self.bundle,
            hardware=self.hardware,
            model=self.model,
            workload=self.workload,
            script=MockScript(
                output=(
                    "Illustrative mock draft. This supplied string was not "
                    "generated by a model."
                ),
                telemetry=MockTelemetry(),
                fail_at=fail_at,
            ),
        )
        self.task_started(task, attempt=attempt)
        session.load()
        if scenario == "cancelled" and session.state == "prepared":
            session.cancel()
        elif session.state == "prepared":
            session.execute()
            if session.state == "running":
                session.finish()
        if session.state in {"completed", "failed", "cancelled", "cleanup_failed"}:
            session.cleanup()
            if session.state == "cleanup_failed":
                session.cleanup()
        self.import_adapter_events(session, task_id=task.task_id, attempt=attempt)
        self.runtime_identity = session.identity
        snapshot = session.snapshot()
        succeeded = snapshot["outcome"] == "completed" and snapshot["state"] == "closed"
        if succeeded:
            result = session.result()
            self.local_results.append(result)
            self.emit(
                "task.completed",
                "execute",
                "completed",
                task_id=task.task_id,
                attempt=attempt,
                executor_class=task.executor_class,
                adapter_id=task.adapter_id,
                payload={
                    "result": result["output"],
                    "adapter_outcome": "mock_completed",
                    "service_acceptance": "not_measured",
                    "semantic_non_regression": "not_measured",
                },
            )
            return True
        reason = (
            "mock_cancelled"
            if snapshot["outcome"] == "cancelled"
            else f"mock_{fail_at}_failure"
            if fail_at
            else "mock_execution_failed"
        )
        self.emit(
            "task.failed",
            "execute",
            "failed",
            task_id=task.task_id,
            attempt=attempt,
            executor_class=task.executor_class,
            adapter_id=task.adapter_id,
            payload={"reason": reason, "reason_code": reason},
        )
        return False

    def run(self) -> dict[str, Any]:
        selected = self.bundle.plan.selected_adapter_id
        if selected is None:
            self.log.extend(deepcopy(self.bundle.events))
            self.compatibility = {
                "compatible": False,
                "reason_codes": ["no_selected_runtime"],
                "live_execution_allowed": False,
            }
            self.reject("no_selected_runtime")
            return self.result()

        descriptor = adapter_descriptor(selected, mode="mock")
        compatibility = check_plan_compatibility(
            descriptor,
            self.bundle,
            self.hardware,
            self.model,
            self.workload,
        )
        self.compatibility = compatibility.model_dump(mode="json")
        if not compatibility.compatible:
            reasons = set(compatibility.reason_codes)
            if reasons != {"placement_unresolved"}:
                raise MockExecutionBridgeError(compatibility.reason_codes[0])
            self.log.extend(deepcopy(self.bundle.events))
            self.reject("placement_unresolved")
            return self.result()

        self.log.extend(deepcopy(self.bundle.events))
        tasks = _tasks(selected)
        self.emit(
            "graph.created",
            "decompose",
            "completed",
            payload={"task_ids": [task.task_id for task in tasks]},
        )
        for task in tasks:
            self.emit(
                "task.created",
                "decompose",
                "created",
                task_id=task.task_id,
                attempt=1,
                payload={
                    "label": task.label,
                    "purpose": task.purpose,
                    "dependencies": list(task.dependencies),
                },
            )
        self.complete_supplied_task(tasks[0])
        self.complete_supplied_task(tasks[1])

        if self.scenario == "replanned":
            first_ok = self.run_local_attempt(
                tasks[2], attempt=1, scenario="execute_failed"
            )
            assert not first_ok
            self.emit(
                "run.replanned",
                "replan",
                "replanned",
                evidence_refs=(f"sha256:{self.bundle.evidence_digest}",),
                payload={
                    "reason": "mock_execute_failure",
                    "reason_code": "mock_execute_failure",
                    "replan_strategy": "bounded_same_plan_retry",
                    "plan_id": self.bundle.plan.plan_id,
                    "planning_digest": self.bundle.evidence_digest,
                },
            )
            self.emit(
                "execution.plan.reaffirmed",
                "replan",
                "replanned",
                evidence_refs=(f"sha256:{self.bundle.evidence_digest}",),
                payload={
                    "plan_id": self.bundle.plan.plan_id,
                    "selected_adapter_id": selected,
                    "effective_config": deepcopy(self.bundle.plan.effective_config),
                    "effective_config_digest": _digest(
                        self.bundle.plan.effective_config
                    ),
                },
            )
            local_ok = self.run_local_attempt(
                tasks[2], attempt=2, scenario="success"
            )
        else:
            local_ok = self.run_local_attempt(
                tasks[2], attempt=1, scenario=self.scenario
            )
        if not local_ok:
            self.emit(
                "run.failed",
                "fail",
                "failed",
                payload={
                    "reason": "local_mock_task_not_completed",
                    "reason_code": "local_mock_task_not_completed",
                },
            )
            return self.result()

        self.complete_supplied_task(tasks[3])
        self.emit("merge.started", "merge", "running")
        self.emit(
            "merge.completed",
            "merge",
            "completed",
            payload={
                "answer": (
                    "Launch brief — illustrative output\n"
                    "Lead with the supplied product facts. Keep the approved brand voice. "
                    "Prepare one concise announcement and retain the evidence behind each claim."
                )
            },
        )
        self.emit("verification.started", "verify", "running")
        passed = self.scenario != "quality_failed"
        self.emit(
            "verification.passed" if passed else "verification.failed",
            "verify",
            "completed" if passed else "failed",
            payload={
                "service_acceptance": "fixture_pass" if passed else "fixture_fail",
                "structural_acceptance": "fixture_pass",
                "semantic_non_regression": "not_measured",
                "reason": (
                    "Synthetic service contract passes."
                    if passed
                    else "Synthetic service-quality failure: required source coverage missing."
                ),
            },
        )
        self.emit(
            "run.completed" if passed else "run.failed",
            "complete" if passed else "fail",
            "completed" if passed else "failed",
        )
        return self.result()

    def result(self) -> dict[str, Any]:
        return {
            "schema_version": "hero.mock-execution-bridge.v1",
            "events": deepcopy(self.log.events_after()),
            "log": self.log.snapshot(),
            "compatibility": deepcopy(self.compatibility),
            "runtime_identity": deepcopy(self.runtime_identity),
            "effective_config": deepcopy(self.bundle.plan.effective_config),
            "effective_config_digest": _digest(self.bundle.plan.effective_config),
            "local_results": deepcopy(self.local_results),
            "accepted_outcome": False,
            "service_acceptance": "not_measured",
            "semantic_non_regression": "not_measured",
            "actual_execution": {
                "runtime_starts": 0,
                "model_calls": 0,
                "provider_calls": 0,
            },
        }


def build_mock_execution_bridge(
    *,
    bundle: HeroPlanningBundle,
    hardware: HardwareProfile,
    model: ModelResourceProfile,
    workload: WorkloadRequirements,
    scenario: MockExecutionScenario = "success",
) -> dict[str, Any]:
    """Build one deterministic fixture-only plan/adapter/task event stream."""

    return _Bridge(
        bundle=bundle,
        hardware=hardware,
        model=model,
        workload=workload,
        scenario=scenario,
    ).run()


__all__ = [
    "MOCK_EXECUTION_SCENARIOS",
    "MockExecutionBridgeError",
    "MockExecutionScenario",
    "build_mock_execution_bridge",
]
