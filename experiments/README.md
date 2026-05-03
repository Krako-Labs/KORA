# KORA Experiments

This directory holds benchmark workloads, generated results, and future experiment runners for KORA.

## Current Status

The benchmark surface is currently a skeleton. It defines the directory layout, an initial deterministic-heavy workload draft, and a minimal dry-run runner, but it does not include direct baseline or KORA-controlled execution yet.

Current contents:

- `workloads/`: versioned workload definitions used by future runners.
- `results/`: generated benchmark outputs. This directory is intentionally kept empty except for `.gitkeep`.
- `run_benchmark.py`: minimal benchmark runner skeleton.

## Deterministic-Heavy Workloads

A deterministic-heavy workload is a collection of tasks where most cases should be resolved by structured logic, validation, routing, cache lookup, or schema checks before any model call is considered.

These workloads are designed to measure whether KORA can avoid unnecessary model invocations while preserving explicit validation and telemetry. They include:

- tasks that should not require model calls
- tasks that may require fallback in later benchmark versions
- tasks that make direct model invocation look wasteful when deterministic handling is sufficient

The first workload draft is:

```text
experiments/workloads/deterministic_heavy_v0.json
```

## Dry-Run Runner

The current runner supports only `dry-run` mode. It loads a workload, validates that it contains a task list, counts tasks by category, counts `requires_model` values, and writes a result JSON artifact.

Example:

```bash
python3 experiments/run_benchmark.py --mode dry-run --workload experiments/workloads/deterministic_heavy_v0.json --output experiments/results/deterministic_heavy_v0.dry_run.json
```

This is not yet a direct baseline versus KORA-controlled comparison. It is only the first executable skeleton for validating workload shape and result artifact structure.

## Future Runner

The expected future runner will compare two execution paths over the same workload:

- direct baseline: treat each task as if it may be sent directly to a model
- KORA-controlled execution: run deterministic, validation, routing, cache, retry, and fallback paths according to KORA semantics

The initial runner should emit structured JSON results that can later be summarized into technical preview tables. Expected metrics include:

- total task count
- model invocation count
- deterministic resolution count
- fallback count
- verifier pass/fail count
- runtime summary
- output correctness against expected results where applicable

## Limitations

This directory is not yet a paper-grade benchmark suite. The current workload is intentionally small, manually written, and intended to harden the shape of the benchmark before scaling to hundreds of cases.

The current workload does not prove production cost reduction, broad performance superiority, or energy reduction. It supports the next step: building a reproducible direct-baseline versus KORA-controlled comparison.

## Technical Preview Path

This skeleton supports the future `v0.3.0-alpha` technical preview by creating a stable place for workloads and result artifacts. Once the runner exists, generated results should be committed only when they are reproducible and tied to documented commands.
