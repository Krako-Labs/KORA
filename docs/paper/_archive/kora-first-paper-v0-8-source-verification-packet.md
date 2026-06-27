# KORA First Paper v0.8 Source Verification Packet

Packet date: 2026-05-18

## Purpose

This packet records source-verification work remaining after manuscript v0.8. It is a review and planning document only.

This packet does not modify manuscript v0.8, add references, generate BibTeX, rebuild figures, generate Word/PDF/arXiv/export artifacts, or mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-8.md`
- `docs/paper/kora-first-paper-v0-7-citation-cleanup-action-plan.md`
- `docs/paper/kora-first-paper-v0-8-citation-cleanup-delta.md`
- `docs/paper/kora-first-paper-v0-7-citation-bibliography-readiness.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-final-blocked-metadata-review-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-bibliography-scope-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-bibliography-sync-v0-1.md`
- `docs/paper/kora-first-paper-final-bibliography-claim-audit-v0-1.md`
- `docs/paper/kora-first-paper-reference-tracker.md`
- `docs/paper/kora-first-paper-reference-metadata-audit-v0-1.md`
- `docs/paper/kora-first-paper-normalized-bibliography-v0-1.md`

## Current v0.8 Citation Baseline

Manuscript v0.8 cites the following record set:

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

Optional preliminary records `[R14]`, `[R16]`, `[R21]`, and `[R24]` remain outside the manuscript body. Deferred or blocked records `[R02]`, `[R15]`, `[R17]`, `[R18]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` remain outside the manuscript body.

Figure 1 and Figure 2 remain text placeholders only. Figure rebuild, Word export, PDF export, arXiv work, and export package assembly remain paused.

## Already Resolved in v0.8

| Record or area | Manuscript section or related-work area | Issue description | What was verified or resolved | Repo evidence currently available | External/manual verification required? | Recommended next action | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `[R01]` | Related work / systems context | The record remains in the manuscript's stable cited set. | v0.8 keeps the record in the aligned marker/reference set and does not broaden the claim it supports. | Preliminary BibTeX, normalized bibliography, v0.7 readiness review, and v0.8 citation cleanup delta. | Not for continued v0.8 text review; final package metadata still needs a later source check. | Keep in the current cited set and recheck final metadata before bibliography freeze. | Resolved for v0.8 |
| `[R06]` | Related work / retrieval-augmented generation context | The record remains in the manuscript's stable cited set. | v0.8 keeps the record in the aligned marker/reference set and does not use it as KORA benchmark evidence. | Preliminary BibTeX, normalized bibliography, v0.7 readiness review, and v0.8 citation cleanup delta. | Not for continued v0.8 text review; final package metadata still needs a later source check. | Keep in the current cited set and recheck final metadata before bibliography freeze. | Resolved for v0.8 |
| `[R08]` | Related work / workflow or DAG orchestration context | The record remains in the manuscript's stable cited set. | v0.8 keeps the record in the aligned marker/reference set and preserves conservative related-work positioning. | Preliminary BibTeX, normalized bibliography, v0.7 readiness review, and v0.8 citation cleanup delta. | Not for continued v0.8 text review; final package metadata still needs a later source check. | Keep in the current cited set and recheck final metadata before bibliography freeze. | Resolved for v0.8 |
| `[R11]` | Related work / agent or tool-use context | The record remains in the manuscript's stable cited set. | v0.8 keeps the record in the aligned marker/reference set and does not imply broad workload superiority. | Preliminary BibTeX, normalized bibliography, v0.7 readiness review, and v0.8 citation cleanup delta. | Not for continued v0.8 text review; final package metadata still needs a later source check. | Keep in the current cited set and recheck final metadata before bibliography freeze. | Resolved for v0.8 |
| Current cited marker/reference set | Whole manuscript | v0.7 working citation markers needed a conservative cleanup pass. | v0.8 preserves the intended cited set `[R01]`, `[R03]` through `[R13]` and keeps optional, deferred, and blocked records outside the body. | v0.8 citation cleanup delta and submission-candidate status. | No for current marker alignment; yes before final package bibliography freeze. | Repeat marker/reference/BibTeX sync after any future manuscript edit. | Resolved for v0.8 |
| Figure placeholder separation | Figure 1 and Figure 2 locations | Figure quality is not part of citation verification. | v0.8 keeps Figure 1 and Figure 2 as text placeholders and does not add figure assets or figure citations. | Manuscript v0.8 and submission-candidate status. | No for this packet. | Keep figure rebuild in a separate later task after text and bibliography scope stabilize. | Resolved for v0.8 |

## Needs Source Verification Before Inclusion

| Record ID | Manuscript section or related-work area | Issue description | What must be verified | Repo evidence currently available | External/manual verification required? | Recommended next action | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `[R03]` | LLM serving and local runtime context | Documentation or repository-style metadata needs final source treatment. | Final entry type, owner or publisher, URL, access-date treatment, and final style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Yes, before final bibliography freeze. | Keep cited for now; verify source metadata and final style before export work resumes. | Needs source verification |
| `[R04]` | Agent/tool routing context | Documentation or repository-style metadata needs final source treatment. | Final entry type, owner or publisher, URL, access-date treatment, and final style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Yes, before final bibliography freeze. | Keep cited for now; verify source metadata and final style before export work resumes. | Needs source verification |
| `[R05]` | Programmatic AI workflow context | Paper or preprint metadata needs final normalization. | Author list, publication or preprint status, venue/status field, DOI if applicable, and URL. | Preliminary BibTeX candidate subset and final blocked metadata review. | Yes, before final bibliography freeze. | Keep cited for now; verify paper metadata before final package assembly. | Needs source verification |
| `[R07]` | Workflow/DAG orchestration context | Documentation or repository-style metadata needs final source treatment. | Final entry type, version placement, owner or publisher, URL, access-date treatment, and final style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Yes, before final bibliography freeze. | Keep cited for now; verify source metadata and final style before export work resumes. | Needs source verification |
| `[R09]` | Local runtime systems context | Repository-style metadata needs final source treatment. | Repository entry type, owner, URL, access-date treatment, and final style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Yes, before final bibliography freeze. | Keep cited for now; verify repository metadata before export work resumes. | Needs source verification |
| `[R10]` | Artifact evaluation and artifact-practice context | Policy or guidance metadata needs final source treatment. | Policy/guidance entry type, publisher, version or date handling, URL, access-date treatment, and final style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Yes, before final bibliography freeze. | Keep cited for now; verify policy/guidance metadata before final package assembly. | Needs source verification |
| `[R12]` | Agent/tool-use context | Paper or preprint metadata needs final normalization. | Author list, publication or preprint status, venue/status field, DOI if applicable, and URL. | Preliminary BibTeX candidate subset and final blocked metadata review. | Yes, before final bibliography freeze. | Keep cited for now; verify paper metadata before final package assembly. | Needs source verification |
| `[R13]` | Program-aided language model context | Paper or preprint metadata needs final normalization. | Author list, publication or preprint status, venue/status field, DOI if applicable, and URL. | Preliminary BibTeX candidate subset and final blocked metadata review. | Yes, before final bibliography freeze. | Keep cited for now; verify paper metadata before final package assembly. | Needs source verification |
| `[R14]` | Optional semantic caching support | The record exists in preliminary materials but is not cited in v0.8. | Whether a later manuscript edit needs a bounded cache-related comparison and whether the source metadata remains correct. | Preliminary BibTeX ready subset, arXiv bibliography scope, and v0.7 citation readiness review. | Yes, before any inclusion. | Keep out of the manuscript unless a later scoped edit adds cache background without production cost claims. | Needs verification before inclusion |
| `[R16]` | Optional reproducibility-program support | The record exists in preliminary materials but is not cited in v0.8. | Whether a later manuscript edit needs reproducibility-program background and whether final report/preprint or venue/status metadata is correct. | Preliminary BibTeX candidate subset, arXiv bibliography scope, and final blocked metadata review. | Yes, before any inclusion. | Keep out of the manuscript unless a later scoped edit adds reproducibility-program context. | Needs verification before inclusion |
| `[R21]` | Optional benchmark or evaluation methodology support | The record exists in preliminary materials but is not cited in v0.8. | Whether a later methodology edit needs this record and whether source metadata remains correct. | Preliminary BibTeX ready subset, arXiv bibliography scope, and v0.7 citation readiness review. | Yes, before any inclusion. | Keep out of the manuscript unless a later scoped methodology edit needs it. | Needs verification before inclusion |
| `[R24]` | Optional benchmark or evaluation methodology support | The record exists in preliminary materials but is not cited in v0.8. | Whether a later methodology edit needs this record and whether source metadata remains correct. | Preliminary BibTeX ready subset, arXiv bibliography scope, and v0.7 citation readiness review. | Yes, before any inclusion. | Keep out of the manuscript unless a later scoped methodology edit needs it. | Needs verification before inclusion |

## Deferred Until Final Packaging/Export

| Record or area | Manuscript section or related-work area | Issue description | What must be verified | Repo evidence currently available | External/manual verification required? | Recommended next action | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Working `[Rxx]` labels | Whole manuscript | Working labels are acceptable for manuscript review but are not final venue or arXiv citation style. | Final citation style, key mapping, reference ordering, and bibliography format. | Citation style decision notes, v0.7 citation cleanup action plan, and v0.8 delta. | Depends on final package route and human approval. | Convert only after manuscript text, cited set, and package route are frozen. | Deferred |
| Final manuscript-to-BibTeX sync | Whole manuscript and bibliography | Current sync is sufficient for v0.8 review but not final packaging. | Exact final marker/reference/BibTeX alignment after future edits. | Manuscript bibliography sync docs, v0.7 readiness review, and v0.8 delta. | No external source needed for the sync itself; source metadata verification remains separate. | Repeat after any v0.9 or final text/bibliography edits. | Deferred |
| Unused preliminary record scope | `[R14]`, `[R16]`, `[R21]`, `[R24]` | Optional records remain outside the body and need a final include/exclude decision. | Whether each record is excluded, integrated by a scoped manuscript edit, or retained only as a non-submission working reference. | Preliminary BibTeX, arXiv bibliography scope, and v0.8 delta. | Yes, human scope approval required before inclusion. | Decide after manuscript text scope is stable. | Deferred |
| Final bibliography formatting | References section and BibTeX | Docs, repositories, policy pages, papers, and preprints need consistent final formatting. | Entry type, field completeness, punctuation, access-date handling, and final style requirements. | Preliminary BibTeX, normalized bibliography, reference metadata audit, and final blocked metadata review. | Yes, before final package assembly. | Apply after final source verification and package-route decision. | Deferred |
| Export package bibliography hygiene | Final Word/PDF/arXiv/export package | Package-level bibliography checks cannot be completed while export work is paused. | Final source package contents, citation commands, bibliography file names, relative paths, and arXiv/package compatibility. | Export readiness, source-package hygiene, and dry-build review docs. | Yes, after export work resumes. | Recheck only after final figures, final text, and export route are ready. | Deferred |
| Final claim-to-evidence audit | Whole manuscript | Citation edits can affect claim scope. | That every KORA-specific evidence claim remains bounded to current repo evidence and does not become a production, cost, energy, or broad-superiority claim. | Final bibliography claim audit, submission-candidate status, and v0.8 delta. | No external source required for current repo-evidence audit; human review still required. | Re-run after all citation and manuscript edits are complete. | Deferred |

## Still Not Eligible / Do Not Add

| Record ID or claim area | Manuscript section or related-work area | Issue description | What must be verified | Repo evidence currently available | External/manual verification required? | Recommended next action | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `[R02]` | Background or related-work candidate | Metadata and inclusion blockers remain unresolved. | Author-list handling and venue/status normalization before any future inclusion. | Final blocked metadata review and v0.7 citation readiness review. | Yes, before any inclusion. | Keep excluded from the manuscript and bibliography scope for now. | Still not eligible |
| `[R15]` | Local runtime systems candidate | Combined documentation/repository treatment remains unresolved. | Whether to split the docs and repository records or keep a single source entry, plus final metadata style. | Final blocked metadata review and v0.7 citation readiness review. | Yes, before any inclusion. | Keep excluded until the docs/repo treatment is resolved. | Still not eligible |
| `[R17]` | Artifact or venue guidance candidate | Inclusion depends on final venue or package direction. | Whether the final target requires or benefits from this artifact-guidance source. | arXiv bibliography scope and v0.7 citation readiness review. | Yes, after final package route is selected. | Keep excluded until venue/package decisions are made. | Deferred / do not add now |
| `[R18]` | Artifact or venue guidance candidate | Inclusion depends on final venue or package direction. | Whether the final target requires or benefits from this artifact-guidance source. | arXiv bibliography scope and v0.7 citation readiness review. | Yes, after final package route is selected. | Keep excluded until venue/package decisions are made. | Deferred / do not add now |
| `[R19]` | Benchmark methodology candidate | Metadata/style blockers remain unresolved and no scoped manuscript edit currently requires it. | Author-list handling, venue/status normalization, and actual need in a later methodology rewrite. | Final blocked metadata review, reference tracker, and v0.7 citation readiness review. | Yes, before any inclusion. | Keep excluded unless a later methodology pass explicitly resolves blockers and needs the record. | Still not eligible |
| `[R20]` | Benchmark methodology candidate | Metadata/style blockers remain unresolved and no scoped manuscript edit currently requires it. | Author-list handling, approved `et al.` style if used, venue/status normalization, and actual need in a later methodology rewrite. | Final blocked metadata review, reference tracker, and v0.7 citation readiness review. | Yes, before any inclusion. | Keep excluded unless a later methodology pass explicitly resolves blockers and needs the record. | Still not eligible |
| `[R22]` | Benchmark methodology candidate | Metadata/style blockers remain unresolved and no scoped manuscript edit currently requires it. | Author-list handling, approved `et al.` style if used, venue/status normalization, and actual need in a later methodology rewrite. | Final blocked metadata review, reference tracker, and v0.7 citation readiness review. | Yes, before any inclusion. | Keep excluded unless a later methodology pass explicitly resolves blockers and needs the record. | Still not eligible |
| `[R23]` | Benchmark methodology candidate | Metadata/style blockers remain unresolved and no scoped manuscript edit currently requires it. | Author-list handling, approved `et al.` style if used, venue/status normalization, and actual need in a later methodology rewrite. | Final blocked metadata review, reference tracker, and v0.7 citation readiness review. | Yes, before any inclusion. | Keep excluded unless a later methodology pass explicitly resolves blockers and needs the record. | Still not eligible |
| Unsupported evidence-claim references | Claims, limitations, and evidence-boundary text | Current evidence does not support production cost reduction proof, real API-cost reduction proof, production benchmark proof, broad workload superiority proof, energy reduction evidence, formal government validation, signed partner validation, or guaranteed adoption or funding. | No source should be used to imply these claims unless a future evidence package actually supports them and a later review approves the wording. | Submission-candidate status, final bibliography claim audit, and approved claim-boundary notes. | Not applicable for the current manuscript; future evidence would require separate review. | Do not add references or wording that imply these unsupported claims. | Do not add |

## Recommended Next Actions

1. Keep manuscript v0.8 text unchanged while source verification is planned.
2. Verify final source metadata for the current cited set `[R01]`, `[R03]` through `[R13]`.
3. Decide whether optional preliminary records `[R14]`, `[R16]`, `[R21]`, and `[R24]` remain excluded or require scoped manuscript edits.
4. Keep `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` excluded until their blockers are resolved.
5. Keep `[R17]` and `[R18]` excluded until final package or venue direction makes artifact-guidance citations necessary.
6. Repeat final marker/reference/BibTeX synchronization after any future manuscript or bibliography edit.
7. Re-run the final claim-to-evidence audit after source verification and bibliography formatting are complete.
8. Resume Word/PDF/arXiv/export work only after manuscript text, figure placeholders, bibliography scope, citation style, and source-package blockers are resolved.

## Status

The v0.8 source-verification packet is complete as a planning document. Manuscript v0.8 was not modified. No references were invented, no unsupported bibliography entries were added, and the bibliography is not final. Figure 1 and Figure 2 remain placeholders, figure rebuild remains out of scope, Word/PDF/arXiv/export work remains paused, and the paper remains not submission-ready.
