# KRK H100 Bounded Summary v0

Status: generated bounded GPU-routed subset summary.

This summary records a bounded H100 execution of the GPU-routed subset selected from the public KRK matrix fixtures. It is not a raw GPU benchmark, production benchmark, provider benchmark, or superiority claim.

## Summary

| Field | Value |
| --- | ---: |
| Subset count | 4 |
| Total compute weight | 58 |
| Runtime seconds | 0.035312 |
| Throughput, requests/second | 113.277481 |
| Throughput, compute weight/second | 1642.523477 |
| Bounded workload peak allocation MB | 240.000 |
| CUDA context memory used before MB | 525.062 |
| CUDA context memory used after MB | 525.062 |

## Subset

| Request | Profile | Class | Selected route | Expected route | Compute weight | Runtime seconds |
| --- | --- | --- | --- | --- | ---: | ---: |
| cache-003 | cache-heavy | cache-miss-complex | GPU | GPU | 10 | 0.001931 |
| gpu-001 | GPU-heavy | large-batch-generation | GPU | GPU | 16 | 0.006089 |
| gpu-002 | GPU-heavy | multimodal-transform | GPU | GPU | 20 | 0.006761 |
| mixed-004 | mixed-realistic | large-batch-embedding-like | GPU | GPU | 12 | 0.003739 |

## Claim Level

`bounded_h100_routed_subset_measured`

Allowed statement:

> KRK-selected GPU subset items from the public matrix fixtures were executed in a bounded H100 evaluation and summarized with runtime, throughput, and memory measurements.

This does not support claims about production savings, customer savings, provider superiority, GPU superiority, broad workload superiority, or infrastructure savings.

## Public Boundary

- Raw logs are not committed.
- Infrastructure identifiers are not included.
- Server names, IPs, users, and SSH details are not included.
- Private resource details are not included.
