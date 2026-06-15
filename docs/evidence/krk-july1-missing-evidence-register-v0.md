# KRK July 1 Missing Evidence Register v0

Status: refreshed after expanded H100 routed-subset evaluation attempt.

## Completed or Downgraded Gaps

| Evidence item | Current status | Why it matters | Current limitation | Public claim impact |
| --- | --- | --- | --- | --- |
| Route-selectivity metrics over public matrix profiles | COMPLETE FOR DRY-RUN MATRIX PATH | Shows whether KRK selects routes that match oracle labels across alpha profiles | Small fixture set; no live execution | Supports bounded dry-run route-selectivity statements only |
| JSON and Markdown route metrics outputs | COMPLETE | Makes results reviewable and reproducible | Generated from committed fixtures and dry-run policy only | Supports public evidence-package review |
| Cache correctness over cache-heavy profile | COMPLETE FOR DRY-RUN MATRIX PATH | Tests whether cache-suitable requests route to cache | Only evaluated on public alpha fixture | Supports bounded cache-route correctness statements for the fixture |
| Compute-weighted GPU demand | COMPLETE FOR DRY-RUN MATRIX PATH | Shows route demand mix without executing GPU workloads | Formula version `cwgd_v0` is early | Supports bounded methodology statements only |
| Runtime-integrated route-selectivity workflow | COMPLETE FOR DRY-RUN WORKFLOW PATH | Connects route decision, dry-run executor, evidence record, and route scoring | Dry-run only; no provider calls, GPU execution, production traffic, or output-quality validation | Supports bounded runtime-integrated dry-run route-selectivity statements only |
| H100 bounded public evidence | COMPLETE FOR PUBLIC MATRIX GPU SUBSET | Separates route selection from actual bounded GPU-class measurement | Small fixture subset only; not production or broad benchmark evidence | Supports only bounded H100 routed-subset measurement statements |
| Expanded H100 bounded public evidence | PREPARED BUT NOT MEASURED | Would expand GPU-routed path evidence beyond the initial 4-item subset | Safe CUDA/H100 runtime was unavailable in the current execution environment | Supports only a prepared-but-not-measured statement |
| Provider validation | COMPLETE FOR EXPANDED PUBLIC MATRIX PROVIDER SUBSET | Tests provider-route selections against bounded commercial LLM API execution | Expanded sample remains bounded and synthetic; raw prompts and responses excluded | Supports only bounded provider-path validation statements |

## Remaining Gaps

| Missing evidence | Why it matters | Current blocker | Next action | Public claim impact |
| --- | --- | --- | --- | --- |
| Broader workload representativeness | Reduces overfitting to small alpha fixtures | Current matrix profiles are intentionally small | Add larger synthetic and service-replay profiles | Cannot claim broad workload superiority |
| Output quality validation | Measures whether selected routes produce acceptable task outputs | Current evaluator measures route selection only | Add quality rubric and sample validation later | Cannot claim task quality improvements |
| Production workload proof | Tests behavior under real production workload conditions | Current evidence uses public fixtures and bounded validation paths | Add production-like methodology only after separate review | Cannot claim production readiness or production savings |

## July 1 RC Decision Impact

The remaining gaps do not block a July 1 RC if the RC is explicitly scoped as GO WITH CAVEATS and limited to deterministic-heavy evidence, four public dry-run route-selectivity profiles, runtime-integrated dry-run route-selectivity evidence, bounded H100-routed subset measurement, prepared-but-not-measured expanded H100 evaluation, and expanded bounded provider-routed validation.

The remaining gaps do block any broader claim that KRK is production-ready, proves production savings, proves customer savings, proves broad workload superiority, proves H100 superiority, proves provider superiority, or replaces existing model serving/provider routing systems.

## Claim Boundary

Current route-selectivity evidence supports bounded statements about dry-run route selection over four public matrix profiles. Current runtime-integrated route-selectivity evidence supports only dry-run workflow-path statements. Current bounded H100 evidence supports only subset-bounded measured execution statements for the GPU-selected public fixture items. Current expanded H100 evidence supports only a prepared-but-not-measured statement. Current expanded provider validation supports only bounded provider-path statements for provider-selected public fixture items. These results do not support savings, broad superiority, provider superiority, GPU superiority, replacement, production readiness, or infrastructure claims.

## H100 Gap Review Result

The narrow H100 measurement gap is closed for the public matrix GPU subset. The expanded H100 measurement gap remains open because Goal 055 could not run without safe CUDA/H100 runtime availability. Broader H100 evidence remains open for larger workloads, runtime-integrated flows, or any claim beyond subset-bounded measured execution.

## Provider Gap Review Result

The narrow provider validation gap is closed and expanded for provider-selected public matrix items. Broader provider evidence remains open for larger workloads, output-quality validation, runtime-integrated flows, or any claim beyond bounded provider-path completion.
