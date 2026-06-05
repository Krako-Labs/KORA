use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SiemEvent {
    pub timestamp: DateTime<Utc>,
    pub graph_id: String,
    pub task_id: String,
    pub event_type: String, // "task_start", "task_success", "task_fail", "budget_breach", "pii_redaction", "escalate"
    pub status: String,     // "ok", "error", "skipped"
    pub duration_ms: u64,
    pub tokens_in: u64,
    pub tokens_out: u64,
    pub estimated_cost_usd: f64,
    pub message: String,
    #[serde(default)]
    pub metadata: serde_json::Value,
}

impl SiemEvent {
    pub fn new(
        graph_id: &str,
        task_id: &str,
        event_type: &str,
        status: &str,
        duration_ms: u64,
        tokens_in: u64,
        tokens_out: u64,
        estimated_cost_usd: f64,
        message: &str,
    ) -> Self {
        Self {
            timestamp: Utc::now(),
            graph_id: graph_id.to_string(),
            task_id: task_id.to_string(),
            event_type: event_type.to_string(),
            status: status.to_string(),
            duration_ms,
            tokens_in,
            tokens_out,
            estimated_cost_usd,
            message: message.to_string(),
            metadata: serde_json::Value::Null,
        }
    }

    pub fn with_metadata(mut self, metadata: serde_json::Value) -> Self {
        self.metadata = metadata;
        self
    }

    /// Emits the event to stdout as a single-line JSON string (standard for SIEM collectors)
    pub fn emit(&self) {
        if let Ok(serialized) = serde_json::to_string(self) {
            println!("{}", serialized);
        }
    }
}
