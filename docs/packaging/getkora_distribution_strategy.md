# getkora Distribution Strategy

## Decision

- Public brand: KORA.
- GitHub repository: `Krako-Labs/KORA`.
- Future PyPI distribution package: `getkora`.
- CLI command: `kora`.
- Python import package: `kora`.

This document is a packaging strategy, not a release announcement. It does not publish a package, create a release, create a tag, or claim that `getkora` is available for installation today.

## Current PyPI Collision

Plain `python3 -m pip install kora` must not be used for this project.

Observed package-index state on June 18, 2026:

- `python3 -m pip index versions kora` reported `kora (0.9.20)` with many existing versions.
- Goal 083A isolated install validation found that PyPI `kora 0.9.20` is an unrelated Colab utility package, not `Krako-Labs/KORA`.
- `python3 -m pip index versions getkora` reported `ERROR: No matching distribution found for getkora`.

Interpretation: `getkora` appears available by package-index lookup, but availability is not ownership. A future release still needs normal PyPI account, project creation, token, Trusted Publisher, and publication checks.

## Current Safe Install Path

Current latest-feature path:

```bash
git clone https://github.com/Krako-Labs/KORA.git
cd KORA

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e .

python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
```

Development/test path:

```bash
python3 -m pip install -e ".[dev]"
```

Do not document `python3 -m pip install getkora` as working until a future packaging goal actually publishes it and validates installation from PyPI.

## Packaging Audit

Current `pyproject.toml` state:

```toml
[project]
name = "kora"
version = "0.1.0a0"
description = "Open-source execution control for AI systems"
requires-python = ">=3.11"

[project.urls]
Homepage = "https://github.com/Krako-Labs/KORA"
Repository = "https://github.com/Krako-Labs/KORA"
Issues = "https://github.com/Krako-Labs/KORA/issues"

[project.scripts]
kora = "kora.cli:main"

[tool.setuptools.packages.find]
include = ["kora*"]
```

No `setup.py`, `setup.cfg`, or `MANIFEST.in` file is present in the repository root. Packaging metadata is centralized in `pyproject.toml`.

Package layout:

- Import package: `kora/`.
- Module entry point: `kora/__main__.py`.
- CLI implementation: `kora/cli.py`.
- Console script: `kora = "kora.cli:main"`.

## Future Metadata Changes

For a future PyPI distribution under `getkora`, update package metadata in `pyproject.toml`:

```toml
[project]
name = "getkora"
```

Keep:

```toml
[project.scripts]
kora = "kora.cli:main"

[tool.setuptools.packages.find]
include = ["kora*"]
```

Recommended additional metadata before publication:

- Set an explicit maintainer email or project contact route.
- Add a `CHANGELOG` or release notes link if publishing public versions.
- Confirm README install examples refer to `getkora` only after publication.
- Verify source distribution and wheel contents include required runtime package data.
- Run isolated `pip install getkora` validation after publication.

## CLI Decision

Keep the CLI command as `kora`.

Reasoning:

- The public brand is KORA.
- Existing documentation and examples use `python3 -m kora` and `kora`.
- The console script is user-facing and should match the brand.
- Changing the CLI command would add unnecessary user-facing churn.

Risk:

- If another installed package provides a `kora` console script, user environments could have command conflicts. Current validation should prefer virtual environments and `python3 -m kora` examples.

## Python Import Decision

Keep the Python import package as `kora`.

Reasoning:

- The repository source layout is already `kora/`.
- The module invocation path `python3 -m kora` depends on that package.
- Distribution package names and import package names do not need to match.
- Renaming the import package would require broad code, test, documentation, and user-facing migration work without clear benefit at this stage.

Risk:

- A user who installs the unrelated PyPI `kora` package will get a different import package. This is addressed by not documenting plain `pip install kora` and by using source install until `getkora` is published.

## Release Boundary

This strategy does not:

- publish `getkora`.
- reserve a PyPI project name.
- create a release.
- create a tag.
- create a GitHub Release.
- claim `pip install getkora` works.
- claim PyPI has latest KORA features.

## Future Release Gate

Before publishing, run a dedicated packaging goal that:

- updates `pyproject.toml` distribution name to `getkora`.
- builds source distribution and wheel.
- inspects wheel and sdist contents.
- installs the wheel into an isolated environment.
- verifies `python3 -m kora --help`.
- verifies `python3 -m kora doctor examples/kora_doctor/customer_support_workload.json` from an installed checkout or packaged sample strategy.
- confirms the CLI command `kora` is installed.
- only then publishes to PyPI, if explicitly approved.
