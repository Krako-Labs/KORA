"""Declared, detection-only runtime capabilities for the KORA Hero planner."""

from __future__ import annotations

import re
from dataclasses import dataclass

from kora.hero_contracts import HardwareProfile, RuntimeCapability


@dataclass(frozen=True)
class RuntimeDefinition:
    """Static adapter declaration; this is not execution or compatibility proof."""

    adapter_id: str
    aliases: tuple[str, ...]
    supported_platforms: tuple[str, ...]
    supported_architectures: tuple[str, ...]
    supported_artifact_formats: tuple[str, ...]
    memory_modes: tuple[str, ...]


_RUNTIME_DEFINITIONS: tuple[RuntimeDefinition, ...] = (
    RuntimeDefinition(
        adapter_id="mlx-lm",
        aliases=("mlx-lm", "mlx_lm", "mlx"),
        supported_platforms=("darwin",),
        supported_architectures=("arm64",),
        supported_artifact_formats=("mlx", "safetensors"),
        memory_modes=("unified",),
    ),
    RuntimeDefinition(
        adapter_id="llama.cpp",
        aliases=("llama.cpp", "llama_cpp", "llamacpp"),
        supported_platforms=("darwin", "linux", "windows"),
        supported_architectures=("arm64", "x86_64", "amd64"),
        supported_artifact_formats=("gguf",),
        memory_modes=("unified", "hybrid_cpu_gpu", "gpu_resident"),
    ),
    RuntimeDefinition(
        adapter_id="freetoken",
        aliases=("freetoken", "free-token"),
        supported_platforms=("linux",),
        supported_architectures=("x86_64", "amd64"),
        supported_artifact_formats=("safetensors",),
        memory_modes=("hybrid_cpu_gpu",),
    ),
    RuntimeDefinition(
        adapter_id="ktransformers",
        aliases=("ktransformers", "k-transformers"),
        supported_platforms=("linux",),
        supported_architectures=("x86_64", "amd64"),
        supported_artifact_formats=("safetensors",),
        memory_modes=("hybrid_cpu_gpu",),
    ),
)


def _normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _profile_evidence_refs(hardware: HardwareProfile) -> list[str]:
    refs = [f"profile:hardware:{hardware.profile_id}", *hardware.evidence_refs]
    refs.extend(
        domain.evidence_ref
        for domain in hardware.memory_domains
        if domain.evidence_ref is not None
    )
    return list(dict.fromkeys(refs))


def runtime_definitions() -> tuple[RuntimeDefinition, ...]:
    """Return immutable registry declarations in stable order."""

    return _RUNTIME_DEFINITIONS


def build_runtime_capabilities(hardware: HardwareProfile) -> list[RuntimeCapability]:
    """Bind static declarations to detection facts from one hardware profile."""

    detected = {_normalized(candidate) for candidate in hardware.runtime_candidates}
    evidence_refs = _profile_evidence_refs(hardware)
    capabilities: list[RuntimeCapability] = []
    for definition in _RUNTIME_DEFINITIONS:
        aliases = {_normalized(alias) for alias in definition.aliases}
        capabilities.append(
            RuntimeCapability(
                adapter_id=definition.adapter_id,
                executor_class="local_ai",
                supported_platforms=list(definition.supported_platforms),
                supported_architectures=list(definition.supported_architectures),
                supported_artifact_formats=list(definition.supported_artifact_formats),
                memory_modes=list(definition.memory_modes),
                detected=bool(detected & aliases),
                evidence_level="fixture",
                evidence_refs=[*evidence_refs, "registry:hero.runtime-capability.v1"],
            )
        )
    return capabilities


def default_adapter_priority(hardware: HardwareProfile, *, artifact_format: str) -> list[str]:
    """Choose a stable platform/format priority without probing or execution."""

    platform = hardware.platform.lower()
    architecture = hardware.architecture.lower()
    has_nvidia = any(
        accelerator.vendor.lower() == "nvidia" for accelerator in hardware.accelerators
    )
    if platform == "darwin" and architecture == "arm64":
        return ["mlx-lm", "llama.cpp", "freetoken", "ktransformers"]
    if has_nvidia and artifact_format == "safetensors":
        return ["freetoken", "ktransformers", "llama.cpp", "mlx-lm"]
    return ["llama.cpp", "freetoken", "ktransformers", "mlx-lm"]


__all__ = [
    "RuntimeDefinition",
    "build_runtime_capabilities",
    "default_adapter_priority",
    "runtime_definitions",
]
