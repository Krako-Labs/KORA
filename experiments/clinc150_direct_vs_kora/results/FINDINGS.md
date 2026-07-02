# Multi-Domain Benchmark Findings

Five intent workloads, one fixed router configuration, zero per-dataset
tuning. Canonical result files follow the `{dataset}_n{N}_seed{S}.json`
naming convention; `run_n500_seed0.json` (legacy name for the clinc run)
and `smoke_n20_seed0.json` (n=20 smoke) are not citable results.
Backend: Qwen2.5-32B-Instruct via local vLLM. Safety analysis:
`analyze_deflection.py` → `deflection_analysis.json`.

## Results summary (seeds 0/1/2 where applicable)

| dataset   | domain        | deflection   | accuracy delta      |
|-----------|---------------|--------------|---------------------|
| symptom   | medical       | 1.9% (all)   | 0.0 (all seeds)     |
| tickets   | IT helpdesk   | 5.4–7.6%     | +0.2 to +0.4pt      |
| clinc_oos | general       | ~21%         | ~-2.6pt             |
| banking77 | banking       | ~24%         | ~-1.8pt             |
| law       | legal         | 34.2–38.8%   | -2.8 to -3.8pt      |

symptom uses the full 212-row test split; identical numbers across seeds
confirm pipeline determinism rather than measuring sampling variance.

## Finding 1: deflection adapts to keyword signal strength

Deflection spans 1.9%–39% across domains under one router. The driver is
not the domain per se but how often label-derived keywords appear in the
utterance: legal questions name their topic ("copyright", "employment");
symptom descriptions never name the diagnosis.

## Finding 2: reasoning-heavy workloads degrade to safe pass-through

symptom_to_diagnosis is a symptom->diagnosis inference task: the label
never appears in the input, so the router abstains on nearly everything
(1.9% deflection) at zero accuracy cost. Where inference is genuinely
required, deflection converges toward zero instead of producing unsafe
deterministic answers. This is the intended failure mode. Note this is
the most router-adversarial slice of the medical domain; operational
medical traffic (appointments, billing, admin intents) resembles the
clinc/banking regime and is expected to deflect at materially higher
rates (untested here).

## Finding 3: accuracy cost is bounded and structurally concentrated

Across all 13 runs, router accuracy on deflected cases matches or
exceeds LLM accuracy on escalated cases (one marginal inversion: law
seed 1). At the highest deflection observed (~39%), accuracy cost stays
within 4pt, and per-case analysis (law seed 0: 31 net-loss vs 16
net-gain cases) shows losses concentrate in semantically overlapping
label pairs (copyright vs intellectual-property, employment vs
contract-law) — a property of the upstream taxonomy, kept unmerged by
design, rather than arbitrary misrouting.

## Dataset notes

- tickets (Tobi-Bueck/customer-support-tickets) is CC-BY-NC-4.0;
  used here for research benchmarking. English subset, `queue` as label.
- law labels kept exactly as upstream, including overlapping pairs;
  merging them would constitute per-dataset tuning.
