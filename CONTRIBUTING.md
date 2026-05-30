# Contributing to KORA

## Project status

Current published release: [`v0.2.0-alpha`](https://github.com/Krako-Labs/KORA/releases/tag/v0.2.0-alpha).

KORA remains alpha / prerelease software with a small terminal-first public surface. The current focus is keeping the CLI, examples, telemetry path, benchmark evidence, and release smoke checks reliable while the project matures.

KORA is not a production release yet. Contributions should be conservative, well-scoped, and easy to verify.

## Contributor path

Start here when orienting yourself:

- [README.md](README.md): project overview, current release status, quickstart, examples, and bounded benchmark evidence.
- [docs/README.md](docs/README.md): public docs navigation, current evidence path, artifact policy, and historical report labels.
- [experiments/README.md](experiments/README.md): deterministic-heavy benchmark workload and regeneration flow.
- [CHANGELOG.md](CHANGELOG.md): release history.
- [SECURITY.md](SECURITY.md): supported reporting path for security issues.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): community expectations.
- [GOVERNANCE.md](GOVERNANCE.md): project governance expectations.
- [docs/community/contact-and-discussion-routes.md](docs/community/contact-and-discussion-routes.md): current route guidance for questions, workload proposals, bugs, security issues, and PRs.
- [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/): issue templates.
- [.github/pull_request_template.md](.github/pull_request_template.md): pull request checklist.

## Who this project is for

KORA is for developers and researchers building AI systems that need stronger execution control.

Good contributors are interested in:

- deterministic-first execution
- explicit task graphs
- bounded model invocation
- schema validation
- telemetry and repeatable verification
- clear examples and documentation

## Local setup

### Prerequisites

KORA uses `pyproject.toml`-based Python packaging.

- Packaged support: Python 3.11 or newer, as declared in `pyproject.toml`.
- Observed local result: Python 3.9.6 has been confirmed to run the offline `direct_vs_kora` example in one user environment.
- Treat Python 3.9.6 as an observed troubleshooting datapoint, not as the advertised package support floor until clean Python 3.9 compatibility testing is completed.
- Check the active terminal interpreter with `python3 --version`.
- VS Code's selected interpreter may differ from terminal `python3`; use the intended `.venv` in both places when debugging.
- Upgrade `pip`, `setuptools`, and `wheel` before editable install.

Check your local tools before installing:

```bash
python3 --version
python3 -m pip --version
which python3
```

Start from a clean checkout of the repository.

```bash
python3 --version

rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e ".[dev]"
```

Run the first local examples:

```bash
python3 -m kora run hello_kora -- --offline
python3 -m kora run direct_vs_kora -- --offline
```

If editable install reports that `setup.py`, `setup.cfg`, or install metadata is missing, first verify that your checkout is current:

```bash
git remote -v
git fetch origin
git checkout main
git pull origin main
ls pyproject.toml
```

If `pyproject.toml` is still missing after pulling, re-clone from `https://github.com/Krako-Labs/KORA.git`.

The editable install should install KORA and its development dependencies into the virtual environment.

### Local setup troubleshooting

For first-run failures after a system restart, Python upgrade, VS Code interpreter change, or virtual environment change, capture the local environment first:

```bash
python3 --version
python3 -m pip --version
python3 -m pip show pydantic
which python3
```

If `python3 -m kora run direct_vs_kora -- --offline` fails with:

```text
TypeError: unsupported operand type(s) for |: 'ModelMetaclass' and 'ModelMetaclass'
```

that usually indicates a local Python, virtual environment, `pip`, `setuptools`, or dependency compatibility problem. Python 3.9.6 has been observed to work with the offline `direct_vs_kora` example in one user environment, but packaged support is currently Python 3.11 or newer. Rebuild the virtual environment using the clean setup block above before drawing a Python-version conclusion.

If editable install says `setup.py` or `setup.cfg` is missing even though `pyproject.toml` exists, upgrade local build tooling inside the activated virtual environment:

```bash
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e ".[dev]"
```

If VS Code fails while Terminal works, select the repository `.venv` interpreter in VS Code and confirm the VS Code terminal reports the same `which python3` and `python3 --version` values as your working shell.

## First verification commands

Before making changes, run the release smoke check:

```bash
./scripts/release_smoke.sh
```

Then run the test suite:

```bash
python3 -m pytest -q
```

Both commands should pass before you open a pull request.

## How to choose a first issue

For a first contribution, choose a task that is small and easy to review.

Good first issues usually:

- touch one or two files
- improve clarity without changing behavior
- add or tighten a narrow test
- explain an existing example or telemetry artifact
- preserve the current public CLI surface

Avoid starting with large runtime changes, new public commands, broad refactors, or changes that alter model-routing semantics.

## Claiming good first issues

Before starting work on a good first issue, leave a short comment on the issue so others know you are working on it.

When preparing a contribution:

- Keep the pull request focused on the issue being addressed.
- Avoid combining unrelated changes into the same PR.
- If the scope or requirements are unclear, ask for clarification before implementing a solution.

This helps reduce duplicate work and makes reviews easier for maintainers.

## Finding a first contribution

Use the [contributor pathway](docs/community/contributor-pathway.md) to choose the right route for questions, bugs, PRs, and workload proposals.

For current route guidance, see [contact and discussion routes](docs/community/contact-and-discussion-routes.md).

For candidate tasks that maintainers may later convert into GitHub issues, see [good first issue candidates](docs/community/good-first-issue-candidates.md).

For validation workload ideas, use the [workload proposal template](docs/community/workload-proposal-template.md). Keep proposals synthetic or sanitized and do not include secrets, private data, proprietary datasets, or raw provider responses.

## Good first contribution types

Good first contribution types include:

- docs improvements
- example explanations
- small tests
- telemetry docs
- benchmark docs
- CLI help wording

If you are unsure whether a change expands the public surface, open an issue or discussion before implementing it.

## Branch and PR workflow

Do not push directly to `main`. Start each change from the latest `main`, create a topic branch, push that branch, and open a pull request into `main`.

Most external contributors will not have write access to `Krako-Labs/KORA`. That is expected. Direct write access is not required to contribute: fork the repository, push your branch to your fork, and open a pull request into `Krako-Labs/KORA:main`.

Start from latest `main`:

```bash
git checkout main
git pull origin main
```

Create your branch:

```bash
git checkout -b <type>/<short-description>
```

Recommended branch name prefixes:

- `feature/` for a new capability or example
- `fix/` for a bug fix
- `docs/` for documentation-only changes
- `test/` for tests or test fixtures
- `chore/` for maintenance that does not change behavior

Good branch names:

- `fix/login-screen-freeze`
- `docs/python-setup-guide`
- `test/offline-runner-smoke`
- `feature/dev-error-reporting`

### Fork workflow for external contributors

Use this workflow if you do not have write access to `Krako-Labs/KORA`.

1. Fork `https://github.com/Krako-Labs/KORA` on GitHub.
2. Clone your fork:

   ```bash
   git clone https://github.com/<your-github-username>/KORA.git
   cd KORA
   ```

3. Add the upstream repository:

   ```bash
   git remote add upstream https://github.com/Krako-Labs/KORA.git
   git fetch upstream
   ```

4. Create a branch from the latest upstream `main`:

   ```bash
   git checkout -b <type>/<short-description> upstream/main
   ```

5. Make your changes, then check the diff:

   ```bash
   git status
   git diff
   ```

6. Commit with a short imperative summary:

   ```bash
   git add .
   git commit -m "Short imperative summary"
   ```

7. Push to your fork:

   ```bash
   git push -u origin <branch-name>
   ```

8. Open a pull request on GitHub from `<your-github-username>:<branch-name>` into `Krako-Labs/KORA:main`.

### Direct branch workflow for contributors with write access

Check your changes before committing:

```bash
git status
git diff
```

Commit with a short imperative summary:

```bash
git add .
git commit -m "Short imperative summary"
```

Push your branch:

```bash
git push -u origin <branch-name>
```

Then open a pull request on GitHub from your branch into `main`.

### If `git push` returns 403

If this push:

```bash
git push -u origin <branch-name>
```

fails with:

```text
remote: Permission to Krako-Labs/KORA.git denied to <username>.
fatal: unable to access 'https://github.com/Krako-Labs/KORA.git/': The requested URL returned error: 403
```

you are probably trying to push directly to the upstream `Krako-Labs/KORA` repository without write access. Use the fork workflow above instead. In that workflow, `origin` should point to your fork and `upstream` should point to `https://github.com/Krako-Labs/KORA.git`.

Check your remotes:

```bash
git remote -v
```

For an external contributor, a typical setup looks like:

```text
origin   https://github.com/<your-github-username>/KORA.git (fetch)
origin   https://github.com/<your-github-username>/KORA.git (push)
upstream https://github.com/Krako-Labs/KORA.git (fetch)
upstream https://github.com/Krako-Labs/KORA.git (push)
```

After fixing the remotes, push your branch to your fork:

```bash
git push -u origin <branch-name>
```

Then open a pull request on GitHub into `Krako-Labs/KORA:main`.

Keep pull requests focused. A good PR should explain:

- what problem it solves
- what files changed
- how behavior is affected, if at all
- what verification commands were run

Prefer one logical change per PR. Do not bundle documentation cleanup, runtime edits, and unrelated formatting in the same pull request.

## Reproducible bug reports

Before attempting a code fix for a support-channel report, capture enough detail for another contributor to reproduce the problem. For example, a report like "login screen appears but code is not accepted" should become a concrete bug report before implementation starts.

Include:

- exact command or screen flow
- operating system and version
- Python version, if Python is involved
- browser or runtime, if a browser or local UI is involved
- screenshot or screen recording, if useful and safe to share
- terminal logs or traceback excerpts
- steps to reproduce
- expected result
- actual result

Do not include secrets, tokens, private data, private paths, or sensitive security details in public issues. Use [SECURITY.md](SECURITY.md) for sensitive security reports.

## Verification expectations

Use verification that matches the change type. Include the commands and results in your PR description.

For documentation-only changes, check that public docs use relative repo paths and do not add unsupported claims. When relevant, scan changed docs for machine-local paths:

```bash
rg -n "/Users/|/home/" <changed-docs>
```

For CLI or example changes, run the CLI smoke checks and the relevant example:

```bash
python3 -m kora --help
python3 -m kora examples list
python3 -m kora run <example_name>
```

For benchmark or evidence changes, run tests and follow the regeneration flow in [experiments/README.md](experiments/README.md). Keep raw benchmark JSON artifacts governed by [docs/reports/benchmark_artifact_policy.md](docs/reports/benchmark_artifact_policy.md).

```bash
python3 -m pytest
```

For general code changes, run the full test suite and at least one relevant CLI smoke test:

```bash
python3 -m pytest
python3 -m kora --help
python3 -m kora run direct_vs_kora -- --offline
```

If your change touches a specific module, also run the relevant focused test file when possible:


```bash
python3 -m pytest tests/test_executor.py -q
python3 -m pytest tests/test_task_ir.py -q
```

## Claim hygiene

Do not claim:

- production cost reduction proof
- real API-cost reduction proof
- production benchmark proof
- full runtime-integrated benchmark evidence
- broad workload superiority proof
- energy reduction evidence

If you reference current benchmark evidence, use only this bounded claim:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

## Local-path hygiene

Public docs should use relative repo paths. Do not include machine-local absolute paths, private notes, or machine-specific setup details.

## Python requirement changes

Python compatibility changes must follow `pyproject.toml` and the public setup docs. KORA's packaged support is Python 3.11 or newer unless `pyproject.toml` is changed through a reviewed compatibility task.

Do not add macOS-specific checks that require Python 3.9.6. Python 3.9.6 is only an observed troubleshooting datapoint from one environment, not the required macOS version and not the advertised package support floor.

## Contribution rules

- Keep PRs small.
- Do not include unrelated refactors.
- Run tests before opening a PR.
- Do not expand the public CLI or public task surface without prior discussion.
- Keep KORA deterministic-first: deterministic work should run before model inference when possible.
- Do not introduce hidden model calls.
- Keep retries, budgets, and validation explicit.
- Preserve schema validation around model outputs.
- Avoid broad claims in docs unless they are backed by committed verification artifacts.

## Community expectations

Be direct, practical, and respectful.

Good project communication is specific:

- describe the concrete issue
- explain the tradeoff
- show the verification result
- ask for review when scope is uncertain

KORA values careful, measurable changes over large speculative additions.
