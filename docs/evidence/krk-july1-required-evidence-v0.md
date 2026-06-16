# KRK July 1 Required Evidence v0

Status: refreshed after route-selectivity evidence generation.

This document lists the evidence expected for a July 1 KRK alpha/release-candidate review. It separates completed public evidence from remaining gaps.

## Evidence Requirements

| Evidence item | Status | Current evidence | Limitation | Next action |
| --- | --- | --- | --- | --- |
| Deterministic-heavy evidence | IMPLEMENTED | 100-task deterministic-heavy benchmark with 80 avoided simulated model invocations and 0 deterministic mismatches | Deterministic-heavy workload only | Keep bounded wording exact |
| KRK matrix examples | IMPLEMENTED | mixed-realistic, GPU-heavy, cache-heavy, and adversarial fixtures | Small alpha fixtures | Add larger profiles after RC scope is fixed |
| Route-selectivity metrics | IMPLEMENTED | Four generated dry-run JSON and Markdown metric reports | No live execution; dry-run policy only | Use as bounded matrix evidence |
| Oracle-label independence | IMPLEMENTED FOR MATRIX PATH | Evaluator separates `router_visible_metadata` from `oracle_labels` | Contract needs broader review as fixture set grows | Preserve separation in future evaluators |
| Compute-weighted GPU demand | IMPLEMENTED FOR MATRIX PATH | `compute_weighted_gpu_demand` emitted with formula version `cwgd_v0` | Formula is early and should stay versioned | Add formula rationale and sensitivity checks later |
| Bounded GPU-routed subset measurement | NOT READY | Methodology exists | No public-safe measurement package in this branch | Define sanitized measurement package before running |
| Provider validation | NOT READY | Provider route methodology exists | No provider calls included in this package | Add a small public-safe sample only if approved |
| Public-safe performance table | IMPLEMENTED FOR CURRENT MATRIX | Performance table includes route-selectivity metrics | Does not include live provider or GPU execution | Refresh table after any new measurements |
| Reproducibility path | IMPLEMENTED FOR MATRIX PATH | `python3 -m kora.matrix_evaluator` commands generate JSON and Markdown outputs | No single wrapper script yet | Add regeneration wrapper if needed |

## Generated Evidence Files

- `docs/evidence/generated/krk-mixed-routing-metrics-v0.json`
- `docs/evidence/generated/krk-mixed-routing-metrics-v0.md`
- `docs/evidence/generated/krk-gpu-heavy-routing-metrics-v0.json`
- `docs/evidence/generated/krk-gpu-heavy-routing-metrics-v0.md`
- `docs/evidence/generated/krk-cache-heavy-routing-metrics-v0.json`
- `docs/evidence/generated/krk-cache-heavy-routing-metrics-v0.md`
- `docs/evidence/generated/krk-adversarial-routing-metrics-v0.json`
- `docs/evidence/generated/krk-adversarial-routing-metrics-v0.md`

## Claim Boundary

The current package supports bounded statements that route-selectivity metrics exist for four public dry-run matrix profiles. It does not support live performance, savings, provider superiority, GPU superiority, broad workload superiority, or release-final claims.
