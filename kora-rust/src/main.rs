use std::env;
use std::fs;
use std::process;
use kora_rust::task_ir::{TaskGraph, validate_graph};
use kora_rust::executor::run_graph;

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: kora-cli <path-to-graph.json>");
        process::exit(1);
    }

    let file_path = &args[1];
    let content = match fs::read_to_string(file_path) {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Error reading file '{}': {}", file_path, e);
            process::exit(1);
        }
    };

    let graph: TaskGraph = match serde_json::from_str(&content) {
        Ok(g) => g,
        Err(e) => {
            eprintln!("Error parsing JSON: {}", e);
            process::exit(1);
        }
    };

    if let Err(e) = validate_graph(&graph) {
        eprintln!("Graph validation failed: {}", e);
        process::exit(1);
    }

    match run_graph(&graph).await {
        Ok(outputs) => {
            println!("\nFinal State Outputs:");
            println!("{}", serde_json::to_string_pretty(&outputs).unwrap());
        }
        Err(e) => {
            eprintln!("Execution error: {}", e);
            process::exit(1);
        }
    }
}
