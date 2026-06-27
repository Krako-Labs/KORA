# KORA Target-Workload Benchmark — Deterministic Front-Door Routing

A **measured** benchmark of KORA's core idea: resolve requests that a
deterministic front door can answer *before* inference, and escalate to an LLM
only when the front door abstains. No projections — every number here comes from
real model calls, and every wrong answer is enumerated in the per-model result
JSON.

## What this measures

A single synthetic customer-service domain (`northwindgoods`, 330 cases across
five categories: `format`, `faq`, `policy`, `reasoning`, `trap`). Two arms on the
identical workload:

- **direct** — every request goes to the LLM.
- **kora** — a deterministic, **answer-blind** dispatcher (sees only the user
  text + optional structured payload, never the category or ground truth) either
  answers deterministically or abstains; abstentions escalate to the same LLM.

The dispatcher is run unchanged across every model. Only the escalation model
changes. That isolates one question: *what does deterministic deflection do to
cost and accuracy, independent of which model you pay for?*

## TL;DR

Deterministic routing is decided by the dispatcher, not the model, so the
deflection rate is **identical across all five models**: KORA makes **76.7% fewer
LLM calls** (330 → 77) on this workload. The accuracy effect, however, depends on
the served model — and it grows as the model gets weaker.

| Served model | tier | deflection | LLM calls saved | with-KB Δacc | without-KB Δacc |
|---|---|---|---|---|---|
| Llama 3.1 8B | tiny | 76.7% | 76.7% | +0.123 | **+0.335** |
| Llama 3.3 70B | large | 76.7% | 76.7% | +0.050 | +0.319 |
| Claude Haiku 4.5 | small | 76.7% | 76.7% | +0.019 | +0.300 |
| Nova Pro | mid | 76.7% | 76.7% | +0.031 | +0.265 |
| Claude Sonnet 4.6 | frontier | 76.7% | 76.7% | +0.012 | +0.223 |

Absolute accuracy (direct → KORA):

| Served model | with-KB direct → KORA | without-KB direct → KORA |
|---|---|---|
| Claude Sonnet 4.6 | 0.988 → 1.000 | 0.765 → 0.988 |
| Nova Pro | 0.969 → 1.000 | 0.715 → 0.981 |
| Claude Haiku 4.5 | 0.981 → 1.000 | 0.677 → 0.977 |
| Llama 3.3 70B | 0.950 → 1.000 | 0.658 → 0.977 |
| Llama 3.1 8B | 0.877 → 1.000 | 0.646 → 0.981 |

Setup: N=330, k=1, FAQ semantic grader **held fixed at Claude Sonnet 4.6 across
all arms** (so grading never varies with the served model). Models served via AWS
Bedrock Converse. A local **Qwen2.5-32B** run (vLLM, 2× H100) reproduces the same
**deflection = 76.7%** (deflection is independent of the judge and of k, since
it is fixed by the deterministic router), confirming the routing result is not
specific to hosted APIs.

## The one result that needs no credentials

Deflection, routing precision, and recall come purely from the deterministic
dispatcher — **zero LLM calls, no API key, no GPU**. Anyone can reproduce them:

```bash
python run.py --routing-only --workload workloads/full.json --out /tmp/routing.json
# -> precision=0.883 recall=0.971  (deflection 76.7%)
```

This is the heart of KORA's claim, and it is fully reproducible offline.

## Reproduce

```bash
# From this directory. Requires Python 3.10+ and pyyaml.
pip install pyyaml
# For workload regeneration, pin the validators used to build it:
#   pip install email_validator==2.3.0 phonenumbers==9.0.33   (Python 3.10)

# (1) Routing only — no LLM, no key, no GPU. Reproduces deflection/precision/recall.
python run.py --routing-only --workload workloads/full.json --out /tmp/routing.json

# (2) Full accuracy run for one model — requires AWS Bedrock access.
#     Export your Bedrock bearer token first (never commit it):
export BEDROCK_KEY=...    # your AWS Bedrock API key
python run.py \
  --backend bedrock \
  --model anthropic.claude-sonnet-4-6 \
  --judge-model anthropic.claude-sonnet-4-6 \
  --workload workloads/full.json \
  --conditions both --k 1 \
  --out results/full_sonnet46.json

# (3) All five models in sequence (Bedrock), then aggregate:
./run_all_models.sh
python aggregate_results.py
```

The committed `results/full_*.json` let you verify every number above without
running anything: each file lists per-category accuracy and **every** wrong
answer and routing miss for both arms.

## What "without-KB" actually means

In the **without-KB** condition the model is asked company-specific facts
(opening hours, support email, refund policy) with no knowledge base in context.
The low `direct` accuracy there is **not** "the model is dumb" — these facts are
simply unknowable without the KB, so the model abstains or guesses. KORA resolves
them via deterministic KB lookup, which is why its accuracy stays ~0.98 regardless
of the served model. With the KB in context, `direct` FAQ accuracy is high too;
the gap is about *grounding*, not raw model quality.

This is the honest framing: KORA does not make models smarter. It guarantees the
company-fact answers deterministically, and only pays for an LLM on the requests
that genuinely need one.

## Honesty notes

- **Measured, not projected.** All numbers come from real model calls on this
  330-case set.
- **Answer-blind router.** The dispatcher never sees the case category or the
  ground truth — only what a real front door sees (user text + optional payload).
- **Errors are public.** Each `results/full_*.json` enumerates every wrong answer
  and every routing miss, including KORA's own (e.g. over-routed cases where the
  deterministic path answered something it should have escalated — 2 such cases
  here, surfaced in the routing report).
- **Fixed judge.** The FAQ semantic grader is held at one model (Sonnet 4.6)
  across all arms, so accuracy differences reflect the served model, not the
  grader.
- **Single domain.** This is one synthetic domain. The deflection rate is a
  property of this workload's deterministic-resolvable fraction, not a universal
  constant. Broader workloads are future work.

## Relation to the root KORA package, and roadmap

The dispatcher used here (`kora/dispatcher.py` in this folder) is a focused
**front-door classifier** built for this benchmark. The root `kora/` package
implements the same deterministic-first philosophy through a task-graph engine;
this dispatcher is an independent, self-contained implementation of that idea,
kept beside the benchmark so the exact measured code is public.

Roadmap toward promoting this into the root package as a first-class
`kora.dispatch()` API:

1. **Generalize** the dispatcher to arbitrary domains (user-supplied KB/rules)
   rather than one hard-coded domain.
2. **Quantify over-routing safety** — formal bounds on when deterministic
   answering is safe (the 2 over-routed cases here are the starting point).
3. **Integrate** with the root task-graph engine as its deterministic-path stage.

Until those land, this stays an independent, reproducible benchmark rather than a
promoted API — to avoid shipping an unvalidated generalization.

## Files

- `run.py` — benchmark runner (vLLM/OpenAI or Bedrock backend; `--routing-only`).
- `bedrock_client.py` — minimal Bedrock Converse → OpenAI-compatible shim.
- `kora/` — the deterministic dispatcher and its rule modules.
- `spec/` — the domain definition the dispatcher reads (`kb.yaml`,
  `policies.yaml`, `format_standards.md`).
- `workloads/full.json` — the frozen 330-case test set (`smoke.json` is a subset).
- `generate.py` — regenerates the workload from the spec. Verified byte-identical to the committed `full.json` (MD5 match) with the library versions in the workload's `generated_with` field.
- `results/full_*.json` — per-model measured results (5 models).
- `results/routing_only.json` — credential-free routing result.
- `results/SUMMARY_model_diversity.md`, `results/REPORT.md` — summary and the
  single-model (Qwen) deep-dive report.
- `run_all_models.sh`, `aggregate_results.py` — sweep and aggregation helpers.
