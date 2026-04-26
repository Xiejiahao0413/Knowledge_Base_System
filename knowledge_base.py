"""Legacy compatibility wrapper around the refactored knowledge service."""

from src.bootstrap import get_document_service, get_knowledge_service


class KnowledgeBaseService:
    def __init__(self):
        self.document_service = get_document_service()
        self.knowledge_service = get_knowledge_service()

    def upload_by_str(self, data: str, filename: str, operator: str = "legacy") -> str:
        request = self.document_service.build_upload_request(
            filename=filename,
            content=data,
            operator=operator,
        )
        result = self.knowledge_service.upload_text(request)
        return result.message
