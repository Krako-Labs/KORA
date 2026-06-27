# KORA First Paper Reproduction Transcript Checklist v0.1

Status date: 2026-05-13

## Purpose

This checklist drafts the commands and evidence expectations for a future clean reproduction transcript. It uses existing repository commands and docs only. It does not create a final transcript and does not mark the paper as submission-ready.

## Source Files Reviewed

- `README.md`
- `docs/reports/v0.3.0-alpha-runtime-evidence-reviewer-guide.md`
- `docs/reports/benchmark_artifact_policy.md`
- `docs/paper/kora-first-paper-evidence-summary.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`

## Baseline Validation Commands

Run these from a clean checkout after installing the project in a local environment:

```bash
git diff --check
python3 -m pytest
python3 -m kora --help
python3 -m kora examples list
```

Expected output type:

- `git diff --check` should complete without whitespace errors.
- `python3 -m pytest` should complete with the test suite passing.
- CLI help and examples listing should print normal command/help output.

## Offline Example Commands

```bash
python3 -m kora run direct_vs_kora -- --offline
python3 -m kora run customer_support_triage_fake_validation -- --offline
python3 -m kora run runtime_integrated_benchmark -- --offline
```

Expected output type:

- Each command should run locally without provider credentials.
- The runtime-integrated benchmark should report deterministic-heavy workload evidence consistent with the current paper claim boundary.
- The customer-support validation remains local/no-network validation evidence, not production evidence.

## Optional Runtime Evidence Commands

The runtime evidence reviewer guide documents optional local report generation commands using temporary output paths:

```bash
python3 -m kora run runtime_integrated_benchmark -- --offline --json-out /tmp/kora_runtime_integrated_benchmark.json
python3 examples/runtime_integrated_benchmark/report.py --input /tmp/kora_runtime_integrated_benchmark.json --md-out /tmp/kora_runtime_integrated_benchmark.md
python3 -m kora telemetry --input /tmp/kora_runtime_integrated_benchmark.json --json-out /tmp/kora_runtime_integrated_telemetry.json --md-out /tmp/kora_runtime_integrated_telemetry.md
```

Expected output type:

- JSON and Markdown outputs should be generated at the requested temporary paths.
- Any final transcript should summarize command success and reviewer-safe metrics.
- Raw generated outputs should be reviewed before inclusion in any submission package.

## Raw Artifact Policy Reminder

- Do not upload raw benchmark artifacts by default.
- Do not commit temporary JSON, Markdown, telemetry, provider-response, or local transcript files unless they are explicitly reviewed and selected for public inclusion.
- Do not include secrets, API keys, private user data, production traffic, raw provider responses, or proprietary datasets.
- Use reviewer-safe summaries and tracked docs where possible.

## Transcript Limitations

- This checklist is not a completed reproduction transcript.
- These commands do not provide production benchmark proof.
- These commands do not provide real API-cost reduction proof.
- These commands do not provide energy reduction evidence.
- These commands do not constitute formal artifact approval.
- Final transcript capture should be repeated on the exact commit intended for a submission package.
