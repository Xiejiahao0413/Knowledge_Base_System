"""Centralized logging configuration."""

from __future__ import annotations

import logging

from src.config.settings import AppSettings


def configure_logging(settings: AppSettings) -> None:
    settings.logs_dir_path.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    logging.basicConfig(
        level=getattr(logging, settings.logging.level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(settings.log_file_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

