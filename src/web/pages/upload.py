"""Knowledge upload Streamlit page."""

from __future__ import annotations

import streamlit as st

from src.bootstrap import get_document_service, get_knowledge_service
from src.config.settings import get_settings
from src.utils.exceptions import KnowledgeBaseSystemError
from src.web.components.sidebar import render_sidebar


def render_upload_page() -> None:
    settings = get_settings()
    document_service = get_document_service()

    st.title("知识库上传")
    st.caption("上传文本文件，自动切分并写入向量库。")

    uploaded_file = st.file_uploader(
        "请选择待上传的 TXT 文件",
        type=["txt"],
        accept_multiple_files=False,
    )

    knowledge_stats = None
    try:
        knowledge_stats = get_knowledge_service().get_stats()
    except KnowledgeBaseSystemError as error:
        st.warning(f"知识库服务尚未就绪：{error}")
    render_sidebar(settings, knowledge_stats)

    if uploaded_file is None:
        return

    content = uploaded_file.getvalue()
    preview = document_service.preview_bytes(uploaded_file.name, content)
    st.subheader("文件信息")
    st.write(f"文件名：{preview.filename}")
    st.write(f"编码：{preview.encoding}")
    st.write(f"大小：{preview.size_bytes} bytes")
    st.text_area("内容预览", preview.preview, height=320)

    if st.button("写入知识库", type="primary"):
        try:
            upload_request = document_service.read_bytes(
                filename=uploaded_file.name,
                content=content,
                operator="streamlit",
            )
            result = get_knowledge_service().upload_text(upload_request)
            st.success(result.message)
            st.write(f"切分块数：{result.chunk_count}")
            st.write(f"文档指纹：{result.document_md5}")
        except KnowledgeBaseSystemError as error:
            st.error(str(error))
