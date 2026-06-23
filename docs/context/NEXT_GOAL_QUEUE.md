# KORA Next Goal Queue

Status: public-safe planning queue; proposals only.

## Purpose

This queue records likely next KORA work without starting it. It is not an approval record. Each item still needs an explicit goal prompt and the usual bounded-loop checks.

## Current Recommended Next Goal

1. Goal 111 - Review the bounded local validation report verifier and decide whether another public-safe report fixture slice is useful.

Suggested scope:

- use the Goal 104 runbooks as the execution checklist.
- verify the goal envelope, base SHA, KORA identity, and clean worktree.
- review [Goal 110 bounded local validation report verifier](../reports/goal110_bounded_local_validation_report_verifier.md).
- review [Goal 109 bounded local validation runner](../reports/goal109_bounded_local_validation_runner.md).
- decide whether another public-safe report fixture slice is useful before starting it.
- keep any follow-on verifier work read-only over JSON reports unless separately approved.
- do not add semantic judging, human grading, provider calls, H100/GPU/CUDA/server/remote execution, model inference, production validation, claim expansion, arbitrary command execution, report-command execution, background automation, or merge automation without separate explicit approval.
- run the claim-boundary checklist before PR-open.
- stop at PR-open unless a separate merge-gate prompt is provided.

## Approved Alternatives Only After Explicit Prompt

- A second route-only fixture slice.
- A second public-safe fixture-check slice.
- Documentation movement for one small bucket.
- Larger bounded H100 or provider validation work.

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

Goal 110 bounded local validation report verification does not execute report commands and does not prove output quality, broader workload representativeness, production workload handling, production readiness, or cost reduction.
