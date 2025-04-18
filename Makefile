.PHONY: install format lint type-check security-check check clean

install:
	uv pip install -e ".[dev]"
	uvx pre-commit install

format:
	uvx ruff format .

lint:
	uvx ruff check . --fix

type-check:
	uvx --with pydantic,types-PyYAML,types-click mypy src/drtail_prompt

security-check:
	uvx bandit -r src/drtail_prompt

check: format lint type-check security-check

test:
	uv run python -m pytest tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
