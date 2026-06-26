# Project Documentation Refresh Prompt

Use this prompt after a completed task to refresh the breadcrumb layer.

```text
You are acting as the execution agent for a project documentation refresh task.

Goal:
Refresh the project breadcrumb and review hub after the latest completed task.

Start by reading:
- OPEN_THIS_FIRST.md
- REVIEW_HUB.md
- latest task report
- latest generated evidence, if any
- claim registry, if present

Update:
- OPEN_THIS_FIRST.md
- REVIEW_HUB.md

Continuation rule:
- OPEN_THIS_FIRST.md is the single source of human continuation.
- REVIEW_HUB.md is the detailed second stop.
- Every completed task must refresh both unless explicitly exempted.

Update at minimum:
- latest completed task
- current branch/worktree/commit
- primary report
- primary evidence
- current state summary
- changed risks
- changed evidence gaps
- supported and unsupported claims
- recommended next task
- how to resume

Preserve:
- public/private boundaries
- unsupported-claim boundaries
- neutral role language
- links to primary evidence and reports

Do not expose:
- private paths
- credentials
- hostnames
- raw access details
- raw provider responses
- raw infrastructure logs
- account IDs
- billing details
- local-only notes

Validation:
- run link/path sanity checks for changed docs
- run scans for private material and unsupported claims
- run tests if the task changed code or generated evidence
- run whitespace/diff checks

Create a short refresh report if requested.
Commit only public-safe files.
Do not push, open PR, tag, or release unless explicitly requested.
```
