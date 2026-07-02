"""Deflection safety analysis across benchmark result files.

For every result JSON produced by run_multi.py (or run.py) that contains
per-case records, this script quantifies where deflection helps and where it
costs accuracy:

  * router accuracy on deflected cases vs LLM accuracy on escalated cases
  * net loss cases (router wrong, direct LLM right) and net gain cases
    (router right, direct LLM wrong)
  * the gold -> predicted confusion pairs behind the losses

The goal is to characterize the safety boundary of pre-inference deflection:
whether accuracy cost, when present, is concentrated in semantically
overlapping labels rather than arbitrary misroutes.

Usage:
    python analyze_deflection.py [results_dir]
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def analyze_file(path: Path) -> dict | None:
    d = json.loads(path.read_text())
    kora = d.get("kora_records")
    direct = d.get("direct_records")
    if not kora or not direct:
        return None

    defl = [(k, dr) for k, dr in zip(kora, direct) if not k["llm_called"]]
    esc = [k for k in kora if k["llm_called"]]

    n_defl, n_esc = len(defl), len(esc)
    router_ok = sum(1 for k, _ in defl if k["correct"])
    esc_ok = sum(1 for k in esc if k["correct"])

    loss = [(k, dr) for k, dr in defl if not k["correct"] and dr["correct"]]
    gain = [(k, dr) for k, dr in defl if k["correct"] and not dr["correct"]]
    loss_pairs = Counter((k["gold"], k["pred"]) for k, _ in loss)

    cfg = d.get("config", {})
    return {
        "file": path.name,
        "dataset": cfg.get("dataset", "clinc_oos"),
        "seed": cfg.get("seed", "?"),
        "n": cfg.get("n", len(kora)),
        "deflected": n_defl,
        "escalated": n_esc,
        "deflection_rate": n_defl / (n_defl + n_esc) if (n_defl + n_esc) else 0.0,
        "router_acc_on_deflected": router_ok / n_defl if n_defl else None,
        "llm_acc_on_escalated": esc_ok / n_esc if n_esc else None,
        "net_loss_cases": len(loss),
        "net_gain_cases": len(gain),
        "accuracy_delta": d.get("comparison", {}).get("accuracy_delta"),
        "top_loss_pairs": [
            {"gold": g, "pred": p, "count": c} for (g, p), c in loss_pairs.most_common(10)
        ],
    }


def main() -> None:
    results_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("results")
    reports = []
    for path in sorted(results_dir.glob("*.json")):
        if path.name.startswith("deflection_analysis"):
            continue
        r = analyze_file(path)
        if r:
            reports.append(r)

    if not reports:
        print(f"No result files with per-case records found in {results_dir}")
        return

    print(f"{'dataset':<12} {'seed':>4} {'defl%':>6} {'router@defl':>12} {'llm@esc':>8} "
          f"{'loss':>5} {'gain':>5} {'d_acc':>7}")
    for r in reports:
        ra = f"{r['router_acc_on_deflected']:.3f}" if r["router_acc_on_deflected"] is not None else "n/a"
        ea = f"{r['llm_acc_on_escalated']:.3f}" if r["llm_acc_on_escalated"] is not None else "n/a"
        print(f"{r['dataset']:<12} {r['seed']:>4} {r['deflection_rate']*100:>5.1f}% "
              f"{ra:>12} {ea:>8} {r['net_loss_cases']:>5} {r['net_gain_cases']:>5} "
              f"{(r['accuracy_delta'] or 0)*100:>+6.1f}p")

    out = results_dir / "deflection_analysis.json"
    out.write_text(json.dumps(reports, indent=2))
    print(f"\nWrote {out}")


def _unused() -> None:  # keep module import-safe for harness reuse
    pass


if __name__ == "__main__":
    main()
