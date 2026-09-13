# Task032 — Byte-Based Hardware and Model Resource Profilers

Status: needs-cto-review
Risk: medium — new local metadata collection and artifact inspection
Base: f15f3f639a85a13b75d53d80b9fda128ec0fda79

- branch: feat/task032-resource-profilers
- PR: pending
- risk level: medium
- final status classification: needs-cto-review

## Outcome

Task032 connects observed, byte-based local facts to the Task031 Hero contracts
without loading a model or starting a runtime.

Delivered:

- exact physical-memory collection for Apple Silicon and Linux hosts;
- explicit unified, system, and dedicated-GPU memory domains;
- Apple display metadata parsing and fixture-covered NVIDIA metadata parsing;
- detection of MLX-LM, llama.cpp, FreeToken, and KTransformers executables
  without starting them;
- static GGUF and safetensors artifact inspection;
- exact safetensors tensor-payload totals and per-shard inventory;
- conservative GGUF container-byte planning with the unresolved exact tensor
  byte count declared as unknown;
- automatic GGUF filename and model-config quantization detection;
- artifact, tokenizer, chat-template, and tensor-inventory digests;
- atomic, claim-bounded JSON evidence export;
- direct compatibility with Task031 HardwareProfile, ModelResourceProfile,
  and feasibility-plan inputs.

## Safety and failure behavior

The profiler fails closed when exact physical memory cannot be observed. It also
rejects malformed safetensors headers, out-of-range or overlapping tensor
offsets, unsupported artifacts, and symbolic-link artifact roots or contents.

Artifact evidence contains relative artifact names and digests, not absolute
local paths. Hardware evidence does not collect serial numbers, hardware UUIDs,
MAC addresses, user names, or network identifiers.

No model code is imported. No model weights are loaded into memory. Runtime
executables are detected by path only and are not started.

## Validation

Executed locally:

- focused Hero profiler, contract, and feasibility tests: 23 passed;
- full repository suite: 830 passed;
- Python compileall: passed;
- diff whitespace check: passed;
- Apple Silicon metadata-only smoke: passed.

The metadata smoke observed one 34,359,738,368-byte unified-memory domain and an
Apple M2 Max accelerator on the development machine. This is hardware metadata,
not performance evidence.

The first metadata smoke used a system Python without the project dependency
set and stopped at import time. The same command passed in the repository-managed
environment. No runtime or model was started in either attempt.

## Claim boundary

Task032 proves only that static local facts can be normalized into the Hero
planning contracts.

It does not prove:

- runtime compatibility;
- successful model loading;
- inference performance or service quality;
- a 2x or 3x larger-than-VRAM result;
- GPU-memory oversubscription;
- cost, energy, or hardware superiority;
- production readiness.

The physical NVIDIA reference-PC measurement remains in H0-B after AI Festa.

Forbidden-action audit: no provider call, model download, model inference,
H100 session, CUDA workload, semantic grading, human grading, production
validation, release, repository-setting change, or public claim expansion was
performed.

## Review focus

1. Whether conservative GGUF container bytes are the correct planning value
   until the full metadata-aware tensor layout parser is implemented.
2. Whether hardware profiles should retain only detected runtime candidates or
   also list explicitly undetected candidates.
3. Whether evidence exports need detached signatures before finals evidence
   packaging.
4. Whether Windows physical-memory probing belongs in the next bounded task.

No merge is authorized by this report.
