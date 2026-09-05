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

A package checked by the Conformance Kit also contains integrity-bound JSON cases under `conformance/cases/`. The deterministic SDK scaffold adds that directory, an example input, and a package README.

JSON is the only canonical v0alpha1 validation format. YAML authoring and canonical conversion remain deferred.

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

The base bounded reference runtime exposes:

| Capability | Behavior | Side-effect boundary |
| --- | --- | --- |
| `det.echo` | Return mapped input fields. | None |
| `text.normalize` | Apply deterministic NFKC, line-ending, whitespace, and blank-line normalization. | None |
| `local.file.read` | Read UTF-8 content inside the current run workspace. | Read is confined to the run workspace. |
| `local.file.write` | Write UTF-8 content inside the current run workspace. | Requires `local.file.write` declaration and grant. |
| `fixture.fail` | Produce a deliberate bounded runtime failure for conformance tests. | Test-only failure path. |
| `approval.require` | Require a named approval and return its granted state. | Test-only approval path. |

When the optional `pypdf` dependency and SQLite FTS5 are available, a separate bounded runtime exposes:

| Capability | Behavior | Side-effect boundary |
| --- | --- | --- |
| `document.pdf.lexical-query` | Ingest integrity-checked, package-local text-layer PDFs with the existing Research Foundry and return its lexical Evidence Card. | Creates fresh SQLite state in the isolated run workspace; requires `local.file.write` declaration and grant. |

Local file paths reject absolute paths, parent traversal, and symlinks. Reads and writes are limited to 1 MiB per file. Package-local PDF resolution also rejects absolute paths, parent traversal, and symlinks, and is capped at 16 PDF files and 8 MiB.

No reference capability performs a provider call, model inference, network request, or GPU execution.

## Local capability registry and runtime resolution

The Host store contains an explicit local capability runtime registry. A runtime descriptor is validated against `kora/solution/schemas/runtime-descriptor.schema.json` and declares:

- stable runtime id and semantic version;
- compatible Solution Protocol versions;
- the exact capabilities implemented by its binding;
- supported Task Graph run kinds;
- deterministic selection priority;
- whether the runtime may use network, model inference, or GPU execution.

Registration persists a canonical descriptor and a digest-bearing receipt under the isolated Host store. Descriptor files, receipts, paths, and directory contents are verified before listing, validation, installation, and every run. A persisted descriptor alone is not executable: the current Host process must also supply a matching trusted in-process binding. v0alpha1 does not dynamically import code from the registry.

Resolution requires one runtime to provide every capability required by a Solution; capabilities are not split across runtimes. Candidates are filtered by protocol, Task Graph run kind, and execution policy. The unique highest-priority compatible binding is selected. No candidate, an unbound descriptor, or a highest-priority tie fails closed with a bounded machine-readable error.

The bundled Host registers `kora.reference` version `0.1.0` on startup. It conditionally registers `kora.document-pdf-reference` version `0.1.0` only when its local PDF and FTS5 dependencies are available. This registry is local Host metadata, not a remote registry, package marketplace, general KORA Target Registry, or production plugin system.

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
6. verify the complete installed snapshot before every run;
7. resolve and record the selected integrity-checked local runtime.

This Host receipt covers `solution.json` and detects added, removed, or modified installed files before execution. Runtime descriptor and registration-receipt integrity are verified independently before execution.

## Bounded Host lifecycle

The implemented synchronous interface is:

1. `validate`: read-only package validation plus deterministic local runtime resolution;
2. `install`: isolated copy, revalidation, full-snapshot receipt, and selected-runtime evidence;
3. `run`: package and runtime integrity, fresh runtime resolution, input, approval, execution, and output gates;
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
- selected runtime id, version, and descriptor digest when resolution succeeds;
- run id and lifecycle state;
- input and output validation status;
- a relative evidence/status reference;
- bounded error code and detail;
- execution, network, model, and GPU activity facts;
- UTC timestamps.

Runtime status also includes transition history. A successful result must have valid input/output, an object output, and no error. A failed result must have a bounded error object and no output.

## CLI

Create a deterministic offline package scaffold and run its declared conformance cases:

    kora solution scaffold example.my-solution --output ./my-solution --json
    kora solution conform ./my-solution --json

Validate either hand-authored reference Solution without executing it:

    kora solution validate examples/solutions/hello-solution --json
    kora solution validate examples/solutions/document-transform-fixture --json
    kora solution validate examples/solutions/research-foundry-reference --json

Inspect the integrity-verified runtime registry, then install and run through an explicit local store:

    kora solution runtimes --store /tmp/kora-host --json
    kora solution install examples/solutions/hello-solution --store /tmp/kora-host --json
    kora solution run example.hello --store /tmp/kora-host --input examples/solutions/inputs/hello.json --json
    kora solution status RUN_ID --store /tmp/kora-host --json
    kora solution result RUN_ID --store /tmp/kora-host --json

The input file for `example.hello` is a JSON object such as `{"message":"Hello"}`. The document-transform input is a JSON object such as `{"text":"  Alpha   value  "}`. The Research Foundry reference uses `{"query":"deterministic routing","top_k":3}`, requires the `research` installation extra, and requires `--approval local.file.write` when run.

## Solution SDK and Conformance Kit

The bounded SDK creates one deterministic JSON echo template, rejects existing output paths, hashes the complete package tree, and binds every generated non-manifest file in `integrity.files`.

The Conformance Kit requires schema-valid, integrity-bound case files under `conformance/cases/`. It validates and installs the package in a fresh isolated Host store, runs cases through the same lifecycle, retrieves persisted status and result contracts, and emits a machine-readable report. A report records package and runtime digests, per-case checks, aggregate results, activity facts, and timestamps.

The bundled schemas are:

- `kora/solution/schemas/conformance-case.schema.json`;
- `kora/solution/schemas/conformance-report.schema.json`.

See [Solution SDK and Conformance Kit](solution-sdk-conformance-kit.md) for the complete authoring and exit-status contract.

## Reference Solutions and conformance

The synthetic reference set is:

- `examples/solutions/hello-solution`, a hand-authored `det.echo` package;
- `examples/solutions/document-transform-fixture`, a hand-authored `text.normalize` package;
- `examples/solutions/generated-echo-fixture`, deterministic SDK scaffold output;
- `examples/solutions/research-foundry-reference`, the existing non-commercial offline vertical mapped to one bounded package-local PDF capability.

They use the same manifest, input/output schema, Task Graph, policy, integrity, Host lifecycle, status, and result contracts. None adds workflow-specific KORA Core logic.

Automated conformance covers deterministic scaffold reproduction, descriptor validation, trusted binding requirements, deterministic priority selection, ambiguity rejection, no cross-runtime capability splitting, execution-policy filtering, registry and installed-package tampering, valid installation and deterministic runs, malformed cases and input/output, missing capabilities, undeclared side effects, missing approvals, deliberate runtime failure, lifecycle transitions, isolated file operations, package-asset path escape rejection, exact PDF evidence/no-hit outputs, contract corruption, and zero network/model/GPU activity.

## Current boundary

Implemented:

- strict manifest and referenced-schema validation;
- Task Graph, capability, side-effect, approval, path, and SHA-256 checks;
- three hand-authored references, including one existing offline vertical migration, and one scaffold-generated synthetic Solution;
- deterministic scaffold and complete package-tree digest helpers;
- integrity-bound conformance case and report schemas;
- isolated local installation and full installed-snapshot verification;
- bounded deterministic base runtime and optional package-local PDF reference runtime;
- integrity-checked local capability registry and deterministic runtime resolution;
- runtime descriptor schema and selected-runtime evidence;
- synchronous run, status, and result lifecycle;
- machine-readable result and runtime-status schemas;
- fail-closed standalone conformance execution and negative tests.

Deferred:

- remove/update lifecycle;
- stop/resume and checkpoints;
- cache execution;
- arbitrary external corpus mounts or bindings and cross-run Research Foundry state;
- dynamic runtime discovery, loading, installation, or remote registry synchronization;
- provider, model, network, and GPU capabilities;
- archive packaging, signing, trust roots, and publication;
- Registry/marketplace;
- arbitrary templates and YAML authoring;
- production validation;
- commercial Solution selection.

These references prove only a bounded architecture path. The Research Foundry package uses one synthetic PDF and is not a commercial-Solution selection. The references do not establish production readiness, workload quality, customer savings, or commercial-product selection.

See [Task 022: Existing Vertical Migration Readiness](reports/task022-existing-vertical-migration-readiness.md) for the inventory, migration gaps, frozen slice, and deferred work.


## Experimental typed node execution

Packages may opt into an integrity-bound `graph.execution` plan with
`kora.node-execution/v1`. This path validates typed input/output bindings and
resolves trusted deterministic runtimes per node. Packages without the field
retain graph-wide resolution; older strict validators reject the new field.
See [typed node execution](typed-node-execution.md) for the bounded contract,
evidence schema, compatibility and limitations, and
[benchmark scenarios](benchmark-scenario-contract.md) for measured versus planned
comparison paths. This extension does not enable network, model, GPU or cluster
execution.
