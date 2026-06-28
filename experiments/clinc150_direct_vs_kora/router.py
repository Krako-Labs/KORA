"""Deterministic keyword router for CLINC150 intent classification.

The router attempts to classify a query *without* an LLM call by matching the
query tokens against keyword sets derived from each intent label. When the match
is confident and unambiguous it returns a deterministic prediction; otherwise it
abstains so the caller can escalate to the LLM.

This is intentionally simple: it is the cheap "first stage" whose whole value is
deflecting easy queries away from the model. Anything it is unsure about is left
for the LLM, which is exactly the KORA routing story we want to measure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

# A few stopword-ish label tokens that are too generic to be discriminative.
# They appear inside many intent labels (e.g. "change_*", "*_status") and would
# otherwise create spurious matches.
_WEAK_TOKENS = {
    # generic label scaffolding tokens (appear across many intents)
    "change",
    "status",
    "update",
    "info",
    "list",
    "new",
    # English function words — non-discriminative and prone to spurious matches
    # (e.g. "what_can_i_ask_you" -> {can, i, ask} matched every "can i ..." query)
    "a",
    "an",
    "the",
    "is",
    "it",
    "to",
    "of",
    "for",
    "do",
    "are",
    "you",
    "your",
    "i",
    "me",
    "my",
    "can",
    "what",
    "how",
    "who",
    "when",
    "where",
    "ask",
    "tell",
}

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


@dataclass(frozen=True)
class RouteDecision:
    """Outcome of a single routing attempt."""

    routed: bool          # True -> deterministic answer, False -> escalate to LLM
    intent: str | None    # predicted intent when routed
    score: float          # best keyword-overlap score
    margin: float         # best_score - second_best_score
    reason: str           # human-readable reason for the decision


class KeywordRouter:
    """Keyword-overlap router built from CLINC150 intent labels."""

    def __init__(
        self,
        intent_labels: Iterable[str],
        *,
        oos_label: str = "oos",
        min_score: float = 2.0,
        min_margin: float = 1.0,
    ) -> None:
        """Build keyword sets from intent labels.

        Args:
            intent_labels: all intent label names (including the oos label).
            oos_label: the out-of-scope label, which carries no keywords.
            min_score: minimum best overlap score required to route deterministically.
            min_margin: minimum gap between the best and runner-up score required
                to consider the match unambiguous.
        """
        self.oos_label = oos_label
        self.min_score = min_score
        self.min_margin = min_margin

        self.keywords: dict[str, set[str]] = {}
        for label in intent_labels:
            if label == oos_label:
                continue
            tokens = {tok for tok in label.split("_") if tok and tok not in _WEAK_TOKENS}
            if tokens:
                self.keywords[label] = tokens

    def route(self, query: str) -> RouteDecision:
        query_tokens = set(_tokenize(query))
        if not query_tokens:
            return RouteDecision(False, None, 0.0, 0.0, "empty_query")

        scored: list[tuple[float, str]] = []
        for label, kw in self.keywords.items():
            overlap = query_tokens & kw
            if not overlap:
                continue
            # Score = number of matched label tokens, with a small bonus for
            # matching a larger fraction of the label's keywords (specificity).
            score = len(overlap) + (len(overlap) / len(kw))
            scored.append((score, label))

        if not scored:
            return RouteDecision(False, None, 0.0, 0.0, "no_keyword_overlap")

        scored.sort(reverse=True)
        best_score, best_label = scored[0]
        second_score = scored[1][0] if len(scored) > 1 else 0.0
        margin = best_score - second_score

        if best_score < self.min_score:
            return RouteDecision(
                False, None, best_score, margin,
                f"below_min_score({best_score:.2f}<{self.min_score})",
            )
        if margin < self.min_margin:
            return RouteDecision(
                False, None, best_score, margin,
                f"ambiguous_margin({margin:.2f}<{self.min_margin})",
            )
        return RouteDecision(
            True, best_label, best_score, margin,
            f"routed(score={best_score:.2f},margin={margin:.2f})",
        )
