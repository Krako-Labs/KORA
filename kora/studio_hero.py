"""Fixture-only Hero planning and event projection for Studio.

No runtime adapter, model loader, provider, or host probe is imported here.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from importlib import resources
from typing import Any

from kora.hero_contracts import (
    AcceleratorProfile,
    HardwareProfile,
    HeroEvent,
    MemoryDomain,
    ModelResourceProfile,
    WorkloadRequirements,
)
from kora.hero_planner import build_hero_planning_bundle
from kora.hero_replay import apply_hero_event

GIB = 1024**3
NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)
SCENARIOS = ("apple", "pc", "unknown", "quality-failed")
REQUEST = (
    "Prepare a launch brief: check the supplied facts, reuse the approved brand "
    "notes, draft a local summary, and request an independent review before acceptance."
)
BOUNDARY = (
    "FIXTURE PLAYBACK — synthetic profiles, task outputs and service acceptance. "
    "No model, runtime or provider execution. No measured performance or "
    "larger-than-VRAM result."
)
LANES = {
    "deterministic": "Deterministic",
    "exact_reuse": "Exact Reuse",
    "local_ai": "Local AI",
    "frontier_ai": "Frontier AI",
}


def build_studio_hero_fixture(scenario: str = "apple") -> dict[str, Any]:
    """Build a real planning bundle from synthetic inputs, then replay fixtures."""
    if scenario not in SCENARIOS:
        raise ValueError("unknown Hero fixture scenario")
    pc = scenario == "pc"
    hardware = HardwareProfile(
        profile_id=f"fixture-hardware-{scenario}",
        captured_at=NOW,
        platform="linux" if pc else "Darwin",
        architecture="x86_64" if pc else "arm64",
        memory_domains=[
            MemoryDomain(
                domain_id="host",
                kind="system" if pc else "unified",
                total_bytes=32 * GIB,
                source="fixture",
                evidence_ref="fixture:memory:host",
            ),
            *(
                [
                    MemoryDomain(
                        domain_id="gpu",
                        kind="dedicated_gpu",
                        total_bytes=8 * GIB,
                        source="fixture",
                        evidence_ref="fixture:memory:gpu",
                    )
                ]
                if pc
                else []
            ),
        ],
        accelerators=[
            AcceleratorProfile(
                accelerator_id="fixture-gpu",
                vendor="NVIDIA" if pc else "Apple",
                product="Synthetic device",
                memory_domain_id="gpu" if pc else "host",
            )
        ],
        runtime_candidates=["llama.cpp"] if pc else ["mlx-lm", "llama.cpp"],
        evidence_level="fixture",
        evidence_refs=["fixture:hardware"],
    )
    model = ModelResourceProfile(
        profile_id=f"fixture-model-{scenario}",
        model_id="Synthetic launch model",
        artifact_id="fixture-artifact",
        artifact_format="gguf" if pc else "safetensors",
        quantization="fixture-only",
        artifact_bytes=20 * GIB,
        model_weight_bytes=18 * GIB,
        sha256="a" * 64,
        source_revision="fixture-v1",
        evidence_level="fixture",
        tensor_inventory_ref="fixture:tensors",
    )
    workload = WorkloadRequirements(
        workload_class="source_bounded_launch_brief",
        context_tokens=4096,
        max_output_tokens=768,
        estimated_kv_bytes=None if scenario == "unknown" else GIB,
        runtime_reserve_bytes=None if scenario == "unknown" else 2 * GIB,
        allow_network=False,
    )
    bundle = build_hero_planning_bundle(
        run_id=f"hero-fixture-{scenario}-v1",
        plan_id=f"fixture-plan-{scenario}",
        occurred_at=NOW,
        hardware=hardware,
        model=model,
        workload=workload,
    )
    events = list(bundle.events)

    def emit(kind: str, phase: str, status: str, **fields: Any) -> None:
        payload = fields.pop("payload", {})
        payload["fixture_only"] = True
        events.append(
            HeroEvent(
                event_id=f"{events[0].run_id}:{len(events):04d}",
                run_id=events[0].run_id,
                sequence=len(events),
                occurred_at=NOW,
                event_type=kind,
                phase=phase,
                status=status,
                source="kora.studio_hero.fixture",
                evidence_level="fixture",
                evidence_refs=("fixture:studio-story-v1",),
                payload=payload,
                **fields,
            )
        )

    if bundle.plan.selected_adapter_id is None:
        emit(
            "run.failed",
            "fail",
            "failed",
            payload={
                "reason": "No feasible runtime plan; fixture stops before task execution."
            },
        )
    else:
        tasks = [
            (
                "facts",
                "Check supplied facts",
                "Apply the supplied structural rules.",
                [],
                "deterministic",
                "deterministic_core",
            ),
            (
                "reuse",
                "Reuse approved brand notes",
                "Reuse an exact matching approved input.",
                [],
                "exact_reuse",
                "exact_reuse_store",
            ),
            (
                "draft",
                "Draft the launch summary",
                "Combine checked facts with approved notes.",
                ["facts", "reuse"],
                "local_ai",
                bundle.plan.selected_adapter_id,
            ),
            (
                "review",
                "Independent review",
                "Illustrate an explicitly gated frontier review.",
                ["draft"],
                "frontier_ai",
                "frontier_provider",
            ),
        ]
        emit(
            "graph.created",
            "decompose",
            "completed",
            payload={"task_ids": [task[0] for task in tasks]},
        )
        for task_id, label, purpose, deps, lane, adapter in tasks:
            emit(
                "task.created",
                "decompose",
                "created",
                task_id=task_id,
                payload={"label": label, "purpose": purpose, "dependencies": deps},
            )
        for task_id, label, purpose, deps, lane, adapter in tasks:
            emit("task.ready", "execute", "ready", task_id=task_id)
            emit(
                "task.routed",
                "plan",
                "ready",
                task_id=task_id,
                executor_class=lane,
                adapter_id=adapter,
            )
            emit(
                "task.started",
                "execute",
                "running",
                task_id=task_id,
                executor_class=lane,
                adapter_id=adapter,
            )
            emit(
                "task.completed",
                "execute",
                "completed",
                task_id=task_id,
                payload={"result": f"Illustrative output: {label}."},
            )
        emit("merge.started", "merge", "running")
        emit(
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
        emit("verification.started", "verify", "running")
        passed = scenario != "quality-failed"
        emit(
            "verification.passed" if passed else "verification.failed",
            "verify",
            "completed" if passed else "failed",
            payload={
                "service_acceptance": "fixture_pass" if passed else "fixture_fail",
                "structural_acceptance": "fixture_pass",
                "semantic_non_regression": "not_measured",
                "reason": "Synthetic service contract passes."
                if passed
                else "Synthetic service-quality failure: required source coverage missing.",
            },
        )
        emit(
            "run.completed" if passed else "run.failed",
            "complete" if passed else "fail",
            "completed" if passed else "failed",
        )

    frames = project_studio_hero_events(events)
    return {
        "schema_version": "hero.studio-fixture.v1",
        "scenario": scenario,
        "run_id": events[0].run_id,
        "request": REQUEST,
        "claim_boundary": BOUNDARY,
        "evidence_level": "fixture",
        "hardware": hardware.model_dump(mode="json"),
        "model": model.model_dump(mode="json"),
        "workload": workload.model_dump(mode="json"),
        "planning_bundle": bundle.model_dump(mode="json"),
        "event_count": len(events),
        "frames": frames,
        "actual_execution": {
            "runtime_starts": 0,
            "model_calls": 0,
            "provider_calls": 0,
        },
    }


def project_studio_hero_events(events: list[HeroEvent]) -> list[dict[str, Any]]:
    """Project ordered events with the canonical reducer; all inputs must be fixtures."""
    state = None
    frames = []
    service = "not_started"
    structural = "not_started"
    answer = ""
    candidates_visible = False
    profiles_visible = False
    outputs: dict[str, str] = {}
    reason = ""
    for event in events:
        if event.evidence_level != "fixture":
            raise ValueError("Studio fixture playback rejects non-fixture events")
        state = apply_hero_event(state, event)
        if event.event_type == "workload.analyzed":
            profiles_visible = True
        if event.event_type == "execution.plan.created":
            candidates_visible = True
        if event.event_type == "task.completed" and event.task_id:
            outputs[event.task_id] = str(event.payload.get("result", ""))
        if event.event_type == "merge.completed":
            answer = str(event.payload.get("answer", ""))
        if event.event_type.startswith("verification."):
            service = str(event.payload.get("service_acceptance", "pending"))
            structural = str(event.payload.get("structural_acceptance", "pending"))
        reason = str(event.payload.get("reason", reason))
        accepted = (
            state.accepted_outcome
            and state.run_state == "completed"
            and state.verification_state == "passed"
            and service == "fixture_pass"
            and structural == "fixture_pass"
        )
        counts = {
            lane: sum(
                task.executor_class == lane and task.state in {"completed", "verified"}
                for task in state.tasks.values()
            )
            for lane in LANES
        }
        frames.append(
            {
                "event": event.model_dump(mode="json"),
                "projection": state.model_dump(mode="json"),
                "view": {
                    "profiles_visible": profiles_visible,
                    "candidates_visible": candidates_visible,
                    "fixture_accepted_outcome": accepted,
                    "service_acceptance": service,
                    "structural_acceptance": structural,
                    "semantic_non_regression": "not_measured",
                    "answer": answer,
                    "reason": reason,
                    "outputs": dict(outputs),
                    "A_workload_control": {
                        "fixture_completed_tasks": counts,
                        "actual_model_calls": 0,
                        "actual_provider_calls": 0,
                    },
                    "B_local_execution": {
                        "execution_performed": False,
                        "peak_memory_bytes": None,
                        "latency_ms": None,
                        "throughput": None,
                        "service_quality_measured": False,
                    },
                },
            }
        )
    return frames


def hero_asset(name: str) -> str:
    """Load only package-controlled Hero assets."""
    if name not in {"hero.html", "hero.css", "hero.js"}:
        raise ValueError("unknown Hero asset")
    return (
        resources.files("kora")
        .joinpath(f"studio_assets/{name}")
        .read_text(encoding="utf-8")
    )


def hero_event_payload(scenario: str, after: int = -1) -> dict[str, Any]:
    fixture = build_studio_hero_fixture(scenario)
    if after < -1 or after >= fixture["event_count"]:
        raise ValueError("cursor outside fixture event range")
    return {
        "run_id": fixture["run_id"],
        "evidence_level": "fixture",
        "frames": fixture["frames"][after + 1 :],
        "event_count": fixture["event_count"],
    }


def hero_sse(payload: dict[str, Any]) -> str:
    chunks = [
        f"id: {frame['event']['sequence']}\nevent: hero\ndata: {json.dumps(frame)}\n\n"
        for frame in payload["frames"]
    ]
    chunks.append("event: end\ndata: {}\n\n")
    return "".join(chunks)
