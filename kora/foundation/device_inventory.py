"""Privacy-safe local device discovery for the KORA Foundation layer.

This module only inspects local metadata. It does not start model runtimes,
perform inference, call providers, or collect serial numbers, hardware UUIDs,
or network MAC addresses.
"""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import asdict, dataclass
from typing import Any

SCHEMA_VERSION = "kora_foundation_device_inventory_v0"
UNKNOWN = "unknown"

CommandExecutor = Callable[[tuple[str, ...]], str | None]
ExecutableDetector = Callable[[str], str | None]


@dataclass(frozen=True)
class RuntimeCandidate:
    """A runtime executable detected locally without starting it."""

    name: str
    detected: bool
    command: str | None
    status: str


@dataclass(frozen=True)
class NetworkInterface:
    """Privacy-safe local network hardware-port record."""

    hardware_port: str
    device: str
    category: str


@dataclass(frozen=True)
class TransportCapability:
    """A transport KORA may benchmark later; detection is not a performance claim."""

    name: str
    detected: bool
    status: str
    devices: tuple[str, ...]
    max_link_speed_gbps: float | None = None
    notes: str | None = None


@dataclass(frozen=True)
class DeviceInventory:
    """Normalized local device metadata for later capability and routing policy."""

    schema_version: str
    node_name: str
    os_name: str
    os_version: str
    architecture: str
    chip_model: str
    total_memory_gb: float | None
    physical_cpu_cores: int | None
    logical_cpu_cores: int | None
    gpu_models: tuple[str, ...]
    gpu_core_counts: tuple[int, ...]
    runtime_candidates: tuple[RuntimeCandidate, ...]
    network_interfaces: tuple[NetworkInterface, ...]
    transports: tuple[TransportCapability, ...]
    inventory_status: str
    collection_scope: str
    sensitive_identifiers_collected: bool
    claim_boundary: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready representation."""

        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DeviceInventory:
        """Validate and load an inventory produced by :meth:`to_dict`."""

        if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"expected schema_version {SCHEMA_VERSION!r}")
        required_strings = ("node_name", "os_name", "os_version", "architecture", "chip_model")
        for field in required_strings:
            if not isinstance(data.get(field), str) or not data[field].strip():
                raise ValueError(f"inventory field {field!r} must be a non-empty string")
        if data.get("sensitive_identifiers_collected") is not False:
            raise ValueError("inventory must explicitly exclude sensitive identifiers")
        try:
            runtimes = tuple(RuntimeCandidate(**item) for item in data["runtime_candidates"])
            interfaces = tuple(NetworkInterface(**item) for item in data["network_interfaces"])
            transports = tuple(TransportCapability(**item) for item in data["transports"])
            return cls(
                **{
                    **data,
                    "gpu_models": tuple(data["gpu_models"]),
                    "gpu_core_counts": tuple(data["gpu_core_counts"]),
                    "runtime_candidates": runtimes,
                    "network_interfaces": interfaces,
                    "transports": transports,
                }
            )
        except (KeyError, TypeError) as exc:
            raise ValueError(f"malformed device inventory: {exc}") from exc


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
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _safe_text(value: str | None) -> str:
    text = (value or "").strip()
    return text or UNKNOWN


def _parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        parsed = int(value.strip())
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def _sysctl(key: str, executor: CommandExecutor) -> str | None:
    return executor(("sysctl", "-n", key))


def _detect_memory_gb(os_name: str, executor: CommandExecutor) -> float | None:
    if os_name == "Darwin":
        memory_bytes = _parse_int(_sysctl("hw.memsize", executor))
        if memory_bytes:
            return round(memory_bytes / (1024**3), 2)

    if hasattr(os, "sysconf"):
        try:
            page_size = os.sysconf("SC_PAGE_SIZE")
            page_count = os.sysconf("SC_PHYS_PAGES")
        except (OSError, ValueError):
            return None
        if isinstance(page_size, int) and isinstance(page_count, int) and page_size > 0 and page_count > 0:
            return round((page_size * page_count) / (1024**3), 2)
    return None


def _detect_cpu_counts(os_name: str, executor: CommandExecutor) -> tuple[int | None, int | None]:
    logical = os.cpu_count()
    physical: int | None = None
    if os_name == "Darwin":
        physical = _parse_int(_sysctl("hw.physicalcpu", executor))
        logical = _parse_int(_sysctl("hw.logicalcpu", executor)) or logical
    return physical, logical


def _detect_chip_model(os_name: str, executor: CommandExecutor) -> str:
    if os_name == "Darwin":
        brand = _sysctl("machdep.cpu.brand_string", executor)
        if brand:
            return _safe_text(brand)
    return _safe_text(platform.processor())


def _detect_gpu(os_name: str, executor: CommandExecutor) -> tuple[tuple[str, ...], tuple[int, ...]]:
    if os_name != "Darwin":
        return (), ()

    raw = executor(("system_profiler", "SPDisplaysDataType", "-json"))
    if not raw:
        return (), ()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return (), ()

    models: list[str] = []
    cores: list[int] = []
    for item in payload.get("SPDisplaysDataType", []):
        if not isinstance(item, dict):
            continue
        model = item.get("sppci_model") or item.get("_name")
        if isinstance(model, str) and model.strip():
            models.append(model.strip())
            core_count = _parse_int(str(item.get("sppci_cores", "")))
            cores.append(core_count or 0)

    # Preserve stable ordering while removing duplicate GPU records.
    unique_models: list[str] = []
    unique_cores: list[int] = []
    seen: set[tuple[str, int]] = set()
    for model, core_count in zip(models, cores, strict=True):
        key = (model, core_count)
        if key in seen:
            continue
        seen.add(key)
        unique_models.append(model)
        unique_cores.append(core_count)
    return tuple(unique_models), tuple(unique_cores)


def _network_category(hardware_port: str) -> str:
    text = hardware_port.lower()
    if "thunderbolt bridge" in text:
        return "thunderbolt_bridge"
    if text.startswith("thunderbolt"):
        return "thunderbolt_interface"
    if "wi-fi" in text or "wifi" in text:
        return "wifi"
    if "ethernet" in text:
        return "ethernet"
    return "other"


def _detect_network_interfaces(os_name: str, executor: CommandExecutor) -> tuple[NetworkInterface, ...]:
    if os_name != "Darwin":
        return ()

    raw = executor(("networksetup", "-listallhardwareports"))
    if not raw:
        return ()

    interfaces: list[NetworkInterface] = []
    hardware_port: str | None = None
    device: str | None = None

    def flush() -> None:
        nonlocal hardware_port, device
        if hardware_port and device:
            interfaces.append(
                NetworkInterface(
                    hardware_port=hardware_port,
                    device=device,
                    category=_network_category(hardware_port),
                )
            )
        hardware_port = None
        device = None

    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("Hardware Port:"):
            flush()
            hardware_port = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("Device:"):
            device = stripped.split(":", 1)[1].strip()
        # Intentionally ignore Ethernet Address / MAC-address lines.
    flush()
    return tuple(interfaces)


def _detect_thunderbolt_max_speed(os_name: str, executor: CommandExecutor) -> float | None:
    if os_name != "Darwin":
        return None
    raw = executor(("system_profiler", "SPThunderboltDataType", "-json"))
    if not raw:
        return None
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None

    speeds: list[float] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "current_speed_key" and isinstance(child, str):
                    match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*Gb/s", child, re.IGNORECASE)
                    if match:
                        speeds.append(float(match.group(1)))
                else:
                    walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload.get("SPThunderboltDataType", []))
    return max(speeds) if speeds else None


def detect_runtime_candidates(which: ExecutableDetector = shutil.which) -> tuple[RuntimeCandidate, ...]:
    """Detect runtime commands without starting model servers or loading models."""

    specs: tuple[tuple[str, tuple[str, ...]], ...] = (
        ("mlx-lm", ("mlx_lm.server", "mlx_lm.generate", "mlx_lm.chat")),
        ("llama.cpp", ("llama-server", "llama-cli", "llama")),
        ("ollama", ("ollama",)),
        ("lm-studio", ("lms", "llmster")),
        ("exo", ("exo",)),
        ("localai", ("local-ai", "localai")),
        ("vllm", ("vllm",)),
    )

    candidates: list[RuntimeCandidate] = []
    for name, commands in specs:
        command: str | None = None
        for candidate in commands:
            found = which(candidate)
            if found:
                command = candidate
                break
        candidates.append(
            RuntimeCandidate(
                name=name,
                detected=command is not None,
                command=command,
                status="detected" if command is not None else "not_detected",
            )
        )
    return tuple(candidates)


def _transport(
    name: str,
    interfaces: tuple[NetworkInterface, ...],
    categories: set[str],
    *,
    max_link_speed_gbps: float | None = None,
    notes: str | None = None,
) -> TransportCapability:
    devices = tuple(item.device for item in interfaces if item.category in categories)
    return TransportCapability(
        name=name,
        detected=bool(devices),
        status="detected" if devices else "not_detected",
        devices=devices,
        max_link_speed_gbps=max_link_speed_gbps if devices else None,
        notes=notes,
    )


def collect_device_inventory(
    *,
    executor: CommandExecutor = _default_executor,
    which: ExecutableDetector = shutil.which,
    node_name: str | None = None,
    os_name: str | None = None,
    os_version: str | None = None,
    architecture: str | None = None,
) -> DeviceInventory:
    """Collect privacy-safe local metadata for KORA Foundation device discovery."""

    detected_os = os_name or platform.system()
    if os_version is not None:
        detected_os_version = os_version
    elif detected_os == "Darwin":
        detected_os_version = platform.mac_ver()[0] or platform.release()
    else:
        detected_os_version = platform.release()

    detected_architecture = architecture or platform.machine()
    chip_model = _detect_chip_model(detected_os, executor)
    total_memory_gb = _detect_memory_gb(detected_os, executor)
    physical_cpu_cores, logical_cpu_cores = _detect_cpu_counts(detected_os, executor)
    gpu_models, gpu_core_counts = _detect_gpu(detected_os, executor)
    if chip_model.lower() in {"arm", "arm64", "aarch64", UNKNOWN} and gpu_models:
        chip_model = gpu_models[0]
    network_interfaces = _detect_network_interfaces(detected_os, executor)
    runtime_candidates = detect_runtime_candidates(which)
    thunderbolt_speed = _detect_thunderbolt_max_speed(detected_os, executor)

    transports = (
        _transport("ethernet", network_interfaces, {"ethernet"}),
        _transport(
            "thunderbolt_bridge",
            network_interfaces,
            {"thunderbolt_bridge"},
            max_link_speed_gbps=thunderbolt_speed,
            notes="Detected transport only; performance must be benchmarked before routing decisions.",
        ),
        _transport("wifi", network_interfaces, {"wifi"}),
    )

    critical_unknown = any(
        value in {"", UNKNOWN}
        for value in (
            _safe_text(detected_os),
            _safe_text(detected_os_version),
            _safe_text(detected_architecture),
            chip_model,
        )
    ) or total_memory_gb is None or physical_cpu_cores is None

    return DeviceInventory(
        schema_version=SCHEMA_VERSION,
        node_name=_safe_text(node_name or platform.node()),
        os_name=_safe_text(detected_os),
        os_version=_safe_text(detected_os_version),
        architecture=_safe_text(detected_architecture),
        chip_model=chip_model,
        total_memory_gb=total_memory_gb,
        physical_cpu_cores=physical_cpu_cores,
        logical_cpu_cores=logical_cpu_cores,
        gpu_models=gpu_models,
        gpu_core_counts=gpu_core_counts,
        runtime_candidates=runtime_candidates,
        network_interfaces=network_interfaces,
        transports=transports,
        inventory_status="detected_with_unknowns" if critical_unknown else "detected",
        collection_scope="local_metadata_only",
        sensitive_identifiers_collected=False,
        claim_boundary=(
            "Inventory records detected local metadata only. It does not prove runtime compatibility, "
            "model fit, transport performance, multi-node scaling, cost savings, or production readiness."
        ),
    )


def render_device_inventory_text(inventory: DeviceInventory | dict[str, Any]) -> str:
    """Render a concise human-readable inventory summary."""

    data = inventory.to_dict() if isinstance(inventory, DeviceInventory) else inventory
    memory = data.get("total_memory_gb")
    memory_text = f"{memory:g} GB" if isinstance(memory, (int, float)) else UNKNOWN

    gpu_models = data.get("gpu_models") or []
    gpu_cores = data.get("gpu_core_counts") or []
    gpu_parts: list[str] = []
    for index, model in enumerate(gpu_models):
        cores = gpu_cores[index] if index < len(gpu_cores) else 0
        gpu_parts.append(f"{model} ({cores} cores)" if cores else str(model))
    gpu_text = ", ".join(gpu_parts) if gpu_parts else "not detected"

    lines = [
        "KORA Foundation Device Inventory",
        f"Node: {data.get('node_name', UNKNOWN)}",
        f"OS: {data.get('os_name', UNKNOWN)} {data.get('os_version', UNKNOWN)}",
        f"Architecture: {data.get('architecture', UNKNOWN)}",
        f"Chip: {data.get('chip_model', UNKNOWN)}",
        f"Memory: {memory_text}",
        f"CPU cores: physical={data.get('physical_cpu_cores')} logical={data.get('logical_cpu_cores')}",
        f"GPU: {gpu_text}",
        "Transports:",
    ]

    for transport in data.get("transports", []):
        name = transport.get("name", UNKNOWN)
        status = transport.get("status", UNKNOWN)
        devices = transport.get("devices", [])
        speed = transport.get("max_link_speed_gbps")
        detail = f" [{', '.join(devices)}]" if devices else ""
        if isinstance(speed, (int, float)):
            detail += f" up to {speed:g} Gb/s detected"
        lines.append(f"  - {name}: {status}{detail}")

    lines.append("Runtime candidates:")
    for runtime in data.get("runtime_candidates", []):
        command = runtime.get("command")
        suffix = f" ({command})" if command else ""
        lines.append(f"  - {runtime.get('name', UNKNOWN)}: {runtime.get('status', UNKNOWN)}{suffix}")

    lines.extend(
        [
            f"Privacy: {data.get('collection_scope', UNKNOWN)}; sensitive identifiers collected={data.get('sensitive_identifiers_collected')}",
            f"Status: {data.get('inventory_status', UNKNOWN)}",
            f"Boundary: {data.get('claim_boundary', '')}",
        ]
    )
    return "\n".join(lines) + "\n"
