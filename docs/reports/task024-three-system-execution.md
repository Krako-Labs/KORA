# Task 024 — Three-system execution harness

Classification: **needs-cto-review**. The implementation is reviewable; the
three-system live acceptance gate has **passed the bounded M/W fixtures** after an
authorized native service window and verified restoration.
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

- Full regression after the operations addition: 725 passed (including two lease tests).
- Focused transport/state/integration tests: 18 passed.
- Isolated non-editable source installation: passed.
- Offline release smoke: passed; no release performed.
- Ruff: passed after import, exception type and formatting repairs.
- Negative coverage: authentication, frame/body bounds, changed request IDs, in-flight
  duplicates, incarnation mismatch, full ledger, failure retention/quarantine,
  model mismatch, missing usage, invalid outputs and distinct cluster workers.
- Mocked model tests are labelled as such; live evidence is separate.

## Initial local acceptance (historical, before native service window)

Pinned Qwen3-30B-A3B Q4_K_M file and upstream tokenizer hashes verified.
The GGUF embedded template differs from the pinned upstream template.
Both local servers explicitly use upstream template SHA-256
`a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8`.
The original GGUF file remains unchanged. This does not prove cross-engine tokenizer
equivalence. Subsequent bounded native acceptance is recorded below.

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

## Initial native endpoint blocker (resolved)

The original endpoint served a different model and occupied most GPU memory.
The adapter rejected it before generation. This initial blocker was resolved by
the subsequently authorized temporary window and verified restoration below.

## Review and scope boundaries

Implementation/review passes: initial protocol, transport hardening, live acceptance,
final lint/report. Repairs included explicit native-client-only labelling, failed
quality token accounting, worker readiness, upstream template selection, relocated
dynamic-library lookup, model-failure quarantine and malformed response handling.

Allowed changes: new benchmark modules/tests, example configuration and bounded
documentation. No existing Solution/Core implementation is altered.
No credentials, private endpoint addresses, personal data, model weights or raw
host logs are committed. Local model execution and trusted-network testing were
authorized for this task, including the temporary native-service handover.
No external provider inference, merge, release, repository settings or public
performance expansion occurred.

## Next gate

Review the code, shared-resource helper and bounded native acceptance. The native
execution gate is complete; merge remains separately unapproved. UI, exact reuse and broader comparative evidence remain later
work. See [execution guide](../benchmark-three-system-execution.md).


## Authorized native acceptance and shared usage board

The native endpoint was run in an explicit temporary service window. Existing
service requests were checked before handover. Systemd time limits and an exit
restoration action protected the borrowed service. Initial launches exposed missing
CUDA/ninja PATH entries; the already-installed runtime paths were applied to the
new process only. A readiness preflight also rejected an attempt while the original
service was still restarting. Those failures are retained, not hidden.

Six cases, three warmups per case per local/native set (54/54 passed),
then five repetitions per case:

| Scenario | Single machine | Two-worker set | Native H100 |
| --- | --- | --- | --- |
| M | 30/30 exact fixture passes | 30/30 | 30/30 |
| W | 30/30 exact fixture passes | 30/30, both workers observed | 30/30 |

Each set/scenario has 30 actual model completions and 300 actual output tokens.
Input hashes agree. The original service was restored and its health/model verified.
The resource lease was released after verification. Native BF16 and local Q4_K_M
remain different configurations, so this is not a hardware-only comparison.

Median controller milliseconds: M single361.71 / worker set472.52 / native218.14;
W single350.65 / cluster520.70 / native280.83. These very short, synthetic
classification fixtures establish execution connectivity and exact fixture output,
not heavy generation throughput, broad quality, H100 parity or cost advantage.

User-authorized operations addition: standalone scripts/gpu_lease.py, focused tests
and docs/shared-gpu-leases.md. Atomic cooperative leases record project, owner,
purpose, expected end, heartbeat, actual observed memory/PID/cgroup and elapsed
reservation time. Conflicts and stale leases fail closed; the utility never kills
another workload. Existing shared services can be labelled separately from leases.
This remains a cooperative convention, not compulsory GPU isolation or a scheduler.
No credentials, raw private host logs or project-specific service controls are public.
