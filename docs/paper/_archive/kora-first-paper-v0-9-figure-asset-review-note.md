# KORA First Paper v0.9 Figure Asset Review Note

Status date: 2026-05-20

## Scope

This note reviews the draft Figure 1 and Figure 2 assets created for the manuscript v0.9 working draft. It does not modify manuscript text, regenerate figure assets, or create Word, PDF, arXiv, archive, or manuscript export artifacts.

Reviewed sources:

- `docs/paper/kora-first-paper-manuscript-v0-9.md`
- `docs/paper/kora-first-paper-v0-9-figure-rebuild-specification.md`
- `docs/paper/kora-first-paper-v0-9-figure-draft-note.md`
- `docs/assets/paper/kora-first-paper-figure-1-v0-9-draft.svg`
- `docs/assets/paper/kora-first-paper-figure-1-v0-9-draft.png`
- `docs/assets/paper/kora-first-paper-figure-2-v0-9-draft.svg`
- `docs/assets/paper/kora-first-paper-figure-2-v0-9-draft.png`

## Figure 1 Review

Figure 1 matches the manuscript purpose: it presents KORA as an execution-control layer between an application request and model invocation. The draft visual separates request intake, task/path analysis, deterministic or structured execution, validation, model-candidate escalation, output, and telemetry. That structure supports the manuscript's category framing without claiming that KORA is a production deployment result or a replacement for all model calls.

The labels are likely sufficient for draft review. They identify the execution-control layer, deterministic/task-graph path, validation/output path, model-candidate route, and telemetry path. The caption requirement is also supportable because the figure can be described as an architecture/control-flow diagram rather than a performance or deployment result.

The visual structure is suitable for later Word/PDF insertion testing. It uses simple boxes and straight connectors instead of fragile generated diagram arrows. The SVG source remains editable, and the flattened PNG rendering provides a stable fallback for document insertion.

Recommended next action: keep Figure 1 as the current draft asset for human visual review and later insertion testing. Before final manuscript integration, verify that the connector labels and telemetry path remain readable at the actual Word/PDF figure size. No immediate redraw is required unless human reviewers request layout or emphasis changes.

## Figure 2 Review

Figure 2 matches the manuscript purpose: it compares the naive direct baseline against KORA-controlled execution for the approved deterministic-heavy benchmark boundary. The draft visual keeps the benchmark scope explicit by using the 100-task workload, the 100 simulated model invocation baseline, the 80 deterministic/no-model completions, and the 20 model-candidate paths.

The labels are likely sufficient for draft review. The figure communicates the approved claim boundary without broadening it beyond the reproducible deterministic-heavy benchmark. The caption can safely state that the result is limited to simulated model invocations in the benchmark workload.

The visual structure is suitable for later Word/PDF insertion testing. It uses a side-by-side baseline/control comparison with simple boxes, straight connectors, and a flattened PNG fallback. This avoids relying on Mermaid-style or Word-generated connector behavior.

Recommended next action: keep Figure 2 as the current draft asset for human visual review and later insertion testing. Before final manuscript integration, confirm that the benchmark boundary statement remains legible at target figure size and that the visual emphasis does not make the result look like production-cost evidence.

## Visual Claim Boundary

The draft figures preserve the current claim boundary. They should continue to avoid visually implying:

- production deployment evidence
- real API-cost reduction proof
- production benchmark proof
- broad workload superiority
- energy reduction proof
- formal external validation
- signed partner validation
- guaranteed adoption or funding
- benchmark results beyond the approved deterministic-heavy benchmark boundary

Figure 2 may continue to show the approved benchmark result only within this boundary: in a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

## Readiness Decision

The draft Figure 1 and Figure 2 assets are ready for a later human visual review and insertion trial. They should not yet be treated as final publication figures or final manuscript layout.

No figure revision pass is required before an insertion test unless a human reviewer requests design changes. Final figure approval, manuscript insertion, Word/PDF readability checks, and export packaging remain pending.
