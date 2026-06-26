# KORA Next Goal Queue

Status: public-safe planning queue; proposals only.

## Purpose

This queue records likely next KORA work without starting it. It is not an approval record. Each item still needs an explicit goal request text and the usual bounded-loop checks.

## Current Recommended Next Goal

1. Review Group 118 - Evidence Breadcrumb Claim Consistency Audit.

Suggested scope:

- use the Goal 104 runbooks and `AGENTS.md` as the execution checklist.
- verify the goal envelope, base SHA, KORA identity, and clean worktree.
- review [Group 118 evidence, breadcrumb, and claim-consistency audit](../reports/group118_evidence_breadcrumb_claim_consistency_audit.md).
- review [Group 117 methodology-aligned deterministic fixture-check slice](../reports/group117_methodology_aligned_fixture_check_slice.md).
- review [Methodology-aligned fixture-check slice](../../examples/workloads/kora-methodology-fixture-check-slice-v0.json).
- review [Methodology fixture-check evaluator](../../scripts/evaluate_methodology_fixture_checks.py).
- review [Methodology fixture-check evaluator tests](../../tests/test_methodology_fixture_check_slice.py).
- rerun `python3 scripts/evaluate_methodology_fixture_checks.py` if reviewer wants to reproduce the deterministic fixture-check counters.
- review [Group 116 second route-only fixture slice](../reports/group116_second_route_only_fixture_slice.md).
- review [Group 115 source-install readiness check](../reports/group115_source_install_readiness_check.md).
- review [Group 114 first-run CLI smoke validation](../reports/group114_first_run_cli_smoke_validation.md).
- review [Group 113 inner loop applied review and queue hardening](../reports/group113_inner_loop_applied_review_queue_hardening.md).
- review [implementation workflow medium-risk profile registry checklist](MEDIUM_RISK_PROFILE_REGISTRY_CHECKLIST.md).
- review [Group 112 PR approval and report consistency](../reports/group112_pr_approval_and_report_consistency.md).
- review [Group 111 validation report control block](../reports/group111_validation_report_control_block.md).
- review [Group 110 implementation workflow ownership](../reports/group110_implementation_workflow_ownership.md).
- review [implementation workflow queue](WORKFLOW_QUEUE.md).
- keep `CIL-003` deferred unless Albert explicitly approves the medium-risk profile-registry checklist.
- confirm Group 117 remains bounded deterministic fixture-check evidence only, without output-quality, broader representativeness, production readiness, production validation, cost-reduction, provider-replacement, or GPU-serving-replacement claims.
- confirm Group 118 is documentation and audit evidence only.
- expected final classification is `merge-ready` if CI passes and claim boundaries remain unchanged.
- preserve the requirement that workflow pass is not merge-ready pass.
- require final classification as `merge-ready`, `needs-r1`, `needs-cto-review`, or `blocked`.
- do not add semantic judging, human grading, provider calls, H100/GPU/CUDA/server/remote execution, model inference, production validation, claim expansion, background automation, actual multi-agent execution, or merge automation without separate explicit approval.
- run the claim-boundary checklist before PR-open.
- stop at PR-open unless a separate merge-gate request text is provided.

## Future Queue Item Sizing

Future queue items should record one expected duration band: `30-60 min`, `1-2 hr`, `2-4 hr`, or `half-day`.

Low-risk adjacent checkers may be bundled when they share the same input surface and validation path. Medium-risk command-surface changes should not be bundled with unrelated work. High-risk work must not be bundled.

Do not split a checker, tests, docs, report, and breadcrumbs into separate tasks unless risk or ownership requires separation. Prefer coherent control blocks that leave the next queue state clearer than before.

## Approved Alternatives Only After Explicit Workflow Guide

- Another bounded public-safe fixture/check slice.
- A second public-safe fixture-check slice.
- Documentation movement for one small bucket.
- Larger bounded H100 or provider validation work.
- Any high-risk work from [implementation workflow risk classification](WORKFLOW_RISK_CLASSIFICATION.md).

## Standing Stop Gates

Do not start without explicit approval:

- merge.
- release, tag, GitHub Release, release asset, or PyPI/package publication.
- repository settings or metadata changes.
- raw benchmark artifact upload.
- provider calls.
- H100/GPU/CUDA/server/remote execution.
- file moves, renames, archival, or deletion.
- public claim expansion.
- public-facing README or major narrative rewrite beyond the approved goal scope.

## Current Claim Reminder

Goal 103 route-only counters do not prove output quality, broader workload representativeness, production workload handling, production readiness, cost reduction, H100/GPU/CPU superiority, customer savings, provider replacement, GPU-serving replacement, or published `getkora`.

Goal 105 methodology documentation does not execute evaluation, prove output quality, prove broader workload representativeness, prove production workload handling, prove production readiness, or prove cost reduction.

Goal 106 aggregate scaffold counts do not prove output quality, broader workload representativeness, production workload handling, production readiness, cost reduction, H100/GPU/CPU superiority, customer savings, provider replacement, GPU-serving replacement, or published `getkora`.

Goal 107 protocol documentation does not execute long-run validation, create background automation, prove output quality, prove broader workload representativeness, prove production workload handling, prove production readiness, or prove cost reduction.

Goal 108 bounded local validation results do not prove output quality, broader workload representativeness, production workload handling, production readiness, or cost reduction.

Goal 109 bounded local validation runner results do not prove output quality, broader workload representativeness, production workload handling, production readiness, or cost reduction.

Group 110 implementation workflow operating guidance does not create production automation, auto-merge, background execution, provider calls, H100/server execution, actual multi-agent execution, output-quality proof, broader workload representativeness proof, production proof, or claim expansion.

Group 111 validation report control-block tooling does not execute report commands, auto-repair, create background automation, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, or expand claims.

Group 112 approval-packet and report-consistency checks do not call GitHub APIs, approve PRs, merge PRs, close PRs, create issues, execute report commands, auto-repair, create background automation, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, or expand claims.

Group 113 queue hardening does not implement `CIL-003`, change validation profiles, execute report commands, call GitHub APIs, mutate PRs, create issues, auto-repair, create background automation, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, or expand claims.

Group 114 first-run CLI smoke validation does not implement `CIL-003`, change validation profile registries, publish packages, call providers, require network access, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, prove broader workload representativeness, or claim that `getkora` is published.

Group 115 source-install readiness checking does not implement `CIL-003`, change validation profile registries, change command profile registries, check PyPI installation, publish packages, create releases or tags, claim that `getkora` is published, claim install-from-PyPI support, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, or prove broader workload representativeness.

Group 116 second route-only fixture slice does not implement `CIL-003`, change validation profile registries, change command profile registries, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, prove broader workload representativeness, prove production readiness, prove cost reduction, claim provider replacement, claim GPU-serving replacement, or expand claims.

Group 117 methodology-aligned deterministic fixture-check slice does not implement `CIL-003`, change validation profile registries, change command profile registries, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, prove broader workload representativeness, prove production readiness, prove cost reduction, claim provider replacement, claim GPU-serving replacement, or expand claims.

Group 118 evidence, breadcrumb, and claim-consistency audit does not implement `CIL-003`, change validation profile registries, change command profile registries, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, prove broader workload representativeness, prove production readiness, prove cost reduction, claim provider replacement, claim GPU-serving replacement, publish packages, or expand claims.
