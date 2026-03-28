"""
基于streamlit完成Web网页上传服务
streamlit:当Web页面元素发生变化的时候，则代码重新执行一遍
"""

import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

st.title("知识库更新服务")

uploader_file = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False    #False表示仅仅接受单个文件夹的上传
)

#ervice = KnowledgeBaseService()
#session_state就是一个字典
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type
    
    #uploader_file 是文件对象，不能直接进行除法运算。正确做法是先获取文件内容的字节数，再除以1024得到KB
    file_size_bytes = len(uploader_file.getvalue())
    file_size_kb = file_size_bytes / 1024

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size_kb:.2f}KB ")

    #直接这样写，如果文件正确可以正常打开，若是文件不是utf-8编码的会导致报错影响系统正常运行，所以这种写法不建议
    #get_value
    # text = uploader_file.getvalue().decode("utf-8")       #字节数组
    # st.write(text)

    try:
        # 尝试UTF-8解码
        text = uploader_file.getvalue().decode("utf-8")
        st.text_area("文件内容", text, height=300)
    except UnicodeDecodeError:
        st.error("文件编码不是UTF-8，请使用UTF-8编码的TXT文件")

    with st.spinner("载入知识库中。。。"):     #执行过程中会有一个转圈动画
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)
    
 
