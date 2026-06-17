# KORA Rust Acceleration & Experimental Security Gateway: Methodology & Local Benchmarks

This document outlines the testing methodology, latency analysis, memory footprint measurements, and security features of the KORA Rust Acceleration and Security Engine (`kora_rust`).

> [!NOTE]
> **Disclaimer & Scope Limitations:**
> * All benchmarks and speedups reported below represent **local experimental results** executed under specific hardware and environment conditions. They are not validated under production workloads or automated CI environments.
> * The Rust Security Gateway is an **experimental developer feature** under active research. It is local-only and must not be relied upon as a production-grade security boundary, compliance firewall, or sanitization control.
> * Telemetry features output JSON logs to `stdout` for local audit simulation and development debugging purposes only.

---

## 1. Benchmarking Methodology

To ensure engineering integrity and avoid common benchmarking mistakes (such as memory accumulation and JVM/interpreter caching biases), we implemented a **subprocess-sandboxed benchmarking harness** in [benchmark.py](./benchmark.py).

* **Isolation**: Each benchmark configuration (Python vs. Rust, validation vs. execution, and size) runs in a dedicated Python subprocess. This guarantees that garbage collection and memory leak accumulation do not contaminate subsequent trials.
* **Latency Measurement**: Timed using Python's high-resolution performance counter `time.perf_counter()`.
* **Memory Tracking**: Measured by tracking the subprocess's **Peak Resident Set Size (RSS)** via the `psutil` library, polling the subprocess memory usage every 2 milliseconds.
* **Warm-up**: We execute a 5-task warm-up pass before starting timers to ensure libraries, thread pools, and regex compilation statics are fully cached.

---

## 2. Benchmark Results

*The following measurements are local-only experimental results and may vary significantly depending on hardware, memory pressure, and interpreter version.*

### Latency (Average in Milliseconds)
| Graph Size | Python Val | Rust Val | Speedup | Python Norm | Rust Norm | Speedup | Python Exec | Rust Exec | Speedup |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **10 tasks** | 1.470 ms | 0.081 ms | **18.2x** | 0.907 ms | 0.353 ms | **2.6x** | 16.028 ms | 25.428 ms | **0.6x** |
| **100 tasks** | 2.015 ms | 0.789 ms | **2.6x** | 7.290 ms | 1.356 ms | **5.4x** | 124.496 ms | 2.008 ms | **62.0x** |
| **1000 tasks** | 17.887 ms | 7.404 ms | **2.4x** | 106.019 ms | 15.918 ms | **6.7x** | 1303.829 ms | 19.643 ms | **66.4x** |
| **10000 tasks** | 382.043 ms | 90.660 ms | **4.2x** | 1437.442 ms | 178.298 ms | **8.1x** | 20461.730 ms | 251.176 ms | **81.5x** |

### Memory Footprint (Peak RSS in Megabytes)
| Graph Size | Python Val RSS | Rust Val RSS | Memory Savings | Python Exec RSS | Rust Exec RSS | Memory Savings |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **10 tasks** | 35.94 MB | 35.46 MB | **0.48 MB** | 36.18 MB | 35.84 MB | **0.35 MB** |
| **100 tasks** | 36.83 MB | 36.44 MB | **0.39 MB** | 37.61 MB | 37.18 MB | **0.43 MB** |
| **1000 tasks** | 48.82 MB | 45.59 MB | **3.23 MB** | 54.17 MB | 52.18 MB | **1.99 MB** |
| **10000 tasks** | 156.25 MB | 132.80 MB | **23.45 MB** | 204.79 MB | 197.11 MB | **7.68 MB** |

---

## 3. Engineering Analysis

### Latency Trade-offs & FFI Boundary
* **Small Graphs (10 tasks)**: Rust execution exhibits a slight latency overhead (25.4ms vs 16.0ms). This is due to the **Tokio runtime initialization overhead** (~10-15ms) when launching a new async Tokio runtime in a fresh process. In a long-running production server, this overhead is paid exactly once upon startup, making it irrelevant.
* **Large Graphs (100 - 10000 tasks)**: Rust scheduler loop execution is **55x to 81x faster** than Python. At 10,000 tasks, Python's runtime loop takes **20.4 seconds** just to schedule and dispatch no-op tasks, whereas Rust completes the entire orchestration in **251 milliseconds**.
* **Impact of Network Calls**: In real-world AI applications where LLM calls dominate (300ms - 3000ms per request), scheduler orchestration overhead matters less. However, Rust's sub-millisecond execution loop is crucial for:
  1. High-frequency edge orchestrators.
  2. Complex multi-agent pipelines with thousands of deterministic decision/branching nodes.
  3. Running massive parallel tasks where scheduling locks in Python would bottleneck throughput.

### Memory & Scale Efficiency
* Pydantic task representation in Python balloons memory footprint as graph size scales. At 10,000 tasks, validating the graph in Python takes **156 MB**, whereas Rust's `serde` parser and cycle-validator take **132 MB** (saving **23.45 MB**).
* Rust's memory savings represent a tighter data density, which prevents heap fragmentation and cache misses on server-class hardware.

---

## 4. Custom Differential Fuzzer

To satisfy standard open-source verification expectations (ensuring 0 panics, crashes, or hangs), we wrote a custom **Differential Fuzzer** in [tests/differential_fuzz.rs](./kora-rust/tests/differential_fuzz.rs).
* **Generation**: Creates 10,000 random/mutated task graphs including cyclic dependencies, missing task fields, duplicate task IDs, random JSON structures, and arbitrary strings.
* **Robustness**: Running `cargo test --test differential_fuzz` feeds these random payloads to the Rust validator and asserts that the code handles all errors gracefully through the Rust `Result` type, achieving **0 panics, 0 crashes, and 0 hangs**.

---

## 5. Experimental Security Gateway Features (Local-Only)

While the scheduler performance gains are local-only optimizations, an experimental feature currently under exploration is KORA's optional Rust Security Gateway:
* **Secrets Redaction**: Recursive JSON-payload scanner that redacts critical secrets before they are forwarded to adapters or LLMs:
  - **OpenAI API Keys** (`sk-[a-zA-Z0-9_-]{32,}`) -> `[REDACTED_OPENAI_KEY]`
  - **AWS Access Key IDs** (`AKIA[0-9A-Z]{16}`) -> `[REDACTED_AWS_KEY]`
  - **GitHub Personal Access Tokens** (`ghp_[a-zA-Z0-9]{36,255}`) -> `[REDACTED_GITHUB_TOKEN]`
  - **JSON Web Tokens (JWTs)** (`eyJ...`) -> `[REDACTED_JWT]`
  - **Generic Bearer Tokens** (`Bearer ...`) -> `[REDACTED_BEARER_TOKEN]`
  - **Credit Cards (Luhn Hardened)** -> Checks digit sequences using Luhn checks to avoid redacting arbitrary numbers, replacing valid card sequences with `[REDACTED_CARD]`.
* **Telemetry**: Emit structured JSON logs directly to standard output to simulate audit trails (ready for local validation before ingestion in tools like Splunk, Datadog, or Elastic).
