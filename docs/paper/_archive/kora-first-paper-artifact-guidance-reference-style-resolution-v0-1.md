# KORA First Paper Artifact Guidance Reference Style Resolution v0.1

## Purpose

This document resolves or classifies style handling for artifact review and artifact evaluation guidance references before any BibTeX expansion.

It is a bibliography-planning document. It does not generate BibTeX, does not modify manuscript v0.3, and does not make the paper submission-ready.

## Scope

This pass covers only artifact guidance and evaluation policy records:

- `[R10]` ACM Artifact Review and Badging
- `[R17]` USENIX NSDI artifact guidance
- `[R18]` MLSys artifact evaluation guidance

This pass makes no manuscript changes. It does not make a full-paper submission-ready claim. It does not add BibTeX by default.

## Style Rules for Artifact Guidance References

- Treat artifact guidance as policy or guidance references, not as paper or evidence references.
- Use organization or conference owner when individual authors are not appropriate.
- Include access-date treatment in a later BibTeX or style pass.
- Keep source URLs stable.
- Do not infer individual authors.
- Do not infer publication years if they are not available.
- Do not claim formal artifact approval from citing guidance pages.
- Keep target-venue conversion deferred.

## Artifact Guidance Resolution Table

| ID | Reference | Source type | Proposed owner | Date/access-date handling | Venue/target handling | BibTeX status | Remaining action |
|---|---|---|---|---|---|---|---|
| `[R10]` | ACM Artifact Review and Badging | official policy / artifact guidance | Association for Computing Machinery | version/year recorded as Version 1.1, 2020; access-date treatment still needed in final style pass | general ACM artifact policy context, not a target-venue approval statement | ready for artifact-guidance BibTeX later; no entry in this pass | choose policy/guidance entry type and access-date field style |
| `[R17]` | USENIX NSDI artifact guidance | official venue guidance | USENIX Association | conference year range recorded as 2025-2026; access-date treatment still needed in final style pass | venue-specific; defer unless the target venue or artifact package uses USENIX/NSDI-style expectations | deferred before BibTeX; no entry in this pass | choose whether this venue-specific guidance belongs in the final bibliography after target venue selection |
| `[R18]` | MLSys artifact evaluation guidance | official venue guidance | MLSys | conference year recorded as 2023; access-date treatment still needed in final style pass | venue-specific; defer unless the target venue or artifact package uses MLSys-style expectations | deferred before BibTeX; no entry in this pass | choose whether this venue-specific guidance belongs in the final bibliography after target venue selection |

## Target-Venue Deferral

`[R17]` and `[R18]` should remain deferred until the target venue is selected.

`[R10]` can remain a general artifact guidance reference for artifact-practice framing, but its final citation style still needs policy-page entry type, URL, and access-date treatment.

These references should not imply that KORA has passed artifact evaluation, received artifact approval, or completed a target-venue artifact review.

## Updated Blocker Status

Ready for artifact-guidance BibTeX later after final access-date and policy-page style are chosen:

- `[R10]`

Needs access-date/style decision:

- `[R10]`
- `[R17]`
- `[R18]`

Defer until target venue chosen:

- `[R17]`
- `[R18]`

Keep blocked until venue/style decision:

- `[R10]`
- `[R17]`
- `[R18]`

## Claim-Safety Note

Artifact guidance references are guidance and artifact-practice context only.

They do not support formal artifact approval. They do not support production cost reduction proof, real API-cost reduction proof, energy reduction evidence, or production benchmark proof. KORA's 80/100 result remains supported by KORA deterministic-heavy benchmark docs and evidence.

## Next Step

Next steps:

1. Update normalized bibliography docs with artifact guidance classifications.
2. Continue paper/preprint metadata-style resolution for remaining blocked records.
3. Later prepare artifact guidance BibTeX only after venue, access-date, and style treatment are stable.
