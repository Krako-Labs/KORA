# KORA First Paper Docs/Repo Reference Style Resolution v0.1

## Purpose

This document resolves or classifies style handling for official documentation and repository references before any BibTeX expansion.

It is a bibliography-planning document. It does not generate BibTeX, does not modify manuscript v0.3, and does not make the paper submission-ready.

## Scope

This pass covers only official documentation and repository records:

- `[R03]` ONNX Runtime docs
- `[R04]` LangGraph Graph API docs
- `[R07]` Apache Airflow DAG docs
- `[R09]` llama.cpp
- `[R15]` Ollama docs and official repo

This pass makes no manuscript changes. It does not make a full-paper submission-ready claim. It does not add BibTeX by default.

## Style Rules for Official Docs and Repositories

- Use project or organization owner when individual authors are not appropriate.
- Include access-date treatment in a later BibTeX or style pass.
- Keep source URLs stable.
- Distinguish official documentation from official repositories.
- Do not infer individual authors.
- Do not infer publication years if they are not available.
- Omit uncertain fields rather than inventing metadata.
- Keep venue-specific conversion deferred.

## Docs/Repo Resolution Table

| ID | Reference | Source type | Proposed owner | Date/access-date handling | URL treatment | BibTeX status | Remaining action |
|---|---|---|---|---|---|---|---|
| `[R03]` | ONNX Runtime docs | official docs | ONNX Runtime project / Microsoft | date unavailable; access date already recorded as 2026-05-11 | keep official docs URL | ready for docs-style BibTeX later; no entry in this pass | choose final docs entry type and access-date field style |
| `[R04]` | LangGraph Graph API docs | official docs | LangChain | date unavailable; access date already recorded as 2026-05-11 | keep official docs URL | ready for docs-style BibTeX later; no entry in this pass | choose final docs entry type and access-date field style |
| `[R07]` | Apache Airflow DAG docs | official docs | Apache Software Foundation / Apache Airflow project | date unavailable; docs version and access date already recorded as 2026-05-11 | keep official docs URL | ready for docs-style BibTeX later; no entry in this pass | choose final docs entry type, version placement, and access-date field style |
| `[R09]` | llama.cpp | official repo | ggml-org | date unavailable; access date already recorded as 2026-05-11 | keep official repository URL | ready for repository-style BibTeX later; no entry in this pass | choose final repository entry type and access-date field style |
| `[R15]` | Ollama docs and official repo | official docs / official repo | Ollama | date unavailable; access date already recorded as 2026-05-11 | keep recorded docs URL and repo URL | keep blocked until split-or-keep decision is finalized for BibTeX | decide whether final BibTeX uses combined entry or split docs/repo entries |

## Split-or-Keep Decision

For `[R15]`, keep the combined docs/repo reference for current tracker and audit continuity.

Before final BibTeX, reconsider whether `[R15]` should split into separate documentation and repository records if the target venue or report style treats official documentation and repositories differently. Until that decision is made, `[R15]` remains blocked before BibTeX.

## Updated Blocker Status

Ready for docs-style BibTeX later, after final access-date and entry-type style are chosen:

- `[R03]`
- `[R04]`
- `[R07]`

Ready for repository-style BibTeX later, after final access-date and entry-type style are chosen:

- `[R09]`

Needs split decision:

- `[R15]`

Keep blocked until venue/style decision:

- `[R03]`
- `[R04]`
- `[R07]`
- `[R09]`
- `[R15]`

## Claim-Safety Note

Docs/repo references are implementation, runtime, orchestration, or future-work context only.

They do not support KORA production claims. They do not support production cost reduction proof, real API-cost reduction proof, energy reduction evidence, or production benchmark proof. KORA's 80/100 result remains supported by KORA deterministic-heavy benchmark docs and evidence.

## Next Step

Next steps:

1. Update normalized bibliography docs with docs/repo style classifications.
2. Later prepare docs/repo BibTeX only after access-date and owner treatment are stable.
3. Continue blocked metadata/style resolution for artifact guidance and paper/preprint records.
