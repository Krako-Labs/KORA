# Task033 — Runtime Capability Registry and Execution Planner v1

Status: needs-cto-review
Risk: medium — new public planner integration and runtime declarations
Base: `f6de32c80b994b9f92248eeaa19b9f66d4792e3d`

- branch: `feat/task033-runtime-planner`
- PR: https://github.com/Krako-Labs/KORA/pull/302
- risk level: medium
- final status classification: `needs-cto-review`

## Outcome

Task033 connects the Task032 profile outputs to the Task031 feasibility and
event contracts without starting a runtime or loading a model.

Delivered:

- a stable runtime capability registry for MLX-LM, llama.cpp, FreeToken, and
  KTransformers;
- normalized detection aliases bound to the hardware profiler's path-only
  runtime candidates;
- platform- and artifact-aware default adapter priority;
- deterministic planner integration from hardware profile, model resource
  profile, and workload requirements to one execution plan;
- replayable planning events for workload analysis, capability registration,
  plan creation, and evidence sealing;
- evidence references linking hardware, model, tensor inventory, and planning
  digest;
- atomic, human-readable JSON planning evidence export;
- bundle validation for profile references, capability/candidate identity,
  contiguous event sequences, planning-only event scope, and sealed digest.

## Planner behavior

The default priority is intentionally narrow:

- Apple Silicon considers MLX-LM first and llama.cpp as the GGUF baseline.
- General PC GGUF planning considers llama.cpp first.
- NVIDIA plus safetensors exposes FreeToken first and KTransformers as the
  challenger.
- A runtime is selectable only when it was detected by the profiler and all
  declared platform, architecture, artifact, and memory constraints pass.
- Missing KV-cache or runtime-reserve estimates remain `unknown` and cannot be
  selected.
- Capability declarations retain `fixture` evidence level even when executable
  detection comes from an observed hardware profile. Detection does not upgrade
  declared compatibility into execution proof.

This priority is planning policy, not a measured ranking. Runtime launch,
placement realization, and service acceptance remain separate later gates.

## Fixture evidence

Two planning fixtures exercise the first target shapes:

1. Apple unified-memory fixture:
   - 32 GiB unified memory;
   - 18 GiB safetensors weight footprint;
   - 1 GiB KV estimate and 2 GiB runtime reserve;
   - detected MLX-LM and llama.cpp candidates;
   - planner selects MLX-LM without runtime execution.
2. General PC fixture:
   - 32 GiB system RAM and 8 GiB dedicated GPU memory;
   - 18 GiB GGUF weight footprint;
   - 1 GiB KV estimate and 2 GiB runtime reserve;
   - detected llama.cpp candidate;
   - planner selects the hybrid path based on host capacity and explicitly
     retains `placement_requires_runtime_plan`.

These are synthetic fixture decisions. They are not physical benchmark results
and do not establish practical speed, latency, quality, or larger-than-VRAM
execution.

## Event and evidence surface

Each planning bundle emits this ordered prefix:

1. `run.started`
2. `workload.analyzed`
3. `runtime.capabilities.registered`
4. `execution.plan.created`
5. `evidence.sealed`

The event payload exposes the selected adapter or fail-closed result and every
candidate reason code. It explicitly records that no runtime was started. The
sealed SHA-256 covers the frozen hardware profile, model resource profile,
workload requirements, registry capabilities, and execution plan.

The replay reducer recognizes the two new planner event types as non-state
events. Replaying the prefix leaves the run active and unaccepted; it cannot
represent a completed or quality-accepted outcome.

## Changed files

- `kora/hero_runtime_registry.py`
- `kora/hero_planner.py`
- `kora/hero_replay.py`
- `tests/test_hero_runtime_registry.py`
- `tests/test_hero_planner.py`
- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- this report

## Validation

Executed locally without model/provider/GPU/server work:

- focused Hero contracts, feasibility, replay, profiler, registry, and planner
  tests: 44 passed;
- full repository suite: 842 passed;
- Ruff over changed Python source and tests: passed;
- Python compileall: passed;
- staged diff whitespace check: passed.

Validation loop count: two.

Repairs:

1. The initial isolated worktree did not include a `ruff` executable in the
   project environment; the same pinned checker was run through its isolated
   tool environment.
2. Ruff identified three mechanical annotation/import-order findings and later
   one formatting finding; all were corrected and the checks rerun cleanly.

## Safety and claim boundary

Confirmed:

- no provider call;
- no model download or inference;
- no runtime launch;
- no H100/GPU/CUDA/server execution;
- no semantic judging or human grading;
- no production validation;
- no measured speed, latency, throughput, memory peak, quality, cost, hardware
  superiority, or larger-than-VRAM result;
- no release, tag, publication, repository-setting change, issue, project-board
  change, collaborator change, or major file movement;
- no Krako Reach integration;
- runtime support declarations remain fixture-level planning inputs;
- the 8 GB physical NVIDIA benchmark remains deferred to H0-B after AI Festa.

## Review focus

1. Whether the declared FreeToken and KTransformers capability scope should
   remain fixture-level until their physical adapter validation.
2. Whether model architecture needs an explicit dense/MoE field before the
   NVIDIA priority becomes physical-demo policy.
3. Whether the five planning events are sufficient for the first animated
   Studio graph.
4. Whether planning evidence should gain detached signatures before the finals
   evidence package.

No merge is authorized by this report.
