# KORA Documentation

KORA is an **AI Workload Control Layer** for inspecting and routing AI workloads before they reach a model.

This documentation index is for readers who want more detail than the root [README](../README.md).

## Start Here

- [Root README](../README.md) - short project landing page.
- [Vision: KORA Workload Control Layer](vision/kora_workload_control_layer.md) - why workload control matters.
- [Example catalog](../examples/README.md) - runnable examples grouped by use case.
- [Packaging: getkora strategy](packaging/getkora_distribution_strategy.md) - package-name and install-path status.
- [Research Foundry Alpha](research-foundry-alpha.md) - Local Only text-layer PDF ingest, lexical retrieval, and deterministic evidence cards.
- [Solution Protocol v0alpha1](solution-protocol-v0.md) - offline package validation, integrity-checked local capability registry, deterministic runtime resolution, and bounded Host lifecycle.
- [Solution SDK and Conformance Kit](solution-sdk-conformance-kit.md) - deterministic scaffolding, integrity-bound cases, isolated lifecycle checks, and machine-readable reports.
- [Reference Solutions](../examples/solutions/README.md) - synthetic packages and one bounded existing-vertical reference using the same Protocol and Host interface.

## Flagship Examples

| Example | Purpose | Path |
| --- | --- | --- |
| KORA Doctor | Inspect sample workloads and identify route candidates. | [`examples/kora_doctor`](../examples/kora_doctor/) |
| Deterministic Classification | Route predictable classification tasks without provider calls. | [`examples/deterministic_classification`](../examples/deterministic_classification/) |
| OpenAI-Compatible Proxy | Demonstrate offline OpenAI-style request routing. | [`examples/openai_compatible_proxy`](../examples/openai_compatible_proxy/) |
| RAG Routing | Separate deterministic, cache, retrieval-needed, and provider-needed paths. | [`examples/rag_routing`](../examples/rag_routing/) |
| Agent Workflow Optimization | Route multi-step agent-style workflows. | [`examples/agent_workflow_optimization`](../examples/agent_workflow_optimization/) |
| Cache Reuse | Show repeated-work reuse through a local offline cache path. | [`examples/cache_reuse`](../examples/cache_reuse/) |

## Architecture and Vision

- [KORA Workload Control Layer](vision/kora_workload_control_layer.md)
- [Architecture docs](architecture/)
- [Claims and public language](claims/)

## Evidence and Reports

- [Reports](reports/)
- [Task 022 existing vertical migration readiness](reports/task022-existing-vertical-migration-readiness.md) - Research Foundry inventory, migration gaps, frozen package-local slice, conformance cases, deferrals, and claim boundary.
- [Evidence docs](evidence/)
- [Benchmarks](benchmarks/)
- [Workloads](workloads/)
- [Public-safe output-quality methodology](methodology/public_safe_output_quality_methodology.md) - future validation design for fixture-derived checks; does not execute evaluation or prove output quality.
- [Goal 106 fixture quality-check scaffold](reports/goal106_fixture_quality_check_scaffold.md) - tiny deterministic fixture-only scaffold with aggregate counts; does not prove output quality.
- [Goal 107 long-run test loop protocol](reports/goal107_long_run_test_loop_protocol.md) - protocol documentation for future bounded local validation loops; does not execute long-run validation or create automation.
- [Goal 108 bounded local test loop](reports/goal108_bounded_local_test_loop.md) - one bounded local-only validation batch; does not prove output quality or production readiness.
- [Goal 109 bounded local validation runner](reports/goal109_bounded_local_validation_runner.md) - approved-command local validation runner; does not prove output quality or production readiness.
- [Group 110 implementation workflow ownership](reports/group110_implementation_workflow_ownership.md) - repo-local implementation workflow operating guidance; does not create auto-merge, production automation, or claim expansion.
- [Group 111 validation report control block](reports/group111_validation_report_control_block.md) - static bounded-validation report verifier and failure classifier; does not execute report commands or prove output quality.
- [Group 112 PR approval and report consistency](reports/group112_pr_approval_and_report_consistency.md) - approval-packet and report-consistency checks; does not mutate GitHub or execute report commands.
- [Group 113 inner loop applied review and queue hardening](reports/group113_inner_loop_applied_review_queue_hardening.md) - operating review and queue hardening; does not implement `CIL-003` or change validation profiles.
- [Group 114 first-run CLI smoke validation](reports/group114_first_run_cli_smoke_validation.md) - deterministic local first-run CLI smoke checks over existing offline commands; does not publish packages or prove production readiness.
- [Group 115 source-install readiness check](reports/group115_source_install_readiness_check.md) - isolated local source-install readiness checking; does not check PyPI, publish packages, or claim `getkora` is published.
- [Group 116 second route-only fixture slice](reports/group116_second_route_only_fixture_slice.md) - second synthetic route-only fixture slice with aggregate counters only; does not prove output quality or broader representativeness.
- [Group 117 methodology-aligned deterministic fixture-check slice](reports/group117_methodology_aligned_fixture_check_slice.md) - exact and structured deterministic fixture checks over public-safe synthetic examples; does not prove output quality.
- [Group 118 evidence, breadcrumb, and claim-consistency audit](reports/group118_evidence_breadcrumb_claim_consistency_audit.md) - post-Group-117 documentation and audit-evidence consistency pass; does not implement `CIL-003` or expand claims.
- [Group 119 public operations wording scrub PR](https://github.com/Krako-Labs/KORA/pull/272) - merged public wording hygiene; keeps `CIL-003`, runtime, provider, package, release, and claim boundaries unchanged.
- [Group 120 long work block candidate selection](reports/group120_long_work_block_candidate_selection.md) - queue rebuild around one 2-4 hour candidate; does not implement the candidate or expand claims.
- [Goal 096 documentation navigation and archive-bucket proposal](reports/goal096_documentation_navigation_archive_bucket_proposal.md) - proposal-only navigation buckets; no files moved.
- [Group 097 H100 evidence inventory and gap audit](reports/group097_h100_evidence_inventory_gap_audit.md) - bounded H100 evidence inventory; no new H100 benchmark claim.
- [Goal 098 controlled CPU/GPU evidence regeneration](reports/goal098_controlled_cpu_gpu_evidence_regeneration.md) - server-run packet with local no-CUDA `not_run` status; no fresh H100 execution claim.
- [Goal 099 AI Champion H100 server run](reports/goal099_ai_champion_h100_server_run.md) - controlled server-run packet execution with aggregate CPU/non-GPU and bounded H100 summaries.
- [Goal 100 Goal 099 evidence index review](reports/goal100_goal099_evidence_index_review.md) - evidence-index decision after Goal 099; narrow index refresh only.
- [Goal 102 workload representativeness seed](reports/goal102_workload_representativeness_seed.md) - public-safe fixture-design seed for broader workload coverage planning; not production workload proof.
- [Goal 103 representativeness route-only evaluator](reports/goal103_representativeness_route_only_evaluator.md) - aggregate route-only counters over the Goal 102 seed; not output-quality or broader representativeness proof.
- [Goal 104 bounded workflow protocol](reports/goal104_bounded_workflow_protocol.md) - operating protocol for PR-open bounded-loop execution with human approval gates.
- [Goal 105 public-safe output-quality methodology](reports/goal105_public_safe_output_quality_methodology.md) - methodology for future public-safe fixture-derived checks.

KORA uses narrow evidence language. Offline examples and reports may describe sample workloads and simulated avoided provider/model invocations, but they do not prove production cost reduction or production readiness.

## Project Operations

- [Contributing](../CONTRIBUTING.md)
- [Security](../SECURITY.md)
- [Governance](../GOVERNANCE.md)
- [Runbooks](runbooks/)
- [bounded workflow protocol](runbooks/bounded_workflow_protocol.md)
- [implementation workflow queue](context/WORKFLOW_QUEUE.md)
- [implementation workflow self-review protocol](context/WORKFLOW_SELF_REVIEW_PROTOCOL.md)
- [implementation workflow risk classification](context/WORKFLOW_RISK_CLASSIFICATION.md)
- [implementation workflow escalation gates](context/WORKFLOW_ESCALATION_GATES.md)
- [implementation workflow approval packet](context/WORKFLOW_APPROVAL_PACKET.md)
- [implementation workflow medium-risk profile registry checklist](context/MEDIUM_RISK_PROFILE_REGISTRY_CHECKLIST.md)
- [Second slice route-only evaluator](../scripts/evaluate_representativeness_slice_routes.py)
- [Source-install readiness checker](../scripts/check_source_install_readiness.py)
- [First-run CLI smoke checker](../scripts/check_first_run_cli_smoke.py)
- [implementation workflow multi-agent operating model](context/WORKFLOW_MULTI_ACTOR_OPERATING_MODEL.md)
- [Long-run test loop protocol](runbooks/long_run_test_loop_protocol.md)
- [Test failure triage checklist](runbooks/test_failure_triage_checklist.md)
- [KORA claim-boundary checklist](runbooks/kora_claim_boundary_checklist.md)
- [KORA PR completion format](runbooks/kora_pr_completion_format.md)
- [Next goal queue](context/NEXT_GOAL_QUEUE.md)
- [Test loop queue](context/TEST_LOOP_QUEUE.md)
