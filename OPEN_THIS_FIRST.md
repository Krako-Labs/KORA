# Open This First

Status: current public project breadcrumb.

Last updated by: Goal 083.

## Current Status

KORA is a public open-source project for making AI workloads routable. The current public alpha is KRK-oriented: deterministic-first workload routing, local first-value CLI workflows, and bounded public evidence reporting through the KORA Routing Kernel.

Current state:

- route-selectivity evidence exists for four public matrix profiles.
- runtime-integrated dry-run route evaluation exists.
- bounded provider-path validation exists.
- bounded H100 subset, repo-owned H100 harness, and expanded H100 representativeness evidence exist.
- baseline equivalence and output-fidelity evidence exists over public fixtures.
- first-value CLI commands exist and the editable-install path has been revalidated for local public-safe onboarding.
- a deterministic classification example pack exists under `examples/deterministic_classification/`, using KORA `TaskGraph` execution across support-ticket routing, issue triage, incident severity routing, document type routing, and log/event classification.
- a KORA Doctor example exists under `examples/kora_doctor/`, using KORA `TaskGraph` execution to inspect a synthetic workload and explain deterministic candidates, provider-needed candidates, route rationale, counters, and next steps.
- the KORA Doctor example now includes a report pack mode across four bundled offline workloads and a README refresh proposal for examples-driven positioning.
- `kora doctor` is now a first-class CLI command for running the offline Doctor workload-control report against a workload JSON file or all bundled Doctor workloads.
- the public README and docs index now position KORA as an AI Workload Control Layer, with examples-first onboarding and explicit claim boundaries.
- the breadcrumb/review-hub pattern has been extracted into a reusable Project Operating System package and validated on KORA as a continuation surface.
- the active branch has a public-safe PR readiness packet with caveats.
- PR #229 is open for the integrated KRK evidence and first-value branch.

## Current Branch

- branch: `goal083_kora_doctor_cli`
- public truth: `origin/main`
- branch pushed to: not pushed in this worktree
- open PR: none for Goal 083
- base commit: `009f11601161fc1d8944e14f3869309e86239e28`

## Last Completed Goal

Goal 083 - Implement KORA Doctor CLI.

Goal 083 promoted the KORA Doctor example into a first-class CLI command. Users can now run a single offline workload-control report with `python3 -m kora doctor examples/kora_doctor/customer_support_workload.json` or an aggregate bundled report with `python3 -m kora doctor --all examples/kora_doctor/`.

Primary report:

- [Goal 083 KORA Doctor CLI](docs/reports/goal083_kora_doctor_cli.md)

Updated public-facing docs:

- [README](README.md)
- [Documentation index](docs/README.md)
- [KORA Doctor README](examples/kora_doctor/README.md)

Claim boundary: In this offline CLI example, KORA Doctor identifies deterministic candidates and provider-needed candidates in sample workloads without making provider calls. It does not claim production diagnostic accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.

Previous completed Goal: Goal 082B - KORA Narrative Repositioning and README Transformation.

Goal 082B repositioned KORA public documentation around the AI Workload Control Layer narrative. The README now starts from developer-facing workload control, explains why not every task should be treated as a model problem, and foregrounds KORA Doctor plus deterministic classification examples.

Primary report:

- [Goal 082B narrative repositioning](docs/reports/goal082b_narrative_repositioning.md)

New vision document:

- [KORA Workload Control Layer](docs/vision/kora_workload_control_layer.md)

Updated public-facing docs:

- [README](README.md)
- [Documentation index](docs/README.md)
- [Open this first](OPEN_THIS_FIRST.md)
- [Review hub](REVIEW_HUB.md)

Claim boundary: this was a narrative and documentation transformation. It did not add new evidence, production cost reduction proof, broad workload superiority, production readiness, benchmark superiority, automatic savings, or model replacement claims.

Previous completed Goal: Goal 082A - Implement KORA Doctor Report Pack and README Refresh Proposal.

Goal 082A expanded `examples/kora_doctor/` into a report pack with multiple offline sample workloads and aggregate report mode. It also added a README refresh proposal for moving public positioning toward examples-driven routing/control language without overclaiming.

Primary reports:

- [Goal 082A KORA Doctor report pack](docs/reports/goal082a_kora_doctor_report_pack.md)
- [Goal 082A README refresh proposal](docs/reports/goal082a_readme_refresh_proposal.md)

Goal 082A aggregate Doctor counters:

- workload count: `4`
- total tasks: `25`
- deterministic candidates: `16`
- provider-needed candidates: `9`
- avoided provider invocations in these offline samples: `16`
- provider calls actually made: `0`

Narrow evidence wording: In these offline sample workloads, KORA Doctor identifies deterministic candidates and provider-needed candidates without making provider calls.

Claim boundary: this is an offline synthetic report pack. It does not claim production diagnostic accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, broad workload superiority, or production proxy readiness.

Previous completed Goal: Goal 082 - Implement KORA Doctor example.

Goal 082 added a first-value developer example under `examples/kora_doctor/`. The example runs offline, wraps every sample workload item in a KORA `TaskGraph`, and uses the deterministic `doctor_inspect_task` handler to report deterministic candidates, provider-needed candidates, route rationale, summary counters, and next-step recommendations.

Primary report:

- [Goal 082 KORA Doctor example](docs/reports/goal082_kora_doctor_example.md)

Example artifacts:

- [KORA Doctor README](examples/kora_doctor/README.md)
- [KORA Doctor sample workload](examples/kora_doctor/workload.json)
- [KORA Doctor runnable script](examples/kora_doctor/run.py)
- [KORA Doctor expected counters](examples/kora_doctor/expected_counters.json)

Goal 082 counters:

- total tasks: `7`
- deterministic candidates: `4`
- provider-needed candidates: `3`
- avoided provider invocations in this offline example: `4`
- provider calls actually made: `0`

Narrow evidence wording: In this offline example, KORA Doctor identifies deterministic candidates and provider-needed candidates in a sample workload without making provider calls.

Claim boundary: this is a first-value developer example over synthetic data. It does not claim production diagnostic accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.

Previous completed Goal: Goal 081A - Implement Deterministic Classification Expansion Pack.

Goal 081A expanded the Goal 080 support-ticket deterministic classification example into a reusable OSS example pack. The pack runs every sample item through a KORA `TaskGraph` and the deterministic `classify_by_rules` handler, preserving explicit provider-needed fallback cases without making provider/model calls.

Primary report:

- [Goal 081A deterministic classification expansion pack](docs/reports/goal081a_deterministic_classification_expansion_pack.md)

Example artifacts:

- [Deterministic classification example pack README](examples/deterministic_classification/README.md)
- [Scenario datasets](examples/deterministic_classification/datasets/)
- [Runnable pack script](examples/deterministic_classification/run.py)
- [Expected output counters](examples/deterministic_classification/expected_outputs/)

Goal 081A aggregate counters:

- total tasks: `32`
- deterministic routes: `21`
- provider-needed routes: `11`
- avoided provider invocations in this example pack: `21`
- provider calls actually made: `0`

Narrow evidence wording: In this example pack, KORA routes `21` of `32` sample classification tasks to deterministic handlers, avoiding simulated provider/model invocation for those sample tasks.

Claim boundary: this is narrow local synthetic example-pack evidence. It is not production cost reduction proof, real API-cost proof, benchmark superiority evidence, broad workload superiority evidence, or production validation.

Previous completed Goal: Goal 075 - Open KRK evidence and first-value PR.

Goal 075 pushed `goal044_krk_route_selectivity_metrics_plan` and opened PR #229 against `main` using the public-safe Goal 074 draft body. The PR was opened only; it was not merged, tagged, or released.

Primary report:

- [KRK Goal 075 PR open v0](docs/reports/krk-goal075-pr-open-v0.md)
- [KRK Goal 074 PR readiness merge packet v0](docs/reports/krk-goal074-pr-readiness-merge-packet-v0.md)
- [KRK Goal 074 PR draft body v0](docs/reports/krk-goal074-pr-draft-body-v0.md)

PR status at creation:

- PR: [#229](https://github.com/Krako-Labs/KORA/pull/229)
- mergeable: `MERGEABLE`
- merge state: `UNSTABLE` because CI was queued

Previous completed technical Goal: Goal 070C - First-value CLI install and packaging polish revalidation.

Goal 070C revalidated the fresh macOS/Linux-style editable-install first-value path after the Project Operating System updates. The package entrypoint remained registered as `kora = "kora.cli:main"`, and no packaging code change was required.

Goal 070C report and evidence:

- [KRK Goal 070C first-value install packaging v0](docs/reports/krk-goal070c-first-value-install-packaging-v0.md)
- [Generated Goal 070C first-value install packaging summary](docs/evidence/generated/krk-goal070c-first-value-install-packaging-summary-v0.md)

Previous completed documentation Goal: Goal 073 - Project Operating System validation on KORA.

Goal 073 audited whether a new reviewer, planning agent, execution agent, or project owner can continue KORA from this file and `REVIEW_HUB.md` without reading chat history. The audit passed with light refinements to the breadcrumb templates and continuation language.

Goal 073 report:

- [KRK Goal 073 project operating system validation v0](docs/reports/krk-goal073-project-operating-system-validation-v0.md)

Previous completed documentation Goal: Goal 072 - Project Operating System extraction.

Goal 072 extracted the Goal 071 breadcrumb/review-hub pattern into reusable templates, prompts, and a project operating standard:

- [Project Operating System README](docs/project-operating-system/README.md).
- [Project Operating Standard v0](docs/project-operating-system/project-operating-standard-v0.md).
- [Project Operating System templates](docs/project-operating-system/templates/OPEN_THIS_FIRST.template.md).
- [Project Operating System prompts](docs/project-operating-system/prompts/project-initialization-prompt.md).

Previous completed breadcrumb Goal: Goal 071 - project breadcrumb and documentation operating standard.

Primary report:

- [KRK Goal 071 project breadcrumb standard v0](docs/reports/krk-goal071-project-breadcrumb-standard-v0.md)
- [KRK Goal 072 project operating system extraction v0](docs/reports/krk-goal072-project-operating-system-extraction-v0.md)
- [KRK Goal 073 project operating system validation v0](docs/reports/krk-goal073-project-operating-system-validation-v0.md)
- [KRK Goal 070C first-value install packaging v0](docs/reports/krk-goal070c-first-value-install-packaging-v0.md)

## Primary Reports

- [Review hub](REVIEW_HUB.md)
- [Goal 083 KORA Doctor CLI](docs/reports/goal083_kora_doctor_cli.md)
- [Goal 082B narrative repositioning](docs/reports/goal082b_narrative_repositioning.md)
- [KORA Workload Control Layer](docs/vision/kora_workload_control_layer.md)
- [Goal 082A KORA Doctor report pack](docs/reports/goal082a_kora_doctor_report_pack.md)
- [Goal 082A README refresh proposal](docs/reports/goal082a_readme_refresh_proposal.md)
- [Goal 082 KORA Doctor example](docs/reports/goal082_kora_doctor_example.md)
- [KORA Doctor README](examples/kora_doctor/README.md)
- [Goal 081A deterministic classification expansion pack](docs/reports/goal081a_deterministic_classification_expansion_pack.md)
- [Deterministic classification example pack README](examples/deterministic_classification/README.md)
- [Project Operating System](docs/project-operating-system/README.md)
- [KRK Goal 073 project operating system validation v0](docs/reports/krk-goal073-project-operating-system-validation-v0.md)
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

Goal 084 - Public reviewer walkthrough and example catalog refresh.

Recommended scope:

- review the README and KORA Doctor CLI narrative from a fresh visitor perspective.
- verify KORA Doctor CLI, KORA Doctor example, and deterministic classification quick starts.
- refresh contributor-facing example catalog pointers if needed.
- preserve current evidence boundaries and avoid production or superiority claims.

## How To Continue

For a reviewer:

1. Read this file.
2. Read [REVIEW_HUB.md](REVIEW_HUB.md).
3. Read [KRK evidence package v0](docs/evidence/krk-evidence-package-v0.md).
4. Run the first-value path from [KORA five-minute first-value quickstart](docs/quickstart-five-minute-first-value.md).
5. Use [Project Operating System](docs/project-operating-system/README.md) when applying the pattern to another project.

For a future Goal:

1. Verify identity and branch.
2. Read this file and [REVIEW_HUB.md](REVIEW_HUB.md).
3. Do the scoped work.
4. Update this file and [REVIEW_HUB.md](REVIEW_HUB.md) before committing, unless the Goal explicitly exempts breadcrumb updates.
