# KORA Target Registry v0

## Purpose

The KORA Target Registry describes execution targets that KRK can consider when routing a workload.

This is a public-safe architecture draft, not a production registry contract.

## Initial Target Types

### `local_ollama`

Local model target through an Ollama-compatible runtime.

### `local_llamacpp`

Local model target through a llama.cpp-compatible runtime.

### `openai_compatible_api`

Provider target with an OpenAI-compatible API surface.

### `h100_vllm`

GPU-backed vLLM-style target class. Public docs should describe this as a target class only. Do not expose private allocation details, server names, IP addresses, users, raw logs, or private artifacts.

### `cpu_local`

CPU-local execution target for deterministic or local runtime paths.

### `fallback`

Fallback target used when preferred routes fail, are unavailable, or violate policy.

### `future_krako_node`

Future-only target class for possible commercial execution infrastructure. Do not present this as implemented.

## Target Metadata Fields

Suggested fields:

- `target_id`.
- `target_type`.
- `display_name`.
- `capabilities`.
- `runtime`.
- `privacy_class`.
- `cost_class`.
- `latency_class`.
- `quality_notes`.
- `availability`.
- `evidence_supported`.
- `fallback_target_id`.

## Public/Private Boundary

Public target examples may include target classes, local demo settings, and sanitized metadata.

Do not publish:

- credentials.
- API keys.
- private endpoints.
- server names.
- IP addresses.
- SSH users.
- raw GPU logs.
- private resource allocation details.
- customer-specific routing metadata.

