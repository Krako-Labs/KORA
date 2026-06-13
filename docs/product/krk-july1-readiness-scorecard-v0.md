# KRK July 1 Readiness Scorecard v0

Status: refreshed after multi-profile route-selectivity evaluation.

This scorecard is not a release announcement. It records readiness based on the current public repository state and the generated dry-run matrix evidence.

## Scorecard

| Area | Status | Evidence | Limitation | Next action |
| --- | --- | --- | --- | --- |
| Product definition | READY | KRK definition, quickstart, architecture, capability matrix | Naming still needs repetition in contributor docs | Keep KRK/KORA Core/KORA hierarchy consistent |
| CLI path | PARTIAL | Current CLI and quickstart docs describe available surfaces | KRK route/explain/benchmark/report are not all top-level commands on this base | Add or document exact command aliases in a future scoped task |
| Docs completeness | READY | Product, architecture, evidence, paper, report, and readiness docs exist | Some docs are planning-level | Keep docs index current as evidence grows |
| Evidence completeness | PARTIAL | Deterministic-heavy evidence plus four dry-run route-selectivity profiles | No live provider validation or bounded H100 subset measurement in this package | Proceed with narrowed RC or run bounded H100 subset only if measured evidence is required |
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

## Readiness Delta

Improved since the prior planning state:

- route-selectivity metrics moved from missing/planned to implemented as dry-run evidence.
- reproducibility moved to READY for the public matrix path because generated JSON and Markdown outputs exist.
- evidence completeness remains PARTIAL because live provider validation, broader workload representativeness, and bounded H100 subset measurement are still open.
- H100 evidence review found methodology and public boundaries, but no public KRK H100 measurement table.

## Current Recommendation

Proceed with a narrowed KRK July 1 RC: package KRK as a deterministic-first routing kernel with deterministic-heavy evidence, four-profile dry-run route-selectivity evidence, and explicit remaining evidence gaps.

H100 measured evidence is not required for this narrowed RC. It becomes required only if the July 1 package expands to measured GPU-class execution claims.
