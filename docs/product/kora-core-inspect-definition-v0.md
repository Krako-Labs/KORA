# KORA Core Inspect Definition v0

Status: alpha surface definition. This is not a completed command spec.

## Definition

`inspect` is the KORA Core workflow for understanding a workload before route comparison or execution.

Inspect should answer:

> What is this workload, what metadata is visible, and what routing evidence can be produced?

## Inputs

Possible future inputs:

- workload fixture.
- workload profile.
- single request.
- target registry entry.
- evidence report.

## Expected Output

Inspect should summarize:

- workload identity.
- task count.
- task classes.
- router-visible metadata.
- missing metadata.
- candidate execution paths.
- policy hints.
- evidence readiness.
- warnings and blocked conditions.

## Current Alpha Status

Current implementation does not expose a first-class top-level `inspect` command.

Current public materials that support future inspect work:

- workload fixtures.
- KRK routing metadata docs.
- KORA Workload Spec docs.
- KORA Target Registry docs.
- benchmark and evidence package docs.

## Relationship To KRK

Inspect prepares input for KRK. It should not make a route decision by itself unless it is explicitly running a KRK dry-run inspection mode.

KRK selects and explains routes. Inspect makes workload and metadata state visible before that selection.

## Roadmap

Near-term inspect work should:

- read existing workload JSON.
- validate expected fields.
- summarize route-relevant metadata.
- identify missing oracle or router-visible fields.
- produce public-safe output.

## Claim Boundary

Inspect is a workflow definition. Do not describe it as a complete implemented command until implementation and tests exist.
