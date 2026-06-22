# KORA PR Completion Format

Status: required completion shape for KORA Codex PR-open tasks.

## Purpose

This format keeps KORA PRs and final responses reviewable. It records what changed, what was validated, what was not claimed, and where Codex stopped.

## Final Response Shape

Start with the exact implemented-task label from the goal prompt. Example:

```text
Implemented Task 104
```

Then include:

- PR URL.
- branch name.
- head SHA.
- base SHA.
- changed files.
- runbooks, reports, or evidence added.
- validation results.
- boundary audit results.
- explicit non-claims.
- stop-gate confirmation.
- next recommended task.

## PR Body Shape

Use this structure for KORA PR bodies:

```markdown
# <Goal title>

## Summary

- <High-signal change 1>
- <High-signal change 2>
- <High-signal change 3>

## Files changed

- `<path>`
- `<path>`

## Validation

- `<command>` - passed
- `<command>` - passed

## Boundary audit

- No provider calls added or performed.
- No H100/GPU/CUDA/server/remote execution added or performed.
- No model inference added or performed.
- No output-quality proof added.
- No broader workload representativeness proof added.
- No production proof, superiority, customer-savings, provider-replacement, or GPU-serving replacement claims added.
- No release, tag, GitHub Release, PyPI/package publication, repository settings change, issue/project-board creation, raw artifact upload, file move, rename, archive, or delete operation performed.
- No local-only ChatGPT context files modified or committed.

## Explicit non-claims

This PR does not prove production readiness, production workload handling, production cost reduction, real API/GPU cost reduction, output quality, broader workload representativeness, H100/GPU/CPU superiority, both-GPU active use, multi-GPU scaling, customer savings, provider replacement, GPU-serving replacement, or published `getkora`.

## Stop-gate confirmation

This PR is open only and not merged. Merge, release, publication, repository settings changes, claim expansion, provider calls, H100/GPU/server execution, file movement, and local source refresh require separate explicit approval.
```

## Fix-Loop Response Shape

For cleanup commits on the same PR, start with the exact cleanup label requested by the reviewer. Include:

- PR URL.
- new head SHA.
- changed files.
- exact fix made.
- validation rerun.
- boundary confirmation.
- confirmation that the PR remains open and not merged.

## Merge-Gate Response Shape

For a separate merge-gate task, start with the exact merge-gate completion label requested by the prompt. Include:

- PR URL.
- merged or not merged status.
- merge commit SHA, if merged.
- new `origin/main` HEAD, if merged.
- pre-merge head SHA verified.
- validation results.
- changed files confirmed.
- explicit non-claims confirmed.
- confirmation that no release, tag, GitHub Release, PyPI/package publication, repository settings change, issue/project-board creation, release asset, raw artifact, or unapproved file movement occurred.
- next required task, usually local ChatGPT source refresh after merge.

## Local Source Refresh Response Shape

For a separate local-only source refresh task, include:

- files updated under `/Users/albertkim/02_PROJECTS/05_KORA_Project/local/chatgpt_context/`.
- public HEAD verified.
- refresh reason.
- latest goal summary added.
- claim boundaries preserved.
- confirmation that no public repo files were modified.
- confirmation that nothing was staged or committed.
- next recommended task.
