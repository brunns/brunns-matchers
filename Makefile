SHELL = /bin/bash

default: help

.PHONY: sync
sync: ## Install/sync dependencies
	uv sync --all-extras

.PHONY: colima
colima: ## Start colima (for Docker-based integration tests)
	colima status || colima start

.PHONY: test
test: colima ## Run tests
	uv run pytest

.PHONY: coverage
coverage: colima ## Test coverage report
	uv run pytest --cov=src/brunns/matchers --cov-report=term-missing --cov-report=html

.PHONY: lint
lint: check-format ## Lint code

.PHONY: extra-lint
extra-lint: mypy bandit  ## Extra, optional linting

.PHONY: mypy
mypy: ## Type check with mypy
	uv run mypy src/ --ignore-missing-imports

.PHONY: bandit
bandit: ## Security check with bandit
	uv run bandit -r src/

.PHONY: check-format
check-format: ## Check code formatting
	uv run ruff format . --check
	uv run ruff check .

.PHONY: format
format: ## Format code
	uv run ruff format .
	uv run ruff check . --fix

.PHONY: piprot
piprot: ## Check for outdated dependencies
	uv pip list --outdated

.PHONY: mutmut
mutmut: clean ## Run mutation tests
	uv run mutmut run
	uv run mutmut html
	open html/index.html

.PHONY: docs
docs: ## Generate documentation
	uv run sphinx-build docs build_docs --color -W -bhtml

.PHONY: build
build: ## Build distribution packages
	uv build

.PHONY: publish
publish: build ## Publish to PyPI (use release workflow instead)
	@echo "WARNING: Manual publishing is not recommended. Use the automated release workflow instead."
	@echo "To release: update version in pyproject.toml, commit, tag with 'v*.*.*', and push the tag."
	@read -p "Continue with manual publish? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		uv run twine upload dist/*; \
	fi

.PHONY: precommit
precommit: test lint coverage mypy docs ## Pre-commit targets
	@ python -m this

.PHONY: clean
clean: ## Clean generated files
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	rm -rf build/ dist/ *.egg-info/ .cache .coverage .pytest_cache  *.svg  .mutmut-cache html/
	find . -name "__pycache__" -type d -print | xargs -t rm -r
	find . -name "test-output" -type d -print | xargs -t rm -r

.PHONY: repl
repl: ## Python REPL
	uv run python

.PHONY: outdated
outdated: ## List outdated dependencies
	uv pip list --outdated

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1,$$2}'
