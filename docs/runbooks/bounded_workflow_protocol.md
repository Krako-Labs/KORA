# Implementation Workflow Bounded Loop Protocol

Status: KORA-specific operating protocol for semi-autonomous execution with human approval gates.

## Purpose

This runbook defines how KORA uses planning gate, implementation workflow, and Albert across scoped implementation, validation, documentation, audit, and PR-opening work.

The protocol is a bounded loop: the implementation workflow may execute a scoped goal through PR-open, then stop. It does not authorize merge, release, publication, repository settings changes, claim expansion, provider calls, H100 execution, file movement, or major public narrative rewrites without an explicit later approval gate.

## Role Split

The planning gate is responsible for:

- planning the goal envelope.
- writing or refining workflow guides.
- reviewing implementation workflow output and PRs.
- identifying stale breadcrumbs, weak validation, scope drift, and missing claim boundaries.
- keeping claim boundaries explicit.
- advising on merge, release, or source-refresh gates.

The implementation workflow is responsible for:

- verifying repository identity, branch, base SHA, and clean worktree state.
- implementing scoped public-safe changes.
- running validation.
- auditing changed files for claim-boundary and public/private risks.
- updating `OPEN_THIS_FIRST.md`, `REVIEW_HUB.md`, and task reports when the goal requires them.
- opening a PR when requested.
- stopping after PR-open unless a separate merge-gate request text is provided.

Albert is the approval gate for:

- merge.
- release, tags, GitHub Releases, release assets, or PyPI/package publication.
- repository settings, metadata, or topic changes.
- public claim expansion.
- public-facing strategy changes.
- file moves, renames, archival, or deletion.
- raw benchmark artifact upload.
- provider calls.
- H100/GPU/CUDA/server/remote execution.

## Standard Bounded Loop

Use this loop for KORA implementation, documentation, evidence, and PR-open goals:

1. Read the attached goal brief completely.
2. Fetch `origin`.
3. Verify `origin/main` exactly matches the base SHA in the brief.
4. Verify KORA GitHub identity when GitHub mutation is possible: `GH_CONFIG_DIR="$HOME/.config/gh-hkalbertkim"` and login `hkalbertkim`.
5. Verify git author is `Albert Kim <hkalbert71@gmail.com>`.
6. Create or enter the scoped clean worktree requested by the brief.
7. Confirm the worktree is clean and is not the dirty source checkout or legacy repo.
8. Read `OPEN_THIS_FIRST.md`, `REVIEW_HUB.md`, and goal-specific source files.
9. Implement only the scoped change.
10. Run requested validation and any relevant fast checks.
11. Run the claim-boundary audit in [KORA claim-boundary checklist](kora_claim_boundary_checklist.md).
12. Update `OPEN_THIS_FIRST.md` and `REVIEW_HUB.md` unless explicitly exempted.
13. Add a goal report under `docs/reports/` when requested.
14. Check `git diff --check`.
15. Check changed files for public/private and claim-boundary issues.
16. Commit only intended public-safe files.
17. Push the branch.
18. Open the PR with summary, validation, boundary audit, non-claims, and stop-gate confirmation.
19. Stop.

## Required Stop Gates

Stop and request or wait for explicit approval before any of these actions:

- squash merge, merge commit, rebase merge, or branch deletion tied to a merge.
- release, tag, GitHub Release, release asset, or PyPI/package publication.
- repository settings, metadata, topics, homepage, visibility, or branch protection changes.
- issue or project-board creation unless the task brief explicitly approves it.
- raw benchmark artifact upload.
- provider calls to OpenAI, Anthropic, Gemini, local model servers, or other inference providers.
- H100/GPU/CUDA/server/remote execution.
- model inference.
- file moves, renames, archival, or deletion.
- claim expansion beyond the approved evidence.
- public-facing README or major narrative rewrite beyond the goal scope.
- local-only project context refresh after merge, unless the task brief is specifically a local-only source refresh task.

## Fix-Loop Behavior

If planning gate or review feedback finds stale breadcrumbs, missing claim boundaries, weak validation, broken links, or scope drift:

1. Patch the same PR branch.
2. Keep the patch scoped to the review finding.
3. Rerun the relevant validation slice.
4. Push the update.
5. Stop again.

Do not merge after a fix-loop patch unless a separate merge-gate request text is provided.

## Local Source Refresh After Merge

After a PR is merged, run a separate local-only source refresh task when requested.

Local source refresh rules:

- update only files under `/Users/albertkim/02_PROJECTS/05_KORA_Project/local/project_context/`.
- prefer the canonical files `project_source.md` and `source_manifest.md`.
- leave `project_instructions.md` unchanged unless it is clearly stale and the task brief allows a narrow factual refresh.
- never commit local-only files.
- never use local-only files as public repo source material without public-safe rewriting and approval.

## Completion Format

Use [KORA PR completion format](kora_pr_completion_format.md) for final implementation workflow responses and PR bodies.

Completion must identify:

- exact implemented-task label.
- PR URL.
- branch.
- head SHA.
- base SHA.
- changed files.
- validation results.
- boundary audit results.
- explicit non-claims.
- stop-gate confirmation.
- next recommended task.
