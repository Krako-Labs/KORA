from __future__ import annotations

import json
import struct
from datetime import datetime, timezone
from pathlib import Path

import pytest

from kora.hero_contracts import RuntimeCapability, WorkloadRequirements
from kora.hero_feasibility import build_execution_plan
from kora.hero_profilers import (
    ProfileCollectionError,
    collect_hardware_profile,
    profile_model_artifact,
    write_profile_evidence,
)


def _executor(mapping: dict[tuple[str, ...], str]):
    return lambda command: mapping.get(command)


def _write_safetensors(path: Path, tensor_sizes: list[int]) -> int:
    offset = 0
    header: dict[str, object] = {}
    for index, size in enumerate(tensor_sizes):
        header[f"tensor.{index}"] = {
            "dtype": "U8",
            "shape": [size],
            "data_offsets": [offset, offset + size],
        }
        offset += size
    raw_header = json.dumps(header, separators=(",", ":")).encode()
    path.write_bytes(struct.pack("<Q", len(raw_header)) + raw_header + bytes(offset))
    return offset


def test_collect_apple_silicon_hardware_uses_exact_unified_bytes() -> None:
    memory_bytes = 128 * 1024**3
    displays = {
        "SPDisplaysDataType": [
            {"sppci_model": "Apple M3 Max", "sppci_cores": "40"}
        ]
    }
    profile = collect_hardware_profile(
        profile_id="mac-m3-max",
        executor=_executor(
            {
                ("sysctl", "-n", "hw.memsize"): str(memory_bytes),
                ("sysctl", "-n", "machdep.cpu.brand_string"): "Apple M3 Max",
                ("system_profiler", "SPDisplaysDataType", "-json"): json.dumps(displays),
            }
        ),
        which=lambda command: f"/mock/{command}"
        if command in {"mlx_lm.generate", "llama-cli"}
        else None,
        captured_at=datetime(2026, 9, 14, tzinfo=timezone.utc),
        platform_name="Darwin",
        architecture="arm64",
    )

    assert profile.memory_domains[0].kind == "unified"
    assert profile.memory_domains[0].total_bytes == memory_bytes
    assert profile.accelerators[0].product == "Apple M3 Max"
    assert profile.accelerators[0].memory_domain_id == "unified:0"
    assert profile.runtime_candidates == ["mlx-lm", "llama.cpp"]
    assert profile.evidence_level == "observed"
    assert "accelerators" not in profile.unknown_fields


def test_collect_linux_nvidia_hardware_keeps_system_and_gpu_domains_separate() -> None:
    profile = collect_hardware_profile(
        profile_id="pc-8gb",
        executor=_executor(
            {
                ("cat", "/proc/meminfo"): "MemTotal:       33554432 kB\n",
                (
                    "nvidia-smi",
                    "--query-gpu=index,name,memory.total,driver_version",
                    "--format=csv,noheader,nounits",
                ): "0, NVIDIA GeForce RTX 3070, 8192, 555.42",
            }
        ),
        which=lambda command: f"/mock/{command}"
        if command in {"nvidia-smi", "llama-server", "freetoken"}
        else None,
        captured_at=datetime(2026, 9, 14, tzinfo=timezone.utc),
        platform_name="Linux",
        architecture="x86_64",
    )

    domains = {item.kind: item for item in profile.memory_domains}
    assert domains["system"].total_bytes == 32 * 1024**3
    assert domains["dedicated_gpu"].total_bytes == 8 * 1024**3
    assert profile.accelerators[0].vendor == "NVIDIA"
    assert profile.accelerators[0].driver_version == "555.42"
    assert profile.runtime_candidates == ["llama.cpp", "freetoken"]
    assert profile.unknown_fields == []


def test_hardware_profiler_fails_closed_without_exact_system_memory() -> None:
    with pytest.raises(ProfileCollectionError, match="exact total physical memory"):
        collect_hardware_profile(
            profile_id="unknown",
            executor=lambda command: None,
            which=lambda command: None,
            platform_name="Linux",
            architecture="x86_64",
        )


def test_detected_nvidia_with_unreadable_rows_is_explicitly_unknown() -> None:
    profile = collect_hardware_profile(
        profile_id="pc-unknown-gpu",
        executor=_executor(
            {
                ("cat", "/proc/meminfo"): "MemTotal: 16777216 kB",
                (
                    "nvidia-smi",
                    "--query-gpu=index,name,memory.total,driver_version",
                    "--format=csv,noheader,nounits",
                ): "malformed",
            }
        ),
        which=lambda command: "/mock/nvidia-smi" if command == "nvidia-smi" else None,
        platform_name="Linux",
        architecture="x86_64",
    )

    assert profile.accelerators == []
    assert "accelerators.nvidia.rows[0]" in profile.unknown_fields
    assert "accelerators" in profile.unknown_fields


def test_safetensors_directory_profile_counts_exact_tensor_payload(tmp_path: Path) -> None:
    artifact = tmp_path / "model"
    artifact.mkdir()
    tensor_bytes = _write_safetensors(artifact / "model-00001-of-00001.safetensors", [7, 11])
    (artifact / "tokenizer.json").write_text('{"version":"1"}', encoding="utf-8")
    (artifact / "tokenizer_config.json").write_text(
        '{"chat_template":"{{ messages }}"}', encoding="utf-8"
    )

    profile, inventory = profile_model_artifact(
        artifact,
        profile_id="qwen-profile",
        model_id="qwen/test",
        source_revision="revision-123",
        quantization="bf16",
    )

    assert profile.artifact_format == "safetensors"
    assert profile.model_weight_bytes == tensor_bytes == 18
    assert profile.artifact_bytes > profile.model_weight_bytes
    assert len(profile.sha256) == 64
    assert profile.tensor_inventory_ref.startswith("sha256:")
    assert profile.tokenizer_digest is not None
    assert profile.chat_template_digest is not None
    assert profile.unknown_fields == []
    assert inventory["tensor_count"] == 2
    assert inventory["tensor_payload_bytes"] == 18
    assert str(tmp_path) not in json.dumps(inventory)


def test_mlx_format_can_be_declared_for_safetensors_directory(tmp_path: Path) -> None:
    artifact = tmp_path / "mlx-model"
    artifact.mkdir()
    _write_safetensors(artifact / "weights.safetensors", [32])

    profile, _inventory = profile_model_artifact(
        artifact,
        profile_id="mlx-profile",
        model_id="mlx/test",
        source_revision="local",
        artifact_format="mlx",
        quantization="4bit",
    )

    assert profile.artifact_format == "mlx"
    assert profile.model_weight_bytes == 32


def test_gguf_profile_uses_conservative_container_footprint(tmp_path: Path) -> None:
    artifact = tmp_path / "model-Q4_K_M.gguf"
    artifact.write_bytes(b"GGUF" + struct.pack("<IQQ", 3, 2, 0) + bytes(64))

    profile, inventory = profile_model_artifact(
        artifact,
        profile_id="gguf-profile",
        model_id="model/test",
        source_revision="sha",
    )

    assert profile.artifact_format == "gguf"
    assert profile.model_weight_bytes == artifact.stat().st_size
    assert profile.quantization == "Q4_K_M"
    assert "exact_tensor_weight_bytes" in profile.unknown_fields
    assert inventory["tensor_count"] == 2
    assert inventory["claim_boundary"].startswith("Static artifact inspection")


def test_model_profiler_rejects_malformed_or_unsupported_artifact(tmp_path: Path) -> None:
    malformed = tmp_path / "broken.safetensors"
    malformed.write_bytes(b"bad")
    with pytest.raises(ProfileCollectionError, match="truncated safetensors"):
        profile_model_artifact(
            malformed,
            profile_id="broken",
            model_id="broken",
            source_revision="local",
        )

    unsupported = tmp_path / "weights.bin"
    unsupported.write_bytes(b"weights")
    with pytest.raises(ProfileCollectionError, match="no supported"):
        profile_model_artifact(
            unsupported,
            profile_id="unsupported",
            model_id="unsupported",
            source_revision="local",
        )


def test_safetensors_profiler_rejects_payload_past_end_of_file(tmp_path: Path) -> None:
    artifact = tmp_path / "bad-offset.safetensors"
    header = {
        "tensor": {"dtype": "U8", "shape": [100], "data_offsets": [0, 100]}
    }
    raw_header = json.dumps(header).encode()
    artifact.write_bytes(struct.pack("<Q", len(raw_header)) + raw_header + bytes(2))

    with pytest.raises(ProfileCollectionError, match="exceeds file size"):
        profile_model_artifact(
            artifact,
            profile_id="bad-offset",
            model_id="bad-offset",
            source_revision="local",
        )


def test_model_profiler_refuses_top_level_symlink(tmp_path: Path) -> None:
    target = tmp_path / "target.safetensors"
    _write_safetensors(target, [4])
    link = tmp_path / "link.safetensors"
    link.symlink_to(target)

    with pytest.raises(ProfileCollectionError, match="symbolic link"):
        profile_model_artifact(
            link,
            profile_id="link",
            model_id="link",
            source_revision="local",
        )


def test_profiler_outputs_feed_task031_feasibility_contract(tmp_path: Path) -> None:
    artifact = tmp_path / "weights.safetensors"
    _write_safetensors(artifact, [1024])
    model, _inventory = profile_model_artifact(
        artifact,
        profile_id="model-profile",
        model_id="test/model",
        source_revision="local",
        quantization="test",
    )
    hardware = collect_hardware_profile(
        profile_id="hardware-profile",
        executor=_executor({("cat", "/proc/meminfo"): "MemTotal: 8388608 kB"}),
        which=lambda command: "/mock/llama-cli" if command == "llama-cli" else None,
        platform_name="Linux",
        architecture="x86_64",
    )
    capability = RuntimeCapability(
        adapter_id="llama.cpp",
        executor_class="local_ai",
        supported_platforms=["Linux"],
        supported_architectures=["x86_64"],
        supported_artifact_formats=["safetensors"],
        memory_modes=["hybrid_cpu_gpu"],
        detected=True,
        evidence_level="observed",
    )
    workload = WorkloadRequirements(
        workload_class="fixture",
        context_tokens=128,
        max_output_tokens=32,
        estimated_kv_bytes=1024,
        runtime_reserve_bytes=1024,
    )

    plan = build_execution_plan(
        plan_id="plan",
        hardware=hardware,
        model=model,
        workload=workload,
        capabilities=[capability],
        adapter_priority=["llama.cpp"],
    )

    assert plan.selected_adapter_id is None
    assert plan.candidates[0].reason_codes == ["hybrid_memory_domains_missing"]


def test_evidence_export_is_atomic_and_claim_bounded(tmp_path: Path) -> None:
    artifact = tmp_path / "weights.safetensors"
    _write_safetensors(artifact, [5])
    model, inventory = profile_model_artifact(
        artifact,
        profile_id="profile",
        model_id="test/model",
        source_revision="local",
    )
    output = tmp_path / "evidence" / "profile.json"

    written = write_profile_evidence(output, model=model, tensor_inventory=inventory)
    payload = json.loads(written.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "hero.profile-evidence.v1"
    assert payload["model"]["model_weight_bytes"] == 5
    assert "does not prove runtime compatibility" in payload["claim_boundary"]
    assert not output.with_name(".profile.json.tmp").exists()


def test_evidence_export_requires_a_profile(tmp_path: Path) -> None:
    with pytest.raises(ProfileCollectionError, match="at least one profile"):
        write_profile_evidence(tmp_path / "empty.json")
