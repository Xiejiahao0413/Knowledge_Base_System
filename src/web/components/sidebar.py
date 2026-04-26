"""Sidebar components."""

from __future__ import annotations

import streamlit as st

from src.config.settings import AppSettings
from src.models.document import KnowledgeBaseStats


def render_sidebar(settings: AppSettings, stats: KnowledgeBaseStats | None = None) -> None:
    with st.sidebar:
        st.header("系统概览")
        st.write(f"应用：{settings.app.name}")
        st.write(f"环境：{settings.app.environment}")
        st.write(f"知识库集合：{settings.rag.collection_name}")
        if stats:
            st.write(f"当前文档数：{stats.document_count}")
            st.caption(f"向量库路径：{stats.storage_path}")

