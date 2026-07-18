## Cross-Dataset Routing: One Fixed Router on Two Intent Domains

**Question.** Does KORA's deterministic keyword router — built automatically
from intent label names, with no per-dataset tuning — generalize across
different intent-classification domains? And what does it cost in accuracy when
it does?

This extends the single-domain CLINC150 experiment to a second, structurally
different domain (banking77), running both through one generalized harness
(`run_multi.py`) against a local vLLM server (Qwen2.5-32B-Instruct). Every query
is classified twice: `direct` (always call the LLM) and `kora` (the keyword
router answers what it confidently can; everything else escalates to the LLM).

**Methodology guard.** The router configuration is held FIXED across both
datasets: `min_score=2.0`, `min_margin=1.0`, and the same weak-token set in
`router.py`. We do not tune the router per dataset. The point is to measure
whether one fixed router generalizes; per-dataset tuning would turn
"domain-agnostic" into "hand-fit per domain" and void the claim. Weaker numbers
on a dataset are an honest result, not something to optimize away.

The router never sees the gold label or the case category — it decides purely
from the query text (answer-blind), exactly as in the front-door experiments.

---

### Results (N=500, seed=0, Qwen2.5-32B-Instruct)

| dataset | labels | direct acc | KORA acc | Δacc | deflection | LLM calls saved | input tokens saved | deflect accuracy |
|---------|-------:|-----------:|---------:|------:|-----------:|----------------:|-------------------:|-----------------:|
| CLINC150  | 151 | 0.836 | 0.810 | −2.6pt | 20.8% (104/500) | 104 | 58,955 | 0.817 |
| banking77 |  77 | 0.700 | 0.682 | −1.8pt | 23.8% (119/500) | 119 | 53,602 | 0.748 |

The CLINC150 row reproduces the previously committed single-domain result
exactly (deflection 0.208, Δacc −0.026), confirming `run_multi.py` shares the
validated routing path.

---

### What this shows

1. **One fixed router generalizes across domains.** With zero per-dataset
   tuning, the same router deflects 20.8% / 23.8% of queries on two unrelated
   intent domains. The deflection rate is a property of the router and the
   workload, not something hand-fit to each dataset.

2. **Routing on pure intent classification trades a little accuracy for fewer
   calls.** Both datasets show ~20–24% fewer LLM calls and tokens at a 1–3 point
   accuracy cost. This ~20-24% is the conservative per-domain band measured on
   these two intent domains (CLINC150 20.8%, banking77 23.8%), not a
   domain-agnostic constant: per-domain deflection tracks how much the label
   vocabulary overlaps the query text, and varies widely across domains.
   This is KORA's *weak* setting: pure judgment tasks where there
   is no deterministic, rule-answerable structure to exploit. It contrasts with
   the rule-rich single-domain workload (northwindgoods), where the front door
   deflects 76.06% with no accuracy loss because the deflected queries have
   deterministic answers (format/FAQ/policy). The honest summary: KORA pays off
   most where queries have deterministic answers, and least on pure
   classification.

3. **The two domains fail differently.** CLINC150's losses come largely from
   weak, non-discriminative label tokens (e.g. `what_can_i_ask_you` →
   {can, i, ask} matching many "can i ..." queries). banking77's losses come
   from fine-grained, near-synonymous labels the keyword overlap cannot separate
   (e.g. `order_physical_card` vs `get_physical_card`, `card_arrival` vs
   `card_delivery_estimate`, `transfer_timing` vs `transfer_into_account`). The
   router lands in the correct topic cluster but cannot resolve within it. This
   is expected: banking77 is deliberately a fine-grained single-domain dataset.

---

### Honest limitations

- **Deflect accuracy is below 1.0 on both datasets** (CLINC150 0.817, banking77
  0.748). The router answers some queries wrongly without escalating — genuine
  over-routing, the source of the accuracy delta. Unlike the front-door
  experiments on northwindgoods (where deflected format/FAQ/policy answers are
  deterministically correct), here the "deterministic" answer is a keyword guess
  at an intent, which can be wrong.

- **banking77 has lower deflect accuracy but smaller Δacc.** Because banking77's
  `direct` accuracy is itself only 0.700, the LLM also struggles on the hard
  fine-grained cases, so the router's wrong deflections cost less in relative
  terms than CLINC150's. Lower deflect accuracy does not mechanically mean a
  larger overall accuracy loss.

- **`min_margin` is a lever, not tuned here.** Raising the margin threshold would
  push more near-synonymous-label cases to the LLM, trading deflection for
  deflect accuracy. We leave it fixed to keep the cross-dataset comparison
  honest; characterizing that trade-off is future work.

---

### Reproduce

```bash
cd experiments/clinc150_direct_vs_kora
# banking77 (parquet, downloaded once; no dataset script)
HF_HOME=~/.cache/huggingface python run_multi.py --dataset banking77 --n 500 --seed 0
# CLINC150 (cached; offline)
HF_HOME=~/.cache/huggingface python run_multi.py --dataset clinc_oos --n 500 --seed 0
```

Requires a local OpenAI-compatible endpoint (vLLM) serving the model at
`--base-url`. Per-query records (including every wrong deflection) are written to
`results/{dataset}_n500_seed0.json`.

Note: banking77 is loaded from `DeepPavlov/banking77` parquet files directly,
because `datasets` 5.x no longer executes dataset loading scripts.
