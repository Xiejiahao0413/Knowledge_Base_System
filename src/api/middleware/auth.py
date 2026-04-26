"""Authentication helpers for API routes."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status

from src.config.settings import AppSettings, get_settings


def require_api_key(
    request: Request,
    settings: AppSettings = Depends(get_settings),
) -> None:
    expected_api_key = settings.security.api_key
    if not expected_api_key:
        return

    provided_api_key = request.headers.get(settings.security.api_key_header)
    if provided_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )

