# KORA Core User Workflow v0

Status: public alpha workflow definition. This is a product and architecture document, not a feature-complete CLI guide.

## User Goal

A KORA Core user should be able to move from workload understanding to route evidence without guessing which execution path was selected.

Target workflow:

```text
inspect -> compare -> run -> report
```

## Current Alpha Path

Today, the public alpha is KRK-oriented. Users can inspect docs, run existing examples, review benchmark evidence, and read telemetry/reporting outputs.

Current verified CLI shape:

```bash
python3 -m kora --help
python3 -m kora examples list
python3 -m kora run hello_kora -- --offline
python3 -m kora run direct_vs_kora -- --offline
python3 -m kora run runtime_integrated_benchmark -- --offline
python3 -m kora telemetry --help
```

This is not yet the full KORA Core workflow. It is the available alpha footing for the workflow described below.

## Future Workflow

### 1. Inspect

A user provides a workload fixture, request, or workload profile.

KORA Core should show:

- workload identity.
- task shape.
- available metadata.
- candidate target classes.
- known policy hints.
- evidence readiness.

### 2. Compare

A user compares route policies, target options, or baselines.

KORA Core should show:

- route distribution.
- expected deterministic/cache/provider/GPU/fallback paths.
- policy differences.
- unsupported or unavailable targets.
- metrics that are measured versus not measured.

### 3. Run

A user executes a selected workload path under explicit constraints.

KORA Core should:

- use the selected policy.
- route through KRK.
- avoid hidden provider or GPU execution.
- record route decisions.
- fail closed when configuration is missing or unsafe.

### 4. Report

A user generates an evidence report.

KORA Core should include:

- workload and commit metadata.
- selected route and reason.
- benchmark or run counters.
- reproducibility commands.
- claim boundary.
- raw artifact policy.

## UX Principles

- Make current status explicit.
- Label roadmap surfaces as roadmap.
- Show measured values separately from placeholders.
- Prefer reproducible commands over screenshots or narrative.
- Keep claim boundaries near evidence tables.
- Never hide fallback or blocked execution.

## Example Alpha Narrative

Current alpha:

1. list examples.
2. run a local/offline example.
3. review telemetry or benchmark counters.
4. read the bounded evidence package.

Future KORA Core:

1. inspect a workload.
2. compare route options.
3. run the selected policy.
4. generate a bounded evidence report.

## Boundary

This workflow does not claim production readiness, provider replacement, infrastructure savings, customer savings, or broad workload superiority.
