"""Loopback-only OpenAI-compatible adapter for user-owned local model servers."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any
from urllib import error, parse, request

from .base import BaseAdapter


class LocalOpenAICompatibleError(RuntimeError):
    """Raised when an explicitly configured loopback model endpoint is invalid."""


def _loopback_endpoint(raw: str) -> str:
    value = raw.strip().rstrip("/")
    if not value:
        raise LocalOpenAICompatibleError("local endpoint is not configured")
    parsed = parse.urlparse(value)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise LocalOpenAICompatibleError("local endpoint must use loopback HTTP")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise LocalOpenAICompatibleError("local endpoint must not contain credentials, query, or fragment")
    return value




def _schema_hint(schema: dict[str, Any]) -> dict[str, Any]:
    """Return a compact non-authoritative shape hint for constrained local models."""
    if not isinstance(schema, dict) or schema.get("type") != "object":
        return {}
    properties = schema.get("properties")
    required = schema.get("required")
    if not isinstance(properties, dict) or not isinstance(required, list):
        return {}
    hint: dict[str, Any] = {}
    for key in required:
        if not isinstance(key, str):
            continue
        child = properties.get(key)
        if not isinstance(child, dict):
            continue
        child_type = child.get("type")
        item: dict[str, Any] = {"type": child_type}
        if child_type == "array":
            child_items = child.get("items")
            if isinstance(child_items, dict):
                item["items_type"] = child_items.get("type")
                if child_items.get("type") == "object" and isinstance(child_items.get("required"), list):
                    item["item_required_keys"] = child_items["required"]
        hint[key] = item
    return hint


class OpenAICompatibleLocalAdapter(BaseAdapter):
    """Call an already-running local OpenAI-compatible server with no remote fallback."""

    def __init__(self, *, environ: dict[str, str] | None = None) -> None:
        self._environ = dict(os.environ if environ is None else environ)
        self.endpoint = _loopback_endpoint(self._environ.get("KORA_LOCAL_OPENAI_ENDPOINT", ""))
        self.model = self._environ.get("KORA_LOCAL_OPENAI_MODEL", "").strip()
        self.runtime_id = self._environ.get("KORA_LOCAL_OPENAI_RUNTIME_ID", "").strip()
        direct_key = self._environ.get("KORA_LOCAL_OPENAI_API_KEY", "").strip()
        key_file_raw = self._environ.get("KORA_LOCAL_OPENAI_API_KEY_FILE", "").strip()
        if direct_key and key_file_raw:
            raise LocalOpenAICompatibleError(
                "configure either KORA_LOCAL_OPENAI_API_KEY or KORA_LOCAL_OPENAI_API_KEY_FILE, not both"
            )
        if key_file_raw:
            key_file = Path(key_file_raw).expanduser()
            if key_file.is_symlink() or not key_file.is_file() or key_file.stat().st_size > 8192:
                raise LocalOpenAICompatibleError("local API key file must be a bounded regular file")
            self.api_key = key_file.read_text(encoding="utf-8").strip()
        else:
            self.api_key = direct_key
        if not self.model:
            raise LocalOpenAICompatibleError("KORA_LOCAL_OPENAI_MODEL is required")
        timeout = self._environ.get("KORA_LOCAL_OPENAI_TIMEOUT_S", "120").strip()
        try:
            self.timeout_s = float(timeout)
        except ValueError as exc:
            raise LocalOpenAICompatibleError("KORA_LOCAL_OPENAI_TIMEOUT_S must be numeric") from exc
        if self.timeout_s <= 0:
            raise LocalOpenAICompatibleError("KORA_LOCAL_OPENAI_TIMEOUT_S must be positive")


    def cache_identity(self) -> dict[str, Any]:
        """Return non-secret execution identity used to bind exact-result reuse."""
        if not self.runtime_id:
            raise LocalOpenAICompatibleError(
                "KORA_LOCAL_OPENAI_RUNTIME_ID is required for persistent exact-result reuse"
            )
        return {
            "adapter": "openai_compatible_local",
            "contract_version": "openai-compatible-local/v2-json-schema",
            "endpoint": self.endpoint,
            "model": self.model,
            "runtime_id": self.runtime_id,
        }

    def run(
        self,
        *,
        task_id: str,
        input: dict[str, Any],
        budget: dict[str, Any],
        output_schema: dict[str, Any],
    ) -> dict[str, Any]:
        max_tokens = budget.get("max_tokens", 256)
        if isinstance(max_tokens, bool) or not isinstance(max_tokens, int):
            max_tokens = 256
        max_tokens = max(1, min(max_tokens, 2048))
        required_keys = output_schema.get("required", []) if isinstance(output_schema, dict) else []
        prompt = json.dumps(
            {
                "task_id": task_id,
                "input": input,
                "required_output_keys": required_keys,
                "output_shape": _schema_hint(output_schema),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        body = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Return one valid JSON object only. No markdown. Include every required output key exactly as named and follow output_shape types exactly.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": max_tokens,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "kora_local_output",
                    "strict": True,
                    "schema": output_schema,
                },
            },
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = request.Request(
            self.endpoint + "/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        start = time.perf_counter()
        try:
            with request.urlopen(req, timeout=self.timeout_s) as response:
                payload = json.load(response)
        except (OSError, error.URLError, json.JSONDecodeError) as exc:
            raise LocalOpenAICompatibleError(
                f"local OpenAI-compatible request failed: {type(exc).__name__}; no remote fallback was attempted"
            ) from exc
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        try:
            choice = payload["choices"][0]
            text = choice["message"]["content"]
            finish_reason = choice.get("finish_reason") if isinstance(choice, dict) else None
            output = json.loads(text)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            reason = "truncated output" if locals().get("finish_reason") == "length" else "invalid JSON output"
            raise LocalOpenAICompatibleError(
                f"local model returned {reason} for task {task_id}; no remote fallback was attempted"
            ) from exc
        if not isinstance(output, dict):
            raise LocalOpenAICompatibleError("local model JSON output must be an object")
        usage = payload.get("usage") if isinstance(payload, dict) else {}
        usage = usage if isinstance(usage, dict) else {}
        return {
            "ok": True,
            "output": output,
            "usage": {
                "time_ms": round(elapsed_ms),
                "tokens_in": int(usage.get("prompt_tokens", 0) or 0),
                "tokens_out": int(usage.get("completion_tokens", 0) or 0),
            },
            "meta": {
                "adapter": "openai_compatible_local",
                "provider": "local",
                "model": self.model,
                "model_calls": 1,
                "network": "loopback",
                "remote_provider_calls": 0,
            },
        }


__all__ = ["LocalOpenAICompatibleError", "OpenAICompatibleLocalAdapter"]
