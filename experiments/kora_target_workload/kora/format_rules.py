"""Deterministic format validators — reference implementation per
spec/format_standards.md. Shared by generate.py (ground truth) and the KORA
dispatcher (deterministic answer), so ground truth and the deterministic path
call the *identical* library code.

Each validator returns "valid" or "invalid". Ground truth == whatever the
authoritative library says; we never hand-label. There is no abstain logic here
— abstain / candidate-extraction / routing belongs to the dispatcher.
"""

from __future__ import annotations

import datetime
import platform

VALID = "valid"
INVALID = "invalid"

PHONE_DEFAULT_REGION = "US"  # per spec; E.164 (+cc) parses without a region hint
DATE_FORMAT = "%Y-%m-%d"

FORMAT_TYPES = ("email", "phone", "date")


def validate_email_value(candidate: str) -> str:
    """email-validator, syntax/normalization only (no DNS)."""
    from email_validator import EmailNotValidError, validate_email

    try:
        validate_email(candidate, check_deliverability=False)
        return VALID
    except EmailNotValidError:
        return INVALID


def validate_phone_value(candidate: str) -> str:
    """phonenumbers.parse(US) + is_valid_number."""
    import phonenumbers

    try:
        parsed = phonenumbers.parse(candidate, PHONE_DEFAULT_REGION)
    except phonenumbers.NumberParseException:
        return INVALID
    return VALID if phonenumbers.is_valid_number(parsed) else INVALID


def validate_date_value(candidate: str) -> str:
    """datetime.strptime against the real Gregorian calendar."""
    try:
        datetime.datetime.strptime(candidate, DATE_FORMAT)
        return VALID
    except ValueError:
        return INVALID


VALIDATORS = {
    "email": validate_email_value,
    "phone": validate_phone_value,
    "date": validate_date_value,
}


def validate(format_type: str, candidate: str) -> str:
    """Dispatch to the validator for `format_type`. Raises on unknown type."""
    try:
        return VALIDATORS[format_type](candidate)
    except KeyError:
        raise ValueError(f"unknown format_type: {format_type!r}") from None


def lib_versions() -> dict[str, str]:
    """Versions captured into the frozen workload for reproducibility."""
    import email_validator
    import phonenumbers

    return {
        "email_validator": getattr(email_validator, "__version__", "?"),
        "phonenumbers": getattr(phonenumbers, "__version__", "?"),
        "python": platform.python_version(),
    }
