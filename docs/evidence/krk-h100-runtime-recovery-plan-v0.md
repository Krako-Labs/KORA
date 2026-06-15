# KRK H100 Runtime Recovery Plan v0

Status: public-safe runtime diagnosis and recovery plan.

## Purpose

This plan diagnoses the KRK H100 evidence runtime gap after Goal 050 and Goal 055.

It answers:

- Goal 050 succeeded with bounded H100 evidence.
- Goal 055 prepared expanded H100 evidence but did not run it.
- Goal 057 diagnosed local runtime availability and identified a public-safe recovery path.

This plan does not run H100 workloads and does not add expanded H100 measurements.

## Goal 050 Measured Evidence Summary

Goal 050 added public-safe bounded H100 evidence for the KRK-selected GPU subset from the public matrix fixtures.

| Metric | Value |
| --- | ---: |
| Subset count | 4 |
| Total compute weight | 58 |
| Runtime seconds | 0.035312 |
| Throughput, requests/second | 113.277481 |
| Throughput, compute weight/second | 1642.523477 |
| Bounded workload peak allocation MB | 240.000 |
| CUDA context memory used before MB | 525.062 |
| CUDA context memory used after MB | 525.062 |

Evidence files:

- [KRK bounded H100 evaluation v0](krk-bounded-h100-evaluation-v0.md)
- [Generated H100 bounded JSON summary](generated/krk-h100-bounded-summary-v0.json)
- [Generated H100 bounded Markdown summary](generated/krk-h100-bounded-summary-v0.md)

Confirmed public facts:

- The measured subset had 4 public fixture-derived GPU-routed items.
- The summary records bounded CUDA execution and sanitized runtime, throughput, and memory metrics.
- Raw GPU logs and private infrastructure details were not committed.

Current public limitation:

- The public repo contains the sanitized Goal 050 summaries, but it does not contain the private raw command log, raw GPU logs, or a reusable H100 execution runner for that measurement.

## Goal 055 Not-Run Summary

Goal 055 prepared expanded bounded H100 evidence, but did not run it.

| Metric | Value |
| --- | --- |
| Claim level | `expanded_h100_validation_not_run` |
| Subset count | 0 |
| Success count | 0 |
| Failure count | 0 |
| Blocker | Safe CUDA/H100 runtime was not available in the current execution environment. |

Evidence files:

- [KRK expanded bounded H100 evaluation v0](krk-expanded-bounded-h100-evaluation-v0.md)
- [Generated expanded H100 bounded JSON summary](generated/krk-expanded-h100-bounded-summary-v0.json)
- [Generated expanded H100 bounded Markdown summary](generated/krk-expanded-h100-bounded-summary-v0.md)

Goal 055 does not add expanded H100 runtime, throughput, or memory evidence.

## Confirmed Runtime Checks

Goal 057 safe local runtime checks showed:

| Check | Result |
| --- | --- |
| `python3 --version` | Python 3.13.5 |
| `python3 -c "import torch; print(torch.cuda.is_available())"` | `False` |
| `nvidia-smi` | unavailable in the local environment |
| `python3 -m pytest` | 321 passed |

Interpretation: the current local worktree environment can run tests and dry-run evaluators, but cannot execute CUDA/H100 workloads.

Goal 057 also checked private H100 access through local-only configuration. Public-safe summary:

- private H100 shell/GPU-inspection access is available through local-only configuration.
- GPU inspection is available in that private environment.
- the checked default Python runtime does not yet have CUDA-capable Torch available.
- exact access details are recorded only in the local-only operational note and are not committed.

## Root-Cause Hypotheses

Confirmed root cause for Goal 055:

- Goal 055 ran from the local worktree environment, which has no CUDA-visible runtime and no `nvidia-smi`.

Likely contributing causes:

- Goal 050 measurement was produced from a private H100-capable environment and committed as sanitized summaries.
- The private Goal 050 raw command path was intentionally not committed.
- No public reusable H100 runner exists in this branch.
- The currently reachable private H100 environment needs a CUDA-capable Python measurement environment prepared before expanded evidence can run.

## Recovery Plan

1. Keep public repo outputs sanitized.
2. Use the public matrix/runtime fixtures to select GPU-routed source items:
   - `cache-003`
   - `gpu-001`
   - `gpu-002`
   - `mixed-004`
3. In a private H100-capable environment, prepare a bounded Python runtime with CUDA-capable Torch.
4. Confirm:
   - `nvidia-smi` is available.
   - `torch.cuda.is_available()` is `True`.
   - visible GPU count is nonzero.
5. Generate 20 to 50 fixture-derived bounded synthetic GPU-routed operations.
6. Run only bounded tensor operations.
7. Write raw logs and operational notes outside the public repo.
8. Commit only sanitized JSON and Markdown summaries.
9. Validate JSON, tests, whitespace, and public/private scans before commit.

## Public-Safe Command Template

Run this only inside a private H100-capable environment after access and runtime readiness are confirmed:

```bash
python3 --version
nvidia-smi
python3 - <<'PY'
import torch
print(torch.cuda.is_available())
print(torch.cuda.device_count())
PY

python3 -m pytest
jq empty docs/evidence/generated/krk-h100-bounded-summary-v0.json
jq empty docs/evidence/generated/krk-expanded-h100-bounded-summary-v0.json
```

The measurement command should write only sanitized outputs to:

```text
docs/evidence/generated/krk-expanded-h100-bounded-summary-v0.json
docs/evidence/generated/krk-expanded-h100-bounded-summary-v0.md
docs/evidence/krk-expanded-bounded-h100-evaluation-v0.md
```

## Public/Private Boundary

Public docs may include:

- subset count.
- success/failure count.
- runtime seconds.
- throughput summary.
- bounded allocation summary.
- generic execution mode.
- claim boundary.
- `raw_logs_committed: false`.
- `private_infrastructure_details_committed: false`.

Public docs must not include:

- raw GPU logs.
- hostnames.
- IP addresses.
- usernames.
- SSH details.
- private paths.
- device serials.
- cloud/account details.
- billing details.
- provider credentials.
- operational access notes.

## Claim Boundary

Allowed:

- Goal 050 bounded H100 evidence exists.
- Goal 055 expanded H100 was prepared but not measured.
- Goal 057 diagnoses runtime availability and the recovery path.

Not allowed:

- expanded H100 evidence exists.
- production savings.
- 10x savings.
- H100 superiority.
- GPU superiority.
- infrastructure savings.
- production readiness.

## Next Task Recommendation

Proceed to Goal 058: Expanded H100 Evidence Execution.

Goal 058 should prepare a CUDA-capable private H100 Python runtime, run the bounded expanded subset if safe, and commit only public-safe aggregate summaries.
