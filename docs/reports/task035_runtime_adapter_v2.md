# Task035 — Runtime Adapter v2 inert/mock contract

- branch: `feat/task035-runtime-adapter-v2`
- PR: https://github.com/Krako-Labs/KORA/pull/304
- base: `00a65f665c192631c8a9e425c78389c75a50c850`
- risk level: medium
- final status classification: `needs-cto-review`

## Outcome

The Hero planner previously selected declared runtime capabilities without a
lifecycle boundary that could validate and retain the exact plan/runtime/model
identity. This change adds an opt-in in-memory adapter contract to exercise that
boundary before connecting real execution.

The module reuses the [Hero runtime registry and planner](task033_runtime_capability_registry_and_planner.md),
the canonical Hero event log and replay, and preserves the
[fixture Studio](task034_hero_studio_planning_and_task_graph.md).
Existing executable MLX/llama.cpp adapters and the Solution Host registry remain
unchanged. Nothing in the CLI or Studio automatically instantiates the new session.

## Contract

| Area | Implemented behavior |
| --- | --- |
| Capability | Canonical registry IDs only; inert by default; mock explicitly selected |
| Probe / health | Declaration-only probe, no host inspection; mock readiness distinct from live readiness |
| Compatibility | Revalidate supplied contracts and rebuild the entire planning bundle from profiles and workload |
| Identity | Binding version, descriptor/planning/hardware/model/configuration/script digests and exact artifact SHA |
| Runtime version | Unknown, not probed; no installed-engine version is invented |
| Lifecycle | new → prepared → running → completed, then closed |
| Cancellation | new/prepared/running → cancelled; no late result; cleanup required |
| Failure | Scripted load/execute/finish failure retains mock allocation until cleanup |
| Cleanup | Explicit, idempotent; cleanup failure remains visible and retryable |
| Telemetry | Strict finite/nonnegative supplied fixture values; unavailable values remain null |
| Events | Contiguous hero.event.v1 stream, canonical reconnect/replay, defensive snapshot copies |
| Unsupported | Live execution, benchmark, calibration and physical telemetry |

A session is single-owner and single-run. Concurrent calls, worker scheduling,
process supervision and live-engine integration are outside this contract.
`load` and `execute` modify mock state only. `finish` returns a bounded supplied
fixture string; it does not interpret a workload or generate a model response.

Malformed contracts raise validation errors before session construction.
Well-formed but incompatible inputs expose stable reason codes with no bound
identity. Rejections include inert binding, no selected runtime, wrong adapter,
descriptor tampering, changed profile/workload/configuration/event data, non-fixture
inputs, network policy and unresolved hybrid placement.

A planning decision containing `placement_requires_runtime_plan` is rejected
even when the planner reports feasibility. A capacity estimate is insufficient
to bind a usable runtime placement plan. FreeToken/KTransformers declarations are
available, but this sprint does not resolve their hybrid placement or execute them.

## Evidence and acceptance

Adapter lifecycle extension events are retained as unknown event IDs by the
existing canonical replay reducer, as allowed by Hero v1. They do not mutate
task graphs or set run completion/verification/acceptance. The existing
`telemetry.sampled` envelope carries explicitly synthetic telemetry.

The deterministic fixture timestamp is supplied by the planning bundle, not a
measured duration. The stream preserves failure and cleanup events and supports
canonical cursor replay. Session snapshots, returned events and identity objects
cannot mutate the internal session through nested references.

A. Workload-control effect is unchanged; the adapter emits no workload-routing
savings, actual model/provider calls or accepted final outcome.

B. Local-execution effect remains unmeasured; all lifecycle/output/telemetry data
from this module is fixture-only. Runtime started is always false.

Mock completion is not service acceptance. `service_acceptance` and
`semantic_non_regression` remain `not_measured`; `accepted_outcome` stays false.
Task027's service-quality requirement and the existing Studio acceptance gate
remain intact. No combined A/B improvement multiplier is calculated.

## Validation

- New adapter tests: **57 passed**.
- Focused Hero / Studio / adapter suite: **121 passed**.
- Full repository regression suite: **919 passed** in 27.75 seconds.
- New-file Ruff: passed; Python compilation and diff whitespace: passed.
- Existing Hero automated browser/rendering regression: **10 checks passed**.
- Desktop/tablet/mobile layout, keyboard/reduced-motion, reload/reconnect,
  failed service acceptance, unknown input rejection and existing Studio harness: passed.
- Unexpected browser errors: zero; external browser requests: zero.
- Desktop accepted and mobile reduced-motion screenshots inspected directly:
  fixture labels, readable state and A/B separation retained.
- Human Visual Review and semantic/human grading: not performed.
- Markdown links and report/breadcrumb consistency: passed with two breadcrumbs.

Validation/repair rounds: two. The initial 57 behavioral checks passed.
Two test-style diagnostics were repaired (import formatting and dictionary
literal), and a mock-script digest was added during self-review before full
validation. No existing implementation or frozen contract was changed.

Reproduce without starting an inference runtime:

```bash
python3 -m pytest -q tests/test_hero_runtime_adapter_v2.py
python3 -m pytest -q tests/test_studio_hero.py tests/test_hero*.py
python3 -m pytest -q
python3 -m ruff check kora/hero_runtime_adapter_v2.py tests/test_hero_runtime_adapter_v2.py
```

The existing browser checker uses a localhost-only Studio fixture preview and
already installed Playwright/Chromium. Its success is UI regression evidence,
not evidence that these new mock sessions are connected to Studio.

## Changed files

- `kora/hero_runtime_adapter_v2.py`
- `tests/test_hero_runtime_adapter_v2.py`
- this report
- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

## Claim-boundary and forbidden-action audit

No model download/loading/inference, provider calls, live runtime execution,
H100/NVIDIA/CUDA/model-server work, semantic/human grading, production validation,
real 2×/3× larger-than-VRAM claim, release/tag/publication or repository settings
change is included. No changes to Krako Reach or its upper-layer role occurred.
Only mock/unit tests and an owned localhost Studio UI preview ran.

This contract does not prove output quality, real runtime compatibility,
performance, service acceptance, production readiness or customer savings.
It does not replace or adapt the executable Solution Host interface.

## Approval packet

Review the compatibility rejection boundary, identity binding, cancellation and
cleanup semantics, fixture labeling and lack of acceptance promotion.
Risk is medium because a future executable binding must preserve these boundaries;
passing mock tests cannot establish production lifecycle behavior.

This PR is open for review only and must not be merged without explicit approval.
The next action is maintainer review of this bounded contract. Live bindings and
the next implementation sprint require separately scoped work.
