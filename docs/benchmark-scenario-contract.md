# Three-environment benchmark contract — preparation only

The intended comparison is a standalone local KORA system, a two-node local
KORA cluster treated as one system, and an H100 native serving baseline without
KORA execution control. A shared measurement interface may launch and observe
the baseline; it must not silently route baseline work through KORA.

Only scenario D below has an executable local collector in this change.
M and W are specifications, not performance evidence or implemented backends.

| Scenario | Work and quality gate | Primary measurements | Status |
|---|---|---|---|
| D: deterministic | Normalize a fixed text fixture and forward typed output; exact expected JSON equality | End-to-end completion time, successful nodes, zero model calls | Local fixture executable |
| M: model inference | Fixed versioned prompt corpus, pinned common model and output budget; validity and task-specific answer rubric fixed before measurement | Quality-pass completion time, actual input/output tokens, TTFT, prefill/decode timing where measured | Planned |
| W: mixed workflow and repeated input | Fixed parse/validate/normalize stages plus required generation; same output rubric on every system; repeat identical and changed inputs | Quality-pass jobs, total completion time, deterministic stages, actual model calls, exact reuse hits and misses | Planned |

## Fair comparisons

Use identical workload input digests and acceptance criteria. The native baseline
may use ordinary deterministic preprocessing and normal runtime optimizations.
Do not construct an all-model baseline for operations that are naturally
deterministic. Hardware-native runtime choices must be disclosed.

Separate two experiments: (1) inference performance with matched model revision,
tokenizer, prompt, generation settings and comparable quantization; (2) workflow
performance with equal work and quality but potentially fewer KORA model calls.
If quantization or model revisions differ, label the result as a configuration
comparison rather than a controlled hardware-only comparison.

On the same local hardware, compare the pipeline with call-reduction and reuse
disabled/enabled to isolate their effect from inference/cache optimizations.
No fictitious “equivalent tokens” may be added to actual generated-token counts.
For deterministic work report jobs and completion time, not token throughput.

## Run record required before M/W execution

Record code revision, workload/input digest, model and tokenizer revisions,
artifact digests and quantization, runtime versions and settings, seed and
sampling parameters, output limits, concurrency, warm-up policy, timed scope,
cold/warm model state, prefix/KV/result cache states, machine/OS/RAM/GPU inventory,
cluster topology and measured link conditions, and other active workloads.

Report raw run records, repetition count, failures/timeouts, quality pass rate,
median and p95 with their sample count. Never discard failed or slow runs
silently. Fix the repetition count and quality rubric before collecting results.
Client elapsed time must be identified separately from server inference time;
remote timestamps need synchronized clocks before cross-host stage subtraction.
Record unavailable counters as null.

Cluster task distribution and model-level sharding are different capabilities.
Two hosts' RAM is not automatically one model's available memory.
Record per-node resource use and cluster-total completed jobs.
Live execution and recorded playback must be visibly distinct.

No H100-equivalent quality, speed, cost, or capacity claim follows from this
contract or the small deterministic fixture. Such claims require matched,
measured results and a clearly stated workload/configuration scope.
