# Group 114 First-Run CLI Smoke Validation

Status: implemented with local validation complete; PR open.

## Objective

Group 114 implements `CIL-004 - First-Run CLI Smoke Validation Expansion`.

This group adds a deterministic local first-run CLI smoke checker over existing offline KORA commands, focused tests, and a public-safe report. It does not implement `CIL-003`, change the bounded validation profile registry, change command profiles, publish packages, call providers, run H100/server work, or expand claims.

## Approval Packet

Decision needed: review and decide whether to merge Group 114 first-run CLI smoke validation.

Risk level: medium

Final status classification: `needs-cto-review`

Changed files: first-run CLI smoke checker, focused tests, Group 114 report, inner-loop queue update, next-goal queue update, docs index, and narrow breadcrumbs.

Validation summary: focused smoke tests, dry-run smoke report, real local offline smoke run, Group 113 approval-packet and report-consistency checks, inner-loop docs validation, bounded local validation dry-run/report verifier/classifier, markdown links, whitespace diff check, and full pytest passed.

Repair attempts: 0.

Failures encountered: none.

Self-review summary: scope is deterministic local first-run CLI smoke validation, tests, report, and breadcrumbs; `CIL-004` is completed, `CIL-003` remains deferred, and no validation profile registry implementation was added.

Claim-boundary audit: no output-quality proof, broader workload representativeness proof, production proof, production validation, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, or published `getkora` claim added.

Forbidden-action audit: no `CIL-003` implementation, validation profile registry change, command profile registry change, dynamic shell loading, external config execution, user command text execution, provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, production validation, scheduler, daemon, background runner, GitHub Actions workflow, remote runner, provider-calling runner, H100 runner, self-merging agent, actual multi-agent execution, GitHub API mutation, PR approval, PR merge, PR close, issue creation, project-board update, repository settings change, collaborator change, release, tag, GitHub Release, PyPI publication, raw artifact upload, file movement, local-only ChatGPT context change, or claim expansion added.

Uncertainty notes: this group touches the local first-run validation surface, so it is classified as medium risk and `needs-cto-review` even though the implementation is deterministic and local-only.

Codex recommendation: CTO Review.

Albert action options: Merge / Request R1 / Stop / CTO Review.

## Base And Branch

- public truth: `origin/main`
- base public HEAD: `bbc673d256f005201925051310342fa78c4af4d2`
- branch: `codex/group114-first-run-cli-smoke-validation`
- worktree: `/Users/albertkim/02_PROJECTS/05_KORA_Project/worktrees/group114_first_run_cli_smoke_validation`
- PR: https://github.com/Krako-Labs/KORA/pull/266

## Queue-State Check

- `CIL-001`: completed by Group 111.
- `CIL-002`: completed by Group 111.
- `CIL-003`: remains deferred and was not run in Group 114.
- `CIL-004`: completed by Group 114.
- `CIL-005`: remains pending and separately approval-gated.
- `CIL-006`: completed by Group 112.
- `CIL-007`: completed by Group 112.

## Implementation Summary

Added `scripts/check_first_run_cli_smoke.py`.

The checker supports one default profile:

- `first-run-cli-core`

It records:

- command label.
- structured argv list.
- status: `passed`, `failed`, or `planned`.
- return code.
- elapsed seconds.
- stdout tail.
- stderr tail.
- aggregate totals.
- final status.

The checker uses static in-repo command definitions and executes subprocesses with `shell=False`. Unknown profiles fail closed with a nonzero exit code. Dry-run mode reports planned commands without executing subprocesses. By default, execution stops on the first failure. `--continue-on-failure` is available for explicit local diagnostics.

Optional report outputs:

- `--json-out`
- `--md-out`

The script does not load commands from external configuration, accept arbitrary user command text, call providers, require network access, run H100/GPU/server/remote execution, or mutate repository files during normal reporting except for explicit output paths supplied by the caller.

## Smoke Command List

The `first-run-cli-core` profile runs these existing offline commands:

| Order | Command |
| --- | --- |
| 1 | `python3 -m kora doctor examples/kora_doctor/customer_support_workload.json` |
| 2 | `python3 -m kora doctor --all examples/kora_doctor/` |
| 3 | `python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json` |
| 4 | `python3 examples/deterministic_classification/run.py` |
| 5 | `python3 examples/cache_reuse/run.py` |
| 6 | `python3 examples/rag_routing/run.py` |
| 7 | `python3 examples/agent_workflow_optimization/run.py` |

## Real Smoke Result

Observed real local smoke result:

- profile: `first-run-cli-core`
- final status: `passed`
- total commands: `7`
- passed commands: `7`
- failed commands: `0`
- planned commands: `0`

Observed dry-run smoke result:

- profile: `first-run-cli-core`
- final status: `planned`
- total commands: `7`
- planned commands: `7`
- passed commands: `0`
- failed commands: `0`

These results are local first-run smoke validation only. They do not prove output quality, production readiness, production workload handling, production cost reduction, broader workload representativeness, provider replacement, or published package availability.

## Files Added

- `scripts/check_first_run_cli_smoke.py`
- `tests/test_first_run_cli_smoke.py`
- `docs/reports/group114_first_run_cli_smoke_validation.md`

## Files Updated

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- `docs/README.md`
- `docs/context/CODEX_INNER_LOOP_QUEUE.md`
- `docs/context/NEXT_GOAL_QUEUE.md`

## Validation Results

Final validation before PR open:

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_first_run_cli_smoke.py` | passed, `13 passed` |
| `python3 scripts/check_first_run_cli_smoke.py --profile first-run-cli-core --dry-run --json-out /tmp/kora-group114-smoke-dry-run.json --md-out /tmp/kora-group114-smoke-dry-run.md` | passed; reported 7 planned commands |
| `python3 scripts/check_first_run_cli_smoke.py --profile first-run-cli-core --json-out /tmp/kora-group114-smoke.json --md-out /tmp/kora-group114-smoke.md` | passed; reported 7 passed commands |
| `python3 scripts/check_pr_approval_packet.py docs/reports/group113_inner_loop_applied_review_queue_hardening.md` | passed |
| `python3 scripts/check_report_consistency.py docs/reports/group113_inner_loop_applied_review_queue_hardening.md --breadcrumb OPEN_THIS_FIRST.md --breadcrumb REVIEW_HUB.md` | passed |
| `python3 scripts/validate_codex_inner_loop_docs.py` | passed |
| `python3 scripts/run_bounded_local_validation.py --profile kora-local-core --dry-run --json-out /tmp/kora-group114-bounded-dry-run.json` | passed |
| `python3 scripts/verify_bounded_local_validation_report.py /tmp/kora-group114-bounded-dry-run.json --profile kora-local-core` | passed |
| `python3 scripts/classify_bounded_local_validation_failure.py /tmp/kora-group114-bounded-dry-run.json --profile kora-local-core` | passed with `dry_run_only` classification |
| `python3 scripts/check_markdown_links_goal082b.py` | passed |
| `git diff --check` | passed |
| `python3 -m pytest` | passed, `487 passed` |

Expected full-suite baseline after Group 113 was `474 passed`; Group 114 observed `487 passed` after adding 13 first-run smoke tests.

## Loop Count And Repairs

- loop count: 1
- repair attempts: 0
- max loop count: 5
- max repair attempts per failing subtask: 2

## Risk And Final Classification

- risk level: medium
- final status classification: `needs-cto-review`

Rationale: this group is deterministic, local-only tooling plus tests and docs, but it touches the first-run validation surface and may influence public onboarding confidence. It does not change README claims or package publication state.

## Self-Review

- changed files match the approved `CIL-004` smoke checker, tests, report, queue, docs index, and breadcrumb scope.
- `CIL-004` is completed.
- `CIL-003` remains deferred and was not implemented.
- no validation profile registry code changed.
- no command profile registry changed.
- no dynamic shell loading was added.
- no external config execution was added.
- no user-provided command text execution was added.
- no `shell=True` execution was added.
- no local-only ChatGPT context changed.
- no GitHub API mutation was added.
- no PR close, approval, merge, issue creation, project-board update, repository settings change, or collaborator change was added.
- no auto-repair, scheduler, daemon, background runner, GitHub Actions workflow, remote runner, provider-calling runner, H100 runner, self-merging agent, or actual multi-agent execution was added.
- no provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, production validation, output-quality proof, broader workload representativeness proof, production proof, or claim expansion was added.
- no release, tag, GitHub Release, PyPI publication, raw artifact upload, file move, rename, archive, or delete was performed.

## Next Recommendation

Recommended next action: review Group 114. After merge, consider `CIL-005 - Source-Install Readiness Check` only after explicit approval.

`CIL-003` remains deferred until Albert explicitly approves the medium-risk profile-registry checklist. Do not treat Group 114 as approval to implement `CIL-003`.

## Claim Boundary Reminder

Group 114 validates a local offline first-run smoke path only. It does not prove output quality, broader workload representativeness, production workload handling, production readiness, production validation, production cost reduction, H100/GPU/CPU superiority, customer savings, provider replacement, GPU-serving replacement, or published `getkora`.
