# KORA First Paper Reference Metadata Audit v0.1

## Purpose

This audit checks metadata completeness and traceability for `[R01]` through `[R24]` before bibliography normalization and BibTeX preparation.

It is a metadata-readiness pass. It does not generate BibTeX, does not change manuscript text, and does not make the paper submission-ready.

## Scope

This audit covers:

- references `[R01]` through `[R24]`
- the current reference tracker
- the citation style decision
- citation audit v0.1
- metadata completeness before normalized bibliography work
- traceability from each stable `[Rxx]` label to a source URL or DOI

This pass does not generate BibTeX. This pass does not modify manuscript v0.3.

## Audit Rules

- Do not invent metadata.
- Do not infer missing authors, venues, years, dates, DOIs, or URLs.
- Use official source pages, DOI pages, arXiv pages, ACL Anthology, ACM, USENIX, MLSys, official documentation, or official repositories.
- Distinguish paper references from official docs, official repositories, policy pages, and venue guidance pages.
- Mark metadata status explicitly before normalization.
- Keep `[Rxx]` labels stable.
- Treat official docs and repositories as organization-owned references when an individual author list is not appropriate.
- Preserve access-date needs for official docs, repositories, and living policy or venue pages until final style conversion.

## Metadata Completeness Table

| ID | Topic | Source type | Title status | Author/org status | Year/date status | URL/DOI status | Venue/status | Metadata status | Action |
|---|---|---|---|---|---|---|---|---|---|
| `[R01]` | vLLM / PagedAttention | paper / arXiv / DOI | title recorded | full author list recorded | year and venue recorded | arXiv URL and DOI recorded | SOSP 2023 recorded from tracker | complete enough for normalized bibliography | normalize next |
| `[R02]` | MLPerf Inference | paper / arXiv | title recorded | author lead with `et al.` in tracker | year and revision note recorded | arXiv URL recorded | arXiv status recorded; venue normalization still needed | needs metadata normalization | review before BibTeX |
| `[R03]` | ONNX Runtime docs | official docs | title recorded | organization owner recorded | date unavailable; access date recorded | official docs URL recorded | documentation reference | official docs/repo reference | keep as official docs reference |
| `[R04]` | LangGraph Graph API docs | official docs | title recorded | organization owner recorded | date unavailable; access date recorded | official docs URL recorded | documentation reference | official docs/repo reference | keep as official docs reference |
| `[R05]` | DSPy | paper / arXiv | title recorded | full author list recorded | year recorded | arXiv URL recorded | arXiv status recorded; venue normalization still needed | needs metadata normalization | review before BibTeX |
| `[R06]` | Retrieval-Augmented Generation | paper / arXiv / DOI | title recorded | full author list recorded | year and venue recorded | arXiv URL and DOI recorded | NeurIPS 2020 recorded | complete enough for normalized bibliography | normalize next |
| `[R07]` | Apache Airflow DAG docs | official docs | title recorded | organization owner recorded | docs version and access date recorded | official docs URL recorded | documentation reference | official docs/repo reference | keep as official docs reference |
| `[R08]` | Snakemake | paper / DOI | title recorded | full author list recorded | year recorded | DOI recorded | journal metadata recorded | complete enough for normalized bibliography | normalize next |
| `[R09]` | llama.cpp | official repo | title recorded | organization owner recorded | date unavailable; access date recorded | official repo URL recorded | repository reference | official docs/repo reference | keep as official docs reference |
| `[R10]` | ACM Artifact Review and Badging | official policy | title recorded | organization owner recorded | version/year recorded | official policy URL recorded | policy page | official artifact/evaluation guidance | review before BibTeX |
| `[R11]` | ReAct | paper / arXiv / DOI | title recorded | full author list recorded | year and venue recorded | arXiv URL and DOI recorded | ICLR 2023 recorded | complete enough for normalized bibliography | normalize next |
| `[R12]` | Toolformer | paper / arXiv / DOI | title recorded | full author list recorded | year recorded | arXiv URL and DOI recorded | arXiv status recorded; venue normalization still needed | needs metadata normalization | review before BibTeX |
| `[R13]` | PAL | paper / arXiv / DOI | title recorded | full author list recorded | year and revision note recorded | arXiv URL and DOI recorded | arXiv status recorded; venue normalization still needed | needs metadata normalization | review before BibTeX |
| `[R14]` | GPTCache | paper / ACL Anthology / DOI | title recorded | author recorded | year, venue, and pages recorded | ACL Anthology URL and DOI recorded | NLP-OSS 2023 recorded | complete enough for normalized bibliography | normalize next |
| `[R15]` | Ollama docs and repo | official docs / official repo | title recorded | organization owner recorded | date unavailable; access date recorded | docs URL and repo URL recorded | documentation and repository reference | official docs/repo reference | keep as official docs reference |
| `[R16]` | NeurIPS reproducibility report | paper / arXiv / DOI | title recorded | full author list recorded | year recorded | arXiv URL and DOI recorded | report status recorded; venue normalization still needed | needs metadata normalization | review before BibTeX |
| `[R17]` | USENIX NSDI artifact guidance | official venue guidance | title recorded | organization owner recorded | conference year range recorded | official USENIX URL recorded | venue guidance page | official artifact/evaluation guidance | defer until venue style selected |
| `[R18]` | MLSys artifact evaluation guidance | official venue guidance | title recorded | organization owner recorded | conference year recorded | official MLSys URL recorded | venue guidance page | official artifact/evaluation guidance | defer until venue style selected |
| `[R19]` | BIG-bench | benchmark suite paper / arXiv / DOI | title recorded | author lead with `et al.` in tracker | year and journal reference recorded | arXiv URL and DOI recorded | TMLR recorded | needs metadata normalization | review before BibTeX |
| `[R20]` | HELM | benchmark suite paper / arXiv / DOI | title recorded | author lead with `et al.` in tracker | year and journal reference recorded | arXiv URL and DOI recorded | TMLR recorded | needs metadata normalization | review before BibTeX |
| `[R21]` | SWE-bench | benchmark paper / arXiv / DOI | title recorded | full author list recorded | year and venue recorded | arXiv URL and DOI recorded | ICLR 2024 recorded | complete enough for normalized bibliography | normalize next |
| `[R22]` | AgentBench | benchmark paper / arXiv / DOI | title recorded | author lead with `et al.` in tracker | year and venue recorded | arXiv URL and DOI recorded | ICLR 2024 recorded | needs metadata normalization | review before BibTeX |
| `[R23]` | Dynabench | benchmark paper / arXiv / DOI | title recorded | author lead with `et al.` in tracker | year and venue recorded | arXiv URL and DOI recorded | NAACL 2021 recorded | needs metadata normalization | review before BibTeX |
| `[R24]` | CheckList | benchmark/test-design paper / ACL Anthology / DOI | title recorded | full author list recorded | year, venue, and pages recorded | ACL Anthology URL and DOI recorded | ACL 2020 recorded | complete enough for normalized bibliography | normalize next |

## Source-Type Summary

Counts by source type in this audit:

- peer-reviewed or preprint paper: 16
- official docs: 4
- official repo: 2
- official artifact/evaluation guidance or policy: 3
- benchmark suite paper/report: 6
- other: 0

Some references belong to more than one practical category. For example, `[R19]` through `[R24]` are counted as benchmark suite paper/report references and also as paper references where applicable. The summary is intended for bibliography planning, not a mutually exclusive taxonomy.

## High-Risk Metadata Items

References requiring extra caution before BibTeX:

- `[R03]`, `[R04]`, `[R07]`, `[R09]`, and `[R15]`: official docs or repositories need organization-owner handling and access-date formatting.
- `[R10]`, `[R17]`, and `[R18]`: artifact policy or venue guidance pages need careful treatment as guidance pages, not formal artifact approval.
- `[R02]`, `[R05]`, `[R12]`, `[R13]`, `[R16]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]`: tracker entries need final author-list or venue/status normalization before BibTeX.
- `[R17]` and `[R18]`: venue-specific guidance should remain deferred until target venue strategy is selected.
- `[R14]`: the source title includes cost-related wording; citation use must not imply KORA production cost or real API-cost evidence.
- `[R19]` through `[R24]`: benchmark references are methodology/background only and must not be used as KORA production benchmark evidence.

## BibTeX Readiness

| ID range | BibTeX readiness | Reason |
|---|---|---|
| `[R01]`, `[R06]`, `[R08]`, `[R11]`, `[R14]`, `[R21]`, `[R24]` | likely ready after normalized bibliography pass | Core title, author, year/date, source URL/DOI, and venue/source details are already present in the tracker. Final formatting still needs normalization. |
| `[R02]`, `[R05]`, `[R12]`, `[R13]`, `[R16]`, `[R19]`, `[R20]`, `[R22]`, `[R23]` | needs extra review before BibTeX | These entries need author-list handling, venue/status normalization, or source-page cross-checking before BibTeX fields are generated. |
| `[R03]`, `[R04]`, `[R07]`, `[R09]`, `[R15]` | official docs/repo BibTeX requires style decision | Organization owner, access date, and documentation/repository entry type need final style treatment. |
| `[R10]`, `[R17]`, `[R18]` | defer until venue style selected | Policy and venue-guidance pages need careful type, owner, date, and access-date formatting. |

BibTeX is not generated in this task. BibTeX should be generated later only from normalized and verified fields.

## Claim-Safety Note

This metadata audit does not change claim support.

- External references remain background, related-work, methodology, reproducibility, artifact-practice, or future-work support only.
- KORA's 80/100 result remains supported by KORA deterministic-heavy benchmark docs and evidence.
- These references do not support production cost reduction proof.
- These references do not support real API-cost reduction proof.
- These references do not support energy reduction evidence.
- These references do not support production benchmark proof.
- These references do not support broad workload superiority.
- Artifact guidance references do not imply formal artifact approval.

## Next Step

Next steps:

1. Update a normalized bibliography table for `[R01]` through `[R24]`.
2. Generate BibTeX only after normalized fields are verified.
3. Keep the paper not submission-ready until bibliography normalization, BibTeX, and final claim audit are stable.
