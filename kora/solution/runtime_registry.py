"""Integrity-checked local capability runtime registration and resolution."""

from __future__ import annotations

import hashlib
import re
import shutil
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from .contracts import (
    RUNTIME_DESCRIPTOR_SCHEMA,
    SolutionContractError,
    canonical_json_bytes,
    load_json_object,
    validate_contract_instance,
)

MAX_REGISTERED_RUNTIMES = 64
RUNTIME_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
RUNTIME_VERSION_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?$"
)


class CapabilityRuntime(Protocol):
    """Runtime interface accepted by the local registry."""

    @property
    def capabilities(self) -> frozenset[str]:
        """Return the exact capability set implemented by this binding."""

    @property
    def descriptor(self) -> dict[str, Any]:
        """Return a machine-readable runtime descriptor."""


class CapabilityRegistryError(RuntimeError):
    """Bounded local registry or resolution failure."""

    def __init__(self, code: str, detail: str):
        self.code = code
        rendered = " ".join(str(detail).split()) or "runtime registry operation failed"
        self.detail = rendered[:512]
        super().__init__(self.detail)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": "error",
            "error": {"code": self.code, "detail": self.detail},
        }


@dataclass(frozen=True)
class ResolvedRuntime:
    """Verified descriptor and in-process runtime selected for one run."""

    descriptor: dict[str, Any]
    descriptor_digest: str
    runtime: CapabilityRuntime

    @property
    def identity(self) -> dict[str, str]:
        return {
            "id": self.descriptor["runtime"]["id"],
            "version": self.descriptor["runtime"]["version"],
            "descriptor_digest": self.descriptor_digest,
        }


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def _is_utc_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.tzinfo == timezone.utc


def _descriptor_digest(descriptor: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(descriptor)).hexdigest()


def _atomic_write_json(path: Path, payload: Any) -> None:
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_bytes(canonical_json_bytes(payload))
    temporary.replace(path)


class LocalCapabilityRegistry:
    """Persist verified descriptors and bind trusted in-process runtimes."""

    def __init__(self, root: str | Path):
        candidate = Path(root).expanduser()
        candidate.mkdir(parents=True, exist_ok=True)
        if candidate.is_symlink() or not candidate.is_dir():
            raise CapabilityRegistryError(
                "invalid_runtime_registry",
                "runtime registry root must be a regular directory",
            )
        self.root = candidate.resolve()
        self._bindings: dict[tuple[str, str], CapabilityRuntime] = {}

    def register(self, runtime: CapabilityRuntime) -> dict[str, Any]:
        """Register one trusted runtime binding with an integrity receipt."""

        try:
            descriptor = runtime.descriptor
        except (AttributeError, TypeError, ValueError) as exc:
            raise CapabilityRegistryError(
                "invalid_runtime_descriptor",
                "runtime did not provide a valid descriptor",
            ) from exc
        if not isinstance(descriptor, dict):
            raise CapabilityRegistryError(
                "invalid_runtime_descriptor",
                "runtime descriptor must be an object",
            )
        descriptor = dict(descriptor)
        try:
            validate_contract_instance(RUNTIME_DESCRIPTOR_SCHEMA, descriptor)
        except (SolutionContractError, TypeError, ValueError) as exc:
            raise CapabilityRegistryError(
                "invalid_runtime_descriptor",
                "runtime descriptor failed schema validation",
            ) from exc

        declared = frozenset(descriptor["capabilities"])
        try:
            implemented = frozenset(runtime.capabilities)
        except (AttributeError, TypeError, ValueError) as exc:
            raise CapabilityRegistryError(
                "invalid_runtime_binding",
                "runtime capability binding is invalid",
            ) from exc
        if declared != implemented or not callable(getattr(runtime, "execute", None)):
            raise CapabilityRegistryError(
                "invalid_runtime_binding",
                "runtime binding does not match its descriptor",
            )

        runtime_id = descriptor["runtime"]["id"]
        version = descriptor["runtime"]["version"]
        target = self._entry_path(runtime_id, version)
        digest = _descriptor_digest(descriptor)
        if target.exists():
            existing, existing_digest = self._verify_entry(target)
            if existing_digest != digest or existing != descriptor:
                raise CapabilityRegistryError(
                    "runtime_already_registered",
                    "a different descriptor is already registered for this runtime version",
                )
        else:
            if len(self._entry_paths()) >= MAX_REGISTERED_RUNTIMES:
                raise CapabilityRegistryError(
                    "runtime_registry_limit_exceeded",
                    "runtime registry reached its bounded entry limit",
                )
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.parent / f".register-{uuid.uuid4().hex}"
            try:
                temporary.mkdir()
                _atomic_write_json(temporary / "runtime.json", descriptor)
                _atomic_write_json(
                    temporary / "registration.json",
                    {
                        "schema_version": "kora.runtime.registration/v0alpha1",
                        "runtime": {"id": runtime_id, "version": version},
                        "descriptor_digest": digest,
                        "registered_at": _utc_now(),
                    },
                )
                temporary.replace(target)
            except Exception:
                if temporary.exists():
                    shutil.rmtree(temporary)
                raise
            self._verify_entry(target)

        self._bindings[(runtime_id, version)] = runtime
        return {
            "schema_version": "kora.runtime.registration/v0alpha1",
            "runtime": {"id": runtime_id, "version": version},
            "descriptor_digest": digest,
            "bound": True,
            "activity": {
                "execution_performed": False,
                "network_accessed": False,
                "model_inference_performed": False,
                "gpu_execution_performed": False,
            },
        }

    def list(self) -> dict[str, Any]:
        """List verified local descriptors without executing a runtime."""

        entries = []
        for path in self._entry_paths():
            descriptor, digest = self._verify_entry(path)
            key = (
                descriptor["runtime"]["id"],
                descriptor["runtime"]["version"],
            )
            entries.append(
                {
                    "descriptor": descriptor,
                    "descriptor_digest": digest,
                    "bound": key in self._bindings,
                }
            )
        return {
            "schema_version": "kora.runtime.registry-list/v0alpha1",
            "runtimes": entries,
            "activity": {
                "execution_performed": False,
                "network_accessed": False,
                "model_inference_performed": False,
                "gpu_execution_performed": False,
            },
        }

    @property
    def available_capabilities(self) -> frozenset[str]:
        """Return capabilities from verified, bound, offline runtimes."""

        capabilities: set[str] = set()
        for path in self._entry_paths():
            descriptor, _ = self._verify_entry(path)
            key = (
                descriptor["runtime"]["id"],
                descriptor["runtime"]["version"],
            )
            execution = descriptor["execution"]
            if (
                key in self._bindings
                and not execution["network_access"]
                and not execution["model_inference"]
                and not execution["gpu_execution"]
            ):
                capabilities.update(descriptor["capabilities"])
        return frozenset(capabilities)

    def resolve(
        self,
        required_capabilities: Iterable[str],
        *,
        protocol_version: str,
        task_kinds: Iterable[str],
        allow_network: bool = False,
        allow_model: bool = False,
        allow_gpu: bool = False,
    ) -> ResolvedRuntime:
        """Resolve one compatible runtime or reject ambiguous selection."""

        required = frozenset(required_capabilities)
        kinds = frozenset(task_kinds)
        verified: list[tuple[dict[str, Any], str]] = [
            self._verify_entry(path) for path in self._entry_paths()
        ]
        capable = [
            item for item in verified if required <= frozenset(item[0]["capabilities"])
        ]
        if not capable:
            raise CapabilityRegistryError(
                "missing_capability_runtime",
                "no registered runtime provides every required capability",
            )

        compatible = []
        for descriptor, digest in capable:
            execution = descriptor["execution"]
            if protocol_version not in descriptor["protocol_versions"]:
                continue
            if not kinds <= frozenset(descriptor["task_kinds"]):
                continue
            if execution["network_access"] and not allow_network:
                continue
            if execution["model_inference"] and not allow_model:
                continue
            if execution["gpu_execution"] and not allow_gpu:
                continue
            compatible.append((descriptor, digest))
        if not compatible:
            raise CapabilityRegistryError(
                "incompatible_runtime",
                "registered capability runtimes are incompatible with this execution policy",
            )

        bound = []
        for descriptor, digest in compatible:
            key = (
                descriptor["runtime"]["id"],
                descriptor["runtime"]["version"],
            )
            if key in self._bindings:
                bound.append((descriptor, digest, self._bindings[key]))
        if not bound:
            raise CapabilityRegistryError(
                "runtime_unavailable",
                "compatible runtime descriptors have no trusted local binding",
            )

        highest = max(item[0]["priority"] for item in bound)
        selected = [item for item in bound if item[0]["priority"] == highest]
        if len(selected) != 1:
            raise CapabilityRegistryError(
                "ambiguous_runtime",
                "multiple compatible runtimes have the same highest priority",
            )
        descriptor, digest, runtime = selected[0]
        return ResolvedRuntime(
            descriptor=descriptor,
            descriptor_digest=digest,
            runtime=runtime,
        )

    def _entry_paths(self) -> list[Path]:
        entries: list[Path] = []
        for runtime_root in sorted(self.root.iterdir()):
            if runtime_root.name.startswith("."):
                raise CapabilityRegistryError(
                    "runtime_integrity_mismatch",
                    "runtime registry contains an incomplete entry",
                )
            if (
                runtime_root.is_symlink()
                or not runtime_root.is_dir()
                or not RUNTIME_ID_PATTERN.fullmatch(runtime_root.name)
            ):
                raise CapabilityRegistryError(
                    "runtime_integrity_mismatch",
                    "runtime registry contains an unsafe runtime directory",
                )
            versions = sorted(runtime_root.iterdir())
            if not versions:
                raise CapabilityRegistryError(
                    "runtime_integrity_mismatch",
                    "runtime registry contains an incomplete runtime directory",
                )
            for entry in versions:
                if (
                    entry.name.startswith(".")
                    or entry.is_symlink()
                    or not entry.is_dir()
                    or not RUNTIME_VERSION_PATTERN.fullmatch(entry.name)
                ):
                    raise CapabilityRegistryError(
                        "runtime_integrity_mismatch",
                        "runtime registry contains an unsafe version directory",
                    )
                entries.append(entry)
        return entries

    def _entry_path(self, runtime_id: str, version: str) -> Path:
        if not RUNTIME_ID_PATTERN.fullmatch(
            runtime_id
        ) or not RUNTIME_VERSION_PATTERN.fullmatch(version):
            raise CapabilityRegistryError(
                "invalid_runtime_descriptor",
                "runtime identity is invalid",
            )
        runtime_root = self.root / runtime_id
        if runtime_root.exists() and (
            runtime_root.is_symlink() or not runtime_root.is_dir()
        ):
            raise CapabilityRegistryError(
                "runtime_integrity_mismatch",
                "runtime registry identity directory is unsafe",
            )
        target = runtime_root / version
        resolved = target.resolve(strict=False)
        if not resolved.is_relative_to(self.root) or target.is_symlink():
            raise CapabilityRegistryError(
                "runtime_integrity_mismatch",
                "runtime registry entry escaped its root",
            )
        return resolved

    def _verify_entry(self, path: Path) -> tuple[dict[str, Any], str]:
        if (
            path.is_symlink()
            or not path.is_dir()
            or not path.resolve().is_relative_to(self.root)
        ):
            raise CapabilityRegistryError(
                "runtime_integrity_mismatch",
                "runtime registry entry is unsafe",
            )
        children = sorted(child.name for child in path.iterdir())
        if children != ["registration.json", "runtime.json"]:
            raise CapabilityRegistryError(
                "runtime_integrity_mismatch",
                "runtime registry entry contains unexpected files",
            )
        descriptor_path = path / "runtime.json"
        receipt_path = path / "registration.json"
        if descriptor_path.is_symlink() or receipt_path.is_symlink():
            raise CapabilityRegistryError(
                "runtime_integrity_mismatch",
                "runtime registry files must not be symbolic links",
            )
        try:
            descriptor = load_json_object(descriptor_path)
            receipt = load_json_object(receipt_path)
            descriptor_bytes = descriptor_path.read_bytes()
            receipt_bytes = receipt_path.read_bytes()
            validate_contract_instance(RUNTIME_DESCRIPTOR_SCHEMA, descriptor)
        except (OSError, TypeError, ValueError, SolutionContractError) as exc:
            raise CapabilityRegistryError(
                "runtime_integrity_mismatch",
                "runtime registry entry failed validation",
            ) from exc
        identity = descriptor["runtime"]
        expected_identity = {"id": path.parent.name, "version": path.name}
        digest = _descriptor_digest(descriptor)
        if (
            identity != expected_identity
            or descriptor_bytes != canonical_json_bytes(descriptor)
            or receipt_bytes != canonical_json_bytes(receipt)
            or receipt.get("schema_version") != "kora.runtime.registration/v0alpha1"
            or receipt.get("runtime") != expected_identity
            or receipt.get("descriptor_digest") != digest
            or not _is_utc_timestamp(receipt.get("registered_at"))
        ):
            raise CapabilityRegistryError(
                "runtime_integrity_mismatch",
                "runtime descriptor or registration receipt was modified",
            )
        return descriptor, digest


__all__ = [
    "MAX_REGISTERED_RUNTIMES",
    "CapabilityRegistryError",
    "CapabilityRuntime",
    "LocalCapabilityRegistry",
    "ResolvedRuntime",
]
