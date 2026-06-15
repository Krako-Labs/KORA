# KRK Goal 070C First-Value Install Packaging v0

Status: public-safe technical report.

## Motivation

Goal 070B added the official first-value CLI surface:

- `kora inspect`
- `kora compare`
- `kora run`
- `kora report`

Goal 070C validates that a fresh macOS/Linux-style user can install the package locally and run that first-value path through the packaged console script.

## Install Workflow

Supported first-value install path:

```bash
git clone https://github.com/Krako-Labs/KORA.git
cd KORA
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e .
```

First-value CLI path:

```bash
kora inspect
kora compare
kora run
kora report \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

## Packaging And Entrypoint Status

KORA uses `pyproject.toml` packaging. The public console script is registered as:

```toml
[project.scripts]
kora = "kora.cli:main"
```

The module entrypoint remains available through:

```bash
python3 -m kora --help
```

Goal 070C adds a test that verifies the package metadata continues to register the `kora` console script.

## Fresh-User Validation Result

Validation ran in a temporary clean virtual environment outside the repository:

- editable install command completed.
- installed `kora --help` completed.
- installed `kora inspect` completed.
- installed `kora compare` completed.
- installed `kora run` completed.
- installed `kora report` generated JSON and Markdown outputs.

Result: `FIRST_VALUE_EDITABLE_INSTALL_VALIDATED`.

## Onboarding Metrics

- install commands count: `6`
- first-value commands count: `4`
- total commands count: `10`
- required user decisions: `0`
- provider credentials required: `no`
- GPU required: `no`
- network required after install: `no`
- generated output files: `2`
- estimated time to first value: `5` minutes
- discovered failure points: none in the validated path

## First-Value Output Summary

The installed CLI path runs over committed public fixtures and reports:

- fixture items: `18`
- dry-run execution success rate: `1.0000`
- unsafe misroute rate: `0.0000`
- acceptable output rate: `1.0000`
- exact output matches: `17`
- structured-equivalent output matches: `1`
- degraded outputs: `0`
- failed outputs: `0`

These are fixture-derived first-value metrics. They are not production measurements.

## Supported Platform Target

Goal 070C validates macOS/Linux-style shell usage with Python 3.11-or-newer package support as declared in `pyproject.toml`.

Deferred platform support:

- native Windows
- WSL-specific validation
- published package installation

## Limitations

- The validation uses editable install, not a published package.
- Dependency installation may require network access when dependencies are not already cached.
- The first-value path uses public fixtures and dry-run evaluators.
- The path is intended for first understanding of KORA behavior, not production qualification.

## Claim Boundary

Allowed claim:

- KORA has a validated local editable-install first-value CLI path for macOS/Linux-style environments.

Not claimed:

- production proof
- production readiness
- production cost reduction
- customer savings
- energy reduction
- broad workload superiority
- real API/GPU cost reduction
- provider superiority
- H100 superiority
- adoption

## Next Packaging Steps

Recommended next steps:

- add release-candidate package smoke checks in CI.
- validate source distribution and wheel builds.
- document published-package installation after a release is explicitly approved.
- improve command output formatting for scanability.
- add user-provided workload selection while keeping the current public-safe fixture path intact.
