use std::collections::{HashMap, VecDeque};
use crate::task_ir::{TaskGraph, ValidationError};

pub fn detect_cycle(graph: &TaskGraph) -> bool {
    let mut in_degree: HashMap<&str, usize> = HashMap::new();
    let mut dependents: HashMap<&str, Vec<&str>> = HashMap::new();

    for task in &graph.tasks {
        in_degree.insert(&task.id, 0);
        dependents.insert(&task.id, vec![]);
    }

    for task in &graph.tasks {
        for dep in &task.deps {
            if in_degree.contains_key(dep.as_str()) {
                *in_degree.entry(&task.id).or_insert(0) += 1;
                dependents.entry(dep.as_str()).or_insert_with(Vec::new).push(&task.id);
            }
        }
    }

    let mut queue: VecDeque<&str> = in_degree
        .iter()
        .filter(|(_, &degree)| degree == 0)
        .map(|(&id, _)| id)
        .collect();

    let mut visited = 0;
    while let Some(current) = queue.pop_front() {
        visited += 1;
        if let Some(deps) = dependents.get(current) {
            for &nxt in deps {
                if let Some(degree) = in_degree.get_mut(nxt) {
                    *degree -= 1;
                    if *degree == 0 {
                        queue.push_back(nxt);
                    }
                }
            }
        }
    }

    visited != graph.tasks.len()
}

pub fn topo_sort(graph: &TaskGraph) -> Result<Vec<String>, ValidationError> {
    let mut in_degree: HashMap<&str, usize> = HashMap::new();
    let mut dependents: HashMap<&str, Vec<&str>> = HashMap::new();

    for task in &graph.tasks {
        in_degree.insert(task.id.as_str(), 0);
        dependents.insert(task.id.as_str(), vec![]);
    }

    for task in &graph.tasks {
        for dep in &task.deps {
            if !in_degree.contains_key(dep.as_str()) {
                return Err(ValidationError::UnknownDependency(task.id.clone(), dep.clone()));
            }
            *in_degree.get_mut(task.id.as_str()).unwrap() += 1;
            dependents.get_mut(dep.as_str()).unwrap().push(task.id.as_str());
        }
    }

    // Sort to maintain deterministic order (like sorting deque input in python)
    let mut initial_nodes: Vec<&str> = in_degree
        .iter()
        .filter(|(_, &degree)| degree == 0)
        .map(|(&id, _)| id)
        .collect();
    initial_nodes.sort();

    let mut queue = VecDeque::from(initial_nodes);
    let mut order = Vec::new();

    while let Some(current) = queue.pop_front() {
        order.push(current.to_string());
        if let Some(deps) = dependents.get_mut(current) {
            deps.sort(); // sort dependents to match python's sorted(dependents[current])
            for &nxt in deps.iter() {
                let degree = in_degree.get_mut(nxt).unwrap();
                *degree -= 1;
                if *degree == 0 {
                    queue.push_back(nxt);
                }
            }
        }
    }

    if order.len() != graph.tasks.len() {
        return Err(ValidationError::CycleDetected);
    }

    Ok(order)
}
