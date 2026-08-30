"""Fail-closed subprocess adapter for an explicitly configured local MLX-LM runtime."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
from typing import Any, Callable

from .base import BaseAdapter

Runner = Callable[..., subprocess.CompletedProcess[str]]


class MLXLocalRuntimeError(RuntimeError):
    """The explicitly configured local MLX runtime could not be used."""


def _cached_model_path(model: str, hf_home: Path) -> tuple[Path, str | None]:
    candidate = Path(model).expanduser()
    if candidate.is_dir():
        return candidate.resolve(), None

    repo_cache = hf_home / "hub" / f"models--{model.replace('/', '--')}"
    ref = repo_cache / "refs" / "main"
    if ref.is_file():
        revision = ref.read_text(encoding="utf-8").strip()
        snapshot = repo_cache / "snapshots" / revision
        if snapshot.is_dir():
            return snapshot.resolve(), revision
    raise MLXLocalRuntimeError(
        "KORA local MLX model is not present in the configured offline cache; "
        "no download or provider fallback was attempted"
    )


class MLXLocalAdapter(BaseAdapter):
    """Invoke MLX-LM in a separate Python process without importing MLX in KORA."""

    def __init__(self, *, environ: dict[str, str] | None = None, runner: Runner | None = None) -> None:
        self._environ = dict(os.environ if environ is None else environ)
        self._runner = runner or subprocess.run

    def _configuration(self) -> tuple[Path, Path, str, str | None, float]:
        python_raw = self._environ.get("KORA_MLX_PYTHON", "").strip()
        model = self._environ.get("KORA_MLX_MODEL", "").strip()
        hf_home_raw = self._environ.get("HF_HOME", "").strip()
        if not python_raw or not model or not hf_home_raw:
            raise MLXLocalRuntimeError(
                "mlx_local requires KORA_MLX_PYTHON, KORA_MLX_MODEL, and HF_HOME; "
                "no provider fallback was attempted"
            )
        python = Path(python_raw).expanduser()
        hf_home = Path(hf_home_raw).expanduser()
        if not python.is_file():
            raise MLXLocalRuntimeError(
                "KORA_MLX_PYTHON is not an existing file; no provider fallback was attempted"
            )
        if not hf_home.is_dir():
            raise MLXLocalRuntimeError(
                "HF_HOME is not an existing directory; no provider fallback was attempted"
            )
        model_path, revision = _cached_model_path(model, hf_home)
        try:
            timeout_s = float(self._environ.get("KORA_MLX_TIMEOUT_S", "180"))
        except ValueError as exc:
            raise MLXLocalRuntimeError("KORA_MLX_TIMEOUT_S must be numeric") from exc
        if timeout_s <= 0:
            raise MLXLocalRuntimeError("KORA_MLX_TIMEOUT_S must be positive")
        # Preserve a virtualenv symlink: resolving it would bypass that environment's
        # site-packages and invoke the base interpreter instead.
        return python.absolute(), model_path, model, revision, timeout_s

    def run(
        self,
        *,
        task_id: str,
        input: dict[str, Any],
        budget: dict[str, Any],
        output_schema: dict[str, Any],
    ) -> dict[str, Any]:
        del output_schema
        python, model_path, model_id, revision, timeout_s = self._configuration()
        question = input.get("question")
        if not isinstance(question, str) or not question.strip():
            raise MLXLocalRuntimeError("mlx_local input.question must be a non-empty string")
        requested_tokens = budget.get("max_tokens", 64)
        if isinstance(requested_tokens, bool) or not isinstance(requested_tokens, int):
            requested_tokens = 64
        max_tokens = max(1, min(requested_tokens, 128))
        request = {
            "task_id": task_id,
            "question": question,
            "max_tokens": max_tokens,
            "model_path": str(model_path),
            "model_id": model_id,
            "revision": revision,
        }
        worker_env = dict(self._environ)
        worker_env.update(
            {
                "HF_HUB_OFFLINE": "1",
                "TRANSFORMERS_OFFLINE": "1",
                "HF_DATASETS_OFFLINE": "1",
                "NO_PROXY": "*",
            }
        )
        try:
            completed = self._runner(
                [str(python), "-m", "kora.adapters.mlx_worker"],
                input=json.dumps(request),
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout_s,
                env=worker_env,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise MLXLocalRuntimeError(
                f"local MLX subprocess failed: {type(exc).__name__}; no provider fallback was attempted"
            ) from exc
        if completed.returncode != 0:
            detail = completed.stderr.strip().splitlines()[-1] if completed.stderr.strip() else "unknown error"
            raise MLXLocalRuntimeError(
                f"local MLX worker exited {completed.returncode}: {detail}; "
                "no provider fallback was attempted"
            )
        try:
            response = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise MLXLocalRuntimeError(
                "local MLX worker did not return one valid JSON object; no provider fallback was attempted"
            ) from exc
        if not isinstance(response, dict) or response.get("ok") is not True:
            raise MLXLocalRuntimeError(
                "local MLX worker returned a failure response; no provider fallback was attempted"
            )
        return response


__all__ = ["MLXLocalAdapter", "MLXLocalRuntimeError"]
