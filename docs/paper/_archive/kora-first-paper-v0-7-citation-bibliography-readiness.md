# KORA First Paper v0.7 Citation and Bibliography Readiness Review

Review date: 2026-05-18

## Purpose

This note reviews citation and bibliography readiness for manuscript v0.7 before any final figure rebuild, Word export, PDF export, arXiv source-package work, or submission packaging.

It does not add references, does not generate BibTeX, does not rebuild figures, and does not mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-7.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-bibliography-sync-v0-1.md`
- `docs/paper/kora-first-paper-final-bibliography-claim-audit-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-bibliography-scope-v0-1.md`
- `docs/paper/kora-first-paper-final-blocked-metadata-review-v0-1.md`
- `docs/paper/kora-first-paper-citation-audit-v0-1.md`
- `docs/paper/kora-first-paper-related-work-map.md`
- `docs/paper/kora-first-paper-reference-tracker.md`

## Manuscript Version Reviewed

- Reviewed manuscript: `docs/paper/kora-first-paper-manuscript-v0-7.md`
- Current status: Word-first text draft, not submission-ready.
- Figure status: Figure 1 and Figure 2 remain text placeholders only.
- Export status: Word/PDF/arXiv/export work remains paused.

## Current Citation Marker Inventory

Manuscript v0.7 currently cites:

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

Reference entries present in the manuscript references section:

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

Current marker alignment:

- No manuscript citation marker is missing from the references section.
- No manuscript references-section entry is unused by the manuscript body.
- No deferred or still-not-eligible record is currently cited in manuscript v0.7.
- No BibTeX citation keys are used directly in manuscript v0.7.

## Preliminary BibTeX Alignment

The current preliminary BibTeX document records 16 preliminary entries:

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

Manuscript v0.7 cites only records already present in preliminary BibTeX. The cited subset is `[R01]`, `[R03]`, `[R04]`, `[R05]`, `[R06]`, `[R07]`, `[R08]`, `[R09]`, `[R10]`, `[R11]`, `[R12]`, and `[R13]`.

Preliminary BibTeX records not cited by manuscript v0.7:

- `[R14]`
- `[R16]`
- `[R21]`
- `[R24]`

These unused records are not errors. They should remain optional until a later citation decision intentionally integrates them or excludes them from the final bibliography.

## Unresolved or Preliminary Citation Items

The following items remain unresolved:

- Stable `[Rxx]` labels are still a working manuscript style, not final venue or arXiv bibliography style.
- Full BibTeX remains incomplete.
- Final citation style conversion remains pending.
- Final manuscript-to-final-BibTeX synchronization remains pending.
- Final access-date and entry-type treatment remains pending for official docs, repositories, and policy/guidance sources.
- Final bibliography formatting remains pending for arXiv or any later venue package.
- A v0.7-specific final bibliography sync should be repeated after any further manuscript edits.

## Deferred and Still-Blocked Records

Deferred records remain excluded:

- `[R17]`
- `[R18]`

Still-not-eligible records remain excluded:

- `[R02]`
- `[R15]`
- `[R19]`
- `[R20]`
- `[R22]`
- `[R23]`

These records should not be cited in manuscript v0.7 unless a later task resolves their metadata/style blockers and records the reason for inclusion.

## Related-Work Citation Readiness

Current related-work coverage is adequate for a conservative first draft:

- LLM serving and inference systems: `[R01]`, `[R03]`
- Workflow and DAG orchestration: `[R07]`, `[R08]`
- Agent/tool routing and programmatic AI workflows: `[R04]`, `[R05]`, `[R11]`, `[R12]`, `[R13]`
- Retrieval-augmented generation: `[R06]`
- Local model and runtime systems: `[R09]`, `[R03]`
- Benchmarking and artifact evaluation: `[R10]`

Areas that may need stronger citation support later, if the manuscript expands:

- Semantic caching and cache-based cost/latency framing. `[R14]` exists in preliminary BibTeX, but it should not be integrated unless the manuscript explicitly adds a cache-related comparison and keeps cost claims bounded.
- Reproducibility program background. `[R16]` exists in preliminary BibTeX and could support broader reproducibility discussion, but it is not currently required by the v0.7 manuscript.
- Broader benchmark methodology. `[R19]` through `[R24]` remain tracker/audit-only or selectively preliminary; they should not be forced into the first package without a scoped methodology rewrite.
- Venue-specific artifact guidance. `[R17]` and `[R18]` remain deferred until venue or package decisions justify them.

## Claim-to-Citation Readiness

External references support background, contrast, terminology, and artifact-practice framing. They do not support KORA's empirical claims.

Claims already supported by KORA evidence docs and manuscript tables:

- In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.
- The deterministic-heavy benchmark reports 80 deterministic outputs checked and 0 mismatches.
- The customer-support triage workload is synthetic local/no-network validation only.
- Current evidence is limited to documented benchmark and local/no-network validation evidence.

Claims that must remain non-claims:

- production cost reduction proof
- real API-cost reduction proof
- production benchmark proof
- real provider benchmark proof
- broad workload superiority proof
- energy reduction evidence
- formal artifact approval
- government validation
- signed partner validation
- guaranteed adoption or funding

Citation readiness does not change the claim boundary. KORA's 80/100 result remains supported by KORA benchmark evidence, not by external related-work citations.

## Bibliography Entry Review

Current bibliography state:

- Manuscript v0.7 has a references section for all currently cited `[Rxx]` labels.
- Preliminary BibTeX has entries for all currently cited records.
- Full BibTeX remains incomplete.
- Preliminary BibTeX includes four records not currently cited by manuscript v0.7: `[R14]`, `[R16]`, `[R21]`, and `[R24]`.
- Deferred records `[R17]` and `[R18]` remain excluded.
- Still-not-eligible records `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` remain excluded.

Potential cleanup before export:

- Decide whether final bibliography should include only manuscript-cited records or retain unused preliminary records.
- Convert stable `[Rxx]` labels to final citation keys/style only after final bibliography scope is approved.
- Recheck docs/repo/policy entry types, access dates, and formatting.
- Recheck author lists, venue/status wording, DOI fields, and URLs for all final included records.
- Ensure final references do not include venue-specific artifact guidance unless the venue/package decision requires it.

No duplicate manuscript references-section entry was found for the current cited marker set. No unresolved citation marker was found in manuscript v0.7.

## Recommended Cleanup Actions Before Export

Before Word/PDF/arXiv/export work resumes:

- Repeat a manuscript-to-BibTeX sync against v0.7 or later.
- Freeze the final cited-record list.
- Decide whether unused preliminary records `[R14]`, `[R16]`, `[R21]`, and `[R24]` stay out of the first package bibliography.
- Keep `[R17]` and `[R18]` deferred unless a venue-specific artifact-guidance need is approved.
- Keep `[R19]` through `[R24]` out of methodology/background unless a later methodology pass intentionally integrates them.
- Resolve final style for official documentation, repositories, and policy pages.
- Re-run a final claim-to-evidence audit after bibliography formatting and before any submission package.

## Submission Packaging Blockers

The following blockers remain before submission packaging:

- Full BibTeX remains incomplete.
- Final bibliography scope is not frozen.
- Final citation style conversion is not complete.
- Final manuscript-to-final-BibTeX synchronization is pending.
- Final claim-to-evidence audit is pending after any later citation or manuscript edits.
- Figure 1 and Figure 2 remain placeholders.
- Word/PDF/arXiv/export work remains paused.

## Status

Manuscript v0.7 citation markers are internally aligned with the manuscript references section and are covered by current preliminary BibTeX. Bibliography readiness is improved enough for continued manuscript review, but final bibliography, final style conversion, and final export/package synchronization remain unresolved. The paper remains not submission-ready.
