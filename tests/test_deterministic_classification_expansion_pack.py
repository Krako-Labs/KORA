import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


SCENARIOS = [
    "support_ticket_routing",
    "issue_triage",
    "incident_severity_routing",
    "document_type_routing",
    "log_event_classification",
]


def _load_example_module():
    script_path = Path("examples/deterministic_classification/run.py")
    spec = importlib.util.spec_from_file_location("deterministic_classification_run", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load deterministic_classification module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[str(spec.name)] = module
    spec.loader.exec_module(module)
    return module


def _projection(summary: dict, expected: dict) -> dict:
    return {key: summary[key] for key in expected}


def test_deterministic_classification_loads_all_scenarios() -> None:
    module = _load_example_module()

    datasets = module.load_scenario_datasets()

    assert [dataset["scenario_id"] for dataset in datasets] == sorted(SCENARIOS)
    assert all(dataset["privacy_class"] == "synthetic" for dataset in datasets)


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_each_deterministic_classification_scenario_matches_expected_output(scenario: str) -> None:
    module = _load_example_module()
    expected_path = Path("examples/deterministic_classification/expected_outputs") / f"{scenario}.json"
    expected = json.loads(expected_path.read_text(encoding="utf-8"))

    summary = module.build_pack_summary(scenario=scenario)

    assert _projection(summary, expected) == expected
    assert summary["provider_calls"] == 0
    assert summary["provider_calls_actually_made"] == 0
    assert summary["scenario_summaries"][0]["expected_match_count"] == summary["total_tasks"]
    assert all(result["kora_event_count"] == 1 for result in summary["scenario_summaries"][0]["results"])


def test_deterministic_classification_aggregate_summary_matches_expected_output() -> None:
    module = _load_example_module()
    expected = json.loads(
        Path("examples/deterministic_classification/expected_outputs/aggregate.json").read_text(
            encoding="utf-8"
        )
    )

    summary = module.build_pack_summary()

    assert _projection(summary, expected) == expected
    assert summary["aggregate_evidence_summary"] == {
        "total_tasks": 32,
        "deterministic_routes": 21,
        "provider_needed_routes": 11,
        "avoided_provider_invocations": 21,
        "provider_calls_actually_made": 0,
    }
    assert len(summary["comparison"]) == 32
    assert "KORA routes 21 of 32 sample classification tasks" in summary["safe_example_claim"]


def test_original_support_ticket_example_path_remains_available() -> None:
    module = _load_example_module()

    summary = module.build_deterministic_classification_summary()

    assert summary["scenario_ids"] == ["support_ticket_routing"]
    assert summary["total_tasks"] == 8
    assert summary["deterministic_routes"] == 5
    assert summary["provider_needed_routes"] == 3
    assert summary["provider_calls"] == 0


def test_expansion_pack_uses_kora_execution_path() -> None:
    module = _load_example_module()

    summary = module.build_pack_summary(scenario="issue_triage")
    first = summary["scenario_summaries"][0]["results"][0]

    assert first["kora_graph_id"].startswith("deterministic-classification-issue_triage-")
    assert first["task_id"] == "classify"
    assert first["selected_route"] == "det.issue.bug"
    assert first["provider_calls"] == 0


def test_deterministic_classification_requires_no_provider_environment(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    module = _load_example_module()

    summary = module.build_pack_summary()

    assert summary["ok"] is True
    assert summary["provider_calls_actually_made"] == 0
    assert "OPENAI_API_KEY" not in os.environ
    assert "ANTHROPIC_API_KEY" not in os.environ


def test_deterministic_classification_cli_writes_outputs(tmp_path: Path) -> None:
    json_out = tmp_path / "goal081a.json"
    report_md = tmp_path / "goal081a.md"

    completed = subprocess.run(
        [
            sys.executable,
            "examples/deterministic_classification/run.py",
            "--json-out",
            str(json_out),
            "--report-md",
            str(report_md),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert json_out.exists()
    assert report_md.exists()
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    report = report_md.read_text(encoding="utf-8")
    assert saved["total_tasks"] == 32
    assert saved["provider_calls_actually_made"] == 0
    assert '"provider_calls_actually_made": 0' in completed.stdout
    assert "Total tasks: `32`" in report
    assert "Provider calls actually made: `0`" in report
    assert "This is not production validation." in report


def test_deterministic_classification_runs_through_kora_example_runner() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "deterministic_classification",
            "--",
            "--scenario",
            "document_type_routing",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert '"scenario_ids": [' in completed.stdout
    assert '"document_type_routing"' in completed.stdout
    assert '"provider_calls_actually_made": 0' in completed.stdout


@pytest.mark.parametrize("context, action", [
    ({"tenant": "Cedar"}, "review"), ({"tenant": "Juniper"}, "transfer"),
    ({}, None), (None, None), ({"tenant": "other"}, None),
    ({"tenant": "cedar"}, None), ({"tenant": ["Cedar"]}, None),
])
def test_classification_uses_explicit_tenant_context(context, action):
    example = _load_example_module()
    routes = [
        {"route_id": name, "keywords": ["pending"], "required_context": {"tenant": tenant},
         "output": {"category": name}}
        for tenant, name in [("Cedar", "review"), ("Juniper", "transfer")]
    ]
    scenario = {"scenario_id": "claims", "scenario_label": "Claims",
                "routes": routes, "provider_required_route": "defer"}
    item = {"id": "request", "subject": "Pending", "body": "Text says tenant Cedar.",
            "context": context}
    result = example._run_kora_classification(scenario, item)
    assert result["provider_calls"] == 0
    if action is None:
        assert result["selected_route"] == "defer"
        assert result["provider_needed_reason"]
        assert result["classification_output"] is None
    else:
        assert result["selected_route"] == action
        assert result["classification_output"] == {"category": action}


@pytest.mark.parametrize("first_scope, context, expected", [
    ({"tenant": "Cedar", "entity": "device"}, {"tenant": "Juniper"}, "juniper"),
    ({"entity": "device", "tenant": "Cedar"}, {"tenant": "Juniper"}, "juniper"),
    ({"entity": "device"}, {"tenant": "Juniper"}, "defer"),
    ({"tenant": "Juniper"}, {"tenant": "Juniper"}, "defer"),
    ({}, {"tenant": "Juniper"}, "defer"),
    (None, {"tenant": "Juniper"}, "defer"),
    ({"tenant": ""}, {"tenant": "Juniper"}, "defer"),
])
def test_partial_or_invalid_competing_scope_is_order_independent(first_scope, context, expected):
    example = _load_example_module()
    routes = [
        {"route_id": "other", "keywords": ["pending"], "required_context": first_scope},
        {"route_id": "juniper", "keywords": ["pending"], "required_context": {"tenant": "Juniper"}},
    ]
    for ordered in (routes, routes[::-1]):
        scenario = {"scenario_id": "claims", "scenario_label": "Claims",
                    "routes": ordered, "provider_required_route": "defer"}
        item = {"id": "request", "subject": "Pending", "body": "", "context": context}
        result = example._run_kora_classification(scenario, item)
        assert result["selected_route"] == expected
        assert result["provider_calls"] == 0


@pytest.mark.parametrize("keywords", [[], [""], ["   "], [None], ["pending", 3], "pending"])
def test_scoped_rule_rejects_invalid_keyword_configuration(keywords):
    example = _load_example_module()
    scenario = {"scenario_id": "claims", "scenario_label": "Claims",
                "routes": [{"route_id": "review", "required_context": {"tenant": "Cedar"},
                            "keywords": keywords}], "provider_required_route": "defer"}
    item = {"id": "request", "subject": "Unrelated", "body": "", "context": {"tenant": "Cedar"}}
    with pytest.raises((RuntimeError, ValueError), match="nonempty string keywords"):
        example._run_kora_classification(scenario, item)
