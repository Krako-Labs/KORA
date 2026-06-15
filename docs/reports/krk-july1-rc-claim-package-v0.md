# KRK July 1 RC Claim Package v0

Status: allowed and prohibited claim package.

## Allowed Statements

These statements are allowed for the July 1 RC package when kept with the same bounded context:

- KRK is a deterministic-first routing kernel for AI workloads.
- KRK demonstrates route-selectivity on four public dry-run matrix profiles.
- KRK achieved 100% acceptable route rate and 0% unsafe misroute rate on the current public matrix profiles.
- KRK includes bounded H100-routed subset measurement.
- KRK includes bounded provider-routed validation.
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

### Bounded Provider-Routed Validation

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
- [KRK provider-routed validation v0](../evidence/krk-provider-routed-validation-v0.md)
- [KRK performance table v0](../evidence/krk-performance-table-v0.md)
- [KRK evidence package v0](../evidence/krk-evidence-package-v0.md)
