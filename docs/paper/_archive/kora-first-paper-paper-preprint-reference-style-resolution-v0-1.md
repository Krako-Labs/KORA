# KORA First Paper Paper/Preprint Reference Style Resolution v0.1

## Purpose

This document resolves or classifies metadata-style handling for paper and preprint references before expanded BibTeX preparation.

It is a bibliography-planning document. It does not generate BibTeX, does not modify manuscript v0.3, and does not make the paper submission-ready.

## Scope

This pass covers:

- `[R02]` MLPerf Inference
- `[R05]` DSPy
- `[R12]` Toolformer
- `[R13]` PAL / program-aided language models
- `[R16]` NeurIPS reproducibility report
- `[R19]` BIG-bench
- `[R20]` HELM
- `[R22]` AgentBench
- `[R23]` Dynabench

This pass makes no manuscript changes. It does not make a full-paper submission-ready claim. It does not add BibTeX by default.

## Style Rules for Papers and Preprints

- Prefer official paper metadata from DOI, arXiv, ACL, or official publication pages already recorded in tracker and audit docs.
- Distinguish arXiv preprints from published proceedings.
- Do not infer proceedings if only arXiv is verified.
- Do not infer author lists beyond verified metadata.
- Do not infer publication year beyond the verified source year.
- Keep stable `[Rxx]` labels.
- Mark any venue/status uncertainty explicitly.
- Do not use papers or preprints as evidence for KORA superiority or production claims.

## Paper/Preprint Resolution Table

| ID | Reference | Source type | Author-list status | Venue/status treatment | Year/date treatment | BibTeX status | Remaining action |
|---|---|---|---|---|---|---|---|
| `[R02]` | MLPerf Inference | paper / arXiv | author lead with `et al.` recorded; needs author-list normalization or approved `et al.` handling | arXiv status recorded; venue/status still needs normalization | 2019 with revised 2020 note recorded | blocked before BibTeX | normalize author list and venue/status before BibTeX |
| `[R05]` | DSPy | paper / arXiv | full author list recorded | arXiv status recorded; venue/status still needs normalization | 2023 recorded | blocked before BibTeX | normalize venue/status before BibTeX |
| `[R12]` | Toolformer | paper / arXiv / DOI | full author list recorded | arXiv status recorded; venue/status still needs normalization | 2023 recorded | blocked before BibTeX | normalize venue/status before BibTeX |
| `[R13]` | PAL / program-aided language models | paper / arXiv / DOI | full author list recorded | arXiv status recorded; venue/status still needs normalization | 2022 with revised 2023 note recorded | blocked before BibTeX | normalize venue/status before BibTeX |
| `[R16]` | NeurIPS reproducibility report | report / arXiv / DOI | full author list recorded | treat as report/preprint until final report/venue status is normalized; not formal artifact approval | 2020 recorded | blocked before BibTeX | normalize report/venue status before BibTeX |
| `[R19]` | BIG-bench | benchmark suite paper / arXiv / DOI | author lead with `et al.` recorded; needs author-list normalization or approved `et al.` handling | TMLR and arXiv status recorded | 2022 recorded | blocked before BibTeX | normalize author list or approved `et al.` style before BibTeX |
| `[R20]` | HELM | benchmark suite paper / arXiv / DOI | author lead with `et al.` recorded; needs author-list normalization or approved `et al.` handling | TMLR and arXiv status recorded | 2023 recorded | blocked before BibTeX | normalize author list or approved `et al.` style before BibTeX |
| `[R22]` | AgentBench | benchmark paper / arXiv / DOI | author lead with `et al.` recorded; needs author-list normalization or approved `et al.` handling | ICLR 2024 and arXiv status recorded | 2024 recorded | blocked before BibTeX | normalize author list or approved `et al.` style before BibTeX |
| `[R23]` | Dynabench | benchmark paper / arXiv / DOI | author lead with `et al.` recorded; needs author-list normalization or approved `et al.` handling | NAACL 2021 and arXiv status recorded | 2021 recorded | blocked before BibTeX | normalize author list or approved `et al.` style before BibTeX |

## Updated Blocker Status

Ready for preliminary BibTeX after author-list/venue check:

- `[R05]`
- `[R12]`
- `[R13]`
- `[R16]`

Needs author-list normalization:

- `[R02]`
- `[R19]`
- `[R20]`
- `[R22]`
- `[R23]`

Needs venue/status normalization:

- `[R02]`
- `[R05]`
- `[R12]`
- `[R13]`
- `[R16]`

Keep blocked until final metadata review:

- `[R02]`
- `[R05]`
- `[R12]`
- `[R13]`
- `[R16]`
- `[R19]`
- `[R20]`
- `[R22]`
- `[R23]`

## Claim-Safety Note

Paper and preprint references are related-work, methodology, or background only.

They do not support KORA production claims. They do not support production cost reduction proof, real API-cost reduction proof, energy reduction evidence, or production benchmark proof. They do not prove KORA outperforms cited systems.

KORA's 80/100 result remains supported by KORA deterministic-heavy benchmark docs and evidence.

## Next Step

Next steps:

1. Update normalized bibliography docs with paper/preprint classifications.
2. Perform final metadata review for these records.
3. Expand BibTeX only after author-list and venue/status treatment are verified.
