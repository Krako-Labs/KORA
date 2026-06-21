from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_representativeness_seed import ALLOWED_ROUTES, DEFAULT_FIXTURE, validate_seed


def test_representativeness_seed_shape_is_public_safe() -> None:
    summary = validate_seed(DEFAULT_FIXTURE)

    assert summary["ok"] is True
    assert summary["item_count"] == 40
    assert summary["category_count"] >= 12
    assert summary["public_safe"] is True
    assert summary["claim_scope"] == "fixture_only"
    assert set(summary["route_counts"]) == ALLOWED_ROUTES


def test_representativeness_seed_items_use_fixture_only_claim_scope() -> None:
    fixture = json.loads(DEFAULT_FIXTURE.read_text(encoding="utf-8"))

    ids = [item["id"] for item in fixture["items"]]
    assert len(ids) == len(set(ids))
    assert all(item["public_safe"] is True for item in fixture["items"])
    assert all(item["claim_scope"] == "fixture_only" for item in fixture["items"])
    assert all("production" not in item["rationale"].lower() for item in fixture["items"])


def test_representativeness_seed_validator_cli() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/validate_representativeness_seed.py",
            "--fixture",
            str(DEFAULT_FIXTURE),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    summary = json.loads(completed.stdout)
    assert summary["item_count"] == 40
    assert summary["route_counts"]["provider_needed"] >= 1
    assert summary["route_counts"]["gpu"] >= 1
