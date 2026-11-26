"""Evaluate a fixed support routing policy with business inputs isolated from the answer key."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from time import perf_counter_ns
from typing import Any, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

from kora.executor import run_graph
from kora.task_ir import TaskGraph, normalize_graph, validate_graph


HERE = Path(__file__).resolve().parent
SPLITS = ("dev", "holdout")
Split = Literal["dev", "holdout"]
Family = Literal["tenant_meaning", "multiple_intents", "entity_collision", "stale_or_missing"]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Context(Record):
    tenant: str | None = None
    entity_type: str | None = None
    as_of: str | None = None
    valid_until: str | None = None


class Request(Record):
    text: str = Field(min_length=1)
    context: Context

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, text: str) -> str:
        if not text.strip():
            raise ValueError("Request text must contain a non-whitespace character")
        return text


class RequestRecord(Request):
    id: str = Field(min_length=1)


class Answer(Record):
    id: str = Field(min_length=1)
    pair: str = Field(min_length=1)
    split: Split
    family: Family
    # Null means that the contract requires deferral.
    action: str | None = Field(min_length=1)


RecordT = TypeVar("RecordT", RequestRecord, Answer)


def read_records(path: Path, record_type: type[RecordT]) -> dict[str, RecordT]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{path.name}: expected a nonempty array")
    records: dict[str, RecordT] = {}
    for row in rows:
        record = record_type.model_validate(row)
        if record.id in records:
            raise ValueError(f"{path.name}: duplicate id {record.id}")
        records[record.id] = record
    return records


def validate_pairs(requests: dict[str, RequestRecord], answers: dict[str, Answer]) -> None:
    if requests.keys() != answers.keys():
        raise ValueError("Request IDs and answer IDs must match exactly")
    groups: dict[str, list[Answer]] = defaultdict(list)
    for answer in answers.values():
        groups[answer.pair].append(answer)
    for pair, group in groups.items():
        if len(group) != 2 or len({(a.split, a.family) for a in group}) != 1:
            raise ValueError(f"{pair}: expected two cases in the same split and family")
        if group[0].action == group[1].action:
            raise ValueError(f"{pair}: expected two different outcomes")
    signatures = {
        (" ".join(r.text.casefold().split()), r.context.model_dump_json())
        for r in requests.values()
    }
    if len(signatures) != len(requests):
        raise ValueError("Duplicate business input")


def route(request: Request, rules: list[dict[str, Any]]) -> dict[str, Any]:
    """Execute the same graph shape for every case. Control IDs never enter this boundary."""
    graph = TaskGraph.model_validate({
        "graph_id": "support-request",
        "version": "0.1",
        "root": "classify",
        "defaults": {},
        "tasks": [{
            "id": "classify",
            "type": "det.classification.support",
            "in": {"text": request.text, "context": request.context.model_dump(exclude_none=True)},
            "run": {"kind": "det", "spec": {
                "handler": "classify_by_rules",
                "args": {"scenario_id": "support", "routes": rules},
            }},
        }],
    })
    graph = normalize_graph(graph)
    validate_graph(graph)
    result = run_graph(graph)
    if not result.get("ok"):
        raise RuntimeError(f"Classification failed: {result.get('error')}")
    final = result["final"]
    if final["provider_calls"] != 0 or final["route_kind"] not in {"deterministic", "provider_required"}:
        raise RuntimeError("Unexpected execution mode in offline routing evaluation")
    return final


def score(answer: Answer, prediction: dict[str, Any]) -> str:
    direct = prediction["route_kind"] == "deterministic"
    if answer.action is None:
        return "false_bypass" if direct else "correct_deferral"
    if not direct:
        return "unnecessary_escalation"
    if prediction["classification_output"] == {"action": answer.action}:
        return "correct_direct"
    return "wrong_direct_output"


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(row["outcome"] for row in rows)
    deferred_gold = counts["false_bypass"] + counts["correct_deferral"]
    directly_answered = counts["wrong_direct_output"] + counts["correct_direct"]
    direct_gold = directly_answered + counts["unnecessary_escalation"]
    return {
        "tasks": len(rows),
        "provider_calls": sum(r["provider_calls"] for r in rows),
        "false_bypass": {"count": counts["false_bypass"], "denominator": deferred_gold},
        "unnecessary_escalation": {"count": counts["unnecessary_escalation"], "denominator": direct_gold},
        "wrong_direct_output": {"count": counts["wrong_direct_output"], "denominator": directly_answered},
        "correct_direct": {"count": counts["correct_direct"], "denominator": directly_answered},
        "correct_deferral": {"count": counts["correct_deferral"], "denominator": deferred_gold},
    }


def evaluate(
    *,
    split: str = "dev",
    rules_path: Path = HERE / "baseline_rules.json",
    requests_path: Path = HERE / "requests.json",
    gold_path: Path = HERE / "gold.json",
    timing: bool = False,
) -> dict[str, Any]:
    if split not in (*SPLITS, "all"):
        raise ValueError(f"Unknown split {split!r}")
    records = read_records(requests_path, RequestRecord)
    answers = read_records(gold_path, Answer)
    validate_pairs(records, answers)
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    if not isinstance(rules, list) or not rules:
        raise ValueError("Expected a nonempty list of routing rules")
    rows = []
    for record_id in sorted(records):
        answer = answers[record_id]
        if split != "all" and split != answer.split:
            continue
        record = records[record_id]
        request = Request(text=record.text, context=record.context)
        start = perf_counter_ns() if timing else 0
        prediction = route(request, rules)
        elapsed = perf_counter_ns() - start if timing else None
        row = {
            **answer.model_dump(exclude={"action"}),
            "request": request.model_dump(exclude_none=True),
            "expected_route": "provider_required" if answer.action is None else "deterministic",
            "expected_action": answer.action,
            "actual_route": prediction["route_kind"],
            "selected_route": prediction["selected_route"],
            "actual_output": prediction["classification_output"],
            "fallback_reason": prediction["provider_needed_reason"],
            "provider_calls": prediction["provider_calls"],
            "outcome": score(answer, prediction),
        }
        if timing:
            row["local_decision_ns"] = elapsed
        rows.append(row)
    if not rows:
        raise ValueError(f"No requests in split {split!r}")
    by_route = defaultdict(list)
    for row in rows:
        by_route[row["selected_route"]].append(row)
    return {
        "split": split,
        "summary": summarize(rows),
        "by_selected_route": {name: summarize(items) for name, items in sorted(by_route.items())},
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=(*SPLITS, "all"), default="dev")
    parser.add_argument("--rules", type=Path, default=HERE / "baseline_rules.json")
    parser.add_argument("--timing", action="store_true", help="Include local graph decision time")
    args = parser.parse_args()
    print(json.dumps(evaluate(split=args.split, rules_path=args.rules, timing=args.timing), indent=2))


if __name__ == "__main__":
    main()
