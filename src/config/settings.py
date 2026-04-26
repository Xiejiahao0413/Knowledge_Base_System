"""Typed application settings loaded from YAML and environment variables."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from src.utils.exceptions import ConfigurationError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = Path(__file__).with_name("config.yaml")


class AppConfig(BaseModel):
    name: str = "Knowledge Base System"
    environment: str = "development"


class PathConfig(BaseModel):
    chroma_db: str = "chroma_db"
    chat_history: str = "chat_history"
    data: str = "data"
    md5_registry: str = "md5.text"
    logs_dir: str = "logs"


class LoggingConfig(BaseModel):
    level: str = "INFO"
    file_name: str = "app.log"


class ModelConfig(BaseModel):
    embedding: str = "text-embedding-v4"
    chat: str = "qwen3-max"


class RagConfig(BaseModel):
    collection_name: str = "rag"
    chunk_size: int = 1000
    chunk_overlap: int = 100
    max_split_char_number: int = 1000
    retrieval_k: int = 2
    separators: list[str] = Field(
        default_factory=lambda: [
            "\n\n",
            "\n",
            ",",
            ".",
            "?",
            "!",
            "，",
            "。",
            "！",
            "？",
            "",
        ]
    )


class SessionConfig(BaseModel):
    default_session_id: str = "user_001"


class SecurityConfig(BaseModel):
    api_key_header: str = "X-API-Key"
    api_key: str | None = None


class AppSettings(BaseModel):
    app: AppConfig = Field(default_factory=AppConfig)
    paths: PathConfig = Field(default_factory=PathConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    models: ModelConfig = Field(default_factory=ModelConfig)
    rag: RagConfig = Field(default_factory=RagConfig)
    session: SessionConfig = Field(default_factory=SessionConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)

    def resolve_path(self, relative_or_absolute: str) -> Path:
        path = Path(relative_or_absolute)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path

    @property
    def chroma_db_path(self) -> Path:
        return self.resolve_path(self.paths.chroma_db)

    @property
    def chat_history_path(self) -> Path:
        return self.resolve_path(self.paths.chat_history)

    @property
    def data_path(self) -> Path:
        return self.resolve_path(self.paths.data)

    @property
    def md5_registry_path(self) -> Path:
        return self.resolve_path(self.paths.md5_registry)

    @property
    def logs_dir_path(self) -> Path:
        return self.resolve_path(self.paths.logs_dir)

    @property
    def log_file_path(self) -> Path:
        return self.logs_dir_path / self.logging.file_name

    def session_config(self, session_id: str | None = None) -> dict[str, dict[str, str]]:
        return {
            "configurable": {
                "session_id": session_id or self.session.default_session_id,
            }
        }

    @classmethod
    def load(cls, config_path: Path | None = None) -> "AppSettings":
        config_file = config_path or DEFAULT_CONFIG_PATH
        if not config_file.exists():
            raise ConfigurationError(f"Config file not found: {config_file}")

        raw_data = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
        settings = cls.model_validate(raw_data)
        merged_data = settings.model_dump()
        merged_data.update(_load_environment_overrides(settings))
        return cls.model_validate(merged_data)


def _load_environment_overrides(settings: AppSettings) -> dict[str, Any]:
    env_map = {
        "KBS_APP_ENV": ("app", "environment"),
        "KBS_CHROMA_DB_DIR": ("paths", "chroma_db"),
        "KBS_CHAT_HISTORY_DIR": ("paths", "chat_history"),
        "KBS_DATA_DIR": ("paths", "data"),
        "KBS_MD5_REGISTRY_PATH": ("paths", "md5_registry"),
        "KBS_LOG_LEVEL": ("logging", "level"),
        "KBS_LOG_FILE_NAME": ("logging", "file_name"),
        "KBS_EMBEDDING_MODEL": ("models", "embedding"),
        "KBS_CHAT_MODEL": ("models", "chat"),
        "KBS_COLLECTION_NAME": ("rag", "collection_name"),
        "KBS_CHUNK_SIZE": ("rag", "chunk_size"),
        "KBS_CHUNK_OVERLAP": ("rag", "chunk_overlap"),
        "KBS_MAX_SPLIT_CHAR_NUMBER": ("rag", "max_split_char_number"),
        "KBS_RETRIEVAL_K": ("rag", "retrieval_k"),
        "KBS_DEFAULT_SESSION_ID": ("session", "default_session_id"),
        "KBS_API_KEY": ("security", "api_key"),
        "KBS_API_KEY_HEADER": ("security", "api_key_header"),
    }
    overrides: dict[str, dict[str, Any]] = {}
    for env_name, (section, key) in env_map.items():
        env_value = os.getenv(env_name)
        if env_value in (None, ""):
            continue

        current_section = getattr(settings, section).model_dump()
        current_value = current_section.get(key)
        if isinstance(current_value, int):
            current_section[key] = int(env_value)
        else:
            current_section[key] = env_value
        overrides[section] = current_section
    return overrides


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings.load()
