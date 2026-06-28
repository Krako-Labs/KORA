"""Deterministic, intent-preserving paraphrase transforms for KORA's routing
robustness test.

Goal: test the claim made in kb_match.py (Safety Guard #3) and implied by the
strict FORMAT frame in dispatcher.py — that routing signals come from a query's
*meaning*, not its exact surface wording. We do this WITHOUT any LLM call: each
transform rewrites only the `text` surface in a way a real user might naturally
phrase the same request, and leaves every label (`should_escalate`,
`ground_truth`, `payload`, `meta`) untouched.

Methodology guard (frozen before measuring anything): transforms are defined by
"would a real user write it this way for the same intent?", NOT by whether they
help or hurt the dispatcher. We report whatever happens — breaks are real
weaknesses, non-breaks are real robustness. We never hand-craft a transform to
force a trap into a valid frame, nor to dodge a known-fragile path.

Each transform maps one case's text -> one new text (deterministic). Applying a
transform to the full workload yields one paraphrased workload variant; routing
metrics on it are compared against the original.
"""

from __future__ import annotations

import re


def t_whitespace(text: str) -> str:
    """Insert benign double spaces between words and pad the ends, the kind of
    sloppy spacing real users produce. A meaning-preserving no-op for a reader."""
    collapsed = re.sub(r"\s+", " ", text.strip())
    return "  " + collapsed.replace(" ", "  ") + " "


def t_punct(text: str) -> str:
    """Flip terminal punctuation: a question gets its '?' dropped, a
    non-question gets a trailing '?' added. Users are inconsistent about this."""
    s = text.rstrip()
    if s.endswith("?"):
        return s[:-1].rstrip()
    if s.endswith("."):
        return s[:-1].rstrip() + "?"
    return s + "?"


def t_case(text: str) -> str:
    """Sentence-case the whole thing. The dispatcher lowercases internally, so
    this is PREDICTED to be a true no-op for routing — it is included as a
    sanity check: any flip here signals a bug in our own pipeline, not a real
    sensitivity in the router."""
    if not text:
        return text
    return text[0].upper() + text[1:].lower()


def t_polite_prefix(text: str) -> str:
    """Prepend a natural politeness lead-in. PREDICTED to break the strict
    FORMAT frame (which anchors on '^is this a valid'), an honest cost-only
    flip; FAQ/POLICY keep their substring keywords and should survive."""
    return "Could you please tell me: " + text[0].lower() + text[1:] if text else text


_SYNONYMS = [
    (r"\bvalid\b", "correct"),
    (r"\bopen\b", "available"),
    (r"\bhours\b", "times"),
    (r"\brefund\b", "money back"),
    (r"\beligible\b", "qualified"),
]


def t_synonym(text: str) -> str:
    """Apply conservative, user-plausible synonym swaps. Some of these are
    PREDICTED to break routing (e.g. 'valid'->'correct' defeats the FORMAT
    frame's literal; 'refund'->'money back' drops the policy topic keyword).
    They are included precisely because a real user would say them — the breaks
    they cause are honest measurements of keyword fragility."""
    out = text
    for pat, repl in _SYNONYMS:
        out = re.sub(pat, repl, out, flags=re.IGNORECASE)
    return out


TRANSFORMS = {
    "whitespace": t_whitespace,
    "punct": t_punct,
    "case": t_case,
    "polite_prefix": t_polite_prefix,
    "synonym": t_synonym,
}


def apply_transform(cases: list[dict], name: str) -> list[dict]:
    """Return a copy of `cases` with `text` rewritten by transform `name`. Only
    `text` changes; all labels are preserved."""
    fn = TRANSFORMS[name]
    out = []
    for c in cases:
        nc = dict(c)
        nc["text"] = fn(c["text"])
        out.append(nc)
    return out
