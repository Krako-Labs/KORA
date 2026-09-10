"""Provider-neutral workload economics runner with exact node reuse evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kora.adapters.base import BaseAdapter

from .contracts import canonical_json_bytes, instance_error_locations


@dataclass(frozen=True)
class EconomicsNode:
    id: str
    instruction: str
    tier: str
    deps: tuple[str, ...] = ()
    cacheable: bool = True
    max_tokens: int = 512
    output_schema: dict[str, Any] | None = None


@dataclass(frozen=True)
class ExecutionPolicy:
    name: str
    routes: dict[str, str]
    exact_reuse: bool = False
    context_mode: str = "full"
    fallback_routes: dict[str, str] | None = None
    full_context_nodes: tuple[str, ...] = ()


class ExactResultStore:
    """Bounded optional persistent store for validated exact-result reuse."""

    def __init__(self, root: Path | None = None, *, capacity: int = 256) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int) or not 1 <= capacity <= 4096:
            raise ValueError("cache capacity must be an integer from 1 through 4096")
        self.root = None if root is None else Path(root)
        self.capacity = capacity
        self.memory: dict[str, dict[str, Any]] = {}
        if self.root is not None:
            self.root.mkdir(parents=True, exist_ok=True)
            if self.root.is_symlink() or not self.root.is_dir():
                raise ValueError("cache directory must be a real directory")

    @staticmethod
    def _checksum(output: dict[str, Any]) -> str:
        return hashlib.sha256(canonical_json_bytes(output)).hexdigest()

    def get(self, key: str) -> dict[str, Any] | None:
        if self.root is None:
            value = self.memory.get(key)
            return None if value is None else copy.deepcopy(value)
        target = self.root / f"{key}.json"
        if target.is_symlink():
            return None
        try:
            if target.stat().st_size > 2 * 1024 * 1024:
                return None
            entry = json.loads(target.read_text(encoding="utf-8"))
            output = entry["output"]
            if (
                entry.get("schema_version") != "kora.exact-result/v1"
                or entry.get("key") != key
                or not isinstance(output, dict)
                or entry.get("checksum") != self._checksum(output)
            ):
                return None
            return copy.deepcopy(output)
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            return None

    def put(self, key: str, output: dict[str, Any]) -> None:
        value = copy.deepcopy(output)
        if self.root is None:
            if key not in self.memory and len(self.memory) >= self.capacity:
                return
            self.memory[key] = value
            return
        target = self.root / f"{key}.json"
        if target.exists():
            return
        if len(list(self.root.glob("*.json"))) >= self.capacity:
            return
        entry = {
            "schema_version": "kora.exact-result/v1",
            "key": key,
            "output": value,
            "checksum": self._checksum(value),
        }
        fd, temporary = tempfile.mkstemp(dir=self.root, prefix=".pending-")
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(canonical_json_bytes(entry))
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


class WorkloadEconomicsRunner:
    """Execute frozen semantic nodes while recording route/call/token/reuse counters."""

    def __init__(
        self,
        *,
        nodes: tuple[EconomicsNode, ...],
        adapters: dict[str, BaseAdapter],
        cache_directory: Path | None = None,
        cache_capacity: int = 256,
    ):
        if not nodes or len({node.id for node in nodes}) != len(nodes):
            raise ValueError("nodes must be non-empty with unique ids")
        known: set[str] = set()
        for node in nodes:
            if node.tier not in {"routine", "frontier"}:
                raise ValueError("semantic node tier must be routine or frontier")
            if not set(node.deps) <= known:
                raise ValueError("node dependencies must refer to prior nodes")
            if not node.instruction.strip():
                raise ValueError("node instruction must not be empty")
            known.add(node.id)
        self.nodes = nodes
        self.adapters = dict(adapters)
        self.cache = ExactResultStore(cache_directory, capacity=cache_capacity)

    @staticmethod
    def _adapter_identity(adapter_name: str, adapter: BaseAdapter) -> dict[str, Any]:
        identity: dict[str, Any] = {
            "route": adapter_name,
            "class": f"{adapter.__class__.__module__}.{adapter.__class__.__qualname__}",
        }
        cache_identity = getattr(adapter, "cache_identity", None)
        if callable(cache_identity):
            declared = cache_identity()
            if not isinstance(declared, dict):
                raise TypeError("adapter cache_identity must return an object")
            identity["declared"] = copy.deepcopy(declared)
        else:
            model = getattr(adapter, "model", None)
            if isinstance(model, str) and model:
                identity["model"] = model
        return identity

    @classmethod
    def _cache_key(
        cls,
        node: EconomicsNode,
        adapter_name: str,
        adapter: BaseAdapter,
        payload: dict[str, Any],
        *,
        fallback_identity: dict[str, Any] | None = None,
    ) -> str:
        bound = {
            "node": {
                "id": node.id,
                "instruction": node.instruction,
                "tier": node.tier,
                "deps": list(node.deps),
                "max_tokens": node.max_tokens,
                "output_schema": node.output_schema or {"type": "object"},
            },
            "adapter": cls._adapter_identity(adapter_name, adapter),
            "fallback_adapter": copy.deepcopy(fallback_identity),
            "payload": payload,
        }
        return hashlib.sha256(canonical_json_bytes(bound)).hexdigest()

    def run(self, *, workload: dict[str, Any], policy: ExecutionPolicy) -> dict[str, Any]:
        started = time.perf_counter()
        outputs: dict[str, dict[str, Any]] = {}
        events: list[dict[str, Any]] = []
        if policy.context_mode not in {"full", "brief+deps"}:
            raise ValueError("policy context_mode must be full or brief+deps")
        for node in self.nodes:
            adapter_name = policy.routes.get(node.tier)
            if not adapter_name or adapter_name not in self.adapters:
                raise ValueError(f"policy route for {node.tier!r} is unavailable")
            effective_workload = (
                copy.deepcopy(workload)
                if policy.context_mode == "full" or not node.deps or node.id in policy.full_context_nodes
                else {"brief": copy.deepcopy(workload.get("brief", {}))}
            )
            brief = workload.get("brief")
            brief = brief if isinstance(brief, dict) else {}
            quality_contract = brief.get("quality_floor")
            quality_contract = copy.deepcopy(quality_contract) if isinstance(quality_contract, dict) else {}
            node_input = {
                "instruction": node.instruction,
                "quality_contract": quality_contract,
                "workload": effective_workload,
                "dependencies": {dep: copy.deepcopy(outputs[dep]) for dep in node.deps},
            }
            adapter = self.adapters[adapter_name]
            fallback_name = None
            fallback_identity = None
            if isinstance(policy.fallback_routes, dict):
                fallback_name = policy.fallback_routes.get(node.tier)
                if fallback_name is not None:
                    if fallback_name == adapter_name or fallback_name not in self.adapters:
                        raise ValueError(f"policy fallback route for {node.tier!r} is unavailable")
                    fallback_identity = self._adapter_identity(fallback_name, self.adapters[fallback_name])
            cache_key = (
                self._cache_key(
                    node,
                    adapter_name,
                    adapter,
                    node_input,
                    fallback_identity=fallback_identity,
                )
                if policy.exact_reuse and node.cacheable
                else None
            )
            cached = self.cache.get(cache_key) if cache_key is not None else None
            schema = node.output_schema or {"type": "object"}
            if cached is not None:
                if instance_error_locations(schema, cached):
                    raise RuntimeError(f"cached output schema failed closed at node {node.id}")
                outputs[node.id] = cached
                events.append(
                    {
                        "node_id": node.id,
                        "tier": node.tier,
                        "route": adapter_name,
                        "status": "ok",
                        "reused": True,
                        "escalated": False,
                        "model_calls": 0,
                        "tokens_in": 0,
                        "tokens_out": 0,
                        "time_ms": 0,
                        "output_digest": hashlib.sha256(canonical_json_bytes(cached)).hexdigest(),
                    }
                )
                continue
            escalated = False
            primary_error_class = None
            try:
                result = adapter.run(
                    task_id=node.id,
                    input=node_input,
                    budget={"max_tokens": node.max_tokens, "max_time_ms": 120000},
                    output_schema=schema,
                )
            except Exception as exc:
                if fallback_name is None:
                    raise
                escalated = True
                primary_error_class = type(exc).__name__
                adapter_name = fallback_name
                adapter = self.adapters[fallback_name]
                result = adapter.run(
                    task_id=node.id,
                    input=node_input,
                    budget={"max_tokens": node.max_tokens, "max_time_ms": 120000},
                    output_schema=schema,
                )
            if (
                (not isinstance(result, dict) or result.get("ok") is not True or not isinstance(result.get("output"), dict))
                and fallback_name is not None
                and not escalated
            ):
                escalated = True
                primary_error_class = "AdapterReturnedNotOk"
                adapter_name = fallback_name
                adapter = self.adapters[fallback_name]
                result = adapter.run(
                    task_id=node.id,
                    input=node_input,
                    budget={"max_tokens": node.max_tokens, "max_time_ms": 120000},
                    output_schema=schema,
                )
            if not isinstance(result, dict) or result.get("ok") is not True or not isinstance(result.get("output"), dict):
                raise RuntimeError(f"adapter failed closed at node {node.id}")
            output = copy.deepcopy(result["output"])
            if instance_error_locations(schema, output):
                raise RuntimeError(f"output schema failed closed at node {node.id}")
            outputs[node.id] = output
            if cache_key is not None:
                self.cache.put(cache_key, output)
            usage = result.get("usage") if isinstance(result.get("usage"), dict) else {}
            meta = result.get("meta") if isinstance(result.get("meta"), dict) else {}
            events.append(
                {
                    "node_id": node.id,
                    "tier": node.tier,
                    "route": adapter_name,
                    "provider": meta.get("provider") or meta.get("adapter"),
                    "escalated": escalated,
                    "primary_error_class": primary_error_class,
                    "model": meta.get("model"),
                    "status": "ok",
                    "reused": False,
                    "model_calls": int(meta.get("model_calls", 1) or 1),
                    "tokens_in": int(usage.get("tokens_in", 0) or 0),
                    "tokens_out": int(usage.get("tokens_out", 0) or 0),
                    "cached_tokens_in": int(usage.get("cached_tokens_in", 0) or 0),
                    "cache_write_tokens_in": int(usage.get("cache_write_tokens_in", 0) or 0),
                    "reasoning_tokens_out": int(usage.get("reasoning_tokens_out", 0) or 0),
                    "time_ms": int(usage.get("time_ms", 0) or 0),
                    "output_digest": hashlib.sha256(canonical_json_bytes(output)).hexdigest(),
                }
            )
        total_ms = round((time.perf_counter() - started) * 1000.0)
        return {
            "schema_version": "kora.workload-economics/v1",
            "policy": policy.name,
            "workload_digest": hashlib.sha256(canonical_json_bytes(workload)).hexdigest(),
            "total_time_ms": total_ms,
            "model_calls": sum(event["model_calls"] for event in events),
            "tokens_in": sum(event["tokens_in"] for event in events),
            "tokens_out": sum(event["tokens_out"] for event in events),
            "cached_tokens_in": sum(event.get("cached_tokens_in", 0) for event in events),
            "cache_write_tokens_in": sum(event.get("cache_write_tokens_in", 0) for event in events),
            "reasoning_tokens_out": sum(event.get("reasoning_tokens_out", 0) for event in events),
            "exact_reuse_hits": sum(event["reused"] for event in events),
            "escalations": sum(1 for event in events if event.get("escalated")),
            "events": events,
            "output": outputs[self.nodes[-1].id],
        }


def compare_economics(baseline: dict[str, Any], kora: dict[str, Any]) -> dict[str, Any]:
    """Return arithmetic deltas only; callers own any cost/quality interpretation."""
    def reduction(key: str) -> float | None:
        left = int(baseline.get(key, 0) or 0)
        right = int(kora.get(key, 0) or 0)
        if left <= 0:
            return None
        return round((left - right) / left * 100.0, 4)
    return {
        "baseline_policy": baseline.get("policy"),
        "kora_policy": kora.get("policy"),
        "model_call_reduction_percent": reduction("model_calls"),
        "input_token_reduction_percent": reduction("tokens_in"),
        "output_token_reduction_percent": reduction("tokens_out"),
        "baseline_model_calls": baseline.get("model_calls"),
        "kora_model_calls": kora.get("model_calls"),
        "baseline_tokens_in": baseline.get("tokens_in"),
        "kora_tokens_in": kora.get("tokens_in"),
        "baseline_tokens_out": baseline.get("tokens_out"),
        "kora_tokens_out": kora.get("tokens_out"),
        "kora_exact_reuse_hits": kora.get("exact_reuse_hits"),
    }


__all__ = [
    "EconomicsNode",
    "ExactResultStore",
    "ExecutionPolicy",
    "WorkloadEconomicsRunner",
    "compare_economics",
]
