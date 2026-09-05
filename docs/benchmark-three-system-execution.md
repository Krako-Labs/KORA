# Three-system execution harness (experimental v1)

This opt-in harness connects fixed benchmark workers; it does not register remote or
model runtimes in the offline Solution Host. Existing false-only activity contracts
remain unchanged. Business-specific arithmetic/classification fixtures live in
`kora.benchmarks`, outside Core. This is not a general remote execution service.

## Topology and responsibilities

| System | Deterministic fixture | Inference | Control |
| --- | --- | --- | --- |
| Single machine | Local worker | Persistent local model server | Explicit benchmark node dispatch |
| Two-machine cluster | Second worker | First worker's persistent model server | Fixed task distribution |
| Native baseline | Common client arithmetic | Direct native model endpoint | No KORA routing/reuse/deflection |

A D-only native-baseline result is labelled **h100-client-only**. It is not a GPU or
server benchmark. M-only does not exercise both cluster workers. Only a successful
W run with two distinct worker identities sets `cluster_cooperation_observed`.
Worker identity is an operator declaration authenticated by the shared secret and
SSH host trust, not hardware attestation. Capture separate host/process evidence.
No model sharding, memory pooling or H100 parity is claimed.

## Start a worker

Install the repository using Python 3.10 or newer. Generate a random secret with at
least 32 characters and deliver it privately to the trusted workers. Set
`KORA_BENCHMARK_TOKEN` without placing its value in command history or public files.

Worker configuration:

```json
{
  "worker_id": "worker-b",
  "port": 9182
}
```

Run `python -m kora.benchmarks.worker --config worker.json`.
A worker always binds 127.0.0.1. For remote access, establish a verified SSH tunnel,
for example `ssh -N -L 127.0.0.1:9282:127.0.0.1:9182 trusted-worker`.
Do not expose the worker port directly to a LAN or the Internet.

To enable inference, add a `backend` object with `url`, `model`, `generation`,
`identity`, and optionally `timeout` (seconds, default 120), `token`, or `token_env`.
Prefer `token_env` so credentials stay out of configuration files.
The endpoint must be loopback or an SSH tunnel. The separately launched persistent
model server owns model loading; this worker never reloads a model per request.
Record server PID, startup-to-ready time and artifact hashes separately.
Worker health reports its own uptime and capabilities, not model readiness.
The adapter checks the served model ID before each inference. This is not sufficient
to prove weights, tokenizer or template; verify those artifacts before measurement.
No automatic model substitution or download occurs in this harness.

## Request, status and retries

`GET /health` and `POST /jobs` require Bearer authentication.
Requests have exactly `schema_version: kora.benchmark.worker/v1`, `boot_id`,
`job_id`, `operation`, `input`, and SHA-256 `input_hash`.
Hash encoding is sorted compact UTF-8 JSON with non-ASCII preserved and no NaN.

Limits: 64 KiB request/response read, eight HTTP handler threads, one active operation,
1024 retained job outcomes per worker incarnation. Socket/header reads time out
after five seconds. Model socket inactivity timeout defaults to 120 seconds; this is not a process-level
absolute execution deadline.
Only fixed arithmetic and configured model operations exist; callers cannot submit
commands, endpoint URLs, files or arbitrary capabilities.

Same ID + identical request returns the original outcome with
`duplicate_delivery: true`; it does not rerun inference.
Same ID + different request fails 409. An in-flight duplicate fails 409.
A full ledger fails 503 without evicting deduplication records.
After worker restart, old `boot_id` fails 409. Retained outcomes are in memory,
not crash-durable; do not retry with a fresh ID after an uncertain timeout.
Exactly-once execution across process failure is not claimed.

A failed model HTTP call can leave native inference running. The worker retains
`unknown-or-not-started` rather than falsely recording that no computation happened.
No backend cancellation or automatic retry is promised. Resolve native server health
before restarting the worker. Model failures quarantine new model jobs with
\`model-recovery-required\`; deterministic operations remain available. Only successful completions with engine usage fields
increment `model_calls_completed`; unknown failures remain explicitly failed.
Duplicate-delivery responses refer to original execution timing, not a new execution.

## Three-system CLI

`python -m kora.benchmarks.three_system --config systems.json --fixtures workloads.json --output new-run-directory --scenario W --repetitions 5`

Configuration contains `mp`, `cluster`, and `h100`.
The first two contain `token_env`, `model_worker`, `deterministic_worker`, and
`identity`. Worker references contain `url` and `worker_id`.
H100 contains `backend` as above and `identity`; it does not run a KORA worker.
Use the pinned comparison plan in `examples/benchmarks/three-environment/`.
The CLI does not provision or stop an existing native server.

Outputs:
- `events.jsonl`: `kora.benchmark.event/v1`, per-run sequence, start/node/finish events.
- `results.jsonl`: `kora.benchmark.execution/v1`, input hash, configuration,
  node evidence, actual engine tokens, fixture quality and controller elapsed time.
- TSV terminal table. Exit status is nonzero when any result fails its quality gate.

Runs are sequential and concurrency is one. Controller elapsed time includes
transport/health calls; node time and load time are separate. No clock synchronization
is assumed. Events indicate lifecycle; this version does not stream individual tokens.
TTFT, GPU memory, energy and prefill/decode speed are not inferred from total time.
Warmups must be executed into a separate output directory before measured repetitions.
Unknown cases fail before creating output. Failed rows remain in the result set.

Quality parses the whole response as JSON, requires exactly `category`, and checks the
frozen expected fixture output. No prose stripping or semantic judging is performed.
These fixtures do not establish general model quality. D, M and W are supported;
bounded exact reuse and a live comparison UI belong to later work.

## Validation boundary

Unit tests use mocked model responses explicitly; they prove transport/state handling,
not inference performance. Real measurements require verified artifacts and separate
live evidence. A model mismatch or unavailable H100 slot is a blocker, not a successful
three-system benchmark. Preserve active native services and obtain a benchmark slot.
