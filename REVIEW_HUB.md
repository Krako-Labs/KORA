# KORA Review Hub

Status: current public review and continuation hub.

Last updated by: Goal 083B.

## Project Identity

KORA makes AI workloads routable.

KRK means KORA Routing Kernel. KRK is the deterministic-first execution routing kernel inside KORA Core. It routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

## Public Truth

- repository: `https://github.com/Krako-Labs/KORA`
- public truth branch: `origin/main`
- active evidence branch: `goal083b_getkora_distribution_strategy`
- worktree label: `goal083b_getkora_distribution_strategy`
- branch pushed to: not pushed in this worktree
- open PR: none for Goal 083B
- base commit: `09c28f15413e9c3ed8498a046f5352eb0ad7b791`

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
- distribution strategy documents PyPI `kora` collision, source-install current path, and planned future PyPI distribution name `getkora`.
- deterministic classification example pack with KORA `TaskGraph` execution across support-ticket routing, issue triage, incident severity routing, document type routing, and log/event classification.
- KORA Doctor first-value developer example with KORA `TaskGraph` execution, deterministic candidate/provider-needed candidate inspection, route rationale, counters, and next-step recommendations.
- KORA Doctor report pack with four bundled offline workloads, aggregate report mode, and a README refresh proposal for examples-driven routing/control positioning.
- first-class `kora doctor` CLI command for offline single-workload and aggregate Doctor reports.
- README and documentation index now present KORA as an AI Workload Control Layer with examples-first onboarding and explicit safe claim boundaries.
- reusable Project Operating System templates, prompts, and adoption standard.
- validated Project Operating System continuation path for KORA.
- public-safe PR readiness packet with classification `READY_FOR_PR_WITH_CAVEATS`.
- PR #229 is open against `main`; initial GitHub state was `MERGEABLE` with CI queued.

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
| Goal 074 | Prepared PR readiness packet and PR draft body for the integrated KRK evidence and first-value branch. | [KRK Goal 074 PR readiness merge packet](docs/reports/krk-goal074-pr-readiness-merge-packet-v0.md) |
| Goal 075 | Pushed the branch and opened PR #229 against `main`; no merge, tag, or release was created. | [KRK Goal 075 PR open](docs/reports/krk-goal075-pr-open-v0.md) |
| Goal 081A | Added a deterministic classification example pack using KORA `TaskGraph` execution across five synthetic routing/classification scenarios. | [Goal 081A deterministic classification expansion pack](docs/reports/goal081a_deterministic_classification_expansion_pack.md) |
| Goal 082 | Added an offline KORA Doctor example that inspects a synthetic workload and explains deterministic versus provider-needed candidates without provider calls. | [Goal 082 KORA Doctor example](docs/reports/goal082_kora_doctor_example.md) |
| Goal 082A | Expanded KORA Doctor into a report pack across four offline workloads and added a README refresh proposal. | [Goal 082A KORA Doctor report pack](docs/reports/goal082a_kora_doctor_report_pack.md) |
| Goal 082B | Repositioned README and docs navigation around KORA as an AI Workload Control Layer while preserving current evidence boundaries. | [Goal 082B narrative repositioning](docs/reports/goal082b_narrative_repositioning.md) |
| Goal 083 | Promoted KORA Doctor into a first-class offline CLI command for single-workload and aggregate workload-control reports. | [Goal 083 KORA Doctor CLI](docs/reports/goal083_kora_doctor_cli.md) |
| Goal 083B | Documented the `getkora` future distribution strategy after verifying the PyPI `kora` collision and current source-install path. | [Goal 083B getkora distribution strategy](docs/reports/goal083b_getkora_distribution_strategy.md) |

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

- [Goal 082B narrative repositioning](docs/reports/goal082b_narrative_repositioning.md)
- [Goal 083B getkora distribution strategy](docs/reports/goal083b_getkora_distribution_strategy.md)
- [getkora distribution strategy](docs/packaging/getkora_distribution_strategy.md)
- [Goal 083 KORA Doctor CLI](docs/reports/goal083_kora_doctor_cli.md)
- [KORA Workload Control Layer](docs/vision/kora_workload_control_layer.md)
- [Goal 082A KORA Doctor report pack](docs/reports/goal082a_kora_doctor_report_pack.md)
- [Goal 082A README refresh proposal](docs/reports/goal082a_readme_refresh_proposal.md)
- [Goal 082 KORA Doctor example](docs/reports/goal082_kora_doctor_example.md)
- [KORA Doctor README](examples/kora_doctor/README.md)
- [Goal 081A deterministic classification expansion pack](docs/reports/goal081a_deterministic_classification_expansion_pack.md)
- [Deterministic classification example pack README](examples/deterministic_classification/README.md)
- [KORA five-minute first-value quickstart](docs/quickstart-five-minute-first-value.md)
- [KRK Goal 075 PR open](docs/reports/krk-goal075-pr-open-v0.md)
- [KRK Goal 074 PR readiness merge packet](docs/reports/krk-goal074-pr-readiness-merge-packet-v0.md)
- [KRK Goal 074 PR draft body](docs/reports/krk-goal074-pr-draft-body-v0.md)
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
- KORA can be described as an AI Workload Control Layer in the current examples-first public narrative.
- KRK is a deterministic-first routing kernel inside KORA Core.
- KRK can route public fixture workloads across deterministic, cache, CPU, provider, GPU, and fallback paths.
- KORA has a public-safe first-value CLI path using `kora inspect`, `kora compare`, `kora run`, and `kora report`.
- KORA has a deterministic classification example pack where KORA routes `21` of `32` synthetic sample classification tasks to deterministic handlers, avoiding simulated provider/model invocation for those sample tasks while making `0` provider calls.
- KORA has an offline Doctor example where KORA Doctor identifies deterministic candidates and provider-needed candidates in a sample workload without making provider calls.
- KORA has an offline Doctor report pack where KORA Doctor identifies deterministic candidates and provider-needed candidates across four bundled sample workloads without making provider calls.
- KORA has a first-class `kora doctor` CLI command for running the same offline Doctor inspection over sample workload JSON files and bundled workload directories.
- KORA's planned future PyPI distribution package name is `getkora`; current latest-feature testing requires source install from the repository.
- Current evidence supports bounded statements about route selectivity, dry-run runtime integration, provider-path validation, bounded H100 execution, expanded H100 representativeness, and fixture-derived output fidelity.
- KORA has reusable public-safe Project Operating System templates for breadcrumbs, review hubs, ADRs, reports, evidence, claim registries, bootstrap checklists, and project prompts.

Not supported:

- production readiness.
- model replacement.
- production diagnostic accuracy from the KORA Doctor example.
- production validation from the deterministic classification example pack.
- production cost reduction.
- automatic cost reduction from the KORA Doctor example.
- production proxy readiness from the KORA Doctor report pack.
- customer savings.
- energy reduction.
- broad workload superiority.
- real API/GPU cost reduction.
- real API-cost proof from the deterministic classification example pack.
- real API-cost proof from the KORA Doctor example.
- benchmark superiority from the deterministic classification example pack.
- benchmark superiority from the KORA Doctor example.
- broad workload superiority from the deterministic classification example pack.
- broad workload superiority from the KORA Doctor example.
- provider superiority.
- H100 superiority.
- replacement of model serving, provider routing, or GPU serving systems.

## Current CLI Surface

First-value CLI:

```bash
# Install from the current repository/source checkout before running these commands.
kora inspect
kora compare
kora run
kora doctor examples/kora_doctor/customer_support_workload.json
kora doctor --all examples/kora_doctor/
kora report --json-out /tmp/kora-first-value.json --md-out /tmp/kora-first-value.md
```

Module form:

```bash
# Install from the current repository/source checkout before running these commands.
python3 -m kora inspect
python3 -m kora compare
python3 -m kora run
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora doctor --all examples/kora_doctor/
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

## Current Deterministic Classification Example Pack

Use [Deterministic classification example pack README](examples/deterministic_classification/README.md).

Quick run:

```bash
python3 examples/deterministic_classification/run.py
```

Structured run:

```bash
python3 examples/deterministic_classification/run.py \
  --json-out /tmp/kora_goal081a_deterministic_classification_pack.json \
  --report-md /tmp/kora_goal081a_deterministic_classification_pack.md
```

KORA example runner:

```bash
python3 -m kora run deterministic_classification -- \
  --json-out /tmp/kora_goal081a_deterministic_classification_pack.json \
  --report-md /tmp/kora_goal081a_deterministic_classification_pack.md
```

Expected aggregate counters:

- total tasks: `32`
- deterministic routes: `21`
- provider-needed routes: `11`
- avoided provider invocations in this example pack: `21`
- provider calls actually made: `0`

Boundary: these counters describe only the synthetic example-pack surface. They do not prove production cost reduction, real API-cost reduction, benchmark superiority, broad workload superiority, or production validation.

## Current KORA Doctor Example

Use [KORA Doctor README](examples/kora_doctor/README.md).

Quick run:

```bash
python3 examples/kora_doctor/run.py
```

Structured run:

```bash
python3 examples/kora_doctor/run.py \
  --json-out /tmp/kora_doctor_example.json \
  --report-md /tmp/kora_doctor_example.md
```

KORA example runner:

```bash
python3 -m kora run kora_doctor
```

Expected counters:

- total tasks: `7`
- deterministic candidates: `4`
- provider-needed candidates: `3`
- avoided provider invocations in this offline example: `4`
- provider calls actually made: `0`

Boundary: this is a first-value developer example over synthetic data. It does not prove production diagnostic accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.

## Current KORA Doctor Report Pack

Use [KORA Doctor README](examples/kora_doctor/README.md).

Aggregate run:

```bash
python3 examples/kora_doctor/run.py --all \
  --json-out /tmp/kora_doctor_report_pack.json \
  --report-md /tmp/kora_doctor_report_pack.md
```

Expected aggregate counters:

- workload count: `4`
- total tasks: `25`
- deterministic candidates: `16`
- provider-needed candidates: `9`
- avoided provider invocations in these offline samples: `16`
- provider calls actually made: `0`

Boundary: this is an offline synthetic report pack. It does not prove production diagnostic accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, broad workload superiority, or production proxy readiness.

## Current Narrative Positioning

Current public README positioning:

- KORA is an AI Workload Control Layer.
- Many AI workflow tasks are classification, validation, routing, policy, cache reuse, workflow control, or deterministic processing.
- KORA helps determine what should reach a model, what does not need a model, and how work should move through an AI system.
- KORA Doctor and deterministic classification examples are the fastest first-value surfaces.

Boundary: this is positioning grounded in current examples and evidence. It does not introduce new technical claims, production readiness claims, model replacement claims, automatic savings claims, or superiority claims.

## Current Risks

- Evidence remains fixture-derived and bounded.
- Runtime-integrated route evaluation is dry-run unless a later Goal adds live execution.
- Provider validation is bounded and aggregate-only.
- H100 measurements are bounded and do not establish H100 superiority.
- Output fidelity is deterministic rule-based over public fixtures, not live semantic judging.
- The deterministic classification example pack is intentionally synthetic and small; broader workload representativeness remains unproven.
- The KORA Doctor example is synthetic and does not inspect arbitrary repositories or prove diagnostic accuracy.
- The KORA Doctor report pack is examples-driven and should not be presented as production proxy readiness.
- Native Windows and WSL-specific first-value install validation are deferred.
- Project Operating System has been validated on KORA, but has not yet been applied to a second project.
- PR readiness classification is `READY_FOR_PR_WITH_CAVEATS` because the branch is large and evidence remains bounded.
- PR #229 needs CI completion and review-gate validation before any merge.

## Remaining Evidence Gaps

- broader workload representativeness.
- live semantic or human-graded output-quality validation.
- production-like workload proof, if a public-safe methodology is later approved.
- broader provider validation without exposing raw responses or private metadata.
- larger H100 samples that remain bounded and public-safe.
- published package and wheel validation.
- applying the Project Operating System to a second project and verifying the templates work outside KORA.

## Recommended Next Goals

1. Goal 084 - Public reviewer walkthrough and example catalog refresh.
2. Goal 085 - Contributor issue seed for examples-first onboarding.
3. Goal 086 - Contributor issue seed for first-value examples.
4. Goal 087 - Wheel and source distribution smoke validation.

## How To Resume With ChatGPT

Paste a new Goal with this instruction:

```text
Start by reading OPEN_THIS_FIRST.md and REVIEW_HUB.md.
Use the active branch goal083_kora_doctor_cli.
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
