# Task 024 — Three-system execution harness

Classification: **needs-cto-review**. The implementation is reviewable; the
three-system live acceptance gate remains **blocked on native model availability**.
Base: `88540fd11a0f5eacc965a5c9872d3d659fd3edc7`.
An open PR is not merge approval or sprint completion.

## Problem and change

The offline node runtime cannot truthfully describe real inference or remote worker
activity. Add an opt-in benchmark harness with independent versioned worker, event
and execution records. The existing offline Solution contracts are unchanged.
A fixed benchmark client dispatches arithmetic and model nodes to authenticated
loopback workers over SSH tunnels. Inference uses persistent local servers.
The native comparison endpoint is contacted directly, without a KORA worker or
KORA routing/reuse/deflection on that server.

This is a bounded harness, not general Host registry integration, durable execution,
model sharding, pooled memory, exact reuse or a production network service.
No workflow-specific code is added to Core.

## Validation

- Full regression during implementation: 723 passed.
- Focused transport/state/integration tests: 18 passed.
- Isolated non-editable source installation: passed.
- Offline release smoke: passed; no release performed.
- Ruff: passed after import, exception type and formatting repairs.
- Negative coverage: authentication, frame/body bounds, changed request IDs, in-flight
  duplicates, incarnation mismatch, full ledger, failure retention/quarantine,
  model mismatch, missing usage, invalid outputs and distinct cluster workers.
- Mocked model tests are labelled as such; live evidence is separate.

## Live acceptance, bounded synthetic fixtures

Pinned Qwen3-30B-A3B Q4_K_M file and upstream tokenizer hashes verified.
The GGUF embedded template differs from the pinned upstream template.
Both local servers explicitly use upstream template SHA-256
`a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8`.
The original GGUF file remains unchanged. This does not prove cross-engine tokenizer
equivalence; the controlled native comparison still needs validation.

| Scenario | Single machine | Two-worker set | Native endpoint |
| --- | --- | --- | --- |
| D, six cases | 6/6, zero model completions | 6/6, deterministic worker only | Client-only arithmetic; no GPU measurement |
| M, six cases × five | 30/30 fixture quality | 30/30 fixture quality, model worker only | 30 model-mismatch failures |
| W, six cases × five | 30/30 fixture quality | 30/30, both workers observed | 30 model-mismatch failures |

Each successful M/W row reports one actual completion and ten engine-reported output
tokens. Input hashes agree across systems per case. Three ready warmups per case
were retained separately for each local set. Two earlier single-machine warmup
connection failures occurred before worker readiness; they remain in the private
diagnostic record. Launch procedures were corrected to wait for authenticated health.

The two-worker topology has a common client coordinating both worker machines.
It is not a direct peer-to-peer Ethernet throughput measurement. Timings include
client and transport overhead; the short classification fixture is not a heavy
generation throughput benchmark. No H100 parity, general quality, cost, energy,
low-memory optimization gain or broad workload claim follows from these results.

## Native endpoint blocker

The existing native endpoint serves a different model and occupies most GPU memory.
The adapter fails before generation rather than substituting that model.
Its service remains running. A dedicated window is required to run the pinned
native model, verify template/generation/cache settings, warm up, collect all
outcomes and restore the original service. No service stop is included in this change.

## Review and scope boundaries

Implementation/review passes: initial protocol, transport hardening, live acceptance,
final lint/report. Repairs included explicit native-client-only labelling, failed
quality token accounting, worker readiness, upstream template selection, relocated
dynamic-library lookup, model-failure quarantine and malformed response handling.

Allowed changes: new benchmark modules/tests, example configuration and bounded
documentation. No existing Solution/Core implementation is altered.
No credentials, private endpoint addresses, personal data, model weights or raw
host logs are committed. Local model execution and trusted-network testing were
authorized for this task. No external provider inference, native-service stop,
merge, release, repository settings or public performance expansion occurred.

## Next gate

Review the code and its experimental contract. Complete matched native execution
during an explicitly allocated service window; then rerun acceptance and update
the sprint status. UI, exact reuse and broader comparative evidence remain later
work. See [execution guide](../benchmark-three-system-execution.md).
