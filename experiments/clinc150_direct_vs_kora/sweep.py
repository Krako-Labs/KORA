"""Router threshold sweep over a cached N=500 run.

The LLM predictions are independent of the router thresholds (same model,
prompt, temperature=0), so we reuse the cached direct-arm predictions as the
escalation oracle and only *replay the router* for each (min_score, min_margin)
config. No new LLM calls are made.

For each threshold config we report deflection rate, accuracy, and accuracy loss
vs the direct (always-LLM) baseline. The keyword dictionary in router.py is used
unchanged — only the confidence thresholds vary.

Run:
    HF_HOME=/data/tta/hf-cache \
    ~/kora-ai-champion/envs/kora-benchmark/bin/python \
    experiments/clinc150_direct_vs_kora/sweep.py \
      --cached results/run_n500_seed0.json
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from router import KeywordRouter

RESULTS_DIR = Path(__file__).with_name("results")

# Sweep grid. Defaults (2.0, 1.0) deflected 20.8% at -2.6pt; we sweep upward to
# find conservative thresholds that keep accuracy loss small.
MIN_SCORES = [2.0, 2.5, 3.0, 3.5, 4.0]
MIN_MARGINS = [1.0, 1.5, 2.0, 2.5, 3.0]

ACCURACY_LOSS_BUDGET = 0.005  # <= 0.5pt loss target


def _load_label_names() -> list[str]:
    os.environ.setdefault("HF_DATASETS_OFFLINE", "1")
    from datasets import load_dataset

    ds = load_dataset("clinc_oos", "plus")["test"]
    return list(ds.features["intent"].names)


def evaluate(
    rows: list[dict[str, Any]],
    oracle: dict[str, str],
    label_names: list[str],
    min_score: float,
    min_margin: float,
) -> dict[str, Any]:
    router = KeywordRouter(label_names, min_score=min_score, min_margin=min_margin)
    n = len(rows)
    deflected = 0
    correct = 0
    for r in rows:
        decision = router.route(r["text"])
        if decision.routed:
            deflected += 1
            pred = decision.intent
        else:
            pred = oracle[r["text"]]  # escalate -> cached LLM prediction
        if pred == r["gold"]:
            correct += 1
    return {
        "min_score": min_score,
        "min_margin": min_margin,
        "deflection_rate": deflected / n if n else 0.0,
        "deflected": deflected,
        "llm_calls": n - deflected,
        "accuracy": correct / n if n else 0.0,
        "correct": correct,
        "n": n,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Router threshold sweep.")
    parser.add_argument("--cached", default="results/run_n500_seed0.json")
    parser.add_argument("--out", default="results/sweep_n500_seed0.json")
    args = parser.parse_args()

    cached_path = Path(args.cached)
    if not cached_path.is_absolute():
        cached_path = Path(__file__).with_name(cached_path.parts[0]).joinpath(*cached_path.parts[1:])
    cached = json.loads(cached_path.read_text(encoding="utf-8"))

    direct_records = cached["direct_records"]
    rows = [{"text": r["text"], "gold": r["gold"]} for r in direct_records]
    oracle = {r["text"]: r["pred"] for r in direct_records}
    direct_accuracy = cached["direct"]["accuracy"]
    label_names = _load_label_names()

    results = []
    for ms in MIN_SCORES:
        for mm in MIN_MARGINS:
            res = evaluate(rows, oracle, label_names, ms, mm)
            res["accuracy_loss_vs_direct"] = direct_accuracy - res["accuracy"]
            res["within_budget"] = res["accuracy_loss_vs_direct"] <= ACCURACY_LOSS_BUDGET
            results.append(res)

    # Best conservative config: among those within the 0.5pt loss budget, pick the
    # one with the highest deflection (ties -> higher thresholds = more conservative).
    eligible = [r for r in results if r["within_budget"]]
    best = max(
        eligible,
        key=lambda r: (r["deflection_rate"], r["min_score"], r["min_margin"]),
        default=None,
    )

    payload = {
        "cached_run": str(cached_path.name),
        "direct_accuracy": direct_accuracy,
        "accuracy_loss_budget": ACCURACY_LOSS_BUDGET,
        "grid": {"min_scores": MIN_SCORES, "min_margins": MIN_MARGINS},
        "best_within_budget": best,
        "results": results,
    }
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = RESULTS_DIR / out_path.name
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # Pretty table
    print(f"direct baseline accuracy = {direct_accuracy:.4f}  (loss budget <= {ACCURACY_LOSS_BUDGET*100:.1f}pt)\n")
    print(f"{'min_score':>9} {'min_margin':>10} {'deflect%':>9} {'accuracy':>9} {'acc_loss_pt':>11} {'ok':>3}")
    print("-" * 56)
    for r in results:
        print(
            f"{r['min_score']:>9.1f} {r['min_margin']:>10.1f} "
            f"{r['deflection_rate']*100:>8.1f}% {r['accuracy']:>9.4f} "
            f"{r['accuracy_loss_vs_direct']*100:>10.2f}  {'Y' if r['within_budget'] else '.':>3}"
        )
    print("\nBest conservative config (max deflection within budget):")
    if best:
        print(
            f"  min_score={best['min_score']} min_margin={best['min_margin']} "
            f"-> deflection={best['deflection_rate']*100:.1f}% "
            f"accuracy={best['accuracy']:.4f} loss={best['accuracy_loss_vs_direct']*100:.2f}pt"
        )
    else:
        print("  (none meet the budget)")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
