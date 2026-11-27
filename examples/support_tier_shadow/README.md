# Observe a support-tier lookup

Run `kora run support_tier_shadow` from an editable KORA checkout. It prints the original result and the proposed KORA decision for seven sequential lookups against a local fixture. Each row records the source, account, principal, grant, data revision and versions of the policy, resolver and prompt configuration used by the example.

The host must already have resolved the read-only support-tier operation and authenticated its subject. The original handler runs on every request. Its adapter must return the response and evidence from the same authorized read. Supply the request date from the host and expiry from the source. Keep all of these inputs outside the request text.

On a verified repeat, `would_reuse` means that the cached tier matched the observed original response. No origin call is skipped. A denied grant, unknown scope or revision, expired fact, or disagreement with the original response defers the shadow decision and discards the previous candidate for that subject. A valid revision change or rollback starts a new observation. The cache belongs to one in-memory observation stream.

The fixture includes the dates from the public `r329` and `r591` regression cases. No external accounts, agents or model services are contacted.
