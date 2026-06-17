import sys
import os
import json
import time
import random
import subprocess
from pathlib import Path

# Add current directory to path so we can import kora and kora_rust
sys.path.append(str(Path(__file__).parent.absolute()))

if len(sys.argv) == 1:
    # Check dependencies before starting the benchmark suite
    missing_deps = []
    try:
        import psutil
    except ImportError:
        missing_deps.append("psutil (install via: pip install -e \".[dev]\")")
    try:
        import kora_rust
    except ImportError:
        missing_deps.append("kora_rust (build and install via: pip install -e \".[rust]\")")

    if missing_deps:
        print("Error: Missing required benchmark dependencies:", file=sys.stderr)
        for dep in missing_deps:
            print(f"  - {dep}", file=sys.stderr)
        print("\nNote: Building the optional Rust acceleration backend requires a Rust compiler toolchain.", file=sys.stderr)
        sys.exit(1)

# --- Subprocess runner commands ---
if len(sys.argv) > 1 and sys.argv[1] in ["run-py-val", "run-rust-val", "run-py-norm", "run-rust-norm", "run-py-exec", "run-rust-exec"]:
    cmd = sys.argv[1]
    size = int(sys.argv[2])
    
    # We must import inside the sub-process to measure import overhead + memory correctly
    from kora.task_ir import TaskGraph, validate_graph, normalize_graph
    from kora.executor import run_graph
    import kora_rust
    
    # Silence telemetry print logs during execution benchmarking
    class SilenceStdout:
        def __enter__(self):
            sys.stdout.flush()
            self.old_stdout_fd = os.dup(1)
            self.devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(self.devnull, 1)
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.flush()
            os.dup2(self.old_stdout_fd, 1)
            os.close(self.old_stdout_fd)
            os.close(self.devnull)

    # Re-use our deterministic graph generator
    def generate_synthetic_graph(num_tasks: int) -> dict:
        tasks = []
        tasks.append({
            "id": "task_0",
            "type": "io.echo",
            "deps": [],
            "in": {"message": "task_0"},
            "run": {"kind": "det", "spec": {"handler": "echo", "args": {"message": "task_0"}}},
            "verify": {
                "schema": {
                    "type": "object",
                    "required": ["status", "task_id", "message"],
                    "properties": {
                        "status": {"type": "string"},
                        "task_id": {"type": "string"},
                        "message": {"type": "string"}
                    }
                },
                "rules": [{"kind": "required", "paths": ["status", "task_id", "message"]}]
            },
            "policy": {"on_fail": "fail"},
            "tags": ["synthetic"]
        })
        random.seed(42)
        for i in range(1, num_tasks):
            deps = [f"task_{i-1}"]
            if i >= 2 and random.random() < 0.2:
                deps.append(f"task_{random.randint(0, i-2)}")
            tasks.append({
                "id": f"task_{i}",
                "type": "io.echo",
                "deps": deps,
                "in": {"message": f"task_{i}"},
                "run": {"kind": "det", "spec": {"handler": "echo", "args": {"message": f"task_{i}"}}},
                "verify": {
                    "schema": {
                        "type": "object",
                        "required": ["status", "task_id", "message"],
                        "properties": {
                            "status": {"type": "string"},
                            "task_id": {"type": "string"},
                            "message": {"type": "string"}
                        }
                    },
                    "rules": [{"kind": "required", "paths": ["status", "task_id", "message"]}]
                },
                "policy": {"on_fail": "fail"},
                "tags": ["synthetic"]
            })
        return {
            "graph_id": f"synthetic-{num_tasks}",
            "version": "0.1",
            "root": f"task_{num_tasks-1}",
            "defaults": {"budget": {"max_time_ms": 15000, "max_tokens": 300, "max_retries": 1}},
            "tasks": tasks
        }

    graph_dict = generate_synthetic_graph(size)
    json_str = json.dumps(graph_dict)
    
    # Run warmup once before timing
    with SilenceStdout():
        kora_rust.validate_graph(json.dumps(generate_synthetic_graph(2)))
        
    start_time = time.perf_counter()
    if cmd == "run-py-val":
        py_graph = TaskGraph.from_json(json_str)
        validate_graph(py_graph)
    elif cmd == "run-rust-val":
        kora_rust.validate_graph(json_str)
    elif cmd == "run-py-norm":
        py_graph = TaskGraph.from_json(json_str)
        normalize_graph(py_graph)
    elif cmd == "run-rust-norm":
        kora_rust.normalize_graph(json_str)
    elif cmd == "run-py-exec":
        py_graph = TaskGraph.from_json(json_str)
        norm_py = normalize_graph(py_graph)
        with SilenceStdout():
            run_graph(norm_py)
    elif cmd == "run-rust-exec":
        with SilenceStdout():
            kora_rust.run_graph(json_str)
            
    latency_ms = (time.perf_counter() - start_time) * 1000.0
    
    sys.stdout.flush()
    print(json.dumps({"latency_ms": latency_ms}))
    sys.exit(0)

import psutil

def run_subprocess_and_measure_peak_rss(args):
    # Launch subprocess in a clean environment
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc = psutil.Process(p.pid)
    peak_rss = 0
    while p.poll() is None:
        try:
            # RSS in bytes
            rss = proc.memory_info().rss
            if rss > peak_rss:
                peak_rss = rss
        except psutil.NoSuchProcess:
            break
        time.sleep(0.002) # poll frequently to catch peak memory
    stdout, stderr = p.communicate()
    
    # Parse the final output JSON
    latency = 0.0
    try:
        lines = stdout.decode().strip().split('\n')
        for line in lines:
            if line.strip().startswith("{") and line.strip().endswith("}"):
                data = json.loads(line)
                latency = data.get("latency_ms", 0.0)
    except Exception as e:
        print(f"Error parsing subprocess output: {stdout.decode()}. Error: {e}", file=sys.stderr)
        
    return latency, peak_rss / (1024.0 * 1024.0) # return memory in MB

def run_benchmarks():
    sizes = [10, 100, 1000, 10000]
    iterations = 5
    
    results = {}
    python_path = sys.executable

    print("KORA Rust vs Python High-Precision Latency & RSS Benchmarks")
    print("==========================================================")
    
    for size in sizes:
        print(f"\nBenchmarking graph size {size} tasks...")
        
        # 1. Validation Benchmarks
        py_val_latencies = []
        py_val_memories = []
        for _ in range(iterations):
            lat, mem = run_subprocess_and_measure_peak_rss([python_path, __file__, "run-py-val", str(size)])
            py_val_latencies.append(lat)
            py_val_memories.append(mem)
            
        rust_val_latencies = []
        rust_val_memories = []
        for _ in range(iterations):
            lat, mem = run_subprocess_and_measure_peak_rss([python_path, __file__, "run-rust-val", str(size)])
            rust_val_latencies.append(lat)
            rust_val_memories.append(mem)
            
        # 2. Normalization Benchmarks
        py_norm_latencies = []
        py_norm_memories = []
        for _ in range(iterations):
            lat, mem = run_subprocess_and_measure_peak_rss([python_path, __file__, "run-py-norm", str(size)])
            py_norm_latencies.append(lat)
            py_norm_memories.append(mem)
            
        rust_norm_latencies = []
        rust_norm_memories = []
        for _ in range(iterations):
            lat, mem = run_subprocess_and_measure_peak_rss([python_path, __file__, "run-rust-norm", str(size)])
            rust_norm_latencies.append(lat)
            rust_norm_memories.append(mem)

        # 3. Execution Benchmarks (reduce iterations for 10000 tasks on Python to stay fast)
        exec_iter = 1 if size == 10000 else (3 if size == 1000 else iterations)
        
        py_exec_latencies = []
        py_exec_memories = []
        # If size is 10000, Python execution might take a very long time (>10s). Run it once.
        for _ in range(exec_iter):
            lat, mem = run_subprocess_and_measure_peak_rss([python_path, __file__, "run-py-exec", str(size)])
            py_exec_latencies.append(lat)
            py_exec_memories.append(mem)
            
        rust_exec_latencies = []
        rust_exec_memories = []
        for _ in range(exec_iter):
            lat, mem = run_subprocess_and_measure_peak_rss([python_path, __file__, "run-rust-exec", str(size)])
            rust_exec_latencies.append(lat)
            rust_exec_memories.append(mem)
            
        results[size] = {
            "py_val_lat": sum(py_val_latencies) / len(py_val_latencies),
            "py_val_mem": max(py_val_memories),
            "rust_val_lat": sum(rust_val_latencies) / len(rust_val_latencies),
            "rust_val_mem": max(rust_val_memories),
            
            "py_norm_lat": sum(py_norm_latencies) / len(py_norm_latencies),
            "py_norm_mem": max(py_norm_memories),
            "rust_norm_lat": sum(rust_norm_latencies) / len(rust_norm_latencies),
            "rust_norm_mem": max(rust_norm_memories),
            
            "py_exec_lat": sum(py_exec_latencies) / len(py_exec_latencies),
            "py_exec_mem": max(py_exec_memories),
            "rust_exec_lat": sum(rust_exec_latencies) / len(rust_exec_latencies),
            "rust_exec_mem": max(rust_exec_memories)
        }

    print("\n### High-Precision Benchmarks: Python vs. Rust")
    print("\n#### 1. Latency (Average of runs in Milliseconds)")
    print("| Graph Size | Py Val | Rust Val | Speedup | Py Norm | Rust Norm | Speedup | Py Exec | Rust Exec | Speedup |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for size in sizes:
        res = results[size]
        val_sp = res['py_val_lat'] / res['rust_val_lat']
        norm_sp = res['py_norm_lat'] / res['rust_norm_lat']
        exec_sp = res['py_exec_lat'] / res['rust_exec_lat'] if res['rust_exec_lat'] > 0 and res['py_exec_lat'] > 0 else 0.0
        
        py_exec_str = f"{res['py_exec_lat']:.3f} ms" if res['py_exec_lat'] > 0 else "N/A"
        rust_exec_str = f"{res['rust_exec_lat']:.3f} ms"
        exec_sp_str = f"{exec_sp:.1f}x" if exec_sp > 0 else "N/A"
        
        print(f"| {size:5d} tasks | {res['py_val_lat']:8.3f} ms | {res['rust_val_lat']:9.3f} ms | {val_sp:6.1f}x | {res['py_norm_lat']:8.3f} ms | {res['rust_norm_lat']:10.3f} ms | {norm_sp:6.1f}x | {py_exec_str} | {rust_exec_str} | {exec_sp_str} |")

    print("\n#### 2. Memory Footprint (Peak RSS in Megabytes)")
    print("| Graph Size | Py Val RSS | Rust Val RSS | Memory Savings | Py Exec RSS | Rust Exec RSS | Memory Savings |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for size in sizes:
        res = results[size]
        val_mem_saved = res['py_val_mem'] - res['rust_val_mem']
        exec_mem_saved = res['py_exec_mem'] - res['rust_exec_mem'] if res['py_exec_mem'] > 0 else 0.0
        
        py_exec_rss_str = f"{res['py_exec_mem']:.2f} MB" if res['py_exec_mem'] > 0 else "N/A"
        exec_saved_str = f"{exec_mem_saved:.2f} MB" if res['py_exec_mem'] > 0 else "N/A"
        
        print(f"| {size:5d} tasks | {res['py_val_mem']:10.2f} MB | {res['rust_val_mem']:12.2f} MB | {val_mem_saved:12.2f} MB | {py_exec_rss_str} | {res['rust_exec_mem']:13.2f} MB | {exec_saved_str} |")

if __name__ == "__main__":
    run_benchmarks()
