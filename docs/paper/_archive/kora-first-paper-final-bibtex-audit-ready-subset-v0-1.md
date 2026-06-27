# KORA First Paper Final BibTeX Audit — Ready Subset v0.1

## Purpose

This audit checks the preliminary BibTeX entries and normalized keys for the ready subset before any broader bibliography work.

It is a bibliography-quality and traceability audit. It does not add blocked-record BibTeX, does not modify manuscript v0.3, and does not make the paper submission-ready.

## Scope

This audit covers ready records only:

- `[R01]`
- `[R06]`
- `[R08]`
- `[R11]`
- `[R14]`
- `[R21]`
- `[R24]`

Blocked records remain excluded. No manuscript changes are made in this pass. This audit does not claim that the paper is submission-ready.

## Audit Rules

- Do not add BibTeX for blocked records.
- Do not invent metadata.
- Do not add fake DOI values.
- Do not add fake venue fields.
- Do not infer missing fields.
- Preserve stable `[Rxx]` traceability.
- Keep BibTeX preliminary until final bibliography and claim audit are complete.

## Ready-Subset BibTeX Audit Table

| ID | Key | Entry type | Required fields present | Risk status | Action |
|---|---|---|---|---|---|
| `[R01]` | `kwon2023pagedattention` | `@inproceedings` | author, title, booktitle, year, DOI, URL | needs final venue check | keep preliminary; normalize later if venue requires |
| `[R06]` | `lewis2020rag` | `@inproceedings` | author, title, booktitle, year, DOI, URL | needs final venue check | keep preliminary; normalize later if venue requires |
| `[R08]` | `koster2012snakemake` | `@article` | author, title, journal, volume, number, pages, year, DOI, URL | low risk | keep preliminary; review before final submission |
| `[R11]` | `yao2023react` | `@inproceedings` | author, title, booktitle, year, DOI, URL | needs final venue check | keep preliminary; normalize later if venue requires |
| `[R14]` | `bang2023gptcache` | `@inproceedings` | author, title, booktitle, pages, publisher, year, DOI, URL | preliminary only | keep preliminary; review before final submission |
| `[R21]` | `jimenez2024swebench` | `@inproceedings` | author, title, booktitle, year, DOI, URL | needs final venue check | keep preliminary; normalize later if venue requires |
| `[R24]` | `ribeiro2020checklist` | `@inproceedings` | author, title, booktitle, pages, year, DOI, URL | needs final venue check | keep preliminary; review before final submission |

## Blocked Record Exclusion Check

Blocked records:

`[R02]`, `[R03]`, `[R04]`, `[R05]`, `[R07]`, `[R09]`, `[R10]`, `[R12]`, `[R13]`, `[R15]`, `[R16]`, `[R17]`, `[R18]`, `[R19]`, `[R20]`, `[R22]`, `[R23]`

No BibTeX entries should exist for these records in preliminary BibTeX v0.1. These records remain deferred until metadata and style gaps are resolved.

## Key Consistency Check

All ready-subset keys are stable and collision-free within the current preliminary BibTeX document.

The keys should remain stable until venue conversion. Any later key changes must be recorded in a key-change log so `[Rxx]` traceability remains clear.

## Claim-Safety Note

This final ready-subset BibTeX audit does not change claim support.

External references remain related-work, methodology, reproducibility, benchmark-construction, or background support only. KORA's 80/100 result remains supported by KORA deterministic-heavy benchmark docs and evidence. BibTeX status does not support production cost reduction proof, real API-cost reduction proof, energy reduction evidence, production benchmark proof, or broad workload superiority.

## Next Step

Next steps:

1. Resolve metadata and style gaps for blocked records.
2. Expand BibTeX only after blocked records are resolved.
3. Run final bibliography and claim audit before any submission-ready statement.
4. Create manuscript v0.4 only after bibliography and claim audit are stable.
