# Three-environment preparation fixtures

These files freeze configuration intent and synthetic inputs. They do not launch
a model or establish working hardware compatibility.

- `comparison-plan.json`: one common model, immutable upstream/GGUF identities,
  local Metal backend, native H100 BF16 serving baseline, supplementary same-GGUF
  CUDA control, and fixed generation/measurement settings.
- `workloads.json`: six synthetic English/Korean support requests with expected
  labels and arithmetic results. These are deliberately small protocol fixtures,
  not a representative benchmark corpus.

The primary H100 baseline uses native serving without KORA execution control.
Its BF16 versus local Q4_K_M comparison is a **configuration/work-outcome**
comparison, not hardware-only speed evidence. The supplementary same-artifact
control has its own label and does not replace the native baseline.

Model weights have not been downloaded or executed by this preparation task.
Upstream API digests must be checked against downloaded bytes during provisioning.
The pinned source revision is not proof of a successful Metal/CUDA build.
Use the model's pinned chat template with thinking disabled and record rendered
prompt/tokenizer identities. The runtime adapter must translate every generation
setting explicitly; unsupported parameters cannot be silently dropped.

## Work and quality

D uses the existing typed-node normalization fixture. M classifies each request.
W adds input validation, integer multiplication and a combined output. Ordinary
deterministic preprocessing is permitted on every baseline. Classification is
not a proof that a model is necessary: a competent rules baseline is permitted
and must be disclosed if evaluated.

M accepts only a whole JSON response equal to the expected one-key object.
W additionally requires exact total and currency. Do not strip prose or repair
invalid model output during grading. Five measured repetitions per case must
all pass the fixture gate. Report failures and timeouts; do not improve the
rubric after viewing model answers without issuing a new fixture version.
These are prospective acceptance criteria, not measured quality claims.

Repeat and changed-input arms are separate. In the changed arm both quantity and
text change; an old combined result must miss. A correctly keyed, field-specific
subresult may still reuse unchanged data. Disable reuse for inference control.

## Event contract for subsequent implementation

The subsequent streaming adapter should use a separately versioned envelope:
run_id, system_set, sequence, event_kind, node_id (nullable), monotonic_elapsed_ms,
runtime_identity, and activity. Event kinds are accepted, node_started,
node_completed, node_failed, run_completed, run_failed and timed_out.
The controller owns elapsed time from submission. Each server owns its own
monotonic stage durations; never subtract unsynchronized host clocks.
Terminal failures are retained and sequence gaps explicitly diagnosed.

This event list is a design contract only. The implemented artifact in this
change remains `kora.node-evidence/v1`; no live event emitter is claimed.
The future model path requires new truthful activity/status contracts because
the current reference Host's activity fields are bounded to offline execution.

## Exit checks before performance collection

Verify runtime build and artifact hashes, available GPU memory, identical fixture
digests, rendered prompt settings, observed network path, cache conditions, and
repetition/timing policy. Record link changes and recollect communication-sensitive
measurements after a network change. One cluster model replica plus a deterministic
worker means task distribution, not combined model memory or tensor parallelism.
No extra capacity candidate is required in this scope.
