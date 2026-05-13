# KORA First Paper Expanded BibTeX Candidate Audit v0.1

## Purpose

This audit checks expanded preliminary BibTeX candidates before the final bibliography and claim audit.

It prepares only the candidate records that pass final field check. It does not modify manuscript v0.3, does not complete full BibTeX, and does not make the paper submission-ready.

## Scope

Candidate set checked in this pass:

- `[R03]`
- `[R04]`
- `[R05]`
- `[R07]`
- `[R09]`
- `[R10]`
- `[R12]`
- `[R13]`
- `[R16]`

Ready subset already handled separately:

- `[R01]`
- `[R06]`
- `[R08]`
- `[R11]`
- `[R14]`
- `[R21]`
- `[R24]`

Deferred and still-not-eligible records are excluded. This pass makes no manuscript changes and makes no submission-ready claim.

## Candidate Field Check Table

| ID | Candidate status | Included in expanded BibTeX | Reason | Remaining risk |
|---|---|---|---|---|
| `[R03]` | pass | yes | Official docs source type, organization owner, title, URL, and access-date treatment are recorded in the tracker and normalized bibliography. | Final venue style may change access-date or entry-type formatting. |
| `[R04]` | pass | yes | Official docs source type, organization owner, title, URL, and access-date treatment are recorded in the tracker and normalized bibliography. | Final venue style may change access-date or entry-type formatting. |
| `[R05]` | pass | yes | Paper/preprint source type, full author list, title, arXiv URL, and year are recorded. | Venue/status conversion remains preliminary; keep as arXiv-style entry for now. |
| `[R07]` | pass | yes | Official docs source type, organization owner, title, docs version, URL, and access-date treatment are recorded. | Final venue style may change access-date, version, or entry-type formatting. |
| `[R09]` | pass | yes | Official repository source type, organization owner, title, URL, and access-date treatment are recorded. | Final venue style may change repository entry type or access-date formatting. |
| `[R10]` | pass | yes | Official policy/artifact guidance source type, organization owner, title, version/year, and URL are recorded. | Final venue style may change policy-page entry type or access-date formatting. |
| `[R12]` | pass | yes | Paper/preprint source type, full author list, title, arXiv URL, DOI, and year are recorded. | Venue/status conversion remains preliminary; keep as arXiv-style entry for now. |
| `[R13]` | pass | yes | Paper/preprint source type, full author list, title, arXiv URL, DOI, year, and revision note are recorded. | Venue/status conversion remains preliminary; keep as arXiv-style entry for now. |
| `[R16]` | pass | yes | Report/preprint source type, full author list, title, arXiv URL, DOI, and year are recorded. | Report/venue status conversion remains preliminary; does not imply formal artifact approval. |

No candidate in this subset failed the final field check.

## Excluded Records

Deferred records:

- `[R17]`
- `[R18]`

Still not eligible:

- `[R02]`
- `[R15]`
- `[R19]`
- `[R20]`
- `[R22]`
- `[R23]`

No candidate record from `[R03]`, `[R04]`, `[R05]`, `[R07]`, `[R09]`, `[R10]`, `[R12]`, `[R13]`, and `[R16]` failed the final field check.

## BibTeX Safety Note

No BibTeX is generated for records that remain deferred or not eligible.

This pass does not invent metadata. It uses only existing repository tracker, normalized bibliography, and style-resolution records. The expanded BibTeX remains preliminary and must be reviewed before submission.

## Claim-Safety Note

BibTeX status does not change claim support.

References remain related-work, methodology, reproducibility, artifact-practice, or background only. KORA's 80/100 result remains supported by KORA deterministic-heavy benchmark docs and evidence.

Expanded BibTeX status does not support production cost reduction proof, real API-cost reduction proof, energy reduction evidence, production benchmark proof, full runtime-integrated real-provider benchmark evidence, broad workload superiority, formal government validation, guaranteed adoption, guaranteed funding, or formal artifact approval.

## Next Step

Recommended next steps:

1. Run final bibliography and claim audit.
2. Run a final BibTeX consistency check.
3. Create manuscript v0.4 only after bibliography and claim audit are stable.
