"""Create a timestamped backup archive of runtime data."""

from __future__ import annotations

import shutil
from datetime import UTC, datetime
from pathlib import Path

from src.config.settings import PROJECT_ROOT, get_settings


def main() -> None:
    settings = get_settings()
    backup_root = PROJECT_ROOT / "backups"
    backup_root.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    archive_base = backup_root / f"knowledge-base-backup-{timestamp}"
    workspace = PROJECT_ROOT / ".backup_tmp"
    workspace.mkdir(parents=True, exist_ok=True)

    for source_path in (
        settings.chroma_db_path,
        settings.chat_history_path,
        settings.data_path,
    ):
        if source_path.exists():
            destination = workspace / source_path.name
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(source_path, destination)

    if settings.md5_registry_path.exists():
        shutil.copy2(settings.md5_registry_path, workspace / settings.md5_registry_path.name)

    shutil.make_archive(str(archive_base), "zip", workspace)
    shutil.rmtree(workspace, ignore_errors=True)
    print(f"Backup created: {archive_base}.zip")


if __name__ == "__main__":
    main()
