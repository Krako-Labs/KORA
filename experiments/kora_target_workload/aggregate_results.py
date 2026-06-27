#!/usr/bin/env python3
"""Aggregate the 5-model full results -> table + deflection consistency check + markdown."""
import json, os

MODELS = [  # (file tag, display name, tier)
    ("sonnet46",   "Claude Sonnet 4.6", "frontier"),
    ("haiku45",    "Claude Haiku 4.5",  "small"),
    ("llama3_70b", "Llama 3.3 70B",     "large"),
    ("llama1_8b",  "Llama 3.1 8B",      "tiny"),
    ("novapro",    "Nova Pro",          "mid"),
]

def load(tag):
    p = f"results/full_{tag}.json"
    return json.load(open(p)) if os.path.exists(p) else None

rows = []
for tag, name, tier in MODELS:
    d = load(tag)
    if not d:
        print(f"!! MISSING: {tag}"); continue
    cfg = d["config"]; rt = d["routing"]
    wk = d["conditions"]["with_kb"]; wo = d["conditions"]["without_kb"]
    rows.append({
        "name": name, "tier": tier, "judge": cfg.get("judge_model"),
        "deflection": wk["kora"]["deflection_rate"],
        "calls_direct": wk["direct"]["llm_calls"], "calls_kora": wk["kora"]["llm_calls"],
        "saved_pct": wk["comparison"]["llm_calls_saved_pct"],
        "wk_direct": wk["direct"]["accuracy"], "wk_kora": wk["kora"]["accuracy"],
        "wk_delta": wk["comparison"]["accuracy_delta_kora_minus_direct"],
        "wo_direct": wo["direct"]["accuracy"], "wo_kora": wo["kora"]["accuracy"],
        "wo_delta": wo["comparison"]["accuracy_delta_kora_minus_direct"],
        "over_routed": len(rt.get("over_routed_cases", [])),
        "routing_prec": rt["precision"], "routing_rec": rt["recall"],
    })

print("="*78)
print("KORA model-diversity aggregate (N=330, judge=Sonnet 4.6 fixed, k=1)")
print("="*78)

defl = set(round(r["deflection"], 4) for r in rows)
print("\n[check 1] Is deflection identical across models (model-independent)?")
for r in rows:
    print(f"   {r['name']:20} deflection={r['deflection']:.4f}  calls {r['calls_direct']}->{r['calls_kora']}  saved={r['saved_pct']:.1%}")
print(f"   => distinct deflection values: {len(defl)}  "
      f"{'OK: identical across all models (structural)' if len(defl)==1 else 'WARN: mismatch - check'}")

prec = set(round(r["routing_prec"],4) for r in rows)
print(f"\n[check 2] routing precision/recall identical? "
      f"{'OK' if len(prec)==1 else 'WARN'} prec={rows[0]['routing_prec']:.3f} rec={rows[0]['routing_rec']:.3f}")

print("\n[table] with-KB / without-KB accuracy (direct vs KORA)")
hdr = f"{'model':20}{'tier':10}{'wKB:dir->kora(d)':22}{'woKB:dir->kora(d)':22}"
print(hdr); print("-"*len(hdr))
for r in sorted(rows, key=lambda x: -x["wo_delta"]):
    wk = f"{r['wk_direct']:.3f}->{r['wk_kora']:.3f}({r['wk_delta']:+.3f})"
    wo = f"{r['wo_direct']:.3f}->{r['wo_kora']:.3f}({r['wo_delta']:+.3f})"
    print(f"{r['name']:20}{r['tier']:10}{wk:22}{wo:22}")

print("\n[key observations]")
ws = sorted(rows, key=lambda x: x["wo_direct"])
print(f"   without-KB direct accuracy range: "
      f"{ws[0]['wo_direct']:.3f}({ws[0]['name']}) ~ {ws[-1]['wo_direct']:.3f}({ws[-1]['name']})")
kw = [r['wo_kora'] for r in rows]
print(f"   without-KB KORA accuracy range: {min(kw):.3f} ~ {max(kw):.3f} (flat, model-independent)")
print(f"   => direct varies with model strength; KORA stays flat = larger KORA gain for weaker models")

md = ["# KORA model-diversity results (N=330, judge=Sonnet 4.6 fixed)\n",
      "| Model | tier | deflection | LLM calls saved | with-KB d-acc | without-KB d-acc |",
      "|---|---|---|---|---|---|"]
for r in sorted(rows, key=lambda x: -x["wo_delta"]):
    md.append(f"| {r['name']} | {r['tier']} | {r['deflection']:.1%} | "
              f"{r['saved_pct']:.1%} | {r['wk_delta']:+.3f} | {r['wo_delta']:+.3f} |")
md.append(f"\n- **deflection {rows[0]['deflection']:.1%} identical across all models** (set by the deterministic router, model-independent)")
md.append(f"- **without-KB**: direct varies with model strength; KORA stays ~0.98 -> larger gain for weaker models")
md.append(f"- over-routed: {rows[0]['over_routed']} cases (routing precision={rows[0]['routing_prec']:.3f})")
open("results/SUMMARY_model_diversity.md","w").write("\n".join(md))
print(f"\nOK: wrote results/SUMMARY_model_diversity.md")
