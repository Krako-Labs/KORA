# Goal 104 Codex Bounded Loop Protocol

Status: KORA-specific bounded-loop protocol added; documentation/protocol only.

## Objective

Goal 104 adds public-safe runbooks for how KORA should use ChatGPT, Codex, and Albert across scoped implementation, validation, documentation, audit, PR opening, review cleanup, merge gates, and local source refresh.

This is a documentation/protocol goal. It adds no runtime feature code and no executable automation.

## Why This Follows Goal 103

Goal 103 introduced a route-only evaluator, then needed a cleanup pass, a merge-gate pass, and a local-only source refresh after merge. That sequence worked, but it exposed a repeatable operating pattern:

- PR-open implementation should stop before merge.
- stale breadcrumb cleanup should patch the same PR and stop again.
- merge requires a separate merge-gate prompt.
- local ChatGPT source refresh belongs after merge and must stay local-only.
- route-only evidence must not become output-quality or broader representativeness claims.

Goal 104 turns that pattern into a reusable KORA protocol.

## Files Added Or Updated

Added:

- [Codex bounded loop protocol](../runbooks/codex_bounded_loop_protocol.md)
- [KORA claim-boundary checklist](../runbooks/kora_claim_boundary_checklist.md)
- [KORA PR completion format](../runbooks/kora_pr_completion_format.md)
- [KORA next goal queue](../context/NEXT_GOAL_QUEUE.md)

Updated:

- [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [REVIEW_HUB.md](../../REVIEW_HUB.md)
- [Documentation index](../README.md)
- [Project Operating System README](../project-operating-system/README.md)

## Bounded-Loop Phases

1. Read the goal brief and source docs.
2. Verify `origin/main`, base SHA, KORA identity, branch, and clean worktree.
3. Implement only the scoped change.
4. Run requested validation.
5. Run claim-boundary and public/private audits.
6. Update `OPEN_THIS_FIRST.md`, `REVIEW_HUB.md`, and the goal report.
7. Commit public-safe files only.
8. Push the branch.
9. Open the PR.
10. Stop.

## Stop Gates

The protocol requires explicit human approval before:

- merge.
- release, tag, GitHub Release, release asset, or PyPI/package publication.
- repository settings, metadata, or topic changes.
- issue or project-board creation unless approved.
- raw benchmark artifact upload.
- provider calls.
- H100/GPU/CUDA/server/remote execution.
- model inference.
- file moves, renames, archival, or deletion.
- claim expansion.
- public-facing README or major narrative rewrite beyond the goal scope.
- local-only source refresh after merge.

## Claim-Boundary Checklist Summary

The checklist preserves these non-claims unless later evidence and approval change them:

- no production readiness.
- no production workload proof.
- no production cost reduction proof.
- no real API-cost proof.
- no real GPU-cost proof.
- no H100/GPU/CPU superiority.
- no both-GPU active-use or multi-GPU scaling claim unless directly proven.
- no output-quality proof from route-only counters.
- no broader workload representativeness proof from Goal 103 route-only counters.
- no customer savings.
- no provider replacement.
- no GPU-serving replacement.
- no published `getkora`.

## Validation Performed

- `python3 scripts/check_markdown_links_goal082b.py` - passed.
- `git diff --check` - passed.
- `python3 -m pytest` - `406 passed`.

## Explicit Non-Claims

Goal 104 does not:

- make Codex self-approving.
- authorize unapproved merge or release.
- add runtime feature code.
- add provider calls.
- add H100/GPU/CUDA/server/remote execution.
- add model inference.
- add output-quality proof.
- add broader workload representativeness proof.
- add production proof.
- add superiority, customer-savings, provider-replacement, or GPU-serving replacement claims.
- publish `getkora`.
- move, rename, archive, or delete files.
- modify or commit local-only ChatGPT context files.

## Next Recommended Goal

Recommended next goal:

- Goal 105 - Apply the Codex bounded-loop protocol to the next approved KORA task.

Alternative next goals require explicit approval and should start from the queue in [KORA next goal queue](../context/NEXT_GOAL_QUEUE.md).
