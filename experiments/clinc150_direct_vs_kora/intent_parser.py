"""Shared intent-response parser for the direct-vs-KORA benchmark arms.

Both run.py (CLINC150-only) and run_multi.py (dataset-agnostic) send a prompt
that asks the model to reply with JSON only: {"intent": "<label>"}. Some hosted
models (notably gpt-4o) wrap that JSON in a markdown code fence
(```json ... ``` or ``` ... ```), which a bare json.loads() cannot parse. When
that happens the response used to collapse to the lenient string fallback and,
finding no matching label, to the out-of-scope/empty value, silently discarding
an otherwise correct answer.

This module centralizes parsing so both arms behave identically:

  1. try json.loads on the response as sent                 -> path "raw"
  2. retry json.loads after stripping one code fence        -> path "fence-stripped"
  3. otherwise keep the original lenient string handling    -> path "fallback-oos"

The fence retry runs BEFORE the fallback, so a fenced JSON reply is recovered
instead of being thrown away. Step 3 is byte-for-byte the previous behavior, so
no new class of malformed reply slips through as a false positive. Each call
returns the parse path taken so callers can log it and tally how responses were
recovered.
"""

from __future__ import annotations

import json
import re
from typing import Iterable

# One markdown code fence: opening ``` with an optional language tag on the same
# line (json, JSON, ...), the body captured lazily, then the closing ```. DOTALL
# lets the body span newlines. Matches both ```json\n{...}\n``` and ```\n{...}\n```.
_FENCE_RE = re.compile(r"```[A-Za-z0-9_-]*\s*(.*?)```", re.DOTALL)

# Parse-path tags. Also used as log labels.
PATH_RAW = "raw"
PATH_FENCE = "fence-stripped"
PATH_FALLBACK = "fallback-oos"


def _strip_fence(text: str) -> str | None:
    """Return the inside of the first markdown code fence, or None if absent."""
    match = _FENCE_RE.search(text)
    if match is None:
        return None
    return match.group(1).strip()


def _intent_from_json(blob: str) -> str | None:
    """Parse `blob` as a JSON object and return its 'intent' string.

    Returns None when `blob` is not valid JSON or is not a JSON object, which is
    the signal to try the next parse path. This mirrors the original code, whose
    `except (json.JSONDecodeError, AttributeError)` caught both a decode failure
    and `.get` on a non-dict JSON value (e.g. a bare number).
    """
    try:
        obj = json.loads(blob)
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None
    return str(obj.get("intent", "")).strip()


def _snap(intent: str, label_names: Iterable[str], label_set: set[str], fallback: str) -> str:
    """Snap a candidate string to a known label, else return `fallback`."""
    if intent in label_set:
        return intent
    lowered = intent.lower()
    for label in label_names:
        if label.lower() == lowered:
            return label
    return fallback


def parse_intent(
    raw: str,
    label_names: Iterable[str],
    label_set: set[str],
    fallback: str,
) -> tuple[str, str]:
    """Parse a model reply into a known label.

    Returns (label, parse_path). parse_path is one of PATH_RAW, PATH_FENCE or
    PATH_FALLBACK and records how the label was recovered. The fallback path may
    still snap a bare-label reply to a valid label; it only returns `fallback`
    (the dataset's out-of-scope label, or "") when nothing matches.
    """
    intent = _intent_from_json(raw)
    if intent is not None:
        path = PATH_RAW
    else:
        stripped = _strip_fence(raw)
        intent = _intent_from_json(stripped) if stripped is not None else None
        if intent is not None:
            path = PATH_FENCE
        else:
            intent = raw.strip().strip('"')
            path = PATH_FALLBACK

    return _snap(intent, label_names, label_set, fallback), path
