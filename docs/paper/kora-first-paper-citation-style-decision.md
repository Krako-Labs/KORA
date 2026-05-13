# KORA First Paper Citation Style Decision

## Purpose

This document records the working citation style strategy before final bibliography normalization and BibTeX preparation for the KORA first paper.

It is a planning and traceability document. It does not generate BibTeX, finalize venue-specific formatting, or make the paper submission-ready.

## Current State

- Manuscript v0.3 is the current latest draft.
- References `[R01]` through `[R13]` are integrated into manuscript v0.3.
- References `[R14]` through `[R18]` are tracker/audit-only, optional, or deferred.
- References `[R19]` through `[R24]` are tracker/audit-only methodology/background references.
- BibTeX remains pending.
- Metadata audit v0.1 exists.
- Normalized bibliography v0.1 exists.
- Metadata gap resolution v0.1 exists at the planning/classification level.
- Preliminary BibTeX v0.1 exists for ready records only.
- Some metadata/style blockers remain before full BibTeX.
- The paper remains not submission-ready.

## Style Decision

Use numbered references with stable bracketed IDs in manuscript text, for example `[R01]`, `[R02]`, and `[R13]`.

Working strategy:

- Keep stable `[Rxx]` labels in manuscript text and paper planning docs.
- Normalize bibliography records in the reference tracker before generating BibTeX.
- Generate BibTeX only after the metadata audit, normalized bibliography, and metadata gap classification are complete.
- Convert to a venue-specific citation style later if a target venue or report format requires it.

Rationale:

- The current manuscript and citation audit already use `[Rxx]` IDs.
- Stable labels preserve traceability while references are still being audited.
- Tracker-first normalization reduces the risk of fake or inferred BibTeX.
- The strategy supports later conversion to ACM, IEEE, arXiv/report, or venue-specific formats without renumbering during active review.

## Citation Label Rules

- Keep `[Rxx]` labels stable once assigned.
- Do not renumber references casually.
- New verified references should append new IDs.
- Manuscript references must map to tracker entries.
- Tracker entries must record status and source URL or DOI.
- Tracker-only references should not appear in the manuscript References section unless cited in text.
- If a reference is rejected or superseded, keep its history clear in the tracker rather than reusing the ID for a different source.

## Bibliography Normalization Rules

For each tracker record, normalize:

- title
- authors or source organization
- year or date
- source URL or DOI
- source type
- verification status
- intended paper use
- claim boundary notes

Normalization rules:

- Mark missing metadata explicitly.
- Do not invent missing metadata.
- Prefer official source pages, DOI records, arXiv pages, ACL Anthology pages, ACM pages, USENIX pages, MLSys pages, or official documentation.
- Distinguish peer-reviewed papers from official docs, policy pages, and repositories.
- Keep official docs and repositories as organization-owned references when an individual author list is not appropriate.
- Preserve access-date needs for official docs and repositories until final style is chosen.

## BibTeX Rules

- Do not add BibTeX until metadata audit, normalized bibliography, and metadata gap classification are complete.
- Do not add fake BibTeX.
- Do not infer venues.
- Do not infer authors.
- Do not infer years.
- Do not infer DOI values.
- BibTeX can be generated in a later task only from normalized tracker records.
- Generated BibTeX must remain traceable to verified source URLs or DOI records.
- Preliminary BibTeX v0.1 covers only `[R01]`, `[R06]`, `[R08]`, `[R11]`, `[R14]`, `[R21]`, and `[R24]`.
- Ready-subset BibTeX keys are normalized using verified author/year/topic metadata.
- Final ready-subset BibTeX audit v0.1 checks only the ready records and does not add blocked-record BibTeX.
- Docs/repo style resolution v0.1 classifies `[R03]`, `[R04]`, `[R07]`, `[R09]`, and `[R15]` without adding BibTeX for those records.
- Artifact guidance style resolution v0.1 classifies `[R10]`, `[R17]`, and `[R18]` without adding BibTeX for those records.
- Paper/preprint style resolution v0.1 classifies `[R02]`, `[R05]`, `[R12]`, `[R13]`, `[R16]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` without adding BibTeX for those records.
- Final blocked metadata review v0.1 consolidates candidate, deferred, and still-blocked status without adding BibTeX for blocked records.
- Expanded preliminary BibTeX v0.1 follows the stable `[Rxx]` strategy for candidate records `[R03]`, `[R04]`, `[R05]`, `[R07]`, `[R09]`, `[R10]`, `[R12]`, `[R13]`, and `[R16]`.
- Venue-specific conversion remains deferred until the target venue or report format is chosen.
- Stable `[Rxx]` labels remain canonical during audit.
- Final venue-specific conversion remains deferred.

## Claim-Safety Rules

- References do not prove KORA is superior.
- Benchmark references do not prove production benchmark evidence.
- References do not prove production cost reduction.
- References do not prove real API-cost reduction.
- References do not prove energy reduction.
- References do not prove formal artifact approval.
- KORA's 80/100 result remains supported by KORA deterministic-heavy benchmark evidence only.
- External references may support background, related work, methodology, reproducibility framing, or future-work context only when their scope has been verified.

## Next Steps

1. Normalize preliminary BibTeX keys and fields for ready records after final style decisions.
2. Defer blocked records until author-list, venue/status, docs/repo style, or venue-guidance style gaps are resolved.
3. Run final bibliography and claim audit.
4. Create manuscript v0.4 only after bibliography and claim audit are stable.
