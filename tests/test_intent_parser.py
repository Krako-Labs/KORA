"""Unit tests for the shared intent-response parser.

Covers the markdown-fence bug fix and pins the pre-existing lenient behavior so
the Qwen path stays byte-identical (only the response mechanism differs).
"""

from experiments.clinc150_direct_vs_kora.intent_parser import (
    PATH_FALLBACK,
    PATH_FENCE,
    PATH_RAW,
    parse_intent,
)

LABELS = ["transfer_money", "check_balance", "oos"]
LABEL_SET = set(LABELS)
FALLBACK = "oos"


def _parse(raw: str, fallback: str = FALLBACK):
    return parse_intent(raw, LABELS, LABEL_SET, fallback)


# --- the five parse-path cases the instruction requires ------------------- #

def test_raw_json() -> None:
    label, path = _parse('{"intent": "transfer_money"}')
    assert label == "transfer_money"
    assert path == PATH_RAW


def test_json_language_tagged_fence() -> None:
    label, path = _parse('```json\n{"intent": "transfer_money"}\n```')
    assert label == "transfer_money"
    assert path == PATH_FENCE


def test_bare_fence_no_language_tag() -> None:
    label, path = _parse('```\n{"intent": "check_balance"}\n```')
    assert label == "check_balance"
    assert path == PATH_FENCE


def test_non_json_inside_fence_falls_back() -> None:
    # Fence strips fine but the body is not JSON, so it must not silently pass;
    # it drops to the fallback path and, matching no label, returns fallback.
    label, path = _parse("```\nnot json at all\n```")
    assert path == PATH_FALLBACK
    assert label == FALLBACK


def test_completely_non_json_falls_back() -> None:
    label, path = _parse("the intent is probably a transfer")
    assert path == PATH_FALLBACK
    assert label == FALLBACK


# --- recovery correctness (the bug this fix exists for) ------------------- #

def test_fence_recovers_the_actual_label_not_fallback() -> None:
    # Before the fix this whole reply failed json.loads and collapsed to oos.
    label, path = _parse('```json\n{"intent": "check_balance"}\n```')
    assert label == "check_balance" != FALLBACK
    assert path == PATH_FENCE


# --- no-regression: pre-existing lenient behavior is preserved exactly ---- #

def test_bare_label_without_json_still_snaps_via_fallback() -> None:
    # Qwen commonly returns a bare label. Old code snapped it in the except
    # branch; new code must reach the same label through the fallback path.
    label, path = _parse("transfer_money")
    assert label == "transfer_money"
    assert path == PATH_FALLBACK


def test_quoted_bare_label_is_unquoted_then_snapped() -> None:
    label, path = _parse('"check_balance"')
    assert label == "check_balance"
    assert path == PATH_FALLBACK


def test_case_insensitive_snap() -> None:
    label, path = _parse('{"intent": "TRANSFER_MONEY"}')
    assert label == "transfer_money"
    assert path == PATH_RAW


def test_json_non_object_falls_back() -> None:
    # json.loads("5") -> int; .get would raise, so this must fall back exactly
    # as the old `except (JSONDecodeError, AttributeError)` did.
    label, path = _parse("5")
    assert path == PATH_FALLBACK
    assert label == FALLBACK


def test_empty_fallback_value_is_respected() -> None:
    # run_multi passes "" as the fallback when a dataset has no oos label.
    label, path = _parse("nothing matches here", fallback="")
    assert label == ""
    assert path == PATH_FALLBACK


def test_unknown_intent_in_valid_json_falls_to_fallback_value() -> None:
    label, path = _parse('{"intent": "no_such_label"}')
    assert label == FALLBACK
    assert path == PATH_RAW
