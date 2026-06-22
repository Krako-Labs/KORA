# KORA Next Goal Queue

Status: public-safe planning queue; proposals only.

## Purpose

This queue records likely next KORA work without starting it. It is not an approval record. Each item still needs an explicit goal prompt and the usual bounded-loop checks.

## Current Recommended Next Goal

1. Goal 105 - Apply the Codex bounded-loop protocol to the next approved KORA task.

Suggested scope:

- use the Goal 104 runbooks as the execution checklist.
- verify the goal envelope, base SHA, KORA identity, and clean worktree.
- run the claim-boundary checklist before PR-open.
- stop at PR-open unless a separate merge-gate prompt is provided.

## Approved Alternatives Only After Explicit Prompt

- Public-safe output-quality methodology design for fixture-derived work.
- A second route-only fixture slice.
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
