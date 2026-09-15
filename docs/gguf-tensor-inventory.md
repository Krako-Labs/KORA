# Offline GGUF tensor inventory

The existing resource profiler records GGUF container size as a conservative
planning footprint. Container size includes metadata and padding, so it cannot
establish an exact tensor payload sum.

The independent inventory utility inspects a local single-file GGUF without
loading a model, allocating GPU memory, importing a runtime, or downloading files:

```bash
python -m kora.gguf_inventory ./model.gguf --output ./tensor-inventory.json
```

The output directory must exist. An existing output, including a symbolic link,
is rejected; successful writes publish complete JSON atomically and exclusively.
No metadata payload or source path is included in the inventory. Tensor names
are retained as evidence; keep real artifact inventories private unless reviewed.

## What the bytes mean

Each tensor record includes its name, numeric GGML type, dimensions in GGML order,
file/data offsets and serialized payload bytes. The sum excludes header metadata,
alignment padding, gaps between tensors and trailing bytes. The full artifact
SHA-256 covers all bytes; artifact bytes and non-tensor bytes are reported separately.
The receipt includes the parser source SHA-256 and pinned layout-reference revision.

The result deliberately inventories **all serialized tensors in one file**.
It does not infer which tensors serve text generation or prove that a model is
complete. `text_model_weight_bytes` stays null and
`text_tensor_selection_reviewed` stays false, even for a file containing only
familiar-looking names. A separate reviewed text-tensor selection, artifact
provenance/license record and physical VRAM observation are needed for any
weight-to-VRAM claim.

This is a separate API/CLI. It does not change the existing profiler, planner,
runtime adapters, replay fixtures, or benchmark acceptance behavior.

## Supported and rejected input

Supported: little-endian GGUF v2/v3, 1-4 tensor dimensions; F32, F16, BF16;
Q4_0/Q4_1, Q5_0/Q5_1, Q8_0/Q8_1 and Q2_K through Q8_K.
A file-level Q4_K_M label is not a tensor encoding: its individual tensors may
use different supported types, each counted using its own descriptor.

Unknown versions, byte orders, tensor/metadata types, split metadata, duplicate
keys/names, invalid dimensions/quantized rows, alignment errors, overlapping or
out-of-file payloads, invalid strings/booleans, nonregular files, leaf symlinks and
detected input changes fail closed. There is no container-size fallback.

Resource limits: 64 MiB parsed header, 16 MiB per metadata string, one million
metadata values, eight nested-array levels, 100,000 tensors, 64-byte tensor names
and power-of-two alignment up to 65,536. These bounded limits may reject otherwise
supported large files; rejection is not model incompatibility. Split/sharded and
new quantization support require a separate extension and validation.

Input integrity assumes trusted local storage: the same open file descriptor is
parsed and hashed, with before/after identity/size/time checks. This is not a
security sandbox against a hostile filesystem.

## Validation and limits

Tiny synthetic GGUF files exercise independent wire-format expectations,
mixed tensor sizes, metadata arrays, alignment/gaps, truncation at every required
byte, malformed lengths/types/ranges, mutation and exclusive output behavior.
These are parser tests, not downloaded-model, GPU, inference or service-quality
measurements. No physical benchmark, runtime compatibility, larger-than-VRAM
execution or performance claim follows.

A previously locked replay package must continue using its original wheel and
lock. Adding package source changes the package fingerprint; do not regenerate
an old lock to hide drift or run a newer source tree under the old identity.

## Format references

Layout facts are pinned to:
- [GGUF specification, ggml 456172e](https://github.com/ggml-org/ggml/blob/456172ec733a135778adcd32d00e576a58232e45/docs/gguf.md).
- [Tensor block sizes and type IDs, llama.cpp 9e71716](https://github.com/ggml-org/llama.cpp/blob/9e71716247113b47bb831d1e0680cbf5f242f094/gguf-py/gguf/constants.py).

Only the listed layout subset is supported. No upstream implementation is
vendored or imported by the production utility.
