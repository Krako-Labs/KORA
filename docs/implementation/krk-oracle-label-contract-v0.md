# KRK Oracle Label Contract v0

## Purpose

Oracle labels define expected and acceptable routes for KRK matrix evaluation.

They are evaluation labels only. They must never be used as route-policy input.

## Fields

### `expected_route`

The single preferred route for the item.

Allowed values:

- `deterministic`.
- `cache`.
- `CPU`.
- `provider`.
- `GPU`.
- `fallback`.

Used for:

- `exact_route_accuracy`.
- `gpu_false_negative_count` when expected route is `GPU`.

### `acceptable_routes`

Routes that are acceptable for this item.

Rules:

- Must include `expected_route`.
- May include multiple values when the route decision is legitimately ambiguous.
- Should stay narrow enough to detect weak routing.

Used for:

- `acceptable_route_rate`.
- GPU false positive classification.
- cache-hit correctness classification.

### `disallowed_routes`

Routes that are unsafe or clearly inappropriate for this item.

Rules:

- Must not include `expected_route`.
- Should include routes prohibited by privacy, malformed input, stale-cache risk, or clear compute mismatch.
- Can be empty only when no route is explicitly disallowed.

Used for:

- `unsafe_misroute_rate`.
- fallback and policy-boundary review.

### `oracle_reason`

Short explanation for the expected, acceptable, and disallowed routes.

Rules:

- Public-safe.
- No private resource details.
- No raw logs.
- No local-only paths.
- No unsupported claims.

Used for:

- reviewer explanation.
- failed-route debugging.
- Markdown summary details when needed.

## Router Visibility Rule

The router must not see `oracle_labels`.

The evaluator should construct route input from:

- `request_id`.
- `workload_profile`.
- `workload_class`.
- `router_visible_metadata`.

The evaluator should not pass:

- `expected_route`.
- `acceptable_routes`.
- `disallowed_routes`.
- `oracle_reason`.
- the full original item object.

## Independence Rule

Oracle labels must be authored independently of the route policy output.

Do not:

- generate oracle labels from router output.
- modify oracle labels to make current policy look better.
- include hidden hints in `router_visible_metadata` that encode the answer.

Do:

- use oracle labels to evaluate route decisions after selection.
- document ambiguous cases with `acceptable_routes`.
- update labels only through explicit review when fixture semantics change.

## Ambiguous Tasks

Ambiguous tasks should use `acceptable_routes`.

Example:

- `expected_route`: `CPU`.
- `acceptable_routes`: `["CPU", "provider"]`.
- `disallowed_routes`: `["GPU"]`.

This allows route evaluation to credit an acceptable alternative while preserving exact-route accuracy.

## Disallowed Routes And Unsafe Misroutes

`disallowed_routes` drives `unsafe_misroute_rate`.

If selected route appears in `disallowed_routes`, then:

- `unsafe_misroute` is true.
- item is not acceptable.
- item should be counted in the unsafe misroute numerator.

## Cache Contract

Cache route is correct only when:

- selected route is `cache`.
- `cache` appears in `acceptable_routes`.
- visible metadata has `cache_key_available: true`.

If `cache_key_available` is true but `cache` is disallowed, a cache route is an unsafe misroute.

## GPU Contract

GPU false positive:

- selected route is `GPU`.
- `GPU` is not in `acceptable_routes`.

GPU false negative:

- `expected_route` is `GPU`.
- selected route is not `GPU`.

These counts are route-selectivity metrics, not production performance or infrastructure savings metrics.

## Fallback Contract

Fallback should be classified when selected route is `fallback`.

Suggested classes:

- `safety_fallback`.
- `failure_fallback`.
- `validation_fallback`.
- `unknown_fallback`.

For the first dry-run evaluator, safety fallback can be inferred from restricted privacy, malformed metadata, or policy conflict. Failure and validation fallback may remain zero unless simulated failures are added.
