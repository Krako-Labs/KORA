# KRK July 1 Readiness Scorecard v0

Status: refreshed for July 1 RC decision refresh.

This scorecard is not a release announcement. It records readiness based on the current public repository state, generated dry-run matrix evidence, runtime-integrated dry-run route-selectivity evidence, bounded H100 subset measurement, repo-owned bounded H100 harness measurement, a historical prepared-but-not-measured expanded H100 evaluation slot, and expanded bounded provider-path validation.

## Scorecard

| Area | Status | Evidence | Limitation | Next action |
| --- | --- | --- | --- | --- |
| Product definition | READY | KRK definition, quickstart, architecture, capability matrix | Naming still needs repetition in contributor docs | Keep KRK/KORA Core/KORA hierarchy consistent |
| CLI path | PARTIAL | Current CLI and quickstart docs describe available surfaces | KRK route/explain/benchmark/report are not all top-level commands on this base | Add or document exact command aliases in a future scoped task |
| Docs completeness | READY | Product, architecture, evidence, paper, report, and readiness docs exist | Some docs are planning-level | Keep docs index current as evidence grows |
| Evidence completeness | PARTIAL | Deterministic-heavy evidence, four dry-run route-selectivity profiles, runtime-integrated dry-run route-selectivity evidence, bounded H100 subset measurement, repo-owned bounded H100 harness measurement, prepared expanded H100 evaluation slot, and expanded bounded provider-path validation | No broader expanded H100 workload representativeness, broad workload coverage, output-quality validation, or production workload proof | Proceed with narrowed RC; keep measurement language subset-bounded |
| Route-selectivity | READY | Four public dry-run profiles with 100% acceptable route rate and 0% unsafe misroute rate | Small public fixture set | Keep as bounded route-selectivity evidence |
| Runtime-integrated dry-run evidence | READY FOR DRY-RUN PATH | Goal 053 runtime-integrated dry-run workflow with 18 evidence records and 100% dry-run execution success rate | No provider calls, GPU execution, production traffic, or output-quality validation | Keep dry-run boundary visible |
| Provider validation | READY FOR BOUNDED PROVIDER PATH | Goal 054 expanded bounded provider validation with 12 successes and 0 failures | Bounded synthetic sample; not provider benchmark evidence | Keep provider claims aggregate-only and bounded |
| H100 bounded evidence | READY FOR SMALL BOUNDED SUBSET | Goal 050 4-item bounded H100 routed-subset measurement | Small subset only | Keep H100 claim subset-bounded |
| H100 repo-owned harness evidence | READY FOR BOUNDED HARNESS PATH | Goal 058C repo-owned harness measured 24 bounded fixture-derived GPU-routed operations with 24 successes and 0 failures | Fixture-derived harness path only; not broader workload representativeness | Keep H100 claim harness-bounded |
| H100 expanded evidence | NOT RUN HISTORICALLY | Goal 055 prepared expanded H100 evaluation, but safe CUDA/H100 runtime was unavailable in that goal | No broader expanded H100 workload-representativeness evidence | Expand later only in a safe bounded environment |
| Reproducibility | READY | Matrix fixtures parse with `jq`; evaluator emits JSON and Markdown outputs | Broader workload sampling is still pending | Add scripted regeneration wrapper if needed |
| Claim boundary | READY | Claim boundary tables and generated output boundaries | Review required before future public announcements | Keep unsupported claims out of README and reports |
| Public/private boundary | READY | Generated metrics contain public fixtures only | Raw private artifacts must remain out of public docs | Continue scan gates before PRs |
| Examples | READY | Four KRK matrix fixtures and generated metrics exist | Fixtures are intentionally small | Expand profiles after RC scope is decided |
| Paper draft | PARTIAL | Draft package exists | Needs final experiment references and editing before submission-style use | Refresh paper after route-selectivity and next evidence |
| Community preview | PARTIAL | Docs explain KRK wedge and KORA Core direction | Contributor tasks and issues are not yet packaged | Create contributor-facing next tasks after RC readiness refresh |

## Route-Selectivity Status

Route-selectivity metrics are no longer missing for the four public alpha matrix profiles. The current status is implemented as dry-run evidence:

| Profile | Exact route accuracy | Acceptable route rate | Unsafe misroute rate |
| --- | ---: | ---: | ---: |
| mixed-realistic | 1.0000 | 1.0000 | 0.0000 |
| GPU-heavy | 1.0000 | 1.0000 | 0.0000 |
| cache-heavy | 1.0000 | 1.0000 | 0.0000 |
| adversarial | 0.7500 | 1.0000 | 0.0000 |

These results are benchmark-methodology evidence, not production proof.

## Runtime-Integrated Dry-Run Route Evaluation Status

The current package now includes runtime-integrated dry-run route-selectivity evidence:

| Metric | Value |
| --- | ---: |
| Total requests | 18 |
| Exact route accuracy | 0.9444 |
| Acceptable route rate | 1.0000 |
| Unsafe misroute rate | 0.0000 |
| Dry-run execution success rate | 1.0000 |
| Evidence records created | 18 |
| Error count | 0 |

This supports only a runtime-integrated dry-run route-selectivity statement. It does not support provider execution, GPU execution, production readiness, savings, or broad workload claims.

## Bounded H100 Subset Status

The current package now includes bounded H100 measurement for the GPU-selected public matrix subset:

| Metric | Value |
| --- | ---: |
| Subset count | 4 |
| Runtime seconds | 0.035312 |
| Throughput, requests/second | 113.277481 |
| Throughput, compute weight/second | 1642.523477 |
| Bounded workload peak allocation MB | 240.000 |

This supports only a subset-bounded measured-evidence statement. It does not support production, savings, provider, GPU-superiority, or broad workload claims.

## Repo-Owned Bounded H100 Harness Status

Goal 058C adds measured repo-owned bounded H100 harness evidence:

| Metric | Value |
| --- | ---: |
| Fixture count | 18 |
| GPU-routed fixture count | 4 |
| Operation count | 24 |
| Success count | 24 |
| Failure count | 0 |
| Runtime seconds | 0.034976 |
| Throughput, requests/second | 686.176591 |
| Throughput, compute weight/second | 9949.560571 |
| Peak bounded allocation MB | 24.0 |
| CUDA device count | 2 |

This supports only a repo-harness-backed bounded H100 measurement statement. It does not support production, savings, H100-superiority, GPU-superiority, infrastructure, or broad workload claims.

## Expanded Bounded H100 Status

Goal 055 prepared an expanded bounded H100 routed-subset evaluation, but it was not run because a safe CUDA/H100 runtime was not available in that goal's execution environment.

| Metric | Value |
| --- | --- |
| Expanded evaluation run | no |
| Subset count | 0 |
| Success count | 0 |
| Failure count | 0 |
| Claim level | `expanded_h100_validation_not_run` |

The Goal 055 expanded evaluation does not add runtime, throughput, memory, production, savings, GPU-superiority, H100-superiority, or broad workload evidence. Goal 058C is separate measured bounded harness evidence and does not convert Goal 055 into a measured expanded evaluation.

## Bounded Provider Path Status

The current package includes bounded and expanded bounded commercial LLM API validation for provider-selected public matrix items:

| Metric | Value |
| --- | ---: |
| Initial sample count | 3 |
| Initial success count | 3 |
| Initial failure count | 0 |
| Expanded sample count | 12 |
| Expanded success count | 12 |
| Expanded failure count | 0 |
| Expanded latency min, ms | 1418.283 |
| Expanded latency median, ms | 2601.086 |
| Expanded latency p95, ms | 5888.007 |
| Expanded latency max, ms | 5888.007 |
| Expanded input units/tokens total | 1102 |
| Expanded output units/tokens total | 745 |

This supports only a subset-bounded provider-path measured-evidence statement. It does not support production, savings, provider-cost, provider-superiority, broad provider benchmark, or replacement claims.

## Readiness Delta

Improved since the prior planning state:

- route-selectivity metrics moved from missing/planned to implemented as dry-run evidence.
- runtime-integrated dry-run route-selectivity moved from missing to measured evidence.
- reproducibility moved to READY for the public matrix path because generated JSON and Markdown outputs exist.
- bounded H100 subset measurement moved from open gap to subset-bounded measured evidence.
- repo-owned bounded H100 harness evidence moved from blocked to measured in Goal 058C.
- Goal 055 expanded H100 evidence remains historical prepared-but-not-measured evidence.
- bounded provider-path validation moved from open gap to subset-bounded measured evidence, then expanded from 3 to 12 bounded calls.
- evidence completeness remains PARTIAL because broader workload representativeness, output-quality validation, and production workload proof are still open.

## Current Recommendation

Proceed with the KRK July 1 RC as GO WITH CAVEATS: package KRK as a deterministic-first routing kernel with deterministic-heavy evidence, four-profile dry-run route-selectivity evidence, runtime-integrated dry-run route-selectivity evidence, bounded H100 routed-subset measurement, repo-owned bounded H100 harness measurement, expanded bounded provider-path validation, and explicit remaining evidence gaps.

The bounded H100, repo-owned H100 harness, and expanded provider-path results improve the RC evidence package, but all must remain fixture-scoped and claim-bounded. The Goal 055 expanded H100 evaluation is prepared but not measured and should not be counted as broader expanded H100 runtime, throughput, or memory evidence.

The July 1 RC is not a production-readiness, production savings, customer savings, infrastructure savings, H100 superiority, provider superiority, broad workload superiority, or replacement claim.
