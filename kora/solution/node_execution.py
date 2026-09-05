"""Versioned, offline typed dataflow over trusted single-node runtime calls."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from kora.task_ir import TaskGraph

from .contracts import (
    canonical_json_bytes,
    instance_error_locations,
    validate_contract_instance,
)
from .reference_runtime import (
    ReferenceRuntimeError,
    RuntimeExecution,
    _topological_tasks,
)
from .runtime_registry import (
    CapabilityRegistryError,
    LocalCapabilityRegistry,
    ResolvedRuntime,
)

PLAN_VERSION = "kora.node-execution/v1"
EVIDENCE_VERSION = "kora.node-evidence/v1"
MAX_NODES = 64


def _fail(detail: str) -> None:
    raise ValueError(detail)


def _schema(schema: Any) -> None:
    if not isinstance(schema, dict) or schema.get("type") != "object":
        _fail("node schemas must declare object type")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ValueError("invalid node schema") from exc

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if any(
                key in value for key in ("$ref", "$dynamicRef", "$recursiveRef", "$id")
            ):
                _fail("node schemas must be self-contained without references")
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(schema)


def validate_node_plan(plan: Any, graph: TaskGraph) -> None:
    """Reject malformed contracts before any runtime execution."""
    validate_contract_instance("node-execution.schema.json", plan)
    if not isinstance(plan, dict) or set(plan) != {"schema_version", "nodes"}:
        _fail("invalid node execution contract")
    if plan["schema_version"] != PLAN_VERSION:
        _fail("unsupported node execution contract")
    nodes = plan["nodes"]
    if not isinstance(nodes, dict) or not 1 <= len(nodes) <= MAX_NODES:
        _fail("node execution contract exceeds node limits")
    if set(nodes) != {task.id for task in graph.tasks}:
        _fail("contract must cover exactly the graph nodes")
    ancestors: dict[str, set[str]] = {}
    for task in _topological_tasks(graph):
        if task.run.kind != "det" or task.in_ or task.policy.on_fail != "fail":
            _fail(
                "node mode requires deterministic tasks, empty legacy inputs and fail policy"
            )
        if task.verify is not None or task.policy.adaptive is not None:
            _fail(
                "node mode uses declared node schemas, without legacy verification or adaptive policy"
            )
        ancestors[task.id] = set(task.deps)
        for dep in task.deps:
            ancestors[task.id].update(ancestors[dep])
        node = nodes[task.id]
        if not isinstance(node, dict) or set(node) != {
            "bindings",
            "input_schema",
            "output_schema",
        }:
            _fail("invalid node contract")
        _schema(node["input_schema"])
        _schema(node["output_schema"])
        bindings = node["bindings"]
        if not isinstance(bindings, dict) or set(bindings) & set(task.run.spec.args):
            _fail("bindings and static arguments must not overlap")
        for binding in bindings.values():
            if not isinstance(binding, dict):
                _fail("bindings must be explicit source objects")
            source = binding.get("source")
            required = (
                {"source", "path"} if source == "input" else {"source", "node", "path"}
            )
            if source not in {"input", "node"} or set(binding) != required:
                _fail("invalid binding source")
            path = binding["path"]
            if (
                not isinstance(path, list)
                or len(path) > 16
                or any(not isinstance(part, str) or len(part) > 128 for part in path)
            ):
                _fail("binding paths must contain bounded object keys")
            if source == "node" and binding["node"] not in ancestors[task.id]:
                _fail("node bindings must reference graph ancestors")


def load_node_plan(package: Path, relative: str, graph: TaskGraph) -> dict[str, Any]:
    plan = json.loads((package / relative).read_text(encoding="utf-8"))
    validate_node_plan(plan, graph)
    return plan


def _bound_value(binding: dict[str, Any], payload: Any, outputs: dict[str, Any]) -> Any:
    current = payload if binding["source"] == "input" else outputs[binding["node"]]
    for part in binding["path"]:
        if not isinstance(current, dict) or part not in current:
            raise ReferenceRuntimeError(
                "runtime_failure", "node binding value is missing"
            )
        current = current[part]
    return copy.deepcopy(current)


class NodeCoordinator:
    """Host-owned coordinator; not a registered model or external plugin."""

    def __init__(
        self, plan: dict[str, Any], graph: TaskGraph, registry: LocalCapabilityRegistry
    ):
        self.plan = copy.deepcopy(plan)
        self.graph = graph.model_copy(deep=True)
        self.registry = registry
        self.selected = {}
        for task in _topological_tasks(graph):
            self.selected[task.id] = registry.resolve(
                {task.run.spec.handler},
                protocol_version="kora.dev/v0alpha1",
                task_kinds={"det"},
            )
        self.capabilities = frozenset(task.run.spec.handler for task in graph.tasks)
        # The digest binds both the contract and selected runtime identities.
        self.descriptor = {
            "runtime": {"id": "kora.node-coordinator", "version": "1.0.0"},
            "contract": self.plan,
            "graph": graph.model_dump(mode="json", by_alias=True),
            "nodes": {key: value.identity for key, value in self.selected.items()},
        }

    def resolve(self) -> ResolvedRuntime:
        return ResolvedRuntime(
            descriptor=copy.deepcopy(self.descriptor),
            descriptor_digest=hashlib.sha256(
                canonical_json_bytes(self.descriptor)
            ).hexdigest(),
            runtime=self,
        )

    def execute(
        self,
        graph: TaskGraph,
        input_payload: dict[str, Any],
        *,
        run_directory: Path,
        package_root: Path | None = None,
        approvals=(),
        declared_side_effects=(),
    ) -> RuntimeExecution:
        del graph  # Execute the validated, frozen plan.
        outputs: dict[str, Any] = {}
        executed: list[str] = []
        records = [
            {
                "node_id": task.id,
                "capability": task.run.spec.handler,
                "runtime": self.selected[task.id].identity,
                "state": "pending",
                "input_valid": False,
                "output_valid": False,
                "error": None,
            }
            for task in _topological_tasks(self.graph)
        ]
        evidence = {"schema_version": EVIDENCE_VERSION, "nodes": records}
        target = run_directory / "node-evidence.json"

        def persist() -> None:
            validate_contract_instance("node-evidence.schema.json", evidence)
            temporary = target.with_suffix(".tmp")
            temporary.write_bytes(canonical_json_bytes(evidence))
            temporary.replace(target)

        persist()
        try:
            for task, record in zip(_topological_tasks(self.graph), records):
                record["state"] = "validating"
                persist()
                selected = self.selected[task.id]
                # Detect changed registry selection/integrity between nodes.
                current = self.registry.resolve(
                    {task.run.spec.handler},
                    protocol_version="kora.dev/v0alpha1",
                    task_kinds={"det"},
                )
                if current.identity != selected.identity:
                    raise ReferenceRuntimeError(
                        "runtime_failure", "node runtime identity changed"
                    )
                effects = {
                    tag.removeprefix("side_effect:")
                    for tag in task.tags
                    if tag.startswith("side_effect:")
                }
                if not effects <= set(declared_side_effects) or not effects <= set(
                    approvals
                ):
                    raise ReferenceRuntimeError(
                        "approval_required", "node side effect is not authorized"
                    )
                node = self.plan["nodes"][task.id]
                params = copy.deepcopy(task.run.spec.args)
                params.update(
                    {
                        key: _bound_value(binding, input_payload, outputs)
                        for key, binding in node["bindings"].items()
                    }
                )
                if instance_error_locations(node["input_schema"], params):
                    raise ReferenceRuntimeError(
                        "input_validation_failed", "node input schema rejected"
                    )
                record["input_valid"] = True
                record["state"] = "running"
                persist()
                one = task.model_copy(deep=True)
                one.deps = []
                one.in_ = {}
                # Literal values stay in static args: strings beginning with '$.'
                # must never be reinterpreted as paths by a legacy runtime.
                one.run.spec.args = copy.deepcopy(params)
                single = self.graph.model_copy(deep=True)
                single.tasks = [one]
                single.root = one.id
                # Use index, not package node id, as a filesystem component.
                node_directory = run_directory / "nodes" / str(len(outputs))
                node_directory.mkdir(parents=True, exist_ok=False)
                result = selected.runtime.execute(
                    single,
                    {},
                    run_directory=node_directory,
                    package_root=package_root,
                    approvals=frozenset(approvals),
                    declared_side_effects=frozenset(declared_side_effects),
                )
                if tuple(result.capabilities_executed) != (task.run.spec.handler,):
                    raise ReferenceRuntimeError(
                        "runtime_failure", "node capability evidence mismatch"
                    )
                if instance_error_locations(node["output_schema"], result.output):
                    raise ReferenceRuntimeError(
                        "output_validation_failed", "node output schema rejected"
                    )
                # Detach downstream values from mutable plugin-owned output.
                outputs[task.id] = copy.deepcopy(result.output)
                record["output_valid"] = True
                record["state"] = "succeeded"
                if task.run.spec.handler not in executed:
                    executed.append(task.run.spec.handler)
                persist()
        except Exception as exc:
            for record in records:
                if record["state"] in {"validating", "running"}:
                    record["state"] = "failed"
                    record["error"] = "node_execution_failed"
                elif record["state"] == "pending":
                    record["state"] = "skipped"
            persist()
            if isinstance(exc, ReferenceRuntimeError):
                raise
            if isinstance(exc, CapabilityRegistryError):
                raise ReferenceRuntimeError(
                    "runtime_failure", "node registry verification failed"
                ) from exc
            raise ReferenceRuntimeError(
                "runtime_failure", "node execution failed closed"
            ) from exc
        return RuntimeExecution(
            output=outputs[self.graph.root], capabilities_executed=tuple(executed)
        )
