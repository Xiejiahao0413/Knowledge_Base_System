"""Knowledge base ingestion service."""

from __future__ import annotations

from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config.settings import AppSettings
from src.models.document import KnowledgeBaseStats, UploadRequest, UploadResult
from src.utils.helpers import compute_md5, utc_timestamp


class Md5Registry:
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.registry_path.exists():
            self.registry_path.write_text("", encoding="utf-8")

    def contains(self, fingerprint: str) -> bool:
        entries = {
            line.strip()
            for line in self.registry_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        return fingerprint in entries

    def add(self, fingerprint: str) -> None:
        with self.registry_path.open("a", encoding="utf-8") as file:
            file.write(f"{fingerprint}\n")


class KnowledgeService:
    def __init__(self, settings: AppSettings, vector_store):
        self.settings = settings
        self.vector_store = vector_store
        self.registry = Md5Registry(settings.md5_registry_path)
        self.splitter = RecursiveCharacterTextSplitter(
            separators=self.settings.rag.separators,
            chunk_size=self.settings.rag.chunk_size,
            chunk_overlap=self.settings.rag.chunk_overlap,
            length_function=len,
        )

    def upload_text(self, request: UploadRequest) -> UploadResult:
        content_md5 = compute_md5(request.content)
        if self.registry.contains(content_md5):
            return UploadResult(
                success=True,
                skipped=True,
                message="[跳过] 内容已经存在知识库中",
                chunk_count=0,
                document_md5=content_md5,
                filename=request.filename,
            )

        chunks = self._split_content(request.content)
        metadatas = self._build_metadata(request, len(chunks))
        self.vector_store.add_texts(texts=chunks, metadatas=metadatas)
        self.registry.add(content_md5)

        return UploadResult(
            success=True,
            skipped=False,
            message="[成功] 内容已经成功载入向量库",
            chunk_count=len(chunks),
            document_md5=content_md5,
            filename=request.filename,
        )

    def get_stats(self) -> KnowledgeBaseStats:
        return KnowledgeBaseStats(
            collection_name=self.settings.rag.collection_name,
            document_count=self.vector_store.count(),
            storage_path=str(self.settings.chroma_db_path),
        )

    def _split_content(self, content: str) -> list[str]:
        if len(content) <= self.settings.rag.max_split_char_number:
            return [content]
        return self.splitter.split_text(content)

    def _build_metadata(self, request: UploadRequest, chunk_count: int) -> list[dict]:
        return [
            {
                "source": request.filename,
                "created_at": utc_timestamp(),
                "operator": request.operator,
                "chunk_index": index,
                "chunk_count": chunk_count,
            }
            for index in range(chunk_count)
        ]

