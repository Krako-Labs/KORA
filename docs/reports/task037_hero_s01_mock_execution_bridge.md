# Task037 — HERO-S01 mock execution bridge

- Date: 2026-09-14
- Baseline: `HERO-BASELINE-v1`
- Goal / Sprint: G1 / HERO-S01
- Branch: `feat/hero-s01-mock-execution-bridge`
- Base: `681fcdfebc49cef85c1fa432c5feb6a983753998`
- PR: https://github.com/Krako-Labs/KORA/pull/306
- Classification: `needs-cto-review`
- Risk: medium

## Outcome

Task037 implements the bounded, fixture-only HERO-S01 bridge from the existing
deterministic planner and effective configuration to the Runtime Adapter v2 mock
lifecycle and the canonical Hero task/event stream.

A successful Studio fixture now records one contiguous ordered history for:

1. the planning bundle and sealed planning digest;
2. the task graph and route decision;
3. the selected `local_ai` adapter and exact effective configuration;
4. the mock adapter prepare/start/complete/cleanup lifecycle;
5. task completion, merge, structural/service fixture verification, and the
   fixture-only accepted outcome.

The bridge performs no model, provider, runtime, GPU, CUDA, model-server, host
probe, or network execution. Adapter completion keeps
`accepted_outcome: false`, service acceptance `not_measured`, semantic
non-regression `not_measured`, and all actual execution counters at zero.
The later Studio acceptance state is explicitly a fixture service gate, not
evidence of an actual accepted service outcome.

## Scope and design

### One canonical event owner

`kora.hero_mock_execution` owns the returned `HeroEventLog`. It copies the
validated five-event planning prefix, declares the task graph, and assigns every
subsequent event a contiguous sequence and unique run-scoped event ID.

Runtime Adapter v2 remains unchanged and independently safe. The bridge consumes
only adapter events after the planning prefix, re-identifies them in the caller's
canonical stream, and binds each event to:

- `task_id=draft`;
- the explicit attempt number;
- the existing plan ID and sealed planning digest;
- the exact effective-configuration digest;
- the selected canonical adapter and immutable mock runtime identity.

This closes the task/event integration gap without adding a live binding or
changing the reviewed adapter contract.

### Preserved task and service behavior

The Task034 Studio request and four lanes remain:

- supplied deterministic fact check;
- supplied exact-reuse result;
- a local-AI draft through the mock adapter contract;
- a supplied, provider-free independent-review fixture.

Dependencies must complete before `task.ready`. Merge is emitted only after all
four tasks have completed. A final `run.completed` requires structural and
service fixture verification to pass. The existing quality-failure path still
blocks acceptance after tasks and merge complete.

### Failure, cancellation, cleanup, and replan

The Studio selector and canonical JSON/SSE replay now cover:

- load failure;
- execute failure;
- finish failure;
- cancellation;
- cleanup failure followed by one bounded cleanup retry;
- execute failure followed by one bounded same-plan retry.

Failed and cancelled local tasks are cleaned and end in `task.failed` and
`run.failed`; merge and verification do not start. The cleanup-retry path
retains `adapter.cleanup.failed` before `adapter.cleaned` and task completion.

The replan path retains the failed attempt, emits `run.replanned`, records
`execution.plan.reaffirmed` with the unchanged plan/config digests, and starts
attempt 2. It does not claim a new optimizer decision or runtime tuning.

### Unsupported hybrid placement

The synthetic PC plan still exposes `placement_requires_runtime_plan`, while
the bridge rejects it as `placement_unresolved` after planning evidence and
before graph creation, task events, session construction, or mock allocation.
Unknown feasibility similarly stops as `no_selected_runtime`.

## Definition of done evidence

- Determinism: identical inputs produce identical bridge results and event
  histories.
- Ordering: every scenario has contiguous sequences; every replay prefix is
  accepted by the canonical reducer.
- Identity: selected adapter, plan ID, model artifact identity, planning digest,
  exact effective config, task ID, and attempt are joined in adapter/task events.
- Integrity: plan, planning-event, or model-profile tampering fails closed as
  `planning_evidence_mismatch` before a bridge result is returned.
- Lifecycle: success, load/execute/finish failure, cancellation, cleanup retry,
  and bounded replan are covered.
- Hybrid guard: unresolved placement has no graph, task, adapter, or allocation
  event.
- Merge gate: failed/cancelled task paths have no merge or verification event.
- Service gate: structural/service fixture verification is required for fixture
  acceptance; mock completion alone never promotes acceptance.
- Labels: fixture, mock, not-measured, and zero-call boundaries remain visible in
  API data and Studio.
- Recovery/UI: canonical JSON/SSE replay, reload, SSE fallback, reduced motion,
  keyboard stepping, and responsive layouts pass automated browser QC.

## Validation

Executed from the clean Task037 worktree with the existing Task034 virtual
environment and pre-existing Playwright/Chromium dependency.

- Focused Hero/adapter/Studio tests: **152 passed**.
- Full repository suite: **994 passed in 32.99s**.
- Updated Hero browser QC: **13 checks passed**.
- Existing adapter browser regression: **9 checks passed**.
- Unexpected browser console errors: zero.
- External browser requests: zero.
- Ruff on changed Python implementation/tests: passed.
- Python `compileall` for `kora` and `tests`: passed.
- JavaScript syntax for shared Hero UI and browser checker: passed.
- `git diff --check`: passed.
- Automated desktop/mobile screenshots: inspected; no clipping or horizontal
  overflow observed.
- Human visual review: not performed.
- Service-quality or semantic grading: not performed.

Browser evidence is held outside the public repository under
`local/hero-s01-task037-mock-execution-bridge/`.

## Repair loops

Three bounded validation repairs were made:

1. simplified a duplicate cleanup branch flagged by Ruff and replaced the
   obsolete fixed out-of-range cursor with an unambiguous cursor;
2. corrected new test serialization/import-boundary assertions without weakening
   execution checks;
3. strengthened the existing hidden event-history browser assertion from
   `innerText` to `textContent`, then reran both browser suites.

No production code was changed to hide a failing assertion.

## Changed files

- `kora/hero_mock_execution.py`
- `kora/studio_hero.py`
- `kora/studio_assets/hero.html`
- `kora/studio_assets/hero.js`
- `tests/test_hero_mock_execution.py`
- `tests/test_studio_hero.py`
- `scripts/check_studio_hero_browser.cjs`
- `docs/reports/task037_hero_s01_mock_execution_bridge.md`
- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

No runtime registry, planner, adapter implementation, dependency, repository
setting, release, tag, publication, model artifact, or local context file was
changed.

## Claim and safety boundary

This is deterministic fixture playback. It does not prove output quality,
semantic non-regression, physical memory behavior, latency, throughput,
larger-than-VRAM execution, production readiness, provider replacement, or a
2×/3× improvement. A. workload-control fixture behavior remains separate from
B. local-execution effects, which remain not performed/not measured.

Krako Reach is unchanged and no Hero dependency was added to it.

## Approval packet

Review the exact branch head for:

1. plan/config/adapter/task identity binding in one canonical event stream;
2. fail-closed integrity and unresolved-placement gates;
3. failure/cancel/cleanup/replan order and retained attempts;
4. merge/service fixture gates and no mock acceptance promotion;
5. canonical replay/reconnect and existing Studio/adapter regressions;
6. fixture-only claim language and zero actual execution counters.

The PR is open for review only. Do not merge without a separate explicit
approval. HERO-S01 is implemented and validated at Task037 scope, but remains
merge-pending; the Sprint and G1 are not accepted or complete.
