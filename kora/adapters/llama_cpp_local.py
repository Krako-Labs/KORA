"""Fail-closed subprocess adapter for an explicitly configured local llama.cpp runtime."""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
from typing import Any, Callable

from .base import BaseAdapter

Runner = Callable[..., subprocess.CompletedProcess[str]]


class LlamaCppLocalRuntimeError(RuntimeError):
    """The explicitly configured local llama.cpp runtime could not be used."""


_LOAD_RE = re.compile(r"load time\s*=\s*([0-9.]+)\s*ms")
_PROMPT_RE = re.compile(r"prompt eval time\s*=\s*([0-9.]+)\s*ms\s*/\s*(\d+) tokens")
_EVAL_RE = re.compile(
    r"(?<!prompt )eval time\s*=\s*([0-9.]+)\s*ms\s*/\s*(\d+) (?:tokens|runs)"
    r"\s*\([^\n]*?([0-9.]+) tokens per second\s*\)"
)


def _last_match(pattern: re.Pattern[str], text: str) -> re.Match[str] | None:
    matches = list(pattern.finditer(text))
    return matches[-1] if matches else None


class LlamaCppLocalAdapter(BaseAdapter):
    """Invoke a local llama.cpp CLI directly, without bindings or network fallback."""

    def __init__(self, *, environ: dict[str, str] | None = None, runner: Runner | None = None) -> None:
        self._environ = dict(os.environ if environ is None else environ)
        self._runner = runner or subprocess.run

    def _configuration(self) -> tuple[Path, Path, float]:
        binary_raw = self._environ.get("KORA_LLAMA_CPP_BIN", "").strip()
        model_raw = self._environ.get("KORA_LLAMA_CPP_MODEL", "").strip()
        if not binary_raw or not model_raw:
            raise LlamaCppLocalRuntimeError(
                "llama_cpp_local requires KORA_LLAMA_CPP_BIN and KORA_LLAMA_CPP_MODEL; "
                "no download or provider fallback was attempted"
            )
        binary = Path(binary_raw).expanduser()
        model = Path(model_raw).expanduser()
        if not binary.is_file() or not os.access(binary, os.X_OK):
            raise LlamaCppLocalRuntimeError(
                "KORA_LLAMA_CPP_BIN is not an executable file; no provider fallback was attempted"
            )
        if not model.is_file():
            raise LlamaCppLocalRuntimeError(
                "KORA_LLAMA_CPP_MODEL is not an existing file; no download or provider fallback was attempted"
            )
        try:
            timeout_s = float(self._environ.get("KORA_LLAMA_CPP_TIMEOUT_S", "180"))
        except ValueError as exc:
            raise LlamaCppLocalRuntimeError("KORA_LLAMA_CPP_TIMEOUT_S must be numeric") from exc
        if timeout_s <= 0:
            raise LlamaCppLocalRuntimeError("KORA_LLAMA_CPP_TIMEOUT_S must be positive")
        return binary.absolute(), model.resolve(), timeout_s

    def run(
        self,
        *,
        task_id: str,
        input: dict[str, Any],
        budget: dict[str, Any],
        output_schema: dict[str, Any],
    ) -> dict[str, Any]:
        del output_schema
        binary, model, timeout_s = self._configuration()
        question = input.get("question")
        if not isinstance(question, str) or not question.strip():
            raise LlamaCppLocalRuntimeError("llama_cpp_local input.question must be a non-empty string")
        requested_tokens = budget.get("max_tokens", 64)
        if isinstance(requested_tokens, bool) or not isinstance(requested_tokens, int):
            requested_tokens = 64
        max_tokens = max(1, min(requested_tokens, 128))
        command = [
            str(binary), "--model", str(model), "--prompt", question,
            "--predict", str(max_tokens), "--temperature", "0", "--seed", "0",
            "--gpu-layers", "99", "--no-conversation", "--no-display-prompt",
            "--ignore-eos", "--simple-io", "--perf", "--log-colors", "off",
        ]
        worker_env = dict(self._environ)
        worker_env.update({"NO_PROXY": "*", "no_proxy": "*"})
        try:
            completed = self._runner(
                command,
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout_s,
                env=worker_env,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise LlamaCppLocalRuntimeError(
                f"local llama.cpp subprocess failed: {type(exc).__name__}; "
                "no provider fallback was attempted"
            ) from exc
        if completed.returncode != 0:
            detail = completed.stderr.strip().splitlines()[-1] if completed.stderr.strip() else "unknown error"
            raise LlamaCppLocalRuntimeError(
                f"local llama.cpp exited {completed.returncode}: {detail}; "
                "no provider fallback was attempted"
            )
        answer = completed.stdout.strip()
        if not answer:
            raise LlamaCppLocalRuntimeError(
                "local llama.cpp returned an empty answer; no provider fallback was attempted"
            )
        load = _last_match(_LOAD_RE, completed.stderr)
        prompt = _last_match(_PROMPT_RE, completed.stderr)
        generated = _last_match(_EVAL_RE, completed.stderr)
        if load is None or prompt is None or generated is None:
            raise LlamaCppLocalRuntimeError(
                "local llama.cpp did not return the required performance timings; "
                "no provider fallback was attempted"
            )
        load_ms = float(load.group(1))
        prompt_ms, tokens_in = float(prompt.group(1)), int(prompt.group(2))
        eval_ms, tokens_out, tokens_per_second = (
            float(generated.group(1)), int(generated.group(2)), float(generated.group(3))
        )
        return {
            "ok": True,
            "output": {"status": "ok", "task_id": task_id, "answer": answer},
            "usage": {
                "time_ms": int(round(load_ms + prompt_ms + eval_ms)),
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
            },
            "meta": {
                "adapter": "llama_cpp_local",
                "runtime": "llama.cpp",
                "model": model.name,
                "model_path_label": str(model),
                "model_calls": 1,
                "network": "none",
                "provider": "local",
                "remote_provider_calls": 0,
                "runtime_reported_load_time_ms": load_ms,
                "runtime_reported_generation_tokens_per_second": tokens_per_second,
            },
        }


__all__ = ["LlamaCppLocalAdapter", "LlamaCppLocalRuntimeError"]
