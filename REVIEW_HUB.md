# KORA Review Hub

Status: current public review and continuation hub.

Last updated by: Goal 070C revalidation.

## Project Identity

KORA makes AI workloads routable.

KRK means KORA Routing Kernel. KRK is the deterministic-first execution routing kernel inside KORA Core. It routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

## Public Truth

- repository: `https://github.com/Krako-Labs/KORA`
- public truth branch: `origin/main`
- active evidence branch: `goal044_krk_route_selectivity_metrics_plan`
- worktree label: `goal044_krk_route_selectivity_metrics_plan`
- base commit before Goal 070C revalidation: `f84756e`

## Current State Summary

KORA now has a public-safe first-value path and an evidence package that covers:

- deterministic-heavy benchmark evidence.
- route-selectivity metrics over four public matrix profiles.
- runtime-integrated dry-run route evaluation.
- bounded provider-path validation.
- bounded H100 subset measurement.
- repo-owned bounded H100 harness measurement.
- expanded H100 representativeness measurement.
- baseline equivalence and output-fidelity evaluation.
- install-revalidated local first-value CLI workflow.
- reusable Project Operating System templates, prompts, and adoption standard.
- validated Project Operating System continuation path for KORA.

Current status is evidence-centered and local-first. It is not production-readiness evidence.

## Recent Goal History

This is a sufficient recent history backfill, not a complete reconstruction.

| Goal | Public result | Primary artifact |
| --- | --- | --- |
| Goal 044 | Created the active KRK route-selectivity planning branch and aligned the worktree around KRK/KORA Core evidence work. | [KRK route-selectivity metrics implementation plan](docs/implementation/krk-route-selectivity-metrics-implementation-plan-v0.md) |
| Goal 045 | Broke route-selectivity metrics implementation into scoped evaluator, fixture, output, and validation tasks. | [KRK Goal 045 task breakdown](docs/implementation/krk-goal045-task-breakdown-v0.md) |
| Goal 046 | Refreshed July 1 readiness after route-selectivity evidence planning and early implementation. | [KRK July 1 readiness refresh](docs/reports/krk-july1-readiness-refresh-v0.md) |
| Goal 050 | Added bounded H100 routed-subset measurement for the public matrix GPU-selected items. | [KRK bounded H100 evaluation](docs/evidence/krk-bounded-h100-evaluation-v0.md) |
| Goal 053 | Added runtime-integrated dry-run route evaluation over the public matrix profiles. | [KRK runtime-integrated route evaluation](docs/evidence/krk-runtime-integrated-route-evaluation-v0.md) |
| Goal 054 | Expanded bounded provider-routed validation to a 12-call bounded public-safe sample. | [KRK expanded provider-routed validation](docs/evidence/krk-expanded-provider-routed-validation-v0.md) |
| Goal 058C | Added a repo-owned bounded H100 harness and measured 24 fixture-derived GPU-routed operations. | [KRK Goal 058C H100 bounded execution](docs/reports/krk-goal058c-h100-bounded-execution-v0.md) |
| Goal 059 | Measured expanded H100 representativeness with 100 public fixture-derived operations. | [KRK Goal 059 expanded H100 representativeness](docs/reports/krk-goal059-expanded-h100-representativeness-v0.md) |
| Goal 060 | Added baseline equivalence and output-fidelity evaluation over public fixtures. | [KRK Goal 060 output fidelity](docs/reports/krk-goal060-baseline-equivalence-output-fidelity-v0.md) |
| Goal 070A | Added one-command public-safe five-minute first-value workflow. | [KRK Goal 070A five-minute first value](docs/reports/krk-goal070a-five-minute-first-value-v0.md) |
| Goal 070B | Added official `kora inspect`, `kora compare`, `kora run`, and `kora report` CLI surface. | [KRK Goal 070B official CLI surface](docs/reports/krk-goal070b-official-cli-surface-v0.md) |
| Goal 070C | Validated and later revalidated the editable-install first-value CLI path in a clean macOS/Linux-style environment. | [KRK Goal 070C first-value install packaging](docs/reports/krk-goal070c-first-value-install-packaging-v0.md) |
| Goal 071 | Added this project breadcrumb and documentation operating standard. | [KRK Goal 071 project breadcrumb standard](docs/reports/krk-goal071-project-breadcrumb-standard-v0.md) |
| Goal 072 | Extracted the breadcrumb and review-hub pattern into a reusable Project Operating System package. | [KRK Goal 072 project operating system extraction](docs/reports/krk-goal072-project-operating-system-extraction-v0.md) |
| Goal 073 | Validated KORA's Project Operating System as a self-contained continuation surface and refined the templates. | [KRK Goal 073 project operating system validation](docs/reports/krk-goal073-project-operating-system-validation-v0.md) |
| Goal 070C refresh | Revalidated package entrypoint, command help, and end-to-end installed first-value CLI path after Project Operating System adoption. | [KRK Goal 070C first-value install packaging](docs/reports/krk-goal070c-first-value-install-packaging-v0.md) |

## Evidence Index

Primary evidence package:

- [KRK evidence package v0](docs/evidence/krk-evidence-package-v0.md)
- [KRK performance table v0](docs/evidence/krk-performance-table-v0.md)
- [KRK July 1 missing evidence register v0](docs/evidence/krk-july1-missing-evidence-register-v0.md)

Generated summaries:

- [Generated Goal 070C first-value install packaging summary](docs/evidence/generated/krk-goal070c-first-value-install-packaging-summary-v0.md)
- [Generated Goal 070B official CLI surface summary](docs/evidence/generated/krk-goal070b-official-cli-surface-summary-v0.md)
- [Generated Goal 070A five-minute first-value summary](docs/evidence/generated/krk-goal070a-five-minute-first-value-summary-v0.md)
- [Generated Goal 060 output fidelity summary](docs/evidence/generated/krk-goal060-output-fidelity-summary-v0.md)
- [Generated Goal 059 expanded H100 representativeness summary](docs/evidence/generated/krk-goal059-expanded-h100-representativeness-summary-v0.md)
- [Generated Goal 058C H100 bounded execution summary](docs/evidence/generated/krk-goal058c-h100-bounded-execution-summary-v0.md)
- [Generated runtime-integrated route evaluation](docs/evidence/generated/krk-runtime-integrated-route-evaluation-v0.md)
- [Generated expanded provider-routed validation summary](docs/evidence/generated/krk-expanded-provider-routed-validation-summary-v0.md)
- [Generated H100 bounded summary](docs/evidence/generated/krk-h100-bounded-summary-v0.md)

## Report Index

Current reviewer path:

- [KORA five-minute first-value quickstart](docs/quickstart-five-minute-first-value.md)
- [KRK Goal 073 project operating system validation](docs/reports/krk-goal073-project-operating-system-validation-v0.md)
- [Project Operating System](docs/project-operating-system/README.md)
- [KRK Goal 070C first-value install packaging](docs/reports/krk-goal070c-first-value-install-packaging-v0.md)
- [KRK Goal 070B official CLI surface](docs/reports/krk-goal070b-official-cli-surface-v0.md)
- [KRK Goal 070A five-minute first value](docs/reports/krk-goal070a-five-minute-first-value-v0.md)

Current evidence path:

- [Project Operating Standard v0](docs/project-operating-system/project-operating-standard-v0.md)
- [Project initialization prompt](docs/project-operating-system/prompts/project-initialization-prompt.md)
- [Project gap analysis prompt](docs/project-operating-system/prompts/project-gap-analysis-prompt.md)
- [Project documentation refresh prompt](docs/project-operating-system/prompts/project-doc-refresh-prompt.md)
- [KRK Goal 060 baseline equivalence and output fidelity](docs/reports/krk-goal060-baseline-equivalence-output-fidelity-v0.md)
- [KRK Goal 059 expanded H100 representativeness](docs/reports/krk-goal059-expanded-h100-representativeness-v0.md)
- [KRK Goal 058C H100 bounded execution](docs/reports/krk-goal058c-h100-bounded-execution-v0.md)
- [KRK July 1 RC decision package](docs/reports/krk-july1-rc-decision-package-v0.md)
- [KRK July 1 RC risk register](docs/reports/krk-july1-rc-risk-register-v0.md)

## Claim Boundary Summary

Supported:

- KORA makes AI workloads routable.
- KRK is a deterministic-first routing kernel inside KORA Core.
- KRK can route public fixture workloads across deterministic, cache, CPU, provider, GPU, and fallback paths.
- KORA has a public-safe first-value CLI path using `kora inspect`, `kora compare`, `kora run`, and `kora report`.
- Current evidence supports bounded statements about route selectivity, dry-run runtime integration, provider-path validation, bounded H100 execution, expanded H100 representativeness, and fixture-derived output fidelity.
- KORA has reusable public-safe Project Operating System templates for breadcrumbs, review hubs, ADRs, reports, evidence, claim registries, bootstrap checklists, and project prompts.

Not supported:

- production readiness.
- production cost reduction.
- customer savings.
- energy reduction.
- broad workload superiority.
- real API/GPU cost reduction.
- provider superiority.
- H100 superiority.
- replacement of model serving, provider routing, or GPU serving systems.

## Current CLI Surface

First-value CLI:

```bash
kora inspect
kora compare
kora run
kora report --json-out /tmp/kora-first-value.json --md-out /tmp/kora-first-value.md
```

Module form:

```bash
python3 -m kora inspect
python3 -m kora compare
python3 -m kora run
python3 -m kora report --json-out /tmp/kora-first-value.json --md-out /tmp/kora-first-value.md
```

Compatibility wrapper:

```bash
python3 scripts/kora_five_minute_demo.py --json-out /tmp/kora-first-value.json --md-out /tmp/kora-first-value.md
```

## Current First-Value Path

Use [KORA five-minute first-value quickstart](docs/quickstart-five-minute-first-value.md).

Expected public fixture result:

- total fixture items: `18`
- dry-run execution success rate: `1.0000`
- unsafe misroute rate: `0.0000`
- acceptable output rate: `1.0000`
- exact output matches: `17`
- structured-equivalent output matches: `1`
- degraded outputs: `0`
- failed outputs: `0`

## Current Risks

- Evidence remains fixture-derived and bounded.
- Runtime-integrated route evaluation is dry-run unless a later Goal adds live execution.
- Provider validation is bounded and aggregate-only.
- H100 measurements are bounded and do not establish H100 superiority.
- Output fidelity is deterministic rule-based over public fixtures, not live semantic judging.
- Native Windows and WSL-specific first-value install validation are deferred.
- Project Operating System has been validated on KORA, but has not yet been applied to a second project.

## Remaining Evidence Gaps

- broader workload representativeness.
- live semantic or human-graded output-quality validation.
- production-like workload proof, if a public-safe methodology is later approved.
- broader provider validation without exposing raw responses or private metadata.
- larger H100 samples that remain bounded and public-safe.
- published package and wheel validation.
- applying the Project Operating System to a second project and verifying the templates work outside KORA.

## Recommended Next Goals

1. Goal 074 - Apply Project Operating System To Permea.
2. Goal 075 - Public Reviewer Packet From Review Hub.
3. Goal 076 - Wheel and Source Distribution Smoke Validation.
4. Goal 077 - Broader Public Workload Coverage Plan.

## How To Resume With ChatGPT

Paste a new Goal with this instruction:

```text
Start by reading OPEN_THIS_FIRST.md and REVIEW_HUB.md.
Use the active branch goal044_krk_route_selectivity_metrics_plan.
Keep public/private and claim boundaries from REVIEW_HUB.md.
Update OPEN_THIS_FIRST.md and REVIEW_HUB.md before committing unless explicitly exempted.
```

## How To Resume With Codex

Use this work sequence:

1. Verify KORA identity and branch.
2. Read [OPEN_THIS_FIRST.md](OPEN_THIS_FIRST.md) as the single source of human continuation.
3. Read this file as the detailed second stop.
4. Read only the linked reports/evidence relevant to the new Goal.
5. Implement the scoped change.
6. Run validation.
7. Update [OPEN_THIS_FIRST.md](OPEN_THIS_FIRST.md) and this file.
8. Commit only public-safe files.

## Maintenance Rule

Every completed Goal must update:

- [OPEN_THIS_FIRST.md](OPEN_THIS_FIRST.md)
- [REVIEW_HUB.md](REVIEW_HUB.md)

Exemptions must be explicit in the Goal prompt or final report. This rule exists so reviewers, owners, future sessions, and contributors can quickly reconstruct the current state without reading every historical report.
