from __future__ import annotations

from datetime import datetime, timezone

from kora.hero_contracts import AcceleratorProfile, HardwareProfile, MemoryDomain
from kora.hero_runtime_registry import (
    build_runtime_capabilities,
    default_adapter_priority,
    runtime_definitions,
)

NOW = datetime(2026, 9, 14, tzinfo=timezone.utc)
GIB = 1024**3


def apple_profile(*, candidates: list[str] | None = None) -> HardwareProfile:
    return HardwareProfile(
        profile_id="apple",
        captured_at=NOW,
        platform="Darwin",
        architecture="arm64",
        memory_domains=[
            MemoryDomain(
                domain_id="unified:0",
                kind="unified",
                total_bytes=32 * GIB,
                source="fixture",
                evidence_ref="fixture:apple-memory",
            )
        ],
        accelerators=[
            AcceleratorProfile(
                accelerator_id="gpu:0",
                vendor="Apple",
                product="Apple fixture",
                memory_domain_id="unified:0",
            )
        ],
        runtime_candidates=candidates or [],
        evidence_level="fixture",
        evidence_refs=["fixture:apple-profile"],
    )


def nvidia_profile() -> HardwareProfile:
    return HardwareProfile(
        profile_id="nvidia",
        captured_at=NOW,
        platform="linux",
        architecture="x86_64",
        memory_domains=[
            MemoryDomain(
                domain_id="system:0",
                kind="system",
                total_bytes=32 * GIB,
                source="fixture",
            ),
            MemoryDomain(
                domain_id="dedicated_gpu:0",
                kind="dedicated_gpu",
                total_bytes=8 * GIB,
                source="fixture",
            ),
        ],
        accelerators=[
            AcceleratorProfile(
                accelerator_id="gpu:0",
                vendor="NVIDIA",
                product="fixture",
                memory_domain_id="dedicated_gpu:0",
            )
        ],
        runtime_candidates=["llama_cpp", "Free-Token"],
        evidence_level="fixture",
    )


def test_registry_has_frozen_backend_set_and_stable_order() -> None:
    assert [item.adapter_id for item in runtime_definitions()] == [
        "mlx-lm",
        "llama.cpp",
        "freetoken",
        "ktransformers",
    ]


def test_detection_aliases_are_normalized_without_starting_runtimes() -> None:
    capabilities = build_runtime_capabilities(
        apple_profile(candidates=["MLX_LM", "llamacpp", "unknown-runtime"])
    )
    by_id = {item.adapter_id: item for item in capabilities}

    assert by_id["mlx-lm"].detected is True
    assert by_id["llama.cpp"].detected is True
    assert by_id["freetoken"].detected is False
    assert by_id["ktransformers"].detected is False
    assert by_id["mlx-lm"].evidence_refs == [
        "profile:hardware:apple",
        "fixture:apple-profile",
        "fixture:apple-memory",
        "registry:hero.runtime-capability.v1",
    ]
    assert all(item.evidence_level == "fixture" for item in capabilities)


def test_apple_priority_prefers_mlx_then_general_gguf_baseline() -> None:
    assert default_adapter_priority(
        apple_profile(),
        artifact_format="safetensors",
    )[:2] == ["mlx-lm", "llama.cpp"]


def test_nvidia_safetensors_priority_exposes_primary_and_challenger() -> None:
    assert default_adapter_priority(
        nvidia_profile(),
        artifact_format="safetensors",
    )[:3] == ["freetoken", "ktransformers", "llama.cpp"]


def test_general_pc_gguf_priority_starts_with_llama_cpp() -> None:
    assert default_adapter_priority(
        nvidia_profile(),
        artifact_format="gguf",
    )[0] == "llama.cpp"
