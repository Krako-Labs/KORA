# Provider Routing Matrix

Status: dry-run planning matrix. No real provider calls are enabled.

| Route | Current dry-run status | Future activation requirement | Current evidence level |
|---|---|---|---|
| `deterministic` | Ready for synthetic dry run | Keep deterministic resolver tests passing | Existing simulated invocation accounting plus dry-run routing |
| `cache` | Ready for synthetic dry run | Define cache key, invalidation, hit accounting, and replay policy | Synthetic route only |
| `local_small_model` | Planned, blocked | Approved local model, disk policy, dependency plan, and no-large-download review | Synthetic route only |
| `local_h100_model` | Planned, blocked | Formal H100 access, environment smoke test, model/runtime approval, cost and artifact policy | Synthetic route only |
| `aws_model` | Planned, blocked | AWS account/resource allocation, credentials, quota, budget, data policy, smoke test | Synthetic route only |
| `azure_model` | Planned, blocked | Azure resource allocation, credentials, quota, budget, data policy, smoke test | Synthetic route only |
| `openai_api` | Planned, blocked | OpenAI API credential, model/version selection, quota, budget, smoke test | Synthetic route only |
| `claude_api` | Planned, blocked | Claude API credential, model/version selection, quota, budget, smoke test | Synthetic route only |
| `gemini_api` | Planned, blocked | Gemini API credential, model/version selection, quota, budget, smoke test | Synthetic route only |

## Routing Principles

- Prefer deterministic execution when the task can be resolved without model inference.
- Prefer cache only when a replay-safe cache key and response provenance are available.
- Use local small model routes only after model acquisition and dependency policy are approved.
- Use H100 routes only after Task 522 confirms formal access and environment readiness.
- Use cloud/API routes only after Task 523 confirms credentials, quota, budget, model IDs, and data handling policy.
- Keep provider selection explainable in the emitted benchmark record.
- Keep dry-run and real-run outputs visibly separated.

## Required Accounting Fields For Future Real Runs

Future real benchmark outputs should include:

- route selected
- provider family
- model identifier and version where applicable
- deterministic/cache bypass reason where applicable
- real call attempted flag
- request token estimate or provider token accounting where applicable
- latency
- status code or provider error class where applicable
- cost estimate source
- retry count
- cache hit/miss state
- benchmark run ID
- workload version

These fields are not populated with real values in the current dry-run harness.
