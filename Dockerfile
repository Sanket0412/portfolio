# API image for Railway (build context = repo root so content/ ships with the API).
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

# Editable install keeps API_ROOT/REPO_ROOT resolving to /app/api and /app (content/ lives there).
COPY api ./api
COPY content ./content
RUN pip install -e ./api

EXPOSE 8000
CMD ["sh", "-c", "uvicorn portfolio_api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
