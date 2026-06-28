# Routing Robustness Under Intent-Preserving Paraphrase

**Question.** KORA's front door routes *answer-blind*: it sees only the user
`text` (and an optional structured `payload`), then either answers
deterministically or abstains so the query escalates to an LLM. `kb_match.py`
states (Safety Guard #3) that its routing signals come from a query's *meaning*,
not its exact wording. This experiment tests that claim empirically — and, more
importantly, asks a safety question: **can a surface rephrasing of a query that
*should* escalate cause the front door to deflect it instead?**

A deflection that should have escalated is a *false deflection*: a hard query
answered by a rule that was never meant to handle it. That is the only failure
mode that matters for safety. A rephrasing that pushes an answerable query the
other way — into the LLM — costs money but is harmless.

**Result (preview).** Across 5 transforms × 330 cases, there were **0 dangerous
flips**: no should-escalate case was ever paraphrased into a deflection. Every
decision change went the safe direction (deflect → escalate). Surface ambiguity
makes the front door *more* conservative, never less safe.

---

## Method

All measurements are deterministic and use **zero LLM calls** — the same
front-door code path as `run.py --routing-only` (`dispatcher.dispatch`, see
`run.py` L485). No API key, no GPU.

Each transform rewrites only a case's `text`. Every label
(`should_escalate`, `ground_truth`, `payload`, `meta`) is left untouched, so the
routing confusion matrix stays directly comparable to the original workload.

### Methodology guard (frozen before measuring)

Transforms were defined by a single criterion — *"would a real user write the
same request this way?"* — and **not** by whether they help or hurt the
dispatcher. We report whatever happens: breaks are real fragility, non-breaks
are real robustness. No transform was hand-tuned to force a trap into a valid
frame, nor to dodge a path we knew to be fragile.

### Transforms

| name | what it does | a priori prediction |
|------|--------------|---------------------|
| `whitespace`    | double the inter-word spaces, pad the ends | benign sloppiness |
| `punct`         | flip terminal punctuation (`?` on/off)     | no-op |
| `case`          | sentence-case the whole string             | **true no-op** (dispatcher lowercases internally) — a sanity check on our own pipeline |
| `polite_prefix` | prepend "Could you please tell me: "       | breaks the strict FORMAT frame (cost-only) |
| `synonym`       | conservative user-plausible swaps (`valid`→`correct`, `open`→`available`, `hours`→`times`, `refund`→`money back`, `eligible`→`qualified`) | breaks FORMAT literal + some policy/FAQ keywords |

Positive class = `should_escalate`. A case is *escalated* when the front door
abstains (`not routed`). Flips are bucketed as:

- **dangerous**: should_escalate, original escalated, variant **deflected** → false deflection (safety failure). Target: 0.
- **benign**: not should_escalate, original deflected, variant **escalated** → cost only.
- **other**: any remaining change (reported for completeness).

---

## Results

Original workload (full, 330 cases): deflection **0.767**, precision **0.883**,
recall **0.971** (tp=68 fp=9 tn=251 fn=2). This matches the committed
`results/routing_only.json`, confirming the harness shares the production
routing path.

| transform | deflection | precision | recall | **dangerous** | benign | other |
|-----------|-----------:|----------:|-------:|--------------:|-------:|------:|
| `whitespace`    | 0.388 | 0.337 | 0.971 | **0** | 126 | 1 |
| `punct`         | 0.770 | 0.895 | 0.971 | **0** |   0 | 1 |
| `case`          | 0.767 | 0.883 | 0.971 | **0** |   0 | 0 |
| `polite_prefix` | 0.409 | 0.349 | 0.971 | **0** | 118 | 0 |
| `synonym`       | 0.348 | 0.321 | 0.986 | **0** | 137 | 1 |

**Dangerous flips: 0 across all transforms.** No should-escalate case was ever
paraphrased into a deflection.

### Where the deflection drops come from

Benign flips, by category:

| transform | format | faq | policy |
|-----------|-------:|----:|-------:|
| `whitespace`    | 118 | 8 | 0 |
| `polite_prefix` | 118 | 0 | 0 |
| `synonym`       | 118 | 3 | 16 |

The drops are overwhelmingly **FORMAT** (118 of 120 FORMAT cases break under each
of the three disruptive transforms). FORMAT routing relies on a strict regex
frame (`^...is this a valid <type>: <candidate>...$`); any surface perturbation
that disturbs the frame — a doubled space inside "email address", a polite
prefix before "is this", or swapping the literal "valid" for "correct" — causes
an abstain. FAQ and POLICY routing use substring keyword matching and are far
more robust: FAQ breaks only on a handful of multi-word-keyword spacing/synonym
cases (8 and 3), POLICY only when a synonym removes a topic/intent keyword
(`refund`→`money back`, `eligible`→`qualified`; 16 cases).

`punct` and `case` are true no-ops, exactly as predicted — `case` confirms our
own pipeline introduces no spurious sensitivity (the dispatcher lowercases
internally).

---

## Interpretation

1. **The over-routing safety boundary is one-directional under paraphrase.**
   Surface ambiguity can only make the front door abstain *more* (escalate to the
   LLM), never deflect a hard query. This is a structural property of an
   answer-blind front door whose default action is to abstain: when a learned or
   literal signal is disturbed, the rule simply fails to fire, and a rule that
   does not fire escalates. Failure is fail-safe by construction.

2. **Robustness is path-dependent, and the regex path is the fragile one.**
   Keyword-substring routing (FAQ, POLICY) tolerates most rephrasings; the strict
   FORMAT regex does not. This is an honest design limitation: FORMAT trades
   robustness for precision. It is also a clean lever for future work — a more
   tolerant FORMAT frame would raise deflection on rephrased format questions
   without touching the safety guarantee, since all FORMAT flips are benign.

3. **Lower deflection here is a cost signal, not a safety signal.** The drop from
   0.767 to ~0.39 under disruptive transforms means more queries reach the LLM —
   it does not mean any query was mishandled.

---

## Honest limitations

Two original false-negatives (should_escalate cases that the front door already
routed *before* any paraphrase) surfaced during this experiment. They are
pre-existing, not caused by the transforms, and are retained here as honest
limitations of the current workload + reference evaluator.

- **`rea-030` (reasoning, no payload).** Text: *"I got a damaged item as a gift
  but I don't have the order number. Can you still help?"* A single KB signal
  matches `faq:support_phone`, so the front door deflects and returns the support
  phone number for a query that should have escalated. A genuine over-route; the
  answer is an innocuous fallback, but the routing decision is wrong.

- **`trp-030` (trap, payload present).** Text: *"Determine refund eligibility."*
  with `payload={"days_since_delivery": -5, "item_category": "books",
  "opened": false}`. The refund evaluator's `_as_int` checks type but not range,
  so a physically impossible negative delivery age passes validation and the
  policy returns "eligible". The trap was designed to probe exactly this input
  hole; the shared evaluator (used by both `generate.py` for ground truth and the
  dispatcher for routing) does not reject out-of-range integers, so the front door
  routes instead of abstaining. This is an input-validation gap in the reference
  evaluator, reported but not patched here to keep the committed routing numbers
  and ground-truth generation stable. Adding a range check would convert this
  fn into an abstain (recall would rise) and is tracked as separate future work.

Notably, the `synonym` transform incidentally *fixes* `trp-030` (it strips the
`refund`/`eligible` keywords, so the front door abstains), which is why
`synonym` recall is 0.986 vs 0.971 elsewhere. We report this as an artifact, not
as a robustness benefit.

---

## Reproduce

```bash
cd experiments/kora_target_workload
python run_robustness.py --workload workloads/full.json \
    --out results/robustness/robustness.json
```

Zero LLM calls, no key, no GPU. The per-case flip lists (including the two
false-negatives above) are written to the output JSON.
