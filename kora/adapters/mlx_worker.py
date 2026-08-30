"""JSON stdin/stdout worker for the optional local MLX-LM runtime."""

from __future__ import annotations

from contextlib import redirect_stdout
from importlib.metadata import version
import json
import sys
import time
from typing import Any


def _main() -> int:
    try:
        request = json.load(sys.stdin)
        task_id = str(request["task_id"])
        question = str(request["question"])
        model_path = str(request["model_path"])
        model_id = str(request["model_id"])
        revision = request.get("revision")
        max_tokens = max(1, min(int(request["max_tokens"]), 128))

        # MLX and mlx_lm remain strictly inside this subprocess boundary.
        with redirect_stdout(sys.stderr):
            import mlx
            import mlx_lm
            from mlx_lm import generate, load

            start = time.monotonic()
            model, tokenizer = load(model_path)
            messages: list[dict[str, Any]] = [
                {"role": "system", "content": "Answer the synthetic question concisely."},
                {"role": "user", "content": question},
            ]
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            tokens_in = len(tokenizer.encode(prompt))
            answer = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False).strip()
            tokens_out = len(tokenizer.encode(answer)) if answer else 0
            elapsed_ms = int((time.monotonic() - start) * 1000)

        response = {
            "ok": True,
            "output": {"status": "ok", "task_id": task_id, "answer": answer},
            "usage": {
                "time_ms": elapsed_ms,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
            },
            "meta": {
                "adapter": "mlx_local",
                "runtime": "mlx-lm",
                "runtime_version": version("mlx-lm"),
                "mlx_version": version("mlx"),
                "model": model_id,
                "revision": revision,
                "model_calls": 1,
                "network": "none",
                "provider": "local",
                "remote_provider_calls": 0,
            },
        }
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        return 0
    except Exception as exc:
        sys.stderr.write(f"mlx_local worker error: {type(exc).__name__}: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(_main())
