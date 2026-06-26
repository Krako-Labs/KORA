# Group 120 Long Work Block Candidate Selection

Status: implemented with local validation complete; PR open.

## Objective

Group 120 refreshes the public continuation state after merged PR #272 and rebuilds the next-work queue around one bounded long work block candidate.

This group is planning, queue, breadcrumb, and report documentation only. It does not implement the selected candidate, implement `CIL-003`, change runtime behavior, change validation profile registries, change command profile registries, call providers, run H100/GPU/CUDA/server/remote work, perform model inference, perform semantic judging or human grading, change package or release behavior, or expand public claims.

## Public State

- public truth: `origin/main`
- starting public HEAD: `824ef643fb1d2aba40800d882c12ab5ccde32e57`
- branch: `Group 120 long work block queue PR branch`
- PR: https://github.com/Krako-Labs/KORA/pull/273
- latest merged PR: PR #272, Group 119 public operations wording scrub
- Group 119 state: completed and merged
- `CIL-003` state: deferred

Group 119 remains public operations wording hygiene only. It neutralized public workflow wording and path names without changing runtime, provider, package, release, validation-profile, command-profile, or claim boundaries.

## Selected Candidate

Candidate name: Group 121 - Bounded Local Validation Evidence Control Block.

Expected duration band: `2-4 hr`.

Candidate risk level: medium.

Expected final classification: `needs-cto-review` unless a future explicit request narrows the work to documentation-only maintenance.

CTO review expected: yes, because the candidate affects validation evidence workflow and review interpretation even if implementation remains local and bounded.

## Candidate Scope

Objective:

- improve the bounded local validation evidence path around report generation, static report verification, deterministic failure classification, focused tests, report documentation, and review closeout.

Allowed files and families:

- `scripts/run_bounded_local_validation.py`
- `scripts/verify_bounded_local_validation_report.py`
- `scripts/classify_bounded_local_validation_failure.py`
- `scripts/check_report_consistency.py` only if needed for this candidate
- focused tests for changed validation/reporting scripts
- one Group 121 report under `docs/reports/`
- narrow breadcrumb and queue updates in `OPEN_THIS_FIRST.md`, `REVIEW_HUB.md`, `docs/README.md`, `docs/context/WORKFLOW_QUEUE.md`, and `docs/context/NEXT_GOAL_QUEUE.md`

Forbidden files and actions:

- no `CIL-003`
- no validation profile registry changes
- no command profile registry changes
- no dynamic command discovery
- no user-provided command execution
- no provider calls
- no H100/GPU/CUDA/server/remote execution
- no model inference
- no semantic judging or human grading
- no production validation
- no package or release behavior
- no repository settings changes
- no issue or project-board creation
- no file movement, rename, archive, or deletion
- no local-only project context changes
- no public claim expansion

## Validation For Future Candidate

The future Group 121 task should use only commands explicitly approved in its request text. The expected validation set is:

| Command | Purpose |
| --- | --- |
| `python3 -m pytest <focused validation/reporting tests> -q` | focused tests for changed scripts |
| `python3 scripts/run_bounded_local_validation.py --profile kora-local-core --dry-run --json-out <temp-report>` | dry-run report generation if the existing profile remains unchanged |
| `python3 scripts/verify_bounded_local_validation_report.py <temp-report> --profile kora-local-core` | static report verification |
| `python3 scripts/classify_bounded_local_validation_failure.py <temp-report> --profile kora-local-core` | deterministic report classification |
| `python3 scripts/validate_workflow_docs.py` | workflow documentation validation |
| `python3 scripts/check_markdown_links_goal082b.py` | Markdown link validation |
| `git diff --check` | whitespace validation |
| changed-file claim and public wording audits | public boundary validation |

Stop if any needed validation requires provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, profile registry changes, command registry changes, package publication, repository settings changes, or claim expansion.

## Why This Avoids Micro-Task Collapse

The candidate is intentionally larger than a link repair, wording cleanup, or single checker tweak. It should combine:

- a bounded implementation change.
- focused tests.
- local dry-run evidence where approved.
- static report verification/classification checks.
- a report and approval packet.
- breadcrumb and queue closeout.

That produces one reviewable control block with a practical 2-4 hour shape and a clear stop gate.

## Rejected Or Parked Candidates

`CIL-003` bounded validation profile registry:

- parked because it touches the validation command/profile surface.
- remains deferred unless Albert explicitly approves the medium-risk profile-registry checklist.

Another public-safe fixture/check slice:

- parked because the fixture evidence path already has recent Group 116 and Group 117 slices.
- useful later, but less directly aligned with the long-work-block queue rebuild than improving validation/reporting evidence workflow.

Documentation movement for one small bucket:

- parked because Group 120 does not authorize file movement, rename, archival, or deletion.

Local-only source refresh:

- parked as a separate private task.
- not a public repository queue implementation item.

Provider, H100, GPU, server, remote, semantic, human, or production-like validation:

- parked behind separate explicit approval.
- not part of Group 120 or the selected Group 121 candidate.

## Breadcrumb Updates

Group 120 updates the public breadcrumbs so they record Group 119 as completed and Group 120 as the current queue rebuild.

Updated state:

- Group 119 is completed and merged in PR #272.
- current public HEAD is `824ef643fb1d2aba40800d882c12ab5ccde32e57`.
- current continuation work is Group 120 queue rebuild.
- next recommended work is Group 121 bounded local validation evidence control block.
- `CIL-003` remains deferred.

## Claim Boundaries

Group 120 does not prove:

- output quality.
- broader workload representativeness.
- production readiness.
- production workload handling.
- production validation.
- production cost reduction.
- real API-cost reduction.
- real GPU-cost reduction.
- H100/GPU/CPU superiority.
- customer savings.
- provider replacement.
- GPU-serving replacement.
- published package availability.

Group 120 does not claim `getkora` is published and does not claim install-from-PyPI support.

## Approval Packet

Decision needed: review Group 120 queue rebuild and decide whether to merge.

Risk level: low

Final status classification: `merge-ready`

Changed files: `OPEN_THIS_FIRST.md`, `REVIEW_HUB.md`, `docs/README.md`, `docs/context/WORKFLOW_QUEUE.md`, `docs/context/NEXT_GOAL_QUEUE.md`, and `docs/reports/group120_long_work_block_candidate_selection.md`.

Validation summary: workflow docs validation, Markdown link check, whitespace diff check, changed-file public wording audit, and neutral workflow path audit passed.

Repair attempts: 0.

Failures encountered: none.

Self-review summary: Group 120 is planning and queue documentation only; it updates stale post-Group-119 continuation state and selects one bounded future candidate without implementing it.

Claim-boundary audit: no output-quality proof, broader workload representativeness proof, production proof, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, published package claim, or install-from-PyPI claim added.

Forbidden-action audit: no `CIL-003` implementation, validation profile registry change, command profile registry change, runtime behavior change, provider call, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, production validation, package/release behavior, issue/project-board creation, repository settings change, file movement, local-only project context change, or public claim expansion was added or performed.

Uncertainty notes: future Group 121 implementation details still require explicit request text and bounded approval before execution.

workflow recommendation: Merge.

Albert action options: Merge / Request R1 / Stop / CTO Review.

## Validation Results

Final validation before PR open:

| Command | Result |
| --- | --- |
| `python3 scripts/validate_workflow_docs.py` | passed |
| `python3 scripts/check_markdown_links_goal082b.py` | passed |
| `git diff --check` | passed |
| focused disallowed public wording grep over changed files | passed, no hits |
| focused neutral workflow path grep over changed files | passed, neutral workflow paths present |

## Loop Count And Repairs

- loop count: 1
- repair attempts: 0

## Final Classification

Final status classification: `merge-ready`.

Rationale: Group 120 is a bounded queue and planning documentation update. It changes no runtime behavior, validation profile registries, command profile registries, package/release behavior, provider/H100/server/model behavior, or public claim boundaries.

## Next Recommendation

Recommended next action: approve or request R1 on Group 120. After Group 120 is merged or explicitly superseded, the next implementation candidate is Group 121 - Bounded Local Validation Evidence Control Block.

`CIL-003` remains deferred unless Albert explicitly approves the medium-risk profile-registry checklist.
