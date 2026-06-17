# KRK Goal 060 Baseline Equivalence and Output Fidelity v0

Status: public-safe measured evidence.

Final classification: `BASELINE_EQUIVALENCE_OUTPUT_FIDELITY_MEASURED`

## Motivation

KRK already has evidence for route selectivity, runtime-integrated dry-run routing, provider-path validation, repo-owned bounded H100 execution, and expanded H100 representativeness. A reviewer-facing evidence package also needs an output-fidelity layer: given the same committed public workload, does KRK preserve a baseline-equivalent output contract while routing eligible execution paths?

This Goal adds that layer through a reproducible deterministic evaluator. It is designed for reviewer inspection and later paper-methods integration, not for production or savings claims.

## Methodology

The evaluator compares two deterministic public fixture-derived outputs for each workload item:

- Baseline output: the public matrix oracle expected route plus the fixture workload class and output contract.
- KRK-routed output: the route selected by the KRK dry-run policy, mapped to the same public fixture output contract.

The evaluator does not call providers, use GPU execution, inspect private logs, or use a semantic model judge. It uses only committed public matrix fixtures and deterministic rule-based comparison.

## Workload Source

The workload is the same four-profile public KRK matrix set used by route-selectivity and runtime-integrated evidence:

| Profile | Source | Items |
| --- | --- | ---: |
| mixed-realistic | `examples/workloads/krk-mixed-routing-matrix-alpha.json` | 6 |
| GPU-heavy | `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json` | 4 |
| cache-heavy | `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json` | 4 |
| adversarial | `examples/workloads/krk-adversarial-routing-matrix-alpha.json` | 4 |

Total evaluated items: `18`.

## Comparison Rules

| Category | Definition |
| --- | --- |
| `exact_match` | KRK selected the same route as the public oracle expected route, and the deterministic fixture output contract is preserved. |
| `structured_equivalent` | KRK selected a different route, but that route is listed as acceptable by the public oracle and does not violate disallowed-route constraints. |
| `semantic_equivalent_stubbed_or_rule_based` | Reserved for explicit rule-based or fixture-stubbed semantic equivalence. It remains zero in this run because no semantic model judge was used. |
| `degraded` | KRK selected a supported route that is not acceptable under the public oracle. |
| `failed` | The item could not be evaluated or produced an unsupported route. |

Acceptable output rate is computed as:

`(exact_match + structured_equivalent + semantic_equivalent_stubbed_or_rule_based) / total_evaluated_items`

## Measured Results

| Metric | Value |
| --- | ---: |
| Total evaluated items | 18 |
| Baseline success count | 18 |
| KRK success count | 18 |
| Exact match count | 17 |
| Structured equivalent count | 1 |
| Semantic equivalent count | 0 |
| Degraded count | 0 |
| Failed count | 0 |
| Exact match rate | 0.9444 |
| Acceptable output rate | 1.0000 |
| Degradation rate | 0.0000 |
| Failure rate | 0.0000 |

## Baseline vs KRK Delta

| Metric | Value |
| --- | ---: |
| Route changed count | 1 |
| Acceptable route changed count | 1 |
| Route changed degraded count | 0 |
| Baseline success minus KRK success | 0 |
| Output failures added by KRK | 0 |

The single route change is an adversarial-profile item where the baseline oracle expected `CPU` and KRK selected `provider`; the public oracle marks `provider` as acceptable for that item. This is counted as structured equivalence, not exact equivalence.

## Per-Route Fidelity

| KRK route | Total | Exact | Structured equivalent | Semantic equivalent | Degraded | Failed | Acceptable output rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| deterministic | 2 | 2 | 0 | 0 | 0 | 0 | 1.0000 |
| cache | 3 | 3 | 0 | 0 | 0 | 0 | 1.0000 |
| CPU | 2 | 2 | 0 | 0 | 0 | 0 | 1.0000 |
| provider | 3 | 2 | 1 | 0 | 0 | 0 | 1.0000 |
| GPU | 4 | 4 | 0 | 0 | 0 | 0 | 1.0000 |
| fallback | 4 | 4 | 0 | 0 | 0 | 0 | 1.0000 |

## Generated Evidence

- [Generated Goal 060 output fidelity JSON](../evidence/generated/krk-goal060-output-fidelity-summary-v0.json)
- [Generated Goal 060 output fidelity Markdown](../evidence/generated/krk-goal060-output-fidelity-summary-v0.md)

## Reproducibility

```bash
python3 scripts/run_krk_output_fidelity.py \
  --matrix examples/workloads/krk-mixed-routing-matrix-alpha.json \
  --matrix examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json \
  --matrix examples/workloads/krk-cache-heavy-routing-matrix-alpha.json \
  --matrix examples/workloads/krk-adversarial-routing-matrix-alpha.json \
  --json-out docs/evidence/generated/krk-goal060-output-fidelity-summary-v0.json \
  --md-out docs/evidence/generated/krk-goal060-output-fidelity-summary-v0.md
```

Validation:

```bash
python3 -m pytest
jq empty docs/evidence/generated/krk-goal060-output-fidelity-summary-v0.json
```

## Limitations

- This is public fixture-derived rule-based output-fidelity evidence.
- It does not evaluate free-form generated text with a semantic model judge.
- It does not execute live provider calls or live GPU/H100 workloads.
- It does not prove production output quality.
- It does not cover customer workloads or broader production traces.
- It treats public oracle acceptable routes as structured-equivalent output paths; reviewers should distinguish this from exact output equality.

## Claim Boundary

Supported:

- KRK has a reproducible baseline-equivalence and output-fidelity evaluator over the four committed public matrix profiles.
- In this public fixture-derived run, KRK produced `17 / 18` exact route/output-contract matches and `1 / 18` structured-equivalent acceptable route change.
- The measured acceptable output rate for the public fixture-derived rule-based comparison is `1.0000`.
- No degraded or failed outputs were observed in this public fixture-derived run.

Not supported:

- production proof.
- production cost reduction.
- customer savings.
- energy reduction.
- broad workload superiority.
- real API/GPU cost reduction.
- semantic-model-judge validation.
- provider superiority.
- H100 superiority.
- production readiness.

## Remaining Gaps

- Add live semantic or human-graded output-quality validation for workloads where exact structural equivalence is insufficient.
- Expand beyond the current 18-item public matrix set.
- Add production-like workload traces only when they can be made public-safe and consented.
- Connect this evaluator to future technical paper methods and reviewer-response tables.
