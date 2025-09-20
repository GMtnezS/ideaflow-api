FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# your package is called api/
COPY api ./api

ENV PORT=8080
EXPOSE 8080
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080}
