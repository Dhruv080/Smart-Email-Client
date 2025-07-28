#!/bin/bash
# Documentation building and serving script

set -e

echo "📚 Building documentation..."

# Build docs
uv run mkdocs build

echo "✅ Documentation built successfully!"
echo "📁 Static files available in site/"
echo ""
echo "🌐 To serve locally:"
echo "   uv run mkdocs serve"
echo ""
echo "🚀 To deploy to GitHub Pages:"
echo "   uv run mkdocs gh-deploy"
