use criterion::{criterion_group, criterion_main, Criterion};
use kora_rust::task_ir::{TaskGraph, validate_graph, normalize_graph};
use kora_rust::executor::run_graph;
use serde_json::json;

fn make_sample_graph() -> TaskGraph {
    let raw = json!({
        "graph_id": "bench-graph",
        "version": "0.1",
        "root": "task1",
        "defaults": {
            "budget": {
                "max_time_ms": 1000,
                "max_tokens": 300,
                "max_retries": 1
            }
        },
        "tasks": [
            {
                "id": "task1",
                "type": "io.echo",
                "deps": [],
                "in": {"message": "hello bench"},
                "run": {"kind": "det", "spec": {"handler": "echo", "args": {}}},
                "policy": {"on_fail": "fail"},
                "tags": []
            }
        ]
    });
    serde_json::from_value(raw).unwrap()
}

fn bench_validation(c: &mut Criterion) {
    let graph = make_sample_graph();
    c.bench_function("validate_graph", |b| b.iter(|| {
        let _ = validate_graph(&graph);
    }));
}

fn bench_normalization(c: &mut Criterion) {
    let graph = make_sample_graph();
    c.bench_function("normalize_graph", |b| b.iter(|| {
        let _ = normalize_graph(&graph);
    }));
}

fn bench_execution(c: &mut Criterion) {
    let graph = make_sample_graph();
    let rt = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap();

    c.bench_function("run_graph", |b| b.iter(|| {
        let _ = rt.block_on(run_graph(&graph));
    }));
}

criterion_group!(benches, bench_validation, bench_normalization, bench_execution);
criterion_main!(benches);
