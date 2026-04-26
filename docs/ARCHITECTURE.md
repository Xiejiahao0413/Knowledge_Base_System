# Architecture

## Overview

The refactored project now follows a layered structure:

- `src/config`: typed configuration and logging bootstrap
- `src/core`: external integrations such as embeddings, LLM, and vector store
- `src/rag`: prompt templates, retrieval formatting, and chain assembly
- `src/services`: document ingestion, knowledge base management, chat orchestration, and history persistence
- `src/api`: FastAPI routes and middleware
- `src/web`: Streamlit UI pages and components
- `tests`: unit tests for service-layer behavior

## Request Flow

1. A document is uploaded from Streamlit or FastAPI.
2. `DocumentService` decodes bytes and normalizes metadata.
3. `KnowledgeService` handles fingerprint deduplication, chunking, and vector-store persistence.
4. `ChatService` invokes the RAG chain, which retrieves context from Chroma and merges it with file-based conversation history.

## Design Decisions

- Business logic is isolated from UI entrypoints.
- Runtime settings are centralized in `src/config/settings.py`.
- Legacy entrypoints remain available through compatibility wrappers at the repository root.
- The current implementation stays compatible with the existing environment while preparing the codebase for stronger API, deployment, and testing workflows.

