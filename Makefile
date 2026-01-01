.PHONY: help install install-dev test test-cov lint format type-check clean build

help:
	@echo "Available commands:"
	@echo "  make install       Install production dependencies"
	@echo "  make install-dev   Install development dependencies"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage"
	@echo "  make lint          Run linting checks"
	@echo "  make format        Format code with black and isort"
	@echo "  make type-check    Run type checking with mypy"
	@echo "  make clean         Clean build artifacts"
	@echo "  make build         Build package"

install:
	poetry install --no-dev

install-dev:
	poetry install

test:
	poetry run pytest -v

test-cov:
	poetry run pytest -v --cov=src/agents --cov-report=html --cov-report=term

lint:
	poetry run flake8 src/agents tests
	poetry run black --check src/agents tests
	poetry run isort --check-only src/agents tests

format:
	poetry run black src/agents tests
	poetry run isort src/agents tests

type-check:
	poetry run mypy src/agents --ignore-missing-imports

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

build: clean
	poetry build

publish: build
	poetry publish

ci: install-dev lint type-check test-cov
	@echo "CI checks passed!"
