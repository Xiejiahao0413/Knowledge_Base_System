"""General-purpose helpers."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from src.utils.exceptions import UnsupportedEncodingError


def compute_md5(content: str, encoding: str = "utf-8") -> str:
    return hashlib.md5(content.encode(encoding=encoding)).hexdigest()


def decode_text_bytes(content: bytes) -> tuple[str, str]:
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return content.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise UnsupportedEncodingError(
        "Only UTF-8/UTF-8-SIG/GB18030 encoded text files are supported."
    )


def utc_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
