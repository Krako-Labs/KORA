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


@pytest.mark.parametrize("ordered", [False, True])
def test_out_of_domain_competing_scope_defers_independent_match(ordered):
    example = _load_example_module()
    aliases = [
        {"route_id": "account", "keywords": ["atlas"],
         "required_context": {"entity_type": "account"},
         "context_domains": {"entity_type": ["account", "device"]}},
        {"route_id": "device", "keywords": ["atlas"],
         "required_context": {"entity_type": "device"},
         "context_domains": {"entity_type": ["account", "device"]}},
    ]
    if ordered:
        aliases.reverse()
    scenario = {"scenario_id": "support", "scenario_label": "Support",
                "routes": aliases + [{"route_id": "reset", "keywords": ["reset password"]}],
                "provider_required_route": "defer"}
    item = {"id": "request", "subject": "Reset password and route Atlas", "body": "",
            "context": {"entity_type": "unknown"}}
    result = example._run_kora_classification(scenario, item)
    assert result["selected_route"] == "defer"
    assert result["provider_calls"] == 0


@pytest.mark.parametrize("domains", [None, [], {}, {"entity_type": []}, {"entity_type": [""]}])
def test_context_domains_reject_invalid_configuration(domains):
    example = _load_example_module()
    scenario = {"scenario_id": "support", "scenario_label": "Support", "routes": [{
        "route_id": "account", "keywords": ["atlas"],
        "required_context": {"entity_type": "account"}, "context_domains": domains,
    }], "provider_required_route": "defer"}
    item = {"id": "request", "subject": "Atlas", "body": "",
            "context": {"entity_type": "unknown"}}
    with pytest.raises((RuntimeError, ValueError), match="context_domains"):
        example._run_kora_classification(scenario, item)


@pytest.mark.parametrize("route", [
    {"route_id": "account", "keywords": ["atlas"],
     "context_domains": {"entity_type": ["account", "device"]}},
    {"route_id": "account", "keywords": ["atlas"],
     "required_context": {"entity_type": "account"},
     "context_domains": {"entity_kind": ["account", "device"]}},
    {"route_id": "account", "keywords": ["atlas"],
     "required_context": {"entity_type": "account"},
     "context_domains": {"entity_type": ["device"]}},
])
def test_context_domains_require_matching_required_context(route):
    example = _load_example_module()
    scenario = {"scenario_id": "support", "scenario_label": "Support",
                "routes": [route], "provider_required_route": "defer"}
    item = {"id": "request", "subject": "Atlas", "body": "",
            "context": {"entity_type": "unknown"}}
    with pytest.raises((RuntimeError, ValueError), match="context_domains"):
        example._run_kora_classification(scenario, item)


@pytest.mark.parametrize("required", [
    {"entity_type": "account", "tenant": "Cedar"},
    {"tenant": "Cedar", "entity_type": "account"},
])
def test_known_context_mismatch_wins_over_out_of_domain_value_in_any_field_order(required):
    example = _load_example_module()
    scenario = {"scenario_id": "support", "scenario_label": "Support", "routes": [
        {"route_id": "alias", "keywords": ["atlas"], "required_context": required,
         "context_domains": {"entity_type": ["account", "device"]}},
        {"route_id": "receipt", "keywords": ["receipt"]},
    ], "provider_required_route": "defer"}
    item = {"id": "request", "subject": "Atlas and receipt", "body": "",
            "context": {"entity_type": "unknown", "tenant": "Juniper"}}
    result = example._run_kora_classification(scenario, item)
    assert result["selected_route"] == "receipt"
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


@pytest.mark.parametrize("companion", [
    "delegated privileges",
    "DELEGATED PRIVILEGES",
    "delegated admin privileges",
    "delegated privilege",
])
def test_route_scoped_provider_required_keywords_defer_companion_work(companion):
    example = _load_example_module()
    scenario = {
        "scenario_id": "support",
        "scenario_label": "Support",
        "routes": [{
            "route_id": "reset_password",
            "keywords": ["reset my password"],
            "provider_required_keywords": [
                "delegated privileges",
                "delegated admin privileges",
                "delegated privilege",
            ],
            "output": {"action": "reset_password"},
        }],
        "provider_required_route": "defer",
    }
    item = {
        "id": "request",
        "subject": f"Reset my password and restore my {companion}.",
        "body": "",
        "context": {},
    }
    result = example._run_kora_classification(scenario, item)
    assert result["selected_route"] == "defer"
    assert result["classification_output"] is None
    assert result["provider_needed_reason"] == "matched route also requires unsupported provider work"


@pytest.mark.parametrize("keywords", [[], [""], ["   "], [None], ["delegated privileges", 3], "delegated privileges"])
def test_route_scoped_provider_required_keywords_reject_invalid_configuration(keywords):
    example = _load_example_module()
    scenario = {
        "scenario_id": "support",
        "scenario_label": "Support",
        "routes": [{
            "route_id": "reset_password",
            "keywords": ["reset my password"],
            "provider_required_keywords": keywords,
            "output": {"action": "reset_password"},
        }],
        "provider_required_route": "defer",
    }
    item = {
        "id": "request",
        "subject": "Reset my password and restore my delegated privileges.",
        "body": "",
        "context": {},
    }
    with pytest.raises((RuntimeError, ValueError), match="provider_required_keywords must be nonempty strings"):
        example._run_kora_classification(scenario, item)


def test_route_scoped_provider_required_keywords_use_unicode_casefold():
    example = _load_example_module()
    scenario = {
        "scenario_id": "support",
        "scenario_label": "Support",
        "routes": [{
            "route_id": "reset_password",
            "keywords": ["reset my password"],
            "provider_required_keywords": ["STRASSE"],
            "output": {"action": "reset_password"},
        }],
        "provider_required_route": "defer",
    }
    item = {
        "id": "request",
        "subject": "Reset my password and restore Straße access.",
        "body": "",
        "context": {},
    }
    result = example._run_kora_classification(scenario, item)
    assert result["selected_route"] == "defer"
    assert result["classification_output"] is None


def test_route_keywords_use_unicode_casefold():
    example = _load_example_module()
    scenario = {
        "scenario_id": "support",
        "scenario_label": "Support",
        "routes": [{
            "route_id": "street_access",
            "keywords": ["Straße"],
            "output": {"action": "street_access"},
        }],
        "provider_required_route": "defer",
    }
    item = {
        "id": "request",
        "subject": "Open STRASSE access.",
        "body": "",
        "context": {},
    }
    result = example._run_kora_classification(scenario, item)
    assert result["selected_route"] == "street_access"
    assert result["classification_output"] == {"action": "street_access"}


@pytest.mark.parametrize("context, expected", [
    ({"as_of": "2028-02-29", "valid_until": "2028-02-29"}, "desk"),
    ({"as_of": "2028-02-28", "valid_until": "2028-02-29"}, "desk"),
    ({"as_of": "2028-03-01", "valid_until": "2028-02-29"}, "defer"),
    ({"as_of": "2028-02-29"}, "defer"),
    ({"valid_until": "2028-02-29"}, "defer"),
    ({"as_of": "2027-02-29", "valid_until": "2028-02-29"}, "defer"),
    ({"as_of": "20280229", "valid_until": "2028-02-29"}, "defer"),
    ({"as_of": "2028-02-28", "valid_until": "2028-W09-2"}, "defer"),
    ({"as_of": "2028-02-28", "valid_until": 20280229}, "defer"),
    (None, "defer"),
])
def test_freshness_requires_two_canonical_business_dates(context, expected):
    scenario = {"scenario_id": "terms", "scenario_label": "Terms", "provider_required_route": "defer",
                "routes": [{"route_id": "desk", "keywords": ["terms"], "require_fresh_context": True}]}
    item = {"id": "sample", "subject": "Terms", "body": "valid_until 2099-12-31", "context": context}
    result = _load_example_module()._run_kora_classification(scenario, item)
    assert result["selected_route"] == expected
    assert result["provider_calls"] == 0
    if expected == "defer":
        assert result["classification_output"] is None
        assert result["provider_needed_reason"]


def test_expired_applicable_route_withholds_overlapping_unscoped_answer():
    scoped = {"route_id": "priced", "keywords": ["quote"], "required_context": {"tenant": "first"},
              "require_fresh_context": True}
    unscoped = {"route_id": "other", "keywords": ["quote"]}
    example = _load_example_module()
    for routes in ([scoped, unscoped], [unscoped, scoped]):
        scenario = {"scenario_id": "price", "scenario_label": "Pricing", "provider_required_route": "defer",
                    "routes": routes}
        for tenant, expected in (("first", "defer"), ("second", "other")):
            item = {"id": "sample", "subject": "Quote", "body": "",
                    "context": {"tenant": tenant, "as_of": "2028-04-10", "valid_until": "2028-04-09"}}
            result = example._run_kora_classification(scenario, item)
            assert result["selected_route"] == expected


@pytest.mark.parametrize("flag", ["false", 1, None])
def test_invalid_freshness_option_is_rejected(flag):
    scenario = {"scenario_id": "terms", "scenario_label": "Terms", "provider_required_route": "defer",
                "routes": [{"route_id": "desk", "keywords": ["terms"], "require_fresh_context": flag}]}
    with pytest.raises((RuntimeError, ValueError), match="require_fresh_context must be a boolean"):
        _load_example_module()._run_kora_classification(scenario, {"id": "one", "subject": "Terms", "body": ""})
