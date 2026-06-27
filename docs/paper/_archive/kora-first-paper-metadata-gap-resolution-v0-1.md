# KORA First Paper Metadata Gap Resolution v0.1

## Purpose

This document resolves or classifies high-risk metadata gaps before BibTeX preparation for the KORA first paper.

It is a bibliography-readiness planning document. It does not generate BibTeX, does not modify the manuscript, and does not make the paper submission-ready.

## Scope

This pass covers the high-risk entries identified in [KORA First Paper Reference Metadata Audit v0.1](kora-first-paper-reference-metadata-audit-v0-1.md) and represented in [KORA First Paper Normalized Bibliography v0.1](kora-first-paper-normalized-bibliography-v0-1.md).

Scope includes:

- official docs and repository references requiring organization-owner, access-date, and entry-type handling
- artifact policy and venue guidance pages requiring careful style treatment
- paper, preprint, benchmark, and report references requiring author-list or venue/status normalization
- no BibTeX generation
- no manuscript changes

## Resolution Rules

- Do not invent metadata.
- Do not infer missing authors, venues, years, dates, DOIs, or URLs.
- Official docs and repositories should use the project or organization owner when an individual author list is not appropriate.
- Official docs and repositories may require access-date fields in the final bibliography or BibTeX style.
- Artifact guidance pages should be treated as policy or venue guidance pages, not as formal artifact approval.
- Paper and preprint entries require author-list and venue/status normalization before BibTeX fields are generated.
- Unresolved fields remain explicitly marked until a later source-check or venue-style pass resolves them.
- Stable `[Rxx]` labels remain unchanged.

## Gap Resolution Table

| ID | Risk type | Current issue | Resolution / classification | Remaining action | BibTeX impact |
|---|---|---|---|---|---|
| `[R03]` | official docs | ONNX Runtime docs need organization-owner, access-date, and docs-entry style | Treat as official docs owned by ONNX Runtime project / Microsoft, using recorded source URL and access-date handling | choose docs entry style and access-date format | needs docs/repo style decision before BibTeX |
| `[R04]` | official docs | LangGraph Graph API docs need organization-owner, access-date, and docs-entry style | Treat as official docs owned by LangChain, using recorded source URL and access-date handling | choose docs entry style and access-date format | needs docs/repo style decision before BibTeX |
| `[R07]` | official docs | Apache Airflow DAG docs need organization-owner, docs version, access-date, and docs-entry style | Treat as official docs owned by Apache Software Foundation / Apache Airflow project, preserving recorded docs version and access-date handling | choose docs entry style and access-date format | needs docs/repo style decision before BibTeX |
| `[R09]` | official repo | llama.cpp repository needs organization-owner, access-date, and repository-entry style | Treat as official repository owned by ggml-org, using recorded source URL and access-date handling | choose repository entry style and access-date format | needs docs/repo style decision before BibTeX |
| `[R15]` | official docs / repo | Ollama docs and repository need owner, access-date, and style for combined docs/repo citation | Treat as official docs and official repository owned by Ollama, using recorded docs and repo URLs | choose whether to cite docs, repo, or combined record before BibTeX | needs docs/repo style decision before BibTeX |
| `[R10]` | artifact policy | ACM Artifact Review and Badging needs policy-page entry treatment | Treat as official ACM policy/artifact guidance page, not as formal approval of KORA artifacts | choose policy/guidance entry style | needs venue/artifact guidance style decision before BibTeX |
| `[R17]` | venue artifact guidance | USENIX NSDI artifact guidance is venue-specific and target-venue dependent | Treat as official venue guidance owned by USENIX Association and keep deferred until venue/artifact planning | decide whether target venue requires this entry | defer until target venue chosen |
| `[R18]` | venue artifact guidance | MLSys artifact evaluation guidance is venue-specific and target-venue dependent | Treat as official venue guidance owned by MLSys and keep deferred until venue/artifact planning | decide whether target venue requires this entry | defer until target venue chosen |
| `[R02]` | paper / arXiv | MLPerf Inference uses author lead with `et al.` and needs venue/status normalization | Keep as paper/preprint reference with recorded arXiv URL, year, and revision note | normalize author list and venue/status before BibTeX | needs author-list and venue/status normalization |
| `[R05]` | paper / arXiv | DSPy has full author list but needs venue/status normalization | Keep as paper/preprint reference with recorded full author list and arXiv URL | normalize venue/status before BibTeX | needs venue/status normalization |
| `[R12]` | paper / arXiv / DOI | Toolformer has full author list and DOI but needs venue/status normalization | Keep as paper/preprint reference with recorded full author list, arXiv URL, DOI, and year | normalize venue/status before BibTeX | needs venue/status normalization |
| `[R13]` | paper / arXiv / DOI | PAL has full author list, DOI, year, and revision note but needs venue/status normalization | Keep as paper/preprint reference with recorded full author list, arXiv URL, DOI, and revision note | normalize venue/status before BibTeX | needs venue/status normalization |
| `[R16]` | report / arXiv / DOI | NeurIPS reproducibility report has full author list and DOI but needs report/venue status normalization | Keep as paper/report reference with recorded full author list, arXiv URL, DOI, and year | normalize report/venue status before BibTeX | needs venue/status normalization |
| `[R19]` | benchmark suite paper / arXiv / DOI | BIG-bench uses author lead with `et al.` and needs author-list handling | Keep as benchmark-methodology paper with recorded title, TMLR/arXiv status, URL, DOI, and year | normalize author list or approved `et al.` style before BibTeX | needs author-list normalization |
| `[R20]` | benchmark suite paper / arXiv / DOI | HELM uses author lead with `et al.` and needs author-list handling | Keep as benchmark-methodology paper with recorded title, TMLR/arXiv status, URL, DOI, and year | normalize author list or approved `et al.` style before BibTeX | needs author-list normalization |
| `[R22]` | benchmark paper / arXiv / DOI | AgentBench uses author lead with `et al.` and needs author-list handling | Keep as benchmark-methodology paper with recorded title, ICLR/arXiv status, URL, DOI, and year | normalize author list or approved `et al.` style before BibTeX | needs author-list normalization |
| `[R23]` | benchmark paper / arXiv / DOI | Dynabench uses author lead with `et al.` and needs author-list handling | Keep as benchmark-methodology paper with recorded title, NAACL/arXiv status, URL, DOI, and year | normalize author list or approved `et al.` style before BibTeX | needs author-list normalization |

## Docs/Repo Style Resolution

[KORA First Paper Docs/Repo Reference Style Resolution v0.1](kora-first-paper-docs-repo-reference-style-resolution-v0-1.md) classifies `[R03]`, `[R04]`, `[R07]`, `[R09]`, and `[R15]`.

Status:

- `[R03]`, `[R04]`, and `[R07]` are ready for docs-style BibTeX later after final docs entry type and access-date field style are chosen.
- `[R09]` is ready for repository-style BibTeX later after final repository entry type and access-date field style are chosen.
- `[R15]` remains blocked until the final split-or-keep decision is made for the combined docs/repo reference.
- No BibTeX is generated for these records in this pass.

## Artifact Guidance Style Resolution

[KORA First Paper Artifact Guidance Reference Style Resolution v0.1](kora-first-paper-artifact-guidance-reference-style-resolution-v0-1.md) classifies `[R10]`, `[R17]`, and `[R18]`.

Status:

- `[R10]` is ready for artifact-guidance BibTeX later after final policy-page entry type and access-date field style are chosen.
- `[R17]` and `[R18]` remain deferred until target venue selection confirms whether USENIX/NSDI-style or MLSys-style guidance belongs in the final bibliography.
- No BibTeX is generated for these records in this pass.

## Paper/Preprint Style Resolution

[KORA First Paper Paper/Preprint Reference Style Resolution v0.1](kora-first-paper-paper-preprint-reference-style-resolution-v0-1.md) classifies `[R02]`, `[R05]`, `[R12]`, `[R13]`, `[R16]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]`.

Status:

- `[R02]` remains blocked pending author-list normalization or approved `et al.` handling, plus venue/status normalization.
- `[R05]`, `[R12]`, `[R13]`, and `[R16]` remain blocked pending venue/status or report/status normalization.
- `[R19]`, `[R20]`, `[R22]`, and `[R23]` remain blocked pending author-list normalization or approved `et al.` handling.
- No BibTeX is generated for these records in this pass.

## Updated BibTeX Readiness

Ready for preliminary BibTeX after normalized record check:

- `[R01]`, `[R06]`, `[R08]`, `[R11]`, `[R14]`, `[R21]`, `[R24]`

Needs author-list normalization:

- `[R02]`, `[R19]`, `[R20]`, `[R22]`, `[R23]`

Needs venue/status normalization:

- `[R02]`, `[R05]`, `[R12]`, `[R13]`, `[R16]`

Paper/preprint style classification recorded:

- `[R02]`, `[R05]`, `[R12]`, `[R13]`, `[R16]`, `[R19]`, `[R20]`, `[R22]`, `[R23]`

Needs docs/repo style decision:

- `[R03]`, `[R04]`, `[R07]`, `[R09]`, `[R15]`

Needs artifact guidance access-date/style decision:

- `[R10]`

Defer until target venue chosen:

- `[R17]`, `[R18]`

## Entries Still Blocked Before BibTeX

The following entries should not receive BibTeX yet:

- `[R02]`: author-list handling and venue/status normalization remain unresolved.
- `[R03]`, `[R04]`, `[R07]`, `[R09]`, `[R15]`: docs/repo entry style and access-date formatting remain unresolved.
- `[R05]`, `[R12]`, `[R13]`, `[R16]`: venue/status normalization remains unresolved.
- `[R10]`: policy/guidance entry style and access-date field style remain unresolved.
- `[R17]`, `[R18]`: target-venue decision and venue-guidance entry style remain unresolved.
- `[R19]`, `[R20]`, `[R22]`, `[R23]`: author-list handling remains unresolved.

After this paper/preprint style pass, all paper/preprint blockers above remain blocked before BibTeX until final author-list, venue/status, or report/preprint metadata review is complete.

## Final Blocked Metadata Review

[KORA First Paper Final Blocked Metadata Review v0.1](kora-first-paper-final-blocked-metadata-review-v0-1.md) consolidates all remaining blocked records before any expanded BibTeX preparation.

Status:

- All remaining blocked records are grouped as docs/repo, artifact guidance, or paper/preprint records.
- Candidate records for later expanded BibTeX after final field check: `[R03]`, `[R04]`, `[R05]`, `[R07]`, `[R09]`, `[R10]`, `[R12]`, `[R13]`, `[R16]`.
- Deferred records until target venue selection: `[R17]`, `[R18]`.
- Records still not eligible until author-list, split, or venue/style decision: `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, `[R23]`.
- No BibTeX is generated for blocked records in the final review.

Next action categories:

- Resolve access-date and entry-type style for docs/repo and artifact-guidance candidate records.
- Resolve venue/status or report/preprint treatment for candidate paper/preprint records.
- Resolve author-list or approved `et al.` handling before any expanded BibTeX for long-author-list records.
- Keep target-venue-specific artifact guidance deferred until the target venue is selected.

## Claim-Safety Note

Metadata gap resolution does not change claim support.

- External references remain related-work, methodology, background, reproducibility, artifact-practice, or future-work support only.
- KORA's 80/100 result remains supported by KORA deterministic-heavy benchmark docs and evidence.
- These references do not support production cost reduction proof.
- These references do not support real API-cost reduction proof.
- These references do not support energy reduction evidence.
- These references do not support production benchmark proof.
- These references do not support broad workload superiority.
- Bibliography metadata does not imply formal artifact approval.

## Next Step

Next steps:

1. Update normalized bibliography records after any remaining source checks or style decisions.
2. Prepare preliminary BibTeX only for records whose fields are complete and verified.
3. Keep the paper not submission-ready until BibTeX, bibliography, and final claim audit are stable.
