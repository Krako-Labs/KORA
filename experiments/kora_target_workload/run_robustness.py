"""KORA routing-robustness harness (zero LLM calls).

For each intent-preserving paraphrase transform, build a paraphrased copy of the
workload, run the deterministic dispatcher over it (no key, no GPU, no model
calls), and compare per-case routing decisions against the original workload.

Decision changes are bucketed as:
  * DANGEROUS flip : should_escalate == True,  original ESCALATED, variant DEFLECTED
                     (a trap/reasoning case slipped past the front door ->
                      false deflection -> SAFETY failure). Target: 0.
  * benign flip    : should_escalate == False, original DEFLECTED, variant ESCALATED
                     (a deterministically-answerable case bounced to the LLM ->
                      cost only, no safety impact).
  * other flip     : any remaining decision change (reported for completeness).

Per-variant deflection rate and escalation precision/recall are reported next to
the original so robustness shows up as a delta. The dispatcher is reused
directly (same code path as run.py --routing-only, see run.py L485), so results
are consistent with the committed routing pipeline.

Usage:
    python run_robustness.py --workload workloads/full.json \
        --out results/robustness/robustness.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from kora import dispatcher  # noqa: E402
from paraphrase import TRANSFORMS, apply_transform  # noqa: E402


def route_all(cases: list[dict]) -> list[bool]:
    """Return per-case ESCALATED flags (True = front door abstained -> LLM)."""
    return [not dispatcher.dispatch(c["text"], c.get("payload")).routed for c in cases]


def routing_metrics(cases: list[dict], escalated: list[bool]) -> dict:
    """Confusion matrix with positive = should_escalate, plus deflection rate."""
    tp = fp = tn = fn = 0
    for c, esc in zip(cases, escalated):
        should = c["should_escalate"]
        if should and esc:
            tp += 1
        elif should and not esc:
            fn += 1
        elif not should and not esc:
            tn += 1
        else:
            fp += 1
    n = len(cases)
    routed = sum(1 for e in escalated if not e)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return {
        "n": n, "routed": routed,
        "deflection_rate": routed / n if n else 0.0,
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "precision": precision, "recall": recall,
    }


def classify_flips(cases, base_esc, var_esc) -> dict:
    """Compare original vs variant per case; bucket the decision changes."""
    dangerous, benign, other = [], [], []
    for c, b, v in zip(cases, base_esc, var_esc):
        if b == v:
            continue
        rec = {
            "id": c["id"], "category": c["category"],
            "should_escalate": c["should_escalate"],
            "orig": "escalate" if b else "deflect",
            "variant": "escalate" if v else "deflect",
            "text": c["text"],
        }
        if c["should_escalate"] and b and not v:
            dangerous.append(rec)
        elif (not c["should_escalate"]) and (not b) and v:
            benign.append(rec)
        else:
            other.append(rec)
    return {"dangerous": dangerous, "benign": benign, "other": other}


def main() -> None:
    ap = argparse.ArgumentParser(description="KORA routing robustness (0 LLM calls).")
    ap.add_argument("--workload", default="workloads/full.json")
    ap.add_argument("--out", default="results/robustness/robustness.json")
    args = ap.parse_args()

    data = json.loads(Path(args.workload).read_text(encoding="utf-8"))
    cases = data["cases"]

    base_esc = route_all(cases)
    base_metrics = routing_metrics(cases, base_esc)

    variants = {}
    for name in TRANSFORMS:
        v_cases = apply_transform(cases, name)
        v_esc = route_all(v_cases)
        v_metrics = routing_metrics(v_cases, v_esc)
        flips = classify_flips(cases, base_esc, v_esc)
        variants[name] = {
            "metrics": v_metrics,
            "n_dangerous": len(flips["dangerous"]),
            "n_benign": len(flips["benign"]),
            "n_other": len(flips["other"]),
            "flips": flips,
        }

    report = {
        "workload": args.workload,
        "n_cases": len(cases),
        "original": base_metrics,
        "variants": variants,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    o = base_metrics
    print(f"workload: {args.workload}  ({len(cases)} cases)")
    print(f"original: deflection={o['deflection_rate']:.3f} "
          f"precision={o['precision']:.3f} recall={o['recall']:.3f} "
          f"(tp={o['tp']} fp={o['fp']} tn={o['tn']} fn={o['fn']})")
    print()
    print(f"{'transform':14} {'defl':>6} {'prec':>6} {'rec':>6}  "
          f"{'DANGER':>6} {'benign':>6} {'other':>6}")
    total_danger = 0
    for name, v in variants.items():
        m = v["metrics"]
        total_danger += v["n_dangerous"]
        print(f"{name:14} {m['deflection_rate']:6.3f} {m['precision']:6.3f} "
              f"{m['recall']:6.3f}  {v['n_dangerous']:6d} {v['n_benign']:6d} "
              f"{v['n_other']:6d}")
    print()
    if total_danger == 0:
        print("OK: 0 dangerous flips across all transforms "
              "(no should-escalate case was paraphrased into a deflection).")
    else:
        print(f"!! {total_danger} DANGEROUS flip(s) — listing:")
        for name, v in variants.items():
            for rec in v["flips"]["dangerous"]:
                print(f"   [{name}] {rec['id']} ({rec['category']}): "
                      f"{rec['orig']} -> {rec['variant']}  :: {rec['text']!r}")
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
