# KORA Reference Solutions

These synthetic packages exercise the same KORA Solution Protocol v0alpha1 contract without workflow-specific KORA Core changes.

| Solution | Capability | Input | Output |
| --- | --- | --- | --- |
| `hello-solution` | `det.echo` | `{"message":"Hello"}` | `{"message":"Hello"}` |
| `document-transform-fixture` | `text.normalize` | `{"text":"  Alpha   value  "}` | `{"text":"Alpha value"}` |

Validate both packages offline:

```bash
python3 -m kora solution validate examples/solutions/hello-solution --json
python3 -m kora solution validate examples/solutions/document-transform-fixture --json
```

Install a package into an explicit isolated store:

```bash
python3 -m kora solution install examples/solutions/hello-solution --store /tmp/kora-host --json
python3 -m kora solution install examples/solutions/document-transform-fixture --store /tmp/kora-host --json
```

Run either package with its UTF-8 JSON input file, then use the returned run id:

```bash
python3 -m kora solution run example.hello --store /tmp/kora-host --input examples/solutions/inputs/hello.json --json
python3 -m kora solution run example.document-transform --store /tmp/kora-host --input examples/solutions/inputs/document-transform.json --json
python3 -m kora solution status RUN_ID --store /tmp/kora-host --json
python3 -m kora solution result RUN_ID --store /tmp/kora-host --json
```

The reference Host is synchronous, deterministic, and offline. It verifies package integrity and input/approval policy before execution, validates output afterward, and persists schema-validated status and result records.

These fixtures do not prove production readiness, output quality, customer savings, or commercial-product selection. Stop/resume, cache execution, provider/model/GPU capabilities, and production validation remain deferred.
