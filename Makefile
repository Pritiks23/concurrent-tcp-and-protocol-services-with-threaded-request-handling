PYTHON ?= python3

.PHONY: run test lint format

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest

lint:
	ruff check app tests

format:
	ruff check --fix app tests
