# Compare document policy reuse paths

Compare exact node reuse with a whole-request cache and an equivalent manual node cache using a synthetic, read-only document-access workflow. This example executes the existing KORA economics runner without a model, provider, or network.

## Run

From the repository root, after installing KORA and its development dependencies:

```bash
python -m examples.document_policy_reuse.run
python -m pytest -q tests/test_document_policy_reuse_example.py
```

The report includes actual fixture adapter dispatches, reuse hits, output checks, and local p50/p95 latency for each path. It prints JSON to standard output.

## Compare the paths

| Path | Meaning |
| --- | --- |
| No reuse | Run all nodes on each request using the KORA runner. |
| Whole-request cache | Cache the final answer only for an identical full request and adapter version. |
| Manual node cache | Use an independent dictionary and the same input projection and cache scope. |
| KORA node cache | Use the runner's exact node reuse. |

The fixture classifies a fabricated document, determines the permitted read mode, and returns a notice code. It does not read or expose document content.

## Validation boundaries

The eleven phases exercise policy change, permission revocation and renewal, expiry, rollback, data changes, adapter version and principal/tenant separation. Each phase includes an exact repeat. Every answer is checked against an authored expected action; the first request in every phase must execute all nodes. The runner's dispatch count is checked against an independent adapter counter. Deterministic adapters explicitly report zero model calls.

These are author-defined regression cases, not independent human labels. The fixture supplies complete trusted context; an integration must obtain and validate that context from an authoritative source. Reuse is not an authorization service. No external agent or real model is compared. Local timings are host-dependent; fewer dispatches do not establish lower cost, and the manual cache can match KORA's call count.

## Test a policy change and rollback

Run the separate synthetic maintenance replay:

```bash
python -m examples.document_policy_reuse.maintenance
python -m pytest -q tests/test_document_policy_maintenance_example.py
```

The replay uses the same policy implementation and expected answers for direct execution, the manual node cache, and KORA. A revised policy allows a redacted restricted document for staff with a live grant and explicit redaction permission. Five other cases check unchanged behavior, including revoked and expired grants.

| Stage | What to check |
| --- | --- |
| Baseline and repeat | All answers match; the repeat can reuse validated results. |
| Deliberately omit the version update | Both caches return one stale answer per round. Direct execution returns the new answer. This is an intentional negative control, not an acceptable policy deployment. |
| Update the adapter identity | Both caches compute the revised answers. |
| Repeat the revised policy | Both caches can reuse the revised results. |
| Roll back under a new identity | Both caches compute the original answers and reuse them on the next repeat. |

Policy code and other material dependencies must have trusted identities that change when their behavior changes. The engine cannot discover an undeclared change in an adapter. This example is not an authorization system; it returns action codes for fabricated data only.

### Bind the declared policy to its cache identity

If a policy is a declared configuration value, include a deterministic digest of that value in the adapter identity. The [declared-policy example](declared_identity.py) does this for the synthetic redaction flag consumed by the fixture.

```python
def cache_identity(self):
    manifest = {"restricted_staff_redaction": self.revised}
    return dict(
        super().cache_identity(),
        declared_policy_sha256=sha256(canonical(manifest).encode("utf-8")).hexdigest(),
    )
```

Run the regression from the repository root:

```bash
python -m pytest -q tests/test_document_policy_declared_identity_example.py
```

The test exercises both the manual cache and KORA. Changing the declared flag changes the identity even when the version is unchanged. Returning to a previously validated identity can reuse the old result only for the same trusted inputs and retained cache. If rollback must start a new validation epoch, change the version or epoch too.

A digest is not proof that an authorization decision is valid. It covers only the declared fields. Obtain trusted permissions, data versions, time and policy identities from authoritative sources; bind other material dependencies separately. This example changes configuration between requests, not concurrently with execution. It neither detects hidden changes nor grants access to real documents.

### Compare developer effort

For an independent trial, freeze the same base revision, task description, policy requirements and acceptance cases for both implementations. Start each trial from a fresh copy. Ask participants to implement the policy revision, validate it, deliberately detect the missing version update, fix it, and roll back. Use the same tools and assistance rules; vary trial order to reduce learning effects. Do not give one group the solution and the other group only the task.

Record setup time, active implementation time, validation time, diagnosis and recovery time separately. Keep the submitted diff, commands, elapsed times, assistance and outcome. Score every required case, not just the changed answer. A cache that produces a stale answer outside the intentional negative control fails. Report changed files and added/deleted lines separately from time. Do not use execution latency or lines of code as a substitute for measured developer time.

The reference replay is an executable scoring example, not an independent developer trial. It shares policy code across the comparison paths, so it does not establish a reduction in policy editing effort or production cost.
