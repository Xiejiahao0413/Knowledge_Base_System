import streamlit as st

from src.web.pages.upload import render_upload_page


if __name__ == "__main__":
    st.set_page_config(page_title="知识库上传", page_icon="📚", layout="wide")
    render_upload_page()
