# Typed node execution (experimental)

This opt-in extends the local Solution Host with typed ancestor-output bindings
and deterministic per-node runtime selection. It is a local execution foundation,
not a remote worker, inference service, or cluster implementation.

## Contract and compatibility

A Solution manifest may add `graph.execution`, a relative path to a JSON document
with `schema_version: "kora.node-execution/v1"`. The file must be contained in the
package and covered by manifest integrity. The plan covers every graph node once.
New packages are rejected by older strict manifest validators; packages without
this property retain their existing graph-wide runtime and input semantics.
The surrounding Solution Protocol remains experimental v0alpha1.

Each node declares `bindings`, `input_schema`, and `output_schema`.
Schemas use JSON Schema Draft 2020-12, declare object type, and cannot contain
reference or identity keywords (`$ref`, `$dynamicRef`, `$recursiveRef`, `$id`).
Bindings have one of these forms:

```json
{"source": "input", "path": ["text"]}
```

```json
{"source": "node", "node": "normalize", "path": ["text"]}
```

Only graph ancestors may supply node output. Paths traverse object keys, not
array indices or query expressions. Empty paths select the source object.
Static arguments and binding keys must not overlap. Bound strings beginning
with `$.` remain literal values. The plan is limited to 64 nodes, 128 bindings
per node, and 16 keys per binding path.

Nodes must be deterministic, have empty legacy `in` mappings, and use fail
policy. Legacy verification and adaptive policies are rejected in this mode.
Input and output schemas are checked immediately around each runtime invocation.

## Runtime and evidence responsibilities

The Host resolves every required node runtime before installation/run acceptance.
Each node uses the existing trusted runtime `execute` interface with a one-node
graph. No new provider interface or dynamic plugin loading is introduced.
A node failure skips all remaining nodes, including independent branches.
Successful upstream output is copied before downstream binding.

The outer result identifies `kora.node-coordinator`. Its composite descriptor
digest binds the plan, graph, and selected node runtime identities; it is not a
registered runtime descriptor. Actual node identities are in
`runs/<run-id>/node-evidence.json`, using `kora.node-evidence/v1`.
`host.node_evidence(run_id)` validates and reads this optional artifact.
Registry integrity and selection are rechecked before each node.
Missing approvals prevent runtime execution.

Node evidence records validation flags, pending/running/succeeded/failed/skipped
states, capability and runtime identity. It does not store raw intermediate
outputs. Existing run status/result schemas are unchanged. After a partial
failure, use node evidence for completed nodes: the legacy result's aggregate
capability field is not a partial-completion ledger.

This remains trusted, synchronous in-process execution. Descriptor integrity
does not sandbox runtime code or attest that code did not access a model.
There is no enforced timeout, process isolation, retry, rollback, crash recovery,
resume, parallel execution, external corpus binding, or persistent worker.
A process crash may leave a node marked running; the artifact is a trace, not a
durable job recovery protocol.

## Reproduce the local fixture

From a source checkout installed with `python -m pip install .`:

```sh
python -m kora.solution.benchmark \
  --package examples/solutions/typed-node-fixture \
  --input examples/solutions/inputs/typed-node.json \
  --expected examples/solutions/inputs/typed-node-expected.json \
  --store /tmp/kora-typed-node-demo \
  --repetitions 3
```

The fixture normalizes whitespace and passes the typed result to an echo node.
The default CLI uses the reference runtime for both capabilities. The focused
test suite configures two distinct runtime bindings to verify cross-runtime
dataflow and persisted identities.

The collector emits `kora.benchmark.local/v1` JSON. Installation is excluded;
each elapsed time covers the synchronous Host run including package validation
and artifact persistence. Page-cache state is uncontrolled; there is no result
reuse. Quality means exact fixture output equality, not semantic model quality.
Token counts and TTFT are null, not derived from avoided calls or word counts.
Model calls and exact reuse are zero for this bounded deterministic reference
path. The collector is not an independent audit of arbitrary trusted plugins.

```sh
pytest -q tests/test_solution_node_execution.py tests/test_solution_benchmark.py
```
