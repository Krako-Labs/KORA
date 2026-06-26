# KORA Repository Hygiene And File Organization Audit

Date: `2026-05-06`

## 1. Purpose

This is an audit-only document. It does not delete, move, rename, or rewrite repository files.

KORA is preparing to grow as a serious OSS infrastructure project. Repository cleanup should make the project easier to navigate without damaging the evidence trail that supports releases, benchmarks, paper work, EIC/grant readiness, investor technical diligence, and community onboarding.

Any cleanup must preserve:

- release evidence
- benchmark evidence
- paper evidence
- EIC/grant evidence
- investor diligence evidence
- community onboarding value
- status closeout/start-of-work continuity

## 2. Current Repository Baseline

- Official repo URL: https://github.com/Krako-Labs/KORA
- Current `origin/main` HEAD: `27242a2d55eb3ad359dcada3cd888c2d7befce0f`
- Published release: `v0.2.0-alpha`
- Release URL: https://github.com/Krako-Labs/KORA/releases/tag/v0.2.0-alpha

Current safe benchmark claim:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

Do-not-claim reminder:

- no production cost reduction proof
- no real API-cost reduction proof
- no production benchmark proof
- no full runtime-integrated benchmark evidence
- no broad workload superiority proof
- no energy reduction evidence
- no formal partnership unless signed or documented
- no government validation unless formally documented

## 3. Top-Level Structure Review

| Path | Classification | Notes |
|---|---|---|
| `README.md` | Needs better linking | Product/category positioning now leads correctly; migration note is subtle. It should later link to claims, OSS operating docs, open roles, and benchmark evidence. Some `v0.1` wording remains and should be reviewed after `v0.2.0-alpha`. |
| `pyproject.toml` | Keep as-is | Package metadata now points to `Krako-Labs/KORA`. Keep unless packaging changes require updates. |
| `CHANGELOG.md` | Needs cleanup audit | Still says `v0.2.0-alpha` is not yet released. Needs safe post-release correction, but not in this audit task. |
| `LICENSE`, `NOTICE` | Keep as-is | Legal surface should remain stable. |
| `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md` | Needs better linking | These are important OSS trust files; link them from future docs index and README contributor section. |
| `ARCHITECTURE-OVERVIEW.md`, `EXECUTIVE-SUMMARY.md`, `GOVERNANCE.md`, `ROADMAP.md`, `VISION.md` | Potential move/rename candidate | Root-level strategic docs overlap with `docs/` versions and newer context/vision docs. Preserve until reviewed; consider linking or moving under docs later. |
| `KORA_Pitch_Source_2026_Feb.txt` | Potential archive candidate | Likely strategic source material. Preserve for investor/EIC history; consider internal/private or `docs/strategy` consolidation later. |
| `appendix_1_kora_technical_overview.md`, `appendix_2_kora_execution_and_quant_model.md` | Needs later technical review | Potential paper/supporting material; should be indexed or moved under `docs/paper`/`docs/research` after review. |
| `kora/` | Keep as-is | Core package structure is clear and test-covered. Needs future technical architecture review before refactor. |
| `examples/` | Keep as-is | Runnable examples align with CLI. Needs stronger README/docs links and smoke-test coverage. |
| `experiments/` | Needs cleanup audit | Contains benchmark scripts and workloads. README has older skeleton language and old v0 counters; update later without altering evidence. |
| `docs/` | Needs better linking | Documentation value is high but navigation is fragmented. Priority next step is a docs index/navigation map. |
| `.github/` | Keep as-is | Issue templates, PR template, and CI exist. Future work may add CODEOWNERS and additional workflows. |
| `tests/` | Keep as-is | Test suite supports current package and benchmark behavior. |
| `scripts/` | Needs cleanup audit | Contains status closeout, release, Linear, metrics, and reporting scripts. Needs ownership and current-use review before any cleanup. |
| `tools/` | Keep as-is | Small utility surface; keep until broader tooling audit. |
| `assets/` | Keep as-is | Logo assets used by README. |
| `artifacts/` | Needs later technical review | Contains metrics artifacts. Determine whether these are historical evidence, generated outputs, or should move to docs/metrics policy. |
| `studio/` | Needs later technical review | Product/prototype surface separate from current CLI-first core. Needs explicit status and public/private boundary review. |

## 4. Docs Structure Review

| Folder | Purpose | Current value | Overlap or duplication risks | Recommended future organization |
|---|---|---|---|---|
| `docs/ops` | Operating system, migration, GitHub setup, coordinator docs | High | Many dated ops docs need an index | Add `docs/ops/README.md` or global docs index |
| `docs/context` | Removed from public docs after public/private boundary audit | N/A | Internal operating context belongs in private internals | Do not restore local handoff context to public docs |
| `docs/claims` | Public language and claim registry | High | Overlaps with non-claim sections in reports | Keep as canonical; reports should reference it later |
| `docs/community` | Community workflow, roles, AI-assisted contribution | High | Overlaps with GitHub setup and open roles | Keep; create community index later |
| `docs/paper` | Paper authorship and contribution policy | High | Paper source material also exists in root/docs research | Expand into paper index later |
| `docs/benchmarks` | Benchmark summaries and workload expansion plans | High | Overlaps with reports, experiments README, technical preview docs | Preserve; add benchmark index and evidence map |
| `docs/reports` | Release readiness, status closeout, artifact policy, validation packets | High | Mixed release reports and sample telemetry input | Preserve; consider reports index |
| `docs/status` | Earlier end-of-day reports | High for continuity | Overlaps with `docs/reports` status closeout content | Preserve; decide whether status closeout reports belong under one folder |
| `docs/vision` | Category thesis | High | Overlaps with root `VISION.md` and docs/VISION.md | Keep new dated thesis; review older vision docs later |
| `docs/specs` | Architecture, contracts, governance, studio specs | High but broad | May contain Krako Cloud/studio material beyond current public core | Preserve; add spec index and status labels |
| `docs/metrics` | Metrics benchmark artifacts and reports | Medium/high | May overlap with `artifacts/metrics` and benchmarks | Preserve; review artifact policy and source-of-truth |
| `docs/progress` | Historical progress reports | Medium | Overlaps with status closeout/reports | Preserve until history consolidation |
| `docs/strategy` | Pitch/source strategy materials | Medium/high | Potential public/private sensitivity | Review public/private boundary before linking |
| Root-level `docs/*.md` | Foundational architecture, philosophy, benchmark, research docs | High but disorganized | Duplicates root docs and newer structured docs | Priority docs index should classify these before move/rename |

## 5. Evidence Preservation Map

Do not remove without explicit review:

Release history:

- `CHANGELOG.md`
- `docs/release_note_v0_1_alpha.md`
- `docs/release_note_v0_1_1_alpha.md`
- `docs/reports/v0.2.0-alpha-*`
- `docs/reports/kora_status_2026-05-05_v0.2.0-alpha.md`

Benchmark evidence:

- `experiments/workloads/deterministic_heavy_v0.json`
- `experiments/workloads/deterministic_heavy_v1_100.json`
- `experiments/generate_workload.py`
- `experiments/run_benchmark.py`
- `experiments/summarize_benchmark_results.py`
- `docs/benchmarks/kora_benchmark_result_v0_1_1_alpha.md`
- `docs/benchmarks/kora_benchmark_result_v1_100.md`
- `docs/reports/benchmark_artifact_policy.md`

status closeout/start-of-work continuity:

- `docs/status/*`
- `docs/reports/kora_status_*`
- Former `docs/context/*` local handoff files, now private-only material

Paper preparation:

- `docs/paper/*`
- `docs/vision/2026-05-06-kora-category-thesis.md`
- `docs/research-agenda.md`
- `docs/technical_preview_results.md`
- root appendix files

EIC/grant readiness:

- private-only operating context
- `docs/claims/*`
- `docs/ops/*`
- `docs/strategy/*`
- `EXECUTIVE-SUMMARY.md` and `docs/EXECUTIVE-SUMMARY.md`

Investor technical diligence:

- architecture/spec docs
- benchmark docs
- release reports
- claim registry
- category thesis

OSS/community operating history:

- `.github/ISSUE_TEMPLATE/*`
- `.github/pull_request_template.md`
- `docs/community/*`
- `docs/ops/2026-05-06-kora-oss-operating-system.md`
- `docs/ops/2026-05-06-kora-github-platform-setup-plan.md`

## 6. Duplicate Or Overlap Candidates

Do not remove anything in this section. These are candidates for later review only.

Benchmark reports:

- `docs/benchmarks/*`, `docs/reports/*`, `docs/technical_preview_results.md`, and `experiments/README.md` overlap. Risk: readers may see older skeleton language beside newer v1_100 evidence.

status closeout reports:

- `docs/status/*` and `docs/reports/kora_status_*` overlap. Risk: multiple history locations make continuity hard to follow.

Technical preview docs:

- `docs/technical_preview_results.md`, `docs/benchmarks/*`, and release readiness reports overlap. Risk: one doc may become stale while another remains accurate.

Migration docs:

- migration checklist, README repository note, current state context, and ops docs overlap. Risk: too many places explain migration; keep one canonical link later.

Context docs:

- category thesis, claim registry, and OSS operating docs overlap in project identity language. Risk: source-of-truth confusion unless indexed.

OSS operating docs:

- `docs/community/*` and `docs/ops/*` overlap around weekly cadence, roles, and GitHub workflow. Risk: duplicate update burden.

Claim language docs:

- claim registry, public language guide, release reports, and benchmark policy all contain non-claim wording. Risk: claim boundary updates must be propagated or referenced.

## 7. Public / Private Boundary Review

Safe public docs:

- README, package metadata, issue templates, contribution docs, claim registry, public language guide, OSS operating docs, benchmark summaries, release reports.

Internal-facing but acceptable in public repo:

- private operating context, historical continuity docs, ops coordinator handbook, GitHub setup plan.

Should maybe move to internal/private repo later:

- strategy pitch source files, investor/EIC narrative drafts, personal operational notes if any are added later.

Should be clearly marked internal-only:

- future private handoff artifacts that include private strategy, names, contact details, or unpublished partner/investor details.

Should not include personal/private data:

- resumes, private contact details, private partner notes, unpublished investor conversations, unapproved institutional interest.

## 8. README And Onboarding Review

- README now leads with KORA's product/category positioning before the migration note.
- The migration note is appropriately subtle.
- Quickstart is runnable and developer-oriented.
- README still uses `v0.1` language while the current published release is `v0.2.0-alpha`; this needs a safe docs polish task.
- Contributor/open roles/community docs are not yet discoverable from README.
- Future links should include claim registry, docs index, open roles, AI-assisted contribution guide, benchmark evidence, and GitHub Discussions once configured.

## 9. Naming And Date Convention Review

- New ops/community/context docs use `2026-05-06-*` naming consistently.
- Some older reports use `2026_05_04` or mixed date separators.
- Task-number references are useful for operating continuity but should not dominate public-facing navigation.
- Alpha naming is mostly consistent, but CHANGELOG still needs post-release correction for `v0.2.0-alpha`.
- Folder naming is mostly clear, but root-level docs versus `docs/` subfolders need index-based clarification before any move.

## 10. Code And Experiment Structure Review

`kora/` package:

- clear modules for adapters, budget, CLI, cost model, executor, retrieval, scheduler, task IR, telemetry, and verification.
- needs later technical review before architecture refactor.
- should remain stable until runtime-integrated benchmark planning.

`examples/`:

- contains `hello_kora`, `direct_vs_kora`, `retry_demo`, `real_workload_harness`, and `stress_test`.
- needs stronger docs links and smoke-test mapping.

`experiments/workloads`:

- `deterministic_heavy_v0.json` and `deterministic_heavy_v1_100.json` should be preserved as benchmark evidence/workload history.

Benchmark-related scripts:

- `experiments/generate_workload.py`, `experiments/run_benchmark.py`, and `experiments/summarize_benchmark_results.py` are core evidence-path files.
- `scripts/metrics/*` may be related to later metrics work and needs technical review before cleanup.

Telemetry/reporting files:

- `kora/telemetry.py`, `docs/reports/sample_telemetry_input.json`, and status closeout/report scripts should be preserved.
- Generated telemetry outputs should remain ignored or ephemeral unless explicitly selected as evidence.

Needs technical review:

- `studio/`
- `artifacts/metrics/`
- `scripts/linear*`
- `scripts/metrics/*`

Needs docs link:

- `examples/`
- `experiments/`
- `docs/claims/`
- `docs/community/`
- `docs/ops/`

Needs smoke test:

- CLI examples list
- hello/retry/direct_vs_kora offline
- telemetry sample
- benchmark dry-run/direct/kora-controlled summary flow

Future cleanup:

- stale README/CHANGELOG/experiments README wording
- root docs versus docs folder duplication
- status closeout/report folder split

Preservation as benchmark artifact:

- tracked workloads
- benchmark result summaries
- artifact policy
- release validation reports

## 11. Cleanup Priority List

Priority 0: do not touch / preserve.

- release notes, changelog history, tags/release docs, benchmark workloads, benchmark runner/generator/summary scripts, test suite, license/security/contributing files, claim registry, artifact policy, v0.2.0-alpha reports.

Priority 1: safe documentation linking or index creation.

- create docs index/navigation map
- link README to claims, open roles, benchmark evidence, docs index
- create ops/community/benchmarks index pages
- link old reports to canonical claim registry

Priority 2: safe rename/move candidates after review.

- root strategic docs into `docs/`
- root appendices into `docs/paper` or `docs/research`
- older docs into structured folders if links are preserved

Priority 3: archive candidates after stronger review.

- stale strategy text files
- old progress/status closeout drafts after index and preservation decision
- legacy pitch source copies

Priority 4: possible removal candidates, only after explicit approval.

- generated artifacts that are not evidence
- obsolete duplicate docs after preservation copies and links exist
- unused scripts after technical ownership review

## 12. Recommended Next Tasks

- Task 134: create docs index / navigation map if needed.
- Task 135: safe docs link cleanup.
- Task 136: repo-managed PR template and CODEOWNERS draft.
- Task 137: private community operations material.
- Task 138: GitHub manual setup execution log.

## 13. Explicit Non-Actions

This task does not:

- delete files
- rename files
- move files
- alter benchmark evidence
- alter release history
- alter public claims
- change repository settings
