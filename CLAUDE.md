# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

brunns-matchers is a Python library providing custom [PyHamcrest](https://pyhamcrest.readthedocs.io) matchers for testing. It extends PyHamcrest with specialized matchers for HTML, HTTP responses, database APIs, URLs, dates, RSS feeds, and more.

## Package Management

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and build tooling. All dependencies are defined in `pyproject.toml`.

### Installing Dependencies

- **Install all dependencies**: `uv sync --all-extras`
- **Update lock file**: `uv lock`
- **Add a dependency**: Edit `pyproject.toml` dependencies, then run `uv sync`

## Development Commands

### Testing
- **Run tests**: `uv run pytest` or `make test`
- **Run single test**: `uv run pytest tests/unit/matchers/test_datetime.py::test_name -v`
- **Run coverage**: `uv run pytest --cov=src/brunns/matchers --cov-report=term-missing` or `make coverage`
  - Coverage requirement is 100% (enforced in CI)
- **Integration tests**: Tests in `tests/integration/` may require Docker via colima (`make colima`)

### Code Quality
- **Format code**: `uv run ruff format . && uv run ruff check . --fix` or `make format`
  - Uses ruff for formatting and auto-fixing
- **Check formatting**: `uv run ruff format . --check && uv run ruff check .` or `make check-format`
  - Runs ruff formatter and linter checks
- **Type checking**: `uv run mypy src/ --ignore-missing-imports` or `make mypy`
  - Uses mypy with settings in pyproject.toml
- **Security scanning**: `uv run bandit -r src/` or `make bandit`
  - Uses bandit to detect security issues
- **Pre-commit checks**: `make precommit`
  - Runs tests, lint, coverage, mypy, and docs

### Documentation
- **Build docs**: `uv run sphinx-build docs build_docs --color -W -bhtml` or `make docs`
  - Uses Sphinx with furo theme
  - Output in `build_docs/`

### Other
- **Check outdated deps**: `uv pip list --outdated` or `make piprot`
- **Python REPL**: `uv run python` or `make repl`
- **Clean build artifacts**: `make clean`
- **Mutation testing**: `make mutmut`
  - Runs mutmut to test test quality

## Building and Publishing

### Building Packages

- **Build wheel and sdist**: `uv build`
  - Output in `dist/`

### Manual Publishing (Not Recommended)

Manual publishing to PyPI is discouraged. Use the automated release workflow instead (see Release Process below).

If you must publish manually:
```bash
uv build
uv run twine upload dist/*
```

## Release Process

Releases are automated via GitHub Actions when a version tag is pushed.

### Steps to Release

1. **Update version** in `pyproject.toml` (line 7)
2. **Run pre-commit checks**: `make precommit`
3. **Commit changes**: `git commit -am "Release vX.Y.Z"`
4. **Create and push tag**:
   ```bash
   git tag vX.Y.Z
   git push origin master --tags
   ```

### What Happens Automatically

When a tag matching `v*.*.*` is pushed:

1. **Build job**: Installs dependencies, runs tests, checks coverage, builds distribution packages
2. **PyPI publishing**: Automatically publishes to PyPI using OIDC trusted publishing (no API keys needed)
3. **GitHub release**: Creates a GitHub release with auto-generated notes and uploads distribution artifacts

### Setting Up PyPI Trusted Publishing

If not already configured, set up trusted publishing at https://pypi.org/manage/project/brunns-matchers/settings/publishing/:

- PyPI Project Name: `brunns-matchers`
- Owner: `brunns`
- Repository: `brunns-matchers`
- Workflow: `release.yml`
- Environment: `pypi`

Also create a GitHub environment named "pypi" in the repository settings.

## Tool Preferences

- **JSON parsing**: Use `jq` instead of `python -c` for parsing JSON output
- **Python tool & package management**: Use `uv` and `uvx` where appropriate.
- **Command-line tools**: Prefer standard Unix tools when available

## Architecture

### Matcher Design Pattern

All matchers inherit from PyHamcrest's `BaseMatcher` and follow this pattern:

1. **Initialization**: Accept expected values or sub-matchers as constructor arguments
2. **`_matches(self, actual)`**: Return True/False for match result
3. **`describe_to(self, description)`**: Describe what the matcher expects
4. **`describe_mismatch(self, actual, description)`**: Explain why a value didn't match

Many matchers support a **fluent builder API** pattern (e.g., `is_response().with_status_code(200).with_json(...)`) where each method returns `self` for chaining.

### Matcher Categories

Each matcher type has its own module in `src/brunns/matchers/`:

- **response.py**: HTTP response matchers (`is_response()`) for `requests.Response` and `httpx.Response`
- **html.py**: HTML/BeautifulSoup matchers for tags, attributes, text content
- **url.py**: URL matchers for `furl`, `yarl.URL`, and `urllib.parse.ParseResult`
- **object.py**: Object property/attribute comparison matchers
- **datetime.py**: Date/time matchers with tolerance support
- **data.py**: JSON and data structure matchers
- **dbapi.py**: DB-API 2.0 result set matchers
- **mock.py**: Mock call matchers
- **rss.py**: RSS feed matchers
- **smtp.py**: SMTP email matchers
- **werkzeug.py**: Werkzeug response matchers
- **matcher.py**: Meta-matchers for testing matchers themselves (`mismatches_with()`, `matches_with()`)
- **meta.py**: `BaseAutoMatcher` metaclass for auto-generating matchers from dataclasses/typed classes
- **utils.py**: Shared utilities for description formatting

### Test Organization

- **Unit tests**: `tests/unit/matchers/` - one file per matcher module
- **Integration tests**: `tests/integration/matchers/` - tests requiring external services (Docker)
- **Test utilities**: `tests/utils/` - helpers like `network.py` for network checks

### Source Layout

The project uses a `src/` layout:
- Source: `src/brunns/matchers/`
- This is a namespace package (no `__init__.py` in `src/brunns/`)
- `py.typed` marker indicates type hints are available

## Coding Conventions

- **Type hints**: All code uses modern type annotations (Python 3.10+)
- **Ruff config**: Line length 120, `select = ["ALL"]` with specific ignores in `pyproject.toml`
- **Max complexity**: 5 (enforced by ruff's mccabe)
- **Docstrings**: Use reStructuredText format for Sphinx autodoc
- **Deprecated code**: Use `@deprecated` decorator from deprecated library

## Version Management

Version is defined in `pyproject.toml` (line 7). When releasing, update this version and follow the release process above.
