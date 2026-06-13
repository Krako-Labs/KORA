# KRK July 1 Missing Evidence Register v0

Status: refreshed after multi-profile route-selectivity evaluation.

## Completed or Downgraded Gaps

| Evidence item | Current status | Why it matters | Current limitation | Public claim impact |
| --- | --- | --- | --- | --- |
| Route-selectivity metrics over public matrix profiles | COMPLETE FOR DRY-RUN MATRIX PATH | Shows whether KRK selects routes that match oracle labels across alpha profiles | Small fixture set; no live execution | Supports bounded dry-run route-selectivity statements only |
| JSON and Markdown route metrics outputs | COMPLETE | Makes results reviewable and reproducible | Generated from committed fixtures and dry-run policy only | Supports public evidence-package review |
| Cache correctness over cache-heavy profile | COMPLETE FOR DRY-RUN MATRIX PATH | Tests whether cache-suitable requests route to cache | Only evaluated on public alpha fixture | Supports bounded cache-route correctness statements for the fixture |
| Compute-weighted GPU demand | COMPLETE FOR DRY-RUN MATRIX PATH | Shows route demand mix without executing GPU workloads | Formula version `cwgd_v0` is early | Supports bounded methodology statements only |

## Remaining Gaps

| Missing evidence | Why it matters | Current blocker | Next action | Public claim impact |
| --- | --- | --- | --- | --- |
| H100 bounded public evidence | Separates route selection from actual bounded GPU-class measurement | No public-safe measurement package in this branch | Define sanitized inputs, outputs, and reproducibility metadata before running | Cannot claim live GPU performance from current matrix results |
| Provider validation | Tests provider-route selections against provider-backed execution | No provider calls are included in this dry-run package | Add a small public-safe provider validation sample only if approved | Cannot claim provider-backed quality or latency evidence |
| Runtime-integrated workflow | Connects dry-run route metrics to real KORA runtime flow | Current evaluator is separate from runtime execution | Add integration plan and tests after metrics stabilize | Cannot claim runtime-integrated route-selectivity evidence |
| Broader workload representativeness | Reduces overfitting to small alpha fixtures | Current matrix profiles are intentionally small | Add larger synthetic and service-replay profiles | Cannot claim broad workload superiority |
| Output quality validation | Measures whether selected routes produce acceptable task outputs | Current evaluator measures route selection only | Add quality rubric and sample validation later | Cannot claim task quality improvements |

## Claim Boundary

Current route-selectivity evidence supports bounded statements about dry-run route selection over four public matrix profiles. It does not support live execution, savings, broad superiority, or infrastructure claims.
