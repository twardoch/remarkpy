# Makefile for remarkpy

.PHONY: help install install-dev clean build test lint format check-format
.PHONY: js-build js-clean py-build py-clean
.PHONY: release-patch release-minor release-major
.PHONY: test-release docs clean-all

# Default target
help:
	@echo "Available targets:"
	@echo "  help           - Show this help message"
	@echo "  install        - Install package in development mode"
	@echo "  install-dev    - Install package with development dependencies"
	@echo "  clean          - Clean build artifacts"
	@echo "  build          - Build JavaScript bundle and Python package"
	@echo "  js-build       - Build JavaScript bundle only"
	@echo "  py-build       - Build Python package only"
	@echo "  test           - Run test suite"
	@echo "  lint           - Run linting (ruff)"
	@echo "  format         - Format code with black"
	@echo "  check-format   - Check code formatting without fixing"
	@echo "  binary         - Build standalone binary"
	@echo "  binary-clean   - Clean binary build artifacts"
	@echo "  release-patch  - Create patch release"
	@echo "  release-minor  - Create minor release"
	@echo "  release-major  - Create major release"
	@echo "  test-release   - Create test release to Test PyPI"
	@echo "  docs           - Build documentation"
	@echo "  clean-all      - Clean all build artifacts and caches"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e .[dev]

# Build targets
build:
	python scripts/build.py

js-build:
	python scripts/build.py --js-only

py-build:
	python scripts/build.py --py-only

# JavaScript specific targets
js-clean:
	rm -rf remarkpyjs/node_modules
	rm -f remarkpy/remarkpy.js

js-deps:
	cd remarkpyjs && npm install

js-bundle:
	cd remarkpyjs && npm run build

# Python specific targets
py-clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/

# Test targets
test:
	python -m pytest -v

test-cov:
	python -m pytest -v --cov=remarkpy --cov-report=html --cov-report=term

test-fast:
	python -m pytest -v -x

# Code quality targets
lint:
	python -m ruff check remarkpy tests scripts

lint-fix:
	python -m ruff check --fix remarkpy tests scripts

format:
	python -m black remarkpy tests scripts

check-format:
	python -m black --check remarkpy tests scripts

mypy:
	python -m mypy remarkpy

# Binary targets
binary:
	python scripts/build_binary.py

binary-clean:
	python scripts/build_binary.py --clean

# Release targets
release-patch:
	python scripts/release.py patch

release-minor:
	python scripts/release.py minor

release-major:
	python scripts/release.py major

test-release:
	python scripts/release.py patch --test-pypi

# Documentation targets
docs:
	@echo "Documentation generation not yet implemented"

# Clean targets
clean: py-clean
	rm -rf temp/

clean-all: clean js-clean
	rm -rf remarkpy/_version.py

# Development workflow targets
dev-setup: install-dev js-deps
	@echo "Development environment setup complete"

check: check-format lint mypy test
	@echo "All checks passed!"

# CI/CD simulation
ci: dev-setup check build
	@echo "CI pipeline simulation complete"

# Quick development cycle
dev: format lint test
	@echo "Development cycle complete"