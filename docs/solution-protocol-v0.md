# KORA Solution Protocol v0alpha1

Status: bounded public architecture, package validation, and reference Host lifecycle contract.

KORA Solution Protocol separates KORA's execution-control layer from independently developed AI services. A conforming Solution Package declares what it needs, what it may do, how its Task Graph and data are validated, and how its files are integrity-checked before execution.

The v0alpha1 reference path is deliberately local, offline, synchronous, and fail-closed. It validates and installs packages, executes a small deterministic capability set, and persists machine-readable status and result records. It is a conformance foundation, not a production Host claim.

## Responsibilities

KORA Core owns cross-solution execution intelligence:

- deterministic-first and model-necessity decisions;
- Task Graph semantics;
- capability selection;
- privacy, budget, approval, and side-effect policy;
- cache/reuse decisions;
- execution evidence and failure semantics.

A KORA Host owns package discovery, validation, installation, lifecycle, status, and evidence surfaces.

Capability Runtimes implement concrete deterministic tools, local models, provider adapters, and artifact operations.

A Solution Package owns only its workflow-specific manifest, schemas, Task Graph, policy declaration, and implementation assets.

A new Solution must not require workflow-specific KORA Core changes.

## Package layout

A v0alpha1 package uses JSON for its canonical hashed representation:

    example-solution/
      solution.json
      graph/
        workflow.json
      schemas/
        input.schema.json
        output.schema.json

YAML authoring and canonical conversion may be added by the SDK later. JSON is the only canonical v0alpha1 validation format.

## Manifest

The manifest is `solution.json` and contains:

- `apiVersion`: protocol compatibility identifier;
- `kind`: `Solution`;
- `metadata`: stable Solution id and semantic version;
- `requires`: KORA version constraint and required capabilities;
- `inputs` and `outputs`: JSON Schema files;
- `graph`: Task Graph file;
- `policy`: network, side effects, and required approvals;
- `integrity`: SHA-256 digests for referenced package files.

The machine-readable schema is packaged at `kora/solution/schemas/solution-manifest.schema.json`.

## Compatibility

The only supported initial `apiVersion` is `kora.dev/v0alpha1`.

Unsupported versions fail before graph, capability, installation, or execution processing. Future major protocol changes may be incompatible. Additive evolution within the same compatibility line must preserve existing valid packages.

The `requires.kora` field is recorded in v0alpha1. Full version-range resolution remains deferred.

## Reference capabilities

Every handler or adapter used by the Task Graph must appear in `requires.capabilities`. Validation fails when a graph uses an undeclared capability or the Host does not provide a declared capability.

The bounded reference runtime exposes only:

| Capability | Behavior | Side-effect boundary |
| --- | --- | --- |
| `det.echo` | Return mapped input fields. | None |
| `text.normalize` | Apply deterministic NFKC, line-ending, whitespace, and blank-line normalization. | None |
| `local.file.read` | Read UTF-8 content inside the current run workspace. | Read is confined to the run workspace. |
| `local.file.write` | Write UTF-8 content inside the current run workspace. | Requires `local.file.write` declaration and grant. |
| `fixture.fail` | Produce a deliberate bounded runtime failure for conformance tests. | Test-only failure path. |
| `approval.require` | Require a named approval and return its granted state. | Test-only approval path. |

Local file paths reject absolute paths, parent traversal, and symlinks. Reads and writes are limited to 1 MiB per file.

No reference capability performs a provider call, model inference, network request, or GPU execution.

## Policy and approvals

Task tags beginning with `side_effect:` declare effects used by the graph. Each effect must appear in both `policy.sideEffects` and `policy.approvals`.

A manifest approval is a requirement, not an automatically granted permission. The Host compares required approvals with explicit run grants before execution. Missing grants fail closed with a machine-readable result.

The bounded reference Host accepts only `network: denied` Solutions. A network-allowed manifest is not executable through this Host even if it contains a network approval declaration.

## Task Graph

The protocol reuses KORA Task IR v0.1. Validation includes:

- Pydantic structure validation;
- unique task ids;
- valid root;
- known dependencies;
- required verification schema for model tasks;
- cycle rejection;
- declared capability and side-effect checks.

The reference runtime schedules validated deterministic nodes in stable dependency order. Model-backed nodes are outside this runtime.

## Integrity and installation

`solution.json` is not self-hashed because that would create a circular digest. Referenced graph and schema files must be listed in `integrity.files`.

Package validation rejects missing files, absolute or parent-traversal paths, symlinked validated files, and SHA-256 mismatches.

The reference Host adds a second installation boundary:

1. scan every regular package file under bounded file-count and byte limits;
2. reject any package symlink;
3. copy the package into an isolated local store;
4. validate the copied package again;
5. persist a receipt containing every copied file digest and a deterministic tree digest;
6. verify the complete installed snapshot before every run.

This Host receipt covers `solution.json` and detects added, removed, or modified installed files before execution.

## Bounded Host lifecycle

The implemented synchronous interface is:

1. `validate`: read-only package validation against runtime capabilities;
2. `install`: isolated copy, revalidation, and full-snapshot receipt;
3. `run`: integrity, package, input, approval, runtime, and output gates;
4. `status`: schema-validated persisted lifecycle status;
5. `result`: schema-validated final result envelope.

Implemented lifecycle states and transitions are:

- `created -> validating -> running -> succeeded`;
- `created -> validating -> failed` for pre-execution rejection;
- `created -> validating -> running -> failed` for runtime or output failure.

Each persisted status includes the complete transition history.

### Stop and resume boundary

Stop and resume are intentionally not exposed by this synchronous reference Host. No fake stop, resume, checkpoint, or resumed state is emitted.

The deferred contract requires all of the following before either operation can be exposed:

- stop is accepted only for a running execution and records a runtime-acknowledged transition through `stopping` to `stopped`;
- resume is accepted only for a stopped execution with an immutable checkpoint reference and an explicit resumability declaration;
- resume records a runtime-acknowledged transition through `resuming` to `running`;
- rejected stop/resume requests return a bounded machine-readable error without changing state;
- an updated runtime-status schema includes the new states and the transition history remains complete;
- conformance tests demonstrate actual interruption, checkpoint persistence, and resumed execution.

Those states are deliberately absent from the current schema and CLI. The contract remains deferred until a runtime can satisfy every requirement above in a testable way.

## Result and runtime-status contracts

The bundled schemas are:

- `kora/solution/schemas/result-envelope.schema.json`;
- `kora/solution/schemas/runtime-status.schema.json`.

Both contracts include:

- schema and protocol version;
- Solution id and version;
- run id and lifecycle state;
- input and output validation status;
- a relative evidence/status reference;
- bounded error code and detail;
- execution, network, model, and GPU activity facts;
- UTC timestamps.

Runtime status also includes transition history. A successful result must have valid input/output, an object output, and no error. A failed result must have a bounded error object and no output.

## CLI

Validate either reference Solution without executing it:

    kora solution validate examples/solutions/hello-solution --json
    kora solution validate examples/solutions/document-transform-fixture --json

Install and run through an explicit local store:

    kora solution install examples/solutions/hello-solution --store /tmp/kora-host --json
    kora solution run example.hello --store /tmp/kora-host --input examples/solutions/inputs/hello.json --json
    kora solution status RUN_ID --store /tmp/kora-host --json
    kora solution result RUN_ID --store /tmp/kora-host --json

The input file for `example.hello` is a JSON object such as `{"message":"Hello"}`. The document-transform input is a JSON object such as `{"text":"  Alpha   value  "}`.

## Reference Solutions and conformance

The two synthetic reference Solutions are:

- `examples/solutions/hello-solution`, using `det.echo`;
- `examples/solutions/document-transform-fixture`, using `text.normalize`.

They use the same manifest, input/output schema, Task Graph, policy, integrity, Host lifecycle, status, and result contracts. Neither adds workflow-specific KORA Core logic.

Automated conformance covers valid installation and deterministic runs, malformed input/output, missing capabilities, undeclared side effects, missing approvals, installed-package tampering, deliberate runtime failure, lifecycle transitions, isolated file operations, contract corruption, and zero network/model/GPU activity.

## Current boundary

Implemented:

- strict manifest and referenced-schema validation;
- Task Graph, capability, side-effect, approval, path, and SHA-256 checks;
- two synthetic reference Solutions;
- isolated local installation and full installed-snapshot verification;
- bounded deterministic reference runtime;
- synchronous run, status, and result lifecycle;
- machine-readable result and runtime-status schemas;
- fail-closed conformance tests.

Deferred:

- remove/update lifecycle;
- stop/resume and checkpoints;
- cache execution;
- persistent external capability registry and runtime negotiation;
- provider, model, network, and GPU capabilities;
- package signing;
- SDK scaffold and packaging;
- registry/marketplace;
- YAML authoring;
- production validation;
- commercial Solution selection.

These synthetic fixtures prove a bounded architecture path. They do not establish production readiness, workload quality, customer savings, or commercial-product selection.
