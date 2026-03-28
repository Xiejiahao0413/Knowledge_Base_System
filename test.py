from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

embedding = DashScopeEmbeddings(model="text-embedding-v4")
vector_store = Chroma(
    collection_name=config.collection_name,
    embedding_function=embedding,
    persist_directory=config.persist_directory,
)

print(f"文档数量: {vector_store._collection.count()}")
results = vector_store.similarity_search("我的体重是180斤，尺码推荐", k=2)
print(f"检索结果数: {len(results)}")
for doc in results:
    print(doc.page_content[:200])