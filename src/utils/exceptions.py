"""Application-specific exceptions."""


class KnowledgeBaseSystemError(Exception):
    """Base exception for the project."""


class ConfigurationError(KnowledgeBaseSystemError):
    """Raised when runtime configuration is invalid."""


class DocumentProcessingError(KnowledgeBaseSystemError):
    """Raised when a document cannot be processed."""


class DuplicateDocumentError(KnowledgeBaseSystemError):
    """Raised when a document already exists in the knowledge base."""


class UnsupportedEncodingError(DocumentProcessingError):
    """Raised when a document cannot be decoded."""

