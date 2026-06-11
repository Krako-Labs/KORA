# KRK Evidence Package v0

Status: current public evidence package.

This package explains what evidence exists for the KRK-oriented alpha and what remains methodology or roadmap.

## What KRK Is

KRK means KORA Routing Kernel. It is the deterministic-first routing kernel inside KORA Core. KRK routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

## What Evidence Currently Exists

### Deterministic Benchmark Evidence

The current bounded benchmark evidence is the deterministic-heavy 100-task workload:

- workload: `experiments/workloads/deterministic_heavy_v1_100.json`.
- total tasks: 100.
- deterministic/no-model tasks: 80.
- fallback/model-candidate tasks: 20.
- direct-baseline simulated model invocations: 100.
- KRK/KORA-controlled simulated model invocations: 20.
- avoided simulated model invocations: 80.
- deterministic mismatches: 0.

Primary references:

- [Benchmark result summary](../benchmarks/kora_benchmark_result_v1_100.md)
- [Runtime evidence reviewer guide](../reports/v0.3.0-alpha-runtime-evidence-reviewer-guide.md)

### Routing Methodology

KRK routing methodology defines:

- independent oracle labels.
- router-visible metadata.
- baseline policies.
- route accuracy metrics.
- fallback classification.
- compute-weight formula versioning.

Reference:

- [KRK routing benchmark methodology v0](krk-routing-benchmark-methodology-v0.md)

### Benchmark Methodology

The current benchmark path supports deterministic-heavy alpha evidence and a future KRK matrix evaluator. The existing deterministic benchmark is already reproducible. The extended matrix runner is not implemented yet.

References:

- [KRK extended H100 test matrix v0](krk-extended-h100-test-matrix-v0.md)
- [KRK performance table schema v0](krk-performance-table-schema-v0.md)

### GPU Subset Methodology

The GPU-routed subset methodology is defined as a measurement plan. It evaluates whether KRK selects GPU-class compute only for workload items where it is justified by visible metadata and policy.

This is methodology, not a completed measurement.

Reference:

- [KRK public evidence boundary v0](krk-public-evidence-boundary-v0.md)

### Bounded GPU Measurement

Bounded GPU measurement is not included in the current public package. No public task count, runtime, throughput, or memory table is included for this package.

Future measurement should report sanitized subset summaries only after the route matrix evaluator and artifact policy are ready.

### Reproducibility Path

Current reproducible path:

```bash
python3 -m pytest
python3 -m kora run runtime_integrated_benchmark -- --offline
```

The runtime evidence reviewer guide contains the current expected counters and optional generated evidence commands.

## What Is Evidence

Evidence in this package means:

- committed workloads.
- reproducible commands.
- expected counters documented in public files.
- explicit claim boundaries.
- methodology docs that define future measurements before they are run.

## What Is Not Evidence

This package does not treat the following as evidence:

- uncommitted generated outputs.
- private or local-only raw artifacts.
- broad extrapolations from deterministic-heavy workloads.
- production deployment assumptions.
- unsupported savings or infrastructure claims.

## Current Status

The current evidence package is ready for public review as a July 1 status package. It should be extended next with a dry-run KRK matrix evaluator and a generated performance table.
