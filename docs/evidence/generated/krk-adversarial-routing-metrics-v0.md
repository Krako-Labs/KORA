# KRK Route-Selectivity Metrics - adversarial

Status: dry-run route-selectivity evidence.

This report evaluates route choices against independent oracle labels in committed matrix fixtures. It does not require GPU access or provider calls.

## Run Metadata

- profile: `adversarial`
- policy: `KRK`
- policy version: `krk_dry_run_v0`
- total requests: `4`
- claim level: `dry_run_route_selectivity`
- source matrix: `examples/workloads/krk-adversarial-routing-matrix-alpha.json`
- repo commit: `committed-example`

## Route Distribution

| Route | Count |
| --- | ---: |
| `deterministic` | `0` |
| `cache` | `0` |
| `CPU` | `1` |
| `provider` | `1` |
| `GPU` | `0` |
| `fallback` | `2` |

## Correctness Metrics

| Metric | Value |
| --- | ---: |
| `exact_route_accuracy` | `0.7500` |
| `acceptable_route_rate` | `1.0000` |
| `unsafe_misroute_rate` | `0.0000` |
| `gpu_false_positive_count` | `0` |
| `gpu_false_negative_count` | `0` |
| `cache_hit_correctness_rate` | `n/a` |
| `safety_fallback_rate` | `0.5000` |
| `failure_fallback_rate` | `0.0000` |
| `error_count` | `0` |
| `error_percentage` | `0.0000` |
| `compute_weighted_gpu_demand` | `0.0000` |

## Fallback Metrics

| Fallback class | Count |
| --- | ---: |
| `safety_fallback` | `2` |
| `failure_fallback` | `0` |
| `validation_fallback` | `0` |
| `unknown_fallback` | `0` |

## Claim Boundary

Dry-run route-selectivity evidence only. This output does not claim production savings, customer savings, infrastructure savings, GPU superiority, broad workload superiority, provider replacement, production readiness, or formal validation.
