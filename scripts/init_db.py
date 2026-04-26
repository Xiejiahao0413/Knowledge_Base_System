"""Initialize runtime directories for the project."""

from __future__ import annotations

from src.config.settings import get_settings


def main() -> None:
    settings = get_settings()
    settings.chroma_db_path.mkdir(parents=True, exist_ok=True)
    settings.chat_history_path.mkdir(parents=True, exist_ok=True)
    settings.data_path.mkdir(parents=True, exist_ok=True)
    settings.logs_dir_path.mkdir(parents=True, exist_ok=True)
    settings.md5_registry_path.touch(exist_ok=True)
    print("Runtime directories initialized.")


if __name__ == "__main__":
    main()

