# Group 115 Source-Install Readiness Check

Status: implemented with local validation complete; PR open.

## Objective

Group 115 implements `CIL-005 - Source-Install Readiness Check`.

This group adds a bounded, public-safe source-install readiness checker that creates an isolated temporary virtual environment, installs the current local source tree, and verifies core import and CLI availability after install. It is source-install readiness only. It does not implement `CIL-003`, change validation profile registries, change command profile registries, publish packages, call providers, run H100/server work, or expand claims.

## Approval Packet

Decision needed: review and decide whether to merge Group 115 source-install readiness checking.

Risk level: medium

Final status classification: `needs-cto-review`

Changed files: source-install readiness checker, focused tests, Group 115 report, inner-loop queue update, next-goal queue update, docs index, and narrow breadcrumbs.

Validation summary: focused readiness tests, real local source-install readiness run, markdown links, whitespace diff check, and full pytest passed.

Repair attempts: 0.

Failures encountered: none.

Self-review summary: scope is source-install readiness checking, tests, report, and breadcrumbs; `CIL-005` is completed, `CIL-003` remains deferred, and no validation or command profile registry implementation was added.

Claim-boundary audit: this checks local source installation only. It does not check PyPI installation, publish a package, claim `getkora` is published, claim install-from-PyPI support, prove production readiness, prove output quality, prove broader workload representativeness, prove production workload handling, prove production validation, prove production cost reduction, claim customer savings, claim H100/GPU/CPU superiority, claim provider replacement, or claim GPU-serving replacement.

Forbidden-action audit: no `CIL-003` implementation, validation profile registry change, command profile registry change, PyPI command, release/tag/GitHub Release/package upload step, package publication, version change, provider call, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, GitHub Actions workflow, scheduler, daemon, background runner, GitHub API mutation, PR approval, PR merge, PR close, issue creation, project-board update, repository settings change, collaborator change, file movement, file rename, file archive, file deletion, or local-only ChatGPT context change was added.

Uncertainty notes: this group touches source-install and CLI availability confidence, so it is classified as medium risk and `needs-cto-review` even though the checker is local-only and deterministic after dependency installation succeeds.

Codex recommendation: CTO Review.

Albert action options: Merge / Request R1 / Stop / CTO Review.

## Base And Branch

- public truth: `origin/main`
- base public HEAD: `a3c9db3f54e17e3d0e292bae4ffce56d8c9262bf`
- branch: `codex/group115-source-install-readiness`
- worktree: `/Users/albertkim/02_PROJECTS/05_KORA_Project/worktrees/group115_source_install_readiness`
- PR: pending until PR open

## Subtasks

- 115-1 Source-install readiness checker: added `scripts/check_source_install_readiness.py`.
- 115-2 Editable install / import / CLI availability checks: checker installs the local repo with `python -m pip install -e <repo>`, then checks `import kora`, `python -m kora --help`, `kora --help`, and `kora examples list`.
- 115-3 No PyPI / no package publication boundary check: script and report explicitly state local source-install only and no PyPI/publication/getkora/install-from-PyPI claim.
- 115-4 Focused tests: added deterministic unit tests with mocked subprocess execution.
- 115-5 Real local source-install readiness run: ran the checker once from the clean Group 115 worktree; result passed.
- 115-6 Report / breadcrumbs / queue update: added this report and updated breadcrumbs, docs index, inner-loop queue, and next-goal queue.
- 115-7 Validation / PR open: validation completed locally; PR opened after commit and push.

## Checker Behavior

The checker creates a temporary environment outside the repository using `python -m venv`, installs the current local source tree, runs readiness checks, prints a concise text summary, exits nonzero on failure, and cleans up the temporary environment by default.

Debug option:

- `--keep-temp` preserves the temporary environment for local debugging.

Install modes:

- default: `editable`, using `python -m pip install -e <repo>`.
- optional: `source`, using `python -m pip install <repo>`.

The checker uses structured subprocess argument lists with `shell=False`.

## Real Source-Install Readiness Run

Command:

```bash
python3 scripts/check_source_install_readiness.py
```

Observed result:

- install mode: `editable`
- final status: `passed`
- checks run: `6`
- passed checks: `6`
- failed checks: `0`
- import check result: `passed`
- `python -m kora` availability check result: `passed`
- `kora` CLI availability check result: `passed`
- no-provider command smoke result: `passed`
- command smoke: `kora examples list`
- temporary environment cleanup: default cleanup path used; no debug environment preserved.

The real run installed KORA from the local Group 115 worktree path. It did not install KORA from PyPI and did not publish any package.

## Files Added

- `scripts/check_source_install_readiness.py`
- `tests/test_source_install_readiness.py`
- `docs/reports/group115_source_install_readiness_check.md`

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
| `python3 -m pytest tests/test_source_install_readiness.py` | passed, `8 passed` |
| `python3 scripts/check_source_install_readiness.py` | passed; editable install; `6 passed / 0 failed / 6 total` |
| `python3 scripts/check_markdown_links_goal082b.py` | passed |
| `git diff --check` | passed |
| `python3 -m pytest` | passed, `495 passed` |

## Loop Count And Repairs

- loop count: 1
- repair attempts: 0
- max loop count: 5
- max repair attempts per failing subtask: 2

## Risk And Final Classification

- risk level: medium
- final status classification: `needs-cto-review`

Rationale: this group is bounded local tooling plus tests and docs, but it touches source-install and CLI availability confidence. It does not change public package publication state or claim PyPI availability.

## Self-Review

- changed files match the approved `CIL-005` checker, tests, report, queue, docs index, and breadcrumb scope.
- `CIL-005` is completed.
- `CIL-003` remains deferred and was not implemented.
- no validation profile registry changed.
- no command profile registry changed.
- no PyPI command was added.
- no release, tag, GitHub Release, release asset, or package upload step was added.
- no package version was changed.
- no provider calls were added or executed.
- no H100/GPU/CUDA/server/remote execution was added or executed.
- no model inference, semantic judging, or human grading was added.
- no local-only ChatGPT context changed.
- no repository settings, collaborator, issue, project-board, PR approval, PR merge, or PR close mutation was performed.
- no file was moved, renamed, archived, or deleted.

## Next Recommendation

Recommended next action: review Group 115.

`CIL-003` remains deferred until Albert explicitly approves the medium-risk profile-registry checklist. Do not treat Group 115 as approval to implement `CIL-003`.

## Non-Claims And Boundaries

Group 115 checks local source installation only. It does not check PyPI installation. It does not publish a package. It does not claim `getkora` is published. It does not claim install-from-PyPI support. It does not prove output quality, broader workload representativeness, production workload handling, production readiness, production validation, production cost reduction, H100/GPU/CPU superiority, customer savings, provider replacement, or GPU-serving replacement.
