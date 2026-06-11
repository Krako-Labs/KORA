# KORA Core Report Definition v0

Status: alpha surface definition. Current reporting exists through benchmark, telemetry, and docs paths; this is not yet a complete KORA Core report command spec.

## Definition

`report` is the KORA Core workflow for producing bounded, reproducible evidence from inspect, compare, or run outputs.

Report should answer:

> What happened, how can it be reproduced, and what claims are allowed?

## Inputs

Possible future inputs:

- route decisions.
- benchmark output.
- telemetry summary.
- workload metadata.
- target metadata.
- reproducibility metadata.
- claim boundary.

## Expected Output

Report should include:

- run or benchmark identifier.
- workload identifier.
- route policy.
- selected route or route distribution.
- counters and metrics.
- measured versus unmeasured fields.
- fallback classification.
- reproducibility commands.
- artifact policy.
- claim boundary.

## Current Alpha Status

Current reporting is represented by:

- runtime evidence reviewer guide.
- benchmark result summary.
- telemetry summary paths.
- KRK performance table package.
- KRK evidence package.
- claim boundary docs.

The current base does not expose a first-class top-level `report` command for KORA Core.

## Relationship To KRK

KRK produces route decisions and route evidence. Report packages those decisions into reviewable evidence.

Report should preserve the distinction between:

- measured values.
- simulated benchmark counters.
- methodology-only placeholders.
- future experiment plans.

## Roadmap

Near-term report work should:

- generate a report from existing runtime benchmark JSON.
- include claim boundary automatically.
- include reproducibility metadata.
- mark unmeasured metrics explicitly.
- keep raw artifacts out of public docs unless a reviewed artifact policy freezes them.

## Claim Boundary

Report is an evidence surface, not a marketing surface.

Reports must not claim production cost reduction, customer savings, infrastructure savings, broad workload superiority, H100 superiority, or replacement of provider/router systems unless separate public evidence and claim review support those statements.
