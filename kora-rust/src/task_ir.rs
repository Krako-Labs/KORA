use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ValidationError {
    #[error("Duplicate task ID: {0}")]
    DuplicateTaskId(String),
    #[error("Root task '{0}' not found in tasks list")]
    RootTaskNotFound(String),
    #[error("Task '{0}' depends on unknown task '{1}'")]
    UnknownDependency(String, String),
    #[error("LLM task '{0}' must include verify schema (directly or via normalization)")]
    LlmTaskMissingSchema(String),
    #[error("Graph contains a cycle; task graph must be a DAG")]
    CycleDetected,
    #[error("Tasks list must contain at least one task")]
    EmptyTasks,
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
pub struct Budget {
    #[serde(default = "default_max_time_ms")]
    pub max_time_ms: u64,
    #[serde(default = "default_max_tokens")]
    pub max_tokens: u64,
    #[serde(default = "default_max_retries")]
    pub max_retries: usize,
}

impl Default for Budget {
    fn default() -> Self {
        Self {
            max_time_ms: default_max_time_ms(),
            max_tokens: default_max_tokens(),
            max_retries: default_max_retries(),
        }
    }
}

fn default_max_time_ms() -> u64 { 1500 }
fn default_max_tokens() -> u64 { 300 }
fn default_max_retries() -> usize { 1 }

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
#[serde(tag = "kind")]
pub enum VerifyRule {
    #[serde(rename = "required")]
    Required { paths: Vec<String> },
    #[serde(rename = "range")]
    Range {
        path: String,
        min: f64,
        max: f64,
    },
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
pub struct VerifySpec {
    pub schema: Option<serde_json::Value>,
    #[serde(default)]
    pub rules: Vec<VerifyRule>,
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
pub struct RunDetSpec {
    pub handler: String,
    #[serde(default)]
    pub args: serde_json::Value,
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
pub struct RunLlmSpec {
    pub adapter: String,
    #[serde(default)]
    pub input: serde_json::Value,
    pub output_schema: serde_json::Value,
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
#[serde(tag = "kind", content = "spec")]
pub enum RunSpec {
    #[serde(rename = "det")]
    Det(RunDetSpec),
    #[serde(rename = "llm")]
    Llm(RunLlmSpec),
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
pub struct Policy {
    pub budget: Option<Budget>,
    #[serde(default = "default_on_fail")]
    pub on_fail: OnFailPolicy,
    pub adaptive: Option<AdaptiveRoutingPolicy>,
}

impl Default for Policy {
    fn default() -> Self {
        Self {
            budget: None,
            on_fail: default_on_fail(),
            adaptive: None,
        }
    }
}

#[derive(Debug, Serialize, Deserialize, Clone, Copy, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum OnFailPolicy {
    Retry,
    Fail,
    Escalate,
}

fn default_on_fail() -> OnFailPolicy { OnFailPolicy::Fail }

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
pub struct AdaptiveRoutingPolicy {
    #[serde(default = "default_routing_profile")]
    pub routing_profile: String,
    #[serde(default = "default_min_confidence")]
    pub min_confidence_to_stop: f64,
    #[serde(default = "default_min_voi")]
    pub min_voi_to_escalate: f64,
    #[serde(default = "default_max_escalations")]
    pub max_escalations: usize,
    #[serde(default = "default_escalation_order")]
    pub escalation_order: Vec<String>,
    #[serde(default = "default_stage_costs")]
    pub stage_costs: HashMap<String, f64>,
    #[serde(default = "default_true")]
    pub use_voi: bool,
    #[serde(default = "default_sc_samples")]
    pub self_consistency_samples: usize,
    #[serde(default = "default_true")]
    pub self_consistency_enabled: bool,
    #[serde(default = "default_sc_max_tokens")]
    pub self_consistency_max_tokens: u64,
    #[serde(default = "default_sc_min_next_cost")]
    pub self_consistency_min_next_cost: f64,
    #[serde(default = "default_sc_min_rem_budget")]
    pub self_consistency_min_remaining_budget: f64,
    #[serde(default = "default_false")]
    pub enable_gate_retrieval: bool,
    #[serde(default = "default_retrieval_strategy")]
    pub retrieval_strategy: String,
    #[serde(default = "default_retrieval_ttl")]
    pub retrieval_ttl_seconds: u64,
    #[serde(default = "default_retrieval_max")]
    pub retrieval_max_entries: usize,
}

fn default_routing_profile() -> String { "balanced".to_string() }
fn default_min_confidence() -> f64 { 0.85 }
fn default_min_voi() -> f64 { 0.2 }
fn default_max_escalations() -> usize { 2 }
fn default_escalation_order() -> Vec<String> { vec!["mini".to_string(), "gate".to_string(), "full".to_string()] }
fn default_stage_costs() -> HashMap<String, f64> {
    let mut m = HashMap::new();
    m.insert("mini".to_string(), 1.0);
    m.insert("gate".to_string(), 3.0);
    m.insert("full".to_string(), 10.0);
    m
}
fn default_true() -> bool { true }
fn default_false() -> bool { false }
fn default_sc_samples() -> usize { 2 }
fn default_sc_max_tokens() -> u64 { 64 }
fn default_sc_min_next_cost() -> f64 { 200.0 }
fn default_sc_min_rem_budget() -> f64 { 500.0 }
fn default_retrieval_strategy() -> String { "exact".to_string() }
fn default_retrieval_ttl() -> u64 { 3600 }
fn default_retrieval_max() -> usize { 1000 }

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
pub struct Task {
    pub id: String,
    #[serde(rename = "type")]
    pub task_type: String,
    #[serde(default)]
    pub deps: Vec<String>,
    #[serde(rename = "in", default)]
    pub input: serde_json::Value,
    pub run: RunSpec,
    pub verify: Option<VerifySpec>,
    #[serde(default)]
    pub policy: Policy,
    #[serde(default)]
    pub tags: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
pub struct GraphDefaults {
    pub budget: Budget,
}

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq)]
pub struct TaskGraph {
    pub graph_id: String,
    pub version: String,
    pub root: String,
    pub defaults: GraphDefaults,
    pub tasks: Vec<Task>,
}

pub fn normalize_graph(graph: &TaskGraph) -> TaskGraph {
    let mut normalized = graph.clone();
    let default_budget = &normalized.defaults.budget;

    for task in &mut normalized.tasks {
        if task.policy.budget.is_none() {
            task.policy.budget = Some(default_budget.clone());
        }

        if let RunSpec::Llm(llm_spec) = &task.run {
            if task.verify.is_none() {
                task.verify = Some(VerifySpec {
                    schema: Some(llm_spec.output_schema.clone()),
                    rules: vec![],
                });
            } else if let Some(verify) = &mut task.verify {
                if verify.schema.is_none() {
                    verify.schema = Some(llm_spec.output_schema.clone());
                }
            }
        }
    }

    normalized
}

pub fn validate_graph(graph: &TaskGraph) -> Result<(), ValidationError> {
    if graph.tasks.is_empty() {
        return Err(ValidationError::EmptyTasks);
    }

    let mut task_ids = HashSet::new();
    for task in &graph.tasks {
        if !task_ids.insert(&task.id) {
            return Err(ValidationError::DuplicateTaskId(task.id.clone()));
        }
    }

    if !task_ids.contains(&graph.root) {
        return Err(ValidationError::RootTaskNotFound(graph.root.clone()));
    }

    for task in &graph.tasks {
        for dep in &task.deps {
            if !task_ids.contains(dep) {
                return Err(ValidationError::UnknownDependency(task.id.clone(), dep.clone()));
            }
        }

        if let RunSpec::Llm(_) = &task.run {
            let has_schema = task.verify.as_ref()
                .and_then(|v| v.schema.as_ref())
                .is_some();
            if !has_schema {
                return Err(ValidationError::LlmTaskMissingSchema(task.id.clone()));
            }
        }
    }

    // Cycle check: simple stack-based DFS
    let mut visited: HashMap<&str, i32> = HashMap::new(); // ID -> status: 0 = unvisited, 1 = visiting, 2 = visited
    for task in &graph.tasks {
        visited.insert(task.id.as_str(), 0);
    }

    let task_map: HashMap<&str, &Task> = graph.tasks.iter().map(|t| (t.id.as_str(), t)).collect();

    fn dfs<'a>(
        node_id: &'a str,
        task_map: &HashMap<&'a str, &'a Task>,
        visited: &mut HashMap<&'a str, i32>,
    ) -> bool {
        visited.insert(node_id, 1); // mark as visiting
        if let Some(task) = task_map.get(node_id) {
            for dep in &task.deps {
                if let Some(status) = visited.get(dep.as_str()) {
                    if *status == 1 {
                        return true; // cycle found
                    } else if *status == 0 {
                        if dfs(dep, task_map, visited) {
                            return true;
                        }
                    }
                }
            }
        }
        visited.insert(node_id, 2); // mark as visited
        false
    }

    for task in &graph.tasks {
        if let Some(&status) = visited.get(task.id.as_str()) {
            if status == 0 {
                if dfs(task.id.as_str(), &task_map, &mut visited) {
                    return Err(ValidationError::CycleDetected);
                }
            }
        }
    }

    Ok(())
}
