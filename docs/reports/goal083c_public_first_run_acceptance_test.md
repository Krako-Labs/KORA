# Goal 083C Public First-Run Acceptance Test

## Summary

Goal 083C tested whether a new external reviewer can start from public repository documentation, install the current source version safely, run KORA Doctor, run deterministic classification, and understand the PyPI package-name boundary.

Result: pass with one small documentation fix.

The tested source included pending local Goal 083B material at commit `f768a353fa02feb0dcf1f02055ae4c029117ad37`.

## Environment

Acceptance test environment:

- Date: June 18, 2026.
- OS context: local macOS shell.
- Fresh install directory: `/tmp/kora083c_fresh.O9XvF6`.
- Fresh source checkout HEAD: `f768a353fa02feb0dcf1f02055ae4c029117ad37`.
- Python: `Python 3.13.5`.
- pip: `pip 26.1.2`.
- Install mode: editable source install with `python3 -m pip install -e .`.

Repository validation environment:

- Worktree: `goal083c_public_first_run_acceptance`.
- Base material: pending Goal 083B distribution strategy.

## Scenario A - README-Only Reviewer

Procedure:

1. Started from `README.md` only.
2. Read the project intro, current availability section, install block, examples section, and evidence limits.
3. Followed the documented current install path in a fresh source checkout.
4. Ran the first KORA Doctor command documented in the current availability and examples sections.

Result: pass.

Findings:

- A new user can understand within 30 seconds that KORA is an AI Workload Control Layer for deciding what should reach a model, what can be deterministic, and how work moves through an AI system.
- The README warns that plain `python3 -m pip install kora` is not this project.
- The README says `getkora` is the planned future distribution name and does not claim it is published.
- The README gives source install commands before the latest example commands.

Ambiguities or failures:

- The deterministic classification README had runnable commands but did not repeat the source-install/PyPI collision note. This was fixed.

## Scenario B - Fresh Source Install

Commands:

```bash
git clone --no-local <goal083c-source-worktree> /tmp/kora083c_fresh.O9XvF6/KORA
cd /tmp/kora083c_fresh.O9XvF6/KORA
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e .
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora doctor --all examples/kora_doctor/
python3 examples/deterministic_classification/run.py
```

Result: pass.

Observed:

- `python3 -m kora doctor examples/kora_doctor/customer_support_workload.json` exited `0`.
- The single Doctor report showed `6` total tasks, `4` deterministic candidates, `2` provider-needed candidates, and `0` provider calls actually made.
- `python3 -m kora doctor --all examples/kora_doctor/` exited `0`.
- The aggregate Doctor report showed `4` workloads, `25` total tasks, `16` deterministic candidates, `9` provider-needed candidates, and `0` provider calls actually made.
- `python3 examples/deterministic_classification/run.py` exited `0`.
- The deterministic classification output showed `32` total tasks and `0` provider calls actually made.

## Scenario C - PyPI Collision Awareness

Procedure:

Scanned public docs for:

- `pip install kora`.
- `python3 -m pip install kora`.
- `getkora`.
- `pip install getkora`.
- claims that `getkora` is published.

Result: pass.

Findings:

- `README.md`, `docs/README.md`, `examples/kora_doctor/README.md`, and `examples/deterministic_classification/README.md` now warn that plain `python3 -m pip install kora` is not this project.
- `README.md` and `docs/README.md` identify `getkora` as a planned future distribution name.
- No public doc claims that `python3 -m pip install getkora` works today.
- The docs say source install from the current repository is the latest-feature path.

## Scenario D - 5-Minute Reviewer Path

Procedure:

1. Read the README intro and current availability section.
2. Installed from source in a fresh virtual environment.
3. Ran KORA Doctor single workload.
4. Ran KORA Doctor aggregate report.
5. Ran deterministic classification.
6. Read safe claim boundaries.

Result: pass.

Findings:

- The flow is feasible within a five-minute reviewer path after dependencies are available.
- The first useful output is a concise KORA Doctor report.
- The deterministic classification example is runnable from the README path.
- Evidence limits are visible before the installation section and again near the example/report docs.

## Documentation Fixes Applied

Applied one direct fix:

- Added a current-availability note to `examples/deterministic_classification/README.md` stating that the example should be run from a current `Krako-Labs/KORA` source checkout, that plain `python3 -m pip install kora` installs a different PyPI project, and that `getkora` is planned but not documented as published.

Updated continuation surfaces:

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- `docs/README.md`

## Validation Commands

Fresh source install:

```bash
git clone --no-local <goal083c-source-worktree> /tmp/kora083c_fresh.O9XvF6/KORA
cd /tmp/kora083c_fresh.O9XvF6/KORA
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e .
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora doctor --all examples/kora_doctor/
python3 examples/deterministic_classification/run.py
```

Repository validation:

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora doctor --all examples/kora_doctor/
python3 examples/deterministic_classification/run.py
python3 -m kora examples list
python3 -m pytest tests/test_kora_doctor_cli.py tests/test_first_value_cli.py tests/test_deterministic_classification_expansion_pack.py
python3 scripts/check_markdown_links_goal082b.py
git diff --check
```

Results:

- `python3 -m pytest tests/test_kora_doctor_cli.py tests/test_first_value_cli.py tests/test_deterministic_classification_expansion_pack.py` passed with `26 passed in 5.54s`.
- `python3 scripts/check_markdown_links_goal082b.py` passed with `Goal 082B markdown links OK`.
- `git diff --check` passed.

## Blockers

No acceptance blockers remain.

## Remaining Limitations

- Latest-feature installation remains source-based until a future packaging goal publishes a distribution.
- `getkora` is only a planned future PyPI distribution name; it is not documented as published.
- The examples are offline and synthetic.
- The deterministic classification output is verbose JSON; it is useful as evidence but not as polished as the Doctor report.

## Recommendation

Proceed to Goal 084.

Reason: first-run source installation, KORA Doctor, deterministic classification, package-collision warnings, `getkora` caveats, and evidence limits are clear enough for the next public reviewer walkthrough and example catalog refresh.
