# Open This First

Status: current public project breadcrumb.

Last updated by: Group 114.

## Current Status

KORA is a public open-source project for making AI workloads routable. The current public alpha is KRK-oriented: deterministic-first workload routing, local first-value CLI workflows, and bounded public evidence reporting through the KORA Routing Kernel.

Current state:

- route-selectivity evidence exists for four public matrix profiles.
- runtime-integrated dry-run route evaluation exists.
- bounded provider-path validation exists.
- bounded H100 subset, repo-owned H100 harness, and expanded H100 representativeness evidence exist.
- baseline equivalence and output-fidelity evidence exists over public fixtures.
- first-value CLI commands exist and the editable-install path has been revalidated for local public-safe onboarding.
- packaging strategy now documents the PyPI `kora` collision and the planned future distribution name `getkora`; latest-feature testing remains source-install from the current repository.
- public first-run acceptance testing has been run against the README/source-install path, KORA Doctor, deterministic classification, and PyPI collision wording.
- an offline OpenAI-compatible proxy example exists under `examples/openai_compatible_proxy/`, showing KORA routing OpenAI-style chat request objects through deterministic handlers, local cache reuse, or provider-needed fallback without provider calls.
- the OpenAI-style proxy demo routing logic is now reusable from `kora.openai_proxy_demo`, and `python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json` runs the same offline no-provider-call path from the first-class CLI.
- an offline RAG routing example exists under `examples/rag_routing/`, showing KORA routing sample queries across deterministic answers, cache hits, retrieval-needed handling, and provider-needed fallback without provider calls.
- an offline agent workflow optimization example exists under `examples/agent_workflow_optimization/`, showing KORA routing sample workflow steps across deterministic, cache, tool-needed, and provider-needed paths without provider calls.
- an offline cache reuse example exists under `examples/cache_reuse/`, showing KORA routing repeated sample requests to cache hits while preserving provider-needed fallback for ambiguous/open-ended requests without provider calls.
- Goal 089 replaced the public workload-control architecture diagram with `docs/assets/kora_workload_control_layer_architecture.svg` and completed a public repository hygiene audit: [Goal 089 repository hygiene and architecture diagram](docs/reports/goal089_repository_hygiene_and_architecture_diagram.md).
- Goal 089A embeds that architecture diagram near the top of the public README and vision doc: [Goal 089A README architecture diagram placement](docs/reports/goal089a_readme_architecture_diagram_placement.md).
- Goal 091 compressed the public README into a focused KORA landing page: [Goal 091 README compression](docs/reports/goal091_readme_compression.md).
- Goal 092 audited the public repository surface after the README replacement and proposed metadata, root, examples, and docs alignment steps without changing repository settings or moving files: [Goal 092 repository public surface alignment audit](docs/reports/goal092_repository_public_surface_alignment_audit.md).
- Goal 093A prepared a metadata change approval packet for the repository description and topics without changing repository settings: [Goal 093A metadata change approval packet](docs/reports/goal093a_metadata_change_approval_packet.md).
- Goal 093B applied the approved GitHub repository description and topics metadata update; Goal 093C verified and documented the readback: [Goal 093C metadata update post-change verification](docs/reports/goal093c_metadata_update_postchange_verification.md).
- Goal 094 adds short orientation notes to older root strategic documents without moving files or deleting historical content: [Goal 094 root orientation stubs](docs/reports/goal094_root_orientation_stubs.md).
- Goal 095 organizes the public examples surface at the README/guide level without moving example directories: [Goal 095 public examples directory organization proposal](docs/reports/goal095_public_examples_directory_organization_proposal.md).
- Goal 096 proposes documentation navigation and candidate archive buckets without moving, archiving, renaming, or deleting files: [Goal 096 documentation navigation and archive-bucket proposal](docs/reports/goal096_documentation_navigation_archive_bucket_proposal.md).
- Group 097 cleaned up Goal 096 continuation state and audited H100 evidence inventory/gaps: [Group 097 H100 evidence inventory and gap audit](docs/reports/group097_h100_evidence_inventory_gap_audit.md).
- Goal 098 prepared controlled CPU/non-GPU and GPU/H100 evidence regeneration on the AI Champion H100 server, with local no-CUDA status recorded as `not_run`: [Goal 098 controlled CPU/GPU evidence regeneration](docs/reports/goal098_controlled_cpu_gpu_evidence_regeneration.md).
- Goal 099 executed the Goal 098 server-run packet through SSH remote execution on the AI Champion H100 server, separating CPU/non-GPU and bounded GPU/H100 paths: [Goal 099 AI Champion H100 server run](docs/reports/goal099_ai_champion_h100_server_run.md).
- a deterministic classification example pack exists under `examples/deterministic_classification/`, using KORA `TaskGraph` execution across support-ticket routing, issue triage, incident severity routing, document type routing, and log/event classification.
- a KORA Doctor example exists under `examples/kora_doctor/`, using KORA `TaskGraph` execution to inspect a synthetic workload and explain deterministic candidates, provider-needed candidates, route rationale, counters, and next steps.
- the KORA Doctor example now includes a report pack mode across four bundled offline workloads and a README refresh proposal for examples-driven positioning.
- `kora doctor` is now a first-class CLI command for running the offline Doctor workload-control report against a workload JSON file or all bundled Doctor workloads.
- the public README and docs index now position KORA as an AI Workload Control Layer, with examples-first onboarding and explicit claim boundaries.
- the breadcrumb/review-hub pattern has been extracted into a reusable Project Operating System package and validated on KORA as a continuation surface.
- current public continuation work is focused on Group 114 first-run CLI smoke validation. Documentation movement remains optional only after later explicit Albert approval.

## Current Branch

- branch: `codex/group114-first-run-cli-smoke-validation`
- public truth: `origin/main`
- branch pushed to: `origin/codex/group114-first-run-cli-smoke-validation`
- open PR: [#266](https://github.com/Krako-Labs/KORA/pull/266)
- base commit: `bbc673d256f005201925051310342fa78c4af4d2`

## Active Goal

Group 114 - First-Run CLI Smoke Validation Expansion.

Group 114 implements `CIL-004` by adding a deterministic local first-run CLI smoke checker over existing offline commands, focused tests, and a public-safe report. It does not implement `CIL-003`, change validation profile registries, publish packages, call providers, require network access, run H100/server work, or expand claims.

Primary report:

- [Group 114 first-run CLI smoke validation](docs/reports/group114_first_run_cli_smoke_validation.md)
- [First-run CLI smoke checker](scripts/check_first_run_cli_smoke.py)
- [First-run CLI smoke tests](tests/test_first_run_cli_smoke.py)
- [Group 113 inner loop applied review and queue hardening](docs/reports/group113_inner_loop_applied_review_queue_hardening.md)
- [Codex medium-risk profile registry checklist](docs/context/CODEX_MEDIUM_RISK_PROFILE_REGISTRY_CHECKLIST.md)
- [Group 112 PR approval and report consistency](docs/reports/group112_pr_approval_and_report_consistency.md)
- [PR approval packet checker](scripts/check_pr_approval_packet.py)
- [Report consistency checker](scripts/check_report_consistency.py)
- [Group 111 validation report control block](docs/reports/group111_validation_report_control_block.md)
- [Bounded local validation report verifier](scripts/verify_bounded_local_validation_report.py)
- [Bounded local validation failure classifier](scripts/classify_bounded_local_validation_failure.py)
- [Group 110 Codex inner loop ownership](docs/reports/group110_codex_inner_loop_ownership.md)
- [Codex inner loop run template](docs/reports/codex_inner_loop_run_template.md)
- [Codex inner loop queue](docs/context/CODEX_INNER_LOOP_QUEUE.md)
- [Codex self-review protocol](docs/context/CODEX_SELF_REVIEW_PROTOCOL.md)
- [Codex risk classification](docs/context/CODEX_RISK_CLASSIFICATION.md)
- [Codex escalation gates](docs/context/CODEX_ESCALATION_GATES.md)
- [Codex approval packet](docs/context/CODEX_APPROVAL_PACKET.md)
- [Codex multi-agent operating model](docs/context/CODEX_MULTI_AGENT_OPERATING_MODEL.md)
- [Goal 109 bounded local validation runner](docs/reports/goal109_bounded_local_validation_runner.md)
- [Goal 108 bounded local test loop](docs/reports/goal108_bounded_local_test_loop.md)
- [Goal 107 long-run test loop protocol](docs/reports/goal107_long_run_test_loop_protocol.md)
- [Long-run test loop protocol](docs/runbooks/long_run_test_loop_protocol.md)
- [Test failure triage checklist](docs/runbooks/test_failure_triage_checklist.md)
- [KORA test loop queue](docs/context/TEST_LOOP_QUEUE.md)
- [Goal 106 fixture quality-check scaffold](docs/reports/goal106_fixture_quality_check_scaffold.md)
- [KORA quality-check seed fixture v0](examples/workloads/kora-quality-check-seed-v0.json)
- [Fixture quality-check evaluator](scripts/evaluate_fixture_quality_checks.py)
- [Goal 105 public-safe output-quality methodology](docs/reports/goal105_public_safe_output_quality_methodology.md)
- [Public-safe output-quality methodology](docs/methodology/public_safe_output_quality_methodology.md)
- [Goal 104 Codex bounded loop protocol](docs/reports/goal104_codex_bounded_loop_protocol.md)
- [Codex bounded loop protocol](docs/runbooks/codex_bounded_loop_protocol.md)
- [KORA claim-boundary checklist](docs/runbooks/kora_claim_boundary_checklist.md)
- [KORA PR completion format](docs/runbooks/kora_pr_completion_format.md)
- [KORA next goal queue](docs/context/NEXT_GOAL_QUEUE.md)
- [Goal 103 representativeness route-only evaluator](docs/reports/goal103_representativeness_route_only_evaluator.md)
- [Goal 102 workload representativeness seed](docs/reports/goal102_workload_representativeness_seed.md)
- [KORA representativeness seed fixture v0](examples/workloads/kora-representativeness-seed-v0.json)

Validation commands:

```bash
python3 scripts/check_markdown_links_goal082b.py
git diff --check
python3 -m pytest
```

Current caveat: Goal 105 is future validation design only. It does not execute output-quality evaluation, make provider calls, run model inference, perform H100/GPU/CUDA/server/remote execution, add output-quality proof, add broader workload representativeness proof, add production proof, or authorize merge, release, publication, repository settings changes, file movement, claim expansion, or local-only source refresh without separate explicit approval.

Current caveat: Goal 106 is a tiny bounded scaffold over a public-safe synthetic fixture. It does not prove output quality, broader workload representativeness, production workload handling, production readiness, production cost reduction, H100/GPU/CPU superiority, customer savings, provider replacement, GPU-serving replacement, or published `getkora`.

Current caveat: Goal 107 is protocol documentation only. It does not execute long-run validation, create background automation, call providers, run model inference, perform H100/GPU/CUDA/server/remote execution, add output-quality proof, add broader workload representativeness proof, add production proof, or authorize merge, release, publication, repository settings changes, file movement, claim expansion, or local-only source refresh without separate explicit approval.

Current caveat: Goal 108 is one bounded local-only validation batch over approved commands. It does not execute provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, production validation, output-quality proof, broader workload representativeness proof, production proof, background automation, merge automation, file movement, release, publication, repository settings changes, or local-only source refresh.

Current caveat: Goal 109 is a bounded local validation runner over approved commands. It does not add production validation, output-quality proof, broader workload representativeness proof, provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, release, publication, repository settings changes, or local-only source refresh.

Current caveat: Group 110 is repo-local operating guidance and validation for that guidance. It does not create production automation, auto-merge, background execution, provider calls, H100/server execution, actual multi-agent execution, or claim expansion.

Current caveat: Group 111 is static validation-report control-block tooling over local JSON reports. It does not execute report commands, auto-repair, schedule background work, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, or prove output quality.

Current caveat: Group 112 validates approval-packet and report/breadcrumb consistency only. It does not call GitHub APIs, approve PRs, merge PRs, close PRs, create issues, execute report commands, auto-repair, create background automation, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, or prove output quality.

Current caveat: Group 113 is operating review and queue hardening only. It does not implement `CIL-003`, change validation profiles, execute report commands, call GitHub APIs, mutate PRs, create issues, auto-repair, create background automation, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, or prove output quality.

Current caveat: Group 114 is local first-run CLI smoke validation only. It does not implement `CIL-003`, change validation profile registries, publish packages, call providers, require network access, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, prove broader workload representativeness, or claim that `getkora` is published.

## Last Completed Goal

Group 113 - Inner Loop Applied Review and Queue Hardening Audit.

Group 113 applied the Group 110-112 operating layer, confirmed the Group 112 checkers pass on the merged Group 112 report, added a medium-risk `CIL-003` checklist, and hardened queue sizing guidance. PR #265 was squash-merged into `origin/main` at `bbc673d256f005201925051310342fa78c4af4d2`.

Primary report:

- [Group 113 inner loop applied review and queue hardening](docs/reports/group113_inner_loop_applied_review_queue_hardening.md)

Claim boundary: Group 113 is operating review and queue hardening only. It does not implement `CIL-003`, change validation profiles, execute report commands, call GitHub APIs, mutate PRs, call providers, run H100/server work, or prove output quality.

Group 112 - PR Approval and Report Consistency Control Block.

Group 112 added deterministic approval-packet and report-consistency checks. PR #264 was squash-merged into `origin/main` at `11232af9027209c0cfd4ae7a5edee79c91d791d4`.

Primary report:

- [Group 112 PR approval and report consistency](docs/reports/group112_pr_approval_and_report_consistency.md)

Claim boundary: Group 112 validates approval-packet and report/breadcrumb consistency only. It does not call GitHub APIs, mutate PRs, execute report commands, call providers, run H100/server work, or prove output quality.

Group 111 - Queue-Driven Validation Report Control Block.

Group 111 added static bounded-local-validation report verification and deterministic failure classification without executing report commands. PR #263 was squash-merged into `origin/main` at `4bb7a4e08b7d644a24b5370e2eeae3194c46e107`.

Primary report:

- [Group 111 validation report control block](docs/reports/group111_validation_report_control_block.md)

Claim boundary: Group 111 is static report-control tooling over local bounded-validation JSON. It does not execute report commands, auto-repair, create background automation, call providers, run H100/server work, or prove output quality.

Group 110 - Codex Inner Loop Ownership with Risk-Gated Self Review.

Group 110 added repo-local operating guidance for Codex-owned bounded inner-loop work: queue selection, validation, repair, self-review, risk classification, escalation gates, approval packets, and PR-open stop behavior. PR #262 was squash-merged into `origin/main` at `a7f5fedc6be534a30818a5b9fc5a877a901f5db7`.

Primary report:

- [Group 110 Codex inner loop ownership](docs/reports/group110_codex_inner_loop_ownership.md)

Claim boundary: Group 110 is repo-local operating guidance and validation for that guidance. It does not create production automation, auto-merge, background execution, provider calls, H100/server execution, actual multi-agent execution, or claim expansion.

Goal 109 - Add Bounded Local Validation Runner.

Goal 109 added a public-safe bounded local validation runner for the `kora-local-core` profile. PR #259 was squash-merged into `origin/main` at `3ea3c9f520fdc70370f28f51a7979b918b0599eb`.

Primary report:

- [Goal 109 bounded local validation runner](docs/reports/goal109_bounded_local_validation_runner.md)

Claim boundary: Goal 109 is a bounded local validation runner over approved commands. It does not prove output quality, broader workload representativeness, production workload handling, production readiness, production cost reduction, H100/GPU/CPU superiority, customer savings, provider replacement, GPU-serving replacement, or published `getkora`.

Goal 107 - Long-Run Test Loop Protocol and Failure Triage.

Goal 107 added a public-safe long-run test loop protocol, failure-triage checklist, and test-loop queue template for future bounded local validation loops. PR #257 was squash-merged into `origin/main` at `7511e3050d4ad33b9274434cf25897da5b1f5406`.

Primary report:

- [Goal 107 long-run test loop protocol](docs/reports/goal107_long_run_test_loop_protocol.md)
- [Long-run test loop protocol](docs/runbooks/long_run_test_loop_protocol.md)
- [Test failure triage checklist](docs/runbooks/test_failure_triage_checklist.md)
- [KORA test loop queue](docs/context/TEST_LOOP_QUEUE.md)

Claim boundary: Goal 107 is protocol documentation only. It does not execute long-run validation, create background automation, call providers, run model inference, perform H100/GPU/CUDA/server/remote execution, add output-quality proof, add broader workload representativeness proof, add production proof, or authorize merge, release, publication, repository settings changes, file movement, claim expansion, or local-only source refresh without separate explicit approval.

Goal 106 - Tiny Public-Safe Fixture-Based Quality-Check Scaffold.

Goal 106 added a tiny public-safe fixture-based quality-check scaffold with deterministic fixture-only checks, aggregate JSON output, and focused tests. PR #256 was squash-merged into `origin/main` at `a2e1164b397fbac0a35186db08348fc80a3fcbab`.

Primary report:

- [Goal 106 fixture quality-check scaffold](docs/reports/goal106_fixture_quality_check_scaffold.md)
- [KORA quality-check seed fixture v0](examples/workloads/kora-quality-check-seed-v0.json)
- [Fixture quality-check evaluator](scripts/evaluate_fixture_quality_checks.py)

Claim boundary: Goal 106 is a tiny bounded scaffold over a public-safe synthetic fixture. It does not prove output quality, broader workload representativeness, production workload handling, production readiness, production cost reduction, H100/GPU/CPU superiority, customer savings, provider replacement, GPU-serving replacement, or published `getkora`.

Goal 105 - Public-Safe Output-Quality Methodology.

Goal 105 added a public-safe methodology for future fixture-derived output-quality validation without executing evaluation or turning Goal 103 route-only counters into output-quality proof. PR #255 was squash-merged into `origin/main` at `c90d5463967394f9cda3cb6a0126e37363f1d95e`.

Primary report:

- [Goal 105 public-safe output-quality methodology](docs/reports/goal105_public_safe_output_quality_methodology.md)
- [Public-safe output-quality methodology](docs/methodology/public_safe_output_quality_methodology.md)

Claim boundary: Goal 105 is future validation design only. It does not execute output-quality evaluation, make provider calls, run model inference, perform H100/GPU/CUDA/server/remote execution, add output-quality proof, add broader workload representativeness proof, add production proof, or authorize merge, release, publication, repository settings changes, file movement, claim expansion, or local-only source refresh without separate explicit approval.

Goal 104 - Codex Bounded Loop Protocol and Claim-Boundary Automation.

Goal 104 added KORA-specific runbooks for semi-autonomous Codex execution with human approval gates, claim-boundary review, PR-open then stop behavior, fix-loop cleanup, merge-gate separation, and local source-refresh after merge. PR #254 was squash-merged into `origin/main` at `2dfcabb2e1949fae12fb41e5d21ae093f3e0802d`.

Primary report:

- [Goal 104 Codex bounded loop protocol](docs/reports/goal104_codex_bounded_loop_protocol.md)
- [Codex bounded loop protocol](docs/runbooks/codex_bounded_loop_protocol.md)
- [KORA claim-boundary checklist](docs/runbooks/kora_claim_boundary_checklist.md)
- [KORA PR completion format](docs/runbooks/kora_pr_completion_format.md)
- [KORA next goal queue](docs/context/NEXT_GOAL_QUEUE.md)

Claim boundary: Goal 104 is protocol documentation only. It does not authorize merge, release, publication, repository settings changes, provider calls, H100/GPU/server execution, file movement, claim expansion, or local-only source refresh without separate explicit approval.

Goal 103 - Representativeness Route-Only Evaluator.

Goal 103 added a route-only evaluator for the Goal 102 public-safe synthetic representativeness seed fixture. It reads the seed, reuses shape-only validation, and emits aggregate public-safe route counters only. PR #253 was squash-merged into `origin/main` at `9d4fff45a448a16c23e2907db68ce68f91e77865`.

Primary report:

- [Goal 103 representativeness route-only evaluator](docs/reports/goal103_representativeness_route_only_evaluator.md)
- [Goal 102 workload representativeness seed](docs/reports/goal102_workload_representativeness_seed.md)
- [KORA representativeness seed fixture v0](examples/workloads/kora-representativeness-seed-v0.json)

Evaluator command:

```bash
python3 scripts/evaluate_representativeness_seed_routes.py
```

Claim boundary: Goal 103 is route-only evidence over a synthetic seed fixture. It does not prove output quality, broad workload representativeness, production readiness, production workload handling, production cost reduction, H100/GPU/CPU superiority, both-GPU active use, multi-GPU scaling, broad workload superiority, customer savings, provider replacement, general GPU-serving replacement, or published `getkora`.

Goal 100 - Review Goal 099 Evidence Package and Evidence Index Decision.

Goal 100 reviewed the merged Goal 099 evidence package and applied a narrow evidence-index refresh after PR #251 was squash-merged into `origin/main` at `5adb19044a697bdb6bfd57b342ba3699efc579c5`.

Primary report:

- [Goal 100 Goal 099 evidence index review](docs/reports/goal100_goal099_evidence_index_review.md)
- [Goal 099 AI Champion H100 server run](docs/reports/goal099_ai_champion_h100_server_run.md)
- [Goal 099 CPU/non-GPU AI Champion summary](docs/evidence/generated/goal099_cpu_nongpu_ai_champion_summary.md)
- [Goal 099 H100 AI Champion summary](docs/evidence/generated/goal099_h100_ai_champion_summary.md)

Claim boundary: Goal 100 is evidence review and narrow index refresh only. Goal 099 remains controlled workload-path execution evidence only; it does not prove both-GPU active use, multi-GPU scaling, H100 superiority, GPU superiority, CPU superiority, production readiness, production benchmark proof, production cost reduction proof, real API-cost proof, real GPU-cost proof, broad workload superiority, energy reduction, customer savings, general GPU-serving replacement, provider replacement, or published `getkora`.

Goal 099 - AI Champion H100 Server Run.

Goal 099 executed the Goal 098 server-run packet through SSH remote execution on the AI Champion H100 server. PR #250 was squash-merged into `origin/main` at `3c3223e01a3a4bc72475ca938c2910053e34c047`.

Primary report:

- [Goal 099 AI Champion H100 server run](docs/reports/goal099_ai_champion_h100_server_run.md)
- [Goal 099 CPU/non-GPU AI Champion summary](docs/evidence/generated/goal099_cpu_nongpu_ai_champion_summary.md)
- [Goal 099 H100 AI Champion summary](docs/evidence/generated/goal099_h100_ai_champion_summary.md)

Claim boundary: Goal 099 is controlled workload-path execution evidence. It does not prove both-GPU active use, multi-GPU scaling, H100 superiority, GPU superiority, CPU superiority, production readiness, production benchmark proof, production cost reduction proof, real API-cost proof, real GPU-cost proof, broad workload superiority, energy reduction, customer savings, provider replacement, general GPU-serving replacement, or published `getkora`.

Previous completed Goal: Goal 098 - Controlled CPU/GPU Evidence Regeneration.

Goal 098 prepared a controlled evidence regeneration packet and recorded local no-CUDA status as `not_run`. PR #249 was squash-merged into `origin/main` at `76c43572c3f636024356c4f722acde9433d713f9`.

Primary report:

- [Goal 098 controlled CPU/GPU evidence regeneration](docs/reports/goal098_controlled_cpu_gpu_evidence_regeneration.md)
- [Goal 098 CPU/non-GPU controlled summary](docs/evidence/generated/goal098_cpu_nongpu_controlled_summary.md)
- [Goal 098 H100 controlled summary](docs/evidence/generated/goal098_h100_controlled_summary.md)

Claim boundary: Goal 098 prepared a server-run packet only. It did not create measured CPU/non-GPU evidence, measured H100 evidence, H100 superiority, GPU superiority, production readiness, production benchmark proof, production cost reduction proof, real API-cost proof, real GPU-cost proof, broad workload superiority, energy reduction, customer savings, or published `getkora` claims.

Previous completed Goal: Group 097 - Documentation Continuation Cleanup and H100 Evidence Inventory.

Group 097 cleaned up Goal 096 continuation state and audited H100 evidence inventory/gaps. PR #248 was squash-merged into `origin/main` at `3df6c8920b74fbaf07eb171075596e44dc25878f`.

Primary report:

- [Group 097 H100 evidence inventory and gap audit](docs/reports/group097_h100_evidence_inventory_gap_audit.md)

Claim boundary: Group 097 was documentation cleanup plus H100 evidence inventory/gap audit only. It did not move, archive, rename, or delete files; create archive directories; change repository settings; create a release; create a tag; create a publication; or add H100 superiority, production readiness, production benchmark proof, production cost reduction proof, real API-cost proof, broad workload superiority, energy reduction, or published `getkora` claims.

Previous completed Goal: Goal 093C - Metadata Update Post-Change Verification.

Goal 093C verified and documented the Goal 093B GitHub repository metadata update. The public README and GitHub About metadata are now aligned around AI Workload Control Layer positioning.

Primary report:

- [Goal 093C metadata update post-change verification](docs/reports/goal093c_metadata_update_postchange_verification.md)

Metadata readback:

- description: `AI Workload Control Layer for routing deterministic, reusable, retrieval-needed, tool-needed, and provider-needed work before model invocation.`
- topics: `ai-infrastructure`, `ai-workload-control`, `deterministic-routing`, `llm-infrastructure`, `open-source`, `python`, `retrieval-routing`, `task-graph`, `tool-routing`, `workload-routing`
- homepage remains empty; visibility remains public; default branch remains `main`.

Claim boundary: Goal 093C is verification and documentation sync only. It did not change repository settings, move files, create a release, create a tag, create a publication, or add product claims.

Previous completed Goal: Goal 093A - Metadata Change Approval Packet.

Goal 093A prepared an approval packet for updating the public repository description and topics to match the AI Workload Control Layer positioning. It made no repository-setting changes.

Primary report:

- [Goal 093A metadata change approval packet](docs/reports/goal093a_metadata_change_approval_packet.md)

Previous completed Goal: Goal 092 - Repository Public Surface Alignment Audit.

Goal 092 audited the public GitHub surface after the exact public documentation replacement. It identified remaining alignment work for repository metadata, root files, example organization, and docs navigation while making no repository-setting changes and moving no files.

Primary report:

- [Goal 092 repository public surface alignment audit](docs/reports/goal092_repository_public_surface_alignment_audit.md)

Claim boundary: Goal 092 is an audit/proposal only. It does not add product claims, production-readiness claims, package-publication claims, release claims, metadata changes, or file moves.

Previous completed Goal: Goal 091B - Exact Public Documentation Replacement.

Goal 091B replaced selected public landing and index documents with exact authored Markdown files, including the root README, docs index, examples index, workload-control vision doc, example guide, and report. PR #241 was squash-merged into `origin/main` at `2972973d732624353bd722d648886eed4d6d9e6c`.

Primary report:

- [Goal 091B exact public documentation replacement](docs/reports/goal091b_exact_public_documentation_replacement.md)

Claim boundary: Goal 091B was documentation replacement only. It did not publish `getkora`, create a release, create a tag, claim production readiness, or move root files.

Previous completed Goal: Goal 088 - Implement Cache Reuse Example.

Goal 088 added an offline cache reuse example under `examples/cache_reuse/`. The example uses KORA `TaskGraph` execution with the deterministic `classify_by_rules` handler for first-time deterministic sample requests, local cache reuse for repeated exact or semantically equivalent sample requests, and provider-needed fallback labels for ambiguous/open-ended sample requests. It makes `0` provider calls.

Primary report:

- [Goal 088 cache reuse example](docs/reports/goal088_cache_reuse_example.md)

Example artifacts:

- [Cache reuse example README](examples/cache_reuse/README.md)
- [Cache reuse runnable script](examples/cache_reuse/run.py)
- [Cache reuse request fixture](examples/cache_reuse/requests.json)
- [Cache reuse expected counters](examples/cache_reuse/expected_counters.json)

Claim boundary: In this offline cache-reuse example, KORA routes repeated sample requests to cache hits without making provider calls and marks ambiguous/open-ended requests as provider-needed. It does not claim production cache correctness, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.

Previous completed Goal: Goal 087 - Implement Agent Workflow Optimization Example.

Goal 087 added an offline agent workflow optimization example under `examples/agent_workflow_optimization/`. The example uses KORA `TaskGraph` execution with the deterministic `agent_route_step` handler for non-cache sample workflow steps, local cache reuse for repeated deterministic steps, tool-needed labels for explicit local action steps, and provider-needed fallback labels for ambiguous planning/open-ended generation steps. It makes `0` provider calls.

Primary report:

- [Goal 087 agent workflow optimization example](docs/reports/goal087_agent_workflow_optimization_example.md)

Example artifacts:

- [Agent workflow optimization example README](examples/agent_workflow_optimization/README.md)
- [Agent workflow optimization runnable script](examples/agent_workflow_optimization/run.py)
- [Agent workflow fixture](examples/agent_workflow_optimization/workflows.json)
- [Agent workflow expected counters](examples/agent_workflow_optimization/expected_counters.json)

Claim boundary: In this offline agent-workflow example, KORA routes sample workflow steps across deterministic, cache, tool-needed, and provider-needed paths without making provider calls. It does not claim production agent readiness, autonomous agent reliability, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.

Previous completed Goal: Goal 086 - Implement RAG Routing Example.

Goal 086 added an offline RAG routing example under `examples/rag_routing/`. The example uses KORA `TaskGraph` execution with the deterministic `rag_route_query` handler for non-cache sample queries, local cache reuse for repeated sample queries, retrieval-needed labels for document-grounded queries over an offline corpus, and provider-needed fallback labels for ambiguous/open-ended sample queries. It makes `0` provider calls.

Primary report:

- [Goal 086 RAG routing example](docs/reports/goal086_rag_routing_example.md)

Example artifacts:

- [RAG routing example README](examples/rag_routing/README.md)
- [RAG routing runnable script](examples/rag_routing/run.py)
- [RAG routing corpus fixture](examples/rag_routing/corpus.json)
- [RAG routing query fixture](examples/rag_routing/queries.json)
- [RAG routing expected counters](examples/rag_routing/expected_counters.json)

Claim boundary: In this offline RAG-routing example, KORA routes sample queries across deterministic, cache, retrieval-needed, and provider-needed paths without making provider calls. It does not claim production RAG readiness, retrieval accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.

Previous completed Goal: Goal 085 - Implement OpenAI Proxy Reusable Module and CLI.

Goal 085 promoted the Goal 084 proxy example's routing logic into `kora.openai_proxy_demo` and added the first-class offline CLI command `python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json`. The existing `examples/openai_compatible_proxy/run.py` script remains a compatibility wrapper over the reusable module. Both paths make `0` provider calls.

Primary report:

- [Goal 085 OpenAI proxy reusable module and CLI](docs/reports/goal085_openai_proxy_reusable_module_cli.md)

Primary artifacts:

- [Reusable OpenAI proxy demo module](kora/openai_proxy_demo.py)
- [OpenAI-compatible proxy example README](examples/openai_compatible_proxy/README.md)
- [OpenAI-compatible proxy runnable wrapper](examples/openai_compatible_proxy/run.py)
- [OpenAI-compatible proxy request fixture](examples/openai_compatible_proxy/requests.json)
- [OpenAI-compatible proxy expected counters](examples/openai_compatible_proxy/expected_counters.json)

Claim boundary: In this offline proxy demo, KORA routes deterministic or cacheable OpenAI-style sample requests without making provider calls and marks ambiguous/open-ended requests as provider-needed. It does not claim production proxy readiness, full OpenAI API compatibility, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.

Previous completed Goal: Goal 084 - Implement OpenAI-Compatible Proxy Example.

Goal 084 added an offline OpenAI-compatible proxy example under `examples/openai_compatible_proxy/`. The example uses KORA `TaskGraph` execution with the deterministic `classify_by_rules` handler for bounded support-ticket classification requests, local cache reuse for repeated sample requests, and provider-needed fallback labels for ambiguous/open-ended sample requests. It makes `0` provider calls.

Primary report:

- [Goal 084 OpenAI-compatible proxy example](docs/reports/goal084_openai_compatible_proxy_example.md)

Example artifacts:

- [OpenAI-compatible proxy example README](examples/openai_compatible_proxy/README.md)
- [OpenAI-compatible proxy runnable script](examples/openai_compatible_proxy/run.py)
- [OpenAI-compatible proxy request fixture](examples/openai_compatible_proxy/requests.json)
- [OpenAI-compatible proxy expected counters](examples/openai_compatible_proxy/expected_counters.json)

Claim boundary: In this offline OpenAI-style proxy example, KORA routes deterministic or cacheable sample requests without making provider calls and marks ambiguous/open-ended requests as provider-needed. It does not claim production proxy readiness, full OpenAI API compatibility, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.

Previous completed Goal: Goal 083C - Public First-Run Acceptance Test.

Goal 083C tested the README-only reviewer path, fresh source install path, PyPI collision awareness, and five-minute reviewer path using the pending Goal 083B distribution strategy material. It also added a short source-install availability note to the deterministic classification README.

Primary report:

- [Goal 083C public first-run acceptance test](docs/reports/goal083c_public_first_run_acceptance_test.md)

Claim boundary: this goal did not add product features, publish a package, create a release, create a tag, or claim `getkora` is published.

Previous completed Goal: Goal 083B - Distribution Strategy and getkora Packaging Plan.

Goal 083B documented the distribution strategy after verifying that PyPI `kora` is occupied by an unrelated package and that `getkora` has no matching distribution by package-index lookup. The docs now state that latest KORA examples and `kora doctor` should be tested from the current repository/source checkout, while future PyPI distribution is planned under `getkora`.

Primary artifacts:

- [getkora distribution strategy](docs/packaging/getkora_distribution_strategy.md)
- [Goal 083B getkora distribution strategy](docs/reports/goal083b_getkora_distribution_strategy.md)

Claim boundary: this goal did not publish a package, create a release, create a tag, create a GitHub Release, reserve a PyPI project, or claim that `pip install getkora` works.

Previous completed Goal: Goal 083 - Implement KORA Doctor CLI.

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
- [Goal 106 fixture quality-check scaffold](docs/reports/goal106_fixture_quality_check_scaffold.md)
- [KORA quality-check seed fixture v0](examples/workloads/kora-quality-check-seed-v0.json)
- [Fixture quality-check evaluator](scripts/evaluate_fixture_quality_checks.py)
- [Goal 105 public-safe output-quality methodology](docs/reports/goal105_public_safe_output_quality_methodology.md)
- [Public-safe output-quality methodology](docs/methodology/public_safe_output_quality_methodology.md)
- [Goal 104 Codex bounded loop protocol](docs/reports/goal104_codex_bounded_loop_protocol.md)
- [Goal 091 README compression](docs/reports/goal091_readme_compression.md)
- [Goal 088 cache reuse example](docs/reports/goal088_cache_reuse_example.md)
- [Cache reuse example README](examples/cache_reuse/README.md)
- [Goal 087 agent workflow optimization example](docs/reports/goal087_agent_workflow_optimization_example.md)
- [Agent workflow optimization example README](examples/agent_workflow_optimization/README.md)
- [Goal 086 RAG routing example](docs/reports/goal086_rag_routing_example.md)
- [RAG routing example README](examples/rag_routing/README.md)
- [Goal 085 OpenAI proxy reusable module and CLI](docs/reports/goal085_openai_proxy_reusable_module_cli.md)
- [Goal 084 OpenAI-compatible proxy example](docs/reports/goal084_openai_compatible_proxy_example.md)
- [OpenAI-compatible proxy example README](examples/openai_compatible_proxy/README.md)
- [Goal 083B getkora distribution strategy](docs/reports/goal083b_getkora_distribution_strategy.md)
- [getkora distribution strategy](docs/packaging/getkora_distribution_strategy.md)
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
- [Generated Goal 099 CPU/non-GPU AI Champion summary](docs/evidence/generated/goal099_cpu_nongpu_ai_champion_summary.md)
- [Generated Goal 099 H100 AI Champion summary](docs/evidence/generated/goal099_h100_ai_champion_summary.md)

## Current Value Proposition

KORA makes AI workloads routable. The current KRK public alpha shows how workload requests can be inspected, compared, routed, run through public-safe dry-run paths, and reported with evidence and claim boundaries before defaulting to provider or GPU execution.

## Recommended Next Goal

Group 115 - Consider `CIL-005 - Source-Install Readiness Check`, only after explicit approval.

Recommended scope:

- use the Goal 104 runbooks as the execution checklist.
- verify the goal envelope, base SHA, KORA identity, and clean worktree.
- review [Group 114 first-run CLI smoke validation](docs/reports/group114_first_run_cli_smoke_validation.md).
- review [Group 113 inner loop applied review and queue hardening](docs/reports/group113_inner_loop_applied_review_queue_hardening.md).
- review [Codex medium-risk profile registry checklist](docs/context/CODEX_MEDIUM_RISK_PROFILE_REGISTRY_CHECKLIST.md).
- review [Group 112 PR approval and report consistency](docs/reports/group112_pr_approval_and_report_consistency.md).
- review [Group 111 validation report control block](docs/reports/group111_validation_report_control_block.md).
- review [Group 110 Codex inner loop ownership](docs/reports/group110_codex_inner_loop_ownership.md).
- review [Codex inner loop queue](docs/context/CODEX_INNER_LOOP_QUEUE.md).
- keep `CIL-003` deferred unless Albert explicitly approves the medium-risk profile-registry checklist.
- verify source-install readiness from local repo state without publishing packages.
- do not claim that `getkora` is published.
- expect final classification `needs-cto-review` if user-facing install docs or onboarding language change.
- preserve the requirement that Codex pass is not merge-ready pass.
- run the claim-boundary checklist before PR-open.
- keep any follow-on work local-only, finite, public-safe, and explicitly bounded.
- do not add semantic judging, human grading, provider calls, H100/GPU/CUDA/server/remote execution, model inference, production validation, claim expansion, background automation, actual multi-agent execution, or merge automation without separate explicit approval.
- stop at PR-open unless a separate merge-gate prompt is provided.

Alternative future goals remain `CIL-003`, a second route-only fixture slice, or documentation movement for one small bucket, but only after explicit approval.

Optional docs-navigation movement remains a separate future track only if Albert explicitly approves movement.

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
## Goal 091B - Exact Public Documentation Replacement

- Replaced selected public landing and index documents with exact authored Markdown files.
- Kept README focused on a short landing-page experience.
- Added or refreshed documentation index and example catalog pages.
- Preserved existing project history and avoided root directory moves.

## Goal 092 - Repository Public Surface Alignment Audit

- Audited GitHub metadata, root structure, examples, docs, and public first impression after the Goal 091B replacement.
- Proposed a metadata-only Goal 093 as the next approved step.
- Did not change repository settings, move files, create a release, create a tag, or publish a package.
