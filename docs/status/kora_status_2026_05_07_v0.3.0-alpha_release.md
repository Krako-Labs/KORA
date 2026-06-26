# KORA status closeout - 2026-05-07 v0.3.0-alpha Release

Date: 2026-05-07

Release: `v0.3.0-alpha`

Release/tag target HEAD: `078de0777178f8b233877f126a4ed844247da7d7`

Current public HEAD after post-release docs: `f41d7a41acb1de4a466c8a478cd03477851aa6d1`

GitHub Release URL: https://github.com/Krako-Labs/KORA/releases/tag/v0.3.0-alpha

## Release State

- Prerelease: `true`
- Release assets: none
- Raw benchmark artifacts uploaded: none
- Package version unchanged: `0.1.0a0`

## Completed Work Summary

- Added the `v0.3.0-alpha` runtime evidence architecture design.
- Added the initial runtime-path benchmark harness.
- Added the runtime benchmark JSON output path.
- Added the Markdown evidence packet/report generator.
- Added the telemetry-connected runtime summary.
- Added the reviewer-facing reproduction guide.
- Added the release-readiness checklist.
- Added the docs cross-link and claim-boundary audit.
- Added the changelog draft and release validation packet.
- Added the release approval checkpoint.
- Executed the approved tag and GitHub prerelease action.
- Refreshed local project context after the release.

## Validation Summary

- `python3 -m pytest`: 54 passed.
- `python3 -m kora run direct_vs_kora -- --offline`: passed.
- `python3 -m kora run runtime_integrated_benchmark -- --offline`: passed.
- Runtime JSON/report/telemetry generation to `/tmp`: passed.

## Expected Runtime Benchmark Counters

| Counter | Expected value |
|---|---:|
| `total_tasks` | `100` |
| `deterministic_route_count` | `80` |
| `fallback_or_model_candidate_route_count` | `20` |
| `simulated_baseline_model_invocations` | `100` |
| `kora_controlled_model_invocations` | `20` |
| `avoided_simulated_model_invocations` | `80` |
| `avoided_simulated_model_invocation_rate` | `0.8` |
| `deterministic_outputs_checked` | `80` |
| `mismatch_count` | `0` |
| `runtime_path_execution_status` | `ok` |
| `telemetry_event_count` | `100` |

## Expected Telemetry Counters

| Counter | Expected value |
|---|---:|
| `total_llm_calls` | `20` |
| `events_ok` | `100` |
| `events_fail` | `0` |
| `events_skipped` | `0` |
| `stage_counts.ADAPTER` | `20` |
| `stage_counts.DETERMINISTIC` | `80` |

## Safe Current Claim

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

## Explicit Non-Claims

KORA does not currently claim:

- production cost reduction proof
- real API-cost reduction proof
- production benchmark proof
- full runtime-integrated benchmark evidence yet
- broad workload superiority proof
- energy reduction evidence
- formal government validation
- signed partner validation unless actually signed and documented
- guaranteed adoption or funding

## Remaining Caveats

- `v0.3.0-alpha` is a prerelease.
- No release assets were uploaded.
- No raw generated benchmark artifacts were uploaded.
- Runtime evidence remains bounded and non-production.

## Recommended Next Priorities

- Prepare a post-release worktree/branch cleanup plan, but do not delete branches or worktrees in this report.
- Plan `v0.3.1-alpha`.
- Design broader workload evidence, if approved.
- Add optional external reviewer onboarding docs.
