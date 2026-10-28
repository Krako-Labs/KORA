# AI Champion 2026 — Bounded Evaluation Results

**Evidence cutoff:** 2026-10-22 KST for the experiments below.
**Publication:** 2026-10-28.
**Status:** Author-reported, limited benchmark results; **not** an independently certified state-of-the-art result or proof of production savings.

These results summarize three **separate evaluations** from the project's AI Champion 2026 report draft v0.6 and frozen local research records. The raw evaluation receipts and model traces have **not** been published in this repository. Results are not reproducible using the public KORA Core checkout alone. The reproducible [100-task simulated benchmark](kora_benchmark_result_v1_100.md) is a **different** experiment; its 80% simulated figure must not be substituted for the actual-model-call result below.

<br />

## Results at a Glance

| Evaluation | Measured result | Evidence type and primary limitation |
| --- | --- | --- |
| **KECB v0.6 (author-designed)** | **2,400 → 31 model calls** (**98.7083% fewer**); KORA **2,400/2,400** correct on the specified rule-based workload | Real local Qwen model requests for the Direct comparison; intentionally favorable known-policy tasks; equal-tools router also scored 2,400/2,400 with 30 calls |
| **Multi-domain offline checks** | **50,000 counted checks/events**, including **40,000/40,000 deterministic output checks** with zero mismatches | Mixed synthetic and public-source input *operations*, not 50,000 question-answering or model-inference accuracy evaluations |
| **CacheEval (original 2,000 items)** | **F1 86.9231%**, **false-hit rate 4.5283%** | Exploratory grouped five-fold evaluation on public-source data; not an identical or independent replication of the published BudCache study |

Do not add the 2,400 KECB tasks to the 50,000 events and claim the resulting number represents one common benchmark population. The evaluations measure different outcomes.

<br />

## 1. KECB v0.6 — Author-Designed Policy Workload

**KORA Execution Control Benchmark (KECB)** uses 2,400 deliberately favorable, author-defined, repeated-policy tasks:

- **2,320** first-seen requests with known rule grammar, numeric facts, and human-authored policies.
- **50** exact-repeat tasks eligible for verified reuse.
- **30** requests missing required facts, routed to the model.

The Direct arm made **2,400 actual requests** to a local Qwen3-30B-A3B model. KORA made **30 actual fallback requests** on this run, plus **one historical real policy-generation request** counted as setup: **31 model requests total**. The resulting call reduction versus Direct is **2,369/2,400 = 98.7083%**. The separate initial policy-generation call was not repeated as part of the same run.

On exact specified task answers, KORA scored **2,400/2,400**. An independently checked **three-arm/direct** comparison passed its author-managed audit. The Direct model-only arm scored **364/2,400** against the same strict answers, but that arm did **not** have the same trusted arithmetic tools or preconfigured policies.

**Critical comparison:** A manually configured router with access to the **same trusted tools and hand-authored rules** also reached **2,400/2,400** correct with **30** live model requests, **tying** KORA on the designated tasks. The experiment demonstrates the possible value of deterministic execution when rules are already known; it does **not** establish superiority to an equally equipped coordinator.

The fourth exact-cache arm did not pass its frozen route assertion: **54** reuses were recorded where **50** were declared, including four missing-fact cases. Therefore **no full four-arm acceptance or audit** is claimed. The independently checked three-arm/direct result remains distinct.

**What this does not measure:** Production usage, typical request mix, general policy extraction, externally billed API savings, equal-tools latency superiority, or semantic generalization.

<br />

## 2. Multi-Domain Offline Checks — 50,000 Events

The **50,000 reported validation count** combines different kinds of operations. The authored synthetic source generated 37,500 raw events but contributes 30,000 deterministic output checks to the official subtotal:

| Cohort | Count | What was checked |
| --- | ---: | --- |
| Authored synthetic workload | **37,500 raw events; 30,000 counted output checks** | 30,000 deterministic expected outputs matched; 7,500 extra fallback/metadata events were not added to the 50,000 checked-task subtotal |
| SQuAD / KLUE-MRC / HotpotQA public text inputs | 10,000 | Explicit case/whitespace text normalization outputs matched a separate standard-library reference, **10,000/10,000** |
| SNLI / KLUE-NLI labeled-source requests | 5,000 | Declared semantic-operation requests were **classified into the model-needed route**, not answered by an LLM |
| HotpotQA source-metadata lookup/reuse events | 5,000 | 2,500 repeated lookups reused exact metadata; this was not end-to-end RAG answer evaluation |

**Counting note:** The official **50,000 counted validations** are 30,000 synthetic deterministic output checks + 10,000 text-normalization output checks + 5,000 explicit routing decisions + 5,000 metadata lookup/reuse events. The source's separate 7,500 synthetic metadata-only fallback events are excluded from this denominator. Therefore 50,000 is a selected count of checks, **not all raw events generated across cohorts**. By type:

- **40,000 deterministic outputs** matched their specified expected results.
- **5,000** explicit semantic route decisions selected model-needed.
- **5,000** metadata lookup/reuse events were exercised.

The original synthetic cohort's **7,500 metadata-only fallback events are not added again** to the reported 50,000 tally.

**Limits:** The 10,000 public question texts were normalized, **not answered**. The semantic route test was an explicit operation-type gate, **not** an out-of-distribution language understanding benchmark. The metadata reuse path is not a full RAG or multi-agent execution test. No model calls were made in these offline cohorts. Exploratory variants of the original evaluation protocol must not be presented as all having satisfied the initial frozen protocol.

<br />

## 3. CacheEval — Public-Source Numerical Comparison

On the **full original 2,000-item CacheEval dataset** across 10 domains, an exploratory ExtraTrees classifier was evaluated using grouped five-fold out-of-fold scoring.

| Metric | KORA exploratory study | BudCache developer-reported value | Numerical difference |
| --- | ---: | ---: | ---: |
| F1 | **86.9231%** | 86.4% | +0.5231 percentage points |
| False-hit rate (FHR; lower is better) | **4.5283%** | 4.9% | −0.3717 percentage points |

The confusion matrix reported for the KORA experiment is **TP 565, FP 60, FN 110, TN 1,265**. F1 and FHR follow from these counts. [CacheEval upstream dataset](https://github.com/BudEcosystem/CacheEval).

**Comparison boundary:** The BudCache figures are its **developer-published reference**, not a rerun using KORA's identical folds, feature choices, or evaluation protocol. KORA's exploratory model also followed prior exposure to the dataset during research. These two numerical crossings do **not** establish a reproducible external head-to-head win, a certified global SOTA title, or a feature shipped in public KORA Core.

<br />

## Scope and Future Updates

The current public update covers **only KECB v0.6, the 50,000-event offline validation, and CacheEval**. Other reported benchmark work is deliberately out of scope and will require separate reviewed publication.

Before upgrading any result to a broader or production claim, publish an independently reproducible evaluation contract, licensed input artifacts, model/tool parity, frozen splits, output-quality criteria, and a complete audit. Do **not** infer user cost savings or provider replacement from these experiments.

For current public-source runnable evidence, start with the [100-task simulated benchmark](kora_benchmark_result_v1_100.md). See the [claim registry](../claims/kora-claim-registry.md) for safe publication wording.
