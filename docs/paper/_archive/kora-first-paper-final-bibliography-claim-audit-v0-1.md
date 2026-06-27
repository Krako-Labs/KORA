# KORA First Paper Final Bibliography and Claim Audit v0.1

Audit date: 2026-05-13

## Purpose

This audit reviews bibliography readiness and claim safety after the expanded preliminary BibTeX candidate subset was prepared. It does not modify manuscript v0.3, does not complete full BibTeX, and does not make the paper submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-3.md`
- `docs/paper/kora-first-paper-citation-audit-v0-1.md`
- `docs/paper/kora-first-paper-reference-metadata-audit-v0-1.md`
- `docs/paper/kora-first-paper-normalized-bibliography-v0-1.md`
- `docs/paper/kora-first-paper-metadata-gap-resolution-v0-1.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-final-bibtex-audit-ready-subset-v0-1.md`
- `docs/paper/kora-first-paper-expanded-bibtex-candidate-audit-v0-1.md`
- `docs/paper/kora-first-paper-final-blocked-metadata-review-v0-1.md`
- `docs/paper/kora-first-paper-bibliography-notes.md`
- `docs/paper/kora-first-paper-reference-plan.md`
- `docs/paper/kora-first-paper-missing-evidence-checklist.md`
- `docs/paper/kora-first-paper-submission-readiness.md`
- `docs/paper/kora-first-paper-citation-style-decision.md`
- `docs/paper/kora-first-paper-docs-repo-reference-style-resolution-v0-1.md`
- `docs/paper/kora-first-paper-artifact-guidance-reference-style-resolution-v0-1.md`
- `docs/paper/kora-first-paper-paper-preprint-reference-style-resolution-v0-1.md`
- `docs/paper/kora-first-paper-claim-boundary.md`

## Bibliography Readiness Summary

| Bucket | Records | Status |
|---|---|---|
| Ready subset | `[R01]`, `[R06]`, `[R08]`, `[R11]`, `[R14]`, `[R21]`, `[R24]` | Included in preliminary BibTeX; ready-subset audit exists; still preliminary before final venue formatting. |
| Expanded candidate subset | `[R03]`, `[R04]`, `[R05]`, `[R07]`, `[R09]`, `[R10]`, `[R12]`, `[R13]`, `[R16]` | Included in expanded preliminary BibTeX after final field check; still preliminary before final venue formatting. |
| Deferred records | `[R17]`, `[R18]` | Excluded from preliminary BibTeX until target venue selection confirms whether venue-specific guidance belongs in the final bibliography. |
| Still-not-eligible records | `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, `[R23]` | Excluded from preliminary BibTeX until author-list, split, or venue/status decisions are resolved. |

## Preliminary BibTeX Inclusion

Preliminary BibTeX currently includes:

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
- `[R14]`
- `[R16]`
- `[R21]`
- `[R24]`

Preliminary BibTeX excludes:

- `[R02]`
- `[R15]`
- `[R17]`
- `[R18]`
- `[R19]`
- `[R20]`
- `[R22]`
- `[R23]`

No deferred or still-not-eligible record was found in preliminary BibTeX. No missing metadata was silently filled in this audit.

## Remaining Metadata Blockers

- `[R02]`: author-list handling and venue/status normalization remain unresolved.
- `[R15]`: split-or-keep treatment for the combined docs/repo citation remains unresolved.
- `[R17]`: target-venue-specific artifact guidance remains deferred.
- `[R18]`: target-venue-specific artifact guidance remains deferred.
- `[R19]`: author-list handling or approved `et al.` style remains unresolved.
- `[R20]`: author-list handling or approved `et al.` style remains unresolved.
- `[R22]`: author-list handling or approved `et al.` style remains unresolved.
- `[R23]`: author-list handling or approved `et al.` style remains unresolved.
- `[R19]` through `[R24]`: benchmark-methodology manuscript integration remains a future decision; these records do not provide KORA production benchmark evidence.

## Claim and Evidence Alignment

The current manuscript v0.3 remains aligned with the approved safe public claim:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

The manuscript constrains the 80/100 result to the documented deterministic-heavy benchmark and explicitly separates that evidence from production, provider, cost, energy, and broad generalization claims. The customer-support local/no-network validation remains framed as a synthetic workload that measures avoided model-call events, not as production evidence.

References remain related-work, methodology, reproducibility, artifact-practice, or background support only. External references do not support the KORA 80/100 result; that result remains supported by KORA deterministic-heavy benchmark docs and evidence.

## Explicit Non-Claims

This audit does not support:

- production cost reduction proof
- real API-cost reduction proof
- production benchmark proof
- full runtime-integrated real-provider benchmark evidence
- broad workload superiority proof
- energy reduction evidence
- formal government validation
- signed partner validation
- guaranteed adoption or funding
- formal artifact approval
- paper submission readiness

## Submission-Readiness Blockers

- Full BibTeX remains incomplete because `[R02]`, `[R15]`, `[R17]`, `[R18]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` remain excluded.
- Final venue-specific bibliography formatting is not complete.
- Final citation style conversion from stable `[Rxx]` labels remains deferred.
- Benchmark-methodology references `[R19]` through `[R24]` are not fully integrated into manuscript methodology.
- Final figures, tables, clean reproduction transcript, and final claim review remain pending.
- Manuscript v0.4 should wait until bibliography and claim boundaries are stable.

## Audit Result

Bibliography readiness has advanced, but full BibTeX is still incomplete. The manuscript claim boundary remains safe and aligned with available evidence. The paper remains not submission-ready.

## Next Recommended Step

Resolve the remaining deferred and still-not-eligible bibliography records, then perform final BibTeX consistency and venue-format checks before any manuscript v0.4 or submission-preparation pass.
