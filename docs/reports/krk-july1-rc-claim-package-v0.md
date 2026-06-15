# KRK July 1 RC Claim Package v0

Status: allowed and prohibited claim package.

## Allowed Statements

These statements are allowed for the July 1 RC package when kept with the same bounded context:

- KRK is a deterministic-first routing kernel for AI workloads.
- KRK demonstrates route-selectivity on four public dry-run matrix profiles.
- KRK achieved 100% acceptable route rate and 0% unsafe misroute rate on the current public matrix profiles.
- KRK includes runtime-integrated dry-run route-selectivity evaluation.
- KRK includes bounded H100-routed subset measurement from Goal 050.
- KRK includes repo-owned bounded H100 harness measurement from Goal 058C.
- KRK includes expanded bounded provider-routed validation from Goal 054.
- KRK prepared expanded bounded H100 routed-subset evaluation in Goal 055, but it was not run because safe CUDA/H100 runtime was unavailable in that goal.
- KRK provides public-safe reproducible evidence for execution-path routing.
- KRK routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

## Exact Evidence Numbers

### Route-Selectivity

| Profile | Requests | Exact route accuracy | Acceptable route rate | Unsafe misroute rate |
| --- | ---: | ---: | ---: | ---: |
| mixed-realistic | 6 | 1.0000 | 1.0000 | 0.0000 |
| GPU-heavy | 4 | 1.0000 | 1.0000 | 0.0000 |
| cache-heavy | 4 | 1.0000 | 1.0000 | 0.0000 |
| adversarial | 4 | 0.7500 | 1.0000 | 0.0000 |

### Bounded H100-Routed Subset

| Metric | Value |
| --- | ---: |
| Subset count | 4 |
| Total compute weight | 58 |
| Runtime seconds | 0.035312 |
| Throughput, requests/second | 113.277481 |
| Throughput, compute weight/second | 1642.523477 |
| Bounded workload peak allocation MB | 240.000 |

### Repo-Owned Bounded H100 Harness

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

### Runtime-Integrated Dry-Run Route Evaluation

| Metric | Value |
| --- | ---: |
| Total requests | 18 |
| Exact route accuracy | 0.9444 |
| Acceptable route rate | 1.0000 |
| Unsafe misroute rate | 0.0000 |
| Dry-run execution success rate | 1.0000 |
| Evidence records created | 18 |
| Error count | 0 |

### Initial Bounded Provider-Routed Validation

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

### Expanded Bounded Provider-Routed Validation

| Metric | Value |
| --- | ---: |
| Sample count | 12 |
| Success count | 12 |
| Failure count | 0 |
| Latency min, ms | 1418.283 |
| Latency median, ms | 2601.086 |
| Latency p95, ms | 5888.007 |
| Latency max, ms | 5888.007 |
| Input units/tokens total | 1102 |
| Output units/tokens total | 745 |

### Expanded H100 Evaluation Status

| Metric | Value |
| --- | --- |
| Expanded evaluation run | no |
| Subset count | 0 |
| Success count | 0 |
| Failure count | 0 |
| Claim level | `expanded_h100_validation_not_run` |

## Prohibited Statements

These statements are not supported by the July 1 RC package:

- production cost reduction.
- 10x savings.
- customer savings.
- infrastructure savings.
- H100 superiority.
- provider superiority.
- broad workload superiority.
- replacement of existing model serving/provider routing systems.
- production readiness.
- provider cost reduction.
- broad provider benchmark superiority.

## Evidence Sources

- [KRK route-selectivity results v0](../evidence/krk-route-selectivity-results-v0.md)
- [KRK multi-profile routing evaluation v0](../evidence/krk-multi-profile-routing-evaluation-v0.md)
- [KRK bounded H100 evaluation v0](../evidence/krk-bounded-h100-evaluation-v0.md)
- [Goal 058C H100 bounded execution report](krk-goal058c-h100-bounded-execution-v0.md)
- [Generated Goal 058C H100 bounded execution JSON summary](../evidence/generated/krk-goal058c-h100-bounded-execution-summary-v0.json)
- [KRK expanded bounded H100 evaluation v0](../evidence/krk-expanded-bounded-h100-evaluation-v0.md)
- [KRK provider-routed validation v0](../evidence/krk-provider-routed-validation-v0.md)
- [KRK expanded provider-routed validation v0](../evidence/krk-expanded-provider-routed-validation-v0.md)
- [KRK runtime-integrated route evaluation v0](../evidence/krk-runtime-integrated-route-evaluation-v0.md)
- [KRK performance table v0](../evidence/krk-performance-table-v0.md)
- [KRK evidence package v0](../evidence/krk-evidence-package-v0.md)
