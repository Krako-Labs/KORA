from __future__ import annotations

import json
from dataclasses import replace

import pytest

from kora.cli import main
from kora.foundation.reality_matrix import (
    SCHEMA_VERSION,
    RealityObservation,
    build_reality_registry,
    load_reality_registry,
)


def _data(observation_id: str = "obs-a", **updates):
    data = {
        "schema_version": SCHEMA_VERSION,
        "observation_id": observation_id,
        "node_labels": ["synthetic-node-a"],
        "runtime": "synthetic-runtime",
        "hardware": "synthetic-hardware",
        "transport": "none",
        "topology": "single_node",
        "evidence_state": "PLANNED",
        "metrics": {},
        "source": None,
        "notes": "synthetic test-only metadata; not KORA evidence",
    }
    data.update(updates)
    return data


@pytest.mark.parametrize(
    ("updates", "message"),
    [
        ({"schema_version": "wrong"}, "schema_version"),
        ({"runtime": "  "}, "runtime"),
        ({"node_labels": []}, "node label"),
        ({"node_labels": ["node-a", "NODE-A"]}, "duplicate node labels"),
        ({"evidence_state": "ASSUMED"}, "unsupported evidence_state"),
        ({"evidence_state": "MEASURED", "metrics": {"value": True}, "source": "test"}, "finite numbers"),
        ({"evidence_state": "MEASURED", "metrics": {}}, "metrics and a source"),
        ({"evidence_state": "MEASURED", "metrics": {"value": "1"}, "source": "test"}, "finite numbers"),
        ({"evidence_state": "MEASURED", "metrics": {"value": 1}, "source": "  "}, "source"),
    ],
)
def test_observation_from_dict_rejects_invalid_evidence(updates, message) -> None:
    with pytest.raises(ValueError, match=message):
        RealityObservation.from_dict(_data(**updates))


def test_observation_from_dict_is_strict_about_json_shape() -> None:
    with pytest.raises(ValueError, match="missing observation fields"):
        RealityObservation.from_dict({"schema_version": SCHEMA_VERSION})
    with pytest.raises(ValueError, match="unexpected observation fields"):
        RealityObservation.from_dict({**_data(), "winner": "synthetic-runtime"})
    with pytest.raises(ValueError, match="JSON array"):
        RealityObservation.from_dict(_data(node_labels="synthetic-node-a"))


def test_measured_observation_requires_numeric_metrics_and_source() -> None:
    observation = RealityObservation.from_dict(
        _data(
            evidence_state="MEASURED",
            metrics={"synthetic_test_value": 1.25},
            source="synthetic-test-only.json",
        )
    )
    assert observation.metrics == {"synthetic_test_value": 1.25}


def test_registry_orders_by_documented_key_and_builds_non_interpretive_counts() -> None:
    observations = [
        RealityObservation.from_dict(_data("z-observation", evidence_state="UNKNOWN", topology="two_nodes", node_labels=["a", "b"])),
        RealityObservation.from_dict(_data("A-observation", evidence_state="FACT")),
        RealityObservation.from_dict(_data("a-observation", evidence_state="DETECTED")),
    ]
    registry = build_reality_registry(observations)

    assert [item.observation_id for item in registry.observations] == [
        "A-observation", "a-observation", "z-observation"
    ]
    assert registry.stable_order_key == "observation_id.casefold(), observation_id"
    assert registry.summary["evidence_state"] == {"DETECTED": 1, "FACT": 1, "UNKNOWN": 1}
    assert registry.summary["node_count"] == {"1": 2, "2": 1}
    assert "winner" not in json.dumps(registry.to_dict()).lower()
    assert "prove performance" in registry.claim_boundary


def test_registry_rejects_duplicate_ids_and_malformed_files(tmp_path) -> None:
    observation = RealityObservation.from_dict(_data())
    with pytest.raises(ValueError, match="duplicate observation IDs"):
        build_reality_registry([observation, replace(observation)])

    malformed = tmp_path / "malformed.json"
    malformed.write_text("not-json", encoding="utf-8")
    with pytest.raises(ValueError, match="cannot load reality observation"):
        load_reality_registry([malformed])


def test_system_reality_cli_text_json_output_and_errors(tmp_path, capsys) -> None:
    later = tmp_path / "later.json"
    earlier = tmp_path / "earlier.json"
    later.write_text(json.dumps(_data("z-observation", evidence_state="UNKNOWN")), encoding="utf-8")
    earlier.write_text(json.dumps(_data("a-observation", evidence_state="FACT")), encoding="utf-8")

    assert main(["system", "reality", str(later), str(earlier)]) == 0
    text = capsys.readouterr().out
    assert text.index("a-observation [FACT]") < text.index("z-observation [UNKNOWN]")
    assert "Evidence-state counts:" in text
    assert "does not create benchmark evidence" in text

    output = tmp_path / "registry.json"
    assert main(["system", "reality", str(later), str(earlier), "--json", "--json-out", str(output)]) == 0
    stdout = capsys.readouterr().out
    printed = json.loads(stdout[: stdout.rindex("\nSaved JSON:")])
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert printed == saved
    assert saved["observation_count"] == 2

    with pytest.raises(SystemExit, match="2"):
        main(["system", "reality", str(earlier), str(earlier)])
    assert "duplicate observation IDs" in capsys.readouterr().err

    malformed = tmp_path / "bad.json"
    malformed.write_text("[]", encoding="utf-8")
    with pytest.raises(SystemExit, match="2"):
        main(["system", "reality", str(malformed)])
    assert "observation must be a JSON object" in capsys.readouterr().err
