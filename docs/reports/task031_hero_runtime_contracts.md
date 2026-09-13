# Task031 — Hero Runtime Contracts and Replayable Event Core

Status: needs-cto-review  
Risk: medium — new public runtime contracts, no execution integration  
Base: `7c7a6b4c57eab15816560cb405fa99f2599dc465`

- branch: `feat/task031-hero-runtime-contract`
- PR: https://github.com/Krako-Labs/KORA/pull/300
- risk level: medium
- final status classification: `needs-cto-review`

## Outcome

Task031 adds a fail-closed foundation for a future dynamic workload-control viewer:

- byte-based hardware and model-resource profile contracts;
- runtime capability and workload requirement contracts;
- auditable execution-plan decisions;
- deterministic `yes / no / unknown` feasibility evaluation;
- immutable ordered runtime events;
- a replay reducer for task, merge, verification and completion state;
- an append-only in-memory event log with reconnect cursors and SSE serialization.

The work does not connect a model, provider, GPU, remote server, model download, or production telemetry.

## Changed files

- `kora/hero_contracts.py`
- `kora/hero_feasibility.py`
- `kora/hero_replay.py`
- `kora/hero_event_log.py`
- `tests/test_hero_contracts.py`
- `tests/test_hero_feasibility.py`
- `tests/test_hero_replay.py`
- `tests/test_hero_event_log.py`
- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- this report

## Contract behavior

- undeclared fields fail validation;
- verified model profiles require a tensor-inventory reference;
- unknown memory overhead yields `unknown` and is not selected;
- infeasible and undetected runtimes are rejected;
- planning order is deterministic and retains rejection reasons;
- event sequences cannot contain gaps, duplicate IDs, or mixed run IDs;
- task dependencies and state transitions are checked during replay;
- a run cannot complete before merge and verification pass;
- unknown future event types are retained for forward compatibility;
- failed event batches do not partially mutate the event log;
- reconnect consumers can request events after a known sequence.

## Validation

Executed locally without model/provider/GPU/server work:

- `git diff --check`: passed.
- `python -m compileall -q kora`: passed.
- focused Hero tests: 19 passed.
- full suite with development and research test dependencies: 817 passed.

The first default-Python attempt could not import pytest. The test environment was recreated with the repository dependencies. The first full-suite attempt omitted the optional PDF test dependency and produced nine environment failures; rerun with the declared research dependency passed 813 tests at that stage. Four event-log tests were then added. One assertion expected the wrong missing sequence number and was corrected; final focused and full suites passed.

## Safety and claim boundary

Confirmed:

- no provider call;
- no model inference or model download;
- no H100/GPU/CUDA/server/remote execution;
- no semantic judging or human grading;
- no production validation;
- no performance, cost, quality, hardware-superiority, or larger-than-memory result claim;
- no repository setting, release, tag, publication, issue, project-board, collaborator, archive, delete, rename, or major file movement;
- no Krako Reach integration;
- fixture evidence remains labeled `fixture`;
- feasibility is planning evidence only, not execution proof.

Forbidden-action audit: no provider calls, model inference, model download, H100/GPU/CUDA/server/remote execution, semantic judging, human grading, production validation, release, publication, repository setting change, file movement, or public claim expansion was performed.

## Review focus

Reviewer attention should concentrate on:

1. whether the memory-domain contract is sufficient before physical profiling;
2. whether forward-compatible unknown events should remain retained but ignored;
3. whether the replay transition rules match the intended UI lifecycle;
4. whether the feasibility engine should remain separate from runtime adapters.

No merge is authorized by this report.
