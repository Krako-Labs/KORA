pub mod task_ir;
pub mod scheduler;
pub mod executor;
pub mod security;

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use crate::task_ir::{TaskGraph, validate_graph as ir_validate_graph, normalize_graph as ir_normalize_graph};
use crate::executor::run_graph as executor_run_graph;

#[pyfunction]
fn validate_graph(json_str: &str) -> PyResult<()> {
    let graph: TaskGraph = serde_json::from_str(json_str)
        .map_err(|e| PyValueError::new_err(format!("Invalid JSON graph: {}", e)))?;

    ir_validate_graph(&graph)
        .map_err(|e| PyValueError::new_err(format!("Graph validation failed: {}", e)))?;

    Ok(())
}

#[pyfunction]
fn normalize_graph(json_str: &str) -> PyResult<String> {
    let graph: TaskGraph = serde_json::from_str(json_str)
        .map_err(|e| PyValueError::new_err(format!("Invalid JSON graph: {}", e)))?;

    let normalized = ir_normalize_graph(&graph);
    let serialized = serde_json::to_string(&normalized)
        .map_err(|e| PyValueError::new_err(format!("Failed to serialize normalized graph: {}", e)))?;

    Ok(serialized)
}

#[pyfunction]
fn run_graph(json_str: &str) -> PyResult<String> {
    let graph: TaskGraph = serde_json::from_str(json_str)
        .map_err(|e| PyValueError::new_err(format!("Invalid JSON graph: {}", e)))?;

    // Create a local runtime to execute the async executor synchronously for Python
    let rt = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .map_err(|e| PyValueError::new_err(format!("Failed to build Tokio runtime: {}", e)))?;

    let outputs = rt.block_on(executor_run_graph(&graph))
        .map_err(|e| PyValueError::new_err(format!("Execution failed: {}", e)))?;

    let serialized = serde_json::to_string(&outputs)
        .map_err(|e| PyValueError::new_err(format!("Failed to serialize execution outputs: {}", e)))?;

    Ok(serialized)
}

#[pymodule]
fn kora_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(validate_graph, m)?)?;
    m.add_function(wrap_pyfunction!(normalize_graph, m)?)?;
    m.add_function(wrap_pyfunction!(run_graph, m)?)?;
    Ok(())
}
