# implementation workflow Inner Loop Queue

Status: repo-local planning queue for future implementation-workflow-owned bounded work blocks.

This queue records public-safe and local-only work blocks. It is not approval to merge, release, call providers, execute H100/server work, or expand claims.

## Queue Hardening Policy

Future queue items should be sized as coherent control blocks rather than 5-15 minute micro-tasks.

Each new or revised queue item should record an expected duration band:

- `30-60 min`
- `1-2 hr`
- `2-4 hr`
- `half-day`

Bundling policy:

- low-risk adjacent checkers may be bundled when they share the same input surface, validation path, report, and claim boundary.
- medium-risk command-surface changes should not be bundled with unrelated work.
- high-risk work must not be bundled.

Micro-task prevention:

- do not split a checker, tests, docs, report, and breadcrumb into separate tasks unless separation is necessary for risk or ownership.
- prefer coherent control blocks that leave one reviewable report and one clear approval packet.
- every PR should leave the next queue state clearer than before.

Stop conditions:

- if work becomes high-risk, stop and classify `needs-cto-review` or `blocked`.
- if validation requires unsafe broadening, stop.
- if command execution, GitHub mutation, provider/H100/server execution, report-command execution, or claim expansion becomes necessary, stop.

Review friction reduction:

- every future work block should be checkable with the Group 111 report verifier/classifier and Group 112 approval-packet/report-consistency checkers when applicable.
- queue items should name the expected report, validation commands, final classification options, and approval-gated follow-up.

## Queue Items

### Primary Candidate - Group 121 Bounded Local Validation Evidence Control Block

- task id: `GROUP-121`
- title: Bounded local validation evidence control block
- objective: improve the bounded local validation evidence path around report generation, static report verification, deterministic failure classification, focused tests, and review closeout.
- expected duration band: `2-4 hr`.
- risk level: medium.
- why this is not a micro-task: the candidate should include implementation, focused tests, generated or sample validation evidence, report documentation, breadcrumbs, queue closeout, and final self-review in one coherent control block.
- why it advances the long-work-block goal: it turns the current validation/reporting surface into a practical multi-hour reviewable task instead of another small isolated wording, link, or queue repair.
- allowed files/families: `scripts/run_bounded_local_validation.py`, `scripts/verify_bounded_local_validation_report.py`, `scripts/classify_bounded_local_validation_failure.py`, `scripts/check_report_consistency.py` only if needed for this candidate, focused tests for those scripts, one Group 121 report under `docs/reports/`, and narrow updates to `OPEN_THIS_FIRST.md`, `REVIEW_HUB.md`, `docs/README.md`, `docs/context/WORKFLOW_QUEUE.md`, and `docs/context/NEXT_GOAL_QUEUE.md`.
- forbidden files/actions: no `CIL-003`, no validation profile registry changes, no command profile registry changes, no dynamic command discovery, no user-provided command execution, no provider calls, no H100/GPU/CUDA/server/remote execution, no model inference, no semantic judging or human grading, no package/release behavior, no repository settings, no issues/project boards, no file movement, no local-only project context, and no claim expansion.
- validation commands: focused pytest for changed validation/reporting scripts; `python3 scripts/run_bounded_local_validation.py --profile kora-local-core --dry-run --json-out <temp-report>` if the approved future task keeps the existing profile unchanged; `python3 scripts/verify_bounded_local_validation_report.py <temp-report> --profile kora-local-core`; `python3 scripts/classify_bounded_local_validation_failure.py <temp-report> --profile kora-local-core`; `python3 scripts/validate_workflow_docs.py`; `python3 scripts/check_markdown_links_goal082b.py`; `git diff --check`; changed-file claim and public wording audits.
- expected final classification: `needs-cto-review` unless the approved future request is narrowed to documentation-only maintenance.
- claim boundaries: local validation/reporting workflow evidence only; no output-quality proof, broader workload representativeness proof, production proof, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, or published package claim.
- stop gate: open PR only, then stop. Merge, release, publication, settings changes, issues/project boards, local-only source refresh, and any follow-on queue item require separate explicit approval.
- CTO review expected: yes, because the candidate affects validation evidence workflow and final review interpretation.

### Parked Candidates

- `CIL-003` remains deferred and may be considered only after explicit approval using [implementation workflow medium-risk profile registry checklist](MEDIUM_RISK_PROFILE_REGISTRY_CHECKLIST.md).
- another bounded public-safe fixture/check slice remains parked until the validation/reporting evidence path is easier to review.
- documentation movement for one small bucket remains parked because file moves, renames, archival, or deletion require separate explicit approval.
- local-only source refresh remains a separate private task and must not be committed to the public repository.
- provider, H100, GPU, server, remote, semantic, human, or production-like validation remains behind separate explicit approval.

### CIL-001 - Bounded Validation Report Verifier

- task id: `CIL-001`
- title: Bounded validation report verifier
- objective: verify JSON reports produced by `scripts/run_bounded_local_validation.py` without executing report commands.
- risk level: low.
- allowed files: `scripts/verify_bounded_local_validation_report.py`, `tests/test_bounded_local_validation_report_verifier.py`, `docs/reports/*bounded*validation*report*verifier*.md`, narrow breadcrumbs.
- forbidden files/actions: no local-only project context, no GitHub Actions workflow, no provider calls, no H100/GPU/CUDA/server/remote execution, no arbitrary shell execution, no report-command execution.
- validation commands: verifier tests, runner tests, dry-run runner, verifier on generated report, markdown links, `git diff --check`, full pytest.
- repair limits: max loop count 5; max repair attempts per failing subtask 2.
- expected outputs: verifier CLI, focused tests, report, approval packet.
- Group 111 status: completed by `workflow/group111-validation-report-control-block`; PR #261 was inspected and left untouched because it was conflicted after Group 110.
- stop gates: unknown profile semantics, command execution risk, claim expansion.
- claim boundaries: report structure only; no output-quality proof, broader workload representativeness proof, production proof, or production validation.
- completion status expected: `merge-ready` only if no command-execution or claim risk remains; otherwise `needs-r1` or `needs-cto-review`.

### CIL-002 - Bounded Validation Failure Classifier

- task id: `CIL-002`
- title: Bounded validation failure classifier
- objective: classify failed bounded validation reports into deterministic failure categories for triage.
- risk level: low.
- allowed files: new classifier script, focused tests, report docs, narrow breadcrumbs.
- forbidden files/actions: no auto-repair, no scheduler, no daemon, no background runner, no report-command execution, no provider/H100/server execution.
- validation commands: focused classifier tests, dry-run runner, markdown links, `git diff --check`, full pytest.
- repair limits: max loop count 5; max repair attempts per failing subtask 2.
- expected outputs: classifier, tests, report, approval packet.
- Group 111 status: completed by `workflow/group111-validation-report-control-block` as part of the same static report-control block.
- stop gates: any attempt to infer semantic quality or execute failed commands.
- claim boundaries: failure classification only; no production validation or output-quality proof.
- completion status expected: `merge-ready` only for deterministic local classification over static report inputs.

### CIL-003 - Bounded Validation Profile Registry

- task id: `CIL-003`
- title: Bounded validation profile registry
- objective: make approved local validation profiles discoverable without enabling arbitrary user commands.
- risk level: medium.
- expected duration band: `1-2 hr` for checklist-only design; `2-4 hr` if implementation is explicitly approved later.
- allowed files: runner profile registry module, tests, report docs, narrow breadcrumbs.
- forbidden files/actions: no dynamic shell command loading, no external config execution, no provider/H100/server execution.
- validation commands: runner tests, registry tests, dry-run runner, markdown links, `git diff --check`, full pytest.
- repair limits: max loop count 5; max repair attempts per failing subtask 2.
- expected outputs: static profile registry, tests, report.
- approval checklist: [implementation workflow medium-risk profile registry checklist](MEDIUM_RISK_PROFILE_REGISTRY_CHECKLIST.md).
- Group 113 status: deferred; checklist added before execution.
- stop gates: any design that permits arbitrary command injection.
- claim boundaries: approved local validation profiles only; no production validation or broader workload proof.
- completion status expected: `needs-cto-review` unless the command surface remains clearly static and claim boundaries are unchanged.

### CIL-004 - First-Run CLI Smoke Validation Expansion

- task id: `CIL-004`
- title: First-run CLI smoke validation expansion
- objective: expand local first-run CLI smoke checks using existing offline commands.
- risk level: medium.
- expected duration band: `2-4 hr`.
- allowed files: smoke validation script/tests/report docs/narrow breadcrumbs.
- forbidden files/actions: no provider calls, no network-dependent smoke tests, no packaging publication, no broad README rewrite.
- validation commands: focused smoke tests, selected offline CLI commands, markdown links, `git diff --check`, full pytest.
- repair limits: max loop count 5; max repair attempts per failing subtask 2.
- expected outputs: smoke checks, tests, report, approval packet.
- Group 114 status: completed by `workflow/group114-first-run-cli-smoke-validation` with a static local-only `first-run-cli-core` smoke profile.
- stop gates: public install-claim expansion, release/PyPI implication, network dependency.
- claim boundaries: local source-install readiness only; no published package claim.
- completion status expected: `needs-cto-review` because first-run validation can affect public onboarding confidence.

### CIL-005 - Source-Install Readiness Check

- task id: `CIL-005`
- title: Source-install readiness check
- objective: verify source-install readiness from local repo state without publishing packages.
- risk level: medium.
- allowed files: readiness checker, tests, report docs, narrow breadcrumbs.
- forbidden files/actions: no PyPI publication, no tag, no release asset, no repo settings, no external publication.
- validation commands: focused readiness tests, source-install smoke in local environment if approved by request text, markdown links, `git diff --check`, full pytest.
- repair limits: max loop count 5; max repair attempts per failing subtask 2.
- expected outputs: readiness checker, report, approval packet.
- Group 115 status: completed by `workflow/group115-source-install-readiness` with an isolated local temporary-venv checker over editable source install, import, module CLI, console script, and no-provider command smoke.
- stop gates: package publication, external index upload, claim that `getkora` is published.
- claim boundaries: local source-install readiness only; no release or publication claim.
- completion status expected: `needs-cto-review` if user-facing install docs change.

### CIL-006 - PR Approval Packet Checker

- task id: `CIL-006`
- title: PR approval packet checker
- objective: validate that PR reports include decision needed, risk level, final status classification, changed files, validation, repair attempts, failures, self-review, claim-boundary audit, forbidden-action audit, uncertainty notes, recommendation, and Albert action options.
- risk level: low.
- allowed files: approval packet checker script, tests, docs, narrow breadcrumbs.
- forbidden files/actions: no GitHub mutation beyond PR creation in the scoped task, no merge, no issue/project board creation.
- validation commands: focused checker tests, markdown links, `git diff --check`, full pytest.
- repair limits: max loop count 5; max repair attempts per failing subtask 2.
- expected outputs: checker, tests, report.
- Group 112 status: completed by `workflow/group112-approval-report-consistency`.
- stop gates: any automatic approval or merge recommendation not backed by risk classification.
- claim boundaries: packet completeness only; no quality/prod proof.
- completion status expected: `merge-ready` if deterministic and narrow.

### CIL-007 - Report Consistency Checker

- task id: `CIL-007`
- title: Report consistency checker
- objective: check that goal reports, breadcrumbs, and next-goal queues agree on goal id, branch, PR, validation, boundaries, and final classification.
- risk level: low.
- allowed files: consistency checker, tests, docs, narrow breadcrumbs.
- forbidden files/actions: no rewriting reports automatically, no file movement, no claim expansion.
- validation commands: focused consistency tests, markdown links, `git diff --check`, full pytest.
- repair limits: max loop count 5; max repair attempts per failing subtask 2.
- expected outputs: checker, tests, report.
- Group 112 status: completed by `workflow/group112-approval-report-consistency`.
- stop gates: checker attempts to infer claims beyond literal docs.
- claim boundaries: document consistency only; no production proof or output-quality proof.
- completion status expected: `merge-ready` if checker is read-only and deterministic.

## Standing Claim Boundary

All queue items must preserve KORA's claim boundaries: no output-quality proof, broader workload representativeness proof, production proof, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, or published `getkora` claim.
