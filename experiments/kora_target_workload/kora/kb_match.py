"""Deterministic KB matcher for the FAQ category. Loads spec/kb.yaml and decides
which fact (if any) a query confidently asks for, using the frozen keyword
signals (Safety Guard #3 — signals come from the fact's meaning, not the
paraphrases).

Match semantics (all on the lowercased query, substring tests):
  all_of  : list of groups; EVERY group must have >= 1 term present (AND of ORs)
  any_of  : list of groups; >= 1 term across ALL groups must be present
  none_of : list of groups; if ANY term is present the fact is disqualified

The dispatcher routes only when EXACTLY ONE fact matches; zero or multiple
matches -> abstain (escalate).
"""

from __future__ import annotations

from pathlib import Path

import yaml

_KB_PATH = Path(__file__).resolve().parent.parent / "spec" / "kb.yaml"


def _load() -> list[dict]:
    data = yaml.safe_load(_KB_PATH.read_text(encoding="utf-8"))
    return data["facts"]


_FACTS = _load()
_ANSWERS = {f["id"]: f["answer"] for f in _FACTS}


def _all_groups_hit(groups: list[list[str]], text: str) -> bool:
    return all(any(term in text for term in group) for group in groups)


def _any_hit(groups: list[list[str]], text: str) -> bool:
    return any(term in text for group in groups for term in group)


def match(text: str) -> list[str]:
    """Return the ids of every fact whose signals fire on `text`."""
    t = text.lower()
    hits: list[str] = []
    for fact in _FACTS:
        m = fact.get("match", {})
        if not _all_groups_hit(m.get("all_of", []), t):
            continue
        any_groups = m.get("any_of", [])
        if any_groups and not _any_hit(any_groups, t):
            continue
        none_groups = m.get("none_of", [])
        if none_groups and _any_hit(none_groups, t):
            continue
        hits.append(fact["id"])
    return hits


def answer(fact_id: str) -> str:
    return _ANSWERS[fact_id]
