# KORA Next Goal Queue

Status: public-safe planning queue; proposals only.

## Purpose

This queue records likely next KORA work without starting it. It is not an approval record. Each item still needs an explicit goal prompt and the usual bounded-loop checks.

## Current Recommended Next Goal

1. Group 112 - Review Group 111 validation report control block and decide whether to run `CIL-003`.

Suggested scope:

- use the Goal 104 runbooks and `AGENTS.md` as the execution checklist.
- verify the goal envelope, base SHA, KORA identity, and clean worktree.
- review [Group 111 validation report control block](../reports/group111_validation_report_control_block.md).
- review [Group 110 Codex inner loop ownership](../reports/group110_codex_inner_loop_ownership.md).
- review [Codex inner loop queue](CODEX_INNER_LOOP_QUEUE.md).
- decide whether to run `CIL-003` or defer it because the bounded validation profile registry is medium risk.
- preserve the requirement that Codex pass is not merge-ready pass.
- require final classification as `merge-ready`, `needs-r1`, `needs-cto-review`, or `blocked`.
- do not add semantic judging, human grading, provider calls, H100/GPU/CUDA/server/remote execution, model inference, production validation, claim expansion, background automation, actual multi-agent execution, or merge automation without separate explicit approval.
- run the claim-boundary checklist before PR-open.
- stop at PR-open unless a separate merge-gate prompt is provided.

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
