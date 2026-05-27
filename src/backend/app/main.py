"""FastAPI application entrypoint.

Run locally:
  pip install -r requirements.txt
  uvicorn app.main:app --reload --port 8000

Swagger UI:
  http://localhost:8000/docs
"""

from app import app  # re-export for uvicorn
