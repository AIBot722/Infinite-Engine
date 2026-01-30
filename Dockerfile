FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m appuser

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY content /app/content

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "dungeon_engine.server.app:app", "--host", "0.0.0.0", "--port", "8000"]
