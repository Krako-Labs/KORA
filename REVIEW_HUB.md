# KORA Review Hub

Status: current public review and continuation hub.

Last updated by: Goal 099.

## Project Identity

KORA makes AI workloads routable.

KRK means KORA Routing Kernel. KRK is the deterministic-first execution routing kernel inside KORA Core. It routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

## Public Truth

- repository: `https://github.com/Krako-Labs/KORA`
- public truth branch: `origin/main`
- active verification branch: `goal099-ai-champion-h100-server-run`
- worktree label: `goal099-ai-champion-h100-server-run`
- branch pushed to: `origin/goal099-ai-champion-h100-server-run`
- open PR: #250
- base commit: `76c43572c3f636024356c4f722acde9433d713f9`

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
- public first-run acceptance testing covers README-only onboarding, fresh source install, KORA Doctor, deterministic classification, and PyPI collision wording.
- OpenAI-compatible proxy example with offline OpenAI-style chat request fixtures, KORA deterministic routing, local cache reuse, provider-needed fallback labels, and `0` provider calls.
- reusable OpenAI-style proxy demo module and first-class `kora proxy-demo` CLI command for running the offline proxy/control path over sample request JSON.
- offline RAG routing example with exact deterministic answers, local cache reuse, retrieval-needed labels over a small offline corpus, provider-needed fallback labels, and `0` provider calls.
- offline agent workflow optimization example with deterministic steps, cache reuse, tool-needed local actions, provider-needed fallback labels, and `0` provider calls.
- offline cache reuse example with first-time deterministic handling, repeated exact and semantic cache hits, provider-needed fallback labels, and `0` provider calls.
- deterministic classification example pack with KORA `TaskGraph` execution across support-ticket routing, issue triage, incident severity routing, document type routing, and log/event classification.
- KORA Doctor first-value developer example with KORA `TaskGraph` execution, deterministic candidate/provider-needed candidate inspection, route rationale, counters, and next-step recommendations.
- KORA Doctor report pack with four bundled offline workloads, aggregate report mode, and a README refresh proposal for examples-driven routing/control positioning.
- first-class `kora doctor` CLI command for offline single-workload and aggregate Doctor reports.
- README and documentation index now present KORA as an AI Workload Control Layer with examples-first onboarding and explicit safe claim boundaries.
- Goal 091 compressed README into a focused landing page with a source quick start, flagship examples table, and short claim boundaries.
- Goal 091B replaced selected public landing and index documents exactly and was merged into `origin/main` at `2972973d732624353bd722d648886eed4d6d9e6c`.
- Goal 092 audited the public repository surface and identified remaining alignment work for GitHub metadata, root files, examples grouping, and docs navigation without changing settings or moving files.
- Goal 093A prepared a metadata change approval packet for repository description and topics without changing repository settings.
- Goal 093B applied the approved GitHub repository description and topics metadata update; Goal 093C verified and documented that repository metadata is now aligned with the README around AI Workload Control Layer positioning.
- Goal 094 adds short orientation notes to older root strategic documents without moving files or deleting historical content.
- Goal 095 organizes the public examples surface at the README/guide level without moving example directories.
- Goal 096 proposes documentation navigation buckets and candidate archive buckets without moving, archiving, renaming, or deleting files.
- Group 097 cleaned up Goal 096 continuation state and audited H100 evidence inventory/gaps.
- Goal 098 prepared controlled CPU/non-GPU and GPU/H100 evidence regeneration on the AI Champion H100 server, with local no-CUDA status recorded as `not_run`.
- Goal 099 executed the Goal 098 server-run packet through SSH remote execution on the AI Champion H100 server, separating CPU/non-GPU and bounded GPU/H100 paths.
- reusable Project Operating System templates, prompts, and adoption standard.
- validated Project Operating System continuation path for KORA.
- no repository settings should be changed further without explicit owner approval.
- current recommended next step is reviewing the Goal 099 evidence package and deciding whether to refresh broader evidence indexes. Documentation movement remains optional only after later explicit Albert approval.

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
| Goal 083C | Ran public first-run acceptance testing over README onboarding, fresh source install, KORA Doctor, deterministic classification, and PyPI collision wording. | [Goal 083C public first-run acceptance test](docs/reports/goal083c_public_first_run_acceptance_test.md) |
| Goal 084 | Added an offline OpenAI-compatible proxy example that routes OpenAI-style sample requests through KORA deterministic handling, cache reuse, or provider-needed fallback. | [Goal 084 OpenAI-compatible proxy example](docs/reports/goal084_openai_compatible_proxy_example.md) |
| Goal 085 | Promoted the OpenAI-style proxy demo into reusable module logic and a first-class offline `kora proxy-demo` CLI command. | [Goal 085 OpenAI proxy reusable module and CLI](docs/reports/goal085_openai_proxy_reusable_module_cli.md) |
| Goal 086 | Added an offline RAG routing example that routes sample queries across deterministic, cache, retrieval-needed, and provider-needed paths without provider calls. | [Goal 086 RAG routing example](docs/reports/goal086_rag_routing_example.md) |
| Goal 087 | Added an offline agent workflow optimization example that routes sample workflow steps across deterministic, cache, tool-needed, and provider-needed paths without provider calls. | [Goal 087 agent workflow optimization example](docs/reports/goal087_agent_workflow_optimization_example.md) |
| Goal 088 | Added an offline cache reuse example that routes repeated sample requests to cache hits and marks ambiguous/open-ended requests as provider-needed without provider calls. | [Goal 088 cache reuse example](docs/reports/goal088_cache_reuse_example.md) |
| Goal 091 | Compressed README into a focused public landing page while preserving source-install guidance, flagship examples, architecture diagram, and claim boundaries. | [Goal 091 README compression](docs/reports/goal091_readme_compression.md) |
| Goal 092 | Audited the post-replacement public repository surface and proposed staged alignment work for metadata, root structure, examples, and docs navigation. | [Goal 092 repository public surface alignment audit](docs/reports/goal092_repository_public_surface_alignment_audit.md) |
| Goal 093A | Prepared the metadata change approval packet for repository description and topics without applying settings changes. | [Goal 093A metadata change approval packet](docs/reports/goal093a_metadata_change_approval_packet.md) |
| Goal 093C | Verified the post-change GitHub metadata readback after Goal 093B and documented that repository metadata now matches the README positioning. | [Goal 093C metadata update post-change verification](docs/reports/goal093c_metadata_update_postchange_verification.md) |
| Goal 094 | Added current-orientation notes to older root strategic documents while preserving historical content and paths. | [Goal 094 root orientation stubs](docs/reports/goal094_root_orientation_stubs.md) |
| Goal 095 | Organized the public examples surface at the README/guide level and proposed future grouping without moving example paths. | [Goal 095 public examples directory organization proposal](docs/reports/goal095_public_examples_directory_organization_proposal.md) |
| Goal 096 | Proposed documentation navigation buckets and candidate archive buckets without moving, archiving, renaming, or deleting files. | [Goal 096 documentation navigation and archive-bucket proposal](docs/reports/goal096_documentation_navigation_archive_bucket_proposal.md) |
| Group 097 | Cleaned up Goal 096 continuation state and audited H100 evidence inventory/gaps without moving files or making new H100 claims. | [Group 097 H100 evidence inventory and gap audit](docs/reports/group097_h100_evidence_inventory_gap_audit.md) |
| Goal 098 | Prepared controlled CPU/non-GPU and GPU/H100 evidence regeneration packet; local no-CUDA status is `not_run` and no fresh H100 execution occurred. | [Goal 098 controlled CPU/GPU evidence regeneration](docs/reports/goal098_controlled_cpu_gpu_evidence_regeneration.md) |
| Goal 099 | Executed the Goal 098 server-run packet through SSH remote execution on the AI Champion H100 server with aggregate CPU/non-GPU and bounded H100 summaries. | [Goal 099 AI Champion H100 server run](docs/reports/goal099_ai_champion_h100_server_run.md) |

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
- [Generated Goal 098 CPU/non-GPU controlled summary](docs/evidence/generated/goal098_cpu_nongpu_controlled_summary.md)
- [Generated Goal 098 H100 controlled summary](docs/evidence/generated/goal098_h100_controlled_summary.md)
- [Generated Goal 099 CPU/non-GPU AI Champion summary](docs/evidence/generated/goal099_cpu_nongpu_ai_champion_summary.md)
- [Generated Goal 099 H100 AI Champion summary](docs/evidence/generated/goal099_h100_ai_champion_summary.md)

## Report Index

Current reviewer path:

- [Goal 099 AI Champion H100 server run](docs/reports/goal099_ai_champion_h100_server_run.md)
- [Goal 098 controlled CPU/GPU evidence regeneration](docs/reports/goal098_controlled_cpu_gpu_evidence_regeneration.md)
- [Group 097 H100 evidence inventory and gap audit](docs/reports/group097_h100_evidence_inventory_gap_audit.md)
- [Goal 096 documentation navigation and archive-bucket proposal](docs/reports/goal096_documentation_navigation_archive_bucket_proposal.md)
- [Goal 095 public examples directory organization proposal](docs/reports/goal095_public_examples_directory_organization_proposal.md)
- [Example catalog](examples/README.md)
- [KORA example guide](docs/examples/kora_example_guide.md)
- [Goal 094 root orientation stubs](docs/reports/goal094_root_orientation_stubs.md)
- [Goal 093C metadata update post-change verification](docs/reports/goal093c_metadata_update_postchange_verification.md)
- [Goal 093A metadata change approval packet](docs/reports/goal093a_metadata_change_approval_packet.md)
- [Goal 092 repository public surface alignment audit](docs/reports/goal092_repository_public_surface_alignment_audit.md)
- [Goal 091 README compression](docs/reports/goal091_readme_compression.md)
- [Goal 089A README architecture diagram placement](docs/reports/goal089a_readme_architecture_diagram_placement.md)
- [Goal 089 repository hygiene and architecture diagram](docs/reports/goal089_repository_hygiene_and_architecture_diagram.md)
- [Goal 082B narrative repositioning](docs/reports/goal082b_narrative_repositioning.md)
- [Goal 088 cache reuse example](docs/reports/goal088_cache_reuse_example.md)
- [Cache reuse example README](examples/cache_reuse/README.md)
- [Goal 087 agent workflow optimization example](docs/reports/goal087_agent_workflow_optimization_example.md)
- [Agent workflow optimization example README](examples/agent_workflow_optimization/README.md)
- [Goal 086 RAG routing example](docs/reports/goal086_rag_routing_example.md)
- [RAG routing example README](examples/rag_routing/README.md)
- [Goal 085 OpenAI proxy reusable module and CLI](docs/reports/goal085_openai_proxy_reusable_module_cli.md)
- [Goal 084 OpenAI-compatible proxy example](docs/reports/goal084_openai_compatible_proxy_example.md)
- [OpenAI-compatible proxy example README](examples/openai_compatible_proxy/README.md)
- [Goal 083C public first-run acceptance test](docs/reports/goal083c_public_first_run_acceptance_test.md)
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

- [Goal 099 AI Champion H100 server run](docs/reports/goal099_ai_champion_h100_server_run.md)
- [Generated Goal 099 CPU/non-GPU AI Champion summary](docs/evidence/generated/goal099_cpu_nongpu_ai_champion_summary.md)
- [Generated Goal 099 H100 AI Champion summary](docs/evidence/generated/goal099_h100_ai_champion_summary.md)
- [Goal 098 controlled CPU/GPU evidence regeneration](docs/reports/goal098_controlled_cpu_gpu_evidence_regeneration.md)
- [Generated Goal 098 CPU/non-GPU controlled summary](docs/evidence/generated/goal098_cpu_nongpu_controlled_summary.md)
- [Generated Goal 098 H100 controlled summary](docs/evidence/generated/goal098_h100_controlled_summary.md)
- [Group 097 H100 evidence inventory and gap audit](docs/reports/group097_h100_evidence_inventory_gap_audit.md)
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
- KORA has an offline OpenAI-style proxy example where sample chat requests are routed through deterministic handling, local cache reuse, or provider-needed fallback without provider calls.
- KORA has a reusable offline proxy demo module and first-class `kora proxy-demo` CLI command for routing OpenAI-style sample request JSON without provider calls.
- KORA has an offline RAG routing example where sample queries are routed across deterministic, cache, retrieval-needed, and provider-needed paths without provider calls.
- KORA has an offline agent workflow optimization example where sample workflow steps are routed across deterministic, cache, tool-needed, and provider-needed paths without provider calls.
- KORA has an offline cache reuse example where repeated sample requests are routed to cache hits without provider calls and ambiguous/open-ended requests are marked provider-needed.
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
- production RAG readiness from the RAG routing example.
- retrieval accuracy from the RAG routing example.
- production agent readiness from the agent workflow example.
- autonomous agent reliability from the agent workflow example.
- production cache correctness from the cache reuse example.
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
kora proxy-demo examples/openai_compatible_proxy/requests.json
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
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
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

## Remaining Evidence Gaps

- broader workload representativeness.
- live semantic or human-graded output-quality validation.
- production-like workload proof, if a public-safe methodology is later approved.
- broader provider validation without exposing raw responses or private metadata.
- larger H100 samples that remain bounded and public-safe.
- published package and wheel validation.
- applying the Project Operating System to a second project and verifying the templates work outside KORA.

## Recommended Next Goals

1. Goal 100 - Review Goal 099 evidence package and decide whether to refresh the broader public evidence index and local ChatGPT context.
2. Optional documentation movement proposal for one small bucket only after later explicit Albert approval.
3. Broader output-quality or workload-representativeness validation after H100 scope is resolved.

## How To Resume Review

Paste a new Goal with this instruction:

```text
Start by reading OPEN_THIS_FIRST.md and REVIEW_HUB.md.
Use the active branch goal099-ai-champion-h100-server-run for the current verification packet, or create a new scoped branch from origin/main for a new Goal.
Keep public/private and claim boundaries from REVIEW_HUB.md.
Update OPEN_THIS_FIRST.md and REVIEW_HUB.md before committing unless explicitly exempted.
```

## How To Resume Implementation

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
## Goal 091B Review Entry

Review these files for public readability and link integrity:

- `README.md`
- `docs/README.md`
- `examples/README.md`
- `docs/vision/kora_workload_control_layer.md`
- `docs/examples/kora_example_guide.md`
- `docs/reports/goal091b_exact_public_documentation_replacement.md`

Required checks:

- README headings render as separate sections.
- README table renders correctly.
- Package note does not claim `getkora` is published.
- No private/internal terms appear in changed public docs.
