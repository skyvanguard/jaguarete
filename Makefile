.PHONY: help setup test fmt lint clean

help:
	@echo "Jaguarete - AI-Powered Purple Team Platform"
	@echo ""
	@echo "Commands:"
	@echo "  make setup    - Install dependencies"
	@echo "  make test     - Run tests"
	@echo "  make fmt      - Format code"
	@echo "  make lint     - Check code style"
	@echo "  make clean    - Clean build artifacts"

setup:
	uv sync

test:
	uv run pytest packages/ -v

fmt:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff check .
	uv run ruff format --check .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
