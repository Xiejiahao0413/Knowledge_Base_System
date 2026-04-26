"""Retriever formatting helpers."""

from __future__ import annotations

from langchain_core.documents import Document


def format_documents(documents: list[Document]) -> str:
    if not documents:
        return "无相关参考资料。"

    formatted_chunks = []
    for index, document in enumerate(documents, start=1):
        formatted_chunks.append(
            f"[片段{index}]\n内容：{document.page_content}\n元数据：{document.metadata}"
        )
    return "\n\n".join(formatted_chunks)

