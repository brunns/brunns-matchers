SHELL = /bin/bash

default: help
.PHONY: help test coverage flake8 bandit safety check-format format piprot precommit clean repl outdated

test: ## Run tests
	tox -e py27,py37

test-all-versions: ## Test against all available python versions
	tox

coverage: ## Test coverage report
	tox -e coverage

lint: check-format flake8 bandit safety ## Lint code

flake8:
	tox -e flake8

bandit:
	tox -e bandit

safety:
	tox -e safety

check-format:
	tox -e check-format

format: ## Format code
	tox -e format

piprot: ## Check for outdated dependencies
	tox -e piprot

precommit: test lint coverage ## Pre-commit targets
	@ python -m this

clean: ## Clean generated files
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	rm -rf build/ dist/ *.egg-info/ .cache .coverage .pytest_cache
	find . -name "__pycache__" -type d -print | xargs -t rm -r
	find . -name "test-output" -type d -print | xargs -t rm -r

repl: ## Python REPL
	tox -e py36 -- python

outdated: ## List outdated dependancies
	tox -e py36 -- pip list --outdated

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1,$$2}'
