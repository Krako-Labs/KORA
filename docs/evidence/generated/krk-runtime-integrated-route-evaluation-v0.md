# KRK Runtime-Integrated Route Evaluation v0

Status: generated runtime-integrated dry-run route-selectivity evidence.

This report runs public matrix requests through a dry-run workflow path: request, KRK route decision, route-specific dry-run executor, evidence record, route-selectivity scoring, and report.

No provider calls or GPU execution were performed.

## Run Metadata

- claim level: `runtime_integrated_dry_run_route_selectivity_measured`
- execution mode: `runtime_integrated_dry_run`
- policy: `KRK`
- policy version: `krk_dry_run_v0`
- total requests: `18`
- provider calls performed: `false`
- GPU execution performed: `false`
- evidence records created: `18`
- repo commit: `cbd32d0`

## Sources

| Profile | Matrix file | Items |
| --- | --- | ---: |
| `mixed-realistic` | `examples/workloads/krk-mixed-routing-matrix-alpha.json` | `6` |
| `GPU-heavy` | `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json` | `4` |
| `cache-heavy` | `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json` | `4` |
| `adversarial` | `examples/workloads/krk-adversarial-routing-matrix-alpha.json` | `4` |

## Route Counts

| Route | Count |
| --- | ---: |
| `deterministic` | `2` |
| `cache` | `3` |
| `CPU` | `2` |
| `provider` | `3` |
| `GPU` | `4` |
| `fallback` | `4` |

## Executor Counts

| Executor route | Count |
| --- | ---: |
| `deterministic` | `2` |
| `cache` | `3` |
| `CPU` | `2` |
| `provider` | `3` |
| `GPU` | `4` |
| `fallback` | `4` |

## Metrics

| Metric | Value |
| --- | ---: |
| `exact_route_accuracy` | `0.9444` |
| `acceptable_route_rate` | `1.0000` |
| `unsafe_misroute_rate` | `0.0000` |
| `safety_fallback_rate` | `0.2222` |
| `failure_fallback_rate` | `0.0000` |
| `error_count` | `0` |
| `error_percentage` | `0.0000` |
| `dry_run_execution_success_rate` | `1.0000` |
| `evidence_records_created` | `18` |

## Fallback Counts

| Fallback class | Count |
| --- | ---: |
| `safety_fallback` | `4` |
| `failure_fallback` | `0` |
| `validation_fallback` | `0` |
| `unknown_fallback` | `0` |

## Claim Boundary

Runtime-integrated dry-run route-selectivity evidence only. This output records request-to-route-to-dry-run-executor evidence records without provider calls, GPU execution, production traffic, production savings, customer savings, infrastructure savings, H100 superiority, provider superiority, or production-readiness claims.
