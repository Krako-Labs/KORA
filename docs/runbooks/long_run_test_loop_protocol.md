# Long-Run Test Loop Protocol

Status: public-safe protocol for future bounded local validation loops.

## Purpose

This runbook defines how a future KORA goal may run a longer validation loop without widening scope, making unsupported claims, or turning implementation workflow into a background runner.

A bounded long-run test loop is a scoped, finite validation loop. It runs known approved commands, records pass, fail, skip, and gated outcomes, stops after the approved loop budget, opens a PR, and stops. It does not merge.

This protocol is documentation only. It does not create a scheduler, daemon, GitHub Actions workflow, remote runner, provider-calling runner, H100 runner, or self-merging agent.

## Required Inputs

Every future long-run loop request text must provide or explicitly approve:

- goal id.
- base SHA.
- branch name.
- allowed test commands.
- maximum loop count.
- maximum repair attempts.
- timeout or practical stop condition.
- files allowed to change.
- files not allowed to change.
- claim-boundary checklist.
- explicit stop gates.

If any required input is missing, the implementation workflow must stop before starting the loop and request a bounded task brief.

## Loop Definition

For each approved loop iteration:

1. Confirm the worktree, branch, base SHA, and allowed changed-file set.
2. Run only the approved command list.
3. Record each command outcome as pass, fail, skip, or gated.
4. Classify any failure using the failure categories in [test failure triage checklist](test_failure_triage_checklist.md).
5. Repair only scoped failures within the approved file set.
6. Rerun the focused failing command first.
7. Rerun full validation only after focused repair passes.
8. Stop when the loop budget, repair budget, timeout, or stop gate is reached.
9. Open a PR when the approved task is complete.
10. Stop after PR-open unless a separate merge-gate request text is provided.

## Repair Rules

Allowed repairs:

- fix deterministic regressions inside the approved changed-file set.
- fix fixture or schema failures caused by the approved goal.
- fix documentation links, stale breadcrumbs, or report formatting caused by the approved goal.
- fix `git diff --check` whitespace failures in changed files.
- add or update focused tests only when the goal explicitly allows tests.

Required repair order:

1. Prefer focused repair before broad changes.
2. Rerun the focused failing command first.
3. Rerun full validation only after the focused command passes.
4. Stop if the same failure repeats after the maximum repair attempts.
5. Stop if the needed repair leaves the approved file set.

the implementation workflow must stop before any repair that requires:

- provider calls.
- H100/GPU/CUDA/server/remote execution.
- model inference.
- semantic judging.
- human grading.
- file moves, renames, archival, or deletion.
- public claim expansion.
- repository settings changes.
- release, tag, GitHub Release, PyPI publication, raw artifact upload, issue, or project-board creation.
- merge approval or self-merging behavior.

## Reporting Rules

Every PR body and final response for a future loop goal must include:

- command list.
- loop count.
- failures encountered.
- repairs attempted.
- final status.
- remaining gated items.
- validation summary.
- explicit non-claims.
- confirmation that the PR is open only and not merged.

For compact loop notes, use [test loop queue](../context/TEST_LOOP_QUEUE.md) as a planning template only. It is not an approval record.

## Stop Gates

Stop immediately if:

- the worktree is dirty with unrelated changes.
- `origin/main` does not match the approved base SHA.
- an unapproved file would need to change.
- a command needs provider, model, H100, GPU, CUDA, server, or remote execution.
- a failure requires semantic judging or human grading.
- a repair would imply output-quality proof, broader workload representativeness proof, production proof, or superiority claims.
- the same failure repeats after the approved maximum repair attempts.
- the loop reaches its approved iteration count, timeout, or practical stop condition.
- merge, release, publication, repo settings, raw artifact upload, issue/project-board creation, or file movement would be needed.

## Future Goal 108 Path

Goal 108 may apply this protocol to one bounded local-only test batch after explicit approval.

Goal 108 should not add provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, production validation, claim expansion, or merge automation.

## Explicit Non-Claims

This protocol does not:

- call providers.
- run H100/GPU/CUDA/server/remote execution.
- run model inference.
- execute semantic judging.
- add human grading.
- prove output quality.
- prove broader workload representativeness.
- prove production readiness, production workload handling, or production cost reduction.
- add superiority, customer-savings, provider-replacement, or GPU-serving replacement claims.
- create a scheduler, daemon, GitHub Actions workflow, remote runner, provider-calling runner, H100 runner, or self-merging agent.
