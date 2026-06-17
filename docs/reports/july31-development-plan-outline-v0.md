# July 31 Development Plan Outline v0

Status: public-safe planning outline. This document describes possible next-round development work and does not create a release, repo split, or implementation claim.

## Purpose

If selected for the next round, KORA development should move from a KRK-oriented alpha toward a tested KORA Core alpha while keeping evidence and claim boundaries explicit.

North star:

> Make AI workloads routable.

Development sequence:

1. strengthen KRK route-selectivity evidence.
2. implement small KORA Core inspect, compare, run, and report workflows.
3. formalize workload, target, and evidence artifacts.
4. grow examples and developer feedback loops.

## Development Themes

### 1. KRK Next Benchmark Work

Goal:

- make KRK route decisions measurable across mixed workload profiles.

Planned work:

- connect existing KRK matrix fixtures to a dry-run evaluator.
- keep router-visible metadata separate from oracle-only labels.
- generate route distribution tables.
- measure exact route accuracy and acceptable route rate.
- measure unsafe misroute rate.
- measure GPU false positives and false negatives.
- measure cache correctness and fallback rates.
- version the compute-weight formula.

Deliverables:

- matrix evaluator command or script.
- generated public-safe performance table.
- reproducibility instructions.
- updated claim boundary table.

### 2. KORA Core Inspect

Goal:

- help developers understand workload shape before execution.

Planned work:

- read workload fixtures.
- summarize workload classes.
- show available router-visible metadata.
- identify missing policy fields.
- show evidence readiness.
- fail closed on malformed inputs.

Deliverables:

- first tested inspect path.
- public-safe fixture examples.
- docs that clearly label implemented behavior.

### 3. KORA Core Compare

Goal:

- compare route policies, target options, and baselines without executing external workloads.

Planned work:

- compare KRK against baseline policies.
- show route distribution differences.
- show potential fallback behavior.
- show measured vs unmeasured fields.

Deliverables:

- dry-run compare path.
- structured comparison output.
- report-ready summary table.

### 4. KORA Core Run

Goal:

- separate example-oriented runs from future workload execution.

Planned work:

- keep existing example commands stable.
- define a workload-run input contract.
- add small public-safe workload execution path.
- preserve offline/no-network operation for tests.

Deliverables:

- minimal tested workload-run path.
- fixture-based example.
- clear limitation notes.

### 5. KORA Core Report

Goal:

- produce bounded evidence reports from inspect, compare, and run outputs.

Planned work:

- standardize report fields.
- mark measured, simulated, and methodology-only values.
- include reproducibility metadata.
- include claim boundary metadata.

Deliverables:

- structured report output.
- Markdown report export.
- evidence package index updates.

## Workload Spec

Goal:

- define portable workload inputs for KORA Core.

Planned fields:

- workload identity.
- workload profile.
- workload class.
- router-visible metadata.
- policy hints.
- privacy, latency, cost, and quality preferences.
- evidence requirements.

Next milestone:

- make existing KRK matrix fixtures compatible with the Workload Spec v0.

## Target Registry

Goal:

- define explicit execution target metadata.

Target classes:

- deterministic.
- cache.
- CPU.
- provider.
- GPU.
- fallback.

Next milestone:

- add public-safe target registry examples with no credentials or local-only details.

## Evidence Report

Goal:

- make every route decision reportable and bounded.

Planned report fields:

- run ID.
- workload ID.
- target ID.
- selected route.
- routing decision.
- latency or runtime when measured.
- throughput when measured.
- estimated cost only when safe and clearly qualified.
- privacy class.
- fallback classification.
- reproducibility metadata.
- claim boundary.

Next milestone:

- generate evidence reports from the KRK matrix evaluator.

## Developer Examples

Planned example path:

1. deterministic-only workload.
2. cache-heavy workload.
3. mixed-realistic workload.
4. provider-routed sample.
5. GPU-eligible subset.
6. adversarial fallback case.

Each example should include:

- input fixture.
- expected route categories.
- reproducibility command.
- generated evidence summary.
- claim boundary.

## Community Feedback Loop

Planned loop:

1. publish clear example contribution guidelines.
2. invite sanitized workload proposals.
3. review workload proposals against public/private boundaries.
4. add accepted examples as fixtures.
5. run matrix evaluator.
6. update evidence and limitation docs.

Feedback should focus on reproducibility, workflow clarity, missing target classes, and evidence readability.

## Repo Restructuring Timing

Near-term recommendation:

- keep the current public repo structure.
- do not rename or split repos before the July 31 package.
- prepare the docs and module boundaries for a possible future umbrella + core split.

Decision inputs after July 31:

- contributor volume.
- workload fixture volume.
- registry governance needs.
- release cadence differences between engine and examples.
- stability of KORA Core commands.

## Milestones After July 31

### Milestone 1: KRK Matrix Evaluator

- dry-run evaluator for existing matrix fixtures.
- route correctness metrics.
- generated performance table.

### Milestone 2: KORA Core Inspect And Compare

- read-only inspect.
- dry-run compare.
- report-ready output.

### Milestone 3: Workload Spec And Target Registry

- schema validation.
- public-safe examples.
- target metadata examples.

### Milestone 4: Evidence Report

- structured evidence schema.
- Markdown export.
- claim boundary metadata.

### Milestone 5: Developer Preview

- quickstart.
- example suite.
- contribution guide.
- feedback templates.

## Non-Goals

This plan does not include:

- repo renaming.
- GitHub repo creation.
- production service operation.
- provider replacement.
- unsupported savings claims.
- raw GPU artifact publication.
