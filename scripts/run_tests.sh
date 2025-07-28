#!/bin/bash
# Comprehensive test runner script

set -e

echo "🧪 Running comprehensive test suite..."

echo "1️⃣  Running ruff format check..."
uv run ruff format --check .

echo "2️⃣  Running ruff lint..."
uv run ruff check .

echo "3️⃣  Running mypy type checking..."
uv run mypy src/

echo "4️⃣  Running pytest with coverage..."
uv run pytest --cov=src --cov-report=html --cov-report=term-missing

echo "5️⃣  Building documentation..."
uv run mkdocs build

echo "✅ All checks passed!"
echo "📊 Coverage report available in htmlcov/index.html"
echo "📚 Documentation built in site/"
