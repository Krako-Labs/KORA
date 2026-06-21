# KRK July 1 Missing Evidence Register v0

Status: refreshed after Goal 102 workload representativeness seed.

## Completed or Downgraded Gaps

| Evidence item | Current status | Why it matters | Current limitation | Public claim impact |
| --- | --- | --- | --- | --- |
| Route-selectivity metrics over public matrix profiles | COMPLETE FOR DRY-RUN MATRIX PATH | Shows whether KRK selects routes that match oracle labels across alpha profiles | Small fixture set; no live execution | Supports bounded dry-run route-selectivity statements only |
| JSON and Markdown route metrics outputs | COMPLETE | Makes results reviewable and reproducible | Generated from committed fixtures and dry-run policy only | Supports public evidence-package review |
| Cache correctness over cache-heavy profile | COMPLETE FOR DRY-RUN MATRIX PATH | Tests whether cache-suitable requests route to cache | Only evaluated on public alpha fixture | Supports bounded cache-route correctness statements for the fixture |
| Compute-weighted GPU demand | COMPLETE FOR DRY-RUN MATRIX PATH | Shows route demand mix without executing GPU workloads | Formula version `cwgd_v0` is early | Supports bounded methodology statements only |
| Runtime-integrated route-selectivity workflow | COMPLETE FOR DRY-RUN WORKFLOW PATH | Connects route decision, dry-run executor, evidence record, and route scoring | Dry-run only; no provider calls, GPU execution, production traffic, or output-quality validation | Supports bounded runtime-integrated dry-run route-selectivity statements only |
| H100 bounded public evidence | COMPLETE FOR PUBLIC MATRIX GPU SUBSET | Separates route selection from actual bounded GPU-class measurement | Small fixture subset only; not production or broad benchmark evidence | Supports only bounded H100 routed-subset measurement statements |
| Expanded H100 bounded public evidence | PREPARED BUT NOT MEASURED | Would expand GPU-routed path evidence beyond the initial 4-item subset | Safe CUDA/H100 runtime was unavailable in Goal 055's execution environment | Supports only a prepared-but-not-measured statement |
| H100 runtime recovery plan | COMPLETE | Diagnoses why Goal 055 could not run and defines the next bounded execution path | Does not itself run H100 workloads or add expanded measurements | Supports runtime-gap and recovery-plan statements only |
| Repo-owned bounded H100 harness evidence | COMPLETE FOR BOUNDED FIXTURE-DERIVED HARNESS PATH | Replaces the prior basic repo-harness execution blocker with reusable public harness code and aggregate measured output | 24 bounded operations derived from 4 GPU-routed fixture items; not expanded workload representativeness | Supports only bounded repo-owned H100 harness measurement statements |
| Goal 099 AI Champion server-run packet | COMPLETE FOR CONTROLLED WORKLOAD-PATH EXECUTION | Confirms the Goal 098 packet was executed on the AI Champion H100 server across CPU/non-GPU and bounded H100 paths | CPU/non-GPU phase used `CUDA_VISIBLE_DEVICES=""`; H100 phase measured 24 public fixture-derived operations; 2 H100-class devices were visible but both-GPU active use and multi-GPU scaling were not proven | Supports only controlled server-run workload-path execution statements |
| Goal 102 workload representativeness seed | SEEDED FOR FUTURE ROUTE-ONLY EVALUATION | Adds a public-safe synthetic 40-item fixture across broader workload categories | Shape-validated fixture only; no runner, provider calls, H100 execution, output-quality proof, or production workload proof | Supports only fixture-design and planning statements |
| Provider validation | COMPLETE FOR EXPANDED PUBLIC MATRIX PROVIDER SUBSET | Tests provider-route selections against bounded commercial LLM API execution | Expanded 12-call sample remains bounded and synthetic; raw prompts and responses excluded | Supports only bounded provider-path validation statements |

## Remaining Gaps

| Missing evidence | Why it matters | Current blocker | Next action | Public claim impact |
| --- | --- | --- | --- | --- |
| Broader workload representativeness | Reduces overfitting to small alpha fixtures | Goal 102 adds a seed fixture, but no route-only evaluator, production workload proof, or output-quality validation exists yet | Implement a route-only evaluator for the Goal 102 seed, then consider larger synthetic profiles only after approval | Cannot claim broad workload superiority or production workload proof |
| Expanded and broader H100 representativeness | Expands GPU-routed path evidence beyond the 4 GPU-routed public fixture items and 24 bounded harness operations | Goal 055 remains historical `not_run`; Goal 058C and Goal 099 measured bounded repo-owned harness paths but not a broader workload set | Add larger fixture-derived H100 samples and workload diversity in a later bounded task | Cannot claim broad H100 runtime, throughput, memory, workload-representativeness evidence, both-GPU active use, or multi-GPU scaling |
| Output quality validation | Measures whether selected routes produce acceptable task outputs | Current evaluator measures route selection only | Add quality rubric and sample validation later | Cannot claim task quality improvements |
| Production workload proof | Tests behavior under real production workload conditions | Current evidence uses public fixtures and bounded validation paths | Add production-like methodology only after separate review | Cannot claim production readiness or production savings |

## July 1 RC Decision Impact

The remaining gaps do not block a July 1 RC if the RC is explicitly scoped as GO WITH CAVEATS and limited to deterministic-heavy evidence, four public dry-run route-selectivity profiles, runtime-integrated dry-run route-selectivity evidence, bounded H100-routed subset measurement, repo-owned bounded H100 harness measurement, Goal 099 controlled server-run workload-path evidence, Goal 102 fixture-design seed support, prepared-but-not-measured historical Goal 055 expanded H100 evaluation, and expanded bounded provider-routed validation.

The remaining gaps do block any broader claim that KRK is production-ready, proves production savings, proves customer savings, proves broad workload superiority, proves H100 superiority, proves provider superiority, or replaces existing model serving/provider routing systems.

## Claim Boundary

Current route-selectivity evidence supports bounded statements about dry-run route selection over four public matrix profiles. Current runtime-integrated route-selectivity evidence supports only dry-run workflow-path statements. Current bounded H100 evidence supports only subset-bounded measured execution statements for the GPU-selected public fixture items and the Goal 058C and Goal 099 repo-owned bounded harness paths. Current Goal 102 representativeness seed supports only fixture-design and planning statements. Current Goal 055 expanded H100 evidence supports only a prepared-but-not-measured historical statement. Current expanded provider validation supports only bounded provider-path statements for provider-selected public fixture items. These results do not support savings, broad superiority, provider superiority, GPU superiority, H100 superiority, both-GPU active use, multi-GPU scaling, replacement, production readiness, production workload proof, output-quality proof, or infrastructure claims.

## Workload Representativeness Gap Review Result

Goal 102 seeds broader workload representativeness with a public-safe synthetic fixture across support/ticket, issue triage, incident routing, document intake, RAG-style routing, agent workflow, cache reuse, tool-needed, provider-needed, fallback, mixed workflow, validation, reporting, GPU-candidate, and output-quality-methodology categories. This is not completed representativeness evidence. A future route-only evaluator or output-quality methodology task is still required before making any measured claim.

## H100 Gap Review Result

The narrow H100 measurement gap is closed for the public matrix GPU subset. Goal 058C closes the basic repo-owned H100 harness blocker with a measured 24-operation bounded harness run. Goal 099 adds controlled AI Champion H100 server-run evidence with 24 operations, 24 successes, and 0 failures over public fixture-derived workload paths. The Goal 055 expanded H100 measurement gap remains historical and open because that goal did not measure expanded runtime, throughput, or memory evidence. Broader H100 evidence remains open for larger workloads, runtime-integrated flows, both-GPU active-use evidence, multi-GPU scaling evidence, or any claim beyond subset-bounded measured execution.

## Provider Gap Review Result

The narrow provider validation gap is closed and expanded for provider-selected public matrix items. Broader provider evidence remains open for larger workloads, output-quality validation, runtime-integrated flows, or any claim beyond bounded provider-path completion.
