# Goal 109 Bounded Local Validation Runner

Status: implemented with local validation passing and PR open.

## Objective

Goal 109 adds a small public-safe bounded local validation runner for the practical development loop. The runner executes only a hardcoded local validation profile and records deterministic step-level results.

This is a local-only bounded validation runner. It is not production validation, output-quality proof, broader workload representativeness proof, provider replacement proof, or GPU/H100 superiority evidence.

## CLI Usage

Run the supported local profile:

```bash
python3 scripts/run_bounded_local_validation.py --profile kora-local-core
```

Optionally write structured reports:

```bash
python3 scripts/run_bounded_local_validation.py \
  --profile kora-local-core \
  --json-out /tmp/kora-goal109-bounded-local-validation.json \
  --md-out /tmp/kora-goal109-bounded-local-validation.md
```

Preview planned steps without execution:

```bash
python3 scripts/run_bounded_local_validation.py --profile kora-local-core --dry-run
```

## Supported Profile

The only supported profile is `kora-local-core`.

Unknown profiles are rejected with a nonzero exit code and a clear error message. The runner does not accept arbitrary user-provided commands or command arguments.

## Approved Command List

The `kora-local-core` profile runs exactly these commands, in this order:

```bash
python3 scripts/evaluate_fixture_quality_checks.py
python3 -m pytest tests/test_fixture_quality_checks.py
python3 -m pytest tests/test_representativeness_seed.py tests/test_representativeness_route_only_evaluator.py
python3 scripts/check_markdown_links_goal082b.py
git diff --check
python3 -m pytest
```

Commands are stored as structured argv lists and executed with `subprocess.run(..., shell=False)` from the repository root. The runner stops on the first failing command and returns a nonzero exit code for any failed command.

## Dry-Run Behavior

`--dry-run` reports the planned profile steps without executing subprocess commands. Each step is marked `skipped/dry-run` with no return code.

## JSON And Markdown Output

`--json-out` writes a structured JSON report containing the profile, final status, repository root, and step records.

`--md-out` writes a simple Markdown report containing the profile, final status, and a table of step names, statuses, return codes, and commands.

If no output paths are supplied, the runner prints a concise text summary to stdout.

## Safety Boundaries

Goal 109 keeps the runner within these boundaries:

- no arbitrary shell command execution.
- no auto-repair.
- no scheduler, daemon, or background runner.
- no GitHub Actions workflow.
- no remote runner.
- no provider-calling runner.
- no H100, GPU, CUDA, server, or remote execution.
- no model inference.
- no semantic judging.
- no human grading.
- no file movement.
- no local-only ChatGPT context changes.
- no releases, tags, release assets, GitHub issues, project boards, repository settings, or collaborator changes.

## Claim Boundaries

Goal 109 does not claim:

- output-quality proof.
- broader workload representativeness proof.
- production proof.
- production cost reduction.
- customer savings.
- H100/GPU/CPU superiority.
- provider replacement or GPU-serving replacement.
- that `getkora` is published.

## Validation Commands For This PR

Final validation required before PR:

```bash
python3 -m pytest tests/test_bounded_local_validation_runner.py
python3 scripts/run_bounded_local_validation.py --profile kora-local-core --dry-run
python3 scripts/run_bounded_local_validation.py --profile kora-local-core
python3 scripts/run_bounded_local_validation.py --profile kora-local-core --json-out /tmp/kora-goal109-bounded-local-validation.json --md-out /tmp/kora-goal109-bounded-local-validation.md
python3 scripts/check_markdown_links_goal082b.py
git diff --check
python3 -m pytest
```

Observed validation before PR open:

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_bounded_local_validation_runner.py` | passed, `8 passed` |
| `python3 scripts/run_bounded_local_validation.py --profile kora-local-core --dry-run` | passed; reported six `skipped/dry-run` steps |
| `python3 scripts/run_bounded_local_validation.py --profile kora-local-core` | passed; all six bounded profile steps passed; final full suite reported `418 passed` |
| `python3 scripts/run_bounded_local_validation.py --profile kora-local-core --json-out /tmp/kora-goal109-bounded-local-validation.json --md-out /tmp/kora-goal109-bounded-local-validation.md` | passed; JSON and Markdown reports written; final full suite reported `418 passed` |
| `python3 scripts/check_markdown_links_goal082b.py` | passed |
| `git diff --check` | passed |
| `python3 -m pytest` | passed, `418 passed` |

The expected full-suite baseline from Goal 108 was `410 passed`; this branch observes `418 passed` after adding the Goal 109 runner tests.

## Final PR Status

- PR: `https://github.com/Krako-Labs/KORA/pull/259`
- branch: `codex/goal109-bounded-local-validation-runner`
- state: open for review
- merge status: not merged by this task

This report does not merge the PR.

## R1 Hidden/Control Unicode Normalization

R1 inspected the three Goal 109 files for hidden, bidirectional, control, and non-ASCII Unicode characters:

- `scripts/run_bounded_local_validation.py`
- `tests/test_bounded_local_validation_runner.py`
- `docs/reports/goal109_bounded_local_validation_runner.md`

The scan found no hidden, bidirectional, control, or non-ASCII Unicode code points in the three files. No functionality, command list, safety boundary, or claim boundary changes were made.
