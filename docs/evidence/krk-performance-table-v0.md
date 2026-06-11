# KRK Performance Table v0

Status: current public evidence package.

This table package summarizes what the current KRK-oriented alpha evidence supports. It uses existing public repository evidence only. Missing values are marked explicitly rather than inferred.

## Scope

KRK means KORA Routing Kernel: a deterministic-first execution routing kernel that routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

This package is not a production performance claim. It is a structured evidence table for the current alpha.

## A. Deterministic-Heavy Benchmark

Source:

- [Benchmark result summary](../benchmarks/kora_benchmark_result_v1_100.md)
- [Runtime evidence reviewer guide](../reports/v0.3.0-alpha-runtime-evidence-reviewer-guide.md)

| Field | Value |
| --- | ---: |
| Workload | `experiments/workloads/deterministic_heavy_v1_100.json` |
| Total tasks | 100 |
| Deterministic tasks | 80 |
| Fallback/model-candidate tasks | 20 |
| Direct baseline model invocations | 100 |
| KRK/KORA-controlled model invocations | 20 |
| Avoided invocations | 80 |
| Avoided invocation rate | 80% |
| Deterministic mismatches | 0 |

Bounded interpretation:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

This benchmark is deterministic-heavy and simulated. It does not measure production execution or external model billing.

## B. KRK Routing Metrics

These metrics are defined in [KRK routing benchmark methodology v0](krk-routing-benchmark-methodology-v0.md). They have not yet been measured against the KRK extended matrix fixtures.

| Metric | Status |
| --- | --- |
| `exact_route_accuracy` | NOT MEASURED YET |
| `acceptable_route_rate` | NOT MEASURED YET |
| `unsafe_misroute_rate` | NOT MEASURED YET |
| `cache_hit_correctness_rate` | NOT MEASURED YET |
| `safety_fallback_rate` | NOT MEASURED YET |
| `failure_fallback_rate` | NOT MEASURED YET |
| `gpu_false_positive_count` | NOT MEASURED YET |
| `gpu_false_negative_count` | NOT MEASURED YET |
| `compute_weighted_gpu_demand` | NOT MEASURED YET |

Next requirement: connect the KRK matrix fixtures to a dry-run evaluator that keeps router-visible metadata separate from oracle labels.

## C. GPU-Routed Subset Evidence

Source methodology:

- [KRK extended H100 test matrix v0](krk-extended-h100-test-matrix-v0.md)
- [KRK public evidence boundary v0](krk-public-evidence-boundary-v0.md)
- [KRK performance table schema v0](krk-performance-table-schema-v0.md)

| Field | Value |
| --- | --- |
| Methodology | Defined |
| Subset selection rule | Select only workload items that KRK routes to GPU-class execution during a bounded matrix run. |
| Subset count | NOT MEASURED YET |
| Measurement status | NOT MEASURED YET |
| Claim level | Methodology defined only |

Public-safe summary:

> KORA benchmarks when GPU-class compute should be used, not raw GPU usage.

## D. H100 Bounded Measurement

The current public package does not include public-safe measured task count, runtime, throughput, or memory values for a KRK H100 bounded measurement.

| Field | Value |
| --- | --- |
| Task count | NOT INCLUDED IN CURRENT PUBLIC PACKAGE |
| Runtime | NOT INCLUDED IN CURRENT PUBLIC PACKAGE |
| Throughput | NOT INCLUDED IN CURRENT PUBLIC PACKAGE |
| Memory | NOT INCLUDED IN CURRENT PUBLIC PACKAGE |
| Claim level | NOT INCLUDED IN CURRENT PUBLIC PACKAGE |

Any future bounded measurement must include sanitized reproducibility metadata and must not publish raw logs, private resource identifiers, credentials, or local-only environment details.

## Claim Boundary

Supported:

- KRK/KORA-controlled execution has bounded deterministic-heavy benchmark evidence.
- The current alpha can produce reproducible evidence counters for the deterministic-heavy workload.
- The KRK extended matrix methodology defines how future route-selectivity metrics should be measured.

Not supported:

- production cost reduction.
- customer savings.
- broad workload superiority.
- infrastructure savings.
- provider or router replacement claims.
