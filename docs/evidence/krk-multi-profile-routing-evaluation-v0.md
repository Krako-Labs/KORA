# KRK Multi-Profile Routing Evaluation v0

Status: generated dry-run route-selectivity evidence.

## Purpose

This document summarizes KRK route-selectivity results across four public matrix profiles. It turns the KRK matrix fixtures into public-safe evidence by comparing dry-run route decisions against independent oracle labels.

KRK means KORA Routing Kernel: a deterministic-first execution routing kernel for routing workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

## Methodology

The evaluator loads each committed matrix fixture, passes only `router_visible_metadata` into the dry-run KRK policy, and then compares the selected route against `oracle_labels`.

The router does not receive `oracle_labels`. Oracle labels are used only after routing to compute route-selectivity metrics.

## Profiles Evaluated

| Profile | Fixture | Requests |
| --- | --- | ---: |
| mixed-realistic | `examples/workloads/krk-mixed-routing-matrix-alpha.json` | 6 |
| GPU-heavy | `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json` | 4 |
| cache-heavy | `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json` | 4 |
| adversarial | `examples/workloads/krk-adversarial-routing-matrix-alpha.json` | 4 |

## Evaluator Commands

```bash
python3 -m kora.matrix_evaluator --matrix examples/workloads/krk-mixed-routing-matrix-alpha.json --json-out docs/evidence/generated/krk-mixed-routing-metrics-v0.json --md-out docs/evidence/generated/krk-mixed-routing-metrics-v0.md --repo-commit committed-example
python3 -m kora.matrix_evaluator --matrix examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json --json-out docs/evidence/generated/krk-gpu-heavy-routing-metrics-v0.json --md-out docs/evidence/generated/krk-gpu-heavy-routing-metrics-v0.md --repo-commit committed-example
python3 -m kora.matrix_evaluator --matrix examples/workloads/krk-cache-heavy-routing-matrix-alpha.json --json-out docs/evidence/generated/krk-cache-heavy-routing-metrics-v0.json --md-out docs/evidence/generated/krk-cache-heavy-routing-metrics-v0.md --repo-commit committed-example
python3 -m kora.matrix_evaluator --matrix examples/workloads/krk-adversarial-routing-matrix-alpha.json --json-out docs/evidence/generated/krk-adversarial-routing-metrics-v0.json --md-out docs/evidence/generated/krk-adversarial-routing-metrics-v0.md --repo-commit committed-example
```

## No-GPU / No-Provider Boundary

This evaluation does not execute GPU workloads, call external providers, or measure live runtime performance. It is a dry-run route-selectivity evaluation over public fixtures.

## Per-Profile Metrics

| Profile | Requests | Exact route accuracy | Acceptable route rate | Unsafe misroute rate | GPU false positives | GPU false negatives | Cache correctness | Safety fallback rate | Failure fallback rate | Compute-weighted GPU demand |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mixed-realistic | 6 | 1.0000 | 1.0000 | 0.0000 | 0 | 0 | 1.0000 | 0.1667 | 0.0000 | 0.5217 |
| GPU-heavy | 4 | 1.0000 | 1.0000 | 0.0000 | 0 | 0 | N/A | 0.2500 | 0.0000 | 0.7059 |
| cache-heavy | 4 | 1.0000 | 1.0000 | 0.0000 | 0 | 0 | 1.0000 | 0.0000 | 0.0000 | 0.5556 |
| adversarial | 4 | 0.7500 | 1.0000 | 0.0000 | 0 | 0 | N/A | 0.5000 | 0.0000 | 0.0000 |

Generated reports:

- [mixed-realistic metrics](generated/krk-mixed-routing-metrics-v0.md)
- [GPU-heavy metrics](generated/krk-gpu-heavy-routing-metrics-v0.md)
- [cache-heavy metrics](generated/krk-cache-heavy-routing-metrics-v0.md)
- [adversarial metrics](generated/krk-adversarial-routing-metrics-v0.md)

## Interpretation

The dry-run KRK policy selected acceptable routes for all evaluated matrix items. Exact route accuracy was 1.0000 for mixed-realistic, GPU-heavy, and cache-heavy profiles, and 0.7500 for the adversarial profile because one ambiguous adversarial item selected an acceptable provider route while the oracle's primary expected route was CPU.

The unsafe misroute rate was 0.0000 across all four profiles. GPU false positive and false negative counts were also 0 across all four profiles.

## Limitations

- The matrix fixtures are small public alpha fixtures, not broad workload samples.
- The policy is the public dry-run policy `krk_dry_run_v0`, not a live provider or GPU execution policy.
- Results measure route selection against oracle labels, not task output quality.
- Compute-weighted GPU demand uses formula version `cwgd_v0` and should remain versioned as the metric evolves.

## Next Evidence Step

The next evidence step is to turn these profile-level results into a July 1 readiness refresh and then extend the matrix with broader workload coverage, provider validation, and bounded GPU-routed subset measurement when public-safe.
