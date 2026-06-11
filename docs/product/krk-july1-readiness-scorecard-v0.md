# KRK July 1 Readiness Scorecard v0

Status: owner-review scorecard for the KRK July 1 alpha/release-candidate planning package.

This scorecard is not a release announcement. It records readiness based on the current public repository state.

## Scorecard

| Area | Status | Evidence | Limitation | Next action |
| --- | --- | --- | --- | --- |
| Product definition | READY | KRK definition, quickstart, architecture, capability matrix | Naming still needs repetition in contributor docs | Keep KRK/KORA Core/KORA hierarchy consistent |
| CLI/user path | PARTIAL | Current CLI and quickstart docs describe available surfaces | KRK route/explain/benchmark/report are not all top-level commands on this base | Add or document exact command aliases in a future scoped task |
| Docs completeness | READY | Product, architecture, evidence, paper, and report docs exist | Some docs are planning-level | Keep docs index current as evidence grows |
| Evidence completeness | PARTIAL | Deterministic-heavy evidence plus four dry-run route-selectivity profiles | No live provider validation or bounded GPU-routed subset measurement in this package | Add broader and live-backed evidence only when public-safe |
| Reproducibility | READY | Matrix fixtures parse with `jq`; evaluator emits JSON and Markdown outputs | Broader workload sampling is still pending | Add scripted regeneration wrapper if needed |
| Claim boundary | READY | Claim boundary tables and generated output boundaries | Review required before future public announcements | Keep unsupported claims out of README and reports |
| Public/private boundary | READY | Generated metrics contain public fixtures only | Raw private artifacts must remain out of public docs | Continue scan gates before PRs |
| Examples | READY | Four KRK matrix fixtures and generated metrics exist | Fixtures are intentionally small | Expand profiles after RC scope is decided |
| Paper/technical note | PARTIAL | Draft package exists | Needs final experiments and editing before submission-style use | Refresh paper after route-selectivity and next evidence |
| Community preview | PARTIAL | Docs explain KRK wedge and KORA Core direction | Contributor tasks and issues are not yet packaged | Create contributor-facing next tasks after RC readiness refresh |

## Route-Selectivity Status

Route-selectivity metrics are no longer missing for the four public alpha matrix profiles. The current status is implemented as dry-run evidence:

- mixed-realistic.
- GPU-heavy.
- cache-heavy.
- adversarial.

These results are benchmark-methodology evidence, not production proof.

## Remaining Readiness Gaps

- Bounded GPU-routed subset measurement is not included in the current public package.
- Provider validation is not included in the current public package.
- Broader workload representativeness remains limited.
- Runtime-integrated route-selectivity workflow remains separate from the dry-run evaluator.

## Current Recommendation

Treat KRK as a July 1 alpha/release-candidate planning package with real dry-run route-selectivity evidence and explicit remaining evidence gaps.
