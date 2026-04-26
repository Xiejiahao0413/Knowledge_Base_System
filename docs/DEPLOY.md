# Deploy

## Local

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements/base.txt`.
3. Configure `.env` based on `.env.example`.
4. Start Streamlit with `streamlit run app.py`.
5. Start FastAPI with `uvicorn src.api.app:app --reload`.

## Docker

Use the files under `docker/` as a base image and compose template. The default deployment mounts `chroma_db`, `chat_history`, and `data` as persistent volumes.

