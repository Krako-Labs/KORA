# KORA First Paper Submission Readiness Gate v0.1

Gate date: 2026-05-13

## Purpose

This gate records what remains before the KORA first paper can be treated as submission-ready. It is a blocker register and sequencing guide. It does not modify manuscript v0.3, does not complete the bibliography, and does not mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-3.md`
- `docs/paper/kora-first-paper-citation-audit-v0-1.md`
- `docs/paper/kora-first-paper-reference-metadata-audit-v0-1.md`
- `docs/paper/kora-first-paper-normalized-bibliography-v0-1.md`
- `docs/paper/kora-first-paper-metadata-gap-resolution-v0-1.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-final-bibtex-audit-ready-subset-v0-1.md`
- `docs/paper/kora-first-paper-expanded-bibtex-candidate-audit-v0-1.md`
- `docs/paper/kora-first-paper-final-bibliography-claim-audit-v0-1.md`
- `docs/paper/kora-first-paper-final-blocked-metadata-review-v0-1.md`
- `docs/paper/kora-first-paper-bibliography-notes.md`
- `docs/paper/kora-first-paper-reference-plan.md`
- `docs/paper/kora-first-paper-missing-evidence-checklist.md`
- `docs/paper/kora-first-paper-submission-readiness.md`
- `docs/paper/kora-first-paper-citation-style-decision.md`
- `docs/paper/kora-first-paper-docs-repo-reference-style-resolution-v0-1.md`
- `docs/paper/kora-first-paper-artifact-guidance-reference-style-resolution-v0-1.md`
- `docs/paper/kora-first-paper-paper-preprint-reference-style-resolution-v0-1.md`

## Current State

- Current manuscript version: manuscript v0.3.
- Current bibliography state: preliminary BibTeX v0.1 has 16 entries.
- Ready records in preliminary BibTeX: `[R01]`, `[R06]`, `[R08]`, `[R11]`, `[R14]`, `[R21]`, `[R24]`.
- Expanded candidate records in preliminary BibTeX: `[R03]`, `[R04]`, `[R05]`, `[R07]`, `[R09]`, `[R10]`, `[R12]`, `[R13]`, `[R16]`.
- Deferred records excluded from preliminary BibTeX: `[R17]`, `[R18]`.
- Still-not-eligible records excluded from preliminary BibTeX: `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, `[R23]`.
- Current claim/evidence state: the bounded 80% deterministic-heavy benchmark claim remains the only approved public quantitative claim.

## Required Blockers Before Submission

| Blocker ID | Category | Required blocker | Required resolution |
|---|---|---|---|
| BIB-1 | Bibliography | Full BibTeX remains incomplete. | Resolve deferred and still-not-eligible records or document an intentional final exclusion policy. |
| BIB-2 | Bibliography | Deferred records `[R17]` and `[R18]` remain target-venue dependent. | Select target venue or decide these artifact-guidance references stay out of final bibliography. |
| BIB-3 | Bibliography | Still-not-eligible records `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` have unresolved author-list, split, or venue/status handling. | Complete metadata/style decisions before final BibTeX. |
| BIB-4 | Bibliography | Manuscript references and preliminary BibTeX are not yet synchronized as final bibliography entries. | Run final manuscript-to-BibTeX consistency check after full BibTeX decisions. |
| CLAIM-1 | Claim/evidence | Final claim-to-evidence pass against the manuscript body is not complete after bibliography closure. | Re-check every quantitative and evidence-bearing statement against public evidence. |
| CLAIM-2 | Claim/evidence | Benchmark-methodology references `[R19]` through `[R24]` are tracker/audit-only or partially integrated. | Decide whether methodology integration is needed, and keep them out of KORA production benchmark evidence. |
| FORMAT-1 | Formatting/export | Final venue format is not selected. | Select target format or produce an arXiv/workshop technical-report package. |
| FORMAT-2 | Formatting/export | Final export package is not prepared. | Generate final manuscript export, bibliography, figures, and tables for the target package. |
| ART-1 | Artifact/reproducibility | Clean reproduction transcript is not captured. | Run and record clean checkout validation commands for the submission package. |
| ART-2 | Artifact/reproducibility | Submission-context artifact package has not been reviewed. | Review public artifact instructions, command reproducibility, and no-network labels. |
| REVIEW-1 | Human review | Final human review is not complete. | Perform final paper readthrough for claims, references, figures, tables, and submission instructions. |

## Optional Before Submission

These items are useful but can remain deferred if the first submission scope stays narrow:

- Expanded workload beyond the deterministic-heavy benchmark and synthetic customer-support validation.
- Latency p50/p95 reporting.
- Additional direct deterministic-heavy synthetic workload construction references.
- Additional semantic caching references if the manuscript expands caching discussion.
- OpenAI or Claude API-cost study.
- Production traffic study.
- Energy measurement study.
- KORA Studio implementation discussion.
- Real customer-data validation.

## Blocker Categories

### Bibliography Blockers

- Full BibTeX remains incomplete.
- Deferred and still-not-eligible records remain unresolved or intentionally excluded.
- Final venue-specific bibliography formatting is not complete.
- Final citation style conversion from stable `[Rxx]` labels remains deferred.
- Final manuscript and bibliography synchronization is not complete.

### Claim and Evidence Blockers

- Final claim-to-evidence pass must be repeated after bibliography and manuscript updates are stable.
- The approved safe claim remains: KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.
- The customer-support local/no-network validation remains synthetic validation of avoided model-call event measurement, not production evidence.
- External references remain related-work, methodology, reproducibility, artifact-practice, or background support only.

### Formatting and Export Blockers

- Target venue or report format is not selected.
- Final bibliography style and citation rendering are not complete.
- Final figures and tables are not locked.
- Final manuscript export and package assembly are not complete.

### Artifact and Reproducibility Blockers

- Clean command transcript is pending.
- Clean checkout reproduction instructions are not yet package-reviewed.
- Raw benchmark artifacts must not be uploaded.
- Artifact guidance references do not imply formal artifact approval.

### Repository and Documentation Blockers

- Public paper docs must remain free of private paths, internal workflow references, secrets, raw provider responses, proprietary datasets, and private campaign material.
- Public docs must preserve explicit non-claim boundaries.
- Any final submission package should be reviewed against repository public-safety rules.

## Explicit Non-Claims

This gate does not support:

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

## Recommended Next Task Sequence

1. Resolve or intentionally exclude `[R17]` and `[R18]` after target venue direction is clear.
2. Resolve `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` metadata/style blockers.
3. Complete final BibTeX consistency and venue-format checks.
4. Synchronize manuscript references and final bibliography.
5. Run final claim-to-evidence audit against manuscript v0.3 or a later manuscript draft.
6. Prepare figures, tables, and final export package.
7. Capture clean reproduction transcript and artifact package review.
8. Complete final human review before any submission or preprint action.

## Gate Conclusion

The paper is not submission-ready. The next required focus is resolving remaining bibliography blockers before final manuscript synchronization, final claim review, and submission-package preparation.
