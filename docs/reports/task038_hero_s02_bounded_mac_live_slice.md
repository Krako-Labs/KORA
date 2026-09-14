# Task038 — HERO-S02 bounded Mac live slice

- Date: 2026-09-14
- Baseline: `HERO-BASELINE-v1`
- Goal / Sprint: G1 / HERO-S02
- Branch: `feat/hero-s02-bounded-mac-live-slice`
- Base: `da0d8481a147a9d2a86a1721f7cb076761a1bc26`
- PR: https://github.com/Krako-Labs/KORA/pull/307
- Classification: `needs-cto-review`
- Risk: medium

## Outcome

Task038 replaces one narrow HERO-S01 fixture boundary with one observed,
bounded, local-only execution slice. The existing deterministic planner selects
the checked `llama.cpp` adapter for an observed Apple Silicon host and a checked
Qwen3 GGUF artifact. One OpenAI-compatible chat-completion call produces a
schema-constrained service brief, after which deterministic checks enforce exact
supplied values, required caveats, prohibited-claim exclusion, cleanup, and
canonical event replay.

The observed run passed those objective checks. It made one model call and zero
provider calls. It does not establish semantic quality, user preference,
production behavior, throughput, total-system peak memory, larger-than-VRAM
behavior, provider replacement, or performance superiority.

## Boundaries and controls

The runner is fail-closed and enforces:

- a loopback-only OpenAI-compatible endpoint;
- exact SHA-256 checks for both runtime binary and model artifact;
- observed host and model profiling before execution;
- a planner result selecting `llama.cpp` before runtime attachment or start;
- concurrency `1`, context `4096`, and output maximum `256` tokens;
- at most two model attempts: the initial call plus one retry only for malformed
  or truncated structured output;
- a five-minute request timeout and a 20-minute live-window ceiling;
- zero provider calls and no remote endpoint;
- process-identity, listener, and health verification before and after borrowing
  a pre-existing project-local server;
- cleanup evidence retained on both success and failure.

The existing-server path does not start, stop, or reconfigure the borrowed
server. The owned-server path starts a new process group, samples its process
RSS, and stops only that owned process. Neither path treats process RSS as total
system memory.

## Objective output contract

The model response must contain exactly these fields:

- one supplied headline;
- one supplied audience;
- one supplied promise;
- exactly three distinct supplied proof points;
- the two required caveats in the required order.

The JSON schema constrains every value to the supplied allowlists. Independent
deterministic validation repeats those checks and rejects prohibited claims.
This is grounding and schema evidence, not semantic grading.

The accepted local output digest is
`2fa5a9f8cc92101c7912a94bb1d081ac7e0fb42152a860d9fc8e4b2aa8d7f82e`.
The raw model output remains in local-only retained evidence and is not copied
into this public report. The objective result records that it matched the
supplied allowlists and preserved the required caveats.

## Observed execution

The run used an existing idle project-local `llama-server`; no runtime process
was started by Task038.

| Field | Observed value |
| --- | ---: |
| Host physical memory | 34,359,738,368 bytes (32 GiB) |
| Architecture | Apple Silicon `arm64` |
| Model artifact | Qwen3-30B-A3B Q4_K_M GGUF |
| Model artifact bytes | 18,556,685,824 |
| Model SHA-256 | `0d003f6662faee786ed5da3e31b29c978de5ae5d275c8794c606a7f3c01aa8f5` |
| Runtime | `llama-server`, build 10818, commit `4d9176092` |
| Runtime SHA-256 | `83f53b104d16220f3f56773137836cf44c9ab1df2f5cc8eead0975c12ab2e667` |
| Runtime processes started | 0 |
| Model calls | 1 |
| Provider calls | 0 |
| Input tokens | 364 |
| Output tokens | 92 |
| Model request time | 54,450 ms |
| Borrowed-runtime interval | 54,605 ms |
| End-to-end bounded runner interval | 97,312 ms |
| Sampled process-RSS peak | 77,430,784 bytes |
| Process-RSS samples | 475 |
| Canonical events | 37 |
| Objective result | pass |
| Semantic non-regression | not measured |
| Cleanup | success; pre-existing runtime preserved |

The process-RSS value is a 50 ms sample of the pre-existing `llama-server`
process only. It excludes total system memory and must not be used as a model
footprint, total peak-memory, or larger-than-VRAM claim. The end-to-end runner
interval includes artifact/identity validation; the borrowed-runtime interval is
the narrower attach-through-cleanup interval.

## Evidence and Studio surface

The local evidence envelope records immutable planning, hardware, model,
runtime, effective-configuration, input, and output digests; usage; cleanup;
actual call counters; separated A/B evidence; and the canonical Hero event log.
The event log replays to the same completed tasks, passed objective verification,
and accepted objective outcome.

Studio adds an opt-in, read-only `/hero/live` surface. It is unavailable unless
`KORA_HERO_LIVE_EVIDENCE_PATH` is explicitly set. The loader accepts only a
small regular non-symlink file and rejects malformed, non-observed, non-loopback,
provider-call, over-budget, semantically promoted, cleanup-failed, or replay-
inconsistent evidence. It never triggers execution.

Raw execution evidence and browser screenshots remain outside the public
repository under the project-local Task038 evidence directory.

## Validation

- Focused live/adapter/Studio and existing Hero regression: **135 passed**.
- Full repository suite: **1018 passed in 34.17s**.
- Existing Hero browser regression: **13 checks passed**.
- Existing adapter browser regression: **9 checks passed**.
- New live-evidence browser QC: **10 checks passed**.
- Unexpected browser console errors: zero.
- External browser requests: zero.
- Ruff on changed Python implementation/tests: passed. The pre-existing Studio
  server file was checked with its unchanged baseline ignores.
- Python `compileall`: passed.
- JavaScript syntax checks: passed.
- `git diff --check`: passed.
- Human visual review: not performed.
- Semantic grading or preference comparison: not performed.

## Changed files

- `kora/hero_live_execution.py`
- `kora/adapters/openai_compatible_local.py`
- `kora/studio_hero_live.py`
- `kora/studio_server.py`
- `kora/studio_hero.py`
- `kora/studio_assets/hero-live.html`
- `kora/studio_assets/hero-live.js`
- `kora/studio_assets/hero.html`
- `scripts/run_hero_s02_mac_live.py`
- `scripts/check_studio_hero_live_browser.cjs`
- `tests/test_hero_live_execution.py`
- `tests/test_studio_hero_live.py`
- `tests/test_openai_compatible_local_adapter.py`
- `docs/reports/task038_hero_s02_bounded_mac_live_slice.md`
- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

No dependency, provider adapter, registry, package, release, tag, repository
setting, H100 path, model artifact, or production configuration was changed.
Krako Reach is unchanged.

## Approval packet

Review the exact branch head for:

1. loopback, identity, token, call, timeout, retry, and cleanup enforcement;
2. exact-value response schema plus independent deterministic validation;
3. canonical task/event ordering and replay agreement;
4. safe preservation of a verified pre-existing runtime;
5. opt-in read-only Studio evidence validation and existing UI regressions;
6. strict separation of observed objective checks from unmeasured semantics,
   production behavior, total memory, and performance claims.

The PR is for review only. Do not merge without a separate explicit approval.
HERO-S02 has one implemented and validated Mac slice at Task038 scope, but the
Sprint and G1 are not accepted or complete.
