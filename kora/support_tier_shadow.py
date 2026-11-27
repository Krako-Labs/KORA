"""Observe a resolved, read-only support-tier lookup alongside its original handler."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from threading import Lock
from typing import Literal

from kora.executor import routing_freshness_failure


@dataclass(frozen=True)
class Subject:
    tenant: str
    account: str
    principal: str


@dataclass(frozen=True)
class RouteVersions:
    policy: str
    resolver: str
    prompt: str


@dataclass(frozen=True)
class ReadBasis:
    """Evidence supplied by the trusted origin adapter for the same atomic read."""

    subject: Subject
    source: str
    fact: str
    revision: str
    grant_revision: str
    can_read: bool
    valid_until: str


@dataclass(frozen=True)
class TierReply:
    status: str
    tier: str | None = None


@dataclass(frozen=True)
class OriginRead:
    reply: TierReply
    basis: ReadBasis | None


@dataclass(frozen=True)
class Observation:
    original: TierReply
    decision: Literal["record", "would_reuse", "defer"]
    reason: str
    cached_tier: str | None = None


def _known(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


class SupportTierShadow:
    """One in-memory observation stream, with a single current candidate per subject."""

    def __init__(self, source: str) -> None:
        if not _known(source):
            raise ValueError("A trusted source identifier is required")
        self.source = source
        self._cache: dict[Subject, tuple[ReadBasis, RouteVersions, str]] = {}
        self._pending: dict[Subject, object] = {}
        self._lock = Lock()

    def observe(
        self, subject: Subject, as_of: str, origin_lookup: Callable[[Subject], OriginRead],
        *, versions: RouteVersions,
    ) -> Observation:
        """Call the original handler exactly once. Always deliver its own reply."""
        if not all(_known(value) for value in (subject.tenant, subject.account, subject.principal)):
            return Observation(origin_lookup(subject).reply, "defer", "scope_mismatch")

        # A late response may still serve its caller, but cannot rewarm an older grant.
        token = object()
        with self._lock:
            self._pending[subject] = token
        try:
            read = origin_lookup(subject)
            basis = read.basis
            reason = self._defer_reason(subject, as_of, read, versions)
        except BaseException:
            with self._lock:
                if self._pending.get(subject) is token:
                    del self._pending[subject]
                    self._cache.pop(subject, None)
            raise

        with self._lock:
            if self._pending.get(subject) is not token:
                return Observation(read.reply, "defer", "superseded_read")
            del self._pending[subject]
            if reason is not None:
                self._cache.pop(subject, None)
                return Observation(read.reply, "defer", reason)

            # The original handler performed an authorized read with a usable tier.
            assert basis is not None and read.reply.tier is not None
            cached = self._cache.get(subject)
            if cached is not None and cached[:2] == (basis, versions):
                previous_tier = cached[2]
                if previous_tier != read.reply.tier:
                    del self._cache[subject]
                    return Observation(read.reply, "defer", "origin_disagrees")
                return Observation(read.reply, "would_reuse", "verified_repeat", previous_tier)

            self._cache[subject] = (basis, versions, read.reply.tier)
            return Observation(read.reply, "record", "observed_origin")

    def _defer_reason(
        self, subject: Subject, as_of: str, read: OriginRead, versions: RouteVersions,
    ) -> str | None:
        basis = read.basis
        if not isinstance(basis, ReadBasis):
            return "missing_basis"
        if basis.subject != subject or basis.source != self.source or basis.fact != "support_tier":
            return "scope_mismatch"
        if basis.can_read is not True:
            return "read_not_granted"
        if not isinstance(versions, RouteVersions) or not all(_known(value) for value in (
            basis.revision, basis.grant_revision, versions.policy, versions.resolver, versions.prompt,
        )):
            return "unknown_version"
        if routing_freshness_failure({"as_of": as_of, "valid_until": basis.valid_until}):
            return "invalid_or_expired"
        if read.reply.status != "ok" or not _known(read.reply.tier):
            return "origin_unavailable"
        return None
