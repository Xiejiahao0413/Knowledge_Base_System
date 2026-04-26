#!/usr/bin/env bash
set -euo pipefail

pip install -r requirements/prod.txt
python scripts/init_db.py
uvicorn src.api.app:app --host 0.0.0.0 --port 8000

