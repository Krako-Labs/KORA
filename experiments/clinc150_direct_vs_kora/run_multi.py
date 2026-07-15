"""Direct-vs-KORA real-inference benchmark across multiple intent datasets.

Generalizes the CLINC150-only run.py into a dataset-agnostic engine. The two
arms, the LLM classifier, the keyword router, and all aggregation
(accuracy / deflection / tokens / latency p50,p95) are unchanged from the
validated CLINC150 experiment — only a dataset-adapter layer and a
parameterized prompt are added, so the same harness can run any intent-labeled
dataset against any OpenAI-compatible backend (local vLLM, hosted APIs).

Methodology guard: the router configuration (min_score, min_margin, the weak-
token set inside router.py) is held FIXED across datasets. We do not tune the
router per dataset. The whole point is to measure whether one fixed router
generalizes across domains; per-dataset tuning would turn "domain-agnostic"
into "hand-fit per domain" and destroy the claim. Weaker numbers on some
dataset are an honest result, not a thing to optimize away.

Datasets:
  * clinc_oos  : CLINC150 (plus) test split. Script-based dataset, already
                 cached locally (HF_DATASETS_OFFLINE). Has an out-of-scope
                 ("oos") label.
  * banking77  : DeepPavlov/banking77, loaded straight from parquet (datasets
                 5.x no longer runs dataset scripts). 77 fine-grained banking
                 intents, no out-of-scope label.

Run:
    HF_HOME=~/.cache/huggingface \
    ~/kora-ai-champion/envs/kora-benchmark/bin/python \
    experiments/clinc150_direct_vs_kora/run_multi.py \
        --dataset banking77 --n 20 --seed 0
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any, Callable

from openai import OpenAI

from intent_parser import parse_intent
from router import KeywordRouter

DEFAULT_BASE_URL = "http://localhost:8000/v1"
DEFAULT_MODEL = "Qwen/Qwen2.5-32B-Instruct"
RESULTS_DIR = Path(__file__).with_name("results")

_TELCO_CSV = (
    "hf://datasets/bitext/Bitext-telco-llm-chatbot-training-dataset/"
    "bitext-telco-llm-chatbot-training-dataset.csv"
)
_ISSUES_TEST_URL = (
    "https://tickettagger.blob.core.windows.net/datasets/"
    "nlbse23-issue-classification-test.csv.tar.gz"
)


def _adapt_clinc(n: int, seed: int) -> tuple[list[dict[str, Any]], list[str], str | None]:
    """CLINC150 (plus) test split. Cached script-based dataset; offline."""
    os.environ.setdefault("HF_DATASETS_OFFLINE", "1")
    from datasets import load_dataset

    ds = load_dataset("clinc_oos", "plus")["test"]
    label_names = list(ds.features["intent"].names)
    sample = ds.shuffle(seed=seed).select(range(n))
    rows = [{"text": ex["text"], "gold": label_names[ex["intent"]]} for ex in sample]
    return rows, label_names, "oos"


def _adapt_banking77(n: int, seed: int) -> tuple[list[dict[str, Any]], list[str], str | None]:
    """DeepPavlov/banking77, loaded directly from parquet (no dataset script).

    The data parquet has columns {utterance, label:int64}; the separate intents
    parquet maps {id:int -> name:str}. We join them to get string gold labels.
    No out-of-scope label.
    """
    from datasets import load_dataset

    base = "hf://datasets/DeepPavlov/banking77"
    data = load_dataset(
        "parquet",
        data_files={"test": f"{base}/data/test-00000-of-00001.parquet"},
    )["test"]
    intents = load_dataset(
        "parquet",
        data_files={"intents": f"{base}/intents/intents-00000-of-00001.parquet"},
    )["intents"]

    id_to_name = {row["id"]: row["name"] for row in intents}
    label_names = [id_to_name[i] for i in sorted(id_to_name)]

    sample = data.shuffle(seed=seed).select(range(n))
    rows = [
        {"text": ex["utterance"], "gold": id_to_name[ex["label"]]}
        for ex in sample
    ]
    return rows, label_names, None



def _norm_label(name: str) -> str:
    """Normalize a raw label to the underscore convention the router expects.

    The keyword router derives its keyword sets from label.split("_"), so
    labels arriving as free text ("peptic ulcer disease") or hyphenated tags
    ("criminal-law") are mapped to lowercase underscore form. This is format
    adaptation only -- no per-dataset semantics are injected.
    """
    return name.strip().lower().replace("-", " ").replace("/", " ").replace("  ", " ").replace(" ", "_")


def _adapt_symptom(n: int, seed: int) -> tuple[list[dict[str, Any]], list[str], str | None]:
    """gretelai/symptom_to_diagnosis test split (medical domain).

    Patient-style symptom descriptions labeled with one of 22 diagnoses.
    Small test split (212 rows); n is capped accordingly. No out-of-scope label.
    """
    from datasets import load_dataset

    ds = load_dataset("gretelai/symptom_to_diagnosis")["test"]
    label_names = sorted({_norm_label(l) for l in ds["output_text"]})
    n = min(n, len(ds))
    sample = ds.shuffle(seed=seed).select(range(n))
    rows = [
        {"text": ex["input_text"], "gold": _norm_label(ex["output_text"])}
        for ex in sample
    ]
    return rows, label_names, None


def _adapt_tickets(n: int, seed: int) -> tuple[list[dict[str, Any]], list[str], str | None]:
    """Tobi-Bueck/customer-support-tickets, English subset (IT helpdesk domain).

    Real-style support tickets routed to one of 10 destination queues; the
    queue is the routing target, which matches the KORA dispatch use case.
    Single train split upstream, so a seeded shuffle provides the eval sample.
    License: CC-BY-NC-4.0 (research benchmark use). No out-of-scope label.
    """
    from datasets import load_dataset

    ds = load_dataset("Tobi-Bueck/customer-support-tickets")["train"]
    ds = ds.filter(lambda x: x["language"] == "en" and x["queue"])
    label_names = sorted({_norm_label(q) for q in ds["queue"]})
    sample = ds.shuffle(seed=seed).select(range(n))
    rows = [
        {
            "text": f"{ex['subject'] or ''}\n{ex['body'] or ''}".strip(),
            "gold": _norm_label(ex["queue"]),
        }
        for ex in sample
    ]
    return rows, label_names, None


def _adapt_law(n: int, seed: int) -> tuple[list[dict[str, Any]], list[str], str | None]:
    """jonathanli/law-stack-exchange test split (legal domain).

    Law Stack Exchange questions labeled with one of 16 topic tags. Labels are
    kept exactly as upstream (including semantically overlapping pairs such as
    contract vs contract-law); merging them would amount to per-dataset tuning.
    Text is title + body, following the source paper. No out-of-scope label.
    """
    from datasets import load_dataset

    ds = load_dataset("jonathanli/law-stack-exchange")["test"]
    label_names = sorted({_norm_label(l) for l in ds["text_label"]})
    sample = ds.shuffle(seed=seed).select(range(n))
    rows = [
        {
            "text": f"{ex['title'] or ''}\n{ex['body'] or ''}".strip(),
            "gold": _norm_label(ex["text_label"]),
        }
        for ex in sample
    ]
    return rows, label_names, None


def _adapt_telco(n: int, seed: int) -> tuple[list[dict[str, Any]], list[str], str | None]:
    """bitext/Bitext-telco-llm-chatbot-training-dataset (telecom support domain).

    Customer utterances labeled with one of 26 telco intents (7 categories).
    Read straight from the CSV; a single split upstream, so a seeded shuffle
    provides the eval sample, as for the tickets adapter.

    The corpus deliberately seeds typos and offensive phrasing (the `tags`
    column marks them Z and W). Those rows are kept: they are real customer
    input, and dropping them would make the workload easier than the thing it
    stands in for. No out-of-scope label.

    License: CDLA-Sharing-1.0 (permits benchmark use and publishing results).
    """
    from datasets import load_dataset

    ds = load_dataset("csv", data_files={"train": _TELCO_CSV})["train"]
    label_names = sorted({_norm_label(i) for i in ds["intent"]})
    sample = ds.shuffle(seed=seed).select(range(min(n, len(ds))))
    rows = [
        {"text": ex["instruction"], "gold": _norm_label(ex["intent"])}
        for ex in sample
    ]
    return rows, label_names, None


def _issues_cache_dir() -> Path:
    """Cache location for the issue-report archive.

    The dataset is not redistributed with this repository, so it is fetched on
    first use and cached outside the tree. HF_HOME is honoured because the
    benchmark hosts already point it at a large volume; the root filesystem is
    typically too small for datasets of this size.
    """
    root = os.getenv("KORA_DATASET_CACHE") or os.path.join(
        os.getenv("HF_HOME") or os.path.expanduser("~/.cache/huggingface"),
        "kora-datasets",
    )
    path = Path(root) / "nlbse2023"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _adapt_issues(n: int, seed: int) -> tuple[list[dict[str, Any]], list[str], str | None]:
    """nlbse2023 issue-report classification, test split (developer-tool domain).

    GitHub issue reports labeled with one issue type: bug, feature, question or
    documentation. Multi-label issues are excluded upstream and the corpus is
    English only. Text is title + body, as for the law adapter.

    The data is downloaded on first use and cached (see _issues_cache_dir); it
    is deliberately not committed to this repository. No out-of-scope label.

    Source: https://github.com/nlbse2023/issue-report-classification (AGPL-3.0).
    The task competition grants use of the data for evaluating classification
    approaches and publishing the comparison.
    """
    import tarfile
    import urllib.request

    from datasets import load_dataset

    cache = _issues_cache_dir()
    csv_path = cache / "nlbse23-issue-classification-test.csv"
    if not csv_path.exists():
        archive = cache / "nlbse23-issue-classification-test.csv.tar.gz"
        if not archive.exists():
            urllib.request.urlretrieve(_ISSUES_TEST_URL, archive)
        with tarfile.open(archive) as tf:
            member = next(m for m in tf.getmembers() if m.name.endswith(".csv"))
            member.name = csv_path.name
            tf.extract(member, path=cache)

    ds = load_dataset("csv", data_files={"test": str(csv_path)})["test"]
    label_names = sorted({_norm_label(l) for l in ds["labels"]})
    sample = ds.shuffle(seed=seed).select(range(min(n, len(ds))))
    rows = [
        {
            "text": f"{ex['title'] or ''}\n{ex['body'] or ''}".strip(),
            "gold": _norm_label(ex["labels"]),
        }
        for ex in sample
    ]
    return rows, label_names, None


DATASETS: dict[str, Callable[[int, int], tuple[list[dict[str, Any]], list[str], str | None]]] = {
    "clinc_oos": _adapt_clinc,
    "banking77": _adapt_banking77,
    "symptom": _adapt_symptom,
    "tickets": _adapt_tickets,
    "law": _adapt_law,
    "telco": _adapt_telco,
    "issues": _adapt_issues,
}


class LLMClassifier:
    def __init__(
        self,
        client: OpenAI,
        model: str,
        label_names: list[str],
        dataset_name: str,
        oos_label: str | None,
    ) -> None:
        self.client = client
        self.model = model
        self.label_names = label_names
        self.dataset_name = dataset_name
        self.oos_label = oos_label
        self._label_set = set(label_names)
        self._label_block = ", ".join(label_names)

    def _system_prompt(self) -> str:
        base = (
            f"You are an intent classifier for the {self.dataset_name} dataset. "
            "Given a user utterance, choose the single best matching intent from "
            "the provided list. "
        )
        if self.oos_label is not None:
            base += (
                f"If none of the in-scope intents apply, answer '{self.oos_label}'. "
            )
        base += 'Respond with JSON only: {"intent": "<label>"}. No prose.'
        return base

    def classify(self, text: str) -> dict[str, Any]:
        """Return {intent, raw, tokens_in, tokens_out, latency_s}."""
        user = f"Allowed intents: {self._label_block}\n\nUtterance: {text}"

        start = time.monotonic()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": user},
            ],
            temperature=0.0,
            max_tokens=30,
        )
        latency_s = time.monotonic() - start

        raw = resp.choices[0].message.content or ""
        fallback = self.oos_label if self.oos_label is not None else ""
        intent, parse_path = parse_intent(
            raw, self.label_names, self._label_set, fallback
        )
        usage = resp.usage
        return {
            "intent": intent,
            "raw": raw,
            "parse_path": parse_path,
            "tokens_in": int(usage.prompt_tokens) if usage else 0,
            "tokens_out": int(usage.completion_tokens) if usage else 0,
            "latency_s": latency_s,
        }


def run_direct(rows: list[dict[str, Any]], clf: LLMClassifier) -> dict[str, Any]:
    records = []
    for row in rows:
        out = clf.classify(row["text"])
        records.append(
            {
                "text": row["text"],
                "gold": row["gold"],
                "pred": out["intent"],
                "correct": out["intent"] == row["gold"],
                "llm_called": True,
                "tokens_in": out["tokens_in"],
                "tokens_out": out["tokens_out"],
                "latency_s": out["latency_s"],
                "raw": out["raw"],
                "parse_path": out["parse_path"],
            }
        )
    return _aggregate("direct", records)


def run_kora(
    rows: list[dict[str, Any]], clf: LLMClassifier, router: KeywordRouter
) -> dict[str, Any]:
    records = []
    for row in rows:
        decision = router.route(row["text"])
        if decision.routed:
            pred = decision.intent
            rec = {
                "text": row["text"],
                "gold": row["gold"],
                "pred": pred,
                "correct": pred == row["gold"],
                "llm_called": False,
                "tokens_in": 0,
                "tokens_out": 0,
                "latency_s": 0.0,
                "route": decision.reason,
                "raw": "",
                "parse_path": "routed",
            }
        else:
            out = clf.classify(row["text"])
            rec = {
                "text": row["text"],
                "gold": row["gold"],
                "pred": out["intent"],
                "correct": out["intent"] == row["gold"],
                "llm_called": True,
                "tokens_in": out["tokens_in"],
                "tokens_out": out["tokens_out"],
                "latency_s": out["latency_s"],
                "route": decision.reason,
                "raw": out["raw"],
                "parse_path": out["parse_path"],
            }
        records.append(rec)
    return _aggregate("kora", records)


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (pct / 100.0) * (len(ordered) - 1)
    low = int(rank)
    high = min(low + 1, len(ordered) - 1)
    frac = rank - low
    return ordered[low] + (ordered[high] - ordered[low]) * frac


def _aggregate(arm: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(records)
    llm_calls = sum(1 for r in records if r["llm_called"])
    correct = sum(1 for r in records if r["correct"])
    deterministic = n - llm_calls
    all_lat = [r["latency_s"] for r in records]
    llm_lat = [r["latency_s"] for r in records if r["llm_called"]]
    return {
        "arm": arm,
        "n": n,
        "accuracy": correct / n if n else 0.0,
        "correct": correct,
        "llm_calls": llm_calls,
        "deterministic_answers": deterministic,
        "deflection_rate": deterministic / n if n else 0.0,
        "tokens_in": sum(r["tokens_in"] for r in records),
        "tokens_out": sum(r["tokens_out"] for r in records),
        "latency_s_total": sum(all_lat),
        "latency_p50_s": _percentile(all_lat, 50),
        "latency_p95_s": _percentile(all_lat, 95),
        "llm_latency_p50_s": _percentile(llm_lat, 50),
        "llm_latency_p95_s": _percentile(llm_lat, 95),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-dataset direct-vs-kora benchmark.")
    parser.add_argument("--dataset", choices=list(DATASETS), default="clinc_oos")
    parser.add_argument("--n", type=int, default=20, help="number of sampled queries")
    parser.add_argument("--seed", type=int, default=0, help="sampling seed")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--min-score", type=float, default=2.0)
    parser.add_argument("--min-margin", type=float, default=1.0)
    parser.add_argument("--api-key-env", default="VLLM_API_KEY",
                        help="env var holding the API key for the backend")
    parser.add_argument("--out", default=None,
                        help="output JSON (default: results/{dataset}_n{N}_seed{SEED}.json)")
    args = parser.parse_args()

    rows, label_names, oos_label = DATASETS[args.dataset](args.n, args.seed)

    client = OpenAI(
        base_url=args.base_url,
        api_key=os.getenv(args.api_key_env, "EMPTY"),
    )
    clf = LLMClassifier(client, args.model, label_names, args.dataset, oos_label)
    router = KeywordRouter(
        label_names,
        oos_label=oos_label if oos_label is not None else "",
        min_score=args.min_score,
        min_margin=args.min_margin,
    )

    print(f"Loaded {len(rows)} {args.dataset} queries (seed={args.seed}); "
          f"labels={len(label_names)}; oos={oos_label}; model={args.model}")
    print("Running direct arm...")
    direct = run_direct(rows, clf)
    print("Running kora arm...")
    kora = run_kora(rows, clf, router)

    summary = {
        "config": {
            "dataset": args.dataset,
            "n": args.n,
            "seed": args.seed,
            "model": args.model,
            "base_url": args.base_url,
            "min_score": args.min_score,
            "min_margin": args.min_margin,
            "num_labels": len(label_names),
            "oos_label": oos_label,
        },
        "direct": {k: v for k, v in direct.items() if k != "records"},
        "kora": {k: v for k, v in kora.items() if k != "records"},
        "comparison": {
            "accuracy_delta": kora["accuracy"] - direct["accuracy"],
            "llm_calls_saved": direct["llm_calls"] - kora["llm_calls"],
            "llm_calls_saved_pct": (
                (direct["llm_calls"] - kora["llm_calls"]) / direct["llm_calls"]
                if direct["llm_calls"]
                else 0.0
            ),
            "tokens_in_saved": direct["tokens_in"] - kora["tokens_in"],
            "tokens_out_saved": direct["tokens_out"] - kora["tokens_out"],
            "latency_s_saved": direct["latency_s_total"] - kora["latency_s_total"],
        },
    }

    payload = {**summary, "direct_records": direct["records"], "kora_records": kora["records"]}

    out_path = (
        Path(args.out) if args.out
        else RESULTS_DIR / f"{args.dataset}_n{args.n}_seed{args.seed}.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
