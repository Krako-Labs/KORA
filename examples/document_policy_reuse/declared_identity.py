"""Bind the declared policy value to the synthetic adapter's cache identity."""
from hashlib import sha256

from examples.document_policy_reuse.maintenance import PolicyFixture
from examples.document_policy_reuse.run import canonical


class DeclaredPolicy(PolicyFixture):
    def cache_identity(self):
        # The manifest contains the same policy value consumed by run().
        # Other dependencies still require their own trusted identities.
        manifest = {"restricted_staff_redaction": self.revised}
        return dict(
            super().cache_identity(),
            declared_policy_sha256=sha256(canonical(manifest).encode("utf-8")).hexdigest(),
        )
