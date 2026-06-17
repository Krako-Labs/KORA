# KORA Core Run Definition v0

Status: alpha surface definition with partial current CLI overlap.

## Definition

`run` is the KORA Core workflow for executing a selected workload path under explicit policy, target, and evidence constraints.

Run should answer:

> Execute this workload under this policy, and record what happened.

## Inputs

Possible future inputs:

- workload fixture.
- route policy.
- target registry.
- adapter configuration.
- evidence output path.
- dry-run or execution mode.

## Expected Output

Run should produce:

- selected route decisions.
- execution status.
- validation status.
- telemetry counters.
- fallback events.
- reproducibility metadata.
- report-ready evidence.

## Current Alpha Status

The current CLI has an example-oriented `run` command:

```bash
python3 -m kora run hello_kora -- --offline
python3 -m kora run direct_vs_kora -- --offline
python3 -m kora run runtime_integrated_benchmark -- --offline
```

This is not yet the full KORA Core workload `run` workflow.

Current `run` is useful for:

- local/offline examples.
- deterministic-first demonstrations.
- runtime benchmark evidence paths.
- public-safe validation examples.

Future KORA Core `run` should separate example execution from workload execution.

## Relationship To KRK

Run should call KRK for route selection before execution when route selection is needed.

KRK decides the route. Run executes the selected path and records outcomes.

## Roadmap

Near-term run work should:

- keep existing example `run` behavior stable.
- define workload-run input shape.
- require explicit dry-run versus execution mode.
- fail closed for unavailable providers, GPU targets, or unsafe configuration.
- emit report-ready structured evidence.

## Claim Boundary

Run output must not imply production readiness, production savings, customer savings, infrastructure savings, or broad workload superiority.
