# KRK July 1 Readiness Scorecard v0

Status: refreshed after bounded H100 routed subset evaluation.

This scorecard is not a release announcement. It records readiness based on the current public repository state, generated dry-run matrix evidence, and bounded H100 subset measurement.

## Scorecard

| Area | Status | Evidence | Limitation | Next action |
| --- | --- | --- | --- | --- |
| Product definition | READY | KRK definition, quickstart, architecture, capability matrix | Naming still needs repetition in contributor docs | Keep KRK/KORA Core/KORA hierarchy consistent |
| CLI path | PARTIAL | Current CLI and quickstart docs describe available surfaces | KRK route/explain/benchmark/report are not all top-level commands on this base | Add or document exact command aliases in a future scoped task |
| Docs completeness | READY | Product, architecture, evidence, paper, report, and readiness docs exist | Some docs are planning-level | Keep docs index current as evidence grows |
| Evidence completeness | PARTIAL | Deterministic-heavy evidence, four dry-run route-selectivity profiles, and bounded H100 subset measurement | No live provider validation, runtime-integrated route-selectivity workflow, or broad workload coverage | Proceed with narrowed RC; keep measurement language subset-bounded |
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

## Readiness Delta

Improved since the prior planning state:

- route-selectivity metrics moved from missing/planned to implemented as dry-run evidence.
- reproducibility moved to READY for the public matrix path because generated JSON and Markdown outputs exist.
- bounded H100 subset measurement moved from open gap to subset-bounded measured evidence.
- evidence completeness remains PARTIAL because live provider validation, broader workload representativeness, and runtime-integrated route-selectivity are still open.

## Current Recommendation

Proceed with a narrowed KRK July 1 RC: package KRK as a deterministic-first routing kernel with deterministic-heavy evidence, four-profile dry-run route-selectivity evidence, bounded H100 routed-subset measurement, and explicit remaining evidence gaps.

The bounded H100 subset result improves the RC evidence package, but it must remain fixture-scoped and claim-bounded.
