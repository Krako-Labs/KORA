use kora_rust::task_ir::{TaskGraph, validate_graph};
use serde_json::{json, Value};

struct LcgRng {
    state: u64,
}

impl LcgRng {
    fn new(seed: u64) -> Self {
        Self { state: seed }
    }

    fn next(&mut self) -> u64 {
        self.state = self.state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        self.state
    }

    fn next_range(&mut self, min: usize, max: usize) -> usize {
        let range = max - min + 1;
        min + (self.next() as usize % range)
    }

    fn next_bool(&mut self, probability: f64) -> bool {
        let val = (self.next() % 1000) as f64 / 1000.0;
        val < probability
    }
}

fn generate_fuzz_graph(rng: &mut LcgRng, mutation_type: usize) -> String {
    match mutation_type {
        0 => {
            // Completely random gibberish string
            let len = rng.next_range(5, 500);
            let mut s = String::new();
            for _ in 0..len {
                let c = rng.next_range(32, 126) as u8 as char;
                s.push(c);
            }
            s
        }
        1 => {
            // Random valid JSON but not a graph schema
            let payload = json!({
                "random_key": rng.next(),
                "another_key": rng.next_bool(0.5),
                "array": [rng.next(), rng.next(), rng.next()]
            });
            serde_json::to_string(&payload).unwrap()
        }
        _ => {
            // Semi-valid graph structure with mutated elements to trigger validation logic
            let num_tasks = rng.next_range(0, 50); // 0 tasks should fail empty tasks check
            let mut tasks = Vec::new();

            for i in 0..num_tasks {
                let id = if rng.next_bool(0.1) && i > 0 {
                    // Introduce duplicate task ID
                    format!("task_{}", i - 1)
                } else {
                    format!("task_{}", i)
                };

                let mut deps = Vec::new();
                for j in 0..i {
                    if rng.next_bool(0.3) {
                        deps.push(format!("task_{}", j));
                    }
                }
                
                // Intentionally introduce cycle or unknown dependency
                if rng.next_bool(0.05) && i > 0 {
                    // Cycle (depends on itself or future task)
                    deps.push(format!("task_{}", i));
                }
                if rng.next_bool(0.05) {
                    // Unknown dependency
                    deps.push("unknown_task_xyz".to_string());
                }

                let run_kind = if rng.next_bool(0.8) { "det" } else { "llm" };
                let run_spec = if run_kind == "det" {
                    json!({ "handler": "echo", "args": { "message": "hello" } })
                } else {
                    json!({
                        "adapter": "openai",
                        "input": { "question": "test" },
                        "output_schema": { "type": "object", "required": ["status"] }
                    })
                };

                let verify = if rng.next_bool(0.5) {
                    json!({
                        "schema": { "type": "object", "required": ["status"] },
                        "rules": []
                    })
                } else {
                    Value::Null
                };

                tasks.push(json!({
                    "id": id,
                    "type": "io.echo",
                    "deps": deps,
                    "in": {},
                    "run": { "kind": run_kind, "spec": run_spec },
                    "verify": verify,
                    "policy": { "on_fail": "fail" },
                    "tags": []
                }));
            }

            let graph_id = format!("fuzz-graph-{}", rng.next());
            let version = if rng.next_bool(0.9) { "0.1" } else { "99.9" };
            let root = if rng.next_bool(0.05) || num_tasks == 0 {
                "missing_root_task".to_string()
            } else {
                format!("task_{}", rng.next_range(0, num_tasks - 1))
            };

            let payload = json!({
                "graph_id": graph_id,
                "version": version,
                "root": root,
                "defaults": {
                    "budget": {
                        "max_time_ms": 1000,
                        "max_tokens": 300,
                        "max_retries": 1
                    }
                },
                "tasks": tasks
            });

            serde_json::to_string(&payload).unwrap()
        }
    }
}

#[test]
fn test_differential_fuzzing_robustness() {
    let mut rng = LcgRng::new(1337); // stable seed for repeatability
    let iterations = 10000;
    
    let mut parsed_ok = 0;
    let mut validation_ok = 0;
    let mut errors_caught = 0;

    for _ in 0..iterations {
        let mutation_type = rng.next_range(0, 5);
        let input_str = generate_fuzz_graph(&mut rng, mutation_type);

        // Parse and validate, asserting ZERO panics
        match serde_json::from_str::<TaskGraph>(&input_str) {
            Ok(graph) => {
                parsed_ok += 1;
                match validate_graph(&graph) {
                    Ok(_) => {
                        validation_ok += 1;
                    }
                    Err(e) => {
                        errors_caught += 1;
                        // Log sample errors for sanity check
                        if errors_caught <= 5 {
                            println!("Caught validation error (expected): {:?}", e);
                        }
                    }
                }
            }
            Err(_) => {
                // Successfully caught parse error
            }
        }
    }

    println!(
        "Fuzzing completed: {} iterations. Parsed successfully: {}/{}. Passed validation: {}/{}. Caught validation errors: {}.",
        iterations, parsed_ok, iterations, validation_ok, parsed_ok, errors_caught
    );
    
    // Assert that we processed a mix of valid/invalid inputs
    assert!(parsed_ok > 0);
}
