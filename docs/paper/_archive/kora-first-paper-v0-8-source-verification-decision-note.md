# KORA First Paper v0.8 Source Verification Decision Note

Decision date: 2026-05-18

## Purpose

This note converts the v0.8 source-verification packet into explicit source-verification decisions for the next manuscript-planning step. It is a decision note only.

This note does not modify manuscript v0.8, add references, generate BibTeX, rebuild figures, generate Word/PDF/arXiv/export artifacts, or mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-8.md`
- `docs/paper/kora-first-paper-v0-8-source-verification-packet.md`
- `docs/paper/kora-first-paper-v0-7-citation-cleanup-action-plan.md`
- `docs/paper/kora-first-paper-v0-8-citation-cleanup-delta.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-final-blocked-metadata-review-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-bibliography-scope-v0-1.md`
- `docs/paper/kora-first-paper-final-bibliography-claim-audit-v0-1.md`

## Decision Summary

Manuscript v0.8 currently cites `[R01]`, `[R03]`, `[R04]`, `[R05]`, `[R06]`, `[R07]`, `[R08]`, `[R09]`, `[R10]`, `[R11]`, `[R12]`, and `[R13]`.

The decision for v0.9 planning is conservative:

- Keep the current v0.8 cited set available for a v0.9 manuscript draft, but do not treat final source verification or final bibliography formatting as complete.
- Do not add optional preliminary records `[R14]`, `[R16]`, `[R21]`, or `[R24]` to v0.9 unless a later scoped text edit creates a clear need and verifies the source.
- Do not add blocked records `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, or `[R23]`.
- Defer `[R17]` and `[R18]` until final venue/package direction makes artifact-guidance citations necessary.
- Defer final citation style conversion, final BibTeX synchronization, and export-package bibliography hygiene until packaging/export work resumes.

Figure 1 and Figure 2 remain text placeholders only. Figure rebuild, Word export, PDF export, arXiv work, archive creation, and generated artifact creation remain out of scope.

## Approve for v0.9 Inclusion if Existing Repo Evidence Is Sufficient

These records or areas are approved to remain in a possible v0.9 manuscript draft because existing repo evidence supports continued manuscript review. This is not final bibliography approval.

| Record ID or area | Related manuscript section | Current status | Verification decision | Reason for decision | Evidence already available in repo | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| `[R01]` | Related work / systems context | Resolved for v0.8 review | Approve to remain in v0.9 draft if no claim broadening occurs. | Existing repo evidence treats the record as part of the stable cited set and does not use it as KORA benchmark proof. | v0.8 source-verification packet, preliminary BibTeX, normalized bibliography, and v0.8 citation cleanup delta. | Keep in the working cited set; recheck final metadata before bibliography freeze. |
| `[R06]` | Related work / retrieval-augmented generation context | Resolved for v0.8 review | Approve to remain in v0.9 draft if no claim broadening occurs. | Existing repo evidence treats the record as part of the stable cited set and not as evidence for KORA-specific benchmark results. | v0.8 source-verification packet, preliminary BibTeX, normalized bibliography, and v0.8 citation cleanup delta. | Keep in the working cited set; recheck final metadata before bibliography freeze. |
| `[R08]` | Related work / workflow or DAG orchestration context | Resolved for v0.8 review | Approve to remain in v0.9 draft if no claim broadening occurs. | Existing repo evidence supports continued conservative related-work positioning. | v0.8 source-verification packet, preliminary BibTeX, normalized bibliography, and v0.8 citation cleanup delta. | Keep in the working cited set; recheck final metadata before bibliography freeze. |
| `[R11]` | Related work / agent or tool-use context | Resolved for v0.8 review | Approve to remain in v0.9 draft if no claim broadening occurs. | Existing repo evidence supports continued related-work use and does not imply broad workload superiority. | v0.8 source-verification packet, preliminary BibTeX, normalized bibliography, and v0.8 citation cleanup delta. | Keep in the working cited set; recheck final metadata before bibliography freeze. |
| Current cited marker/reference set | Whole manuscript | Resolved for v0.8 marker alignment | Approve the same working marker set for v0.9 only if no manuscript citation additions are made. | v0.8 preserves the intended cited set and keeps optional, deferred, and blocked records outside the body. | v0.8 source-verification packet and v0.8 citation cleanup delta. | Repeat marker/reference/BibTeX sync after any v0.9 edit. |
| Figure placeholder separation | Figure 1 and Figure 2 locations | Resolved for this source-verification decision | Approve continued placeholder treatment for v0.9 planning. | Figure quality and final figure assets are separate from citation/source verification. | Manuscript v0.8 and submission-candidate status. | Keep figure rebuild in a later dedicated task. |

## Requires Manual or External Verification Before Inclusion

These items should not be treated as final source-verified records. Current cited records in this section may remain in a working v0.9 draft, but final metadata/source verification must happen before bibliography freeze or export packaging.

| Record ID | Related manuscript section | Current status | Verification decision | Reason for decision | Evidence already available in repo | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| `[R03]` | LLM serving and local runtime context | Cited in v0.8; source treatment unresolved | Requires manual/external verification before final bibliography approval. | Documentation or repository-style metadata still needs final entry type, owner/publisher, URL, access-date, and style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Keep as a working citation if needed; verify source metadata before bibliography freeze. |
| `[R04]` | Agent/tool routing context | Cited in v0.8; source treatment unresolved | Requires manual/external verification before final bibliography approval. | Documentation or repository-style metadata still needs final entry type, owner/publisher, URL, access-date, and style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Keep as a working citation if needed; verify source metadata before bibliography freeze. |
| `[R05]` | Programmatic AI workflow context | Cited in v0.8; source treatment unresolved | Requires manual/external verification before final bibliography approval. | Paper/preprint metadata still needs author-list, publication/preprint status, venue/status, DOI if applicable, and URL verification. | Preliminary BibTeX candidate subset and final blocked metadata review. | Keep as a working citation if needed; verify paper metadata before bibliography freeze. |
| `[R07]` | Workflow/DAG orchestration context | Cited in v0.8; source treatment unresolved | Requires manual/external verification before final bibliography approval. | Documentation or repository-style metadata still needs final entry type, version placement, owner/publisher, URL, access-date, and style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Keep as a working citation if needed; verify source metadata before bibliography freeze. |
| `[R09]` | Local runtime systems context | Cited in v0.8; source treatment unresolved | Requires manual/external verification before final bibliography approval. | Repository-style metadata still needs final entry type, owner, URL, access-date, and style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Keep as a working citation if needed; verify repository metadata before bibliography freeze. |
| `[R10]` | Artifact evaluation and artifact-practice context | Cited in v0.8; source treatment unresolved | Requires manual/external verification before final bibliography approval. | Policy/guidance metadata still needs entry type, publisher, version/date, URL, access-date, and style handling. | Preliminary BibTeX candidate subset and final blocked metadata review. | Keep as a working citation if needed; verify policy/guidance metadata before bibliography freeze. |
| `[R12]` | Agent/tool-use context | Cited in v0.8; source treatment unresolved | Requires manual/external verification before final bibliography approval. | Paper/preprint metadata still needs author-list, publication/preprint status, venue/status, DOI if applicable, and URL verification. | Preliminary BibTeX candidate subset and final blocked metadata review. | Keep as a working citation if needed; verify paper metadata before bibliography freeze. |
| `[R13]` | Program-aided language model context | Cited in v0.8; source treatment unresolved | Requires manual/external verification before final bibliography approval. | Paper/preprint metadata still needs author-list, publication/preprint status, venue/status, DOI if applicable, and URL verification. | Preliminary BibTeX candidate subset and final blocked metadata review. | Keep as a working citation if needed; verify paper metadata before bibliography freeze. |
| `[R14]` | Optional semantic caching support | Not cited in v0.8 | Requires manual/external verification before any future inclusion. | Existing repo evidence does not show a current v0.8 need, and the record must not imply KORA production cost proof. | Preliminary BibTeX ready subset, arXiv bibliography scope, and v0.7 citation readiness review. | Keep out unless a later scoped edit adds bounded cache background. |
| `[R16]` | Optional reproducibility-program support | Not cited in v0.8 | Requires manual/external verification before any future inclusion. | Existing repo evidence does not show a current v0.8 need, and final report/preprint or venue/status metadata still needs verification. | Preliminary BibTeX candidate subset, arXiv bibliography scope, and final blocked metadata review. | Keep out unless a later scoped edit adds reproducibility-program background. |
| `[R21]` | Optional benchmark or evaluation methodology support | Not cited in v0.8 | Requires manual/external verification before any future inclusion. | Existing repo evidence does not show a current v0.8 need for methodology expansion. | Preliminary BibTeX ready subset, arXiv bibliography scope, and v0.7 citation readiness review. | Keep out unless a later scoped methodology edit needs it. |
| `[R24]` | Optional benchmark or evaluation methodology support | Not cited in v0.8 | Requires manual/external verification before any future inclusion. | Existing repo evidence does not show a current v0.8 need for methodology expansion. | Preliminary BibTeX ready subset, arXiv bibliography scope, and v0.7 citation readiness review. | Keep out unless a later scoped methodology edit needs it. |

## Defer to Final Packaging/Export

These items should wait until manuscript text, cited-record scope, figure handling, and package route are stable.

| Record ID or area | Related manuscript section | Current status | Verification decision | Reason for decision | Evidence already available in repo | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Working `[Rxx]` labels | Whole manuscript | Working citation labels only | Defer to final packaging/export. | Final citation style depends on final package route and human approval. | Citation style decision notes, v0.7 citation cleanup action plan, v0.8 cleanup delta, and v0.8 source-verification packet. | Convert labels only after manuscript text, cited set, and package route are frozen. |
| Final manuscript-to-BibTeX synchronization | Whole manuscript and bibliography | Pending | Defer to final packaging/export. | Future manuscript edits can change marker/reference/BibTeX alignment. | Manuscript bibliography sync docs, v0.7 readiness review, v0.8 cleanup delta, and v0.8 source-verification packet. | Repeat after any v0.9 or final text/bibliography edits. |
| Unused preliminary record scope | `[R14]`, `[R16]`, `[R21]`, `[R24]` | Outside manuscript body | Defer final include/exclude decision unless a scoped v0.9 text edit needs them. | The records are optional and should not be added merely to enlarge the bibliography. | Preliminary BibTeX, arXiv bibliography scope, v0.7 readiness review, and v0.8 source-verification packet. | Decide after manuscript text scope is stable. |
| Final bibliography formatting | References section and BibTeX | Pending | Defer to final packaging/export. | Formatting should follow final style and source verification outcomes. | Preliminary BibTeX, normalized bibliography, reference metadata audit, and final blocked metadata review. | Apply after final source verification and package-route decision. |
| Export package bibliography hygiene | Final package | Paused | Defer to final packaging/export. | Package-level bibliography checks cannot be completed while Word/PDF/arXiv/export work is paused. | Export readiness, source-package hygiene, dry-build review, and v0.8 source-verification packet. | Recheck after final figures, final text, and export route are ready. |
| Final claim-to-evidence audit | Whole manuscript | Pending | Defer until all citation and manuscript edits are complete. | Citation or bibliography changes can affect claim support and scope. | Final bibliography claim audit, submission-candidate status, and v0.8 source-verification packet. | Re-run after source verification and bibliography formatting are complete. |

## Keep Excluded / Do Not Add

These records or claim areas should not be added to v0.9 from current repo evidence.

| Record ID or area | Related manuscript section | Current status | Verification decision | Reason for decision | Evidence already available in repo | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| `[R02]` | Background or related-work candidate | Still not eligible | Keep excluded / do not add. | Metadata and inclusion blockers remain unresolved. | Final blocked metadata review and v0.7 citation readiness review. | Keep excluded until author-list and venue/status blockers are resolved by a later task. |
| `[R15]` | Local runtime systems candidate | Still not eligible | Keep excluded / do not add. | Combined documentation/repository treatment remains unresolved. | Final blocked metadata review and v0.7 citation readiness review. | Keep excluded until docs/repo treatment is resolved. |
| `[R17]` | Artifact or venue guidance candidate | Deferred | Keep excluded for v0.9 unless venue/package direction changes. | Inclusion depends on final venue or package direction. | arXiv bibliography scope and v0.7 citation readiness review. | Revisit only after target package or venue direction is selected. |
| `[R18]` | Artifact or venue guidance candidate | Deferred | Keep excluded for v0.9 unless venue/package direction changes. | Inclusion depends on final venue or package direction. | arXiv bibliography scope and v0.7 citation readiness review. | Revisit only after target package or venue direction is selected. |
| `[R19]` | Benchmark methodology candidate | Still not eligible | Keep excluded / do not add. | Metadata/style blockers remain unresolved and no scoped manuscript edit currently requires it. | Final blocked metadata review, reference tracker, and v0.7 citation readiness review. | Keep excluded unless a later methodology pass resolves blockers and needs it. |
| `[R20]` | Benchmark methodology candidate | Still not eligible | Keep excluded / do not add. | Metadata/style blockers remain unresolved and no scoped manuscript edit currently requires it. | Final blocked metadata review, reference tracker, and v0.7 citation readiness review. | Keep excluded unless a later methodology pass resolves blockers and needs it. |
| `[R22]` | Benchmark methodology candidate | Still not eligible | Keep excluded / do not add. | Metadata/style blockers remain unresolved and no scoped manuscript edit currently requires it. | Final blocked metadata review, reference tracker, and v0.7 citation readiness review. | Keep excluded unless a later methodology pass resolves blockers and needs it. |
| `[R23]` | Benchmark methodology candidate | Still not eligible | Keep excluded / do not add. | Metadata/style blockers remain unresolved and no scoped manuscript edit currently requires it. | Final blocked metadata review, reference tracker, and v0.7 citation readiness review. | Keep excluded unless a later methodology pass resolves blockers and needs it. |
| Unsupported evidence-claim references | Claims, limitations, and evidence-boundary text | Not supported by current evidence | Keep excluded / do not add. | Current evidence does not support production cost reduction proof, real API-cost reduction proof, production benchmark proof, broad workload superiority proof, energy reduction evidence, formal government validation, signed partner validation, or guaranteed adoption or funding. | Submission-candidate status, final bibliography claim audit, and approved claim-boundary notes. | Do not add references or wording that imply unsupported claims. |

## Status

The v0.8 source-verification decision note is complete as a planning document. Manuscript v0.8 was not modified. No references were invented, no unsupported bibliography entries were added, and the bibliography is not final. Figure 1 and Figure 2 remain text placeholders only, figure rebuild remains out of scope, Word/PDF/arXiv/export work remains paused, and the paper remains not submission-ready.
