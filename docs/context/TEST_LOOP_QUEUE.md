# KORA Test Loop Queue

Status: planning template only; not an approval record.

## Purpose

This queue records candidate bounded local test loops for future KORA goals. A listed item is not approved until Albert provides an explicit goal request text with base SHA, branch, allowed commands, loop budget, repair budget, allowed files, forbidden files, claim boundaries, and stop gates.

## Current Candidate

1. Goal 109 - Review the bounded local test loop result and decide whether another bounded local-only batch is useful.

Suggested future scope:

- review [Goal 108 bounded local test loop](../reports/goal108_bounded_local_test_loop.md).
- start any approved follow-on loop from the then-current `origin/main`.
- run only approved local validation commands.
- record pass, fail, skip, and gated outcomes.
- keep a finite loop count and finite repair budget.
- open PR and stop.
- do not merge.

## Standing Non-Approvals

The queue does not approve:

- provider calls.
- H100/GPU/CUDA/server/remote execution.
- model inference.
- semantic judging.
- human grading.
- production validation.
- output-quality proof.
- broader workload representativeness proof.
- claim expansion.
- background daemon, scheduler, GitHub Actions workflow, remote runner, or self-merging automation.
- release, tag, GitHub Release, PyPI publication, repository settings change, issue/project-board creation, raw artifact upload, file move, rename, archive, or delete operation.
- local-only project context changes.
