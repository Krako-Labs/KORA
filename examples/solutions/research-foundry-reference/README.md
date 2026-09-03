# Research Foundry Reference Solution

This non-commercial reference Solution maps the existing deterministic Research Foundry ingest and lexical-query behavior through KORA Solution Protocol v0alpha1.

The bounded migration slice reads an integrity-verified text-layer PDF corpus packaged with the Solution, builds temporary SQLite FTS5 state inside the isolated run workspace, and returns the existing deterministic evidence-card result. The caller supplies only a query and `top_k`. The run requires an explicit `local.file.write` approval because it creates temporary local index state.

Install KORA from source with the Research extra before using this package:

```bash
python3 -m pip install -e '.[research]'
```

Then validate and run conformance:

```bash
python3 -m kora solution validate examples/solutions/research-foundry-reference --json
python3 -m kora solution conform examples/solutions/research-foundry-reference --json
```

This package is a migration-readiness fixture. It does not expose arbitrary host folders, preserve state between runs, add OCR or semantic retrieval, synthesize claims, select a commercial Solution, or establish production readiness or retrieval quality.
