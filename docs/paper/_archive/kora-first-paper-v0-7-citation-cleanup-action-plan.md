# KORA First Paper v0.7 Citation Cleanup Action Plan

Plan date: 2026-05-18

## Purpose

This action plan converts the manuscript v0.7 citation and bibliography readiness review into concrete cleanup actions. It is intended to guide a later citation cleanup pass before any final figure rebuild, Word export, PDF export, arXiv source-package work, or submission packaging.

This plan does not rewrite manuscript v0.7, does not add references, does not generate BibTeX, does not rebuild figures, does not generate export artifacts, and does not mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-7.md`
- `docs/paper/kora-first-paper-v0-7-citation-bibliography-readiness.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-bibliography-sync-v0-1.md`
- `docs/paper/kora-first-paper-final-bibliography-claim-audit-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-bibliography-scope-v0-1.md`
- `docs/paper/kora-first-paper-final-blocked-metadata-review-v0-1.md`
- `docs/paper/kora-first-paper-citation-audit-v0-1.md`
- `docs/paper/kora-first-paper-related-work-map.md`
- `docs/paper/kora-first-paper-reference-tracker.md`

## Current v0.7 Citation Baseline

Manuscript v0.7 currently uses the following citation markers and matching references-section entries:

- `[R01]`
- `[R03]`
- `[R04]`
- `[R05]`
- `[R06]`
- `[R07]`
- `[R08]`
- `[R09]`
- `[R10]`
- `[R11]`
- `[R12]`
- `[R13]`

The readiness review found no manuscript citation marker missing from the references section and no unused references-section entry for the current cited marker set.

The current preliminary BibTeX document includes all currently cited records plus unused preliminary records `[R14]`, `[R16]`, `[R21]`, and `[R24]`. Deferred records `[R17]` and `[R18]` remain excluded. Still-not-eligible records `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` remain excluded.

Figure 1 and Figure 2 remain text placeholders only. Figure rebuild, Word export, PDF export, arXiv work, and export package assembly remain paused.

## Ready to Apply Now

| Manuscript location or section | Issue description | Proposed cleanup action | Evidence/source currently available in repo | Status |
| --- | --- | --- | --- | --- |
| Submission-candidate status | The citation cleanup sequence needs a status link after the v0.7 readiness review. | Link this action plan from `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`. | `docs/paper/kora-first-paper-v0-7-citation-bibliography-readiness.md` and this action plan. | Ready |
| Manuscript references section | v0.7 uses working `[Rxx]` labels that are internally aligned but not final export style. | Preserve the current manuscript text until a later citation-style cleanup pass converts the working labels into final approved citation style. | v0.7 citation readiness review found marker/reference alignment with no missing entries. | Ready |
| Related work | Current conservative coverage is enough for continued human review. | Do not add optional related-work citations during the cleanup planning step. Keep `[R14]`, `[R16]`, `[R21]`, and `[R24]` optional until a later scoped edit requires them. | v0.7 citation readiness review and preliminary BibTeX inventory. | Ready |
| Evidence and benchmark wording | KORA empirical claims must remain supported by KORA evidence docs, not by external related-work citations. | Preserve the current claim boundary and avoid using external citations as evidence for KORA benchmark results. | v0.7 citation readiness review and final bibliography claim audit. | Ready |
| Figure placeholder sections | Figure 1 and Figure 2 are not citation cleanup blockers because they remain placeholders. | Keep figure-related work out of this citation cleanup sequence. | v0.7 manuscript and submission-candidate status. | Ready |

## Needs Source Verification

| Manuscript location or section | Issue description | Proposed cleanup action | Evidence/source currently available in repo | Status |
| --- | --- | --- | --- | --- |
| LLM serving and local runtime citations | Final metadata for docs, repositories, and tooling sources needs style and access-date verification. | Recheck final entry type, URL, publisher/organization, and access-date treatment for `[R03]`, `[R09]`, and similar documentation or repository sources before final BibTeX. | Preliminary BibTeX, docs/repo reference style resolution, and final blocked metadata review. | Needs verification |
| Related work paper citations | Paper/preprint entries need final author, venue/status, DOI, and URL verification. | Recheck `[R01]`, `[R05]`, `[R06]`, `[R08]`, `[R11]`, `[R12]`, and `[R13]` before final bibliography freeze. | Preliminary BibTeX and reference metadata audit. | Needs verification |
| Workflow and artifact-practice citations | Documentation-style references may need consistent final formatting. | Verify final formatting for `[R04]`, `[R07]`, and `[R10]`, including whether the final style treats them as documentation, repositories, proceedings, or web resources. | Preliminary BibTeX and docs/repo reference style resolution. | Needs verification |
| Optional semantic caching support | `[R14]` exists in preliminary BibTeX but is not cited by v0.7. | Verify and add only if a later manuscript edit adds a bounded cache-related comparison; do not use it to imply KORA production cost proof. | v0.7 citation readiness review, arXiv bibliography scope, and preliminary BibTeX. | Needs verification |
| Optional reproducibility-program support | `[R16]` exists in preliminary BibTeX but is not cited by v0.7. | Verify and add only if a later manuscript edit expands reproducibility-program background. | v0.7 citation readiness review and preliminary BibTeX. | Needs verification |
| Optional benchmark-methodology support | `[R21]` and `[R24]` exist in preliminary BibTeX but are not cited by v0.7. | Verify and add only if a later methodology pass intentionally expands benchmark-methodology framing. | v0.7 citation readiness review, reference tracker, and preliminary BibTeX. | Needs verification |
| Blocked and still-not-eligible records | `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` remain excluded. | Do not cite until metadata/style blockers are resolved and a later task records an inclusion reason. | Final blocked metadata review and citation readiness review. | Needs verification |

## Defer Until Final Packaging

| Manuscript location or section | Issue description | Proposed cleanup action | Evidence/source currently available in repo | Status |
| --- | --- | --- | --- | --- |
| Whole manuscript | Working `[Rxx]` labels are not final venue or arXiv citation style. | Convert working labels to the final approved citation style only after manuscript text and bibliography scope are frozen. | Citation readiness review and citation style decision notes. | Deferred |
| Whole manuscript and bibliography | Final manuscript-to-final-BibTeX synchronization remains pending. | Repeat marker/reference/BibTeX sync after any v0.8 or later text edits and before any export package. | Manuscript bibliography sync and v0.7 citation readiness review. | Deferred |
| Preliminary BibTeX | Unused preliminary entries `[R14]`, `[R16]`, `[R21]`, and `[R24]` require a final scope decision. | Decide whether each unused preliminary entry stays out, is integrated by a scoped edit, or remains in a non-submission working file. | Preliminary BibTeX and arXiv bibliography scope. | Deferred |
| Final references formatting | Official docs, repositories, policy pages, papers, and preprints need consistent final entry formatting. | Apply final formatting only after source verification and final citation style selection. | Reference style resolution docs and metadata audits. | Deferred |
| Export package | Bibliography files must match the final manuscript and package route. | Recheck bibliography hygiene, source package contents, and citation commands after Word/PDF/arXiv/export work resumes. | Source package readiness and arXiv export readiness docs. | Deferred |
| Final audit | Citation cleanup can affect claim support and scope. | Re-run final claim-to-evidence audit after all manuscript and bibliography edits are complete. | Final bibliography claim audit and v0.7 citation readiness review. | Deferred |

## Do Not Add

| Manuscript location or section | Issue description | Proposed cleanup action | Evidence/source currently available in repo | Status |
| --- | --- | --- | --- | --- |
| Venue or artifact guidance | `[R17]` and `[R18]` remain deferred. | Do not add unless a later venue or package decision makes artifact-guidance citation necessary. | v0.7 citation readiness review and arXiv bibliography scope. | Do not add |
| Benchmark methodology | `[R19]` through `[R24]` should not be forced into the manuscript without a scoped methodology rewrite. | Do not add benchmark-methodology citations merely to enlarge the bibliography. | Citation readiness review and reference tracker. | Do not add |
| Cost or caching framing | `[R14]` must not be used to support KORA production cost-reduction or real API-cost claims. | Do not cite `[R14]` unless the manuscript adds a bounded cache-related comparison and preserves non-claim language. | Citation readiness review and approved claim boundary. | Do not add |
| Blocked records | `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` remain still-not-eligible. | Do not cite until blockers are resolved and inclusion is explicitly approved in a later citation task. | Final blocked metadata review and v0.7 citation readiness review. | Do not add |
| Unsupported evidence claims | Production cost reduction proof, real API-cost reduction proof, production benchmark proof, broad workload superiority proof, energy reduction evidence, formal government validation, signed partner validation, and guaranteed adoption or funding are not supported by current evidence. | Do not add references or wording that imply these claims. | Submission-candidate status, claim audit, and v0.7 citation readiness review. | Do not add |

## Recommended Next Cleanup Sequence

1. Keep manuscript v0.7 text stable while human text review continues.
2. If a later v0.8 or citation cleanup pass changes manuscript text, run a marker/reference scan immediately afterward.
3. Freeze the final cited-record set before any Word/PDF/arXiv/export work resumes.
4. Verify source metadata and final style for every cited record in the frozen set.
5. Decide whether unused preliminary records `[R14]`, `[R16]`, `[R21]`, and `[R24]` are excluded, integrated by scoped manuscript edits, or retained only as non-submission working references.
6. Keep deferred and still-not-eligible records out unless a later task resolves their blockers.
7. Repeat final manuscript-to-final-BibTeX synchronization.
8. Re-run final claim-to-evidence audit.
9. Resume Word/PDF/arXiv/export work only after manuscript text, figure placeholders, bibliography scope, citation style, and source-package blockers are resolved.

## Status

The citation cleanup path is planned but not applied to the manuscript in this task. Manuscript v0.7 citation markers are internally aligned with the references section and covered by current preliminary BibTeX, but final bibliography scope, final citation style conversion, final source verification, and final manuscript-to-final-BibTeX synchronization remain unresolved. Figure 1 and Figure 2 remain placeholders, figure rebuild remains out of scope, Word/PDF/arXiv/export work remains paused, and the paper remains not submission-ready.
