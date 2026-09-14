"""Opt-in, in-memory Runtime Adapter v2 contract; no live execution bindings."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Literal

from pydantic import ConfigDict, Field

from kora.hero_contracts import (
    HardwareProfile,
    HeroEvent,
    ModelResourceProfile,
    RuntimeCapability,
    StrictContract,
    WorkloadRequirements,
)
from kora.hero_event_log import HeroEventLog
from kora.hero_planner import HeroPlanningBundle, build_hero_planning_bundle
from kora.hero_runtime_registry import runtime_definitions


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


class AdapterContractError(ValueError):
    """Stable failure code without raw model, process or provider output."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class MockTelemetry(StrictContract):
    """Supplied synthetic values, never physical measurements or inferred zeros."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    evidence_level: Literal["fixture"] = "fixture"
    input_tokens: int | None = Field(default=None, ge=0, strict=True)
    output_tokens: int | None = Field(default=None, ge=0, strict=True)
    peak_host_bytes: int | None = Field(default=None, ge=0, strict=True)
    peak_gpu_bytes: int | None = Field(default=None, ge=0, strict=True)
    load_ms: float | None = Field(default=None, ge=0, allow_inf_nan=False, strict=True)
    ttft_ms: float | None = Field(default=None, ge=0, allow_inf_nan=False, strict=True)
    end_to_end_ms: float | None = Field(
        default=None, ge=0, allow_inf_nan=False, strict=True
    )


class MockScript(StrictContract):
    """Bounded fixture result and one-shot lifecycle fault injection."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    output: str = Field(default="Illustrative mock output.", max_length=8192)
    telemetry: MockTelemetry = Field(default_factory=MockTelemetry)
    fail_at: Literal["load", "execute", "finish", "cleanup"] | None = None


class AdapterDescriptor(StrictContract):
    """Declaration for an inert or mock implementation, not an installed engine."""

    schema_version: Literal["hero.adapter-descriptor.v2"] = "hero.adapter-descriptor.v2"
    binding_id: str
    binding_version: Literal["2.0.0"] = "2.0.0"
    mode: Literal["inert", "mock"]
    capability: RuntimeCapability
    operations: tuple[str, ...] = (
        "probe",
        "health",
        "compatibility",
        "load",
        "execute",
        "finish",
        "cancel",
        "cleanup",
    )
    unsupported: tuple[str, ...] = (
        "live_execution",
        "benchmark",
        "calibration",
        "physical_telemetry",
    )
    evidence_level: Literal["fixture"] = "fixture"


def adapter_descriptor(adapter_id: str, *, mode: str = "inert") -> AdapterDescriptor:
    """Resolve only canonical Hero IDs; never import existing executable adapters."""

    if mode not in {"inert", "mock"}:
        raise AdapterContractError("unsupported_binding_mode")
    definition = next(
        (item for item in runtime_definitions() if item.adapter_id == adapter_id), None
    )
    if definition is None:
        raise AdapterContractError("unsupported_adapter")
    return AdapterDescriptor(
        binding_id=f"{mode}:{definition.adapter_id}",
        mode=mode,
        capability=RuntimeCapability(
            adapter_id=definition.adapter_id,
            executor_class="local_ai",
            supported_platforms=list(definition.supported_platforms),
            supported_architectures=list(definition.supported_architectures),
            supported_artifact_formats=list(definition.supported_artifact_formats),
            memory_modes=list(definition.memory_modes),
            detected=False,
            evidence_level="fixture",
            evidence_refs=["registry:hero.runtime-capability.v1"],
        ),
    )


class PlanCompatibility(StrictContract):
    compatible: bool
    reason_codes: tuple[str, ...]
    evidence_level: Literal["fixture"] = "fixture"
    live_execution_allowed: Literal[False] = False
    runtime_identity: dict[str, Any] | None = None


def check_plan_compatibility(
    descriptor: AdapterDescriptor,
    bundle: HeroPlanningBundle,
    hardware: HardwareProfile,
    model: ModelResourceProfile,
    workload: WorkloadRequirements,
) -> PlanCompatibility:
    """Recompute the complete planning bundle and bind immutable evidence digests."""

    reasons: list[str] = []
    # Revalidation also catches mutations and model_copy(update=...) bypasses.
    descriptor = AdapterDescriptor.model_validate(descriptor.model_dump(mode="json"))
    bundle = HeroPlanningBundle.model_validate(bundle.model_dump(mode="json"))
    hardware = HardwareProfile.model_validate(hardware.model_dump(mode="json"))
    model = ModelResourceProfile.model_validate(model.model_dump(mode="json"))
    workload = WorkloadRequirements.model_validate(workload.model_dump(mode="json"))
    canonical_descriptor = adapter_descriptor(
        descriptor.capability.adapter_id, mode=descriptor.mode
    )
    if descriptor != canonical_descriptor:
        reasons.append("descriptor_mismatch")
    rebuilt = build_hero_planning_bundle(
        run_id=bundle.events[0].run_id,
        plan_id=bundle.plan.plan_id,
        occurred_at=bundle.events[0].occurred_at,
        hardware=hardware,
        model=model,
        workload=workload,
    )
    if bundle != rebuilt:
        reasons.append("planning_evidence_mismatch")
    if any(
        level != "fixture"
        for level in (
            hardware.evidence_level,
            model.evidence_level,
            bundle.plan.evidence_level,
        )
    ):
        reasons.append("fixture_inputs_required")
    if descriptor.mode != "mock":
        reasons.append("inert_binding")
    if bundle.plan.selected_adapter_id is None:
        reasons.append("no_selected_runtime")
    elif bundle.plan.selected_adapter_id != descriptor.capability.adapter_id:
        reasons.append("selected_adapter_mismatch")
    selected = next(
        (
            item
            for item in bundle.plan.candidates
            if item.adapter_id == bundle.plan.selected_adapter_id
        ),
        None,
    )
    if selected and "placement_requires_runtime_plan" in selected.reason_codes:
        reasons.append("placement_unresolved")
    if bundle.plan.executor_class != "local_ai":
        reasons.append("executor_unsupported")
    if workload.allow_network:
        reasons.append("network_policy_unsupported")
    if bundle.plan.expert_overrides_required:
        reasons.append("expert_overrides_unsupported")
    identity = None
    if not reasons:
        identity = {
            "binding_id": descriptor.binding_id,
            "binding_version": descriptor.binding_version,
            "adapter_id": descriptor.capability.adapter_id,
            "descriptor_digest": _digest(descriptor.model_dump(mode="json")),
            "planning_digest": bundle.evidence_digest,
            "hardware_digest": _digest(hardware.model_dump(mode="json")),
            "model_profile_digest": _digest(model.model_dump(mode="json")),
            "model_id": model.model_id,
            "model_revision": model.source_revision,
            "model_artifact_sha256": model.sha256,
            "effective_config": deepcopy(bundle.plan.effective_config),
            "effective_config_digest": _digest(bundle.plan.effective_config),
            "runtime_version": None,
            "runtime_version_status": "not_probed",
            "mode": "mock",
        }
    return PlanCompatibility(
        compatible=not reasons,
        reason_codes=tuple(reasons) or ("mock_contract_compatible",),
        runtime_identity=identity,
    )


class MockRuntimeSession:
    """Single-owner, one-run mock lifecycle with canonical ordered Hero events.

    load/execute change only in-memory mock state. finish returns the supplied
    script; this class cannot invoke a model, provider, engine or subprocess.
    It emits no task completion, verification pass or accepted outcome.
    """

    def __init__(
        self,
        *,
        descriptor: AdapterDescriptor,
        bundle: HeroPlanningBundle,
        hardware: HardwareProfile,
        model: ModelResourceProfile,
        workload: WorkloadRequirements,
        script: MockScript | None = None,
    ) -> None:
        compatibility = check_plan_compatibility(
            descriptor, bundle, hardware, model, workload
        )
        if not compatibility.compatible:
            raise AdapterContractError(compatibility.reason_codes[0])
        self._descriptor = descriptor.model_copy(deep=True)
        self._identity = deepcopy(compatibility.runtime_identity)
        assert self._identity is not None
        self._script = MockScript.model_validate(
            (script or MockScript()).model_dump(mode="json")
        )
        self._identity["mock_script_digest"] = _digest(
            self._script.model_dump(mode="json")
        )
        self._state = "new"
        self._allocated = False
        self._fault_consumed = False
        self._output: str | None = None
        self._outcome: str | None = None
        self._at = bundle.events[-1].occurred_at
        self._log = HeroEventLog(bundle.events[0].run_id)
        self._log.extend(deepcopy(bundle.events))

    @property
    def state(self) -> str:
        return self._state

    @property
    def identity(self) -> dict[str, Any]:
        return deepcopy(self._identity)

    def probe(self) -> dict[str, Any]:
        return {
            "descriptor": self._descriptor.model_dump(mode="json"),
            "runtime_detected": False,
            "host_probe_performed": False,
            "evidence_level": "fixture",
        }

    def health(self) -> dict[str, Any]:
        return {
            "state": self._state,
            "mock_ready": self._state in {"new", "prepared"},
            "live_ready": False,
            "mock_allocation_retained": self._allocated,
            "evidence_level": "fixture",
        }

    def unsupported(self, operation: str) -> None:
        """Explicit rejection for benchmark/calibration/live requests."""
        del operation
        raise AdapterContractError("operation_unsupported")

    def _require(self, *states: str) -> None:
        if self._state not in states:
            raise AdapterContractError("invalid_lifecycle_state")

    def _emit(self, event_type: str, status: str, **payload: Any) -> None:
        projection = self._log.projection
        assert projection is not None
        sequence = projection.last_sequence + 1
        self._log.append(
            HeroEvent(
                event_id=f"{self._log.run_id}:{sequence:04d}",
                run_id=self._log.run_id,
                sequence=sequence,
                occurred_at=self._at,
                event_type=event_type,
                phase="execute",
                status=status,
                source="kora.hero_runtime_adapter_v2",
                evidence_level="fixture",
                adapter_id=self._descriptor.capability.adapter_id,
                executor_class="local_ai",
                evidence_refs=(
                    f"sha256:{self._identity['planning_digest']}",
                    f"sha256:{self._identity['descriptor_digest']}",
                    f"sha256:{self._identity['model_artifact_sha256']}",
                ),
                payload={
                    "mode": "mock",
                    "runtime_identity": self.identity,
                    "state": self._state,
                    "mock_allocation_retained": self._allocated,
                    "actual_model_calls": 0,
                    "actual_provider_calls": 0,
                    "runtime_started": False,
                    **payload,
                },
            )
        )

    def _fault(self, operation: str) -> bool:
        if self._script.fail_at == operation and not self._fault_consumed:
            self._fault_consumed = True
            self._state = "cleanup_failed" if operation == "cleanup" else "failed"
            if operation != "cleanup":
                self._outcome = "failed"
            self._emit(
                f"adapter.{operation}.failed",
                "failed",
                reason_code=f"mock_{operation}_failure",
            )
            return True
        return False

    def load(self) -> None:
        self._require("new")
        # A mock allocation flag permits testing partial-load cleanup.
        self._allocated = True
        if self._fault("load"):
            return
        self._state = "prepared"
        self._emit("adapter.prepared", "ready")

    def execute(self) -> None:
        self._require("prepared")
        if self._fault("execute"):
            return
        self._state = "running"
        self._emit("adapter.started", "running")

    def finish(self) -> dict[str, Any] | None:
        self._require("running")
        if self._fault("finish"):
            return None
        self._emit(
            "telemetry.sampled",
            "running",
            telemetry=self._script.telemetry.model_dump(mode="json"),
        )
        self._output = self._script.output
        self._state = "completed"
        self._outcome = "completed"
        self._emit("adapter.completed", "completed", output=self._output)
        return self.result()

    def cancel(self) -> None:
        if self._state == "cancelled":
            return
        self._require("new", "prepared", "running")
        self._state = "cancelled"
        self._outcome = "cancelled"
        self._emit("adapter.cancelled", "failed", reason_code="mock_cancelled")

    def cleanup(self) -> None:
        if self._state == "closed":
            return
        self._require(
            "new", "prepared", "completed", "failed", "cancelled", "cleanup_failed"
        )
        if self._fault("cleanup"):
            return
        self._allocated = False
        self._state = "closed"
        self._emit("adapter.cleaned", "completed", outcome=self._outcome)

    def result(self) -> dict[str, Any]:
        self._require("completed", "closed", "cleanup_failed")
        if self._outcome != "completed":
            raise AdapterContractError("no_completed_result")
        return {
            "output": self._output,
            "evidence_level": "fixture",
            "runtime_identity": self.identity,
            "telemetry": self._script.telemetry.model_dump(mode="json"),
            "service_acceptance": "not_measured",
            "semantic_non_regression": "not_measured",
            "accepted_outcome": False,
            "actual_model_calls": 0,
            "actual_provider_calls": 0,
            "runtime_started": False,
        }

    def events_after(self, sequence: int | None = None) -> list[HeroEvent]:
        projection = self._log.projection
        assert projection is not None
        if sequence is not None and (
            type(sequence) is not int
            or sequence < -1
            or sequence > projection.last_sequence
        ):
            raise AdapterContractError("invalid_event_cursor")
        return deepcopy(self._log.events_after(sequence))

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(
            {
                "schema_version": "hero.mock-adapter-session.v2",
                "state": self._state,
                "outcome": self._outcome,
                "runtime_identity": self._identity,
                "mock_allocation_retained": self._allocated,
                "log": self._log.snapshot(),
            }
        )


__all__ = [
    "AdapterContractError",
    "AdapterDescriptor",
    "MockRuntimeSession",
    "MockScript",
    "MockTelemetry",
    "PlanCompatibility",
    "adapter_descriptor",
    "check_plan_compatibility",
]
