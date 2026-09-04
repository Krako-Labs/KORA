# KORA Reference Solutions

These reference packages exercise the same KORA Solution Protocol v0alpha1 contract without workflow-specific KORA Core changes.

| Solution | Origin | Capability | Input | Output |
| --- | --- | --- | --- | --- |
| `hello-solution` | Hand-authored reference | `det.echo` | `{"message":"Hello"}` | `{"message":"Hello"}` |
| `document-transform-fixture` | Hand-authored reference | `text.normalize` | `{"text":"  Alpha   value  "}` | `{"text":"Alpha value"}` |
| `generated-echo-fixture` | SDK scaffold output | `det.echo` | `{"message":"..."}` | Same object |
| `research-foundry-reference` | Existing offline reference vertical | `document.pdf.lexical-query` | `{"query":"...","top_k":3}` | Research Evidence Card envelope |

Validate the packages offline:

```bash
python3 -m kora solution validate examples/solutions/hello-solution --json
python3 -m kora solution validate examples/solutions/document-transform-fixture --json
python3 -m kora solution validate examples/solutions/generated-echo-fixture --json
python3 -m kora solution validate examples/solutions/research-foundry-reference --json
```

Run each package-declared suite through the same isolated conformance entry point:

```bash
python3 -m kora solution conform examples/solutions/hello-solution --json
python3 -m kora solution conform examples/solutions/document-transform-fixture --json
python3 -m kora solution conform examples/solutions/generated-echo-fixture --json
python3 -m kora solution conform examples/solutions/research-foundry-reference --json
```

Reproduce the generated package in a new path:

```bash
python3 -m kora solution scaffold example.generated-echo --output ./generated-echo --json
```

Inspect the local runtime registry, then install a package into an explicit isolated store:

```bash
python3 -m kora solution runtimes --store /tmp/kora-host --json
python3 -m kora solution install examples/solutions/hello-solution --store /tmp/kora-host --json
python3 -m kora solution install examples/solutions/document-transform-fixture --store /tmp/kora-host --json
python3 -m kora solution install examples/solutions/research-foundry-reference --store /tmp/kora-host --json
```

Run an installed package with its UTF-8 JSON input file, then use the returned run id. The Research Foundry reference requires the `research` extra plus an explicit per-run local-write grant:

```bash
python3 -m kora solution run example.hello --store /tmp/kora-host --input examples/solutions/inputs/hello.json --json
python3 -m kora solution run example.document-transform --store /tmp/kora-host --input examples/solutions/inputs/document-transform.json --json
python3 -m kora solution run example.research-foundry-reference --store /tmp/kora-host --input examples/solutions/research-foundry-reference/examples/input.json --approval local.file.write --json
python3 -m kora solution status RUN_ID --store /tmp/kora-host --json
python3 -m kora solution result RUN_ID --store /tmp/kora-host --json
```

The reference Host is synchronous, deterministic, and offline. It verifies package and local runtime-registry integrity, resolves one trusted capability runtime before execution, validates input/approval policy and output, and persists schema-validated status and result records with selected-runtime evidence. The registry does not dynamically load code. When `pypdf` and SQLite FTS5 are available, the Host also binds the package-local, bounded `kora.document-pdf-reference` runtime; install with `pip install -e '.[research]'` for that path.

The scaffold and Conformance Kit are described in [Solution SDK and Conformance Kit](../../docs/solution-sdk-conformance-kit.md).

The Research Foundry migration inventory, frozen slice, gaps, and deferrals are recorded in [Task 022: Existing Vertical Migration Readiness](../../docs/reports/task022-existing-vertical-migration-readiness.md).

These references do not prove production readiness, output quality, customer savings, or commercial-product selection. External corpus mounts, cross-run Foundry state, stop/resume, cache execution, provider/model/GPU capabilities, and production validation remain deferred.
