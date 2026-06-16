# KRK Runtime-Integrated Route Evaluation v0

Status: runtime-integrated dry-run route-selectivity evidence.

This document summarizes a runtime-integrated dry-run KRK route-selectivity evaluation. It moves beyond static matrix scoring by sending public matrix requests through an executable workflow path:

request -> KRK route decision -> route-specific dry-run executor -> evidence record -> route-selectivity scoring -> report.

No provider calls, GPU execution, H100 execution, production traffic, or customer workload execution were performed.

## Scope

The evaluation uses the four existing public KRK matrix profiles:

| Profile | Requests |
| --- | ---: |
| mixed-realistic | 6 |
| GPU-heavy | 4 |
| cache-heavy | 4 |
| adversarial | 4 |

Total requests: 18.

## Dry-Run Executors

Each selected route is passed to a route-specific dry-run executor:

| Route | Executor |
| --- | --- |
| deterministic | `deterministic_dry_run_executor_v0` |
| cache | `cache_dry_run_executor_v0` |
| CPU | `cpu_dry_run_executor_v0` |
| provider | `provider_dry_run_executor_v0` |
| GPU | `gpu_dry_run_executor_v0` |
| fallback | `fallback_dry_run_executor_v0` |

The provider and GPU executors are dry-run only. They do not call providers or use GPU hardware.

## Results

| Metric | Value |
| --- | ---: |
| Total requests | 18 |
| Exact route accuracy | 0.9444 |
| Acceptable route rate | 1.0000 |
| Unsafe misroute rate | 0.0000 |
| Safety fallback rate | 0.2222 |
| Failure fallback rate | 0.0000 |
| Error count | 0 |
| Dry-run execution success rate | 1.0000 |
| Evidence records created | 18 |

## Route Counts

| Route | Count |
| --- | ---: |
| deterministic | 2 |
| cache | 3 |
| CPU | 2 |
| provider | 3 |
| GPU | 4 |
| fallback | 4 |

## Executor Counts

| Executor route | Count |
| --- | ---: |
| deterministic | 2 |
| cache | 3 |
| CPU | 2 |
| provider | 3 |
| GPU | 4 |
| fallback | 4 |

## Generated Evidence

- [Generated runtime-integrated route evaluation JSON](generated/krk-runtime-integrated-route-evaluation-v0.json)
- [Generated runtime-integrated route evaluation Markdown](generated/krk-runtime-integrated-route-evaluation-v0.md)

## What This Proves

This supports the bounded statement that KRK has runtime-integrated dry-run route-selectivity evidence over the current public matrix profiles. The workflow creates one public-safe evidence record per evaluated request and scores route selectivity after the dry-run executor step.

## What This Does Not Prove

This does not prove:

- production savings.
- 10x savings.
- customer savings.
- infrastructure savings.
- H100 superiority.
- provider superiority.
- production readiness.
- output quality improvements.
- broad workload superiority.

## Claim Level

`runtime_integrated_dry_run_route_selectivity_measured`
