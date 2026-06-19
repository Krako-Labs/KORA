# provider routing H100 Environment Setup

Status: public-safe setup note for a private H100 benchmark server.

This document records the safe environment preparation pattern for the provider routing H100 track. It intentionally omits private hostnames, IP addresses, SSH aliases, credentials, GPU UUIDs, private mount details, and server-local logs. Exact baseline details belong in private server-local reports, not in this public repository.

## Scope

The setup target is a private Ubuntu 22.04 H100 server intended for future KORA GPU/API benchmark smoke tests and dry-run preparation.

Task 524 allowed:

- SSH access through local user configuration.
- Baseline inspection of OS, CPU, RAM, disk, GPU, driver, Docker, Python, Git, and editor/tool availability.
- Installation of lightweight base development packages when missing.
- Creation of server-local workspace directories.
- Creation of a lightweight Python virtual environment for smoke tests.
- Cloning the public KORA repository.
- Running KORA dry-run provider routing validation only.
- Writing private server-local reports.

Task 524 did not allow:

- storing passwords, SSH private keys, API keys, bearer tokens, or cloud credentials
- publishing private infrastructure details
- destructive disk operations
- large model downloads
- long-running training jobs
- external LLM provider API calls
- raw benchmark uploads
- GitHub releases, tags, or release assets

## Server-Local Workspace Pattern

Use a private server-local workspace outside the public repository:

```text
~/kora-ai-champion/
~/kora-ai-champion/repos/
~/kora-ai-champion/envs/
~/kora-ai-champion/logs/
~/kora-ai-champion/models/
~/kora-ai-champion/reports/
~/kora-ai-champion/tmp/
```

Recommended use:

- `repos/`: public source checkouts.
- `envs/`: Python virtual environments.
- `logs/`: private operational logs.
- `models/`: model caches or approved model assets only.
- `reports/`: private server-local setup and smoke-test reports.
- `tmp/`: transient generated outputs and dry-run summaries.

Do not commit files from `logs/`, `models/`, `reports/`, or `tmp/` to the public KORA repository.

## Lightweight Base Tools

Safe base packages for an Ubuntu 22.04 server:

```bash
sudo apt-get update
sudo apt-get install -y \
  git \
  curl \
  wget \
  build-essential \
  python3 \
  python3-venv \
  python3-pip \
  python-is-python3 \
  micro \
  tmux \
  htop \
  unzip \
  jq \
  rsync
```

If available for the distribution, `nvtop` is useful for interactive GPU monitoring:

```bash
sudo apt-get install -y nvtop
```

## Python Smoke-Test Environment

Create a lightweight environment:

```bash
python3 -m venv ~/kora-ai-champion/envs/kora-benchmark
. ~/kora-ai-champion/envs/kora-benchmark/bin/activate
python -m pip install --upgrade pip wheel setuptools requests pyyaml rich pytest
```

Validation:

```bash
python --version
pip --version
pytest --version
```

## GPU And Driver Inspection

Use inspection only until a future task approves GPU smoke workloads:

```bash
nvidia-smi
nvidia-smi -L
lspci | grep -i nvidia
cat /proc/driver/nvidia/version 2>/dev/null || true
command -v nvcc || true
nvcc --version 2>/dev/null || true
```

Do not change a working NVIDIA driver unless a future runtime requirement explicitly calls for it. Do not install the host CUDA toolkit unless local CUDA compilation is needed.

## Docker And NVIDIA Runtime

Inspect existing Docker first:

```bash
docker --version
docker info
```

If Docker requires elevated access, inspect with:

```bash
sudo docker info
```

If Docker is missing, plan the install in a separate approved task. If NVIDIA container runtime is missing, prefer documented NVIDIA container toolkit setup and avoid changing an existing Docker configuration without review.

Do not pull container images or run GPU containers unless the task explicitly approves that smoke test.

## Public KORA Clone

Clone only the public repository unless private authentication has already been approved:

```bash
git clone https://github.com/Krako-Labs/KORA.git ~/kora-ai-champion/repos/KORA
```

Keep generated outputs outside the repository:

```bash
. ~/kora-ai-champion/envs/kora-benchmark/bin/activate
python ~/kora-ai-champion/repos/KORA/experiments/provider_routing/run_dry_run.py \
  --config ~/kora-ai-champion/repos/KORA/experiments/provider_routing/config.example.yaml \
  --output ~/kora-ai-champion/tmp/provider-routing.dry_run.json
```

Expected safety flags:

- `dry_run_only: true`
- `synthetic_results_only: true`
- `real_provider_calls_enabled: false`
- `real_network_calls_attempted: false`
- `real_gpu_calls_attempted: false`

## Private Reports

Write exact server findings only to server-local private reports such as:

```text
~/kora-ai-champion/reports/h100_server_baseline_report.md
~/kora-ai-champion/reports/h100_environment_setup_report.md
~/kora-ai-champion/reports/h100_next_steps.md
```

Public docs should summarize process and guardrails, not private infrastructure details.

## Next Recommended Gates

Before real H100 benchmark work:

1. Approve Docker user/group policy.
2. Approve any container image pulls.
3. Run a minimal GPU container smoke test.
4. Choose vLLM or TGI for the first serving smoke test.
5. Approve any model download explicitly.
6. Keep serving endpoints local-only unless network exposure is reviewed.
7. Keep real provider/API credentials in private ignored configs only.
8. Keep raw benchmark outputs in private artifact storage until a release process selects evidence.

## Claim Boundary

This setup note is not benchmark evidence.

It does not claim:

- production benchmark proof
- real API-cost reduction proof
- production cost reduction proof
- broad workload superiority proof
- energy reduction evidence
- formal government validation
- real GPU/API benchmark results
