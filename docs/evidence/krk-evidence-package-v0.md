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

The current benchmark path supports deterministic-heavy alpha evidence and a dry-run KRK matrix evaluator. The existing deterministic benchmark is reproducible, and the four public matrix fixtures now have generated route-selectivity metrics.

References:

- [KRK extended H100 test matrix v0](krk-extended-h100-test-matrix-v0.md)
- [KRK performance table schema v0](krk-performance-table-schema-v0.md)
- [KRK multi-profile routing evaluation v0](krk-multi-profile-routing-evaluation-v0.md)
- [KRK route-selectivity results v0](krk-route-selectivity-results-v0.md)

### Route-Selectivity Metrics

KRK now has dry-run route-selectivity metrics for four public alpha matrix profiles:

| Profile | Requests | Exact route accuracy | Acceptable route rate | Unsafe misroute rate |
| --- | ---: | ---: | ---: | ---: |
| mixed-realistic | 6 | 1.0000 | 1.0000 | 0.0000 |
| GPU-heavy | 4 | 1.0000 | 1.0000 | 0.0000 |
| cache-heavy | 4 | 1.0000 | 1.0000 | 0.0000 |
| adversarial | 4 | 0.7500 | 1.0000 | 0.0000 |

These metrics evaluate selected routes against oracle labels without GPU execution or provider calls. They are benchmark-methodology evidence, not production evidence.

### Runtime-Integrated Dry-Run Route Evaluation

KRK now has runtime-integrated dry-run route-selectivity evidence over the four public matrix profiles. The workflow path is:

request -> KRK route decision -> route-specific dry-run executor -> evidence record -> route-selectivity scoring -> report.

| Metric | Value |
| --- | ---: |
| Total requests | 18 |
| Exact route accuracy | 0.9444 |
| Acceptable route rate | 1.0000 |
| Unsafe misroute rate | 0.0000 |
| Dry-run execution success rate | 1.0000 |
| Evidence records created | 18 |
| Error count | 0 |

Generated evidence:

- [KRK runtime-integrated route evaluation v0](krk-runtime-integrated-route-evaluation-v0.md)
- [Generated runtime-integrated route evaluation JSON](generated/krk-runtime-integrated-route-evaluation-v0.json)
- [Generated runtime-integrated route evaluation Markdown](generated/krk-runtime-integrated-route-evaluation-v0.md)

This evidence is runtime-integrated only in the dry-run sense. It does not call providers, use GPU hardware, run H100 workloads, execute production traffic, or validate task output quality.

### GPU Subset Methodology

The GPU-routed subset methodology is defined as a measurement plan. It evaluates whether KRK selects GPU-class compute only for workload items where it is justified by visible metadata and policy.

The public matrix path now includes a bounded H100 subset measurement for the GPU-selected fixture items.

Reference:

- [KRK public evidence boundary v0](krk-public-evidence-boundary-v0.md)
- [KRK bounded H100 evaluation v0](krk-bounded-h100-evaluation-v0.md)

### Bounded GPU Measurement

Bounded GPU measurement is included for the small public matrix GPU subset:

| Metric | Value |
| --- | ---: |
| Subset count | 4 |
| Runtime seconds | 0.035312 |
| Throughput, requests/second | 113.277481 |
| Throughput, compute weight/second | 1642.523477 |
| Bounded workload peak allocation MB | 240.000 |

Generated summaries:

- [Generated H100 bounded JSON summary](generated/krk-h100-bounded-summary-v0.json)
- [Generated H100 bounded Markdown summary](generated/krk-h100-bounded-summary-v0.md)

This is a bounded H100 routed-subset measurement. It is not a production benchmark, provider benchmark, raw GPU benchmark, or broad workload superiority claim.

### Expanded Bounded GPU Measurement

An expanded bounded H100 routed-subset evaluation was prepared for Goal 055, but it was not run because a safe CUDA/H100 runtime was not available in the current execution environment.

| Metric | Value |
| --- | --- |
| Expanded evaluation status | not run |
| Subset count | 0 |
| Success count | 0 |
| Failure count | 0 |
| Claim level | `expanded_h100_validation_not_run` |
| Raw logs committed | false |
| Private infrastructure details committed | false |

Generated summaries:

- [KRK expanded bounded H100 evaluation v0](krk-expanded-bounded-h100-evaluation-v0.md)
- [Generated expanded H100 bounded JSON summary](generated/krk-expanded-h100-bounded-summary-v0.json)
- [Generated expanded H100 bounded Markdown summary](generated/krk-expanded-h100-bounded-summary-v0.md)

The existing 4-item bounded H100 subset remains the current measured H100 evidence. The expanded attempt is documented as a prepared but not measured evidence slot.

### Provider-Routed Validation

KRK now includes bounded and expanded bounded provider-path validation for provider-selected public matrix items.

| Metric | Value |
| --- | ---: |
| Initial sample count | 3 |
| Initial success count | 3 |
| Initial failure count | 0 |
| Expanded sample count | 12 |
| Expanded success count | 12 |
| Expanded failure count | 0 |
| Expanded latency min, ms | 1418.283 |
| Expanded latency median, ms | 2601.086 |
| Expanded latency p95, ms | 5888.007 |
| Expanded latency max, ms | 5888.007 |
| Expanded input units/tokens total | 1102 |
| Expanded output units/tokens total | 745 |

Initial validation:

| Metric | Value |
| --- | ---: |
| Sample count | 3 |
| Success count | 3 |
| Failure count | 0 |
| Latency min, ms | 1581.517 |
| Latency median, ms | 1583.670 |
| Latency max, ms | 3635.988 |
| Input units/tokens total | 176 |
| Output units/tokens total | 156 |

Generated summaries:

- [KRK provider-routed validation v0](krk-provider-routed-validation-v0.md)
- [KRK expanded provider-routed validation v0](krk-expanded-provider-routed-validation-v0.md)
- [Generated provider-routed validation JSON summary](generated/krk-provider-routed-validation-summary-v0.json)
- [Generated provider-routed validation Markdown summary](generated/krk-provider-routed-validation-summary-v0.md)
- [Generated expanded provider-routed validation JSON summary](generated/krk-expanded-provider-routed-validation-summary-v0.json)
- [Generated expanded provider-routed validation Markdown summary](generated/krk-expanded-provider-routed-validation-summary-v0.md)

This is bounded commercial LLM API path validation. It is not a production benchmark, provider benchmark, provider-cost benchmark, provider superiority claim, broad commercial LLM benchmark, or replacement claim.

### Reproducibility Path

Current reproducible local paths:

```bash
python3 -m pytest
python3 -m kora run runtime_integrated_benchmark -- --offline
python3 -m kora.runtime_route_evaluator --matrix examples/workloads/krk-mixed-routing-matrix-alpha.json --matrix examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json --matrix examples/workloads/krk-cache-heavy-routing-matrix-alpha.json --matrix examples/workloads/krk-adversarial-routing-matrix-alpha.json --json-out docs/evidence/generated/krk-runtime-integrated-route-evaluation-v0.json --md-out docs/evidence/generated/krk-runtime-integrated-route-evaluation-v0.md
```

The runtime evidence reviewer guide contains the current expected counters and optional generated evidence commands. The bounded H100 subset summary is reproducible only in an H100-capable environment and should be regenerated through a controlled evidence task, not by committing raw logs.

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

The current evidence package is ready for public review as a July 1 status package. It includes deterministic-heavy benchmark evidence, generated dry-run route-selectivity metrics for the four KRK matrix profiles, runtime-integrated dry-run route-selectivity evidence, a bounded H100 subset measurement for the GPU-selected public fixture items, a prepared-but-not-measured expanded H100 evaluation slot, and expanded bounded provider-path validation for the provider-selected public fixture items. It should be extended next with broader workload coverage, output-quality validation, and larger GPU samples when public-safe.
