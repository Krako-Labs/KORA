"""Direct-vs-KORA real-inference smoke on CLINC150.

Two arms classify the same N sampled CLINC150 queries against the local vLLM
server (Qwen/Qwen2.5-32B-Instruct):

  * direct : every query goes to the LLM.
  * kora   : a deterministic keyword router answers easy queries; only the ones
             it abstains on are escalated to the LLM.

We report accuracy, LLM-call count, token usage and latency for both arms so the
routing economics (fewer LLM calls / tokens at comparable accuracy) are visible.

Run:
    HF_HOME=~/.cache/huggingface \
    ~/kora-ai-champion/envs/kora-benchmark/bin/python \
    experiments/clinc150_direct_vs_kora/run.py --n 20 --seed 0
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any

from openai import OpenAI

from intent_parser import parse_intent
from router import KeywordRouter

DEFAULT_BASE_URL = "http://localhost:8000/v1"
DEFAULT_MODEL = "Qwen/Qwen2.5-32B-Instruct"
RESULTS_DIR = Path(__file__).with_name("results")


# --------------------------------------------------------------------------- #
# Dataset
# --------------------------------------------------------------------------- #
def load_clinc_sample(n: int, seed: int) -> tuple[list[dict[str, Any]], list[str]]:
    """Load CLINC150 (plus) test split and return a shuffled sample + label names."""
    os.environ.setdefault("HF_DATASETS_OFFLINE", "1")
    from datasets import load_dataset

    ds = load_dataset("clinc_oos", "plus")["test"]
    label_names = list(ds.features["intent"].names)

    sample = ds.shuffle(seed=seed).select(range(n))
    rows = [
        {"text": ex["text"], "gold": label_names[ex["intent"]]}
        for ex in sample
    ]
    return rows, label_names


# --------------------------------------------------------------------------- #
# LLM classifier (shared by both arms)
# --------------------------------------------------------------------------- #
class LLMClassifier:
    def __init__(self, client: OpenAI, model: str, label_names: list[str]) -> None:
        self.client = client
        self.model = model
        self.label_names = label_names
        self._label_set = set(label_names)
        self._label_block = ", ".join(label_names)

    def classify(self, text: str) -> dict[str, Any]:
        """Return {intent, raw, tokens_in, tokens_out, latency_s}."""
        system = (
            "You are an intent classifier for the CLINC150 dataset. "
            "Given a user utterance, choose the single best matching intent from the "
            "provided list. If none of the in-scope intents apply, answer 'oos'. "
            'Respond with JSON only: {"intent": "<label>"}. No prose.'
        )
        user = f"Allowed intents: {self._label_block}\n\nUtterance: {text}"

        # NOTE: we deliberately do NOT use response_format / guided decoding here.
        # vLLM 0.6.6.post1's xgrammar backend crashes the engine with
        # "TokenizerInfo has no attribute 'from_huggingface'" on guided requests,
        # so we rely on prompt-enforced JSON + robust parsing in intent_parser.
        start = time.monotonic()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.0,
            max_tokens=30,
        )
        latency_s = time.monotonic() - start

        raw = resp.choices[0].message.content or ""
        intent, parse_path = parse_intent(
            raw, self.label_names, self._label_set, "oos"
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


# --------------------------------------------------------------------------- #
# Arms
# --------------------------------------------------------------------------- #
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
    """Linear-interpolated percentile (pct in [0, 100]). Empty -> 0.0."""
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
    # End-to-end per-query latency (deterministic answers are ~0s) and the
    # LLM-call-only latency distribution, both as p50/p95.
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


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description="CLINC150 direct-vs-kora smoke.")
    parser.add_argument("--n", type=int, default=20, help="number of sampled queries")
    parser.add_argument("--seed", type=int, default=0, help="sampling seed")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--min-score", type=float, default=2.0)
    parser.add_argument("--min-margin", type=float, default=1.0)
    parser.add_argument(
        "--out",
        default=None,
        help="output JSON path (default: results/smoke_n{N}_seed{SEED}.json)",
    )
    args = parser.parse_args()

    rows, label_names = load_clinc_sample(args.n, args.seed)
    client = OpenAI(base_url=args.base_url, api_key=os.getenv("VLLM_API_KEY", "EMPTY"))
    clf = LLMClassifier(client, args.model, label_names)
    router = KeywordRouter(
        label_names, min_score=args.min_score, min_margin=args.min_margin
    )

    print(f"Loaded {len(rows)} CLINC150 queries (seed={args.seed}); model={args.model}")
    print("Running direct arm...")
    direct = run_direct(rows, clf)
    print("Running kora arm...")
    kora = run_kora(rows, clf, router)

    summary = {
        "config": {
            "n": args.n,
            "seed": args.seed,
            "model": args.model,
            "base_url": args.base_url,
            "min_score": args.min_score,
            "min_margin": args.min_margin,
            "num_labels": len(label_names),
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
        Path(args.out)
        if args.out
        else RESULTS_DIR / f"smoke_n{args.n}_seed{args.seed}.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
