# KRK July 1 RC Decision Package v0

Status: refreshed decision package for owner approval.

## Final Recommendation

Recommendation: GO WITH CAVEATS.

KRK July 1 RC can proceed as an evidence-centered release-candidate package if the scope remains limited to deterministic-first routing evidence, four public dry-run matrix profiles, runtime-integrated dry-run route-selectivity evidence, bounded H100-routed subset measurement from Goal 050, repo-owned bounded H100 harness measurement from Goal 058C, historical prepared-but-not-measured expanded H100 evaluation from Goal 055, and expanded bounded provider-routed validation from Goal 054.

This recommendation does not approve a release, tag, production-readiness claim, production savings claim, customer savings claim, provider superiority claim, GPU superiority claim, or broad workload superiority claim.

## Decision

GO WITH CAVEATS.

Reasons:

- KRK now has route-selectivity evidence across four public dry-run matrix profiles.
- KRK now has runtime-integrated dry-run route-selectivity evidence from Goal 053.
- KRK now has bounded H100-routed subset evidence from Goal 050 for the public matrix GPU-selected items.
- KRK now has repo-owned bounded H100 harness measurement from Goal 058C for fixture-derived GPU-routed operations.
- KRK has historical prepared expanded H100-routed subset evaluation from Goal 055, but it was not measured because safe runtime was unavailable in that goal.
- KRK now has expanded bounded provider-routed validation from Goal 054 for the public matrix provider-selected items.
- KRK still does not have production workload proof, customer proof, broad workload representativeness, or output-quality validation.

## Evidence Basis

| Evidence area | Current evidence | Decision impact |
| --- | --- | --- |
| Deterministic-heavy benchmark | 100-task deterministic-heavy benchmark with 80 deterministic/no-model tasks, 20 fallback/model-candidate tasks, 80 avoided simulated model invocations, and 0 deterministic mismatches | Supports deterministic-heavy bounded evidence |
| Route-selectivity | Four public dry-run profiles with 100% acceptable route rate and 0% unsafe misroute rate | Supports execution-path routing evidence over current public matrix profiles |
| Runtime-integrated route-selectivity | Runtime-integrated dry-run workflow with 18 evidence records, 100% acceptable route rate, 0% unsafe misroute rate, and 100% dry-run execution success rate | Supports dry-run workflow-path route-selectivity evidence only |
| H100 bounded subset | Four GPU-selected public matrix items measured in a bounded H100-class execution summary | Supports subset-bounded GPU-routed measurement only |
| Repo-owned H100 harness | Goal 058C measured 24 bounded fixture-derived GPU-routed operations with a reusable public harness | Supports repo-harness-backed bounded H100 measurement only |
| Expanded H100 bounded subset | Goal 055 expanded evaluation prepared but not run because safe CUDA/H100 runtime was unavailable in that goal | Supports only a historical prepared-but-not-measured statement |
| Provider-routed validation | Provider-selected public matrix items completed initial and expanded bounded commercial LLM API validation | Supports bounded provider-path validation only |
| Claim boundary | Existing docs state unsupported claims directly | Supports public-safe RC packaging if wording stays narrow |

## Decision Refresh Source

This package is refreshed by [KRK July 1 RC decision refresh v0](krk-july1-rc-decision-refresh-v0.md), which incorporates Goals 053, 054, and 055.

## Route-Selectivity Evidence

| Profile | Requests | Exact route accuracy | Acceptable route rate | Unsafe misroute rate |
| --- | ---: | ---: | ---: | ---: |
| mixed-realistic | 6 | 1.0000 | 1.0000 | 0.0000 |
| GPU-heavy | 4 | 1.0000 | 1.0000 | 0.0000 |
| cache-heavy | 4 | 1.0000 | 1.0000 | 0.0000 |
| adversarial | 4 | 0.7500 | 1.0000 | 0.0000 |

Evidence sources:

- [KRK route-selectivity results v0](../evidence/krk-route-selectivity-results-v0.md)
- [KRK multi-profile routing evaluation v0](../evidence/krk-multi-profile-routing-evaluation-v0.md)
- generated route metrics JSON files under `docs/evidence/generated/`

Interpretation: KRK demonstrates route-selectivity on four public dry-run matrix profiles. This is not live runtime proof.

## Runtime-Integrated Dry-Run Evidence

| Metric | Value |
| --- | ---: |
| Total requests | 18 |
| Exact route accuracy | 0.9444 |
| Acceptable route rate | 1.0000 |
| Unsafe misroute rate | 0.0000 |
| Dry-run execution success rate | 1.0000 |
| Evidence records created | 18 |
| Error count | 0 |

Evidence sources:

- [KRK runtime-integrated route evaluation v0](../evidence/krk-runtime-integrated-route-evaluation-v0.md)
- [Generated runtime-integrated route evaluation JSON](../evidence/generated/krk-runtime-integrated-route-evaluation-v0.json)

Interpretation: KRK has runtime-integrated dry-run route-selectivity evidence over the current public matrix profiles. This does not prove provider execution, GPU execution, H100 execution, production readiness, savings, or broad workload behavior.

## H100 Bounded Subset Evidence

| Metric | Value |
| --- | ---: |
| Subset count | 4 |
| Total compute weight | 58 |
| Runtime seconds | 0.035312 |
| Throughput, requests/second | 113.277481 |
| Throughput, compute weight/second | 1642.523477 |
| Bounded workload peak allocation MB | 240.000 |

Evidence sources:

- [KRK bounded H100 evaluation v0](../evidence/krk-bounded-h100-evaluation-v0.md)
- [Generated H100 bounded JSON summary](../evidence/generated/krk-h100-bounded-summary-v0.json)
- [Goal 058C H100 bounded execution report](krk-goal058c-h100-bounded-execution-v0.md)
- [Generated Goal 058C H100 bounded execution JSON summary](../evidence/generated/krk-goal058c-h100-bounded-execution-summary-v0.json)
- [KRK expanded bounded H100 evaluation v0](../evidence/krk-expanded-bounded-h100-evaluation-v0.md)
- [Generated expanded H100 bounded JSON summary](../evidence/generated/krk-expanded-h100-bounded-summary-v0.json)

Interpretation: KRK-selected GPU subset items from the public matrix fixtures have bounded H100-class measurement, and Goal 058C adds repo-owned bounded harness evidence for 24 fixture-derived operations. This is not H100 superiority, broad GPU benchmark, infrastructure savings, customer savings, or production performance proof.

Expanded H100 note: Goal 055 prepared the expanded bounded H100 evaluation, but did not run it because a safe CUDA/H100 runtime was not available in that goal. Goal 058C supersedes the basic repo-harness execution blocker with bounded measured harness evidence, but broader expanded H100 representativeness remains open.

## Provider-Routed Validation Evidence

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

Initial validation:

| Metric | Value |
| --- | ---: |
| Sample count | 3 |
| Success count | 3 |
| Failure count | 0 |
| Latency min, ms | 1581.517 |
| Latency median, ms | 1583.670 |
| Latency max, ms | 3635.988 |
| Input units/tokens total | 176 |
| Output units/tokens total | 156 |

Evidence sources:

- [KRK provider-routed validation v0](../evidence/krk-provider-routed-validation-v0.md)
- [KRK expanded provider-routed validation v0](../evidence/krk-expanded-provider-routed-validation-v0.md)
- [Generated provider-routed validation JSON summary](../evidence/generated/krk-provider-routed-validation-summary-v0.json)
- [Generated expanded provider-routed validation JSON summary](../evidence/generated/krk-expanded-provider-routed-validation-summary-v0.json)

Interpretation: KRK-selected provider-path items from the public matrix fixtures completed bounded and expanded bounded provider-path validation. The expanded sample strengthens the bounded provider-path evidence and downgrades the provider sample-size risk, but it is not provider superiority, provider cost reduction, broad provider benchmarking, or replacement of provider routing systems.

## Remaining Caveats

- Runtime-integrated route-selectivity evidence is dry-run only.
- Current matrix profiles are small alpha fixtures.
- Output quality validation is not included.
- Provider sample size is expanded to 12 successful bounded calls, but still bounded.
- H100 subset and harness samples are bounded; broader expanded H100 representativeness remains open.
- CLI surface still has mismatch between planned top-level KRK commands and current available commands.
- KORA Core inspect/compare/run/report workflow remains roadmap-level rather than fully implemented.

## Owner Approval Checklist

- [ ] Approve `GO WITH CAVEATS` as the July 1 RC decision.
- [ ] Confirm the final RC scope excludes production, savings, customer, broad superiority, replacement, and production-readiness claims.
- [ ] Confirm no release or tag should be created until explicitly approved in a later goal.
- [ ] Confirm public copy uses only the allowed claim package.
- [ ] Confirm remaining caveats are visible in the RC package.
- [ ] Confirm validation gates pass before PR readiness work begins.

## Release/Tag Boundary

This package is not a release approval and does not create a tag.

Allowed next step: prepare PR readiness for the RC package.

Not allowed in this goal:

- create a release.
- create a tag.
- push commits.
- open a PR.
- claim production readiness.
- claim production savings, customer savings, infrastructure savings, provider superiority, GPU superiority, or broad workload superiority.
