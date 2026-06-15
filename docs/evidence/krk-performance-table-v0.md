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

## F. Expanded H100 Bounded Measurement

Goal 055 prepared an expanded bounded H100 routed-subset evaluation, but it was not run because a safe CUDA/H100 runtime was not available in that goal's execution environment.

| Field | Value |
| --- | --- |
| Expanded evaluation status | not run |
| Subset count | 0 |
| Success count | 0 |
| Failure count | 0 |
| Runtime | N/A |
| Throughput | N/A |
| Memory | N/A |
| Claim level | `expanded_h100_validation_not_run` |

Generated summaries:

- [KRK expanded bounded H100 evaluation v0](krk-expanded-bounded-h100-evaluation-v0.md)
- [Generated expanded H100 bounded JSON summary](generated/krk-expanded-h100-bounded-summary-v0.json)
- [Generated expanded H100 bounded Markdown summary](generated/krk-expanded-h100-bounded-summary-v0.md)

This prepared expanded evaluation does not add measured H100 runtime, throughput, or memory evidence.

## G. Repo-Owned Bounded H100 Harness Measurement

Goal 058C added and ran a repo-owned bounded H100 harness against KRK-selected GPU fixture items. The harness emits structured `not_run` output when CUDA is unavailable and aggregate-only measured output when CUDA is available.

| Field | Value |
| --- | --- |
| Fixture count | 18 |
| GPU-routed fixture count | 4 |
| Operation count | 24 |
| Success count | 24 |
| Failure count | 0 |
| Runtime | 0.034976 seconds |
| Throughput | 686.176591 requests/second |
| Compute-weight throughput | 9949.560571 compute weight/second |
| Memory | 24.0 MB peak bounded allocation |
| CUDA device count | 2 |
| CUDA device class | H100-class GPU |
| Claim level | `bounded_h100_execution_measured` |

Generated summaries:

- [Goal 058C H100 bounded execution report](../reports/krk-goal058c-h100-bounded-execution-v0.md)
- [Generated Goal 058C H100 bounded JSON summary](generated/krk-goal058c-h100-bounded-execution-summary-v0.json)
- [Generated Goal 058C H100 bounded Markdown summary](generated/krk-goal058c-h100-bounded-execution-summary-v0.md)

This measurement is repo-harness-backed and fixture-bounded. It does not replace the historical Goal 055 `not_run` expanded evaluation result and must not be generalized into raw H100 performance, production performance, infrastructure savings, customer savings, GPU superiority, H100 superiority, or broad workload superiority.

## H. Provider-Routed Validation

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

## I. Expanded Provider-Routed Validation

The current public package also includes an expanded bounded commercial LLM API validation derived from provider-selected public matrix items.

| Field | Value |
| --- | --- |
| Sample count | 12 |
| Success count | 12 |
| Failure count | 0 |
| Latency min | 1418.283 ms |
| Latency median | 2601.086 ms |
| Latency p95 | 5888.007 ms |
| Latency max | 5888.007 ms |
| Input units/tokens total | 1102 |
| Output units/tokens total | 745 |
| Claim level | `expanded_bounded_provider_path_measured` |

Generated summaries:

- [KRK expanded provider-routed validation v0](krk-expanded-provider-routed-validation-v0.md)
- [Generated expanded provider-routed validation JSON summary](generated/krk-expanded-provider-routed-validation-summary-v0.json)
- [Generated expanded provider-routed validation Markdown summary](generated/krk-expanded-provider-routed-validation-summary-v0.md)

This expanded validation strengthens the provider-routed evidence package, but it remains bounded. It must not be generalized into production performance, provider cost reduction, customer savings, provider superiority, broad provider benchmark performance, or replacement of commercial LLM APIs.

## Claim Boundary

Supported:

- KRK/KORA-controlled execution has bounded deterministic-heavy benchmark evidence.
- The current alpha can produce reproducible evidence counters for the deterministic-heavy workload.
- The KRK extended matrix methodology defines how future route-selectivity metrics should be measured.
- KRK now has dry-run route-selectivity metrics over four public matrix profiles.
- KRK now has runtime-integrated dry-run route-selectivity evidence over the four public matrix profiles.
- KRK-selected GPU subset items from the public matrix fixtures were executed in a bounded H100 evaluation and summarized with runtime, throughput, and memory measurements.
- KRK has a prepared expanded H100 routed-subset evaluation slot, but it has not been measured.
- KRK now has repo-owned bounded H100 harness evidence for 24 fixture-derived GPU-routed operations, summarized with aggregate runtime, throughput, and memory metrics.
- KRK-selected provider-path items from the public matrix fixtures completed bounded and expanded bounded commercial LLM API validation with sanitized latency and token/unit metadata.

Not supported:

- production cost reduction.
- customer savings.
- broad workload superiority.
- infrastructure savings.
- provider or router replacement claims.
