# Codex Multi-Agent Operating Model

Status: future operating rules only. This file does not create actual multi-agent automation.

## Core Principles

- One writer per branch.
- Reviewer/checker agents are read-only by default.
- Multiple builders require separate worktrees, separate branches, non-overlapping allowed files, and separate PRs.
- No auto-merge.
- Integrator and merge roles are human-gated.
- Any high-risk finding forces `needs-cto-review` or `blocked`.

## Roles

### Builder

The builder role may implement within allowed files, run approved validation, repair within limits, update reports, and open a PR.

### Reviewer

The reviewer role may inspect diff, tests, docs, reports, and approval packet. Reviewer agents are read-only by default and must not modify files unless assigned a separate R1 patch task.

### Test Planner

The test-planner role may propose missing tests but must not edit files by default.

### Claim Auditor

The claim-auditor role may scan for claim-boundary risk and must escalate unsupported claims.

### Integrator

The integrator or merge role is human-gated. No agent may merge without explicit Albert approval.

## Required Separation

Multiple builders require:

- separate worktrees.
- separate branches.
- non-overlapping allowed files.
- separate PRs.
- explicit coordination through approval packets.

## Hard Boundaries

The multi-agent operating model forbids:

- provider calls.
- H100/GPU/CUDA/server/remote execution.
- repository settings changes.
- releases, tags, GitHub Releases, or PyPI publication.
- GitHub issues, project boards, or collaborator changes.
- auto-merge.
- self-merging agents.
- background execution.
- claim expansion.

## Claim Boundary Reminder

Multi-agent review does not create output-quality proof, broader workload representativeness proof, production proof, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, or published `getkora` claims.
