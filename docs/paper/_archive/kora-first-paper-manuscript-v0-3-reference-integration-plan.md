# KORA First Paper Manuscript v0.3 Reference Integration Plan

## Purpose

This document plans the safe integration of [R11] through [R18] into a future manuscript v0.3. It does not create manuscript v0.3, does not add BibTeX, and does not make the paper submission-ready.

## Current State

- Manuscript v0.2 currently integrates [R01] through [R10].
- References [R11] through [R18] are verified but tracker/audit-only.
- The paper remains not submission-ready.
- BibTeX and final citation style remain pending.
- Final bibliography normalization and metadata audit remain pending.

## Integration Principles

- Integrate only references that strengthen required related-work context.
- Avoid citation bloat.
- Avoid using references as proof of KORA superiority.
- Avoid using external references as production, API-cost, or energy evidence.
- Keep KORA's 80/100 result mapped to KORA deterministic-heavy benchmark evidence.
- Keep manuscript v0.3 complementary in tone.
- Defer references that are useful for bibliography or artifact planning but not necessary in manuscript text.

## Reference-by-Reference Integration Decision

| ID | Reference | Current status | Proposed manuscript section | Decision | Rationale | Claim boundary |
|---|---|---|---|---|---|---|
| [R11] | ReAct | verified, tracker/audit-only | Background and Related Work / Agent/tool routing and programmatic AI workflows | integrate in v0.3 | Strengthens discussion of reasoning/action and agent tool-use context. | Use as background only; do not claim KORA outperforms ReAct or agent systems. |
| [R12] | Toolformer | verified, tracker/audit-only | Background and Related Work / Agent/tool routing and programmatic AI workflows | integrate in v0.3 | Helps distinguish model-centered tool-use training from KORA's deterministic-first execution control. | Do not imply KORA uses Toolformer-style training or outperforms tool-use systems. |
| [R13] | PAL / program-aided language models | verified, tracker/audit-only | Background and Related Work / Agent/tool routing and programmatic AI workflows | integrate in v0.3 | Strengthens programmatic AI workflow context near DSPy and KORA's deterministic routes. | Use as program-aided workflow context only; not as KORA model-call avoidance evidence. |
| [R14] | GPTCache | verified, tracker/audit-only | Background and Related Work / Retrieval-augmented generation or caching contrast | optional if section expands | Useful if v0.3 adds explicit semantic-cache contrast, but not required if the manuscript keeps caching brief. | Do not use to support KORA production cost, real API-cost, or latency claims. |
| [R15] | Ollama docs and official repo | verified, tracker/audit-only | Background and Related Work / Local model and runtime systems | optional if section expands | Useful if v0.3 expands local runtime future-work context. | Do not imply current KORA paper evidence includes Ollama integration. |
| [R16] | NeurIPS reproducibility report | verified, tracker/audit-only | Reproducibility and Artifact Notes | optional if section expands | Useful for reproducibility framing and checklist discipline. | Does not make KORA formally reproducible by venue standards or submission-ready. |
| [R17] | USENIX NSDI artifact guidance | verified, tracker/audit-only | Reproducibility and Artifact Notes / future artifact package planning | defer until target venue | Best used if a USENIX-style artifact strategy becomes relevant. | Do not imply KORA has artifact approval or formal artifact evaluation. |
| [R18] | MLSys artifact evaluation guidance | verified, tracker/audit-only | Reproducibility and Artifact Notes / future artifact package planning | defer until target venue | Best used if an MLSys-style artifact strategy becomes relevant. | Do not imply KORA has artifact approval or formal artifact evaluation. |

## Proposed v0.3 Manuscript Changes

Background and Related Work:

- Add agent/tool-use subsection details for [R11] and [R12].
- Add programmatic AI workflow context for [R13].
- Optionally mention semantic caching [R14] only if caching becomes more central.
- Optionally mention local runtime [R15] only if the local runtime section needs more support.

Reproducibility and Artifact Notes:

- Optionally mention [R16] if the reproducibility section expands beyond the current ACM artifact-practice reference.
- Defer [R17] and [R18] until venue or artifact package planning.

Limitations:

- Keep non-claims unchanged.
- Preserve the statement that current evidence does not prove production behavior, real provider behavior, API-cost reduction, energy reduction, or broad workload superiority.

References section:

- Add only the references actually integrated into manuscript text.
- Keep all added references clearly preliminary until final citation style and bibliography normalization are complete.
- Do not add BibTeX in the manuscript.

## References to Keep Tracker-Only for Now

- [R14] GPTCache: keep tracker-only unless semantic caching receives more explicit treatment in v0.3.
- [R15] Ollama: keep tracker-only unless the local runtime section expands beyond future-work context.
- [R16] NeurIPS reproducibility report: keep tracker-only unless reproducibility notes expand.
- [R17] USENIX NSDI artifact guidance: defer until target venue or artifact package planning.
- [R18] MLSys artifact evaluation guidance: defer until target venue or artifact package planning.

## Claim-Safety Checklist for v0.3

- No "KORA outperforms X" claim.
- No production cost reduction proof.
- No real API-cost reduction proof.
- No energy reduction evidence.
- No broad workload superiority.
- No formal artifact approval.
- No submission-ready implication.
- No use of external references to prove KORA's 80/100 result.
- Keep the 80/100 result tied to KORA's deterministic-heavy benchmark evidence.

## Next Step

- Task 318C or later: create manuscript v0.3 with selected [R11] through [R18] integration.
- Alternative: verify synthetic workload / benchmark-construction references before manuscript v0.3 if the evaluation-methodology section should be strengthened first.
