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
- [Goal 058C H100 bounded execution report](../reports/krk-goal058c-h100-bounded-execution-v0.md)

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

### Repo-Owned Bounded H100 Harness Measurement

Goal 058C added a reusable repo-owned bounded H100 harness and measured a 24-operation fixture-derived H100-class run. The harness safely emits structured `not_run` output in no-CUDA environments and runs bounded CUDA tensor work only when CUDA is available.

| Metric | Value |
| --- | ---: |
| Fixture count | 18 |
| GPU-routed fixture count | 4 |
| Operation count | 24 |
| Success count | 24 |
| Failure count | 0 |
| Runtime seconds | 0.034976 |
| Throughput, requests/second | 686.176591 |
| Throughput, compute weight/second | 9949.560571 |
| Peak bounded allocation MB | 24.0 |
| CUDA device count | 2 |

Generated summaries:

- [Goal 058C H100 bounded execution report](../reports/krk-goal058c-h100-bounded-execution-v0.md)
- [Generated Goal 058C H100 bounded JSON summary](generated/krk-goal058c-h100-bounded-execution-summary-v0.json)
- [Generated Goal 058C H100 bounded Markdown summary](generated/krk-goal058c-h100-bounded-execution-summary-v0.md)

This supersedes the prior repo-harness execution blocker for basic bounded H100 execution. It does not replace the historical Goal 055 `not_run` expanded evaluation result, and it does not support broad H100 performance, production performance, infrastructure savings, customer savings, GPU superiority, H100 superiority, or broad workload superiority claims.

### Expanded H100 Representativeness Measurement

Goal 059 measured a bounded multi-profile H100 representativeness run using the repo-owned harness and public fixture-derived GPU-routed workload items.

| Metric | Value |
| --- | ---: |
| Fixture count | 18 |
| GPU-routed fixture count | 4 |
| Operation count | 100 |
| Success count | 100 |
| Failure count | 0 |
| Runtime seconds | 0.054051 |
| Throughput, requests/second | 1850.090914 |
| Throughput, compute weight/second | 26826.318247 |
| Peak bounded allocation MB | 24.0 |
| CUDA device count | 2 |

Generated summaries:

- [Goal 059 expanded H100 representativeness report](../reports/krk-goal059-expanded-h100-representativeness-v0.md)
- [Generated Goal 059 expanded H100 JSON summary](generated/krk-goal059-expanded-h100-representativeness-summary-v0.json)
- [Generated Goal 059 expanded H100 Markdown summary](generated/krk-goal059-expanded-h100-representativeness-summary-v0.md)

This moves the H100 evidence state from basic bounded repo-owned harness execution to bounded multi-profile H100 representativeness over public fixture-derived GPU-routed operations. It does not support production performance, infrastructure savings, customer savings, GPU superiority, H100 superiority, or broad workload superiority claims.

### Goal 099 Controlled AI Champion H100 Server Run

Goal 099 executed the Goal 098 server-run packet through SSH remote execution on the AI Champion H100 server and recorded aggregate public-safe CPU/non-GPU and bounded H100 summaries.

CPU/non-GPU evidence:

- [Goal 099 CPU/non-GPU AI Champion summary](generated/goal099_cpu_nongpu_ai_champion_summary.md)
- phase status: `measured_cpu_nongpu_remote`
- GPU visibility setting: `CUDA_VISIBLE_DEVICES=""`
- provider calls actually made: `0`

Bounded H100 evidence:

| Metric | Value |
| --- | ---: |
| Operation count | 24 |
| Success count | 24 |
| Failure count | 0 |

Generated summaries:

- [Goal 099 AI Champion H100 server run report](../reports/goal099_ai_champion_h100_server_run.md)
- [Goal 099 CPU/non-GPU AI Champion summary](generated/goal099_cpu_nongpu_ai_champion_summary.md)
- [Goal 099 H100 AI Champion summary](generated/goal099_h100_ai_champion_summary.md)

The environment reported 2 H100-class devices visible, but this does not establish both-GPU active use or multi-GPU scaling. This evidence is controlled workload-path evidence over public fixtures. It does not support H100 superiority, GPU superiority, CPU superiority, production readiness, production benchmark proof, production cost reduction proof, real API-cost proof, real GPU-cost proof, energy reduction, customer savings, provider replacement, general GPU-serving replacement, or broad workload superiority claims.

### Expanded Bounded GPU Measurement

An expanded bounded H100 routed-subset evaluation was prepared for Goal 055, but it was not run because a safe CUDA/H100 runtime was not available in that goal's execution environment.

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

The Goal 055 expanded attempt remains documented as a prepared but not measured historical evidence slot. Goal 058C now adds measured repo-owned bounded harness evidence, but broader expanded H100 representativeness remains open.

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

### Baseline Equivalence and Output Fidelity

Goal 060 adds a deterministic, reviewer-facing baseline-equivalence and output-fidelity evaluator over the four public matrix profiles. The evaluator compares public fixture-derived baseline output contracts with KRK-routed output contracts. It uses deterministic rule-based comparison only and does not call providers, use GPU execution, inspect private logs, or use a semantic model judge.

| Metric | Value |
| --- | ---: |
| Total evaluated items | 18 |
| Baseline success count | 18 |
| KRK success count | 18 |
| Exact match count | 17 |
| Structured equivalent count | 1 |
| Semantic equivalent count | 0 |
| Degraded count | 0 |
| Failed count | 0 |
| Exact match rate | 0.9444 |
| Acceptable output rate | 1.0000 |
| Degradation rate | 0.0000 |
| Failure rate | 0.0000 |

Generated summaries:

- [Goal 060 baseline equivalence and output fidelity report](../reports/krk-goal060-baseline-equivalence-output-fidelity-v0.md)
- [Generated Goal 060 output fidelity JSON summary](generated/krk-goal060-output-fidelity-summary-v0.json)
- [Generated Goal 060 output fidelity Markdown summary](generated/krk-goal060-output-fidelity-summary-v0.md)

This supports a public fixture-derived output-fidelity statement only. It does not support semantic-model-judge validation, production output quality, production readiness, production cost reduction, customer savings, energy reduction, real API/GPU cost reduction, provider superiority, H100 superiority, or broad workload superiority claims.

### Reproducibility Path

Current reproducible local paths:

```bash
python3 -m pytest
python3 -m kora run runtime_integrated_benchmark -- --offline
python3 -m kora.runtime_route_evaluator --matrix examples/workloads/krk-mixed-routing-matrix-alpha.json --matrix examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json --matrix examples/workloads/krk-cache-heavy-routing-matrix-alpha.json --matrix examples/workloads/krk-adversarial-routing-matrix-alpha.json --json-out docs/evidence/generated/krk-runtime-integrated-route-evaluation-v0.json --md-out docs/evidence/generated/krk-runtime-integrated-route-evaluation-v0.md
python3 scripts/run_krk_h100_bounded.py --matrix examples/workloads/krk-mixed-routing-matrix-alpha.json --matrix examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json --matrix examples/workloads/krk-cache-heavy-routing-matrix-alpha.json --matrix examples/workloads/krk-adversarial-routing-matrix-alpha.json --target-count 24 --json-out /tmp/krk-h100-bounded.json --md-out /tmp/krk-h100-bounded.md
python3 scripts/run_krk_output_fidelity.py --matrix examples/workloads/krk-mixed-routing-matrix-alpha.json --matrix examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json --matrix examples/workloads/krk-cache-heavy-routing-matrix-alpha.json --matrix examples/workloads/krk-adversarial-routing-matrix-alpha.json --json-out docs/evidence/generated/krk-goal060-output-fidelity-summary-v0.json --md-out docs/evidence/generated/krk-goal060-output-fidelity-summary-v0.md
```

The runtime evidence reviewer guide contains the current expected counters and optional generated evidence commands. The bounded H100 harness is safe to run in no-CUDA environments, where it emits structured `not_run` output. Measured H100 summaries are reproducible only in a CUDA/H100-capable environment and should be regenerated through a controlled evidence task, not by committing raw logs.

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

The current evidence package is ready for public review as a July 1 status package. It includes deterministic-heavy benchmark evidence, generated dry-run route-selectivity metrics for the four KRK matrix profiles, runtime-integrated dry-run route-selectivity evidence, bounded H100 subset measurement for the GPU-selected public fixture items, repo-owned bounded H100 harness measurement from Goal 058C, expanded bounded H100 representativeness evidence from Goal 059, Goal 099 controlled server-run evidence over public CPU/non-GPU and bounded H100 workload paths, a historical prepared-but-not-measured expanded H100 evaluation slot from Goal 055, expanded bounded provider-path validation for the provider-selected public fixture items, and deterministic public fixture-derived output-fidelity evidence from Goal 060. It should be extended next with broader workload coverage, live semantic or human-graded output-quality validation, and larger GPU samples when public-safe.
