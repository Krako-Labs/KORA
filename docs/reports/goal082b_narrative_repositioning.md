# Goal 082B Narrative Repositioning

Status: implemented.

## Scope

Goal 082B repositions public documentation from a routing-kernel/evidence-focused presentation toward KORA as an AI Workload Control Layer. The work updates onboarding and navigation while staying inside existing evidence boundaries.

No new technical evidence was created. No production claims were added.

## Base Condition

This work used the latest completed Goal 082A material as the confirmed-available base in a fresh scoped worktree. Dirty local `main` was not used.

## Files Updated

- `README.md`
- `docs/README.md`
- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

## Files Added

- `docs/vision/kora_workload_control_layer.md`
- `docs/reports/goal082b_narrative_repositioning.md`

## Narrative Shift

Previous public emphasis:

- KORA Core.
- KRK routing kernel.
- benchmark/evidence package.
- release-candidate readiness.

New README emphasis:

- KORA as an AI Workload Control Layer.
- model calls should not be the default unit of all work.
- many AI tasks are classification, validation, routing, policy, cache reuse, workflow control, or deterministic processing.
- KORA helps determine what should reach a model, what does not need a model, and how work should move through an AI system.
- examples are the first-value path.

## Example Visibility

The README now prominently features:

- KORA Doctor.
- KORA Doctor Report Pack.
- Deterministic Classification.
- Classification Expansion Pack.

Quick-start commands included:

```bash
python3 -m kora examples list
python3 examples/kora_doctor/run.py
python3 examples/kora_doctor/run.py --all
python3 examples/deterministic_classification/run.py
python3 -m kora run deterministic_classification
```

## Claim Boundaries

The rewrite avoids claims of:

- production cost reduction proof.
- broad workload superiority.
- production readiness.
- benchmark superiority.
- automatic savings.
- model replacement.
- production diagnostic accuracy.
- real API-cost proof.
- production proxy readiness.

The rewrite uses bounded language tied to current examples and evidence:

- KORA helps make AI workloads routable and controllable.
- KORA examples identify deterministic candidates and provider-needed candidates in bundled offline sample workloads.
- KORA examples execute deterministic sample tasks through KORA `TaskGraph` paths.
- KORA examples preserve provider-needed fallback cases while making zero provider calls.

## Validation

Validation commands and results:

```bash
python3 -m kora examples list
```

Result: passed. The output includes `deterministic_classification` and `kora_doctor`.

```bash
python3 examples/kora_doctor/run.py
python3 examples/kora_doctor/run.py --all
python3 examples/deterministic_classification/run.py
```

Result: passed for Doctor single-workload mode, Doctor report-pack mode, and deterministic classification example execution.

```bash
python3 -m pytest tests/test_first_value_cli.py tests/test_kora_doctor_example.py tests/test_kora_doctor_report_pack.py tests/test_deterministic_classification_expansion_pack.py
```

Result: passed, `35 passed`.

```bash
python3 scripts/check_markdown_links_goal082b.py
```

Result: passed, `Goal 082B markdown links OK`.

## Residual Risk

The biggest risk is over-reading examples as production diagnostics or cost proof. The README, docs index, and vision document explicitly label current examples as offline, synthetic, and bounded.
