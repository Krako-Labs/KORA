# KRK Route-Selectivity Results v0

Status: computed dry-run matrix results.

This document records computed route-selectivity metrics for the four public KRK matrix profiles. The source outputs are committed under `docs/evidence/generated/`.

## Scope

These results evaluate route decisions against oracle labels. They do not measure live provider calls, GPU execution, production deployments, or user-facing task quality.

## Results

| Metric | mixed-realistic | GPU-heavy | cache-heavy | adversarial |
| --- | ---: | ---: | ---: | ---: |
| `total_requests` | 6 | 4 | 4 | 4 |
| `exact_route_accuracy` | 1.0000 | 1.0000 | 1.0000 | 0.7500 |
| `acceptable_route_rate` | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `unsafe_misroute_rate` | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `gpu_false_positive_count` | 0 | 0 | 0 | 0 |
| `gpu_false_negative_count` | 0 | 0 | 0 | 0 |
| `cache_hit_correctness_rate` | 1.0000 | N/A | 1.0000 | N/A |
| `safety_fallback_rate` | 0.1667 | 0.2500 | 0.0000 | 0.5000 |
| `failure_fallback_rate` | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `compute_weighted_gpu_demand` | 0.5217 | 0.7059 | 0.5556 | 0.0000 |

## Route Distribution

| Profile | deterministic | cache | CPU | provider | GPU | fallback |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| mixed-realistic | 1 | 1 | 1 | 1 | 1 | 1 |
| GPU-heavy | 1 | 0 | 0 | 0 | 2 | 1 |
| cache-heavy | 0 | 2 | 0 | 1 | 1 | 0 |
| adversarial | 0 | 0 | 1 | 1 | 0 | 2 |

## Source Outputs

- [mixed-realistic JSON](generated/krk-mixed-routing-metrics-v0.json)
- [mixed-realistic Markdown](generated/krk-mixed-routing-metrics-v0.md)
- [GPU-heavy JSON](generated/krk-gpu-heavy-routing-metrics-v0.json)
- [GPU-heavy Markdown](generated/krk-gpu-heavy-routing-metrics-v0.md)
- [cache-heavy JSON](generated/krk-cache-heavy-routing-metrics-v0.json)
- [cache-heavy Markdown](generated/krk-cache-heavy-routing-metrics-v0.md)
- [adversarial JSON](generated/krk-adversarial-routing-metrics-v0.json)
- [adversarial Markdown](generated/krk-adversarial-routing-metrics-v0.md)

## Claim Boundary

These are dry-run matrix metrics. They support the statement that KRK has public route-selectivity evidence over four alpha matrix profiles. They do not support production, savings, broad superiority, or live infrastructure claims.
