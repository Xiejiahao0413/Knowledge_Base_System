"""Document preprocessing service."""

from __future__ import annotations

from src.models.document import DocumentPreview, UploadRequest
from src.utils.helpers import decode_text_bytes


class DocumentService:
    def build_upload_request(
        self,
        filename: str,
        content: str,
        operator: str = "system",
    ) -> UploadRequest:
        return UploadRequest(filename=filename, content=content, operator=operator)

    def preview_bytes(self, filename: str, content: bytes) -> DocumentPreview:
        text, encoding = decode_text_bytes(content)
        return DocumentPreview(
            filename=filename,
            encoding=encoding,
            size_bytes=len(content),
            preview=text[:1000],
        )

    def read_bytes(self, filename: str, content: bytes, operator: str = "system") -> UploadRequest:
        text, _ = decode_text_bytes(content)
        return self.build_upload_request(filename=filename, content=text, operator=operator)

