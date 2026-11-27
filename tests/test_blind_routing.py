import json
import sys
from collections import Counter, defaultdict

import pytest
from pydantic import ValidationError

from experiments.blind_routing import run


def test_fixed_pairs_and_grouped_splits():
    requests = run.read_records(run.HERE / "requests.json", run.RequestRecord)
    answers = run.read_records(run.HERE / "gold.json", run.Answer)
    run.validate_pairs(requests, answers)
    assert len(requests) == 24
    groups = defaultdict(set)
    for row in answers.values():
        groups[row.family, row.split].add(row.pair)
    assert len(groups) == 8
    assert all(len(pairs) == (1 if split == "dev" else 2) for (_, split), pairs in groups.items())


def test_runtime_receives_only_business_input_and_fixed_policy(monkeypatch):
    captured = []
    real_run_graph = run.run_graph

    def spy(graph):
        task = graph.tasks[0]
        captured.append((graph.graph_id, task.id, task.in_, task.run.spec.args))
        return real_run_graph(graph)

    monkeypatch.setattr(run, "run_graph", spy)
    result = run.evaluate(split="dev")
    assert len(captured) == len(result["rows"]) == 8
    assert {name for name, _, _, _ in captured} == {"support-request"}
    assert {name for _, name, _, _ in captured} == {"classify"}
    rules = json.loads((run.HERE / "baseline_rules.json").read_text())
    for (_, _, business_input, args), row in zip(captured, result["rows"], strict=True):
        assert business_input == row["request"]
        assert set(business_input) == {"text", "context"}
        assert args == {"scenario_id": "support", "routes": rules}


def test_gold_change_does_not_change_runtime_decisions(tmp_path):
    raw = json.loads((run.HERE / "gold.json").read_text())
    for answer in raw:
        if answer["action"] == "review_queue":
            answer["action"] = "different_oracle_action"
    modified_gold = tmp_path / "gold.json"
    modified_gold.write_text(json.dumps(raw))
    original = run.evaluate(split="dev")
    modified = run.evaluate(split="dev", gold_path=modified_gold)
    for before, after in zip(original["rows"], modified["rows"], strict=True):
        for name in ("selected_route", "actual_output", "fallback_reason"):
            assert before[name] == after[name]
    assert original["summary"] != modified["summary"]


@pytest.mark.parametrize("bad", [{"expected_route": "provider_required"},
                                 {"context": {"family": "tenant_meaning"}}])
def test_unrecognized_input_fields_rejected(tmp_path, bad):
    raw = json.loads((run.HERE / "requests.json").read_text())
    raw[0].update(bad)
    path = tmp_path / "requests.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(ValidationError):
        run.evaluate(requests_path=path)


@pytest.mark.parametrize("defect,match", [("duplicate", "duplicate id"), ("missing", "IDs"),
                                         ("split", "same split"), ("same", "different outcomes")])
def test_malformed_answer_key_rejected(tmp_path, defect, match):
    raw = json.loads((run.HERE / "gold.json").read_text())
    if defect == "duplicate":
        raw.append(raw[0])
    elif defect == "missing":
        raw.pop()
    elif defect == "split":
        raw[0]["split"] = "dev" if raw[0]["split"] == "holdout" else "holdout"
    elif defect == "same":
        other = next(a for a in raw if a["pair"] == raw[0]["pair"] and a["id"] != raw[0]["id"])
        raw[0]["action"] = other["action"]
    path = tmp_path / "gold.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match=match):
        run.evaluate(gold_path=path)


def test_metrics_distinguish_all_error_modes_and_denominators():
    cases = [
        (None, "deterministic", "x", "false_bypass"),
        (None, "provider_required", None, "correct_deferral"),
        ("x", "provider_required", None, "unnecessary_escalation"),
        ("y", "deterministic", "x", "wrong_direct_output"),
        ("x", "deterministic", "x", "correct_direct"),
    ]
    rows = []
    for action, kind, observed, expected in cases:
        answer = run.Answer(id="q", pair="p", family="entity_collision", split="dev", action=action)
        prediction = {"route_kind": kind, "classification_output": {"action": observed}}
        assert run.score(answer, prediction) == expected
        rows.append({"outcome": expected, "provider_calls": 0})
    summary = run.summarize(rows)
    for key, denominator in [("false_bypass", 2), ("correct_deferral", 2), ("unnecessary_escalation", 3),
                             ("wrong_direct_output", 2), ("correct_direct", 2)]:
        assert summary[key] == {"count": 1, "denominator": denominator}


def test_default_stable_output_and_local_timing():
    first = run.evaluate(split="dev")
    assert first == run.evaluate(split="dev")
    assert first["summary"]["provider_calls"] == 0
    assert sum(s["tasks"] for s in first["by_selected_route"].values()) == 8
    outcomes = Counter(row["outcome"] for row in first["rows"])
    assert sum(outcomes.values()) == 8
    assert all("local_decision_ns" not in row for row in first["rows"])
    timed = run.evaluate(split="dev", timing=True)
    assert all(row["local_decision_ns"] >= 0 for row in timed["rows"])


def test_scoped_policy_preserves_known_tenant_and_defers_missing_tenant():
    baseline = run.evaluate()
    candidate = run.evaluate(rules_path=run.HERE / "tenant_rules.json")
    before = {row["id"]: row for row in baseline["rows"]}
    status_rows = [row for row in candidate["rows"] if row["family"] == "tenant_meaning"]
    assert len(status_rows) == 2
    for row in status_rows:
        assert before[row["id"]]["actual_route"] == "deterministic"
        if row["request"]["context"]:
            assert row["actual_output"] == before[row["id"]]["actual_output"] == {"action": "review_queue"}
        else:
            assert row["actual_route"] == "provider_required"
            assert row["actual_output"] is None


def test_default_dev_only_api_and_cli(monkeypatch, capsys):
    assert {row["split"] for row in run.evaluate()["rows"]} == {"dev"}
    monkeypatch.setattr(sys, "argv", ["run"])
    run.main()
    result = json.loads(capsys.readouterr().out)
    assert result["split"] == "dev"
    assert len(result["rows"]) == 8
    assert {row["split"] for row in result["rows"]} == {"dev"}


def test_rejects_whitespace_only_request():
    with pytest.raises(ValidationError, match="non-whitespace"):
        run.Request(text="  \t\n", context=run.Context())


def test_case_and_whitespace_variants_are_duplicate_business_input(tmp_path):
    raw = json.loads((run.HERE / "requests.json").read_text())
    raw[1]["text"] = "  " + raw[0]["text"].swapcase().replace(" ", "  ") + "  "
    raw[1]["context"] = raw[0]["context"]
    path = tmp_path / "requests.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match="Duplicate business input"):
        run.evaluate(requests_path=path)


def test_hardened_policy_changes_only_declared_public_regression_cases():
    prior = run.evaluate(split="all", rules_path=run.HERE / "tenant_rules.json")
    fresh = run.evaluate(split="all", rules_path=run.HERE / "freshness_rules.json")
    changed = []
    for before, after in zip(prior["rows"], fresh["rows"], strict=True):
        assert before["id"] == after["id"]
        if before["id"] in {"r164", "r263", "r901", "r937"}:
            assert before["family"] == after["family"] == "entity_collision"
            assert after["outcome"] in {"correct_direct", "correct_deferral"}
            changed.append(after["id"])
        elif before["id"] == "r645":
            assert before["outcome"] == "false_bypass"
            assert after["outcome"] == "correct_deferral"
            assert after["fallback_reason"] == "matched route also requires unsupported provider work"
            changed.append(after["id"])
        elif before["family"] != "stale_or_missing" or before["expected_action"] is not None:
            assert after == before
        else:
            assert before["outcome"] == "false_bypass"
            assert after["outcome"] == "correct_deferral"
            assert after["fallback_reason"]
            changed.append(after["id"])
    assert changed == ["r164", "r263", "r400", "r521", "r591", "r645", "r901", "r937"]
    assert fresh["summary"]["provider_calls"] == 0


def test_freshness_policy_preserves_r104_and_routes_entity_aliases_by_context():
    rows = {
        row["id"]: row
        for row in run.evaluate(split="all", rules_path=run.HERE / "freshness_rules.json")["rows"]
    }
    assert rows["r104"]["actual_route"] == "deterministic"
    assert rows["r104"]["actual_output"] == {"action": "reset_password"}
    assert rows["r104"]["outcome"] == "correct_direct"
    assert rows["r263"]["actual_route"] == "provider_required"
    assert rows["r263"]["actual_output"] is None
    assert rows["r263"]["outcome"] == "correct_deferral"


@pytest.mark.parametrize("text,entity,expected", [
    ("Please route this to the device desk.", None, "device_desk"),
    ("Please route this to the device desk.", "device", "device_desk"),
    ("Please route Atlas to the device desk.", "device", "provider_required.support"),
    ("Please route Atlas to the device desk.", "account", "provider_required.support"),
    ("I need help with Atlas.", None, "provider_required.support"),
    ("I need help with Atlas.", "device", "device_desk"),
    ("I need help with Atlas.", "account", "account_desk"),
    ("I need help with Atlas.", "unknown", "provider_required.support"),
])
def test_original_entity_boundary_controls(text, entity, expected):
    request = run.Request(text=text, context=run.Context(entity_type=entity))
    result = run.route(request, json.loads((run.HERE / "freshness_rules.json").read_text()))
    assert result["selected_route"] == expected
    assert result["provider_calls"] == 0


@pytest.mark.parametrize("entity", [None, "unknown", "account", "device"])
@pytest.mark.parametrize("alias", ["Atlas", "Phoenix", "Summit"])
def test_entity_aliases_require_known_compatible_context(entity, alias):
    request = run.Request(text=f"Please route {alias}.", context=run.Context(entity_type=entity))
    result = run.route(request, json.loads((run.HERE / "freshness_rules.json").read_text()))
    expected = {"account": "account_desk", "device": "device_desk"}.get(entity, "provider_required.support")
    assert result["selected_route"] == expected
    assert result["provider_calls"] == 0


def test_entity_alias_rules_share_keywords_and_context_domain():
    rules = json.loads((run.HERE / "freshness_rules.json").read_text())
    aliases = [rule for rule in rules if rule["route_id"] in {"account_desk", "device_desk"}
               and "required_context" in rule]
    assert len(aliases) == 2
    assert aliases[0]["keywords"] == aliases[1]["keywords"]
    assert aliases[0]["context_domains"] == aliases[1]["context_domains"] == {
        "entity_type": ["account", "device"]
    }


@pytest.mark.parametrize("entity", [None, "unknown", "account", "device"])
@pytest.mark.parametrize("text,expected", [
    ("Please route this to the device desk.", "device_desk"),
    ("Please route Atlas to the device desk.", "provider_required.support"),
])
def test_recovery_type_boundary_controls(entity, text, expected):
    request = run.Request(text=text, context=run.Context(entity_type=entity))
    result = run.route(request, json.loads((run.HERE / "freshness_rules.json").read_text()))
    assert result["selected_route"] == expected
    assert result["provider_calls"] == 0


@pytest.mark.parametrize("text", [
    "Please reset my password and route Atlas to the right desk.",
    "Send my receipt and route Summit to the right desk.",
    "Please track my parcel and route Phoenix to the right desk.",
    "Please cancel my order and route Phoenix to the right desk.",
])
def test_out_of_domain_entity_alias_defers_supported_companion_intent(text):
    request = run.Request(text=text, context=run.Context(entity_type="unknown"))
    result = run.route(request, json.loads((run.HERE / "freshness_rules.json").read_text()))
    assert result["selected_route"] == "provider_required.support"
    assert result["provider_calls"] == 0


@pytest.mark.parametrize("text,expected", [
    ("Please reset my password.", "reset_password"),
    ("Send my receipt.", "send_receipt"),
    ("Please track my parcel.", "track_parcel"),
    ("Please cancel my order.", "cancel_order"),
])
def test_out_of_domain_entity_context_does_not_block_unrelated_single_intent(text, expected):
    request = run.Request(text=text, context=run.Context(entity_type="unknown"))
    result = run.route(request, json.loads((run.HERE / "freshness_rules.json").read_text()))
    assert result["selected_route"] == expected
    assert result["provider_calls"] == 0
