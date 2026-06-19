use kora_rust::task_ir::{TaskGraph, Task, RunSpec, RunDetSpec, GraphDefaults, Budget, VerifySpec, VerifyRule, Policy};
use kora_rust::executor::{run_graph, run_graph_contract};
use serde_json::json;

fn make_test_graph(tasks: Vec<Task>) -> TaskGraph {
    TaskGraph {
        graph_id: "test-graph".to_string(),
        version: "0.1".to_string(),
        root: tasks.last().unwrap().id.clone(),
        defaults: GraphDefaults {
            budget: Budget {
                max_time_ms: 2000,
                max_tokens: 300,
                max_retries: 0,
            },
        },
        tasks,
    }
}

fn save_test_output(name: &str, data: &serde_json::Value) {
    let dir = std::path::Path::new("tests/outputs");
    if !dir.exists() {
        std::fs::create_dir_all(dir).unwrap();
    }
    let filepath = dir.join(format!("{}.json", name));
    std::fs::write(&filepath, serde_json::to_string_pretty(data).unwrap()).unwrap();
}

#[tokio::test]
async fn test_deterministic_echo_and_classify_success() {
    let tasks = vec![
        Task {
            id: "t1".to_string(),
            task_type: "det.echo".to_string(),
            deps: vec![],
            input: json!({}),
            run: RunSpec::Det(RunDetSpec {
                handler: "echo".to_string(),
                args: json!({"message": "test msg"}),
            }),
            verify: None,
            policy: Policy::default(),
            tags: vec![],
        },
        Task {
            id: "t2".to_string(),
            task_type: "det.classify_simple".to_string(),
            deps: vec![],
            input: json!({}),
            run: RunSpec::Det(RunDetSpec {
                handler: "classify_simple".to_string(),
                args: json!({"text": "A very short string"}),
            }),
            verify: None,
            policy: Policy::default(),
            tags: vec![],
        },
    ];

    let graph = make_test_graph(tasks);
    let outputs = run_graph(&graph).await.unwrap();

    save_test_output("deterministic_echo_and_classify_success", &serde_json::to_value(&outputs).unwrap());

    assert_eq!(outputs.get("t1").unwrap()["message"], "test msg");
    assert_eq!(outputs.get("t2").unwrap()["is_simple"], true);
}

#[tokio::test]
async fn test_verification_rule_failure() {
    let tasks = vec![
        Task {
            id: "t1".to_string(),
            task_type: "det.echo".to_string(),
            deps: vec![],
            input: json!({}),
            run: RunSpec::Det(RunDetSpec {
                handler: "echo".to_string(),
                args: json!({"message": "test msg"}),
            }),
            verify: Some(VerifySpec {
                schema: None,
                rules: vec![VerifyRule::Required {
                    paths: vec!["non_existent_key".to_string()],
                }],
            }),
            policy: Policy::default(),
            tags: vec![],
        },
    ];

    let graph = make_test_graph(tasks);
    let result = run_graph(&graph).await;
    assert!(result.is_err());
    
    // Test the contract format directly
    let contract = run_graph_contract(&graph).await;
    
    save_test_output("verification_rule_failure", &contract);

    assert_eq!(contract["ok"], false);
    assert_eq!(contract["error"]["error_type"], "OUTPUT_SCHEMA_INVALID");
    assert_eq!(contract["error"]["stage"], "VERIFY");
    assert_eq!(contract["error"]["task_id"], "t1");
}

#[tokio::test]
async fn test_budget_timeout_breach() {
    let tasks = vec![
        Task {
            id: "t1".to_string(),
            task_type: "det.sleep".to_string(),
            deps: vec![],
            input: json!({"ms": 150}),
            run: RunSpec::Det(RunDetSpec {
                handler: "sleep".to_string(),
                args: json!({}),
            }),
            verify: None,
            policy: Policy::default(),
            tags: vec![],
        },
    ];

    let mut graph = make_test_graph(tasks);
    // Overwrite budget to be very short (50ms)
    graph.defaults.budget.max_time_ms = 50;
    
    let result = run_graph(&graph).await;
    assert!(result.is_err());

    let contract = run_graph_contract(&graph).await;

    save_test_output("budget_timeout_breach", &contract);

    assert_eq!(contract["ok"], false);
    assert_eq!(contract["error"]["error_type"], "BUDGET_BREACH");
    assert_eq!(contract["error"]["stage"], "BUDGET");
    assert_eq!(contract["error"]["task_id"], "t1");
}

#[tokio::test]
async fn test_invalid_handler_failure() {
    let tasks = vec![
        Task {
            id: "t1".to_string(),
            task_type: "det.unknown".to_string(),
            deps: vec![],
            input: json!({}),
            run: RunSpec::Det(RunDetSpec {
                handler: "some_unregistered_handler".to_string(),
                args: json!({}),
            }),
            verify: None,
            policy: Policy::default(),
            tags: vec![],
        },
    ];

    let graph = make_test_graph(tasks);
    let result = run_graph(&graph).await;
    assert!(result.is_err());

    let contract = run_graph_contract(&graph).await;

    save_test_output("invalid_handler_failure", &contract);

    assert_eq!(contract["ok"], false);
    assert_eq!(contract["error"]["error_type"], "DETERMINISTIC_EXEC_FAILED");
    assert_eq!(contract["error"]["stage"], "DETERMINISTIC");
}

#[tokio::test]
async fn test_run_graph_contract_success_fields() {
    let tasks = vec![
        Task {
            id: "t1".to_string(),
            task_type: "det.echo".to_string(),
            deps: vec![],
            input: json!({}),
            run: RunSpec::Det(RunDetSpec {
                handler: "echo".to_string(),
                args: json!({"message": "contract test"}),
            }),
            verify: None,
            policy: Policy::default(),
            tags: vec![],
        },
    ];

    let graph = make_test_graph(tasks);
    let contract = run_graph_contract(&graph).await;

    save_test_output("run_graph_contract_success_fields", &contract);

    assert_eq!(contract["ok"], true);
    assert_eq!(contract["graph_id"], "test-graph");
    assert_eq!(contract["order"], json!(["t1"]));
    assert_eq!(contract["outputs"]["t1"]["message"], "contract test");
    assert_eq!(contract["final"]["message"], "contract test");
    assert!(contract["error"].is_null());
    assert!(contract["stage_timings"]["overall_total_s"].is_number());
    assert!(contract["stage_timings"]["det_total_s"].is_number());
    
    // Check events list
    let events = contract["events"].as_array().unwrap();
    assert_eq!(events.len(), 1);
    assert_eq!(events[0]["task_id"], "t1");
    assert_eq!(events[0]["status"], "ok");
    assert_eq!(events[0]["stage"], "DETERMINISTIC");
}
