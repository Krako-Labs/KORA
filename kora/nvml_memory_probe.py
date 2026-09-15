"""Explicit local NVML observation; no allocation, model load or settings change."""
from __future__ import annotations

import argparse
import ctypes as ct
import hashlib
import json
import platform
import re
from datetime import datetime, timezone
from pathlib import Path

from kora.gguf_inventory import write_inventory

PROBE_VERSION = "kora.nvml-memory-probe.v1"
_UUID = re.compile(r"GPU-[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}")
_NOT_SUPPORTED = 3


class MemoryProbeError(ValueError):
    """No complete native-byte observation could be produced."""


class _Memory(ct.Structure):
    # nvmlMemory_t, not nvmlMemory_v2_t. NVML defines all three in bytes.
    _fields_ = [(name, ct.c_ulonglong) for name in ("total", "free", "used")]


def _bind(library, name, arguments):
    try:
        function = getattr(library, name)
    except AttributeError as exc:
        raise MemoryProbeError(f"required NVML function missing: {name}") from exc
    function.argtypes = arguments
    function.restype = ct.c_int
    return function


def _check(code, name):
    if code != 0:
        raise MemoryProbeError(f"{name} failed with NVML status {code}")


def _string(function, *arguments):
    buffer = ct.create_string_buffer(256)
    _check(function(*arguments, buffer, len(buffer)), "identity query")
    try:
        value = buffer.value.decode("ascii")
    except UnicodeDecodeError as exc:
        raise MemoryProbeError("invalid NVML identity string") from exc
    if not value or len(value) == 256 or any(ord(c) < 32 or ord(c) > 126 for c in value):
        raise MemoryProbeError("invalid NVML identity string")
    return value


def _observe(library, gpu_uuid):
    handle_type = ct.c_void_p
    uint_pointer = ct.POINTER(ct.c_uint)
    init = _bind(library, "nvmlInit_v2", [])
    shutdown = _bind(library, "nvmlShutdown", [])
    by_uuid = _bind(library, "nvmlDeviceGetHandleByUUID", [ct.c_char_p, ct.POINTER(handle_type)])
    strings = {
        name: _bind(library, name, args + [ct.POINTER(ct.c_char), ct.c_uint])
        for name, args in {
            "nvmlDeviceGetUUID": [handle_type],
            "nvmlDeviceGetName": [handle_type],
            "nvmlSystemGetDriverVersion": [],
            "nvmlSystemGetNVMLVersion": [],
        }.items()
    }
    memory_query = _bind(library, "nvmlDeviceGetMemoryInfo", [handle_type, ct.POINTER(_Memory)])
    is_mig = _bind(library, "nvmlDeviceIsMigDeviceHandle", [handle_type, uint_pointer])
    mig_mode = _bind(library, "nvmlDeviceGetMigMode", [handle_type, uint_pointer, uint_pointer])
    virtual = _bind(library, "nvmlDeviceGetVirtualizationMode", [handle_type, uint_pointer])
    _check(init(), "nvmlInit_v2")
    try:
        handle = handle_type()
        _check(by_uuid(gpu_uuid.encode("ascii"), ct.byref(handle)), "UUID selection")
        if not handle.value:
            raise MemoryProbeError("null GPU handle")
        actual_uuid = _string(strings["nvmlDeviceGetUUID"], handle)
        if actual_uuid.lower() != gpu_uuid.lower():
            raise MemoryProbeError("selected GPU UUID mismatch")
        mig = ct.c_uint()
        _check(is_mig(handle, ct.byref(mig)), "MIG handle query")
        if mig.value != 0:
            raise MemoryProbeError("MIG device handles are not supported")
        current, pending, virtualization = ct.c_uint(), ct.c_uint(), ct.c_uint()
        mig_status = mig_mode(handle, ct.byref(current), ct.byref(pending))
        virtual_status = virtual(handle, ct.byref(virtualization))
        for code, name in [(mig_status, "MIG mode"), (virtual_status, "virtualization")]:
            if code not in (0, _NOT_SUPPORTED):
                _check(code, name)
        if mig_status == 0 and (current.value not in (0, 1) or pending.value not in (0, 1)):
            raise MemoryProbeError("invalid MIG mode")
        if virtual_status == 0 and virtualization.value not in range(5):
            raise MemoryProbeError("unsupported virtualization mode value")
        memory = _Memory()
        _check(memory_query(handle, ct.byref(memory)), "native memory query")
        total, free, used = memory.total, memory.free, memory.used
        if not 0 < total < 2**64 - 1 or free > total or used > total:
            raise MemoryProbeError("invalid native memory byte counters")
        # These are a driver snapshot, not a promise of allocatable capacity.
        if _string(strings["nvmlDeviceGetUUID"], handle) != actual_uuid:
            raise MemoryProbeError("GPU identity changed during observation")
        return {
            "schema_version": PROBE_VERSION,
            "observed_at_utc": datetime.now(timezone.utc).isoformat(),
            "gpu_uuid": actual_uuid,
            "gpu_name": _string(strings["nvmlDeviceGetName"], handle),
            "driver_version": _string(strings["nvmlSystemGetDriverVersion"]),
            "nvml_version": _string(strings["nvmlSystemGetNVMLVersion"]),
            "memory_api": "nvmlDeviceGetMemoryInfo",
            "memory_structure": "nvmlMemory_t",
            "memory_unit": "bytes",
            "total_bytes": total, "free_bytes": free, "used_bytes": used,
            "reserved_bytes": None,
            "mig_device_handle": False,
            "mig_mode": {"nvml_status": mig_status,
                         "current": current.value if mig_status == 0 else None,
                         "pending": pending.value if mig_status == 0 else None},
            "virtualization": {"nvml_status": virtual_status,
                               "mode": virtualization.value if virtual_status == 0 else None},
            "physical_device_reviewed": False,
            "physical_vram_bytes": None,
            "probe_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "claim_boundary": (
                "Native driver observation only; physical dedicated-device identity, "
                "nominal capacity, isolation, allocatable memory, model fit and "
                "performance require separate evidence and review."
            ),
        }
    finally:
        _check(shutdown(), "nvmlShutdown")


def probe_memory(gpu_uuid: str) -> dict:
    """Read one explicitly selected GPU on Linux64 using the installed NVML.

    No fallback to rounded command output, free memory, caps or another device.
    The loader uses the trusted host's normal shared-library search path.
    """
    if not isinstance(gpu_uuid, str) or not _UUID.fullmatch(gpu_uuid):
        raise MemoryProbeError("a full GPU UUID is required")
    if platform.system() != "Linux" or ct.sizeof(ct.c_void_p) != 8:
        raise MemoryProbeError("this probe requires a 64-bit Linux host")
    try:
        library = ct.CDLL("libnvidia-ml.so.1")
    except OSError as exc:
        raise MemoryProbeError("installed NVML library is unavailable") from exc
    return _observe(library, gpu_uuid)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gpu-uuid", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.output and (args.output.exists() or args.output.is_symlink()):
            raise MemoryProbeError("output already exists")
        result = probe_memory(args.gpu_uuid)
        if args.output:
            write_inventory(args.output, result)
        else:
            print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    except (MemoryProbeError, OSError, ValueError) as exc:
        parser.exit(2, f"native memory probe failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
