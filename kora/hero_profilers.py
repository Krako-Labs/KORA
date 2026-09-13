"""Byte-based, non-inference profilers for the KORA Hero execution path."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import struct
import subprocess
from collections.abc import Callable, Iterable
from datetime import datetime, timezone
from itertools import pairwise
from pathlib import Path
from typing import Any

from kora.hero_contracts import (
    AcceleratorProfile,
    HardwareProfile,
    MemoryDomain,
    ModelResourceProfile,
)

CommandExecutor = Callable[[tuple[str, ...]], str | None]
ExecutableDetector = Callable[[str], str | None]

_RUNTIME_COMMANDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("mlx-lm", ("mlx_lm.server", "mlx_lm.generate", "mlx_lm.chat")),
    ("llama.cpp", ("llama-server", "llama-cli", "llama")),
    ("freetoken", ("freetoken",)),
    ("ktransformers", ("ktransformers",)),
)
_TOKENIZER_FILES = ("tokenizer.json", "tokenizer.model", "tokenizer_config.json")


class ProfileCollectionError(ValueError):
    """Raised when a required observed fact cannot be collected safely."""


def _default_executor(command: tuple[str, ...]) -> str | None:
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
            env={**os.environ, "LC_ALL": "C", "LANG": "C"},
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def _positive_int(value: str | None) -> int | None:
    try:
        parsed = int((value or "").strip())
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _runtime_candidates(which: ExecutableDetector) -> list[str]:
    detected: list[str] = []
    for runtime, commands in _RUNTIME_COMMANDS:
        if any(which(command) for command in commands):
            detected.append(runtime)
    return detected


def _darwin_memory_bytes(executor: CommandExecutor) -> int | None:
    return _positive_int(executor(("sysctl", "-n", "hw.memsize")))


def _linux_memory_bytes(executor: CommandExecutor) -> int | None:
    raw = executor(("cat", "/proc/meminfo"))
    if raw:
        for line in raw.splitlines():
            if line.startswith("MemTotal:"):
                parts = line.split()
                kib = _positive_int(parts[1] if len(parts) > 1 else None)
                if kib is not None:
                    return kib * 1024
    pages = _positive_int(executor(("getconf", "PHYS_PAGES")))
    page_size = _positive_int(executor(("getconf", "PAGE_SIZE")))
    return pages * page_size if pages is not None and page_size is not None else None


def _darwin_gpu_payload(executor: CommandExecutor) -> list[dict[str, Any]]:
    raw = executor(("system_profiler", "SPDisplaysDataType", "-json"))
    if not raw:
        return []
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return []
    records = payload.get("SPDisplaysDataType", [])
    return [item for item in records if isinstance(item, dict)] if isinstance(records, list) else []


def _darwin_accelerators(
    records: Iterable[dict[str, Any]],
    *,
    unified: bool,
) -> tuple[list[AcceleratorProfile], list[MemoryDomain], list[str]]:
    accelerators: list[AcceleratorProfile] = []
    domains: list[MemoryDomain] = []
    unknowns: list[str] = []
    for index, record in enumerate(records):
        product = record.get("sppci_model") or record.get("_name")
        if not isinstance(product, str) or not product.strip():
            continue
        product = product.strip()
        domain_id = "unified:0" if unified else f"dedicated_gpu:{index}"
        if not unified:
            raw_vram = record.get("spdisplays_vram") or record.get("spdisplays_vram_shared")
            vram_bytes = _parse_size_bytes(raw_vram)
            if vram_bytes is None:
                unknowns.append(f"accelerators[{index}].dedicated_memory_bytes")
                continue
            domains.append(
                MemoryDomain(
                    domain_id=domain_id,
                    kind="dedicated_gpu",
                    total_bytes=vram_bytes,
                    source="system_profiler.SPDisplaysDataType",
                    evidence_ref="probe:system_profiler.SPDisplaysDataType",
                )
            )
        vendor = "Apple" if product.lower().startswith("apple ") else str(
            record.get("spdisplays_vendor") or "unknown"
        )
        accelerators.append(
            AcceleratorProfile(
                accelerator_id=f"gpu:{index}",
                vendor=vendor,
                product=product,
                memory_domain_id=domain_id,
                device_identifier=str(index),
            )
        )
    return accelerators, domains, unknowns


def _parse_size_bytes(value: object) -> int | None:
    if not isinstance(value, str):
        return None
    parts = value.replace(",", "").split()
    if not parts:
        return None
    try:
        amount = float(parts[0])
    except ValueError:
        return None
    unit = parts[1].lower() if len(parts) > 1 else "bytes"
    factors = {
        "bytes": 1,
        "b": 1,
        "kb": 1000,
        "mb": 1000**2,
        "gb": 1000**3,
        "kib": 1024,
        "mib": 1024**2,
        "gib": 1024**3,
    }
    factor = factors.get(unit)
    result = int(amount * factor) if factor is not None else 0
    return result if result > 0 else None


def _nvidia_accelerators(
    executor: CommandExecutor,
) -> tuple[list[AcceleratorProfile], list[MemoryDomain], list[str]]:
    command = (
        "nvidia-smi",
        "--query-gpu=index,name,memory.total,driver_version",
        "--format=csv,noheader,nounits",
    )
    raw = executor(command)
    if not raw:
        return [], [], ["accelerators.nvidia"]
    accelerators: list[AcceleratorProfile] = []
    domains: list[MemoryDomain] = []
    unknowns: list[str] = []
    for line_number, line in enumerate(raw.splitlines()):
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 4:
            unknowns.append(f"accelerators.nvidia.rows[{line_number}]")
            continue
        index, product, memory_mib_text, driver = parts
        memory_mib = _positive_int(memory_mib_text)
        if not index or not product or memory_mib is None:
            unknowns.append(f"accelerators.nvidia.rows[{line_number}]")
            continue
        domain_id = f"dedicated_gpu:{index}"
        domains.append(
            MemoryDomain(
                domain_id=domain_id,
                kind="dedicated_gpu",
                total_bytes=memory_mib * 1024**2,
                source="nvidia-smi.memory.total",
                evidence_ref="probe:nvidia-smi.memory.total",
            )
        )
        accelerators.append(
            AcceleratorProfile(
                accelerator_id=f"gpu:{index}",
                vendor="NVIDIA",
                product=product,
                memory_domain_id=domain_id,
                device_identifier=index,
                driver_version=driver or None,
            )
        )
    return accelerators, domains, unknowns


def collect_hardware_profile(
    *,
    profile_id: str,
    executor: CommandExecutor = _default_executor,
    which: ExecutableDetector = shutil.which,
    captured_at: datetime | None = None,
    platform_name: str | None = None,
    architecture: str | None = None,
) -> HardwareProfile:
    """Collect exact memory-domain facts without starting a model or runtime."""

    observed_platform = platform_name or platform.system()
    observed_architecture = architecture or platform.machine()
    captured = captured_at or datetime.now(timezone.utc)
    if observed_platform == "Darwin":
        total_memory = _darwin_memory_bytes(executor)
    elif observed_platform == "Linux":
        total_memory = _linux_memory_bytes(executor)
    else:
        total_memory = None
    if total_memory is None:
        raise ProfileCollectionError("exact total physical memory is unavailable")

    memory_domains: list[MemoryDomain] = []
    accelerators: list[AcceleratorProfile] = []
    unknowns: list[str] = []
    evidence_refs = ["probe:physical_memory_bytes"]

    if observed_platform == "Darwin":
        chip = executor(("sysctl", "-n", "machdep.cpu.brand_string")) or ""
        records = _darwin_gpu_payload(executor)
        is_apple_silicon = observed_architecture == "arm64" and (
            chip.startswith("Apple ") or any(
                str(item.get("sppci_model", "")).startswith("Apple ") for item in records
            )
        )
        if is_apple_silicon:
            memory_domains.append(
                MemoryDomain(
                    domain_id="unified:0",
                    kind="unified",
                    total_bytes=total_memory,
                    source="sysctl.hw.memsize",
                    evidence_ref="probe:sysctl.hw.memsize",
                )
            )
        else:
            memory_domains.append(
                MemoryDomain(
                    domain_id="system:0",
                    kind="system",
                    total_bytes=total_memory,
                    source="sysctl.hw.memsize",
                    evidence_ref="probe:sysctl.hw.memsize",
                )
            )
        detected, gpu_domains, gpu_unknowns = _darwin_accelerators(
            records, unified=is_apple_silicon
        )
        accelerators.extend(detected)
        memory_domains.extend(gpu_domains)
        unknowns.extend(gpu_unknowns)
        evidence_refs.append("probe:system_profiler.SPDisplaysDataType")
    else:
        memory_domains.append(
            MemoryDomain(
                domain_id="system:0",
                kind="system",
                total_bytes=total_memory,
                source="proc.meminfo" if observed_platform == "Linux" else "platform",
                evidence_ref="probe:physical_memory_bytes",
            )
        )
        if observed_platform == "Linux" and which("nvidia-smi"):
            detected, gpu_domains, gpu_unknowns = _nvidia_accelerators(executor)
            accelerators.extend(detected)
            memory_domains.extend(gpu_domains)
            unknowns.extend(gpu_unknowns)
            evidence_refs.append("probe:nvidia-smi.memory.total")

    if not accelerators:
        unknowns.append("accelerators")
    return HardwareProfile(
        profile_id=profile_id,
        captured_at=captured,
        platform=observed_platform,
        architecture=observed_architecture,
        memory_domains=memory_domains,
        accelerators=accelerators,
        runtime_candidates=_runtime_candidates(which),
        evidence_level="observed",
        evidence_refs=list(dict.fromkeys(evidence_refs)),
        unknown_fields=list(dict.fromkeys(unknowns)),
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_artifact_files(path: Path) -> list[Path]:
    if path.is_symlink():
        raise ProfileCollectionError("artifact path must not be a symbolic link")
    if path.is_file():
        return [path]
    if not path.is_dir():
        raise ProfileCollectionError("artifact path must be a regular file or directory")
    nested = list(path.rglob("*"))
    if any(item.is_symlink() for item in nested):
        raise ProfileCollectionError(
            "artifact directory must not contain symbolic links"
        )
    files = sorted(
        (item for item in nested if item.is_file()),
        key=lambda item: item.relative_to(path).as_posix(),
    )
    if not files:
        raise ProfileCollectionError("artifact directory contains no regular files")
    return files


def _aggregate_digest(root: Path, files: list[Path]) -> str:
    if root.is_file():
        return _sha256_file(root)
    digest = hashlib.sha256()
    for item in files:
        relative = item.relative_to(root).as_posix()
        file_digest = _sha256_file(item)
        digest.update(f"{relative}\0{item.stat().st_size}\0{file_digest}\n".encode())
    return digest.hexdigest()


def _safetensors_inventory(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        raw_length = handle.read(8)
        if len(raw_length) != 8:
            raise ProfileCollectionError(f"truncated safetensors header: {path.name}")
        header_length = struct.unpack("<Q", raw_length)[0]
        if header_length <= 0 or header_length > path.stat().st_size - 8:
            raise ProfileCollectionError(f"invalid safetensors header length: {path.name}")
        raw_header = handle.read(header_length)
    try:
        header = json.loads(raw_header)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProfileCollectionError(f"invalid safetensors JSON header: {path.name}") from exc
    if not isinstance(header, dict):
        raise ProfileCollectionError(f"invalid safetensors inventory: {path.name}")
    tensor_count = 0
    tensor_bytes = 0
    ranges: list[tuple[int, int]] = []
    for name, descriptor in header.items():
        if name == "__metadata__":
            continue
        if not isinstance(descriptor, dict):
            raise ProfileCollectionError(f"invalid tensor descriptor: {path.name}:{name}")
        offsets = descriptor.get("data_offsets")
        if (
            not isinstance(offsets, list)
            or len(offsets) != 2
            or not all(isinstance(value, int) for value in offsets)
            or offsets[0] < 0
            or offsets[1] < offsets[0]
        ):
            raise ProfileCollectionError(f"invalid tensor offsets: {path.name}:{name}")
        ranges.append((offsets[0], offsets[1]))
        tensor_count += 1
        tensor_bytes += offsets[1] - offsets[0]
    if tensor_count == 0 or tensor_bytes <= 0:
        raise ProfileCollectionError(f"no tensor payload found: {path.name}")
    payload_bytes = path.stat().st_size - 8 - header_length
    ordered = sorted(ranges)
    if ordered[-1][1] > payload_bytes:
        raise ProfileCollectionError(f"tensor payload exceeds file size: {path.name}")
    if any(left[1] > right[0] for left, right in pairwise(ordered)):
        raise ProfileCollectionError(f"overlapping tensor payloads: {path.name}")
    return tensor_count, tensor_bytes


def _gguf_inventory(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:4] != b"GGUF":
        raise ProfileCollectionError("invalid GGUF header")
    version, tensor_count, _metadata_count = struct.unpack("<IQQ", header[4:])
    if version not in {2, 3} or tensor_count <= 0:
        raise ProfileCollectionError("unsupported or empty GGUF artifact")
    # GGUF tensor descriptors require metadata-aware alignment parsing. Until that
    # parser lands, container bytes are the conservative planning footprint.
    return int(tensor_count), path.stat().st_size


def _infer_format(path: Path, files: list[Path], requested: str | None) -> str:
    if requested is not None:
        if requested not in {"gguf", "safetensors", "mlx", "other"}:
            raise ProfileCollectionError(f"unsupported artifact format: {requested}")
        return requested
    if path.is_file() and path.suffix.lower() == ".gguf":
        return "gguf"
    if path.is_file() and path.suffix.lower() == ".safetensors":
        return "safetensors"
    if any(item.suffix.lower() == ".safetensors" for item in files):
        return "safetensors"
    return "other"


def _digest_named_files(root: Path, files: list[Path], names: Iterable[str]) -> str | None:
    selected = [item for item in files if item.name in set(names)]
    if not selected:
        return None
    digest = hashlib.sha256()
    for item in selected:
        relative = item.name if root.is_file() else item.relative_to(root).as_posix()
        digest.update(f"{relative}\0{_sha256_file(item)}\n".encode())
    return digest.hexdigest()


def _chat_template_digest(root: Path, files: list[Path]) -> str | None:
    config = next((item for item in files if item.name == "tokenizer_config.json"), None)
    if config is None:
        return None
    try:
        payload = json.loads(config.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    template = payload.get("chat_template") if isinstance(payload, dict) else None
    return hashlib.sha256(template.encode()).hexdigest() if isinstance(template, str) else None


def _infer_quantization(
    path: Path,
    files: list[Path],
    requested: str | None,
) -> str:
    if requested:
        return requested
    match = re.search(
        r"(?:^|[._-])(Q[0-9](?:_[A-Z0-9]+)*|BF16|F16|F32)(?:[._-]|$)",
        path.name.upper(),
    )
    if match:
        return match.group(1)
    config = next((item for item in files if item.name == "config.json"), None)
    if config is not None:
        try:
            payload = json.loads(config.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            payload = None
        quantization = (
            payload.get("quantization_config") if isinstance(payload, dict) else None
        )
        if isinstance(quantization, dict):
            method = quantization.get("quant_method") or quantization.get("method")
            bits = quantization.get("bits")
            if isinstance(method, str):
                return f"{method}:{bits}bit" if isinstance(bits, int) else method
    return "unknown"


def profile_model_artifact(
    artifact_path: str | os.PathLike[str],
    *,
    profile_id: str,
    model_id: str,
    source_revision: str,
    quantization: str | None = None,
    artifact_format: str | None = None,
) -> tuple[ModelResourceProfile, dict[str, Any]]:
    """Measure a local model artifact without importing or loading model code."""

    path = Path(artifact_path).expanduser()
    files = _safe_artifact_files(path)
    detected_format = _infer_format(path, files, artifact_format)
    detected_quantization = _infer_quantization(path, files, quantization)
    artifact_bytes = sum(item.stat().st_size for item in files)
    artifact_digest = _aggregate_digest(path, files)
    tensor_count = 0
    model_weight_bytes = 0
    inventory_files: list[dict[str, Any]] = []
    unknowns: list[str] = []

    weight_files = [
        item for item in files if item.suffix.lower() in {".safetensors", ".gguf"}
    ]
    if not weight_files:
        raise ProfileCollectionError("no supported local model weight files found")
    for item in weight_files:
        if item.suffix.lower() == ".safetensors":
            count, payload_bytes = _safetensors_inventory(item)
        else:
            count, payload_bytes = _gguf_inventory(item)
            unknowns.append("exact_tensor_weight_bytes")
        tensor_count += count
        model_weight_bytes += payload_bytes
        relative = item.name if path.is_file() else item.relative_to(path).as_posix()
        inventory_files.append(
            {
                "path": relative,
                "artifact_bytes": item.stat().st_size,
                "tensor_count": count,
                "tensor_payload_bytes": payload_bytes,
                "sha256": _sha256_file(item),
            }
        )
    inventory = {
        "schema_version": "hero.tensor-inventory.v1",
        "artifact_id": path.name,
        "artifact_format": detected_format,
        "files": inventory_files,
        "tensor_count": tensor_count,
        "tensor_payload_bytes": model_weight_bytes,
        "claim_boundary": "Static artifact inspection only; no model or runtime was loaded.",
    }
    inventory_digest = hashlib.sha256(
        json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    profile = ModelResourceProfile(
        profile_id=profile_id,
        model_id=model_id,
        artifact_id=path.name,
        artifact_format=detected_format,
        quantization=detected_quantization,
        artifact_bytes=artifact_bytes,
        model_weight_bytes=model_weight_bytes,
        sha256=artifact_digest,
        source_revision=source_revision,
        evidence_level="observed",
        tensor_inventory_ref=f"sha256:{inventory_digest}",
        tokenizer_digest=_digest_named_files(path, files, _TOKENIZER_FILES),
        chat_template_digest=_chat_template_digest(path, files),
        unknown_fields=list(
            dict.fromkeys(
                unknowns + (["quantization"] if detected_quantization == "unknown" else [])
            )
        ),
    )
    return profile, inventory


def write_profile_evidence(
    output_path: str | os.PathLike[str],
    *,
    hardware: HardwareProfile | None = None,
    model: ModelResourceProfile | None = None,
    tensor_inventory: dict[str, Any] | None = None,
) -> Path:
    """Atomically write human-auditable profiler evidence as canonical JSON."""

    if hardware is None and model is None:
        raise ProfileCollectionError("at least one profile is required")
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "hero.profile-evidence.v1",
        "hardware": hardware.model_dump(mode="json") if hardware is not None else None,
        "model": model.model_dump(mode="json") if model is not None else None,
        "tensor_inventory": tensor_inventory,
        "claim_boundary": (
            "Observed static metadata only. This evidence does not prove runtime "
            "compatibility, performance, service quality, or larger-than-VRAM execution."
        ),
    }
    temporary = target.with_name(f".{target.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, target)
    return target


__all__ = [
    "ProfileCollectionError",
    "collect_hardware_profile",
    "profile_model_artifact",
    "write_profile_evidence",
]
