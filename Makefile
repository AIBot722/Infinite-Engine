VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

install:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev]

fmt:
	$(VENV)/bin/ruff format .

lint:
	$(VENV)/bin/ruff check .

test:
	$(VENV)/bin/pytest

run:
	$(VENV)/bin/uvicorn dungeon_engine.server.app:app --host 0.0.0.0 --port 8000
