# Development Guide for Dr.Tail Prompt

This guide will help you set up your development environment and understand the development workflow for Dr.Tail Prompt.

## Prerequisites

- Python 3.8 or higher
- Git
- A code editor (VS Code recommended)
- [uv](https://github.com/astral-sh/uv) for dependency management (recommended)

## Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dr-tail-prompt.git
cd dr-tail-prompt
```

2. Create and activate a virtual environment:
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

## Development Workflow

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Description of your changes"
```

3. Push your changes and create a pull request:
```bash
git push origin feature/your-feature-name
```

## Code Style and Quality

We use several tools to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Linting and code analysis
- **pytest**: Testing
- **mypy**: Type checking

Run the quality checks:
```bash
# Format code
black .

# Run linter
ruff check .

# Run type checker
mypy .

# Run tests
pytest
```

## Testing

We use pytest for testing. Write tests in the `tests/` directory:

```python
# tests/test_prompt.py
def test_prompt_creation():
    prompt = Prompt(name="test", description="test prompt")
    assert prompt.name == "test"
```

Run tests:
```bash
pytest
```

For test coverage:
```bash
pytest --cov=src
```

## Documentation

We use Sphinx for documentation. To build the docs:

```bash
cd docs
make html
```

Documentation will be available in `docs/_build/html/`.

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Build and publish to PyPI:
```bash
uv pip install build twine
python -m build
twine upload dist/*
```

## Project Structure

```
dr-tail-prompt/
├── src/
│   └── dr_tail_prompt/
│       ├── __init__.py
│       ├── prompt.py
│       └── version.py
├── tests/
│   └── test_prompt.py
├── docs/
│   └── ...
├── pyproject.toml
├── README.md
└── ...
```

## Common Issues and Solutions

### Virtual Environment Issues

If you encounter issues with the virtual environment:
```bash
# Remove existing venv
rm -rf .venv

# Create new venv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Dependency Issues

If you have dependency conflicts:
```bash
uv pip install --upgrade -e ".[dev]"
```

## Getting Help

- Check the [issue tracker](https://github.com/yourusername/dr-tail-prompt/issues)
- Join our [community chat](https://github.com/yourusername/dr-tail-prompt/discussions)
- Contact the maintainers

## Best Practices

1. Write meaningful commit messages
2. Keep PRs focused and small
3. Add tests for new features
4. Update documentation when changing APIs
5. Follow PEP 8 style guide
6. Use type hints
7. Write docstrings for public APIs
