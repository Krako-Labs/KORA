"""Machine-readable contracts for bounded KORA Solution Host runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

RESULT_ENVELOPE_SCHEMA = "result-envelope.schema.json"
RUNTIME_DESCRIPTOR_SCHEMA = "runtime-descriptor.schema.json"
RUNTIME_STATUS_SCHEMA = "runtime-status.schema.json"


class SolutionContractError(ValueError):
    """Raised when a result or runtime-status payload violates its contract."""

    def __init__(self, contract: str, locations: tuple[str, ...]):
        self.contract = contract
        self.locations = locations
        rendered = ", ".join(locations) if locations else "$"
        super().__init__(f"{contract} contract validation failed at {rendered}")


def canonical_json_bytes(payload: Any) -> bytes:
    """Serialize a JSON value deterministically for local records and digests."""

    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def load_json_object(path: Path) -> dict[str, Any]:
    """Load a JSON object from a regular UTF-8 file."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"expected a JSON object: {path.name}")
    return payload


def load_contract_schema(name: str) -> dict[str, Any]:
    """Load and self-check a bundled Solution contract schema."""

    path = Path(__file__).with_name("schemas") / name
    schema = load_json_object(path)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:  # pragma: no cover - bundled-schema defect
        raise RuntimeError(f"invalid bundled Solution contract schema {name}: {exc.message}") from exc
    return schema


def instance_error_locations(schema: dict[str, Any], payload: Any) -> tuple[str, ...]:
    """Return stable JSON locations that do not echo private input values."""

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    locations = {
        "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}"
            for part in error.absolute_path
        )
        for error in validator.iter_errors(payload)
    }
    return tuple(sorted(locations))


def validate_contract_instance(name: str, payload: Any) -> None:
    """Validate a result/status payload against a bundled schema."""

    locations = instance_error_locations(load_contract_schema(name), payload)
    if locations:
        raise SolutionContractError(name, locations)


def validate_declared_instance(schema_path: Path, payload: Any) -> tuple[str, ...]:
    """Validate Solution input or output without exposing instance content."""

    schema = load_json_object(schema_path)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ValueError(f"invalid declared schema: {schema_path.name}: {exc.message}") from exc
    return instance_error_locations(schema, payload)


__all__ = [
    "RESULT_ENVELOPE_SCHEMA",
    "RUNTIME_DESCRIPTOR_SCHEMA",
    "RUNTIME_STATUS_SCHEMA",
    "SolutionContractError",
    "canonical_json_bytes",
    "instance_error_locations",
    "load_contract_schema",
    "load_json_object",
    "validate_contract_instance",
    "validate_declared_instance",
]
