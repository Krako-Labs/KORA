# KRK July 1 Evidence Summary v0

Status: current status package.

This summary describes the KRK-oriented alpha as it stands in the public repository. It is a status package, not marketing copy.

## What KRK Is

KRK means KORA Routing Kernel. It is the deterministic-first routing kernel inside KORA Core.

KRK routes workload tasks across execution paths:

- deterministic.
- cache.
- CPU.
- provider.
- GPU.
- fallback.

## What Has Been Implemented

The current public alpha includes:

- an example-oriented KORA CLI with `examples`, `run`, `studio`, and `telemetry` commands.
- deterministic-heavy benchmark evidence.
- runtime evidence reviewer documentation.
- KRK architecture and quickstart docs.
- KRK extended matrix methodology and small fixture workloads.
- KRK public evidence boundary docs.
- KRK performance table schema and current performance table package.

The standalone KRK commands `route`, `explain`, `benchmark`, and `report` are alpha primitives and documentation surfaces. They are not exposed as top-level CLI commands on the current base.

## Evidence Generated

Current deterministic-heavy evidence:

| Metric | Value |
| --- | ---: |
| Total tasks | 100 |
| Deterministic/no-model tasks | 80 |
| Fallback/model-candidate tasks | 20 |
| Direct-baseline simulated model invocations | 100 |
| KRK/KORA-controlled simulated model invocations | 20 |
| Avoided simulated model invocations | 80 |
| Deterministic mismatches | 0 |

Approved bounded interpretation:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

## Benchmark Methodology

The current methodology separates:

- router-visible metadata.
- oracle-only labels.
- baseline policies.
- route correctness metrics.
- fallback classification.
- compute-weight formula versioning.

This supports the next dry-run KRK matrix evaluator.

## Current Limitations

- Extended KRK matrix fixtures are not yet connected to an evaluator.
- Route accuracy, acceptable route rate, unsafe misroute rate, cache correctness, and fallback rates are not measured yet.
- GPU-routed subset measurement is methodology-only.
- Bounded H100 task count, runtime, throughput, and memory values are not included in the current public package.
- Current benchmark evidence is deterministic-heavy and simulated.
- The current package does not support production savings, customer savings, infrastructure savings, broad workload superiority, or provider replacement claims.

## Next Steps Before July 1

1. Add a dry-run evaluator for the KRK matrix fixtures.
2. Generate route distribution and correctness tables from the matrix.
3. Produce a public-safe performance table artifact from structured results.
4. Define a bounded GPU-routed subset measurement command.
5. Keep all public claims tied to measured and reproducible artifacts.

## Related Docs

- [KRK performance table v0](../evidence/krk-performance-table-v0.md)
- [KRK evidence package v0](../evidence/krk-evidence-package-v0.md)
- [KRK reproducibility matrix v0](../evidence/krk-reproducibility-matrix-v0.md)
- [KRK claim boundary table v0](../evidence/krk-claim-boundary-table-v0.md)
- [KRK capability matrix v0](../evidence/krk-capability-matrix-v0.md)
