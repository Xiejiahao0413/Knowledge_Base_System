"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI

from src.api.middleware.logging import RequestLoggingMiddleware
from src.api.routes.chat import router as chat_router
from src.api.routes.documents import router as documents_router
from src.api.routes.knowledge import router as knowledge_router
from src.config.logging_config import configure_logging
from src.config.settings import get_settings
from src.models.schemas import HealthResponse

settings = get_settings()
configure_logging(settings)
app = FastAPI(title=settings.app.name)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(knowledge_router)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app=settings.app.name,
        environment=settings.app.environment,
    )
