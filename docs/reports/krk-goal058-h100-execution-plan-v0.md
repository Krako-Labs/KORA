# KRK Goal 058 H100 Execution Plan v0

Status: public-safe execution plan for the next H100 evidence task.

## Objective

Generate expanded bounded H100 routed-subset evidence for KRK if a safe CUDA/H100 runtime is available.

This objective is public-safe and bounded. It is not a raw H100 benchmark, production benchmark, production savings claim, infrastructure savings claim, H100 superiority claim, GPU superiority claim, or broad workload superiority claim.

## Target Evidence

Target claim level if run:

`expanded_bounded_h100_routed_subset_measured`

Target claim level if not run:

`expanded_h100_validation_not_run`

Target sample:

- 20 to 50 bounded synthetic GPU-routed operations.
- generated from public-safe fixture metadata.
- derived from the current public GPU-routed source items:
  - `cache-003`
  - `gpu-001`
  - `gpu-002`
  - `mixed-004`

## Expected Inputs

Public inputs:

- `examples/workloads/krk-mixed-routing-matrix-alpha.json`
- `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-adversarial-routing-matrix-alpha.json`
- `docs/evidence/generated/krk-h100-bounded-summary-v0.json`
- `docs/evidence/generated/krk-expanded-h100-bounded-summary-v0.json`
- `docs/evidence/krk-h100-runtime-recovery-plan-v0.md`

Private inputs:

- private H100 runtime access.
- CUDA-capable Python environment.
- raw runtime logs stored outside the public repo.

## Expected Outputs

If run, update:

- `docs/evidence/krk-expanded-bounded-h100-evaluation-v0.md`
- `docs/evidence/generated/krk-expanded-h100-bounded-summary-v0.json`
- `docs/evidence/generated/krk-expanded-h100-bounded-summary-v0.md`

If not run, keep the output status as not run and update the blocker clearly.

The public JSON summary should include:

```json
{
  "claim_level": "expanded_bounded_h100_routed_subset_measured",
  "subset_count": 0,
  "execution_mode": "bounded_h100",
  "success_count": 0,
  "failure_count": 0,
  "runtime_seconds": 0,
  "throughput_requests_per_second": 0,
  "throughput_compute_weight_per_second": 0,
  "memory": {
    "peak_bounded_allocation_mb": 0,
    "cuda_context_before_mb": 0,
    "cuda_context_after_mb": 0
  },
  "raw_logs_committed": false,
  "private_infrastructure_details_committed": false
}
```

Use real measured values only after a bounded run completes. Do not commit placeholder measured values.

## Execution Sequence

Run inside a private H100-capable environment:

```bash
python3 --version
nvidia-smi
python3 - <<'PY'
import torch
print(torch.cuda.is_available())
print(torch.cuda.device_count())
PY
```

Stop if CUDA is unavailable.

If CUDA is available:

```bash
python3 -m pytest
jq empty docs/evidence/generated/krk-h100-bounded-summary-v0.json
jq empty docs/evidence/generated/krk-expanded-h100-bounded-summary-v0.json
```

Then run the bounded expanded measurement task and write only sanitized outputs to the public repo.

## Validation Commands

After generating public outputs:

```bash
python3 -m pytest
git diff --check
jq empty docs/evidence/generated/krk-h100-bounded-summary-v0.json
jq empty docs/evidence/generated/krk-expanded-h100-bounded-summary-v0.json
```

Also run the standard public/private scan set for project boundary terms, local-only paths, operational tooling references, secrets, credentials, and unsupported positive claims. Treat known pre-existing matches separately from Goal 058 changes.

## Stop Conditions

Stop and write a not-run summary if:

- private H100 access is unavailable.
- `nvidia-smi` is unavailable.
- CUDA-capable Torch is unavailable.
- a safe bounded runtime cannot be prepared.
- the run would exceed 50 bounded synthetic operations.
- raw logs or private infrastructure details would enter public outputs.
- any command would require provider credentials, account details, or billing data.
- validation fails and cannot be fixed without broadening scope.

## Public Summary Requirements

The public summary must state:

- whether expanded H100 execution was run.
- subset count.
- success/failure counts.
- sanitized runtime, throughput, and memory metrics if measured.
- that raw logs were not committed.
- that private infrastructure details were not committed.
- claim level.
- limitations.

The public summary must not state:

- production savings.
- 10x savings.
- customer savings.
- infrastructure savings.
- H100 superiority.
- GPU superiority.
- production readiness.
- broad workload superiority.
