# KORA First Paper v0.9 Figure Draft Note

Status date: 2026-05-20

## Purpose

This note records draft Figure 1 and Figure 2 assets created for manuscript v0.9:

- `docs/paper/kora-first-paper-manuscript-v0-9.md`
- `docs/paper/kora-first-paper-v0-9-figure-rebuild-specification.md`

The assets are draft review figures, not final publication figures. They are based on the merged v0.9 figure rebuild specification and are intended for later human visual review before any manuscript integration, Word export, PDF export, arXiv packaging, or source-package work.

## Draft Assets

| Figure | SVG source | PNG rendering | Status |
| --- | --- | --- | --- |
| Figure 1: KORA execution-control architecture | `docs/assets/paper/kora-first-paper-figure-1-v0-9-draft.svg` | `docs/assets/paper/kora-first-paper-figure-1-v0-9-draft.png` | Draft for review |
| Figure 2: direct baseline vs KORA-controlled benchmark flow | `docs/assets/paper/kora-first-paper-figure-2-v0-9-draft.svg` | `docs/assets/paper/kora-first-paper-figure-2-v0-9-draft.png` | Draft for review |

## Figure 1 Scope

Figure 1 shows KORA as an execution-control layer before inference. It includes request intake, KORA execution control, task path/task graph, deterministic or structured route, validation, output, model-candidate escalation, and telemetry.

The figure is architecture-only. It does not imply production readiness, that every task can be handled deterministically, that models are unnecessary, or that KORA replaces serving systems, workflow engines, RAG systems, agent frameworks, or local runtimes.

## Figure 2 Scope

Figure 2 shows the approved deterministic-heavy benchmark comparison using simulated model-invocation counters:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

The figure does not imply real API calls, production traffic, production benchmark proof, production cost savings, latency improvement, energy reduction, broad workload superiority, formal external validation, signed partner validation, guaranteed adoption, or guaranteed funding.

## Rendering Approach

The draft figures use:

- simple rectangles
- straight connector lines
- large horizontal labels
- high-contrast colors
- no gradients
- no shadows
- no Mermaid-derived source rendering
- flattened PNG renderings alongside editable SVG sources

This approach is intended to reduce the risk of the prior Word arrow and diagram-element rendering issues.

## Current Status

Current Figure 1 and Figure 2 remain placeholders in manuscript v0.9. These draft assets have not been inserted into the manuscript. Word/PDF/arXiv/export work remains paused. Final manuscript integration, final visual review, final figure export decisions, and publication package checks remain for later tasks. The paper remains not submission-ready.
