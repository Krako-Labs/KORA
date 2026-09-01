"""KORA Solution Protocol validation and bounded Host primitives."""

from .contracts import (
    RESULT_ENVELOPE_SCHEMA,
    RUNTIME_DESCRIPTOR_SCHEMA,
    RUNTIME_STATUS_SCHEMA,
    SolutionContractError,
    validate_contract_instance,
)
from .host import LocalSolutionHost, SolutionHostError
from .reference_runtime import (
    REFERENCE_CAPABILITIES,
    ReferenceRuntime,
    ReferenceRuntimeError,
    RuntimeExecution,
)
from .runtime_registry import (
    CapabilityRegistryError,
    CapabilityRuntime,
    LocalCapabilityRegistry,
    ResolvedRuntime,
)
from .validator import (
    DEFAULT_REFERENCE_CAPABILITIES,
    SUPPORTED_API_VERSION,
    SolutionValidationError,
    SolutionValidationIssue,
    validate_solution_package,
)

__all__ = [
    "DEFAULT_REFERENCE_CAPABILITIES",
    "REFERENCE_CAPABILITIES",
    "RESULT_ENVELOPE_SCHEMA",
    "RUNTIME_DESCRIPTOR_SCHEMA",
    "RUNTIME_STATUS_SCHEMA",
    "SUPPORTED_API_VERSION",
    "CapabilityRegistryError",
    "CapabilityRuntime",
    "LocalCapabilityRegistry",
    "LocalSolutionHost",
    "ReferenceRuntime",
    "ReferenceRuntimeError",
    "ResolvedRuntime",
    "RuntimeExecution",
    "SolutionContractError",
    "SolutionHostError",
    "SolutionValidationError",
    "SolutionValidationIssue",
    "validate_contract_instance",
    "validate_solution_package",
]
