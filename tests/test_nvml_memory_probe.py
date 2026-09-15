import ctypes as ct
import json
from types import SimpleNamespace

import pytest

from kora import nvml_memory_probe as probe

UUID = "GPU-01234567-89ab-cdef-0123-456789abcdef"


class Function:
    def __init__(self, name, owner):
        self.name, self.owner = name, owner

    def __call__(self, *args):
        o, n = self.owner, self.name
        o.calls.append(n)
        if n in o.errors:
            return o.errors[n]
        if n == "nvmlDeviceGetHandleByUUID":
            assert args[0] == UUID.encode()
            ct.cast(args[1], ct.POINTER(ct.c_void_p))[0] = 123
        elif n == "nvmlDeviceGetMemoryInfo":
            # Independent ABI: write three uint64 slots in NVIDIA's field order.
            values = ct.cast(args[1], ct.POINTER(ct.c_ulonglong))
            values[0], values[1], values[2] = o.memory
        elif n == "nvmlDeviceIsMigDeviceHandle":
            ct.cast(args[1], ct.POINTER(ct.c_uint))[0] = o.mig
        elif n == "nvmlDeviceGetMigMode":
            ct.cast(args[1], ct.POINTER(ct.c_uint))[0] = o.mode
            ct.cast(args[2], ct.POINTER(ct.c_uint))[0] = o.mode
        elif n == "nvmlDeviceGetVirtualizationMode":
            ct.cast(args[1], ct.POINTER(ct.c_uint))[0] = o.virtual
        elif n in o.strings:
            args[-2].value = o.strings[n]
        return 0


@pytest.fixture
def nvml(monkeypatch):
    owner = SimpleNamespace(calls=[], errors={}, memory=(8589934501, 8000000001, 589934500),
                            mig=0, mode=0, virtual=0, strings={
                                "nvmlDeviceGetUUID": UUID.encode(),
                                "nvmlDeviceGetName": b"Synthetic GPU",
                                "nvmlSystemGetDriverVersion": b"fixture-driver",
                                "nvmlSystemGetNVMLVersion": b"fixture-nvml",
                            })
    names = ["nvmlInit_v2", "nvmlShutdown", "nvmlDeviceGetHandleByUUID",
             "nvmlDeviceGetMemoryInfo", "nvmlDeviceIsMigDeviceHandle",
             "nvmlDeviceGetMigMode", "nvmlDeviceGetVirtualizationMode", *owner.strings]
    library = SimpleNamespace(**{n: Function(n, owner) for n in names})
    owner.library = library
    monkeypatch.setattr(probe.platform, "system", lambda: "Linux")
    monkeypatch.setattr(probe.ct, "CDLL", lambda name: library)
    return owner


def test_native_bytes_and_no_physical_claim(nvml):
    result = probe.probe_memory(UUID)
    assert (result["total_bytes"], result["free_bytes"], result["used_bytes"]) == nvml.memory
    assert result["total_bytes"] % 1048576 != 0
    assert result["physical_vram_bytes"] is None
    assert result["physical_device_reviewed"] is False
    assert result["reserved_bytes"] is None
    assert result["gpu_uuid"] == UUID
    assert len(result["probe_source_sha256"]) == 64
    assert nvml.calls[0] == "nvmlInit_v2" and nvml.calls[-1] == "nvmlShutdown"
    assert ct.sizeof(probe._Memory) == 24
    assert [getattr(probe._Memory, n).offset for n in ("total", "free", "used")] == [0, 8, 16]
    assert nvml.library.nvmlDeviceGetMemoryInfo.restype is ct.c_int


@pytest.mark.parametrize("uuid", [None, "", "0", "GPU-0", "MIG-" + UUID[4:], UUID + "\n"])
def test_invalid_selection_does_not_query(nvml, uuid):
    with pytest.raises(probe.MemoryProbeError):
        probe.probe_memory(uuid)
    assert nvml.calls == []


@pytest.mark.parametrize("name", ["nvmlInit_v2", "nvmlShutdown", "nvmlDeviceGetHandleByUUID",
                                 "nvmlDeviceGetMemoryInfo", "nvmlDeviceGetUUID",
                                 "nvmlDeviceGetName", "nvmlSystemGetDriverVersion",
                                 "nvmlSystemGetNVMLVersion", "nvmlDeviceIsMigDeviceHandle",
                                 "nvmlDeviceGetMigMode", "nvmlDeviceGetVirtualizationMode"])
def test_query_failures_do_not_publish(nvml, name, tmp_path):
    nvml.errors[name] = 999
    target = tmp_path / "receipt.json"
    with pytest.raises(SystemExit) as exc:
        probe.main(["--gpu-uuid", UUID, "--output", str(target)])
    assert exc.value.code == 2 and not target.exists()
    if name != "nvmlInit_v2":
        assert nvml.calls[-1] == "nvmlShutdown"


def test_missing_function_before_init(nvml):
    del nvml.library.nvmlDeviceGetMemoryInfo
    with pytest.raises(probe.MemoryProbeError, match="missing"):
        probe.probe_memory(UUID)
    assert not nvml.calls


@pytest.mark.parametrize("field,value", [("mig", 1), ("mode", 2), ("virtual", 99)])
def test_bad_modes(nvml, field, value):
    setattr(nvml, field, value)
    with pytest.raises(probe.MemoryProbeError):
        probe.probe_memory(UUID)
    assert nvml.calls[-1] == "nvmlShutdown"


def test_unsupported_modes_stay_unknown(nvml):
    nvml.errors.update(nvmlDeviceGetMigMode=3, nvmlDeviceGetVirtualizationMode=3)
    result = probe.probe_memory(UUID)
    assert result["mig_mode"] == {"nvml_status": 3, "current": None, "pending": None}
    assert result["virtualization"] == {"nvml_status": 3, "mode": None}
    assert result["physical_vram_bytes"] is None


@pytest.mark.parametrize("memory", [(0, 0, 0), (2**64-1, 0, 0), (10, 11, 0), (10, 0, 11)])
def test_invalid_memory(nvml, memory):
    nvml.memory = memory
    with pytest.raises(probe.MemoryProbeError):
        probe.probe_memory(UUID)


@pytest.mark.parametrize("identity", [b"wrong", b"", b"\xff", b"GPU-\n"])
def test_bad_identity(nvml, identity):
    nvml.strings["nvmlDeviceGetUUID"] = identity
    with pytest.raises(probe.MemoryProbeError):
        probe.probe_memory(UUID)


def test_platform_guard(nvml, monkeypatch):
    monkeypatch.setattr(probe.platform, "system", lambda: "Darwin")
    with pytest.raises(probe.MemoryProbeError, match="Linux"):
        probe.probe_memory(UUID)
    assert not nvml.calls


def test_library_unavailable(nvml, monkeypatch):
    def unavailable(name):
        raise OSError("fixture missing library")
    monkeypatch.setattr(probe.ct, "CDLL", unavailable)
    with pytest.raises(probe.MemoryProbeError, match="unavailable"):
        probe.probe_memory(UUID)


def test_cli_exclusive_receipt(nvml, tmp_path):
    target = tmp_path / "receipt.json"
    assert probe.main(["--gpu-uuid", UUID, "--output", str(target)]) == 0
    before = target.read_bytes()
    assert json.loads(before)["total_bytes"] == nvml.memory[0]
    nvml.calls.clear()
    with pytest.raises(SystemExit):
        probe.main(["--gpu-uuid", UUID, "--output", str(target)])
    assert target.read_bytes() == before and not nvml.calls


def test_output_symlink_rejected_before_query(nvml, tmp_path):
    target = tmp_path / "receipt.json"
    target.symlink_to(tmp_path / "missing")
    with pytest.raises(SystemExit):
        probe.main(["--gpu-uuid", UUID, "--output", str(target)])
    assert target.is_symlink() and not nvml.calls


def test_cli_stdout(nvml, capsys):
    assert probe.main(["--gpu-uuid", UUID]) == 0
    assert json.loads(capsys.readouterr().out)["memory_unit"] == "bytes"
