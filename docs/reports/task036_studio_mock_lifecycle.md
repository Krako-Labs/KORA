# Task036 — Hero Studio mock lifecycle replay

- branch: `feat/task036-studio-mock-lifecycle`
- base: `aab7958f5a55912276ef522e6e17992d5aa1c26d`
- risk level: medium
- final status classification: `needs-cto-review`

## Outcome

The [Runtime Adapter v2 contract](task035_runtime_adapter_v2.md) produced ordered
mock lifecycle events, but the [Hero Studio](task034_hero_studio_planning_and_task_graph.md)
could not inspect their state. This change adds an explicit mock review link from
the existing Hero page and a fixture-only review at `/hero/adapter`.

The review executes only the in-memory mock contract. It does not invoke the
existing executable MLX/llama.cpp adapters. Each scenario has one canonical event
log; browser play/step controls only pace its replay.

## Implemented behavior

- Six paths: success, cancellation, load failure, execute failure, finish failure,
  and cleanup failure followed by retry.
- A seventh blocked review explains unresolved hybrid placement without constructing
  a mock session or allocating even a mock resource.
- Full plan reconstruction and bound descriptor/model/configuration/script identity
  are reused from Task035.
- A narrow adapter projection validates known event identity, fixture evidence,
  exact payload, script fault, legal lifecycle order and canonical event sequence.
  Rejected events cannot partially mutate the committed projection.
- Future adapter extension events are retained in canonical history and ignored by
  the adapter-state projection. Task/run/verification promotion events are rejected.
- The canonical Hero reducer remains unchanged. Its unknown adapter event IDs are
  still retained; the new view is a separate adapter projection alongside it.
- Failure and cancellation reasons remain visible after cleanup; mock completion is
  distinct from service acceptance.
- Supplied token values say fixture; unavailable timing and memory remain null.
  No physical telemetry is inferred.
- The existing SSE, events fallback, replay pacing and keyboard controls are reused.
  Saved mock cursors bind the complete event-log digest, including the script.
- Task034 and mock review cursors have independent storage keys.
- Existing Hero task graphs, service-quality gates and reduced-motion behavior remain.

No task execution bridge, concurrent scheduling, live binding, persistent adapter
resume or hybrid placement solver is introduced. Browser reload restores a replay
cursor, not a running engine. The review page does not accept arbitrary external
model or event inputs.

## Validation

- New tests: **48 passed**.
- Focused Hero / Studio / adapter tests: **169 passed**.
- Full regression suite: **967 passed** in 31.24 seconds.
- New-file Ruff, changed Python compilation, JavaScript syntax and diff check: passed.
- New automated browser QC: **9 checks passed**.
- Existing Hero / Studio automated browser regression: **10 checks passed**.
- Every mock scenario frame compared with canonical server projection.
- Partial/completed reload, SSE failure recovery, keyboard stepping and reduced
  motion checked.
- Desktop/tablet/mobile controls and expanded identity checked for horizontal overflow.
- Unexpected browser errors: zero. External browser requests: zero.
- Automated Visual QC: desktop cleanup failure and mobile reduced-motion captures
  inspected directly; fixture labels, A/B separation and readable state retained.
- Human Visual Review and semantic/human grading: not performed.

Two implementation/self-review rounds: import formatting and a dictionary style
diagnostic were corrected; self-review enforced mandatory scripted failure and
clarified failure/blocked state color. No frozen execution or acceptance contracts
were changed. The browser QC was repeated after the color clarification.

Reproduce the contract checks without inference:

```bash
python3 -m pytest -q tests/test_studio_hero_adapter.py tests/test_studio_hero.py tests/test_hero*.py
python3 -m pytest -q
python3 -m ruff check kora/studio_hero_adapter.py tests/test_studio_hero_adapter.py
node --check kora/studio_assets/hero.js
```

The browser check is `scripts/check_studio_hero_adapter_browser.cjs`; it requires
an installed Playwright/Chromium and an explicitly started localhost Studio fixture
preview. Browser checks do not establish real engine compatibility or service quality.

## Changed files

- New adapter review/projection module and focused tests.
- New mock review HTML and browser QC script.
- Targeted Studio routes and asset allowlist.
- Existing Hero page link, shared browser playback and mock detail styles.
- This report and the two review breadcrumbs.

## Claim boundary and forbidden-action audit

A. Workload-control effect: actual model/provider calls remain zero. Mock adapter
events do not create task completions, savings or accepted outcomes.

B. Local-execution effect: runtime execution and physical measurements remain absent.
All output/telemetry is fixture data. Mock completion is not service acceptance.
Service acceptance and semantic non-regression remain `not_measured`;
`accepted_outcome` remains false throughout the new review.

Task027's service-quality requirement remains binding. There is no combined A/B
improvement multiplier and no measured larger-than-VRAM result.

No model download/loading/inference, provider call, H100/NVIDIA/CUDA/model-server
execution, semantic/human grading, production validation, 2×/3× claim, release,
tag, publication or repository-settings change is included.
Krako Reach remains a separate upper layer and is unchanged.

## Approval packet

Classification is `needs-cto-review`, risk medium because a new adapter event
projection and shared browser transport path need maintainer review.
Review the fixture boundary, exact identity/lifecycle validation, cleanup history,
absence of acceptance promotion and preservation of the original Hero view.

The PR is open for review only and must not be merged without explicit approval.
The next bounded implementation scope is not approved by completion of this sprint.
Actual engine configuration, placement resolution and execution require separately
scoped work and explicit execution authorization.
