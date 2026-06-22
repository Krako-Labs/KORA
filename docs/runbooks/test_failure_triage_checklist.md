# Test Failure Triage Checklist

Status: public-safe checklist for bounded KORA validation loops.

## Purpose

Use this checklist when an approved KORA long-run test loop encounters a failure. The checklist classifies the failure, limits repairs to the approved scope, and preserves stop gates.

This checklist is documentation only. It does not execute tests, schedule background work, call providers, run model inference, run H100/GPU/CUDA/server/remote work, or authorize merge.

## Failure Categories

### Deterministic Regression

Use when a deterministic command or test that previously passed now fails because changed public code, fixture data, or docs changed behavior inside the approved goal.

Allowed response:

- inspect the smallest failing assertion or output delta.
- repair only the scoped changed file.
- rerun the focused failing command.

Stop if repair requires unapproved behavior changes, broad rewrites, provider calls, model inference, H100/GPU/server execution, or claim expansion.

### Fixture Or Schema Failure

Use when a fixture, JSON shape, schema version, required field, allowed enum, or aggregate counter check fails.

Allowed response:

- confirm whether the fixture or evaluator is within the approved file set.
- repair the fixture or validation code only when the goal explicitly allows it.
- rerun the fixture-specific command first.

Stop if the fix would convert route-only or fixture-only evidence into output-quality proof, broader representativeness proof, production proof, or semantic judging.

### Documentation Or Link Failure

Use when Markdown links, breadcrumb references, report paths, or review-hub references fail.

Allowed response:

- update stale links or breadcrumbs in approved docs.
- keep wording narrow and evidence-bounded.
- rerun the Markdown link checker.

Stop if the repair requires moving, renaming, archiving, or deleting files without explicit approval.

### Formatting Or Diff-Check Failure

Use when `git diff --check` reports whitespace or formatting problems in changed files.

Allowed response:

- fix only the reported changed-file formatting issue.
- rerun `git diff --check`.

Stop if unrelated dirty files are involved.

### Test Environment Failure

Use when a dependency, local interpreter, file permission, or test discovery issue prevents a command from running.

Allowed response:

- record the command, error, environment detail, and whether the failure is local-only.
- retry only if the failure is clearly transient and retrying is inside the approved loop budget.

Stop if resolving it requires network installation, provider credentials, H100/GPU/server access, repository settings changes, or unapproved environment mutation.

### Flaky Or Nondeterministic Failure

Use when a command alternates between pass and fail without a scoped code or fixture cause.

Allowed response:

- record the observed pass/fail sequence.
- rerun only within the approved loop budget.
- isolate the smallest flaky command.

Stop if nondeterminism remains after the approved repair attempts or if diagnosing it requires unapproved infrastructure.

### Scope Violation

Use when a failure suggests changing files or behavior outside the approved goal.

Required response:

- stop.
- report the needed out-of-scope change.
- do not broaden the PR.

### Claim-Boundary Violation

Use when changed text implies unsupported output-quality proof, broader workload representativeness proof, production proof, superiority, customer savings, provider replacement, GPU-serving replacement, or published package availability.

Allowed response:

- rewrite the changed text to explicit non-claim language inside the approved files.
- rerun the changed-file claim scan.

Stop if the goal depends on making the unsupported claim.

### Gated Failure Requiring Human Approval

Use when repair requires a decision from Albert or a separate goal prompt.

Examples:

- provider calls.
- H100/GPU/CUDA/server/remote execution.
- model inference.
- semantic judging.
- human grading.
- file movement.
- merge.
- release, publication, repository settings, raw artifact upload, issue, or project-board creation.

Required response:

- stop.
- report the gate.
- do not perform the gated action.

## Failure Record Template

Use this shape in a report, PR body, or final response:

```text
Command:
Outcome:
Category:
Loop iteration:
Repair attempted:
Focused rerun:
Full validation rerun:
Final status:
Remaining gated item:
Non-claims preserved:
```

## Completion Check

Before opening a PR after a loop, confirm:

- all approved commands were run or explicitly marked skipped/gated.
- loop count and repair count are recorded.
- any remaining failure is classified.
- no unapproved files changed.
- no provider calls, model inference, H100/GPU/CUDA/server/remote execution, semantic judging, or human grading occurred.
- no output-quality proof, broader workload representativeness proof, production proof, or superiority/customer-savings/provider-replacement claims were added.
- no release, tag, GitHub Release, PyPI publication, repository settings change, issue/project-board creation, raw artifact upload, file move, rename, archive, or delete operation occurred.
- the PR is open only and not merged.
