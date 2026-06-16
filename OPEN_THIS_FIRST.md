# Open This First

Status: current public project breadcrumb.

Last updated by: Goal 071.

## Current Status

KORA is a public open-source project for making AI workloads routable. The current public alpha is KRK-oriented: deterministic-first workload routing, local first-value CLI workflows, and bounded public evidence reporting through the KORA Routing Kernel.

Current state:

- route-selectivity evidence exists for four public matrix profiles.
- runtime-integrated dry-run route evaluation exists.
- bounded provider-path validation exists.
- bounded H100 subset, repo-owned H100 harness, and expanded H100 representativeness evidence exist.
- baseline equivalence and output-fidelity evidence exists over public fixtures.
- first-value CLI commands exist for local public-safe onboarding.

## Current Branch

- branch: `goal044_krk_route_selectivity_metrics_plan`
- public truth: `origin/main`
- current commit when this breadcrumb was created: `8c4f178`

## Last Completed Goal

Goal 071 - project breadcrumb and documentation operating standard.

Goal 071 created:

- this root breadcrumb.
- [REVIEW_HUB.md](REVIEW_HUB.md).
- [Project Documentation Operating Standard](docs/runbooks/project-documentation-operating-standard.md).
- [ADR-001 project breadcrumb and review hub standard](docs/adr/ADR-001-project-breadcrumb-and-review-hub-standard.md).

Previous completed technical Goal: Goal 070C - first-value install packaging validation.

Goal 070C validated the editable-install first-value path for macOS/Linux-style environments:

```bash
kora inspect
kora compare
kora run
kora report --json-out /tmp/kora-first-value.json --md-out /tmp/kora-first-value.md
```

Primary report:

- [KRK Goal 071 project breadcrumb standard v0](docs/reports/krk-goal071-project-breadcrumb-standard-v0.md)
- [KRK Goal 070C first-value install packaging v0](docs/reports/krk-goal070c-first-value-install-packaging-v0.md)

## Primary Reports

- [Review hub](REVIEW_HUB.md)
- [KRK evidence package v0](docs/evidence/krk-evidence-package-v0.md)
- [KRK performance table v0](docs/evidence/krk-performance-table-v0.md)
- [KRK Goal 070A five-minute first value v0](docs/reports/krk-goal070a-five-minute-first-value-v0.md)
- [KRK Goal 070B official CLI surface v0](docs/reports/krk-goal070b-official-cli-surface-v0.md)
- [KRK Goal 070C first-value install packaging v0](docs/reports/krk-goal070c-first-value-install-packaging-v0.md)
- [KRK Goal 060 baseline equivalence and output fidelity v0](docs/reports/krk-goal060-baseline-equivalence-output-fidelity-v0.md)
- [KRK Goal 059 expanded H100 representativeness v0](docs/reports/krk-goal059-expanded-h100-representativeness-v0.md)
- [KRK July 1 RC decision package v0](docs/reports/krk-july1-rc-decision-package-v0.md)

## Primary Evidence

- [Generated Goal 070C first-value install packaging summary](docs/evidence/generated/krk-goal070c-first-value-install-packaging-summary-v0.md)
- [Generated Goal 070B official CLI surface summary](docs/evidence/generated/krk-goal070b-official-cli-surface-summary-v0.md)
- [Generated Goal 070A five-minute first-value summary](docs/evidence/generated/krk-goal070a-five-minute-first-value-summary-v0.md)
- [Generated Goal 060 output fidelity summary](docs/evidence/generated/krk-goal060-output-fidelity-summary-v0.md)
- [Generated Goal 059 expanded H100 representativeness summary](docs/evidence/generated/krk-goal059-expanded-h100-representativeness-summary-v0.md)
- [Generated runtime-integrated route evaluation](docs/evidence/generated/krk-runtime-integrated-route-evaluation-v0.md)
- [Generated expanded provider-routed validation summary](docs/evidence/generated/krk-expanded-provider-routed-validation-summary-v0.md)
- [Generated H100 bounded summary](docs/evidence/generated/krk-h100-bounded-summary-v0.md)

## Current Value Proposition

KORA makes AI workloads routable. The current KRK public alpha shows how workload requests can be inspected, compared, routed, run through public-safe dry-run paths, and reported with evidence and claim boundaries before defaulting to provider or GPU execution.

## Recommended Next Goal

Goal 072 - Keep Breadcrumbs Current During PR Readiness.

Recommended scope:

- verify `OPEN_THIS_FIRST.md` and `REVIEW_HUB.md` against the current branch state.
- update the latest completed Goal and commit hash.
- prepare PR readiness without expanding public claims.

## How To Continue

For a reviewer:

1. Read this file.
2. Read [REVIEW_HUB.md](REVIEW_HUB.md).
3. Read [KRK evidence package v0](docs/evidence/krk-evidence-package-v0.md).
4. Run the first-value path from [KORA five-minute first-value quickstart](docs/quickstart-five-minute-first-value.md).

For a future Goal:

1. Verify identity and branch.
2. Read this file and [REVIEW_HUB.md](REVIEW_HUB.md).
3. Do the scoped work.
4. Update this file and [REVIEW_HUB.md](REVIEW_HUB.md) before committing, unless the Goal explicitly exempts breadcrumb updates.
