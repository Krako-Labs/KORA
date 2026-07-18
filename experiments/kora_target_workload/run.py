"""KORA target-workload benchmark: direct (all-LLM) vs kora (deterministic
front-door + escalate) on the same ground truth.

For every case the harness shows BOTH arms only `text` + `payload` (never the
category or ground truth):

  * direct : 1 LLM call per case.
  * kora   : kora/dispatcher.dispatch(); routed -> deterministic answer (0 LLM
             calls); abstain -> escalate to the same LLM. KORA accuracy =
             deterministic answers + escalated LLM answers (Safety Guard #2: any
             routed-but-wrong case is reported, not hidden).

Two LLM conditions are measured (main numbers = with-KB):
  (a) with_kb    : KB facts + policy rules are placed in the LLM prompt (fairest
                   baseline — the LLM gets the same source of truth KORA's
                   handlers use).
  (b) without_kb : parametric knowledge only (realistic, secondary check).

Metrics: accuracy (overall + per category over the scorable categories
format/faq/policy), LLM-call count, token usage, latency, escalation-routing
precision/recall (deterministic, KB-independent), and optional consistency
(K resamples of the LLM arm at a higher temperature -> answer variance).

Run (smoke):
    HF_HOME=~/.cache/huggingface \
    ~/kora-ai-champion/envs/kora-benchmark/bin/python \
        experiments/kora_target_workload/run.py --workload workloads/smoke.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import yaml  # noqa: E402
# `openai` is imported lazily, only when an OpenAI/vLLM client is actually
# constructed (see main()). The --routing-only path and the bedrock backend make
# no OpenAI calls, so they must not require the `openai` package to be installed.
from bedrock_client import BedrockClient  # noqa: E402

from kora import dispatcher  # noqa: E402

DEFAULT_BASE_URL = "http://localhost:8000/v1"
DEFAULT_MODEL = "Qwen/Qwen2.5-32B-Instruct"
SPEC_DIR = HERE / "spec"
RESULTS_DIR = HERE / "results"

SCORABLE_KINDS = ("valid_invalid", "eligibility", "kb_answer")
VERDICTS = ("valid", "invalid", "eligible", "ineligible")


# --------------------------------------------------------------------------- #
# Prompt construction
# --------------------------------------------------------------------------- #
SYSTEM_BASE = (
    "You are a customer-support assistant for the online store Northwind Goods. "
    "Answer the user's request.\n"
    "- If the user asks whether a specific value is a valid email address, phone "
    "number, or calendar date, decide and set verdict to exactly \"valid\" or "
    "\"invalid\".\n"
    "- If the user asks an eligibility or policy question and gives structured "
    "details, decide and set verdict to exactly \"eligible\" or \"ineligible\".\n"
    "- Otherwise set verdict to null and put a concise, helpful reply in answer.\n"
    'Respond with JSON only: {"verdict": <"valid"|"invalid"|"eligible"|'
    '"ineligible"|null>, "answer": "<concise answer>"}. No text outside the JSON.'
)


def build_kb_block() -> str:
    kb = yaml.safe_load((SPEC_DIR / "kb.yaml").read_text(encoding="utf-8"))
    pol = yaml.safe_load((SPEC_DIR / "policies.yaml").read_text(encoding="utf-8"))
    lines = ["", "Knowledge Base (authoritative facts):"]
    for f in kb["facts"]:
        lines.append(f"- Q: {f['canonical_question']} A: {f['answer']}")
    lines.append("")
    lines.append("Policies (authoritative rules; evaluate over the structured details):")
    for p in pol["policies"]:
        fields = ", ".join(p["fields"].keys())
        rule = " ".join(p["rule"].split())
        lines.append(f"- {p['id']} ({p['title']}). Fields: {fields}. Rule: {rule}")
    return "\n".join(lines)


def system_prompt(with_kb: bool, kb_block: str) -> str:
    return SYSTEM_BASE + (("\n" + kb_block) if with_kb else "")


def user_prompt(case: dict) -> str:
    msg = case["text"]
    if case.get("payload") is not None:
        msg += "\nStructured details (JSON): " + json.dumps(case["payload"])
    return msg


# --------------------------------------------------------------------------- #
# LLM client
# --------------------------------------------------------------------------- #
class LLM:
    def __init__(self, client: OpenAI, model: str) -> None:
        self.client = client
        self.model = model

    def judge_faq(self, question: str, canonical: str, answer: str) -> bool:
        """Semantic FAQ grader: does `answer` convey the same key fact as the
        frozen canonical answer? Evaluation infra — not counted as a serving call."""
        sys = (
            "You are a strict grader. Decide if a candidate response conveys the "
            "same key fact as the canonical correct answer to a customer question. "
            "Ignore wording, politeness, and extra detail; judge only whether the "
            'key fact matches. Respond JSON only: {"correct": true|false}.'
        )
        user = (f"Question: {question}\nCanonical correct answer: {canonical}\n"
                f"Candidate response: {answer}\nDoes the candidate convey the same "
                "key fact as the canonical answer?")
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": sys},
                      {"role": "user", "content": user}],
            temperature=0.0, max_tokens=16,
        )
        raw = resp.choices[0].message.content or ""
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                return json.loads(m.group(0)).get("correct") is True
            except (json.JSONDecodeError, AttributeError):
                pass
        low = raw.lower()
        return "true" in low and "false" not in low

    def call(self, system: str, user: str, temperature: float) -> dict[str, Any]:
        t0 = time.time()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            temperature=temperature,
            max_tokens=256,
        )
        latency = time.time() - t0
        raw = resp.choices[0].message.content or ""
        verdict, answer = parse_llm(raw)
        usage = resp.usage
        return {
            "verdict": verdict,
            "answer": answer,
            "raw": raw,
            "tokens_in": getattr(usage, "prompt_tokens", 0) or 0,
            "tokens_out": getattr(usage, "completion_tokens", 0) or 0,
            "latency_s": latency,
        }


def parse_llm(raw: str) -> tuple[str | None, str]:
    """Robustly pull {verdict, answer} from the model text (no guided decoding)."""
    verdict: str | None = None
    answer = raw.strip()
    m = re.search(r"\{.*\}", raw, re.S)
    if m:
        try:
            obj = json.loads(m.group(0))
            v = obj.get("verdict")
            if isinstance(v, str) and v.strip().lower() in VERDICTS:
                verdict = v.strip().lower()
            a = obj.get("answer")
            if isinstance(a, str):
                answer = a
        except (json.JSONDecodeError, AttributeError):
            pass
    return verdict, answer


# --------------------------------------------------------------------------- #
# Scoring (uniform for both arms)
# --------------------------------------------------------------------------- #
def score(case: dict, verdict: str | None, answer: str) -> bool | None:
    kind = case["gt_kind"]
    gt = case["ground_truth"]
    if kind == "valid_invalid":
        v = verdict or _fallback_verdict(answer, ("invalid", "valid"))
        return v == gt
    if kind == "eligibility":
        v = verdict or _fallback_verdict(answer, ("ineligible", "eligible"))
        return v == gt
    if kind == "kb_answer":
        a = answer.lower()
        return all(k in a for k in gt)
    return None  # freeform: not scored for accuracy


def _fallback_verdict(answer: str, ordered: tuple[str, str]) -> str | None:
    """Check the longer/negative token first ('invalid' before 'valid')."""
    a = answer.lower()
    for tok in ordered:
        if tok in a:
            return tok
    return None


def grade_case(case: dict, verdict: str | None, answer: str, faq_grader) -> bool | None:
    """Accuracy grading. Verdict categories use exact match; FAQ uses the
    pluggable `faq_grader` (substring or LLM judge)."""
    kind = case["gt_kind"]
    if kind in ("valid_invalid", "eligibility"):
        return score(case, verdict, answer)
    if kind == "kb_answer":
        return faq_grader(case, answer)
    return None


def make_faq_grader(mode: str, llm: "LLM"):
    if mode == "judge":
        return lambda case, answer: llm.judge_faq(
            case["text"], case["meta"]["canonical_answer"], answer)
    return lambda case, answer: all(k in answer.lower() for k in case["ground_truth"])


# --------------------------------------------------------------------------- #
# Routing metrics (deterministic; identical across KB conditions)
# --------------------------------------------------------------------------- #
def routing_report(cases: list[dict], decisions: dict[str, dispatcher.Decision]) -> dict:
    tp = fp = tn = fn = 0
    by_cat = defaultdict(lambda: {"n": 0, "routed": 0, "abstain": 0})
    over_routed = []
    for c in cases:
        d = decisions[c["id"]]
        cat = c["category"]
        by_cat[cat]["n"] += 1
        by_cat[cat]["routed" if d.routed else "abstain"] += 1
        should, escalated = c["should_escalate"], (not d.routed)
        if should and escalated:
            tp += 1
        elif should and not escalated:
            fn += 1
            over_routed.append({"id": c["id"], "category": cat,
                                "handler": d.handler, "answer": d.answer})
        elif not should and not escalated:
            tn += 1
        else:
            fp += 1
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    return {
        "positive_class": "should_escalate",
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "precision": prec, "recall": rec,
        "by_category": {k: dict(v) for k, v in by_cat.items()},
        "over_routed_cases": over_routed,
    }


# --------------------------------------------------------------------------- #
# Arms
# --------------------------------------------------------------------------- #
def make_record(case: dict, verdict: str | None, answer: str, correct: bool | None,
                llm_called: bool, tokens_in: int, tokens_out: int, latency_s: float,
                routed: bool | None = None, handler: str | None = None) -> dict:
    return {
        "id": case["id"],
        "category": case["category"],
        "gt_kind": case["gt_kind"],
        "scorable": case["gt_kind"] in SCORABLE_KINDS,
        "correct": correct,
        "llm_called": llm_called,
        "routed_deterministic": routed,
        "handler": handler,
        "verdict": verdict,
        "answer": answer[:200],
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "latency_s": latency_s,
    }


def run_direct(cases: list[dict], llm_results: dict[str, list[dict]], faq_grader) -> list[dict]:
    records = []
    for c in cases:
        r = llm_results[c["id"]][0]
        correct = grade_case(c, r["verdict"], r["answer"], faq_grader)
        records.append(make_record(c, r["verdict"], r["answer"], correct, True,
                                    r["tokens_in"], r["tokens_out"], r["latency_s"]))
    return records


def run_kora(cases: list[dict], llm_results: dict[str, list[dict]],
             decisions: dict[str, dispatcher.Decision], faq_grader) -> list[dict]:
    records = []
    for c in cases:
        d = decisions[c["id"]]
        if d.routed:
            verdict = d.answer if d.answer in VERDICTS else None
            # routed FAQ returns the frozen canonical answer -> correct by
            # construction (not re-judged); format/policy use exact verdict match.
            if c["gt_kind"] == "kb_answer":
                correct: bool | None = True
            else:
                correct = grade_case(c, verdict, d.answer, faq_grader)
            records.append(make_record(c, verdict, d.answer, correct, False, 0, 0, 0.0,
                                        routed=True, handler=d.handler))
        else:
            r = llm_results[c["id"]][0]
            correct = grade_case(c, r["verdict"], r["answer"], faq_grader)
            records.append(make_record(c, r["verdict"], r["answer"], correct, True,
                                        r["tokens_in"], r["tokens_out"], r["latency_s"],
                                        routed=False, handler=None))
    return records


def _pct(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    rank = (pct / 100.0) * (len(s) - 1)
    lo = int(rank)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (rank - lo)


def aggregate(arm: str, records: list[dict], price_in: float, price_out: float) -> dict:
    scorable = [r for r in records if r["scorable"]]
    correct = sum(1 for r in scorable if r["correct"])
    by_cat = defaultdict(lambda: {"n": 0, "correct": 0})
    for r in scorable:
        by_cat[r["category"]]["n"] += 1
        by_cat[r["category"]]["correct"] += int(bool(r["correct"]))
    cat_acc = {k: {"n": v["n"], "correct": v["correct"],
                   "accuracy": v["correct"] / v["n"] if v["n"] else 0.0}
               for k, v in by_cat.items()}
    llm_calls = sum(1 for r in records if r["llm_called"])
    tokens_in = sum(r["tokens_in"] for r in records)
    tokens_out = sum(r["tokens_out"] for r in records)
    all_lat = [r["latency_s"] for r in records]
    return {
        "arm": arm,
        "n_total": len(records),
        "n_scorable": len(scorable),
        "accuracy": correct / len(scorable) if scorable else 0.0,
        "correct": correct,
        "accuracy_by_category": cat_acc,
        "llm_calls": llm_calls,
        "deterministic_answers": len(records) - llm_calls,
        "deflection_rate": (len(records) - llm_calls) / len(records) if records else 0.0,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "estimated_cost_usd": (tokens_in * price_in + tokens_out * price_out) / 1_000_000,
        "latency_s_total": sum(all_lat),
        "latency_p50_s": _pct(all_lat, 50),
        "latency_p95_s": _pct(all_lat, 95),
    }


def collect_errors(records: list[dict], cases_by_id: dict[str, dict]) -> list[dict]:
    """Every scorable mismatch, surfaced in full (Safety Guard #2)."""
    errs = []
    for r in records:
        if r["scorable"] and not r["correct"]:
            c = cases_by_id[r["id"]]
            errs.append({
                "id": r["id"], "category": r["category"], "gt_kind": r["gt_kind"],
                "ground_truth": c["ground_truth"],
                "verdict": r["verdict"], "answer": r["answer"],
                "llm_called": r["llm_called"], "handler": r["handler"],
                "text": c["text"], "payload": c.get("payload"),
            })
    return errs


def compare(direct: dict, kora: dict) -> dict:
    def saved(a, b):
        return a - b
    return {
        "accuracy_delta_kora_minus_direct": kora["accuracy"] - direct["accuracy"],
        "llm_calls_saved": saved(direct["llm_calls"], kora["llm_calls"]),
        "llm_calls_saved_pct": (saved(direct["llm_calls"], kora["llm_calls"]) /
                                direct["llm_calls"]) if direct["llm_calls"] else 0.0,
        "tokens_in_saved": saved(direct["tokens_in"], kora["tokens_in"]),
        "tokens_out_saved": saved(direct["tokens_out"], kora["tokens_out"]),
        "cost_saved_usd": saved(direct["estimated_cost_usd"], kora["estimated_cost_usd"]),
        "latency_s_saved": saved(direct["latency_s_total"], kora["latency_s_total"]),
    }


# --------------------------------------------------------------------------- #
# Consistency (LLM answer variance across K resamples)
# --------------------------------------------------------------------------- #
def consistency_report(cases: list[dict], llm_results: dict[str, list[dict]], k: int) -> dict:
    if k <= 1:
        return {"k": k, "measured": False}
    by_cat = defaultdict(lambda: {"n": 0, "stable": 0})
    unstable = []
    for c in cases:
        if c["gt_kind"] not in SCORABLE_KINDS:
            continue
        outcomes = set()
        for r in llm_results[c["id"]][:k]:
            if c["gt_kind"] in ("valid_invalid", "eligibility"):
                v = r["verdict"] or _fallback_verdict(
                    r["answer"], ("invalid", "valid") if c["gt_kind"] == "valid_invalid"
                    else ("ineligible", "eligible"))
                outcomes.add(v)
            else:  # kb_answer: stability of correctness
                outcomes.add(bool(score(c, r["verdict"], r["answer"])))
        by_cat[c["category"]]["n"] += 1
        stable = len(outcomes) == 1
        by_cat[c["category"]]["stable"] += int(stable)
        if not stable:
            unstable.append({"id": c["id"], "category": c["category"],
                             "distinct_outcomes": sorted(map(str, outcomes))})
    n = sum(v["n"] for v in by_cat.values())
    stable = sum(v["stable"] for v in by_cat.values())
    return {
        "k": k, "measured": True,
        "n_scorable": n,
        "stable": stable,
        "consistency_rate": stable / n if n else 0.0,
        "by_category": {kk: {"n": vv["n"], "stable": vv["stable"],
                             "consistency_rate": vv["stable"] / vv["n"] if vv["n"] else 0.0}
                        for kk, vv in by_cat.items()},
        "unstable_cases": unstable,
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def collect_llm(cases: list[dict], llm: LLM, system: str, k: int, temp: float,
                cons_temp: float) -> dict[str, list[dict]]:
    """One pass over all cases. Sample 0 at `temp` (accuracy); samples 1..k-1 at
    `cons_temp` (consistency)."""
    out: dict[str, list[dict]] = {}
    for i, c in enumerate(cases):
        up = user_prompt(c)
        samples = [llm.call(system, up, temp)]
        for _ in range(max(0, k - 1)):
            samples.append(llm.call(system, up, cons_temp))
        out[c["id"]] = samples
        if (i + 1) % 20 == 0:
            print(f"    ... {i + 1}/{len(cases)} cases")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="KORA target-workload direct-vs-kora run.")
    ap.add_argument("--workload", default="workloads/smoke.json")
    ap.add_argument("--conditions", choices=["both", "with_kb", "without_kb"], default="both")
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--backend", choices=["openai", "bedrock"], default="openai",
                    help="openai=vLLM/local, bedrock=AWS Converse")
    ap.add_argument("--region", default="us-east-1", help="Bedrock region")
    ap.add_argument("--judge-model", default=None,
                    help="Fixed FAQ judge model (defaults to the served model). For cross-model comparison, use the same value across all arms.")
    ap.add_argument("--temperature", type=float, default=0.0, help="accuracy-pass temperature")
    ap.add_argument("--k", type=int, default=1, help="LLM resamples per case (>=2 enables consistency)")
    ap.add_argument("--consistency-temperature", type=float, default=0.7)
    ap.add_argument("--faq-grader", choices=["judge", "substring"], default="judge",
                    help="FAQ accuracy grader (judge=semantic vs canonical; substring=frozen keys)")
    ap.add_argument("--limit", type=int, default=0, help="use only first N cases (plumbing test)")
    ap.add_argument("--price-in", type=float, default=0.0, help="USD per 1M input tokens")
    ap.add_argument("--price-out", type=float, default=0.0, help="USD per 1M output tokens")
    ap.add_argument("--out", default=None)
    ap.add_argument("--routing-only", action="store_true",
                    help="Compute/save deterministic routing only and exit (no LLM/key/GPU; fully reproducible)")
    args = ap.parse_args()

    wl_path = Path(args.workload)
    if not wl_path.is_absolute():
        wl_path = HERE / wl_path
    workload = json.loads(wl_path.read_text(encoding="utf-8"))
    cases = workload["cases"]
    if args.limit:
        cases = cases[:args.limit]

    # deterministic routing (KB-independent) -------------------------------- #
    decisions = {c["id"]: dispatcher.dispatch(c["text"], c.get("payload")) for c in cases}
    routing = routing_report(cases, decisions)

    if args.routing_only:
        payload = {
            "config": {"workload": str(wl_path.name), "n_cases": len(cases),
                       "mode": "routing_only", "generated_with": workload.get("generated_with")},
            "routing": routing,
        }
        out = args.out or 'results/routing_only.json'
        import os as _os; _os.makedirs(_os.path.dirname(out), exist_ok=True) if _os.path.dirname(out) else None
        open(out, 'w').write(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"[routing-only] deflection computed (0 LLM calls). -> {out}")
        print(f"  precision={routing['precision']:.3f} recall={routing['recall']:.3f}")
        return

    if args.backend == "bedrock":
        client = BedrockClient(region=args.region)
    else:
        from openai import OpenAI  # lazy: only the vLLM/OpenAI backend needs it
        client = OpenAI(base_url=args.base_url, api_key=os.getenv("VLLM_API_KEY", "EMPTY"))
    llm = LLM(client, args.model)
    # Fixed judge: when --judge-model is set, use a separate grader LLM (same across all arms); otherwise reuse the served llm.
    if args.judge_model:
        if args.backend == "bedrock":
            judge_client = BedrockClient(region=args.region)
        else:
            from openai import OpenAI  # lazy: only the vLLM/OpenAI backend needs it
            judge_client = OpenAI(base_url=args.base_url, api_key=os.getenv("VLLM_API_KEY", "EMPTY"))
        judge_llm = LLM(judge_client, args.judge_model)
    else:
        judge_llm = llm
    kb_block = build_kb_block()

    conditions = ["with_kb", "without_kb"] if args.conditions == "both" else [args.conditions]
    results: dict[str, Any] = {}
    for cond in conditions:
        print(f"[{cond}] collecting LLM responses (k={args.k}) over {len(cases)} cases...")
        sysprompt = system_prompt(cond == "with_kb", kb_block)
        llm_results = collect_llm(cases, llm, sysprompt, args.k,
                                  args.temperature, args.consistency_temperature)
        cases_by_id = {c["id"]: c for c in cases}
        faq_grader = make_faq_grader(args.faq_grader, judge_llm)
        direct_records = run_direct(cases, llm_results, faq_grader)
        kora_records = run_kora(cases, llm_results, decisions, faq_grader)
        direct = aggregate("direct", direct_records, args.price_in, args.price_out)
        kora = aggregate("kora", kora_records, args.price_in, args.price_out)
        results[cond] = {
            "direct": direct,
            "kora": kora,
            "comparison": compare(direct, kora),
            "consistency_direct": consistency_report(cases, llm_results, args.k),
            "direct_errors": collect_errors(direct_records, cases_by_id),
            "kora_errors": collect_errors(kora_records, cases_by_id),
        }

    payload = {
        "config": {
            "workload": str(wl_path.name),
            "profile": workload.get("profile"),
            "n_cases": len(cases),
            "model": args.model,
            "base_url": args.base_url,
            "temperature": args.temperature,
            "k": args.k,
            "consistency_temperature": args.consistency_temperature,
            "faq_grader": args.faq_grader,
            "judge_model": args.judge_model or args.model,
            "conditions": conditions,
            "price_in_per_1m": args.price_in,
            "price_out_per_1m": args.price_out,
            "generated_with": workload.get("generated_with"),
        },
        "routing": routing,
        "conditions": results,
    }

    out_path = Path(args.out) if args.out else RESULTS_DIR / f"run_{workload.get('profile', 'wl')}.json"
    if not out_path.is_absolute():
        out_path = HERE / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print_summary(payload)
    print(f"\nWrote {out_path}")


def print_summary(payload: dict) -> None:
    r = payload["routing"]
    print("\n=== ROUTING (deterministic, KB-independent) ===")
    print(f"  precision={r['precision']:.3f} recall={r['recall']:.3f} "
          f"(tp={r['tp']} fp={r['fp']} tn={r['tn']} fn={r['fn']})")
    print(f"  by_category: " + ", ".join(
        f"{k}:{v['routed']}/{v['n']}routed" for k, v in r["by_category"].items()))
    if r["over_routed_cases"]:
        print(f"  !! over-routed (should-escalate but handled): {len(r['over_routed_cases'])}")
        for o in r["over_routed_cases"]:
            print(f"     {o['id']} {o['category']} -> {o['handler']} = {o['answer']!r}")
    for cond, blk in payload["conditions"].items():
        d, k = blk["direct"], blk["kora"]
        c = blk["comparison"]
        print(f"\n=== {cond.upper()} ===")
        print(f"  direct: acc={d['accuracy']:.3f} ({d['correct']}/{d['n_scorable']})  "
              f"llm_calls={d['llm_calls']}  tok_in={d['tokens_in']} tok_out={d['tokens_out']}")
        print(f"  kora  : acc={k['accuracy']:.3f} ({k['correct']}/{k['n_scorable']})  "
              f"llm_calls={k['llm_calls']}  tok_in={k['tokens_in']} tok_out={k['tokens_out']}  "
              f"deflection={k['deflection_rate']:.3f}")
        print(f"  delta : acc {c['accuracy_delta_kora_minus_direct']:+.3f}  "
              f"llm_calls saved {c['llm_calls_saved']} ({c['llm_calls_saved_pct']*100:.1f}%)  "
              f"tok_in saved {c['tokens_in_saved']}")
        print("  per-category accuracy (direct vs kora):")
        for cat in ("format", "faq", "policy"):
            dd = d["accuracy_by_category"].get(cat, {})
            kk = k["accuracy_by_category"].get(cat, {})
            if dd:
                print(f"     {cat:7} direct={dd['accuracy']:.3f}({dd['correct']}/{dd['n']})  "
                      f"kora={kk['accuracy']:.3f}({kk['correct']}/{kk['n']})")
        print(f"  errors surfaced: direct={len(blk['direct_errors'])}  kora={len(blk['kora_errors'])}")
        for tag in ("direct_errors", "kora_errors"):
            for e in blk[tag]:
                print(f"     [{tag.split('_')[0]}] {e['id']} {e['category']} gt={e['ground_truth']!r} "
                      f"verdict={e['verdict']!r} llm={e['llm_called']}")
        cons = blk["consistency_direct"]
        if cons.get("measured"):
            print(f"  consistency (direct, k={cons['k']}): "
                  f"rate={cons['consistency_rate']:.3f} "
                  f"({cons['stable']}/{cons['n_scorable']} stable)")
            for cat, cv in cons["by_category"].items():
                print(f"     {cat:7} consistency={cv['consistency_rate']:.3f} "
                      f"({cv['stable']}/{cv['n']})")


if __name__ == "__main__":
    main()
