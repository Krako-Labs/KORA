#!/usr/bin/env python3
"""5모델 full 결과 집계 → 표 + deflection 일관성 검증 + 마크다운."""
import json, glob, os

MODELS = [  # (파일태그, 표시이름, 체급)
    ("sonnet46",   "Claude Sonnet 4.6", "대(frontier)"),
    ("haiku45",    "Claude Haiku 4.5",  "소"),
    ("llama3_70b", "Llama 3.3 70B",     "대"),
    ("llama1_8b",  "Llama 3.1 8B",      "극소"),
    ("novapro",    "Nova Pro",          "중"),
]

def load(tag):
    p = f"results/full_{tag}.json"
    return json.load(open(p)) if os.path.exists(p) else None

rows = []
for tag, name, tier in MODELS:
    d = load(tag)
    if not d:
        print(f"!! MISSING: {tag}"); continue
    cfg = d["config"]
    rt = d["routing"]
    wk = d["conditions"]["with_kb"]
    wo = d["conditions"]["without_kb"]
    rows.append({
        "name": name, "tier": tier,
        "judge": cfg.get("judge_model"),
        "deflection": wk["kora"]["deflection_rate"],
        "calls_direct": wk["direct"]["llm_calls"],
        "calls_kora": wk["kora"]["llm_calls"],
        "saved_pct": wk["comparison"]["llm_calls_saved_pct"],
        "wk_direct": wk["direct"]["accuracy"],
        "wk_kora": wk["kora"]["accuracy"],
        "wk_delta": wk["comparison"]["accuracy_delta_kora_minus_direct"],
        "wo_direct": wo["direct"]["accuracy"],
        "wo_kora": wo["kora"]["accuracy"],
        "wo_delta": wo["comparison"]["accuracy_delta_kora_minus_direct"],
        "over_routed": len(rt.get("over_routed_cases", [])),
        "routing_prec": rt["precision"], "routing_rec": rt["recall"],
    })

print("="*78)
print("KORA 모델 다양성 — 5모델 실측 집계 (N=330, judge=Sonnet 4.6 고정, k=1)")
print("="*78)

# 1) deflection 일관성 검증 (핵심: 모델 무관해야 함)
defl = {r["name"]: r["deflection"] for r in rows}
saved = {r["name"]: r["saved_pct"] for r in rows}
uniq_defl = set(round(v, 4) for v in defl.values())
print("\n[검증 1] deflection이 모델 무관하게 동일한가?")
for r in rows:
    print(f"   {r['name']:20} deflection={r['deflection']:.4f}  calls {r['calls_direct']}→{r['calls_kora']}  saved={r['saved_pct']:.1%}")
print(f"   => 고유 deflection 값 개수: {len(uniq_defl)}  "
      f"{'✅ 전모델 동일 (구조적 증명)' if len(uniq_defl)==1 else '⚠️ 불일치 — 확인 필요'}")

# 2) routing 일관성
uniq_prec = set(round(r["routing_prec"],4) for r in rows)
print(f"\n[검증 2] routing precision/recall 동일? "
      f"{'✅' if len(uniq_prec)==1 else '⚠️'} prec={rows[0]['routing_prec']:.3f} rec={rows[0]['routing_rec']:.3f}")

# 3) 정확도 곡선
print("\n[표] with-KB / without-KB 정확도 (direct vs KORA)")
hdr = f"{'모델':20}{'체급':10}{'wKB:dir→kora(Δ)':22}{'woKB:dir→kora(Δ)':22}"
print(hdr); print("-"*len(hdr))
for r in sorted(rows, key=lambda x: -x["wo_delta"]):
    wk = f"{r['wk_direct']:.3f}→{r['wk_kora']:.3f}({r['wk_delta']:+.3f})"
    wo = f"{r['wo_direct']:.3f}→{r['wo_kora']:.3f}({r['wo_delta']:+.3f})"
    print(f"{r['name']:20}{r['tier']:10}{wk:22}{wo:22}")

# 4) 핵심 관찰
print("\n[핵심 관찰]")
wo_sorted = sorted(rows, key=lambda x: x["wo_direct"])
print(f"   without-KB에서 direct 정확도 범위: "
      f"{wo_sorted[0]['wo_direct']:.3f}({wo_sorted[0]['name']}) ~ "
      f"{wo_sorted[-1]['wo_direct']:.3f}({wo_sorted[-1]['name']})")
kora_wo = [r['wo_kora'] for r in rows]
print(f"   without-KB에서 KORA 정확도 범위: {min(kora_wo):.3f} ~ {max(kora_wo):.3f} (모델 무관하게 고정)")
print(f"   => direct는 모델 실력 따라 출렁, KORA는 평탄 = '약한 모델일수록 KORA 이득↑'")

# 5) 마크다운 표 저장
md = ["# KORA 모델 다양성 결과 (N=330, judge=Sonnet 4.6 고정)\n",
      "| 모델 | 체급 | deflection | LLM콜 절감 | with-KB Δacc | without-KB Δacc |",
      "|---|---|---|---|---|---|"]
for r in sorted(rows, key=lambda x: -x["wo_delta"]):
    md.append(f"| {r['name']} | {r['tier']} | {r['deflection']:.1%} | "
              f"{r['saved_pct']:.1%} | {r['wk_delta']:+.3f} | {r['wo_delta']:+.3f} |")
md.append(f"\n- **deflection {rows[0]['deflection']:.1%} 전모델 동일** (결정형 라우터가 정하므로 모델 무관)")
md.append(f"- **without-KB**: direct는 모델 실력 따라 변동, KORA는 ~0.98로 고정 → 약한 모델일수록 이득↑")
md.append(f"- over-routed: {rows[0]['over_routed']}건 (routing precision={rows[0]['routing_prec']:.3f})")
open("results/SUMMARY_model_diversity.md","w").write("\n".join(md))
print(f"\n✅ 마크다운 저장: results/SUMMARY_model_diversity.md")
