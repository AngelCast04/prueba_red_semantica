FROM python:3.12.8-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GRAPH_WORKING_DIR=./grafo_libros \
    CONCURRENT_TASK_LIMIT=4

WORKDIR /app

# Dependencias base para compilar ruedas cuando haga falta.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Mantiene el mismo flujo de Render: upgrade de herramientas + requirements.
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt

# Código necesario para ejecutar el backend FastAPI.
COPY app /app/app
COPY fast_graphrag /app/fast_graphrag
COPY grafo_libros /app/grafo_libros
COPY pyproject.toml /app/pyproject.toml
COPY README.md /app/README.md

EXPOSE 8000

# OPENAI_API_KEY debe inyectarse en runtime, igual que en Render (sync: false).
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
