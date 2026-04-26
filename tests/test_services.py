"""Unit tests for service layer behavior."""

from __future__ import annotations

import unittest
from pathlib import Path
import shutil
from uuid import uuid4

from langchain_core.documents import Document

from src.config.settings import AppSettings
from src.models.document import UploadRequest
from src.services.chat_service import ChatService
from src.services.document_service import DocumentService
from src.services.knowledge_service import KnowledgeService


class FakeVectorStore:
    def __init__(self):
        self.records: list[tuple[list[str], list[dict]]] = []

    def add_texts(self, texts: list[str], metadatas: list[dict]) -> list[str]:
        self.records.append((texts, metadatas))
        return [str(index) for index in range(len(texts))]

    def similarity_search(self, query: str, k: int) -> list[Document]:
        return [
            Document(
                page_content=f"{query} - source snippet",
                metadata={"source": "unit-test.txt"},
            )
        ]

    def count(self) -> int:
        return sum(len(texts) for texts, _ in self.records)


class FakeRagChain:
    def invoke(self, payload, config):
        return f"answer for {payload['input']} / {config['configurable']['session_id']}"


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_root = Path("tests") / ".tmp"
        temp_root.mkdir(parents=True, exist_ok=True)
        self.temp_dir = temp_root / f"service-tests-{uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        root = self.temp_dir
        self.settings = AppSettings.model_validate(
            {
                "paths": {
                    "chroma_db": str(root / "chroma_db"),
                    "chat_history": str(root / "chat_history"),
                    "data": str(root / "data"),
                    "md5_registry": str(root / "md5.text"),
                    "logs_dir": str(root / "logs"),
                }
            }
        )
        self.vector_store = FakeVectorStore()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_document_service_detects_utf8(self):
        service = DocumentService()
        preview = service.preview_bytes("demo.txt", "你好，知识库".encode("utf-8"))
        self.assertEqual(preview.encoding, "utf-8")
        self.assertEqual(preview.filename, "demo.txt")

    def test_knowledge_service_skips_duplicate_document(self):
        service = KnowledgeService(settings=self.settings, vector_store=self.vector_store)
        request = UploadRequest(filename="demo.txt", content="same content", operator="tester")

        first_result = service.upload_text(request)
        second_result = service.upload_text(request)

        self.assertTrue(first_result.success)
        self.assertFalse(first_result.skipped)
        self.assertTrue(second_result.skipped)
        self.assertEqual(self.vector_store.count(), 1)

    def test_chat_service_returns_answer_and_sources(self):
        service = ChatService(
            settings=self.settings,
            vector_store=self.vector_store,
            rag_chain=FakeRagChain(),
        )

        response = service.ask("如何推荐尺码", session_id="u-001")

        self.assertIn("如何推荐尺码", response.answer)
        self.assertEqual(response.session_id, "u-001")
        self.assertEqual(len(response.sources), 1)


if __name__ == "__main__":
    unittest.main()
