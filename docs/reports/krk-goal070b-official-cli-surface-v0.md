# KRK Goal 070B Official CLI Surface v0

Status: public-safe CLI surface implemented.

Final classification: `FIVE_MINUTE_FIRST_VALUE_PATH_MEASURED`

## Motivation

Goal 070A proved that KORA can offer a public-safe first-value workflow through a compatibility script. Goal 070B moves that experience into the official package CLI so a new OSS user can run:

```bash
kora inspect
kora compare
kora run
kora report
```

The purpose is usability and onboarding, not stronger benchmark evidence.

## CLI Design

The repository already exposes the package entrypoint:

```toml
[project.scripts]
kora = "kora.cli:main"
```

Goal 070B extends `kora.cli` using the existing `argparse` style. The existing example runner remains compatible:

```bash
kora run direct_vs_kora -- --offline
```

When no example is supplied, `kora run` now executes the public-safe first-value fixture path.

## Command Semantics

| Command | Purpose | Output options | Provider/GPU required |
| --- | --- | --- | --- |
| `kora inspect` | Print execution paths, workload profiles, and first-value environment requirements. | `--json-out` | no |
| `kora compare` | Compare direct model-candidate behavior with KRK-routed public fixture behavior. | `--json-out` | no |
| `kora run` | Run the public-safe fixture dry-run path when no example is provided. | `--json-out` | no |
| `kora report` | Generate the full first-value JSON and Markdown report. | `--json-out`, `--md-out` | no |

The commands reuse the Goal 070A implementation in `kora/five_minute_first_value.py`, which itself reuses:

- `kora.runtime_route_evaluator.evaluate_runtime_routes`
- `kora.output_fidelity.evaluate_output_fidelity`

## User Workflow

Fresh-clone local workflow:

```bash
python3 -m kora inspect
python3 -m kora compare
python3 -m kora run
python3 -m kora report \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

Installed console-script workflow:

```bash
kora inspect
kora compare
kora run
kora report \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

Compatibility workflow:

```bash
python3 scripts/kora_five_minute_demo.py \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

## Packaging and Entrypoint Notes

- Package entrypoint remains `kora = "kora.cli:main"`.
- No new packaging backend or dependency was added.
- The official commands work through both `python3 -m kora ...` and an installed `kora` console script.
- The compatibility script remains available and delegates to the same first-value module.

## Test Coverage

Goal 070B adds `tests/test_first_value_cli.py`, covering:

- top-level CLI help lists `inspect`, `compare`, `run`, and `report`.
- each command's `--help` succeeds.
- `kora inspect --json-out ...` succeeds without provider credentials or GPU.
- `kora compare --json-out ...` reports `11 / 18` local-or-guardrail routing opportunities.
- `kora run --json-out ...` executes the public fixture dry-run path.
- `kora run hello_kora -- --offline` remains compatible with the example runner.
- `kora report --json-out ... --md-out ...` generates JSON and Markdown.
- `scripts/kora_five_minute_demo.py` remains compatible.

## First-Value Impact

| Metric | Value |
| --- | ---: |
| Official commands added | 4 |
| Fixture items | 18 |
| Dry-run execution success rate | 1.0000 |
| Unsafe misroute rate | 0.0000 |
| Output exact match count | 17 |
| Output structured equivalent count | 1 |
| Output degraded count | 0 |
| Output failed count | 0 |
| Acceptable output rate | 1.0000 |
| Provider credentials required | false |
| GPU required | false |
| Network required | false |

Generated evidence:

- [Generated Goal 070B official CLI surface JSON summary](../evidence/generated/krk-goal070b-official-cli-surface-summary-v0.json)
- [Generated Goal 070B official CLI surface Markdown summary](../evidence/generated/krk-goal070b-official-cli-surface-summary-v0.md)

## Platform Support Status

- macOS/Linux-style Python environments: supported by current repository tests and CLI commands.
- Windows/WSL/native Windows: deferred unless validated separately.
- Provider credentials: not required for the first-value path.
- GPU/CUDA/H100: not required for the first-value path.
- Network access: not required for the first-value path.

## Limitations

- The CLI uses public fixtures, not user workloads.
- `kora run` keeps dual behavior: no example runs first-value fixtures; an example name runs the legacy example path.
- JSON output is supported for `inspect`, `compare`, and `run`; Markdown output is concentrated in `report`.
- Console-script behavior depends on package installation. `python3 -m kora ...` works directly from the repository checkout.
- This is local dry-run onboarding, not production execution.

## Claim Boundary

Supported:

- KORA has official public-safe CLI commands for `inspect`, `compare`, `run`, and `report`.
- The official first-value CLI path works without provider credentials, GPU, or network access.
- The official CLI path produces JSON and Markdown evidence through `kora report`.
- The compatibility script remains functional.

Not supported:

- production proof.
- production adoption.
- production readiness.
- production cost reduction.
- customer savings.
- energy reduction.
- broad workload superiority.
- real API/GPU cost reduction.
- provider superiority.
- H100 superiority.

## Roadmap to Installable Package Polish

Recommended next improvements:

- Add richer terminal formatting while preserving plain text and JSON outputs.
- Add workload selection once public workload specs are stable.
- Add `--matrix` or workload-source options to official commands when reviewer-safe defaults are defined.
- Add shell-completion documentation if the CLI grows.
- Add install-path smoke tests for built wheels and editable installs.
- Keep the claim boundary visible in report outputs and docs.
