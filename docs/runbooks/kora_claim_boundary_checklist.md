# KORA Claim-Boundary Checklist

Status: KORA-specific public claim gate for Codex and reviewer use.

## Purpose

Use this checklist before committing, opening a PR, approving a PR, or preparing a merge gate. It keeps KORA public language tied to evidence and prevents scoped route, fixture, and documentation work from becoming unsupported product claims.

## Required Checks

For every changed public file, verify that the change does not add or imply:

- production readiness unless explicitly proven and approved.
- production workload proof unless explicitly proven and approved.
- production cost reduction proof.
- real API-cost proof.
- real GPU-cost proof.
- H100, GPU, or CPU superiority.
- both-GPU active-use or multi-GPU scaling unless directly proven and approved.
- output-quality proof from route-only counters.
- broader workload representativeness proof from Goal 103 route-only counters.
- customer savings.
- provider replacement.
- model-serving replacement.
- GPU-serving replacement.
- published `getkora` availability.
- unapproved merge, release, or self-approval.

## KORA-Safe Language

Preferred phrases:

- "bounded loop"
- "semi-autonomous execution"
- "human approval gates"
- "PR-open then stop"
- "claim-boundary review"
- "source-refresh after merge"
- "route-only aggregate seed analysis"
- "public-safe fixture"
- "shape-validated seed analysis"

Avoid phrases that imply unsupported autonomy, production proof, publication, or superiority.

## Route-Only Evidence Boundary

Goal 103 route-only counters support only aggregate route/counter inspection over the public-safe synthetic seed fixture.

They do not support:

- output quality.
- broad workload representativeness.
- production workload handling.
- production readiness.
- cost reduction.
- provider replacement.
- H100/GPU/CPU superiority.

## Infrastructure Boundary

Before committing or opening a PR, confirm:

- no provider calls were added or performed.
- no H100/GPU/CUDA/server/remote execution was added or performed.
- no model inference was added or performed.
- no raw provider responses were added.
- no raw GPU logs or infrastructure logs were added.
- no hostnames, IP addresses, SSH paths, credentials, tokens, billing details, or private infrastructure details were added.

## Repository Action Boundary

Before completion, confirm no unapproved:

- merge.
- release.
- tag.
- GitHub Release.
- PyPI or package publication.
- repository settings change.
- repository metadata change.
- issue or project-board creation.
- raw benchmark artifact upload.
- file move, rename, archive, or delete operation.
- local-only ChatGPT context commit.

## Changed-File Scan

Use changed-file-only review first:

```bash
git diff --name-only
git diff --check
```

Then review changed Markdown for risky terms in context. The presence of a prohibited phrase inside a non-claim list can be acceptable, but the surrounding wording must clearly say the claim is not supported.

## Completion Statement

Every Goal PR body and final Codex response should include a boundary audit such as:

```text
Boundary audit: no provider calls, H100/GPU/CUDA/server/remote execution, model inference, output-quality proof, broader workload representativeness proof, production proof, superiority/customer-savings/provider-replacement claims, releases, tags, publications, repository settings changes, raw artifacts, file moves, renames, archives, deletes, or local-only context commits were added or performed.
```
