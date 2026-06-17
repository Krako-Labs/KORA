# KRK Expanded Bounded H100 Evaluation v0

Status: prepared, not run.

This document records the Goal 055 attempt to expand bounded H100 routed-subset evidence beyond the initial 4-item public matrix subset. The expanded evaluation was not run because a safe CUDA/H100 runtime was not available in the current execution environment.

## Purpose

The purpose of this evaluation is to strengthen KRK GPU-routed path evidence while preserving public/private and claim boundaries. It is not a raw H100 benchmark, H100 superiority claim, production cost claim, infrastructure savings claim, or broad workload superiority claim.

## Subset Construction

The intended expanded subset is derived from KRK-selected GPU-routed public matrix and runtime evidence. The current public GPU-routed source items remain:

| Request | Profile | Workload class | Expected route |
| --- | --- | --- | --- |
| cache-003 | cache-heavy | cache-miss-complex | GPU |
| gpu-001 | GPU-heavy | large-batch-generation | GPU |
| gpu-002 | GPU-heavy | multimodal-transform | GPU |
| mixed-004 | mixed-realistic | large-batch-embedding-like | GPU |

For an expanded run, these public-safe source items should be used to construct 20 to 50 bounded synthetic GPU-routed operations. The construction must remain fixture-derived, bounded, and public-safe.

## H100 Evaluation Run

Expanded H100 evaluation run: no.

Reason: safe CUDA/H100 runtime was not available in the current execution environment.

No GPU workload was executed for this expanded evaluation. No raw GPU logs, hostnames, IP addresses, usernames, SSH details, device serials, private paths, cloud/account details, or operational notes were committed.

## Sanitized Metrics

| Metric | Value |
| --- | --- |
| Claim level | `expanded_h100_validation_not_run` |
| Subset count | 0 |
| Execution mode | not run |
| Success count | 0 |
| Failure count | 0 |
| Runtime seconds | N/A |
| Throughput, requests/second | N/A |
| Throughput, compute weight/second | N/A |
| Peak bounded allocation MB | N/A |
| CUDA context memory before MB | N/A |
| CUDA context memory after MB | N/A |
| Raw logs committed | false |
| Private infrastructure details committed | false |

Generated summaries:

- [Generated expanded H100 bounded JSON summary](generated/krk-expanded-h100-bounded-summary-v0.json)
- [Generated expanded H100 bounded Markdown summary](generated/krk-expanded-h100-bounded-summary-v0.md)

## Comparison to Goal 050

Goal 050 remains the current measured H100 evidence. It measured the initial 4-item GPU-selected public matrix subset and reported:

| Metric | Goal 050 value |
| --- | ---: |
| Subset count | 4 |
| Runtime seconds | 0.035312 |
| Throughput, requests/second | 113.277481 |
| Throughput, compute weight/second | 1642.523477 |
| Bounded workload peak allocation MB | 240.000 |

Goal 055 prepared the expanded evidence slot but did not add a new H100 measurement because safe runtime was unavailable.

## Limitations

- The expanded H100 subset was not measured.
- The current measured H100 evidence remains limited to 4 public matrix GPU-routed items.
- No runtime-integrated GPU execution was performed.
- No output-quality validation was performed.
- No production workload, infrastructure, or cost evidence was produced.

## Claim Boundary

Allowed:

- Expanded H100 evaluation is prepared but not yet measured.
- Existing H100 evidence remains limited to the prior bounded 4-item public matrix subset.

Not allowed:

- production cost reduction.
- GPU cost reduction.
- 10x savings.
- customer savings.
- H100 superiority.
- GPU superiority.
- broad GPU benchmark.
- infrastructure savings.
- replacement of GPU serving systems.
- production readiness.

## Public/Private Boundary

This document and its generated summaries intentionally exclude raw GPU logs, server names, IP addresses, usernames, SSH details, private paths, device serials, cloud/account details, billing details, and private operational notes.
