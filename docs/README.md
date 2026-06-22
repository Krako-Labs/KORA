# KORA Documentation

KORA is an **AI Workload Control Layer** for inspecting and routing AI workloads before they reach a model.

This documentation index is for readers who want more detail than the root [README](../README.md).

## Start Here

- [Root README](../README.md) — short project landing page.
- [Vision: KORA Workload Control Layer](vision/kora_workload_control_layer.md) — why workload control matters.
- [Example catalog](../examples/README.md) — runnable examples grouped by use case.
- [Packaging: getkora strategy](packaging/getkora_distribution_strategy.md) — package-name and install-path status.

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
- [Evidence docs](evidence/)
- [Benchmarks](benchmarks/)
- [Workloads](workloads/)
- [Public-safe output-quality methodology](methodology/public_safe_output_quality_methodology.md) - future validation design for fixture-derived checks; does not execute evaluation or prove output quality.
- [Goal 096 documentation navigation and archive-bucket proposal](reports/goal096_documentation_navigation_archive_bucket_proposal.md) - proposal-only navigation buckets; no files moved.
- [Group 097 H100 evidence inventory and gap audit](reports/group097_h100_evidence_inventory_gap_audit.md) - bounded H100 evidence inventory; no new H100 benchmark claim.
- [Goal 098 controlled CPU/GPU evidence regeneration](reports/goal098_controlled_cpu_gpu_evidence_regeneration.md) - server-run packet with local no-CUDA `not_run` status; no fresh H100 execution claim.
- [Goal 099 AI Champion H100 server run](reports/goal099_ai_champion_h100_server_run.md) - controlled server-run packet execution with aggregate CPU/non-GPU and bounded H100 summaries.
- [Goal 100 Goal 099 evidence index review](reports/goal100_goal099_evidence_index_review.md) - evidence-index decision after Goal 099; narrow index refresh only.
- [Goal 102 workload representativeness seed](reports/goal102_workload_representativeness_seed.md) - public-safe fixture-design seed for broader workload coverage planning; not production workload proof.
- [Goal 103 representativeness route-only evaluator](reports/goal103_representativeness_route_only_evaluator.md) - aggregate route-only counters over the Goal 102 seed; not output-quality or broader representativeness proof.
- [Goal 104 Codex bounded loop protocol](reports/goal104_codex_bounded_loop_protocol.md) - operating protocol for PR-open bounded-loop execution with human approval gates.
- [Goal 105 public-safe output-quality methodology](reports/goal105_public_safe_output_quality_methodology.md) - methodology for future public-safe fixture-derived checks.

KORA uses narrow evidence language. Offline examples and reports may describe sample workloads and simulated avoided provider/model invocations, but they do not prove production cost reduction or production readiness.

## Project Operations

- [Contributing](../CONTRIBUTING.md)
- [Security](../SECURITY.md)
- [Governance](../GOVERNANCE.md)
- [Runbooks](runbooks/)
- [Codex bounded loop protocol](runbooks/codex_bounded_loop_protocol.md)
- [KORA claim-boundary checklist](runbooks/kora_claim_boundary_checklist.md)
- [KORA PR completion format](runbooks/kora_pr_completion_format.md)
- [Next goal queue](context/NEXT_GOAL_QUEUE.md)
