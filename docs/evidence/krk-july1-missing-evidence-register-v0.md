# KRK July 1 Missing Evidence Register v0

Status: refreshed after bounded provider-routed validation.

## Completed or Downgraded Gaps

| Evidence item | Current status | Why it matters | Current limitation | Public claim impact |
| --- | --- | --- | --- | --- |
| Route-selectivity metrics over public matrix profiles | COMPLETE FOR DRY-RUN MATRIX PATH | Shows whether KRK selects routes that match oracle labels across alpha profiles | Small fixture set; no live execution | Supports bounded dry-run route-selectivity statements only |
| JSON and Markdown route metrics outputs | COMPLETE | Makes results reviewable and reproducible | Generated from committed fixtures and dry-run policy only | Supports public evidence-package review |
| Cache correctness over cache-heavy profile | COMPLETE FOR DRY-RUN MATRIX PATH | Tests whether cache-suitable requests route to cache | Only evaluated on public alpha fixture | Supports bounded cache-route correctness statements for the fixture |
| Compute-weighted GPU demand | COMPLETE FOR DRY-RUN MATRIX PATH | Shows route demand mix without executing GPU workloads | Formula version `cwgd_v0` is early | Supports bounded methodology statements only |
| H100 bounded public evidence | COMPLETE FOR PUBLIC MATRIX GPU SUBSET | Separates route selection from actual bounded GPU-class measurement | Small fixture subset only; not production or broad benchmark evidence | Supports only bounded H100 routed-subset measurement statements |
| Provider validation | COMPLETE FOR PUBLIC MATRIX PROVIDER SUBSET | Tests provider-route selections against bounded commercial LLM API execution | Small fixture subset only; raw prompts and responses excluded | Supports only bounded provider-path validation statements |

## Remaining Gaps

| Missing evidence | Why it matters | Current blocker | Next action | Public claim impact |
| --- | --- | --- | --- | --- |
| Runtime-integrated workflow | Connects dry-run route metrics to real KORA runtime flow | Current evaluator is separate from runtime execution | Add integration plan and tests after metrics stabilize | Cannot claim runtime-integrated route-selectivity evidence |
| Broader workload representativeness | Reduces overfitting to small alpha fixtures | Current matrix profiles are intentionally small | Add larger synthetic and service-replay profiles | Cannot claim broad workload superiority |
| Output quality validation | Measures whether selected routes produce acceptable task outputs | Current evaluator measures route selection only | Add quality rubric and sample validation later | Cannot claim task quality improvements |

## Claim Boundary

Current route-selectivity evidence supports bounded statements about dry-run route selection over four public matrix profiles. Current bounded H100 evidence supports only subset-bounded measured execution statements for the GPU-selected public fixture items. Current provider validation supports only subset-bounded provider-path statements for the provider-selected public fixture items. These results do not support savings, broad superiority, provider superiority, GPU superiority, replacement, or infrastructure claims.

## H100 Gap Review Result

The narrow H100 measurement gap is closed for the public matrix GPU subset. Broader H100 evidence remains open for larger workloads, runtime-integrated flows, or any claim beyond subset-bounded measured execution.

## Provider Gap Review Result

The narrow provider validation gap is closed for the public matrix provider subset. Broader provider evidence remains open for larger workloads, output-quality validation, runtime-integrated flows, or any claim beyond subset-bounded provider-path completion.
