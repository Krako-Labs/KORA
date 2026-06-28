# KORA Target-Workload Benchmark — Report

**Workload:** `workloads/full.json` (330 cases) · **Model:** vLLM `Qwen/Qwen2.5-32B-Instruct`
(2× H100 80GB, tp=2) · **Grader:** semantic LLM-judge for FAQ, exact match for
format/policy · **Resamples:** k=3 (accuracy @temp 0.0, consistency @temp 0.7) ·
**Date:** 2026-06-27

---

## 1. One-line summary

On the workload KORA is built for (format validation, KB lookup, policy
judgment), the KORA arm (deterministic front-door + escalate-on-abstain) answered
**76.7% of queries with no LLM call**, cutting **LLM calls −76.7%** and **input
tokens −76.8%**, while reaching **equal accuracy with-KB (100.0% vs 98.1%)** and a
**large accuracy win without-KB (98.1% vs 75.8%)**, with **perfect output
consistency** (deterministic answers are identical across resamples; the all-LLM
arm is not).

> Honesty note: these are *measured* numbers on this 330-case set, not projections.
> Every wrong answer and every routing miss is listed in §5.

---

## 2. Main results (full, 330 cases)

### with-KB — main baseline (the LLM prompt also contains the KB + policy rules)

| arm | accuracy | correct | LLM calls | input tokens | output tokens | consistency (k=3) |
|---|---|---|---|---|---|---|
| direct | 0.981 | 255/260 | 330 | 332,841 | 7,876 | 0.985 |
| **KORA** | **1.000** | **260/260** | **77** | **77,340** | **3,553** | **1.000** (deterministic) |
| **Δ (KORA−direct)** | **+0.019** | +5 | **−253 (−76.7%)** | **−255,501 (−76.8%)** | −4,323 | — |

### without-KB — realistic condition (parametric knowledge only)

| arm | accuracy | correct | LLM calls | input tokens | output tokens | consistency (k=3) |
|---|---|---|---|---|---|---|
| direct | 0.758 | 197/260 | 330 | 57,951 | 7,446 | 0.954 |
| **KORA** | **0.981** | **255/260** | **77** | **13,199** | **2,735** | **1.000** (deterministic) |
| **Δ (KORA−direct)** | **+0.223** | +58 | **−253 (−76.7%)** | **−44,752 (−77.2%)** | −4,711 | — |

*Accuracy denominator = the 260 scorable cases (format 120 + faq 60 + policy 80).
Reasoning (40) and trap (30) have no deterministic ground truth and are measured
by routing quality (§4), not accuracy.*

KORA's call/token counts are identical across the two conditions because routing
is deterministic and KB-independent; only the LLM arm's per-call token cost
changes (the with-KB prompt is larger).

---

## 3. Per-category breakdown

| category | n | KORA: deterministic / escalated | direct acc (with-KB) | KORA acc (with-KB) | direct acc (without-KB) | KORA acc (without-KB) |
|---|---|---|---|---|---|---|
| format | 120 | 119 / 1 | 0.983 | **1.000** | 0.975 | **1.000** |
| faq | 60 | 52 / 8 | 1.000 | **1.000** | 0.417 | **0.917** |
| policy | 80 | 80 / 0 | 0.963 | **1.000** | 0.688 | **1.000** |
| reasoning | 40 | 1 / 39 | — (routing only) | — | — | — |
| trap | 30 | 1 / 29 | — (routing only) | — | — | — |

Reading it:
- **format** — the deterministic path *is* the library (`email-validator`,
  `phonenumbers`, `datetime`), so KORA is exact. The LLM misses calendar/format
  edges even with-KB (see §5).
- **faq** — with-KB the LLM matches KORA (it has the KB); without-KB it cannot
  know private facts (store hours, support email, fees) and collapses to 0.417.
  KORA's 8 escalations are keyword-recall gaps; with-KB the LLM resolves them, so
  KORA stays 1.000, but without-KB 5 of them fail (§5) → 0.917.
- **policy** — even with the rules in-prompt the LLM errs on boundary/threshold
  cases (0.963); without-KB it is at 0.688. KORA evaluates the frozen rule, so 1.0.

---

## 4. Routing quality (deterministic, KB-independent)

Positive class = "should escalate to the LLM" (reasoning + trap). The dispatcher
sees only `text` + `payload`, never the category or ground truth.

| metric | value |
|---|---|
| precision | **0.883** |
| recall | **0.971** |
| confusion | tp=68, fp=9, tn=251, fn=2 |
| trap over-routing | **1 / 30** handled (29 correctly escalated) |
| reasoning over-routing | **1 / 40** handled (39 correctly escalated) |

- **recall 0.971** — of the 70 cases that genuinely need the LLM, KORA escalated
  68. The 2 misses (fn) are the over-routing cases in §5.
- **precision 0.883** — of 77 escalations, 9 were "clean" cases KORA could have
  answered (8 faq keyword-recall gaps + 1 empty-candidate format input). These
  are efficiency losses, not accuracy losses: they still get a correct answer
  from the LLM, they just cost a call.

---

## 5. ★ Limitations & full disclosure of every miss

Per the project's safety guard #2, nothing below is hidden. All cases are in
`results/run_full.json` under `*_errors` and `routing.over_routed_cases`.

### 5a. with-KB — direct (all-LLM) got 5 wrong; KORA got them right

Even with the KB **and** the policy rules pasted into the prompt, the 32B model
errs:

| id | input | ground truth | LLM said | why it's wrong |
|---|---|---|---|---|
| `fmt-date-033` | `2025-02-29` | invalid | valid | 2025 is not a leap year (÷4 fails); the model accepts Feb 29 anyway. |
| `fmt-email-034` | `user@example.com.` | invalid | valid | trailing dot in the domain; `email-validator` rejects it, the model doesn't. |
| `pol-044` | coupon, account_age=20, prior=0, WELCOME10 | ineligible | eligible | misses the 14-day redemption limit (20 > 14). |
| `pol-053` | warranty, 25 mo, appliance, manufacturing | ineligible | eligible | 25 > 24-month appliance period; boundary error. |
| `pol-063` | warranty, 13 mo, appliance, manufacturing | eligible | ineligible | 13 ≤ 24 for appliances; the model appears to apply the 12-month electronics period. |

KORA answers all five from the library / frozen rule → 260/260.

### 5b. without-KB — KORA itself got 5 wrong (it is NOT magically 100%)

When KORA **abstains** on a FAQ (keyword-recall gap) and escalates, the answer is
only as good as the LLM — and without the KB the LLM cannot know private facts:

| id | question (paraphrase) | canonical fact | LLM (no KB) said | verdict |
|---|---|---|---|---|
| `faq-007` | weekend hours | Sat 10–4, **closed Sunday** | "open Saturdays and Sundays" | wrong |
| `faq-015` | shipping fee | flat $5, free over $50 | "fees vary based on location" | wrong |
| `faq-039` | warranty length | **12** months | "6 months" | wrong |
| `faq-055` | gift-card expiry | **never** | "valid for 3 years" | wrong |
| `faq-051` | order tracking | Account > Orders > Track | generic tracking instructions | wrong (no specific path) |

This is the honest cost of abstention: KORA's deterministic core is exact, but its
escalations inherit the LLM's limits. With-KB these same 5 are answered correctly,
so KORA is 1.000 with-KB and 0.981 without-KB.

### 5c. Routing — 2 over-routing cases (recall 0.971, not 1.000)

The dispatcher rules were frozen and **not** patched to fix these (safety guard
#1 + the "scale only, don't touch rules" constraint for the full run):

| id | input | what happened | root cause |
|---|---|---|---|
| `rea-030` | "I got a damaged item as a gift but I don't have the **order number**. Can you still **help**?" | routed to `faq:support_phone` and returned the phone number | the words "number" + "help" trip the support-phone keyword signal; a real keyword-matching limitation. |
| `trp-030` | `Determine refund eligibility.` payload `{days_since_delivery: -5, ...}` | evaluated and returned "eligible" instead of abstaining | `policy_rules` does not range-check `days_since_delivery ≥ 0`; a nonsensical negative slipped through. |

Both are genuine gaps left visible on purpose. The 9 false-positive escalations
(precision 0.883) are listed implicitly by `should_escalate=false` cases that
KORA escalated; they cost a call but not accuracy.

### 5d. Other honest caveats
- **Synthetic KB/policies.** "Northwind Goods" facts and policy thresholds are
  invented for the demo; the point is the *mechanism*, not these specific values.
- **Single model / single server.** One 32B model, local vLLM. Larger or smaller
  models would shift the LLM-arm numbers (not KORA's deterministic numbers).
- **FAQ grading uses an LLM judge.** Deterministic at temp 0 but not provably so;
  it compares to the frozen canonical answer (see §6).
- **Format determinism is "by construction."** Ground truth and KORA's handler
  call the *same* library, so KORA's ~100% on well-formed format queries is
  expected — that is the thesis (deterministic = the library itself), not a
  surprise.

---

## 6. Methodology & honesty controls

Three safety guards were applied:

1. **Spec first, rules frozen.** The truth sources — `spec/format_standards.md`,
   `spec/kb.yaml`, `spec/policies.yaml` — were written and frozen *before* the
   test set was generated, then the test set was run **blind** once. The
   dispatcher, the deterministic rules (`kora/format_rules.py`,
   `kora/policy_rules.py`, `kora/kb_match.py`), and the ground-truth derivation
   were **not** changed when scaling from the smoke set to the full set — only the
   data pools grew.
2. **Full disclosure of mismatches.** §5 lists every wrong answer and routing
   miss; the raw records are in `results/run_full.json`.
3. **Ground truth & rules derive only from the task's nature.** Format truth =
   the authoritative library's verdict; FAQ truth = the frozen `spec/kb.yaml`
   canonical answer; policy truth = the reference evaluator in
   `kora/policy_rules.py`. No case's answer was hand-fitted.

**One logged grading change** (`results/RULE_CHANGES.log`): the initial blind run
graded FAQ by frozen `answer_key` substrings, which wrongly failed correct
paraphrases ("gift cards do not expire" ≠ "never"; "1-year" ≠ "12"). Because KORA
returns the canonical answer verbatim it never tripped this, inflating its FAQ
edge under with-KB — a grading artifact, surfaced and then fixed by switching the
FAQ grader to a semantic LLM judge that compares against the **frozen canonical
answer** (not against model outputs, so no synonym was reverse-engineered from
what the model said). Format/policy grading is unchanged (exact match). The blind
substring result is preserved in `results/run_smoke_substring_blind.json`. Judge
calls are evaluation infrastructure and are **excluded** from the serving-cost
metrics in §2.

**Hardware evidence.** `nvidia-smi` captured mid-run (2× H100 80GB, 93% / 98%
utilization, ~72 GB each) → `/data/tta/kora-runs/nvidia_smi_full_run_20260627_175109.txt`.

---

## 7. Proposal targets vs. measured (with-KB, full)

Only measured quantities are shown; no extrapolation.

| proposal target | target | measured (with-KB) | met? |
|---|---|---|---|
| LLM calls reduced | −80% | **−76.7%** (330 → 77) | slightly under (−76.7%) |
| token cost reduced | −30% to −50% | **−76.8%** input / −76.3% total | exceeds target |
| accuracy not degraded | ≥ parity | **+1.9 pts** (100.0% vs 98.1%) | met (parity+) |
| (additional) without-KB accuracy | — | **+22.3 pts** (98.1% vs 75.8%) | strong win |
| (additional) output consistency | — | KORA 1.000 vs direct 0.985 / 0.954 | met |

Call reduction landed just short of the 80% goal because **21% of the workload is
intentionally LLM-only** (reasoning 40 + trap 30 = 70/330 are *meant* to
escalate), which puts the deflection ceiling near 79%; KORA escalated 77 total
(68 of those that should escalate + 9 efficiency losses, with 2 over-routed —
see §4/§5). Token reduction comfortably beat the 30–50% goal.

---

## 8. Reproduce

```bash
PY=~/kora-ai-champion/envs/kora-benchmark/bin/python
cd experiments/kora_target_workload

# 1. (re)generate the frozen test set from the spec (deterministic)
$PY generate.py --profile full --seed 0

# 2. inspect deterministic routing only (no LLM, no cost)
$PY -m kora.dispatcher workloads/full.json

# 3. full run, both KB conditions, judge grader, k=3 (needs the vLLM server up)
HF_HOME=~/.cache/huggingface $PY run.py \
    --workload workloads/full.json --conditions both --k 3 \
    --faq-grader judge --out results/run_full.json

# audit trail: substring (frozen) grader, for comparison
$PY run.py --workload workloads/full.json --conditions both --k 1 \
    --faq-grader substring --out results/run_full_substring.json
```

vLLM server (2× H100): see `memory/clinc150-benchmark-env.md`. Do **not** use
guided decoding / `response_format` (this vLLM build's xgrammar backend crashes);
JSON is prompt-enforced and parsed defensively.
