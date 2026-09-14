# Task034 — Hero Studio Planning and Task Graph

- branch: `feat/task034-hero-studio`
- PR: https://github.com/Krako-Labs/KORA/pull/303
- base: `581440094001dd776d35a071c8243dac6ba5553b`
- risk level: medium
- final status classification: `needs-cto-review`

## Outcome and scope

Studio now has an additive `/hero` surface linked from the existing Studio rail.
It consumes a canonical `HeroPlanningBundle` produced by the existing planner and
an ordered `HeroEvent` fixture stream. Each displayed frame is projected by the
existing Python replay reducer. No runtime adapter or model loader is connected.

The visible story follows the supplied workload through profile analysis,
candidate decisions, task creation, the four executor routes, merge,
verification plus service acceptance, and the final accepted or rejected outcome.
The sample request is read-only: arbitrary workload interpretation is outside this
fixture sprint. Every output and acceptance decision is illustrative.

## Delivered behavior

- Large THIS COMPUTER and MODEL FOOTPRINT cards retain adjacent FIXTURE labels.
  Weight bytes are distinct from model artifact size and runtime peak memory.
- MLX-LM, llama.cpp, FreeToken and KTransformers display the actual planner
  selected/rejected decisions and reason codes.
- Nodes appear only on task-created events, move into lanes only when routed,
  and change state only as the event cursor advances. Dependencies, adapter,
  attempt, and illustrative result remain visible.
- Deterministic, Exact Reuse, Local AI and Frontier AI have separate lanes.
  The frontier lane is simulated, not a network or provider execution.
- Pause, next-event stepping and replay control the event cursor.
- SSE supplies bounded fixture frames. JSON event retrieval is the recovery path;
  Last-Event-ID and explicit cursor bounds are supported.
- Reload restores the same projection, task outputs, service state and history
  from the stored scenario, planning digest and event cursor. Reload is paused.
- Reduced-motion preferences disable animation while preserving all state changes.
- All Hero handlers bypass real system probing. Existing Studio behavior is
  retained, including the deterministic local harness.
- Package data includes the reviewed HTML, CSS and JavaScript assets.

## Fixture scenarios

| Scenario | Planning result | Final fixture state |
| --- | --- | --- |
| Apple | 32 GiB unified / 18 GiB safetensors weights; MLX-LM selected | Accepted after synthetic service verification |
| PC | 8 GiB dedicated GPU + 32 GiB RAM / 18 GiB GGUF weights; llama.cpp selected | Accepted fixture; placement still requires a runtime plan |
| Unknown overhead | KV and reserve estimates absent; no candidate selected | Fails before task creation |
| Service-quality failure | Same feasible Apple plan and completed tasks | Not accepted despite structural pass and completed merge |

The planning prefix contains five events. Complete and service-failure stories
contain 31 events; the unknown-overhead story contains six. All events retain
`evidence_level=fixture`.

## Acceptance and evidence separation

The UI requires canonical run completion, verification pass, structural fixture
pass, and service fixture pass together before displaying **Accepted · fixture**.
Canonical completion alone cannot bypass the UI service gate. This preserves the
Task027 principle that completed work or resource reduction cannot substitute for
service acceptance.

A. Workload-control effect exposes completed **fixture task counts** by route.
Actual model calls and actual provider calls remain zero. No savings percentage
is derived.

B. Local-execution effect exposes planning-only profiles and explicitly
unmeasured peak memory, latency and throughput. No runtime was started.
Semantic non-regression and real service quality remain unmeasured. A and B are
never combined into an improvement multiplier.

## Validation

- Focused Hero + Studio Hero tests: **64 passed**.
- Full repository suite: **862 passed** in 27.06 seconds.
- New Python files: Ruff passed.
- Touched legacy Python files: baseline comparison found **zero new diagnostics**.
  There are 37 inherited diagnostics (four in Studio server, 33 in its existing
  tests); these remain separate maintenance debt.
- Python compileall, JavaScript syntax and diff whitespace checks: passed.
- Release smoke: passed. This is a local packaging check, not a release.
- sdist/wheel build and isolated installed-wheel Hero asset/fixture smoke: passed.
- Automated browser/rendering QC: **10 checks passed**:
  exact-frame reload, history restoration, play/pause, completed reload,
  service rejection, unknown-input rejection, SSE failure recovery,
  reduced-motion plus keyboard operation, responsive layout at 1440×1080,
  1024×768 and 390×844, and existing Studio harness regression.
- Unexpected browser console errors: zero. External browser requests: zero.
- Desktop and mobile screenshots were directly inspected. Human Visual Review
  has not been performed; this is automated visual review, not semantic grading.
- An offline review copy uses the same fixture frames and renderer; its complete
  file-based playback passed with no page errors. It is review material, not a separate execution result.
- Markdown links and report/breadcrumb consistency: passed with two breadcrumbs.

Validation/repair rounds: four. Repairs were limited to generated-source newline
escaping, the HTTP JavaScript MIME expectation, the package-data allowlist for
the new HTML asset, and import presentation/static-baseline reconciliation.
No runtime, provider, model or service execution failure was concealed as success.

## Reproduction

Start the existing localhost-only Studio preview:

```bash
python3 -m kora studio --no-browser --port 8794
```

Open `http://127.0.0.1:8794/hero`. Choose a planning fixture, then Play fixture,
Next event, or Replay. Reload mid-story to inspect state restoration.

Run focused checks:

```bash
python3 -m pytest -q tests/test_studio_hero.py tests/test_hero*.py
node scripts/check_studio_hero_browser.cjs http://127.0.0.1:8794
```

The browser checker requires an already installed Playwright module and Chromium.
It may resolve Playwright through `KORA_PLAYWRIGHT_MODULE`. It does not install or
download models. Screenshots and browser QC JSON are local review artifacts.

## Changed files

- `kora/studio_hero.py`
- `kora/studio_assets/hero.html`
- `kora/studio_assets/hero.css`
- `kora/studio_assets/hero.js`
- `kora/studio_server.py`
- `kora/studio_shell_render.py`
- `pyproject.toml`
- `tests/test_studio_hero.py`
- `tests/test_kora_studio_server.py`
- `scripts/check_studio_hero_browser.cjs`
- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- this report

## Claim-boundary and forbidden-action audit

No provider calls, model download/loading/inference, runtime execution,
H100/NVIDIA/CUDA execution, semantic/human grading, production validation,
measured larger-than-VRAM claim, release, tag, repository-setting change or
Krako Reach integration occurred. Only the explicitly authorized localhost UI
preview and test infrastructure ran.

No private operational paths or raw model/provider outputs belong to this PR.
Fixture acceptance does not prove output quality, production readiness,
performance, customer savings or real 2×/3× model execution.

## Approval packet

Review the fixture labeling, acceptance gate, event/state recovery, accessibility,
and additive Studio integration. Risk is medium because this is a new public
demo surface with claim-sensitive presentation.

This PR is open for review only and must not be merged without explicit
maintainer approval. The next bounded engineering block after merge is Runtime
Adapter v2 using inert/mock adapters before any live execution authorization.
