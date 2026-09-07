# Task026 — S4 exhibition readiness

Status: S4 mandatory evidence gates passed on the frozen Task026 candidate. Maintainer approval for this documentation merge was granted on 2026-09-08 KST.

Classification: merge-ready.

Frozen base and rehearsal source: `2f59cec7a6e092abc14f36124e4bc8ce246e17f4`.

Feature freeze remains in effect. This report records validation evidence only; it does not add product capability, expand public claims, authorize merge, or constitute a release.

## Objective

Demonstrate a repeatable exhibition path for the local three-system comparison using frozen synthetic/reference fixtures, while preserving failure visibility, native-resource ownership checks, browser interaction evidence, representative older-device evidence, and explicit claim boundaries.

## Acceptance matrix

| Gate | Result | Bounded evidence |
|---|---|---|
| Frozen source and regression | PASS | `origin/main` was re-fetched and matched the frozen rehearsal commit. Fresh Python 3.13 validation completed with `749 passed`. |
| Package/build path | PASS | Fresh sdist and wheel built; benchmark HTML/CSS/JS assets were present in both artifacts; the wheel installed in an isolated environment and the packaged CLI/assets smoke passed. |
| Three-system native smoke | PASS | Five fresh HTTP batches completed across MP, two-Mac cluster, and native H100 execution. All recorded quality rows passed. Deterministic-only H100-column work is controller CPU work and is not GPU evidence. |
| Recovery behavior | PASS, bounded | Controller restart, worker identity restart, and tunnel-loss/recovery drills were exercised during Task026/S3-close validation. Worker identity changes are boot-ID bound so stale reuse is not accepted across a restarted worker. H100 borrowing was restored to the prior shared service and the lease was released. |
| Browser visual/interaction QA | PASS | Google Chrome interaction validation passed at 1440x900, 1024x768, and 768x900 with no horizontal overflow; controls, changed-input preview, history/recorded state, JSON export, keyboard focus order, and a deterministic UI run were exercised. |
| Representative older-device path | PASS, bounded | Two Mac Studio M2 Max / 32 GB endpoints executed frozen fixture roles successfully. A fresh wheel also installed and passed CLI smoke on the M2 Max validation host. CLI package-path peak RSS was 43,679,744 bytes with a 121 ms observed wall time for `python -m kora --help`; this is not model-inference memory or a performance comparison. |
| Four-hour rehearsal | PASS | The frozen candidate ran for 14,400.927 seconds with 50 periodic health samples. Controller, required listeners, and all three non-H100 worker endpoints remained healthy in every sample. Native H100 had already passed fresh preflight and was deliberately released rather than held during the long persistence window. |
| Public claim/privacy review | PASS | Only bounded synthetic/reference evidence is summarized here. No raw provider responses, private hostnames, IP addresses, credentials, tokens, billing data, raw infrastructure logs, or local filesystem paths are added. |
| Final S4 readiness | PASS for exhibition evidence | The frozen S4 exhibition evidence set is complete. This does not imply production readiness and does not remove the human merge/release approval gates. |

## Fresh native acceptance

Five fresh comparison batches were recorded against the frozen Task026 code and fixtures:

| Scenario | Reuse | Changed input | Repetitions | MP | Two-Mac cluster | Native column |
|---|---:|---:|---:|---:|---:|---:|
| D | off | no | 5 | 30/30 | 30/30 | 30/30 controller CPU only |
| M | off | no | 5 | 30/30 | 30/30 | 30/30 |
| W | on | no | 2 | 12/12 | 12/12 | 12/12 |
| W | on | yes | 2 | 12/12 | 12/12 | 12/12 |
| W | off | no | 5 | 30/30 | 30/30 | 30/30 |

For each reuse-enabled W batch, MP and cluster executed six model calls, generated 60 output tokens, and reused 12 task nodes. The native path executed 12 model calls and 120 output tokens because KORA exact-result reuse is not applied there. These counts describe the frozen harness only; they do not establish general cost, throughput, or quality claims.

A guarded-off follow-up retained H100 model rows as explicit blocked outcomes when no native execution window was active. Blocked rows were not rewritten as success or dropped from the record.

## Visual and interaction evidence

The local comparison UI was exercised in Google Chrome rather than inferred from HTTP tests. Validation covered three viewport sizes, control visibility, three result cards, changed-input preview, disabling exact reuse for the model-only scenario, recorded-history labeling, JSON export, keyboard tab order, disclosure controls, and an end-to-end deterministic UI run. The deterministic UI run collected 3/3 results and displayed completion normally.

This is browser behavior evidence for the tested local UI and viewports, not proof for every browser, operating system, accessibility configuration, or device size.

## Representative older-device evidence

The available representative older class was Mac Studio `Mac14,13`, Apple M2 Max, 32 GB, macOS 26.6.2. Two endpoints of that class were exercised: one as the model worker for a fixed M fixture and one as the deterministic worker for a fixed D fixture. Both fixture roles passed their registered quality checks. The model-worker sample executed one actual model call; the deterministic sample executed no model call.

The model-worker sample did not capture model-process peak memory, so no model-memory claim is made. Separately, the final wheel was installed into an isolated Python 3.13 environment on the same representative hardware class and passed CLI/package-path smoke. That CLI-only measurement observed 43,679,744 bytes peak RSS and about 121 ms wall time for `python -m kora --help`. It must not be interpreted as inference memory, inference latency, or hardware superiority.

Both measured endpoints are the same hardware class. This evidence therefore establishes only a bounded representative older-device path, not broad Mac compatibility.

## Recovery and persistence evidence

Task026 validation exercised recovery at the benchmark-control layer: the controller was restarted, benchmark-worker identities were restarted during the validation sequence, and worker tunnels were recovered after connection loss. The worker protocol binds requests and reuse identity to the worker boot ID, preventing a prior worker identity from being silently treated as the restarted worker. Operational details and raw logs remain private.

The native preflight was followed by restoration checks: the temporary native execution window ended, the prior shared service returned healthy with the expected model identity, and no active Task026 lease remained.

The four-hour persistence rehearsal then ran without holding the shared H100 resource. It recorded 50 health samples over 14,400.927 seconds; all sampled controller, listener, and worker checks passed. Background load and warm state were uncontrolled, so this persistence result is not a latency, throughput, energy, or hardware-comparison benchmark.

## Final source/package validation

Fresh validation on the current frozen source produced:

- `python -m pytest -q`: `749 passed`.
- repository release smoke: PASS.
- `ruff check kora/benchmarks`: PASS.
- Python compile check for `kora`: PASS.
- JavaScript syntax check for the comparison UI asset: PASS.
- sdist + wheel build: PASS.
- benchmark HTML/CSS/JS inclusion in both package artifacts: PASS.
- isolated wheel install, packaged dashboard asset read, and CLI smoke: PASS.

A broader advisory Ruff scan across the entire historical test tree reports pre-existing style findings and is not a repository CI gate. This documentation-only PR does not modify those test files. The full regression remains green.

## Claim boundary and non-claims

This evidence supports only the frozen exhibition workflow and the specific synthetic/reference cases described above. It does not establish:

- production readiness or production workload coverage;
- general output-quality superiority or broad workload representativeness;
- production cost reduction, real API/GPU cost savings, or customer savings;
- H100, GPU, CPU, M3 Max, or M2 Max performance superiority;
- multi-GPU scaling or both-GPU active-use claims;
- provider, model-serving, or GPU-serving replacement;
- general cold-start performance, because storage/OS caches were not controlled;
- broad browser, operating-system, or older-Mac compatibility;
- a published package, release, or `getkora` availability.

No release, tag, publication, repository-settings change, raw benchmark artifact upload, or public claim expansion is authorized by this report.

## Stop gate

S4 mandatory exhibition-evidence gates are complete for this frozen candidate. Maintainer approval for this bounded documentation merge was granted on 2026-09-08 KST after the evidence and claim boundaries were reviewed. Release, tags, publication, and any broader public positioning remain separate explicit approval gates.
