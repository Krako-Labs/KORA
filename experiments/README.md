# KORA Experiments

This directory holds benchmark workloads, generated results, and future experiment runners for KORA.

## Current Status

The benchmark surface is currently a skeleton. It defines the directory layout, an initial deterministic-heavy workload draft, a minimal dry-run runner, a simulated direct baseline mode, and a simulated KORA-controlled mode.

Current contents:

- `workloads/`: versioned workload definitions used by future runners.
- `results/`: generated benchmark outputs. This directory is intentionally kept empty except for `.gitkeep`.
- `generate_workload.py`: deterministic-heavy workload generator.
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

The first generated near-term workload is:

```text
experiments/workloads/deterministic_heavy_v1_100.json
```

It contains 100 deterministic-heavy tasks generated from seed `42`, with approximately 80 deterministic/no-model tasks and 20 fallback/model-candidate tasks.

## Workload Generator

The workload generator creates reproducible deterministic-heavy workload JSON from a fixed seed.

Example:

```bash
python3 experiments/generate_workload.py --count 100 --seed 42 --benchmark-name deterministic_heavy_v1 --output experiments/workloads/deterministic_heavy_v1_100.json
```

Generated workloads are reproducible from the same seed, count, and benchmark name. Generated tasks should still be reviewed for category balance, expected outputs, and fallback-candidate clarity before benchmark claims are made.

## Dry-Run Runner

The runner supports `dry-run` mode for workload shape validation. It loads a workload, validates that it contains a task list, counts tasks by category, counts `requires_model` values, and writes a result JSON artifact.

Example:

```bash
python3 experiments/run_benchmark.py --mode dry-run --workload experiments/workloads/deterministic_heavy_v0.json --output experiments/results/deterministic_heavy_v0.dry_run.json
```

This is not yet a direct baseline versus KORA-controlled comparison. It is only the first executable skeleton for validating workload shape and result artifact structure.

## Direct Baseline Runner

The runner also supports `direct-baseline` mode. This mode simulates a naive baseline where every task is counted as one model invocation. It does not call a real model, use external APIs, or measure actual API cost.

Example:

```bash
python3 experiments/run_benchmark.py --mode direct-baseline --workload experiments/workloads/deterministic_heavy_v0.json --output experiments/results/deterministic_heavy_v0.direct_baseline.json
```

This gives the benchmark a baseline model-invocation count to compare against the simulated KORA-controlled mode.

## KORA-Controlled Runner

The runner also supports `kora-controlled` mode. This mode simulates deterministic-first KORA execution using workload metadata:

- tasks with `requires_model: false` are counted as deterministic resolutions
- tasks with `requires_model: true` are counted as fallback/model-invocation candidates

Example:

```bash
python3 experiments/run_benchmark.py --mode kora-controlled --workload experiments/workloads/deterministic_heavy_v0.json --output experiments/results/deterministic_heavy_v0.kora_controlled.json
```

For the current deterministic-heavy workload, the simulated comparison is:

- direct-baseline simulated model invocations: 20
- kora-controlled simulated model invocations: 4
- avoided model invocations: 16
- avoided invocation rate: 80%

This is not production cost reduction, not a real API measurement, and not full KORA runtime integration.

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
