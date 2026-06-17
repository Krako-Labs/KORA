# Goal 083B getkora Distribution Strategy

## Motivation

Goal 083B defines the packaging strategy after discovering that plain `python3 -m pip install kora` installs an unrelated PyPI package. The goal is to keep the public brand KORA while avoiding the existing PyPI `kora` collision.

## Decision

- Public brand: KORA.
- GitHub repository: `Krako-Labs/KORA`.
- Future PyPI distribution package: `getkora`.
- CLI command: `kora`.
- Python import package: `kora`.

This goal did not publish anything.

## PyPI Checks

Command:

```bash
python3 -m pip index versions getkora
```

Result:

```text
ERROR: No matching distribution found for getkora
```

Interpretation: `getkora` appears available by package-index lookup, but this does not reserve the name or prove future publishability.

Command:

```bash
python3 -m pip index versions kora
```

Result: PyPI `kora` exists, with latest version `0.9.20`. Goal 083A isolated install validation found that package is an unrelated Colab utility package, not this `Krako-Labs/KORA` project.

## Packaging Audit

Current `pyproject.toml`:

- `[project].name` is `kora`.
- `[project].version` is `0.1.0a0`.
- Project URLs point to `https://github.com/Krako-Labs/KORA`.
- Console script is `kora = "kora.cli:main"`.
- Package discovery includes `kora*`.
- Runtime dependencies are `pydantic` and `jsonschema`.
- Optional dependency groups are `openai` and `dev`.

No root `setup.py`, `setup.cfg`, or `MANIFEST.in` file is present. Packaging metadata is centralized in `pyproject.toml`.

Current import and CLI layout:

- Import package: `kora`.
- Module entry point: `kora/__main__.py`.
- CLI implementation: `kora/cli.py`.
- Console command: `kora`.

## Proposed Future Metadata Change

For a future packaging goal, change:

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

The distribution name can be `getkora` while the import package and CLI remain `kora`.

## CLI Decision

Keep the CLI command as `kora`.

Reason: it matches the public brand and current docs. Changing it would create unnecessary user-facing churn.

## Import Package Decision

Keep the Python import package as `kora`.

Reason: the source layout, tests, module invocation path, and docs already use `kora`. Distribution package names and import package names do not need to match.

## Documentation Updates

Updated:

- `README.md`
- `docs/README.md`
- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- `examples/kora_doctor/README.md`
- `docs/packaging/getkora_distribution_strategy.md`

The docs now state:

- plain `python3 -m pip install kora` is not this project.
- current latest-feature path is source install from the repository.
- future PyPI distribution package is planned as `getkora`.
- `pip install getkora` must not be documented as working until a future publication validates it.

## Validation Results

```bash
python3 -m pip index versions getkora
```

Result: `ERROR: No matching distribution found for getkora`.

```bash
python3 -m pip index versions kora
```

Result: PyPI `kora` exists; latest reported version was `0.9.20`.

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
```

Result: passed; reported `6` total tasks, `4` deterministic candidates, `2` provider-needed candidates, and `0` provider calls.

```bash
python3 -m kora doctor --all examples/kora_doctor/
```

Result: passed; reported `4` workloads, `25` total tasks, `16` deterministic candidates, `9` provider-needed candidates, and `0` provider calls.

```bash
python3 -m kora examples list
```

Result: passed; listed `kora_doctor`.

```bash
python3 -m pytest tests/test_kora_doctor_cli.py tests/test_first_value_cli.py
```

Result: passed, `14 passed in 3.88s`.

```bash
python3 scripts/check_markdown_links_goal082b.py
git diff --check
```

Result: markdown link validation passed with `Goal 082B markdown links OK`; `git diff --check` passed.

## Release Boundary

This goal did not:

- publish to PyPI.
- reserve a PyPI package.
- create a release.
- create a tag.
- create a GitHub Release.
- claim `pip install getkora` works.
- claim PyPI contains the latest KORA features.

## Recommended Next Goal

Run a dedicated packaging implementation goal that changes `pyproject.toml` to `name = "getkora"`, builds wheel and source distributions, inspects package contents, and validates isolated wheel install without publishing.
