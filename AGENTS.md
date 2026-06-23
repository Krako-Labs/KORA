# KORA Codex Operating Contract

This file is the repo-local operating contract for Codex work in KORA.

## Project Positioning

KORA is an AI Workload Control Layer for inspecting and routing AI workloads before they reach a model. Public work must preserve KORA's claim boundaries and evidence limits.

## Public Truth And Worktrees

- Public truth is `origin/main`.
- New public work must start from a fresh clean worktree under `/Users/albertkim/02_PROJECTS/05_KORA_Project/worktrees/`.
- Do not use the legacy dirty repo `/Users/albertkim/02_PROJECTS/05_KORA`.
- Do not mutate dirty local `main`.
- Do not touch local-only ChatGPT context under `/Users/albertkim/02_PROJECTS/05_KORA_Project/local/chatgpt_context/` during public PR work.

## Inner Loop Ownership

Codex owns the repo-grounded inner development loop:

1. Read repo-local operating docs and the current goal prompt.
2. Confirm the base SHA, branch, allowed files, forbidden files, and validation commands.
3. Implement within scope.
4. Validate.
5. Repair safely within the allowed scope when validation fails.
6. Self-review changed files, claims, breadcrumbs, reports, and forbidden actions.
7. Classify the completed work block.
8. Produce an approval packet.
9. Open a PR and stop.

ChatGPT and Albert are escalation and approval gates, not micro-task schedulers for ordinary bounded implementation details.

## Completion Classifications

Codex pass is not merge-ready pass. Every completed work block must end with exactly one of:

- `merge-ready`
- `needs-r1`
- `needs-cto-review`
- `blocked`

Do not mark `merge-ready` merely because tests passed. If semantic, claim, scope, evidence, release, provider, H100/server, file-movement, multi-agent, or public-positioning risk remains, classify the work as `needs-cto-review` or `blocked`.

## Required Validation And Self-Review

Before PR creation, Codex must:

- confirm changed files match the allowed scope.
- confirm forbidden files and actions were not touched.
- run the required validation commands or stop with a clear failure.
- update required report and breadcrumb docs.
- run claim-boundary review.
- confirm local-only ChatGPT context is unchanged.
- confirm no provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, or production validation were added.
- confirm no release, tag, GitHub Release, PyPI publication, repo settings, issues, project boards, collaborator changes, raw artifacts, or file movement occurred.

## Hard Approval Gates

Stop for explicit Albert approval before:

- merge.
- release, tag, GitHub Release, release asset, or PyPI publication.
- repository settings, metadata, issues, project boards, or collaborator changes.
- provider calls.
- H100/GPU/CUDA/server/remote execution.
- model inference.
- semantic judging or human grading.
- production validation.
- public claim expansion.
- major file movement, archive, delete, or rename work.
- large public-facing document replacement.
- local-only ChatGPT context changes.

## Claim Boundaries

Do not claim:

- output-quality proof.
- broader workload representativeness proof.
- production proof.
- production cost reduction.
- customer savings.
- H100/GPU/CPU superiority.
- provider replacement or GPU-serving replacement.
- that `getkora` is published.

## PR Completion Expectations

Every PR should include:

- summary.
- changed files.
- validation results.
- loop count and repair attempts.
- final status classification.
- risk level.
- approval packet.
- safety boundary confirmation.
- claim boundary confirmation.
- explicit note that the PR is open only and not merged.
