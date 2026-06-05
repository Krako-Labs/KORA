use crate::scheduler::topo_sort;
use crate::task_ir::{Task, TaskGraph, RunSpec, VerifyRule, Budget};
use crate::security::pii_redact::redact_json_value;
use crate::security::telemetry::SiemEvent;
use std::collections::HashMap;
use std::time::{Duration, Instant};
use serde_json::{json, Value};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ExecutorError {
    #[error("Task '{0}' timed out (max_time_ms = {1} exceeded)")]
    Timeout(String, u64),
    #[error("Verification failed for task '{0}': {1}")]
    VerificationFailed(String, String),
    #[error("Deterministic handler '{0}' failed: {1}")]
    HandlerFailed(String, String),
    #[error("LLM adapter failed: {0}")]
    LlmFailed(String),
    #[error("Execution failed: {0}")]
    ExecutionFailed(String),
}

/// Execute a task graph and return the final state and outputs map
pub async fn run_graph(graph: &TaskGraph) -> Result<HashMap<String, Value>, ExecutorError> {
    let normalized = crate::task_ir::normalize_graph(graph);
    
    // Sort tasks topologically
    let order = topo_sort(&normalized).map_err(|e| ExecutorError::ExecutionFailed(e.to_string()))?;
    
    let mut outputs: HashMap<String, Value> = HashMap::new();
    let task_map: HashMap<&str, &Task> = normalized.tasks.iter().map(|t| (t.id.as_str(), t)).collect();

    for task_id in order {
        let task = task_map.get(task_id.as_str()).unwrap();
        
        let start_time = Instant::now();
        
        // Log start SIEM event
        SiemEvent::new(&normalized.graph_id, &task.id, "task_start", "ok", 0, 0, 0, 0.0, "Starting task execution").emit();

        let budget = task.policy.budget.as_ref().cloned().unwrap_or_default();
        let max_time_ms = budget.max_time_ms;

        // Wrap execution in timeout
        let result = tokio::time::timeout(
            Duration::from_millis(max_time_ms),
            execute_single_task(task, &outputs, &budget)
        ).await;

        let duration_ms = start_time.elapsed().as_millis() as u64;

        match result {
            Ok(Ok((output, tokens_in, tokens_out))) => {
                // Verify output
                if let Err(e) = verify_task_output(task, &output) {
                    SiemEvent::new(
                        &normalized.graph_id,
                        &task.id,
                        "task_fail",
                        "error",
                        duration_ms,
                        tokens_in,
                        tokens_out,
                        0.0,
                        &format!("Output verification failed: {}", e)
                    ).emit();
                    return Err(ExecutorError::VerificationFailed(task.id.clone(), e.to_string()));
                }

                // Log success SIEM event
                SiemEvent::new(
                    &normalized.graph_id,
                    &task.id,
                    "task_success",
                    "ok",
                    duration_ms,
                    tokens_in,
                    tokens_out,
                    0.0,
                    "Task executed successfully"
                ).emit();

                outputs.insert(task.id.clone(), output);
            }
            Ok(Err(e)) => {
                // Log failure SIEM event
                SiemEvent::new(
                    &normalized.graph_id,
                    &task.id,
                    "task_fail",
                    "error",
                    duration_ms,
                    0,
                    0,
                    0.0,
                    &format!("Task execution failed: {}", e)
                ).emit();
                return Err(e);
            }
            Err(_) => {
                // Timeout breached
                SiemEvent::new(
                    &normalized.graph_id,
                    &task.id,
                    "budget_breach",
                    "error",
                    duration_ms,
                    0,
                    0,
                    0.0,
                    &format!("Time budget of {}ms exceeded", max_time_ms)
                ).emit();
                return Err(ExecutorError::Timeout(task.id.clone(), max_time_ms));
            }
        }
    }

    Ok(outputs)
}

/// Run a single task based on its spec
async fn execute_single_task(
    task: &Task,
    outputs: &HashMap<String, Value>,
    budget: &Budget,
) -> Result<(Value, u64, u64), ExecutorError> {
    match &task.run {
        RunSpec::Det(det_spec) => {
            if det_spec.handler == "sleep" {
                let ms = task.input.get("ms")
                    .or_else(|| det_spec.args.get("ms"))
                    .and_then(|v| v.as_u64())
                    .unwrap_or(100);
                tokio::time::sleep(Duration::from_millis(ms)).await;
                return Ok((json!({"status": "ok", "task_id": task.id}), 0, 0));
            }
            let output = run_deterministic_handler(task, det_spec)?;
            Ok((output, 0, 0))
        }
        RunSpec::Llm(llm_spec) => {
            // Check skip_if logic
            if should_skip_task(task, outputs) {
                let skipped_output = json!({
                    "status": "ok",
                    "task_id": task.id,
                    "skipped": true,
                    "message": "Skipped due to skip_if condition"
                });
                return Ok((skipped_output, 0, 0));
            }

            // High-End Security Feature: PII Redaction
            // Mask any PII in inputs before forwarding to the LLM Adapter
            let mut redacted_input = llm_spec.input.clone();
            let count_before = serde_json::to_string(&redacted_input).unwrap_or_default();
            
            redact_json_value(&mut redacted_input);
            
            let count_after = serde_json::to_string(&redacted_input).unwrap_or_default();
            if count_before != count_after {
                SiemEvent::new(
                    "unknown",
                    &task.id,
                    "pii_redaction",
                    "ok",
                    0,
                    0,
                    0,
                    0.0,
                    "Sensitive PII/PCI pattern matched and redacted before adapter call"
                ).emit();
            }

            // Run Mock LLM Adapter
            let (output, tokens_in, tokens_out) = run_mock_adapter(&task.id, &redacted_input, budget).await;
            Ok((output, tokens_in, tokens_out))
        }
    }
}

/// Deterministic Handlers registered in KORA
fn run_deterministic_handler(task: &Task, spec: &crate::task_ir::RunDetSpec) -> Result<Value, ExecutorError> {
    match spec.handler.as_str() {
        "echo" => {
            let message = task.input.get("message")
                .or_else(|| spec.args.get("message"))
                .and_then(|v| v.as_str())
                .unwrap_or("hello from kora");

            Ok(json!({
                "status": "ok",
                "task_id": task.id,
                "message": message
            }))
        }
        "classify_simple" => {
            let text = task.input.get("text")
                .or_else(|| spec.args.get("text"))
                .and_then(|v| v.as_str())
                .unwrap_or("");

            Ok(json!({
                "status": "ok",
                "task_id": task.id,
                "is_simple": text.len() < 80
            }))
        }
        unknown => Err(ExecutorError::HandlerFailed(
            task.id.clone(),
            format!("Unknown deterministic handler: {}", unknown)
        )),
    }
}

/// Checks the task graph skip_if logic matching Python behavior
fn should_skip_task(task: &Task, outputs: &HashMap<String, Value>) -> bool {
    if let RunSpec::Llm(llm_spec) = &task.run {
        if let Some(skip_if) = llm_spec.input.get("skip_if") {
            if let (Some(path), Some(equals)) = (skip_if.get("path"), skip_if.get("equals")) {
                let path_str = path.as_str().unwrap_or("");
                let key = if path_str.starts_with("$.") { &path_str[2..] } else { path_str };
                
                for dep in &task.deps {
                    if let Some(dep_output) = outputs.get(dep) {
                        if let Some(val) = dep_output.get(key) {
                            if val == equals {
                                return true;
                            }
                        }
                    }
                }
            }
        }
    }
    false
}

/// Simulated OpenAI/Mock LLM Adapter
async fn run_mock_adapter(task_id: &str, input: &Value, _budget: &Budget) -> (Value, u64, u64) {
    // Simulated adapter network delay (25ms)
    tokio::time::sleep(Duration::from_millis(25)).await;

    let question = input.get("question").and_then(|v| v.as_str()).unwrap_or("");
    let tokens_in = (question.len() / 4).max(1) as u64;
    let tokens_out = 40;

    let output = json!({
        "status": "ok",
        "task_id": task_id,
        "answer": format!("Mock answer for: {}", if question.len() > 80 { &question[..80] } else { question })
    });

    (output, tokens_in, tokens_out)
}

/// Custom JSON Schema & Verification Rule engine
fn verify_task_output(task: &Task, output: &Value) -> Result<(), String> {
    let verify = match &task.verify {
        Some(v) => v,
        None => return Ok(()),
    };

    // 1. Check schema (lightweight required field verification)
    if let Some(schema) = &verify.schema {
        if let Some(required) = schema.get("required").and_then(|v| v.as_array()) {
            for req_field in required {
                if let Some(field_name) = req_field.as_str() {
                    if output.get(field_name).is_none() {
                        return Err(format!("Schema validation failed: missing required property '{}'", field_name));
                    }
                }
            }
        }
    }

    // 2. Evaluate custom verification rules
    for rule in &verify.rules {
        match rule {
            VerifyRule::Required { paths } => {
                for path in paths {
                    if output.get(path).is_none() {
                        return Err(format!("Rule 'required' failed: path '{}' not found", path));
                    }
                }
            }
            VerifyRule::Range { path, min, max } => {
                if let Some(val) = output.get(path).and_then(|v| v.as_f64()) {
                    if val < *min || val > *max {
                        return Err(format!("Rule 'range' failed: {} = {} is outside [{}, {}]", path, val, min, max));
                    }
                } else if output.get(path).is_some() {
                    return Err(format!("Rule 'range' failed: path '{}' is not numeric", path));
                }
            }
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::task_ir::{TaskGraph, GraphDefaults, Task, RunSpec, RunDetSpec, Policy};

    #[tokio::test]
    async fn test_run_simple_graph() {
        let graph = TaskGraph {
            graph_id: "test-graph".to_string(),
            version: "0.1".to_string(),
            root: "task1".to_string(),
            defaults: GraphDefaults {
                budget: Budget {
                    max_time_ms: 1000,
                    max_tokens: 300,
                    max_retries: 1,
                },
            },
            tasks: vec![
                Task {
                    id: "task1".to_string(),
                    task_type: "io.echo".to_string(),
                    deps: vec![],
                    input: json!({"message": "test hello"}),
                    run: RunSpec::Det(RunDetSpec {
                        handler: "echo".to_string(),
                        args: Value::Null,
                    }),
                    verify: None,
                    policy: Policy::default(),
                    tags: vec![],
                }
            ],
        };

        let outputs = run_graph(&graph).await.unwrap();
        assert_eq!(outputs.get("task1").unwrap()["message"], "test hello");
    }

    #[tokio::test]
    async fn test_budget_timeout_breached() {
        let graph = TaskGraph {
            graph_id: "timeout-graph".to_string(),
            version: "0.1".to_string(),
            root: "task1".to_string(),
            defaults: GraphDefaults {
                budget: Budget {
                    max_time_ms: 50, // 50ms budget
                    max_tokens: 100,
                    max_retries: 0,
                },
            },
            tasks: vec![
                Task {
                    id: "task1".to_string(),
                    task_type: "det.sleep".to_string(),
                    deps: vec![],
                    input: json!({"ms": 200}), // task sleeps for 200ms
                    run: RunSpec::Det(RunDetSpec {
                        handler: "sleep".to_string(),
                        args: Value::Null,
                    }),
                    verify: None,
                    policy: Policy::default(),
                    tags: vec![],
                }
            ],
        };

        let result = run_graph(&graph).await;
        assert!(result.is_err());
        match result.unwrap_err() {
            ExecutorError::Timeout(task_id, time) => {
                assert_eq!(task_id, "task1");
                assert_eq!(time, 50);
            }
            other => panic!("Expected Timeout error, got {:?}", other),
        }
    }
}
