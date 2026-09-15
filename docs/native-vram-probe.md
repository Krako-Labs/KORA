# Native NVML memory observation

`kora.nvml_memory_probe` provides an explicit, read-only query on a trusted
64-bit Linux host with an already installed NVIDIA NVML library. It accepts one
full GPU UUID; it does not select an arbitrary index or discover remote hosts.

```bash
python -m kora.nvml_memory_probe --gpu-uuid "$GPU_UUID" --output new-memory-receipt.json
```

Set `GPU_UUID` to the exact approved local device UUID before running. No query
occurs on import or `--help`. The module does not install a driver, download a
model, create a CUDA context, allocate GPU memory, launch inference, or change
device settings. Running it still requires authorized access to the target host.
It does not acquire resource reservations or establish that a shared GPU is idle.

The receipt includes the selected UUID/name, driver and NVML versions, observation
time, probe source SHA-256, MIG and virtualization query statuses, and original
integer `total_bytes`, `free_bytes`, and `used_bytes`. It uses the v1
`nvmlDeviceGetMemoryInfo` / `nvmlMemory_t` ABI. The counters are bytes; there is no
MiB conversion. Reserved memory is not separately available through this version
and remains `null`. See NVIDIA's [memory structure](https://docs.nvidia.com/deploy/nvml-api/api/structnvmlMemory__t.html)
and [device query reference](https://docs.nvidia.com/deploy/nvml-api/api/group__nvmlDeviceQueries.html).

`total_bytes` is the driver's reported framebuffer capacity. It is not a promise
of allocatable space, a nominal marketing capacity, or proof of a physical
dedicated device. ECC and the operating environment affect interpretation.
`physical_device_reviewed` remains false and `physical_vram_bytes` remains null.
Bind this receipt to separately reviewed hardware/PCI identity, environment,
isolation and provenance before using it as a physical benchmark denominator.
No device eligibility or memory-ratio threshold is embedded in the probe.

Missing required symbols, query failures, an identity mismatch, a MIG device
handle, or invalid counters reject the observation. Unsupported MIG-mode or
virtualization queries are recorded explicitly with null values, never inferred
as disabled. Parent devices with MIG enabled and known virtualized devices remain
observations requiring review; they are not certified as suitable physical hosts.
The three memory counters are a driver snapshot, not a synchronized workload
measurement. No relationship between their sum is imposed across driver modes.

The output parent must exist. Receipt creation is exclusive and never overwrites
an existing file or symlink. Preserve receipts locally: UUIDs identify hardware.
The standard shared-library search path is trusted; this is not a hostile-host
security boundary. The tool has no Windows or macOS native probing path and no
fallback to rounded `nvidia-smi` output. Existing planning profiles are unchanged.

Tests use synthetic NVML responses, including non-MiB-aligned counters, ctypes
layout, query failures and exclusive output. Passing them establishes software
behavior; actual hardware/driver validation remains a separate prerequisite.

ABI declarations were checked against the official NVIDIA/go-nvml header at
[revision e5441f354b4c7dea74ad35ebe22b774bb5c36ec5](https://github.com/NVIDIA/go-nvml/blob/e5441f354b4c7dea74ad35ebe22b774bb5c36ec5/pkg/nvml/nvml.h).
The reference header is not vendored into this package.
