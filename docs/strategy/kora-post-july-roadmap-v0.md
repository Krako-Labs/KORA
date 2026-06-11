# KORA Post-July Roadmap v0

Status: planning document. This roadmap does not create releases, repos, branches, or GitHub changes.

## Purpose

This roadmap describes the post-July path from a KRK-oriented alpha toward KORA Core and the broader KORA ecosystem.

## Current Position

Current public position:

- KORA is the umbrella for routable AI workloads.
- KORA Core is the planned OSS AI workload execution layer.
- KRK is the deterministic-first execution routing kernel inside KORA Core.
- Current alpha is KRK-oriented and evidence-first.

Current implementation center:

- examples.
- runtime benchmark path.
- telemetry.
- KRK docs.
- KORA Core surface definitions.
- bounded evidence package.

## Roadmap Principles

- Evidence over claims.
- Current implementation before future naming.
- Simple developer path before repo split.
- Public-safe examples before registry scale.
- Explicit limitations near benchmark results.

## Phase 1: KRK Stabilization

Goal:

- make KRK understandable, reproducible, and small enough for developers to run.

Focus:

- keep quickstart current.
- stabilize KRK route terminology.
- connect matrix fixtures to a dry-run evaluator.
- generate route distribution and correctness tables.
- keep the performance table package current.

Exit criteria:

- deterministic-heavy benchmark remains reproducible.
- extended matrix dry-run produces structured output.
- claim boundary table is current.
- docs avoid unsupported production or savings claims.

## Phase 2: KORA Core Alpha Surface

Goal:

- turn KRK into the first building block of KORA Core.

Focus:

- inspect: read and summarize workload fixtures.
- compare: dry-run route policies and target options.
- run: separate example run from workload run.
- report: generate bounded evidence from structured outputs.

Exit criteria:

- each workflow has at least one tested public-safe path.
- CLI/API docs clearly match implemented behavior.
- unimplemented roadmap surfaces are labeled.

## Phase 3: Workload Spec And Target Registry

Goal:

- make workloads and targets portable enough for community examples.

Focus:

- KORA Workload Spec v0.
- Target Registry v0.
- schema validation.
- public-safe YAML/JSON examples.
- dry-run target selection.

Exit criteria:

- examples can be inspected without custom code.
- target metadata is explicit.
- missing or unsafe configuration fails closed.

## Phase 4: Evidence Registry Foundation

Goal:

- make evidence packages discoverable and comparable.

Focus:

- Evidence Report schema.
- Evidence Registry concept.
- reproducibility metadata.
- artifact policy.
- claim boundary metadata.

Exit criteria:

- evidence packages can be indexed.
- reports can distinguish measured, simulated, and methodology-only fields.
- raw artifacts are excluded unless explicitly frozen by policy.

## Phase 5: Community And OSS Growth

Goal:

- make it easy for developers to test KORA with sanitized workloads.

Focus:

- workload proposal template.
- example contribution guide.
- issue labels for workload, target, evidence, docs, and good first issue.
- public-safe benchmark review checklist.
- community feedback loop.

Exit criteria:

- contributors can propose workloads without exposing private data.
- maintainers can review examples and evidence consistently.
- docs explain what claims are and are not supported.

## Phase 6: Repo Structure Decision

Goal:

- decide whether the single repo still fits.

Decision inputs:

- volume of workload fixtures.
- stability of KORA Core commands.
- number of external contributors.
- registry governance needs.
- release cadence differences between engine and examples.

Default recommendation:

- remain single-repo unless the split solves a real contributor or artifact-management problem.

Possible next step:

- umbrella + core split after KORA Core alpha stabilizes.

Later possible step:

- workloads or registry repo after workload volume and review policy justify it.

## Post-July Public Narrative

Use:

> KORA makes AI workloads routable. KRK proved the first routing-kernel wedge. KORA Core expands that wedge into an open-source workload execution layer around inspect, compare, run, and report.

Avoid:

- production readiness claims.
- savings claims.
- provider replacement claims.
- infrastructure reduction claims.
- repo-split announcements before a concrete approved migration plan exists.
