# KORA status closeout Report — Validation Workstream

## Date

2026-05-09

## Public repo

https://github.com/Krako-Labs/KORA

## Public HEAD

`7657ddb6ad153ea28c222a4b13b8cefc5d7f54d3`

## Private internals repo

https://github.com/Krako-Labs/internals

## Internals HEAD

`869216eb7dd34bf8f50750d2348f3d6508e5108b`

## GitHub CLI identity

`gh auth status` confirmed the active GitHub CLI account as `hkalbertkim`.

## Summary

The validation workstream moved KORA from deterministic-heavy alpha benchmark evidence toward a safer, reviewer-facing validation path for measured model-call routing. The public repository now includes local/no-network validation examples, customer-support triage synthetic workload materials, Markdown validation reports, a reviewer packet, local model adapter design, adapter selection, and a blocked local runtime adapter skeleton.

This work remains claim-safe. It does not implement real provider calls, real local runtime calls, production validation, or real API-cost evidence.

## Completed public PRs/tasks

- Public/private messaging split and claim boundary cleanup.
- README image system finalized with PNG displayed diagrams and preserved SVG sources.
- Real model-call validation design docs added.
- Provider-neutral model-call adapter interface added.
- Deterministic local validation adapter added.
- Blocked adapter added.
- Model-call summary helper added.
- Local/no-network validation examples added.
- Customer-support triage synthetic workload spec added.
- Customer-support triage local validation path added.
- Markdown validation report generator added.
- Reviewer-facing local validation packet added.
- Local model adapter design added.
- Adapter selection skeleton added.
- Blocked local runtime adapter skeleton added.

## Completed private internals work

- Internals repository structure and detailed internal operations docs were added.
- Internal claim tracker was updated for the real model-call validation workstream.
- Internal messaging notes now preserve the public/private boundary.

## Current public README/image state

The README displays PNG diagrams:

- `docs/assets/kora-execution-control-overview.png`
- `docs/assets/kora-benchmark-evidence-card.png`
- `docs/assets/kora-validation-roadmap.png`
- `docs/assets/kora-help-test-flow.png`

SVG source/reference files remain preserved in `docs/assets/`.

## Current validation capability

KORA can run local/no-network validation examples that measure avoided model-call events in synthetic workloads:

- `python3 -m kora run real_model_call_validation_fake -- --offline`
- `python3 -m kora run customer_support_triage_fake_validation -- --offline`

Customer-support local validation counters:

- `total_requests`: 12
- `baseline_model_calls`: 12
- `kora_model_calls`: 4
- `avoided_model_calls`: 8
- `avoided_model_call_rate`: 0.6667
- `deterministic_routes`: 8
- `model_escalations`: 4

## Current adapter capability

The model-call adapter layer includes:

- `ModelCallRequest`
- `ModelCallResponse`
- `ModelCallAdapter`
- deterministic local validation adapter
- blocked adapter
- model-call summary helper
- adapter selection for `local_validation`, `blocked`, and `local_runtime_placeholder`
- blocked local runtime adapter skeleton for future local runtime work

The blocked local runtime adapter skeleton fails closed and does not call Ollama, llama.cpp, vLLM, HTTP endpoints, subprocess runtimes, remote providers, or other external runtimes.

## Current reviewer packet/report capability

KORA can generate local Markdown validation reports from aggregate counters:

```bash
python3 -m kora run customer_support_triage_fake_validation -- --offline --report-md /tmp/kora_customer_support_validation.md
python3 -m kora run real_model_call_validation_fake -- --offline --report-md /tmp/kora_local_validation.md
```

Reviewer guidance is available at:

- `docs/benchmarks/local-validation-reviewer-packet.md`
- `docs/benchmarks/real-model-call-validation-report-template.md`

Generated reports should remain local unless intentionally reviewed. They should not include secrets, raw provider responses, private data, or production data.

## Current safe public claim

KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

## Explicit non-claims

- No production cost reduction proof.
- No real API-cost reduction proof.
- No production benchmark proof.
- No full runtime-integrated real-provider benchmark evidence.
- No broad workload superiority proof.
- No energy reduction evidence.
- No formal government validation.
- No signed partner validation unless actually signed and documented.
- No guaranteed adoption or funding.

## Validation commands

```bash
python3 -m pytest
python3 -m kora --help
python3 -m kora examples list
python3 -m kora run real_model_call_validation_fake -- --offline
python3 -m kora run customer_support_triage_fake_validation -- --offline
python3 -m kora run customer_support_triage_fake_validation -- --offline --report-md /tmp/kora_customer_support_validation.md
python3 -m kora run direct_vs_kora -- --offline
python3 -m kora run runtime_integrated_benchmark -- --offline
```

## Remaining TODOs

- Krako 2.0: TBD.
- Canonical GitHub Discussions/contact route TODO.
- Decide next technical path:
  1. explicit adapter-selection CLI option
  2. first concrete local runtime adapter behind explicit opt-in
  3. local validation report packet polish
  4. real provider adapter design only
  5. cleanup old worktrees after explicit approval

## Recommended next technical work

Implement an explicit adapter-selection CLI option for local validation examples, keeping the default local/no-network path unchanged and keeping local runtime placeholders fail-closed.

## Next Technical Work

The next public technical step is an explicit adapter-selection CLI option for local validation examples, while preserving the current local/no-network default path and fail-closed local runtime placeholders.
