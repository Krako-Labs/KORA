# KORA First Paper v0.9 Figure Rebuild Specification

Status date: 2026-05-18

## Purpose

This specification defines the rebuild requirements for Figure 1 and Figure 2 in manuscript v0.9:

- `docs/paper/kora-first-paper-manuscript-v0-9.md`

Current Figure 1 and Figure 2 remain text placeholders only. This task does not generate final figures, image assets, Word files, PDF files, arXiv files, archives, or export artifacts. Final figures should be generated in a later task only after this specification is reviewed.

Earlier Word review figures are not accepted for publication use because arrows and diagram elements did not render reliably in the generated Word draft. The rebuilt figures should therefore prioritize stable, simple geometry and export-safe readability over decorative styling.

## Scope

In scope:

- specify the intended purpose, visual structure, required labels, captions, and claim boundaries for Figure 1 and Figure 2
- define rendering constraints to avoid the prior Word arrow and diagram breakage
- define later export/readability requirements for Word and PDF use
- state visual non-claims that must not be implied

Out of scope:

- figure generation
- image rendering
- Word export
- PDF export
- arXiv source-package work
- manuscript v0.9 body edits
- final bibliography formatting

## Figure 1: KORA Execution-Control Architecture

### Intended Purpose

Figure 1 should explain KORA's architectural role as an execution-control layer placed before model inference. The figure should help readers understand the call/no-call boundary: KORA first attempts deterministic, structured, policy, or validation routes, then escalates to a model-candidate path only when deterministic handling is insufficient.

### Required Visual Structure

Figure 1 should use a left-to-right flow with one primary path and one clearly separated escalation path.

Minimum structure:

1. Request intake
2. KORA execution-control layer
3. Task graph or task-path representation
4. Deterministic, structured, policy, or validation route
5. Validated output
6. Model-candidate escalation path for unresolved cases
7. Validation and telemetry after either route

Recommended layout:

```text
Request
  -> KORA execution control
  -> Task path / task graph
  -> Deterministic or structured route
  -> Validation
  -> Output

Task path / task graph
  -> Model-candidate escalation when deterministic handling is insufficient
  -> Validation
  -> Output

Telemetry records route decisions and counters across both paths.
```

The visual should make deterministic-first control the main reading path. Model escalation should be visible but secondary, not hidden and not drawn as a failure.

### Minimum Labels

Required labels:

- Request
- KORA execution control
- Task path or task graph
- Deterministic/structured route
- Policy/validation
- Model-candidate escalation
- Output
- Telemetry

Optional labels if space allows:

- Known logic / templates / lookups
- Model required when deterministic handling is insufficient
- Route counters

### Caption Requirements

The caption should state that KORA inserts an execution-control layer before inference, attempts deterministic or structured routes when sufficient, validates route outcomes, records telemetry, and keeps model escalation available when deterministic handling is insufficient.

The caption must state that the figure describes architecture only and does not claim production readiness.

### Claim-Boundary Constraints

Figure 1 must not imply:

- every task can be handled deterministically
- KORA removes the need for models
- KORA replaces model-serving systems, workflow engines, RAG systems, agent frameworks, or local runtimes
- KORA improves model runtime internals, scheduler performance, batching, memory management, or kernel performance
- KORA is production-deployed or externally validated
- KORA has proven production cost reduction, real API-cost reduction, energy reduction, or broad workload superiority

## Figure 2: Direct Baseline vs KORA-Controlled Benchmark Flow

### Intended Purpose

Figure 2 should explain the deterministic-heavy benchmark comparison behind the approved claim boundary. It should show that the direct baseline counts one simulated model invocation for every task, while the KORA-controlled path routes deterministic tasks before inference and counts model-candidate paths only for unresolved tasks.

### Required Visual Structure

Figure 2 should use a two-lane comparison.

Lane 1: direct baseline

```text
100 benchmark tasks -> direct baseline -> 100 simulated model invocations
```

Lane 2: KORA-controlled execution

```text
100 benchmark tasks -> KORA execution control
  -> 80 deterministic/no-model completions
  -> 20 model-candidate paths
  -> 80 avoided simulated model invocations
```

The lanes should be visually parallel so the comparison is obvious. The figure should use simple count boxes rather than dense prose.

### Minimum Labels

Required labels:

- 100 benchmark tasks
- Direct baseline
- 100 simulated model invocations
- KORA-controlled execution
- 80 deterministic/no-model completions
- 20 model-candidate paths
- 80 avoided simulated model invocations
- 80% avoided invocation rate in this workload

Optional labels if space allows:

- deterministic-heavy workload
- zero mismatches in deterministic subset
- simulated invocation counters

### Caption Requirements

The caption should state that Figure 2 compares the naive direct baseline with KORA-controlled execution for the reproducible 100-task deterministic-heavy benchmark workload.

The caption must use the approved benchmark boundary:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

The caption must also state that the result does not imply real API calls, production traffic, production cost savings, latency improvement, energy reduction, or broad workload superiority.

### Claim-Boundary Constraints

Figure 2 must not imply:

- production deployment evidence
- production benchmark proof
- real provider or real API-call validation
- real API-cost reduction proof
- energy reduction proof
- latency improvement proof
- broad workload superiority
- formal external validation
- benchmark results beyond the approved deterministic-heavy benchmark boundary

## Rendering Constraints

The rebuild should avoid the previous Word arrow and diagram-element breakage. Later figure generation should follow these constraints:

- Use simple rectangular boxes and straight connector lines.
- Avoid Mermaid-derived arrow rendering as the publication source.
- Avoid thin arrowheads, overlapping connectors, curved arrows, diagonal connectors, nested arrow groups, and tiny labels.
- Keep all text as large, high-contrast, horizontal labels.
- Prefer a single font family and consistent font sizes.
- Keep connector lines thick enough to survive Word scaling and PDF conversion.
- Keep arrowheads simple and large if arrows are used at all.
- Do not rely on gradients, shadows, transparency, or small decorative icons to convey meaning.
- Design figures so they remain readable when printed in grayscale.
- Leave adequate whitespace around labels and connectors.
- Keep figure geometry stable at manuscript column width and full-page draft width.

## Later Export and Readability Requirements

Before final insertion into Word, PDF, or arXiv packaging, each rebuilt figure should pass a visual review in the target format.

Required later checks:

- labels remain readable at expected Word review size
- arrows or connectors render correctly after Word insertion
- connectors do not detach from boxes
- no label overlaps a connector, box, or neighboring label
- grayscale rendering remains understandable
- figure can be exported to the final package format without broken elements
- caption and visual labels agree with manuscript v0.9 wording or its successor manuscript
- the figure does not introduce claims broader than the manuscript text

Preferred future asset approach:

- create a source-editable figure file for design iteration
- export a stable raster image for Word review if vector import remains unreliable
- use a separate final export pass for publication packaging after visual review

## Visual Non-Claims

Neither figure may visually imply:

- production deployment evidence
- production benchmark proof
- real provider validation
- real API-cost reduction proof
- energy reduction proof
- latency improvement proof
- broad workload superiority
- formal external validation or artifact approval
- signed partner validation
- guaranteed adoption or funding
- final submission readiness

## Current Status

Figure 1 and Figure 2 remain placeholders in manuscript v0.9. This specification is a planning document for a later figure-finalization task. It does not create or commit figures, images, Word documents, PDFs, arXiv files, archives, or export artifacts. Word/PDF/arXiv/export work remains paused. The paper remains not submission-ready.
