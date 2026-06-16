# [Evidence Name]

Status: `[measured / generated / prepared / not run / blocked]`.

Claim level: `[claim_level]`.

## Purpose

`[What this evidence is intended to show.]`

## Source Inputs

| Input | Location | Public-safe? |
| --- | --- | --- |
| `[input]` | `[public GitHub path / private GitHub source / local-only source]` | `[yes / no / sanitized]` |

## Method

`[Describe the reproducible method. Do not include private paths, credentials, hostnames, or raw access details.]`

## Run Status

- status: `[measured / generated / prepared / not run / blocked]`
- execution mode: `[local / dry-run / live bounded / generated / other]`
- raw outputs committed: `[true / false]`
- credentials committed: `false`

## Aggregate Results

| Metric | Value |
| --- | --- |
| `[metric]` | `[value]` |

## Reproducibility

```bash
[public-safe command]
```

If reproduction requires private or local-only context, state that the public repo contains only sanitized aggregate evidence.

## Public / Private Boundary

Committed public evidence includes:

- `[summary]`

Not committed:

- raw logs.
- credentials.
- private paths.
- hostnames.
- raw provider responses.
- account or billing details.

## Limitations

- `[limitation]`
- `[limitation]`

## Claim Boundary

Supported:

- `[supported bounded claim]`

Not supported:

- `[unsupported claim]`
