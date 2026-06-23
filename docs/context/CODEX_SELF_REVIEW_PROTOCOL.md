# Codex Self-Review Protocol

Status: required review protocol before KORA PR creation.

## Purpose

Codex self-review is a repo-grounded check before PR creation. It does not replace Albert review, CTO review, merge gates, or release approval.

## Required Checks

Before PR open, Codex must review:

- changed files vs allowed scope.
- forbidden paths and forbidden actions.
- validation commands and exact results.
- report consistency.
- breadcrumb consistency.
- local-only ChatGPT context untouched.
- no provider calls.
- no H100/GPU/CUDA/server/remote execution.
- no model inference.
- no semantic judging or human grading.
- no production validation claims.
- no output-quality proof claims.
- no broader workload representativeness proof claims.
- no production proof claims.
- no release, tag, PyPI publication, GitHub Release, repo settings, issues, project boards, collaborators, or raw artifact uploads.
- no file movement unless explicitly approved.
- no arbitrary shell command execution beyond approved validation commands.
- no scheduler, daemon, background runner, GitHub Actions workflow, remote runner, provider-calling runner, H100 runner, or self-merging agent.
- uncertainty notes.

## Validation Review

Codex must record:

- commands run.
- pass/fail result.
- failing output summary.
- repair attempts.
- rerun results.
- final validation status.

## Report Review

Codex must confirm the report includes:

- objective.
- files added and changed.
- validation results.
- loop count.
- repair attempts.
- safety boundaries.
- claim boundaries.
- final status classification.
- next recommended work.

## Final Classification

Every completed work block must end with exactly one:

- `merge-ready`
- `needs-r1`
- `needs-cto-review`
- `blocked`

Use `merge-ready` only when scope, validation, claim boundaries, and review uncertainty are all low. Use `needs-r1` when a narrow follow-up patch is needed. Use `needs-cto-review` when semantic, claim, scope, evidence, release, provider, H100/server, file-movement, multi-agent, or public-positioning risk remains. Use `blocked` when a hard approval gate or unresolved validation failure prevents safe PR completion.

## Claim Boundary Reminder

Self-review must preserve that KORA work does not claim output-quality proof, broader workload representativeness proof, production proof, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, or published `getkora` unless separately approved and evidenced.
