"""Deterministic policy evaluators — reference implementation per
spec/policies.yaml. Shared by generate.py (ground truth) and the KORA dispatcher.

Each evaluator returns "eligible" or "ineligible". When a required field is
missing, out of its enum, or the wrong type, it raises PolicyInputError. The
dispatcher catches that to ABSTAIN (-> escalate); generate.py only ever feeds
well-formed inputs, so its ground truth is always a clean eligible/ineligible.

SCHEMA exposes each policy's required fields and types so the dispatcher can
decide abstain without re-deriving the rules.
"""

from __future__ import annotations

ELIGIBLE = "eligible"
INELIGIBLE = "ineligible"


class PolicyInputError(ValueError):
    """Raised when a structured input is missing fields / wrong type / bad enum."""


# --- enums (from spec/policies.yaml) ---------------------------------------- #
REFUND_CATEGORIES = ("electronics", "clothing", "food", "books", "other")
SHIPPING_ZONES = ("domestic", "remote", "international")
MEMBERSHIPS = ("none", "plus")
WARRANTY_CATEGORIES = ("electronics", "appliance", "accessory")
DEFECT_TYPES = ("manufacturing", "accidental", "wear")
RETURN_REASONS = ("defective", "wrong_item", "changed_mind")

WARRANTY_PERIOD_MONTHS = {"electronics": 12, "appliance": 24, "accessory": 6}
REFUND_WINDOW_DAYS = 30
RETURN_WINDOW_DAYS = 30
WELCOME_CODE = "WELCOME10"
WELCOME_MAX_ACCOUNT_AGE_DAYS = 14
FREE_SHIP_THRESHOLD = 50  # USD, domestic non-member


# --- typed field extraction ------------------------------------------------- #
def _get(payload: dict, field: str):
    if not isinstance(payload, dict) or field not in payload:
        raise PolicyInputError(f"missing field: {field}")
    return payload[field]


def _as_int(payload: dict, field: str) -> int:
    v = _get(payload, field)
    # bool is a subclass of int — reject it as a wrong type for int fields.
    if isinstance(v, bool) or not isinstance(v, int):
        raise PolicyInputError(f"field {field} must be an int, got {type(v).__name__}")
    return v


def _as_number(payload: dict, field: str) -> float:
    v = _get(payload, field)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise PolicyInputError(f"field {field} must be a number, got {type(v).__name__}")
    return v


def _as_bool(payload: dict, field: str) -> bool:
    v = _get(payload, field)
    if not isinstance(v, bool):
        raise PolicyInputError(f"field {field} must be a bool, got {type(v).__name__}")
    return v


def _as_enum(payload: dict, field: str, allowed: tuple) -> str:
    v = _get(payload, field)
    if v not in allowed:
        raise PolicyInputError(f"field {field}={v!r} not in {allowed}")
    return v


# --- policies (semantics MUST match spec/policies.yaml) --------------------- #
def refund_eligibility(payload: dict) -> str:
    days = _as_int(payload, "days_since_delivery")
    category = _as_enum(payload, "item_category", REFUND_CATEGORIES)
    opened = _as_bool(payload, "opened")
    if category == "food":
        return INELIGIBLE
    if days > REFUND_WINDOW_DAYS:
        return INELIGIBLE
    if category == "electronics" and opened:
        return INELIGIBLE
    return ELIGIBLE


def free_shipping(payload: dict) -> str:
    total = _as_number(payload, "order_total")
    zone = _as_enum(payload, "destination_zone", SHIPPING_ZONES)
    membership = _as_enum(payload, "membership", MEMBERSHIPS)
    if zone == "international":
        return INELIGIBLE
    if membership == "plus":
        return ELIGIBLE
    if zone == "domestic" and total >= FREE_SHIP_THRESHOLD:
        return ELIGIBLE
    return INELIGIBLE


def welcome_coupon(payload: dict) -> str:
    age = _as_int(payload, "account_age_days")
    prior = _as_int(payload, "prior_orders")
    code = _get(payload, "coupon_code")
    if not isinstance(code, str):
        raise PolicyInputError("field coupon_code must be a string")
    if code != WELCOME_CODE:  # case-sensitive by spec
        return INELIGIBLE
    if prior > 0:
        return INELIGIBLE
    if age > WELCOME_MAX_ACCOUNT_AGE_DAYS:
        return INELIGIBLE
    return ELIGIBLE


def warranty_claim(payload: dict) -> str:
    months = _as_int(payload, "months_since_purchase")
    category = _as_enum(payload, "product_category", WARRANTY_CATEGORIES)
    defect = _as_enum(payload, "defect_type", DEFECT_TYPES)
    if defect != "manufacturing":
        return INELIGIBLE
    if months > WARRANTY_PERIOD_MONTHS[category]:
        return INELIGIBLE
    return ELIGIBLE


def return_label(payload: dict) -> str:
    reason = _as_enum(payload, "reason", RETURN_REASONS)
    days = _as_int(payload, "days_since_delivery")
    if days > RETURN_WINDOW_DAYS:
        return INELIGIBLE
    if reason in ("defective", "wrong_item"):
        return ELIGIBLE
    return INELIGIBLE


POLICIES = {
    "refund_eligibility": refund_eligibility,
    "free_shipping": free_shipping,
    "welcome_coupon": welcome_coupon,
    "warranty_claim": warranty_claim,
    "return_label": return_label,
}

# Field -> ("int"|"number"|"bool"|"str"|"enum", enum_values_or_None).
# Used by the dispatcher to verify a payload before evaluating (else abstain).
SCHEMA = {
    "refund_eligibility": {
        "days_since_delivery": ("int", None),
        "item_category": ("enum", REFUND_CATEGORIES),
        "opened": ("bool", None),
    },
    "free_shipping": {
        "order_total": ("number", None),
        "destination_zone": ("enum", SHIPPING_ZONES),
        "membership": ("enum", MEMBERSHIPS),
    },
    "welcome_coupon": {
        "account_age_days": ("int", None),
        "prior_orders": ("int", None),
        "coupon_code": ("str", None),
    },
    "warranty_claim": {
        "months_since_purchase": ("int", None),
        "product_category": ("enum", WARRANTY_CATEGORIES),
        "defect_type": ("enum", DEFECT_TYPES),
    },
    "return_label": {
        "reason": ("enum", RETURN_REASONS),
        "days_since_delivery": ("int", None),
    },
}


def evaluate(policy_id: str, payload: dict) -> str:
    """Evaluate a policy. Raises PolicyInputError on a bad payload."""
    try:
        fn = POLICIES[policy_id]
    except KeyError:
        raise ValueError(f"unknown policy_id: {policy_id!r}") from None
    return fn(payload)
