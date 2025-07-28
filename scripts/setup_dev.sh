#!/bin/bash
# Development environment setup script

set -e

echo "🔧 Setting up development environment..."

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Setup workspace
echo "📦 Installing dependencies..."
uv sync --all-extras

# Setup pre-commit hooks (if available)
if command -v pre-commit &> /dev/null; then
    uv run pre-commit install
fi

echo "✅ Development environment ready!"
echo "💡 Next steps:"
echo "  1. Add your Gmail credentials.json file"
echo "  2. Run tests: uv run pytest"
echo "  3. Try the example: uv run python example_cli.py"
