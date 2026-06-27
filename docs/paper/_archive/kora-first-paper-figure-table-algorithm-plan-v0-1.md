# KORA First Paper Figure, Table, and Algorithm Plan v0.1

Status date: 2026-05-13

## Purpose

This plan inventories existing paper-support assets and identifies the minimum figure, table, flowchart, pseudocode, and appendix materials needed around manuscript v0.4. It does not create binary image assets, does not submit to arXiv, and does not mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-4.md`
- `docs/paper/kora-first-paper-figures-and-tables.md`
- `docs/paper/kora-first-paper-figure-specs.md`
- `docs/paper/kora-first-paper-table-specs.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-submission-package-readiness-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-style-package-readiness-v0-1.md`
- `docs/paper/kora-first-paper-reproduction-transcript-checklist-v0-1.md`
- `docs/paper/kora-first-paper-artifact-package-inventory-v0-1.md`
- `docs/reports/benchmark_artifact_policy.md`
- `docs/README.md`
- `README.md`
- `experiments/README.md`

## Current Manuscript Version

- Current manuscript: `docs/paper/kora-first-paper-manuscript-v0-4.md`
- Current status: submission-candidate draft, not submission-ready.
- Manuscript v0.4 already contains text tables for deterministic-heavy and customer-support results.
- Manuscript v0.4 has not been edited in this asset pass.

## Existing Assets Found

| Asset or spec | Path | Status for paper |
|---|---|---|
| KORA benchmark evidence card | `docs/assets/kora-benchmark-evidence-card.svg`, `docs/assets/kora-benchmark-evidence-card.png` | Existing public visual; needs paper-fit review before inclusion |
| KORA control layer architecture | `docs/assets/kora_workload_control_layer_architecture.svg` | Existing public visual; candidate architecture reference |
| KORA execution control overview | `docs/assets/kora-execution-control-overview.svg`, `docs/assets/kora-execution-control-overview.png` | Existing public visual; candidate architecture reference |
| Help-test flow | `docs/assets/kora-help-test-flow.svg`, `docs/assets/kora-help-test-flow.png` | Existing public visual; not first-paper core unless appendix needs contributor flow |
| Validation roadmap | `docs/assets/kora-validation-roadmap.svg`, `docs/assets/kora-validation-roadmap.png` | Existing public visual; future-work context only |
| Figure specifications | `docs/paper/kora-first-paper-figure-specs.md` | Planning spec exists |
| Table specifications | `docs/paper/kora-first-paper-table-specs.md` | Planning spec exists |
| Figure/table planning doc | `docs/paper/kora-first-paper-figures-and-tables.md` | Planning doc exists |

## Missing Recommended Assets

- Paper-ready architecture figure draft with caption.
- Paper-ready benchmark-flow figure draft with caption.
- Consolidated deterministic-heavy benchmark result table using only established counters.
- Evidence boundary / non-claim table.
- Deterministic-first routing pseudocode.
- Appendix artifact/reproducibility inventory table using real repository paths.
- Human-reviewed insertion decision for manuscript v0.4 or a later v0.5/export draft.

## Proposed Asset Set

| Asset | Proposed insertion section | Claim boundary | Status |
|---|---|---|---|
| Figure 1: KORA execution-control architecture | Section 3, KORA Execution Model | Architecture explanation only; no production-readiness claim | Drafted in `kora-first-paper-figure-table-algorithm-drafts-v0-1.md`; needs human review |
| Figure 2: direct baseline vs KORA-controlled benchmark flow | Section 4 or Section 5.1 | Simulated model invocation counts only; no real API or cost claim | Drafted; needs human review |
| Table 1: deterministic-heavy benchmark result summary | Section 5.1 | Reproducible deterministic-heavy benchmark only | Drafted; values already established |
| Table 2: evidence boundary / non-claim table | Section 6 or near Results | Separates supported claims from non-claims | Drafted; needs human review |
| Algorithm 1: deterministic-first routing pseudocode | Section 3, after execution model | Conceptual pseudocode only; not an implementation guarantee | Drafted; needs human review |
| Appendix table: artifact/reproducibility inventory | Appendix or Reproducibility section | Repository artifact planning only; no formal artifact approval | Drafted; needs human review |

## Manuscript Insertion Decision

Direct insertion into manuscript v0.4 was deferred in this pass. The manuscript already contains text flow snippets and result tables, and inserting multiple new assets would affect paper layout, numbering, and final export decisions. The safe next step is human review of the draft assets before insertion into manuscript v0.4 or a later manuscript/export draft.

## Status

Paper-ready text asset drafts now exist, but figure/table/algorithm insertion, layout, numbering, and final captions require human review. The paper remains not submission-ready.
