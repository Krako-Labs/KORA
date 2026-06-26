# Goal 107 Long-Run Test Loop Protocol

Status: public-safe protocol documentation added.

## Objective

Goal 107 adds a KORA long-run test loop protocol and failure-triage checklist so future implementation workflow tasks can safely run longer local validation loops while preserving finite budgets, stop gates, and claim boundaries.

This is documentation and protocol work only. It does not create a scheduler, daemon, background runner, GitHub Actions workflow, remote runner, provider-calling runner, H100 runner, or self-merging agent.

## Why This Follows Goal 106

Goal 106 added a tiny public-safe fixture-based quality-check scaffold with deterministic fixture-only checks and aggregate JSON output. Goal 107 adds the operating protocol needed before a future goal applies longer validation loops to local test batches.

The sequence keeps the boundary clear:

- Goal 106 provides a tiny deterministic scaffold.
- Goal 107 defines how future looped validation should be bounded and reported.
- Goal 108 may apply the protocol to one bounded local-only test batch only after explicit approval.

## Files Added Or Updated

Added:

- [Long-run test loop protocol](../runbooks/long_run_test_loop_protocol.md)
- [Test failure triage checklist](../runbooks/test_failure_triage_checklist.md)
- [KORA test loop queue](../context/TEST_LOOP_QUEUE.md)
- [Goal 107 long-run test loop protocol report](goal107_long_run_test_loop_protocol.md)

Updated:

- [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [REVIEW_HUB.md](../../REVIEW_HUB.md)
- [KORA next goal queue](../context/NEXT_GOAL_QUEUE.md)
- [Documentation index](../README.md)

## Protocol Summary

The long-run test loop protocol defines a bounded long-run test loop as a scoped, finite validation loop that:

- runs known approved commands.
- records pass, fail, skip, and gated outcomes.
- stops after the approved loop budget.
- uses a finite repair budget.
- fixes only scoped failures.
- reruns focused failing commands before full validation.
- opens PR and stops.
- does not merge.

Required future inputs include goal id, base SHA, branch, allowed commands, max loop count, max repair attempts, timeout or practical stop condition, allowed files, forbidden files, claim-boundary checklist, and explicit stop gates.

## Failure Triage Summary

The failure-triage checklist classifies future loop failures as:

- deterministic regression.
- fixture or schema failure.
- documentation or link failure.
- formatting or diff-check failure.
- test environment failure.
- flaky or nondeterministic failure.
- scope violation.
- claim-boundary violation.
- gated failure requiring human approval.

Each category includes allowed response rules and stop conditions.

## Validation Performed

Validation for this PR:

- `python3 scripts/check_markdown_links_goal082b.py`
- `git diff --check`
- `python3 -m pytest`

## Explicit Non-Claims

Goal 107 does not:

- call providers.
- run H100/GPU/CUDA/server/remote execution.
- run model inference.
- execute semantic judging.
- add human grading.
- prove output quality.
- prove broader workload representativeness.
- prove production readiness, production workload handling, or production cost reduction.
- add superiority, customer-savings, provider-replacement, or GPU-serving replacement claims.
- create a scheduler, daemon, background runner, GitHub Actions workflow, remote runner, provider-calling runner, H100 runner, or self-merging agent.
- create a release, tag, GitHub Release, PyPI publication, repository settings change, issue, project board, raw artifact upload, file move, rename, archive, or delete operation.
- modify local-only project context files.

## Next Recommended Goal

Recommended next goal:

- Goal 108 - Apply the long-run test loop protocol to one bounded local-only test batch, only after explicit approval.

Goal 108 should not add provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, production validation, claim expansion, or merge automation.
