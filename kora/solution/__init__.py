"""KORA Solution Protocol validation and bounded Host primitives."""

from .authoring import (
    SCAFFOLD_SCHEMA_VERSION,
    SolutionAuthoringError,
    integrity_file_digests,
    package_digest,
    package_file_digests,
    scaffold_solution,
)
from .conformance import (
    CONFORMANCE_CASES_DIRECTORY,
    SolutionConformanceError,
    run_solution_conformance,
)
from .contracts import (
    CONFORMANCE_CASE_SCHEMA,
    CONFORMANCE_REPORT_SCHEMA,
    RESULT_ENVELOPE_SCHEMA,
    RUNTIME_DESCRIPTOR_SCHEMA,
    RUNTIME_STATUS_SCHEMA,
    SolutionContractError,
    validate_contract_instance,
)
from .host import LocalSolutionHost, SolutionHostError
from .reference_runtime import (
    DOCUMENT_PDF_CAPABILITIES,
    DOCUMENT_PDF_CAPABILITY,
    REFERENCE_CAPABILITIES,
    DocumentPdfReferenceRuntime,
    ReferenceRuntime,
    ReferenceRuntimeError,
    RuntimeExecution,
    default_reference_runtimes,
    document_pdf_runtime_available,
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
    "CONFORMANCE_CASES_DIRECTORY",
    "CONFORMANCE_CASE_SCHEMA",
    "CONFORMANCE_REPORT_SCHEMA",
    "DEFAULT_REFERENCE_CAPABILITIES",
    "DOCUMENT_PDF_CAPABILITIES",
    "DOCUMENT_PDF_CAPABILITY",
    "REFERENCE_CAPABILITIES",
    "RESULT_ENVELOPE_SCHEMA",
    "RUNTIME_DESCRIPTOR_SCHEMA",
    "RUNTIME_STATUS_SCHEMA",
    "SCAFFOLD_SCHEMA_VERSION",
    "SUPPORTED_API_VERSION",
    "CapabilityRegistryError",
    "CapabilityRuntime",
    "LocalCapabilityRegistry",
    "LocalSolutionHost",
    "DocumentPdfReferenceRuntime",
    "ReferenceRuntime",
    "ReferenceRuntimeError",
    "ResolvedRuntime",
    "RuntimeExecution",
    "SolutionAuthoringError",
    "SolutionConformanceError",
    "SolutionContractError",
    "SolutionHostError",
    "SolutionValidationError",
    "SolutionValidationIssue",
    "integrity_file_digests",
    "package_digest",
    "package_file_digests",
    "default_reference_runtimes",
    "document_pdf_runtime_available",
    "run_solution_conformance",
    "scaffold_solution",
    "validate_contract_instance",
    "validate_solution_package",
]
