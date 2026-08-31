# KORA Solution Protocol v0alpha1

Status: initial public architecture and validation contract.

KORA Solution Protocol separates KORA's execution-control layer from independently developed AI services. A conforming Solution Package declares what it needs, what it may do, how its Task Graph is validated, and how its files are integrity-checked before execution.

This initial slice is deliberately offline and fail-closed. It validates packages; it does not install or execute them.

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

A v0alpha1 package uses JSON for its canonical signed and hashed representation:

    example-solution/
      solution.json
      graph/
        workflow.json
      schemas/
        input.schema.json
        output.schema.json

YAML authoring and canonical conversion may be added by the SDK later. JSON is the only canonical v0alpha1 validation format.

## Manifest

The manifest is solution.json and contains:

- apiVersion: protocol compatibility identifier;
- kind: Solution;
- metadata: stable Solution id and semantic version;
- requires: KORA version constraint and required capabilities;
- inputs and outputs: JSON Schema files;
- graph: Task Graph file;
- policy: network, side effects, and approvals;
- integrity: SHA-256 digests for every referenced package file.

The machine-readable schema is packaged at kora/solution/schemas/solution-manifest.schema.json.

## Compatibility

The only supported initial apiVersion is kora.dev/v0alpha1.

Unsupported versions fail before schema, graph, capability, or execution processing. Future major protocol changes may be incompatible. Additive evolution within the same compatibility line must preserve existing valid packages.

The requires.kora field is recorded in this slice but full version-range resolution is deferred to the Host lifecycle milestone.

## Capabilities

Every deterministic handler or model adapter used by the Task Graph must appear in requires.capabilities.

Validation fails when:

- a graph uses an undeclared capability;
- a declared capability is unavailable from the Host capability set.

The initial offline reference capability set contains det.echo and text.normalize. A persistent capability registry is the next Host milestone.

## Policy and approvals

Task tags beginning with side_effect: declare effects used by the graph. Each effect must appear in policy.sideEffects and policy.approvals.

Network is denied by default in the reference fixtures. When network is allowed, policy.approvals must include network.access.

This intentionally conservative v0 rule will later evolve into typed approval scopes and lifecycle-bound grants.

## Task Graph

The protocol reuses KORA Task IR v0.1. Validation includes:

- Pydantic structure validation;
- unique task ids;
- valid root;
- known dependencies;
- required verification schema for model tasks;
- cycle rejection;
- declared capability and side-effect checks.

## Integrity

solution.json is not self-hashed because that would create a circular digest. Every referenced graph and schema file must be listed in integrity.files.

Validation rejects:

- missing referenced files;
- absolute paths or parent traversal;
- symlinked validated files;
- SHA-256 mismatch.

The design follows the same content-addressed trust principle used by OCI descriptors: verify size and digest before consuming untrusted content. The initial KORA slice requires SHA-256.

## CLI

Validate the bundled reference Solution:

    kora solution validate examples/solutions/hello-solution

Structured output:

    kora solution validate examples/solutions/hello-solution --json

Override the available Host capability set for conformance testing:

    kora solution validate examples/solutions/hello-solution --capability det.echo

Validation performs no Solution execution, provider call, model inference, network request, or GPU work.

## Current boundary

Implemented in this slice:

- strict manifest schema;
- referenced JSON Schema checks;
- Task Graph validation;
- capability declaration and availability checks;
- side-effect and approval checks;
- path containment and symlink rejection;
- SHA-256 verification;
- structured CLI results;
- positive and negative conformance tests.

Deferred:

- installation and removal;
- persistent capability registry;
- runtime handshake;
- result/status envelopes;
- stop/resume lifecycle;
- cache execution;
- package signing;
- SDK scaffold and packaging;
- registry/marketplace;
- YAML authoring;
- commercial Solution selection.

## Alpha direction

Protocol Alpha ultimately requires two different reference Solutions to install and run through the same contract without Core changes. hello-solution is the first validation fixture. document-transform-fixture, Host lifecycle, reference runtime, and full conformance execution follow in later bounded slices.
