"""KORA deterministic front-door dispatcher.

Given only what a real front door would see — the user `text` and an optional
structured `payload` — it either answers deterministically (format / FAQ /
policy) or ABSTAINS so the query escalates to the LLM. It NEVER sees the case
category or ground truth, so routing is answer-blind.

Decision order (each step can abstain):
  1. POLICY  — a policy topic + a judgment intent (or a payload). Routes only when
               exactly one topic is identified, a payload is present, and the
               shared evaluator accepts it. Missing/invalid fields -> abstain.
  2. payload present but no single identifiable policy -> abstain.
  3. FORMAT  — a strict "Is this a valid <email|phone|date>: <candidate>" frame.
               The library decides valid/invalid. Off-frame look-alikes (why/fix/
               compare/ambiguous-type) don't match -> abstain.
  4. FAQ     — exactly one KB fact matches -> answer it; else abstain.

Abstain conditions follow spec/format_standards.md and the policy/KB docs. The
abstain cases are exactly what the `trap` and `reasoning` categories exercise.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from . import format_rules, kb_match, policy_rules


@dataclass
class Decision:
    routed: bool          # True = deterministic answer produced; False = escalate
    answer: str | None    # deterministic answer ("valid"/"eligible"/KB text/...)
    handler: str | None   # e.g. "format:email", "faq:refund_window", "policy:free_shipping"
    reason: str           # human-readable route/abstain reason


def _route(answer: str, handler: str, reason: str) -> Decision:
    return Decision(routed=True, answer=answer, handler=handler, reason=reason)


def _abstain(reason: str) -> Decision:
    return Decision(routed=False, answer=None, handler=None, reason=reason)


# --------------------------------------------------------------------------- #
# Policy detection
# --------------------------------------------------------------------------- #
# Topic keywords map text -> candidate policy id(s). Derived from policy names.
_POLICY_INTENT_MARKERS = ("eligib", "qualif", "cover", "determine", "claim", "refundable")


def _policy_topics(t: str) -> set[str]:
    topics: set[str] = set()
    if "refund" in t or "refundable" in t:
        topics.add("refund_eligibility")
    if "free shipping" in t or ("shipping" in t and "free" in t):
        topics.add("free_shipping")
    if "coupon" in t or "welcome10" in t:
        topics.add("welcome_coupon")
    if "warranty" in t:
        topics.add("warranty_claim")
    if "return-label" in t or "return label" in t:
        topics.add("return_label")
    return topics


def _has_policy_intent(t: str) -> bool:
    return any(m in t for m in _POLICY_INTENT_MARKERS)


# --------------------------------------------------------------------------- #
# Format detection — strict request frame; the candidate is whatever follows ":"
# --------------------------------------------------------------------------- #
_FORMAT_FRAME = re.compile(
    r"^\s*is this a valid (email address|phone number|calendar date[^:]*?):\s*(\S.*?)\s*\??\s*$",
    re.IGNORECASE,
)


def _detect_format(text: str) -> tuple[str, str] | None:
    m = _FORMAT_FRAME.match(text)
    if not m:
        return None
    phrase = m.group(1).lower()
    candidate = m.group(2).strip()
    # Reject multi-candidate / comparison forms.
    if " and " in f" {candidate} " or " vs " in candidate.lower():
        return None
    if "email" in phrase:
        ftype = "email"
    elif "phone" in phrase:
        ftype = "phone"
    else:
        ftype = "date"
    return ftype, candidate


# --------------------------------------------------------------------------- #
# Dispatch
# --------------------------------------------------------------------------- #
def dispatch(text: str, payload: dict | None = None) -> Decision:
    t = text.lower()

    # 1. Policy path -------------------------------------------------------- #
    topics = _policy_topics(t)
    if topics and (payload is not None or _has_policy_intent(t)):
        if len(topics) != 1:
            return _abstain(f"policy: ambiguous policy topic ({sorted(topics)})")
        policy_id = next(iter(topics))
        if payload is None:
            return _abstain(f"policy:{policy_id}: judgment requested but no structured payload")
        try:
            verdict = policy_rules.evaluate(policy_id, payload)
        except policy_rules.PolicyInputError as exc:
            return _abstain(f"policy:{policy_id}: payload invalid ({exc})")
        return _route(verdict, f"policy:{policy_id}", f"evaluated {policy_id}")

    # 2. Structured input we couldn't tie to a policy ----------------------- #
    if payload is not None:
        return _abstain("policy: payload present but no policy identifiable")

    # 3. Format path -------------------------------------------------------- #
    fmt = _detect_format(text)
    if fmt is not None:
        ftype, candidate = fmt
        verdict = format_rules.validate(ftype, candidate)
        return _route(verdict, f"format:{ftype}", f"validated {ftype} via library")

    # 4. FAQ path ----------------------------------------------------------- #
    matches = kb_match.match(text)
    if len(matches) == 1:
        fid = matches[0]
        return _route(kb_match.answer(fid), f"faq:{fid}", f"KB match: {fid}")
    if not matches:
        return _abstain("faq: no confident KB match")
    return _abstain(f"faq: ambiguous KB match ({matches})")


# --------------------------------------------------------------------------- #
# Self-check: run the dispatcher over a generated workload and report routing
# quality (answer-aware ONLY for reporting; rules are not tuned to it).
# --------------------------------------------------------------------------- #
def _selfcheck(workload_path: str) -> None:
    import json
    from collections import defaultdict

    data = json.loads(open(workload_path, encoding="utf-8").read())
    cases = data["cases"]

    by_cat = defaultdict(lambda: {"n": 0, "routed": 0, "abstain": 0})
    det_correct = defaultdict(lambda: {"routed": 0, "correct": 0})
    routing = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}  # positive = should_escalate
    surprises = []

    for c in cases:
        d = dispatch(c["text"], c.get("payload"))
        cat = c["category"]
        by_cat[cat]["n"] += 1
        by_cat[cat]["routed" if d.routed else "abstain"] += 1

        should = c["should_escalate"]
        escalated = not d.routed
        if should and escalated:
            routing["tp"] += 1
        elif should and not escalated:
            routing["fn"] += 1   # over-routed a trap/reasoning case
            surprises.append((c["id"], cat, "ROUTED a should-escalate case", d.handler, d.answer))
        elif not should and not escalated:
            routing["tn"] += 1
        else:
            routing["fp"] += 1   # escalated a deterministically-answerable case (recall gap)

        # deterministic correctness on routed, scorable cases
        if d.routed and c["gt_kind"] in ("valid_invalid", "eligibility", "kb_answer"):
            det_correct[cat]["routed"] += 1
            ok = _det_correct(c, d.answer)
            det_correct[cat]["correct"] += int(ok)
            if not ok:
                surprises.append((c["id"], cat, "ROUTED but WRONG vs ground truth", d.handler, d.answer))

    print(f"workload: {workload_path}  ({len(cases)} cases)")
    print("\n routing by category (routed / abstain):")
    for cat, s in sorted(by_cat.items()):
        print(f"   {cat:10} n={s['n']:3}  routed={s['routed']:3}  abstain={s['abstain']:3}")

    p = routing["tp"] / (routing["tp"] + routing["fp"]) if (routing["tp"] + routing["fp"]) else 0.0
    r = routing["tp"] / (routing["tp"] + routing["fn"]) if (routing["tp"] + routing["fn"]) else 0.0
    print("\n escalation routing (positive = should_escalate):")
    print(f"   tp={routing['tp']} fp={routing['fp']} tn={routing['tn']} fn={routing['fn']}")
    print(f"   precision={p:.3f}  recall={r:.3f}")

    print("\n deterministic correctness on ROUTED scorable cases:")
    for cat, s in sorted(det_correct.items()):
        acc = s["correct"] / s["routed"] if s["routed"] else 0.0
        print(f"   {cat:10} routed={s['routed']:3}  correct={s['correct']:3}  acc={acc:.3f}")

    print(f"\n surprises ({len(surprises)}):")
    for row in surprises:
        print("   ", row)


def _det_correct(case: dict, answer: str | None) -> bool:
    kind = case["gt_kind"]
    gt = case["ground_truth"]
    if answer is None:
        return False
    if kind in ("valid_invalid", "eligibility"):
        return answer == gt
    if kind == "kb_answer":
        a = answer.lower()
        return all(k in a for k in gt)
    return False


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else str(
        __import__("pathlib").Path(__file__).resolve().parent.parent / "workloads" / "smoke.json"
    )
    _selfcheck(path)
