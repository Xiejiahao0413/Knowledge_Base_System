"""Legacy compatibility module for the refactored settings layer."""

from src.config.settings import get_settings

_settings = get_settings()

md5_path = str(_settings.md5_registry_path)
collection_name = _settings.rag.collection_name
persist_directory = str(_settings.chroma_db_path)
chunk_size = _settings.rag.chunk_size
chunk_overlap = _settings.rag.chunk_overlap
separators = _settings.rag.separators
max_split_char_number = _settings.rag.max_split_char_number
similary_thredshold = _settings.rag.retrieval_k
embedding_model_name = _settings.models.embedding
chat_model_name = _settings.models.chat
session_config = _settings.session_config()
