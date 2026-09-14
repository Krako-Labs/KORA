# Task040 — Festa replay operations and show-build lock

## Problem and outcome

The retained Mac/H100 view exposed source evidence but lacked a complete operator
path for preflight, interrupted playback, recovery and explicit fixture fallback.
The new `/hero/festa` screen adds that path while keeping source-run acceptance,
viewer readiness and synthetic playback separate.

The screen shows the request, ordered source-task lanes, recorded merge answer,
historical objective verification, source dates/call counts and evidence details.
Current-session model calls remain zero. Desktop/mobile layouts, keyboard controls
and reduced-motion playback are covered by browser verification.

## Operating contract

- `GET /api/hero/festa` revalidates package software, strict retained evidence,
  canonical event replay and a configured show-build lock on every request.
- The lock binds the package's Python sources, browser assets and JSON schemas,
  the canonical retained-view digest, and the deterministic fixture-frame digest.
- A running process whose on-disk software changes requires restart. Missing,
  malformed, symlinked, mismatched or unaccepted retained inputs block playback.
- Session recovery preserves the displayed cursor only when evidence identity,
  build identity and mode still match. A changed identity resets to event one.
- Recovery has an eight-second request timeout and disables overlapping actions.
  It revalidates and restores the viewer; it does not restart or test a model service.
- Network loss pauses retained playback. An explicit button can use the fixture
  already loaded by preflight, including while the current tab is disconnected.
  This does not provide an offline cold-start page or service worker.
- Fixture fallback remains visibly labeled synthetic; fixture completion is never
  measured source acceptance. Returning to retained mode requires fresh preflight.
- The read-only route accepts no query-driven file selection or execution command.

## Local show lock

Use an explicitly configured, privately retained integration record. No implicit
discovery, runtime connection, model download or execution is performed.

```bash
export KORA_HERO_HYBRID_EVIDENCE_PATH=/path/to/retained-integration.json
python scripts/hero_show_lock.py create --output /path/to/show-lock.json
export KORA_HERO_SHOW_LOCK_PATH=/path/to/show-lock.json
python scripts/hero_show_lock.py check --output /path/to/show-lock.json
```

Creation is exclusive and will not overwrite an existing lock. This is a local
replay build lock, not a release, deployment, digital signature or runtime-health
certificate. Keep source Git identity, dependency/environment inventory and
rehearsal receipts alongside the lock; the lock itself contains no private paths.

## Validation

- 146 focused Hero/operations tests passed.
- Full regression: 1,123 tests passed.
- Festa browser rehearsal: 36 checks passed, covering full retained playback,
  network disconnect/reconnect, one-button recovery, explicit cached offline
  fixture playback, return, identity mismatch, rejected/missing/mismatched
  preflight, overlapping-action prevention, mobile layout and reduced motion.
- Separate actual loopback test-server stop/restart: four checks passed; cursor
  and source identity survived. No model runtime was restarted.
- Existing browser regression: Hero 13, adapter 9, Mac 10 and hybrid 20 checks passed.
- Local source install, offline release smoke, wheel asset inclusion, lock overwrite
  rejection and changed-source Python/JavaScript checks passed.
- Desktop and mobile retained/fixture screenshots inspected.
- Human visual review and semantic grading were not performed.
- No new model/provider/GPU execution. Original source evidence remains unchanged.

## Evidence and closure boundary

Rehearsal uses retained sequential Mac plus separately measured H100 evidence,
alongside explicitly synthetic fixtures. It is not a fresh live multi-device
rehearsal. Viewer recovery is not runtime recovery; fixture fallback is not a
measured model success. The underlying evidence does not establish simultaneous
multi-device execution, semantic quality, production readiness, 2x/3x benefits or
physical 8GB performance.

HERO-S03 covers the frozen operating surface, retained-evidence rehearsal and local
show lock. Goal acceptance and any later live resource use remain separate.
