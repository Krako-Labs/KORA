use crate::scheduler::topo_sort;
use crate::task_ir::{Task, TaskGraph, RunSpec, VerifyRule, Budget, OnFailPolicy};
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
    let result = run_graph_contract(graph).await;
    if result["ok"].as_bool().unwrap_or(false) {
        let outputs: HashMap<String, Value> = serde_json::from_value(result["outputs"].clone()).unwrap_or_default();
        Ok(outputs)
    } else {
        let err_obj = &result["error"];
        let details = err_obj["details"].as_str().unwrap_or("").to_string();
        let task_id = err_obj["task_id"].as_str().unwrap_or("").to_string();
        let error_type = err_obj["error_type"].as_str().unwrap_or("");
        
        if error_type == "BUDGET_BREACH" {
            let max_time_ms = graph.defaults.budget.max_time_ms;
            Err(ExecutorError::Timeout(task_id, max_time_ms))
        } else if error_type == "OUTPUT_SCHEMA_INVALID" {
            Err(ExecutorError::VerificationFailed(task_id, details))
        } else if error_type == "DETERMINISTIC_EXEC_FAILED" {
            Err(ExecutorError::HandlerFailed(task_id, details))
        } else {
            Err(ExecutorError::ExecutionFailed(details))
        }
    }
}

/// Execute a task graph, returning the full Python execution result contract
pub async fn run_graph_contract(graph: &TaskGraph) -> serde_json::Value {
    let start_overall = Instant::now();
    let normalized = crate::task_ir::normalize_graph(graph);
    
    let mut outputs = HashMap::new();
    let mut events = Vec::new();
    let mut stage_timings = HashMap::new();
    
    // Sort tasks topologically
    let order_result = topo_sort(&normalized);
    let order = match order_result {
        Ok(o) => o,
        Err(e) => {
            let elapsed = start_overall.elapsed().as_secs_f64();
            stage_timings.insert("overall_total_s".to_string(), elapsed);
            return json!({
                "ok": false,
                "graph_id": normalized.graph_id,
                "order": Vec::<String>::new(),
                "error": {
                    "error_type": "DAG_INVALID",
                    "stage": "SCHEDULER",
                    "retryable": false,
                    "budget_breached": false,
                    "details": e.to_string(),
                    "task_id": Value::Null,
                },
                "events": events,
                "outputs": outputs,
                "final": Value::Null,
                "stage_timings": stage_timings,
            });
        }
    };
    
    let task_map: HashMap<&str, &Task> = normalized.tasks.iter().map(|t| (t.id.as_str(), t)).collect();
    
    let mut overall_success = true;
    let mut final_error = None;
    
    let mut det_total_s = 0.0;
    let mut llm_total_s = 0.0;
    let mut verify_total_s = 0.0;
    
    for task_id in &order {
        let task = match task_map.get(task_id.as_str()) {
            Some(t) => t,
            None => {
                overall_success = false;
                final_error = Some(json!({
                    "error_type": "INVALID_TASK",
                    "stage": "IR",
                    "retryable": false,
                    "budget_breached": false,
                    "details": format!("Task '{}' not found in task map", task_id),
                    "task_id": task_id,
                }));
                break;
            }
        };
        
        let budget = task.policy.budget.as_ref().cloned().unwrap_or_default();
        let max_retries = budget.max_retries;
        let max_attempts = 1 + max_retries;
        let mut attempt = 0;
        let mut task_success = false;
        
        while attempt < max_attempts {
            attempt += 1;
            let start_attempt = Instant::now();
            
            let run_kind = match &task.run {
                RunSpec::Det(_) => "det",
                RunSpec::Llm(_) => "llm",
            };
            
            // Log start SIEM event
            SiemEvent::new(&normalized.graph_id, &task.id, "task_start", "ok", 0, 0, 0, 0.0, "Starting task execution").emit();

            let max_time_ms = budget.max_time_ms;
            
            let result = tokio::time::timeout(
                Duration::from_millis(max_time_ms),
                execute_single_task(task, &outputs, &budget)
            ).await;
            
            let duration_ms = start_attempt.elapsed().as_millis() as u64;
            let duration_s = start_attempt.elapsed().as_secs_f64();
            if run_kind == "det" {
                det_total_s += duration_s;
            } else if run_kind == "llm" {
                llm_total_s += duration_s;
            }
            
            match result {
                Ok(Ok((output, tokens_in, tokens_out))) => {
                    let verify_start = Instant::now();
                    let verify_res = verify_task_output(task, &output);
                    let verify_duration_s = verify_start.elapsed().as_secs_f64();
                    verify_total_s += verify_duration_s;
                    
                    if let Err(e) = verify_res {
                        let err_detail = e.to_string();
                        let retryable = task.policy.on_fail == OnFailPolicy::Retry && attempt < max_attempts;
                        let error_obj = json!({
                            "error_type": "OUTPUT_SCHEMA_INVALID",
                            "stage": "VERIFY",
                            "retryable": retryable,
                            "budget_breached": false,
                            "details": err_detail,
                            "task_id": task.id,
                        });
                        
                        SiemEvent::new(
                            &normalized.graph_id,
                            &task.id,
                            "task_fail",
                            "error",
                            duration_ms,
                            tokens_in,
                            tokens_out,
                            0.0,
                            &format!("Output verification failed: {}", err_detail)
                        ).emit();

                        events.push(json!({
                            "task_id": task.id,
                            "attempt": attempt,
                            "status": "fail",
                            "stage": "VERIFY",
                            "time_ms": duration_ms + (verify_duration_s * 1000.0) as u64,
                            "error": error_obj,
                        }));
                        
                        if task.policy.on_fail != OnFailPolicy::Retry || attempt == max_attempts {
                            overall_success = false;
                            final_error = Some(error_obj);
                            break;
                        }
                    } else {
                        // Success!
                        let event_stage = if run_kind == "det" { "DETERMINISTIC" } else { "ADAPTER" };
                        let mut event_obj = json!({
                            "task_id": task.id,
                            "attempt": attempt,
                            "status": "ok",
                            "stage": event_stage,
                            "time_ms": duration_ms,
                        });
                        if run_kind == "llm" {
                            event_obj["usage"] = json!({
                                "tokens_in": tokens_in,
                                "tokens_out": tokens_out,
                            });
                            event_obj["meta"] = json!({
                                "cost_units": tokens_in + tokens_out,
                                "confidence": Value::Null,
                                "uncertainty": Value::Null,
                                "voi": Value::Null,
                                "escalate_recommended": false,
                                "stop_reason": "accepted_gate_verified",
                            });
                        }
                        
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

                        events.push(event_obj);
                        outputs.insert(task.id.clone(), output);
                        task_success = true;
                        break;
                    }
                }
                Ok(Err(e)) => {
                    let err_detail = e.to_string();
                    let error_type = match run_kind {
                        "det" => "DETERMINISTIC_EXEC_FAILED",
                        _ => "ADAPTER_FAILED",
                    };
                    let stage_str = match run_kind {
                        "det" => "DETERMINISTIC",
                        _ => "ADAPTER",
                    };
                    let retryable = task.policy.on_fail == OnFailPolicy::Retry && attempt < max_attempts;
                    let error_obj = json!({
                        "error_type": error_type,
                        "stage": stage_str,
                        "retryable": retryable,
                        "budget_breached": false,
                        "details": err_detail,
                        "task_id": task.id,
                    });
                    
                    SiemEvent::new(
                        &normalized.graph_id,
                        &task.id,
                        "task_fail",
                        "error",
                        duration_ms,
                        0,
                        0,
                        0.0,
                        &format!("Task execution failed: {}", err_detail)
                    ).emit();

                    events.push(json!({
                        "task_id": task.id,
                        "attempt": attempt,
                        "status": "fail",
                        "stage": stage_str,
                        "time_ms": duration_ms,
                        "error": error_obj,
                    }));
                    
                    if task.policy.on_fail != OnFailPolicy::Retry || attempt == max_attempts {
                        overall_success = false;
                        final_error = Some(error_obj);
                        break;
                    }
                }
                Err(_) => {
                    let retryable = task.policy.on_fail == OnFailPolicy::Retry && attempt < max_attempts;
                    let error_obj = json!({
                        "error_type": "BUDGET_BREACH",
                        "stage": "BUDGET",
                        "retryable": retryable,
                        "budget_breached": true,
                        "details": format!("Task '{}' timed out (max_time_ms = {} exceeded)", task.id, max_time_ms),
                        "task_id": task.id,
                    });
                    
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

                    events.push(json!({
                        "task_id": task.id,
                        "attempt": attempt,
                        "status": "fail",
                        "stage": "BUDGET",
                        "time_ms": duration_ms,
                        "error": error_obj,
                    }));
                    
                    if task.policy.on_fail != OnFailPolicy::Retry || attempt == max_attempts {
                        overall_success = false;
                        final_error = Some(error_obj);
                        break;
                    }
                }
            }
        }
        
        if !task_success {
            break;
        }
    }
    
    if det_total_s > 0.0 {
        stage_timings.insert("det_total_s".to_string(), det_total_s);
    }
    if llm_total_s > 0.0 {
        stage_timings.insert("llm_total_s".to_string(), llm_total_s);
    }
    if verify_total_s > 0.0 {
        stage_timings.insert("verify_total_s".to_string(), verify_total_s);
    }
    let overall_elapsed = start_overall.elapsed().as_secs_f64();
    stage_timings.insert("overall_total_s".to_string(), overall_elapsed);
    
    let final_val = if overall_success {
        outputs.get(&normalized.root).cloned().unwrap_or(Value::Null)
    } else {
        Value::Null
    };
    
    let mut result = json!({
        "ok": overall_success,
        "graph_id": normalized.graph_id,
        "order": order,
        "events": events,
        "outputs": outputs,
        "final": final_val,
        "stage_timings": stage_timings,
    });
    
    if let Some(err) = final_error {
        result["error"] = err;
    }
    
    result
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
