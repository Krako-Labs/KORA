# Task039 — HERO-S02 owned H100 execution and evidence integration

- Date: 2026-09-14
- Baseline: `HERO-BASELINE-v1`; Goal / Sprint: G1, G2 / HERO-S02
- Branch: `feat/hero-s02-h100-integration`
- Base: `891695ae9fc4ae5ebced4835065f9c18a1aa2bff`
- Status: implemented and validated; uncommitted; PR not created
- Classification: `needs-cto-review`; risk: medium

## Outcome

The existing Mac slice had no measured owned-H100 counterpart or restoration-bound
combined evidence view. This change adds a bounded H100 worker, a separate service
handover supervisor state machine, and read-only composition of the retained Mac
result with the separately measured H100 result for the same supplied-value request.

The final H100 run passed structural and supplied-value validation. Its canonical
event replay and the combined replay passed. The borrowed service's pre-run model
identity and health were restored before the lease was released. Two preceding
failed attempts remain retained with their restoration receipts.

This is sequential evidence integration. It does not establish simultaneous
multi-device execution, general autonomous tuning, semantic equivalence, production
behavior, throughput, larger-than-VRAM operation, or performance superiority.

## Execution controls

- Verified existing Qwen3-30B-A3B BF16 revision
  `ad44e777bcd18fa416d9da3bd8f70d33ebb85d39`; all 16 shard hashes rechecked.
- Existing vLLM 0.28.0 and Torch 2.13.0; checked Python binary and API entrypoint.
- Observed H100 resource plan; explicitly scoped GPU-resident capability.
  The global adapter registry and physical hybrid placement are unchanged.
- Exact launch command/environment digest, offline model loading, native sampler,
  loopback model API and separately labeled private-network orchestration.
- Context 4096, concurrency 1, output maximum 256 tokens, request timeout 300 seconds.
- Worker maximum 1200 seconds inside a 30-minute exclusive lease with a 600-second
  restoration reserve; fresh ownership and remaining-time checks.
- At most two submitted model requests across this work block. The final repair
  packet reduced its call cap to one after the earlier rejected request.
- No provider fallback, package installation, model download or conversion.
- Owned process group and unit only; foreign work is preserved.
- Baseline health, served identity and idle requests checked before handover;
  restore the exact baseline and verify health before releasing the lease.

## Preserved failures and repairs

| Attempt | Result | Submitted requests | Restoration |
| --- | --- | ---: | --- |
| 1 | Engine startup failed: FlashInfer sampler JIT required unavailable nvcc | 0 | Verified; lease released |
| 2 | Engine started; decoder rejected unsupported schema feature with HTTP 400 | 1 | Verified; lease released |
| 3 | Structured response and objective checks passed | 1 | Verified; lease released |

The first repair explicitly selects the installed native PyTorch sampler. The
second adapts decoder syntax by omitting unsupported `uniqueItems` only from
the decoder schema. Independent validation still requires exactly three distinct
approved proof points, all allowed values and the ordered caveats. CPU validation
using the installed decoder reproduced the original rejection and passed the
compatible schema. The acceptance contract was not relaxed.

Attempt 2 has unknown token usage; it is counted as a submitted request, not a
completed model response. The accepted source run has one completed response.

## Final observed run

| Field | Value |
| --- | ---: |
| GPU reported memory | 85,520,809,984 bytes |
| Model shard file bytes | 61,066,575,648 |
| Input / output tokens | 256 / 108 |
| Model request interval | 7,626 ms |
| Worker interval including verification/start/cleanup | 93,138 ms |
| Full handover including baseline restoration | 161.710 seconds |
| Device-wide sampled GPU-used maximum | 77,012,664,320 bytes |
| GPU samples | 46 |
| Remote / combined canonical events | 28 / 22 |
| Commercial provider calls | 0 |
| Objective output / replay / restoration | passed |
| Semantic quality | not measured |

GPU memory was sampled with nvidia-smi at approximately one-second intervals
under an exclusive lease. It is a device-wide sample, excludes host RAM and is
not an exact peak. Shard file bytes include metadata and are not exact tensor
payload bytes. The plan's memory estimate is separate from measured runtime use.
The request interval includes inference-time kernel compilation; it is not a
steady-state benchmark or a fair speed comparison against the Mac run.

The final output digest matches the retained Mac output:
`2fa5a9f8cc92101c7912a94bb1d081ac7e0fb42152a860d9fc8e4b2aa8d7f82e`.
Both runs use a narrow allowlisted-output contract; matching digests do not prove
general model quality or semantic non-regression.

## Read-only Studio evidence

`/hero/hybrid` and `/api/hero/hybrid` are opt-in via
`KORA_HERO_HYBRID_EVIDENCE_PATH`. Composition verifies same-request digests,
output grounding, usage, replay and the matching restoration receipt. The screen
shows retained outputs, separate call counts, source digests and ordered playback.
It cannot execute, retry or send data to an external service.

Absent evidence remains unavailable. Invalid or inconsistent evidence is rejected;
fixture evidence cannot be loaded as a live result. Browser assets follow the
existing content-security policy. Raw logs, outputs, leases, host paths and
screenshots remain private.

## Validation and review

- 83 focused tests passed, including failure/cancel/lease/cleanup/budget,
  decoder compatibility, tamper rejection and read-only HTTP boundaries.
- Latest full suite after review repair: 1101 tests passed in 36.23s.
  The earlier pre-review suite passed 1092 tests in 34.79s.
- Retained pre-review browser checks: Hero 13, adapter 9, Mac evidence 10,
  combined evidence 20. UI assets are unchanged by the review repair.
- Combined browser check: keyboard stepping, final task states, API agreement,
  desktop/mobile layout, no horizontal overflow, no external or mutating requests,
  and no unexpected console errors.
- Desktop and mobile screenshots inspected; human grading was not performed.
- Changed Python Ruff/compile checks, JavaScript syntax and diff checks passed.
  The legacy Studio server retains its pre-existing Ruff exceptions.
- Initial asset routing and mobile stylesheet failures were repaired and rechecked.

## Review repair — retained event integrity

Review reproduced an inconsistent final answer accepted by the combined loader.
Acceptance-only replay checking did not bind the displayed events to the verified
sources. The loader now compares all regenerated event fields except timestamps,
checks the log identity, and validates the stored projection against replay.
Recorded timestamps and source evidence remain unchanged.

Eight new inconsistency tests failed before repair and passed afterward; a ninth
test confirms valid recorded evidence remains unchanged. The actual retained
integration record passes the repaired loader. This is an offline validation
repair; no new model execution or service handover was performed.

## Approval packet

Review the controller, handover state machine, restoration-linked evidence loader,
read-only assets and failure tests together. The executable controller digest used
by the accepted run is
`44fd8d69e19737f79369c34e7ca3a312fb37bd0b0b9aae8ec233a9d7fdb4c7a5`.

The code is validated but uncommitted. Commit, push, PR and merge require their
applicable approval. No release, tag, repository settings, public raw artifacts,
semantic grading or expanded claim is included.

HERO-S02 remains in progress pending review/integration and Sprint closure.
G1–G4 remain unaccepted. The next fixed milestone remains September 27;
HERO-S03 Festa readiness and rehearsal follow the frozen baseline.
