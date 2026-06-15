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

These metrics are defined in [KRK routing benchmark methodology v0](krk-routing-benchmark-methodology-v0.md) and computed in the [KRK multi-profile routing evaluation v0](krk-multi-profile-routing-evaluation-v0.md).

Scope:

- dry-run matrix evaluation.
- not a production benchmark.
- no provider calls.
- no GPU execution.

| Profile | Requests | Exact route accuracy | Acceptable route rate | Unsafe misroute rate | Cache correctness | Safety fallback rate | Failure fallback rate | GPU false positives | GPU false negatives | Compute-weighted GPU demand |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mixed-realistic | 6 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.1667 | 0.0000 | 0 | 0 | 0.5217 |
| GPU-heavy | 4 | 1.0000 | 1.0000 | 0.0000 | N/A | 0.2500 | 0.0000 | 0 | 0 | 0.7059 |
| cache-heavy | 4 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0 | 0 | 0.5556 |
| adversarial | 4 | 0.7500 | 1.0000 | 0.0000 | N/A | 0.5000 | 0.0000 | 0 | 0 | 0.0000 |

Generated outputs:

- [mixed-realistic metrics](generated/krk-mixed-routing-metrics-v0.md)
- [GPU-heavy metrics](generated/krk-gpu-heavy-routing-metrics-v0.md)
- [cache-heavy metrics](generated/krk-cache-heavy-routing-metrics-v0.md)
- [adversarial metrics](generated/krk-adversarial-routing-metrics-v0.md)

## C. Runtime-Integrated Dry-Run Route Evaluation

The current public package includes a runtime-integrated dry-run route evaluation over the four public matrix profiles. It runs request, KRK route decision, route-specific dry-run executor, evidence record creation, route-selectivity scoring, and report generation.

Scope:

- dry-run executors only.
- no provider calls.
- no GPU execution.
- no H100 workload execution.
- no production traffic.

| Field | Value |
| --- | --- |
| Total requests | 18 |
| Route counts | deterministic 2, cache 3, CPU 2, provider 3, GPU 4, fallback 4 |
| Executor counts | deterministic 2, cache 3, CPU 2, provider 3, GPU 4, fallback 4 |
| Exact route accuracy | 0.9444 |
| Acceptable route rate | 1.0000 |
| Unsafe misroute rate | 0.0000 |
| Safety fallback rate | 0.2222 |
| Failure fallback rate | 0.0000 |
| Error count | 0 |
| Dry-run execution success rate | 1.0000 |
| Evidence records created | 18 |
| Claim level | `runtime_integrated_dry_run_route_selectivity_measured` |

Generated summaries:

- [KRK runtime-integrated route evaluation v0](krk-runtime-integrated-route-evaluation-v0.md)
- [Generated runtime-integrated route evaluation JSON summary](generated/krk-runtime-integrated-route-evaluation-v0.json)
- [Generated runtime-integrated route evaluation Markdown summary](generated/krk-runtime-integrated-route-evaluation-v0.md)

This evidence supports only a runtime-integrated dry-run route-selectivity statement. It must not be generalized into production readiness, provider execution, GPU execution, savings, or broad workload claims.

## D. GPU-Routed Subset Evidence

Source methodology:

- [KRK extended H100 test matrix v0](krk-extended-h100-test-matrix-v0.md)
- [KRK public evidence boundary v0](krk-public-evidence-boundary-v0.md)
- [KRK performance table schema v0](krk-performance-table-schema-v0.md)

| Field | Value |
| --- | --- |
| Methodology | Defined |
| Subset selection rule | Select only workload items that KRK routes to GPU-class execution during a bounded matrix run. |
| Subset count | 4 |
| Measurement status | Bounded H100 subset measured |
| Claim level | `bounded_h100_routed_subset_measured` |

Public-safe summary:

> KORA benchmarks when GPU-class compute should be used, not raw GPU usage.

## E. H100 Bounded Measurement

The current public package includes a sanitized bounded H100 measurement for the GPU-selected public matrix subset.

| Field | Value |
| --- | --- |
| Task count | 4 |
| Runtime | 0.035312 seconds |
| Throughput | 113.277481 requests/second |
| Compute-weight throughput | 1642.523477 compute weight/second |
| Memory | 240.000 MB bounded workload peak allocation |
| Claim level | `bounded_h100_routed_subset_measured` |

Generated summaries:

- [Generated H100 bounded JSON summary](generated/krk-h100-bounded-summary-v0.json)
- [Generated H100 bounded Markdown summary](generated/krk-h100-bounded-summary-v0.md)

This measurement is subset-bounded. It must not be generalized into raw H100 performance, production performance, infrastructure savings, customer savings, provider superiority, GPU superiority, or broad workload superiority.

## F. Provider-Routed Validation

The current public package includes a sanitized bounded commercial LLM API validation for the provider-selected public matrix subset.

| Field | Value |
| --- | --- |
| Sample count | 3 |
| Success count | 3 |
| Failure count | 0 |
| Latency min | 1581.517 ms |
| Latency median | 1583.670 ms |
| Latency max | 3635.988 ms |
| Input units/tokens total | 176 |
| Output units/tokens total | 156 |
| Claim level | `bounded_provider_path_measured` |

Generated summaries:

- [KRK provider-routed validation v0](krk-provider-routed-validation-v0.md)
- [Generated provider-routed validation JSON summary](generated/krk-provider-routed-validation-summary-v0.json)
- [Generated provider-routed validation Markdown summary](generated/krk-provider-routed-validation-summary-v0.md)

This validation is subset-bounded. It must not be generalized into production performance, provider cost reduction, customer savings, provider superiority, broad provider benchmark performance, or replacement of commercial LLM APIs.

## Claim Boundary

Supported:

- KRK/KORA-controlled execution has bounded deterministic-heavy benchmark evidence.
- The current alpha can produce reproducible evidence counters for the deterministic-heavy workload.
- The KRK extended matrix methodology defines how future route-selectivity metrics should be measured.
- KRK now has dry-run route-selectivity metrics over four public matrix profiles.
- KRK now has runtime-integrated dry-run route-selectivity evidence over the four public matrix profiles.
- KRK-selected GPU subset items from the public matrix fixtures were executed in a bounded H100 evaluation and summarized with runtime, throughput, and memory measurements.
- KRK-selected provider-path items from the public matrix fixtures completed a bounded commercial LLM API validation with sanitized latency and token/unit metadata.

Not supported:

- production cost reduction.
- customer savings.
- broad workload superiority.
- infrastructure savings.
- provider or router replacement claims.
