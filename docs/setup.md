# Setup Guide

## Prerequisites

- Python 3.10 or higher
- Gmail account with API access
- Git (for version control)

## Step 1: Install uv

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to your PATH (restart terminal or source your shell config)
export PATH="$HOME/.cargo/bin:$PATH"
```

## Step 2: Clone and Setup Project

```bash
# Clone your repository
git clone <your-repo-url>
cd smart-email-client

# Install dependencies and setup workspace
uv sync --all-extras
```

## Step 3: Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application"
   - Download the JSON file
5. Save the downloaded file as `credentials.json` in your project root

## Step 4: Verify Setup

```bash
# Run tests to verify everything works
uv run pytest

# Check code quality
uv run ruff check .
uv run mypy src/

# Build documentation
uv run mkdocs build
```

## Troubleshooting

### Common Issues

**uv not found**: Make sure uv is installed and in your PATH
**Credentials error**: Ensure `credentials.json` is in the project root
**Import errors**: Run `uv sync --all-extras` to install dependencies
**Test failures**: Check that Gmail API is enabled in Google Cloud Console

### Getting Help

1. Check the [Usage Guide](usage.md)
2. Review the [Architecture Documentation](architecture.md)
3. Look at test files for usage examples
