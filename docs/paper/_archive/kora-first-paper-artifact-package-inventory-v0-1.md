# KORA First Paper Artifact Package Inventory v0.1

Status date: 2026-05-13

## Purpose

This inventory lists repository-tracked materials that may support a future paper submission package. It does not create a package, upload artifacts, or claim formal artifact approval.

## Tracked Paper Files

- `docs/paper/kora-first-paper-manuscript-v0-4.md`
- `docs/paper/kora-first-paper-manuscript-bibliography-sync-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-claim-to-evidence-audit-v0-1.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-submission-readiness-gate-v0-1.md`
- `docs/paper/kora-first-paper-final-bibliography-claim-audit-v0-1.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-figures-and-tables.md`
- `docs/paper/kora-first-paper-figure-specs.md`
- `docs/paper/kora-first-paper-table-specs.md`
- `docs/paper/kora-first-paper-evidence-summary.md`

## Tracked Runtime and Evidence Docs

- `docs/reports/v0.3.0-alpha-runtime-evidence-reviewer-guide.md`
- `docs/reports/benchmark_artifact_policy.md`
- `docs/reports/v0.3.0-alpha-docs-claim-audit.md`
- `docs/reports/v0.3.0-alpha-release-validation-packet.md`

## Tracked Code, Workloads, and Examples

- `kora/`
- `tests/`
- `examples/runtime_integrated_benchmark/run.py`
- `examples/runtime_integrated_benchmark/report.py`
- `examples/customer_support_triage_fake_validation/run.py`
- `examples/direct_vs_kora/run.py`
- `experiments/generate_workload.py`
- `experiments/run_benchmark.py`
- `experiments/summarize_benchmark_results.py`
- `experiments/workloads/deterministic_heavy_v1_100.json`
- `experiments/workloads/customer_support_triage_synthetic_v1.json`

## Tracked Benchmark or Report Artifacts

- The repository includes reviewer-safe documentation and sample inputs.
- The repository does not need raw temporary benchmark JSON outputs for this packet.
- Any generated benchmark or telemetry output should be reviewed before public inclusion.

## Included In Repository

- Source code needed to run local KORA examples.
- Offline examples and tests.
- Deterministic-heavy workload files.
- Paper draft and audit docs.
- Claim-boundary, bibliography, and submission-readiness docs.
- Repository license file.

## Deliberately Not Included

- Raw provider responses.
- API keys or provider credentials.
- Production traffic.
- Private user data.
- Proprietary datasets.
- Raw benchmark artifacts generated in temporary directories.
- Release assets or packaged submission uploads.

## Remaining Package Work

- Select exact artifact bundle after venue/export direction is known.
- Capture a clean reproduction transcript on the final package commit.
- Finalize figures, tables, captions, and manuscript export.
- Finalize bibliography and citation format.
- Prepare artifact availability statement.
- Review license, author, affiliation, acknowledgement, funding, conflict, and ethics metadata.

## Claim Boundary

This inventory supports reproducibility planning only. It does not support production cost reduction proof, real API-cost reduction proof, production benchmark proof, broad workload superiority, energy reduction evidence, formal government validation, signed partner validation, guaranteed adoption or funding, or formal artifact approval.
