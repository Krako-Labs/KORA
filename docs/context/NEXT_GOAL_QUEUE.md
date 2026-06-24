# KORA Next Goal Queue

Status: public-safe planning queue; proposals only.

## Purpose

This queue records likely next KORA work without starting it. It is not an approval record. Each item still needs an explicit goal prompt and the usual bounded-loop checks.

## Current Recommended Next Goal

1. Group 115 - Consider `CIL-005 - Source-Install Readiness Check`, only after explicit approval.

Suggested scope:

- use the Goal 104 runbooks and `AGENTS.md` as the execution checklist.
- verify the goal envelope, base SHA, KORA identity, and clean worktree.
- review [Group 114 first-run CLI smoke validation](../reports/group114_first_run_cli_smoke_validation.md).
- review [Group 113 inner loop applied review and queue hardening](../reports/group113_inner_loop_applied_review_queue_hardening.md).
- review [Codex medium-risk profile registry checklist](CODEX_MEDIUM_RISK_PROFILE_REGISTRY_CHECKLIST.md).
- review [Group 112 PR approval and report consistency](../reports/group112_pr_approval_and_report_consistency.md).
- review [Group 111 validation report control block](../reports/group111_validation_report_control_block.md).
- review [Group 110 Codex inner loop ownership](../reports/group110_codex_inner_loop_ownership.md).
- review [Codex inner loop queue](CODEX_INNER_LOOP_QUEUE.md).
- keep `CIL-003` deferred unless Albert explicitly approves the medium-risk profile-registry checklist.
- for `CIL-005`, verify source-install readiness from local repo state without publishing packages.
- do not claim that `getkora` is published.
- expect final classification `needs-cto-review` if user-facing install docs or onboarding language change.
- preserve the requirement that Codex pass is not merge-ready pass.
- require final classification as `merge-ready`, `needs-r1`, `needs-cto-review`, or `blocked`.
- do not add semantic judging, human grading, provider calls, H100/GPU/CUDA/server/remote execution, model inference, production validation, claim expansion, background automation, actual multi-agent execution, or merge automation without separate explicit approval.
- run the claim-boundary checklist before PR-open.
- stop at PR-open unless a separate merge-gate prompt is provided.

## Future Queue Item Sizing

Future queue items should record one expected duration band: `30-60 min`, `1-2 hr`, `2-4 hr`, or `half-day`.

Low-risk adjacent checkers may be bundled when they share the same input surface and validation path. Medium-risk command-surface changes should not be bundled with unrelated work. High-risk work must not be bundled.

Do not split a checker, tests, docs, report, and breadcrumbs into separate tasks unless risk or ownership requires separation. Prefer coherent control blocks that leave the next queue state clearer than before.

## Approved Alternatives Only After Explicit Prompt

- A second route-only fixture slice.
- A second public-safe fixture-check slice.
- Documentation movement for one small bucket.
- Larger bounded H100 or provider validation work.
- Any high-risk work from [Codex risk classification](CODEX_RISK_CLASSIFICATION.md).

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

Group 110 Codex inner-loop operating guidance does not create production automation, auto-merge, background execution, provider calls, H100/server execution, actual multi-agent execution, output-quality proof, broader workload representativeness proof, production proof, or claim expansion.

Group 111 validation report control-block tooling does not execute report commands, auto-repair, create background automation, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, or expand claims.

Group 112 approval-packet and report-consistency checks do not call GitHub APIs, approve PRs, merge PRs, close PRs, create issues, execute report commands, auto-repair, create background automation, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, or expand claims.

Group 113 queue hardening does not implement `CIL-003`, change validation profiles, execute report commands, call GitHub APIs, mutate PRs, create issues, auto-repair, create background automation, call providers, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, or expand claims.

Group 114 first-run CLI smoke validation does not implement `CIL-003`, change validation profile registries, publish packages, call providers, require network access, run H100/GPU/CUDA/server/remote execution, run model inference, perform semantic judging or human grading, add production validation, prove output quality, prove broader workload representativeness, or claim that `getkora` is published.
