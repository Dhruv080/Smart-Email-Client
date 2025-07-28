#!/usr/bin/env python3
"""Validation script to ensure the setup is complete and working."""

import sys
import subprocess
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (missing)")
        return False


def run_command(command, description):
    """Run a command and report status."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description}: Command timed out")
        return False
    except Exception as e:
        print(f"❌ {description}: {e}")
        return False


def main():
    """Main validation function."""
    print("🔍 Validating Smart Email Client Setup")
    print("=" * 50)
    
    all_good = True
    
    # Check core files
    print("\n📁 Checking project structure...")
    files_to_check = [
        ("pyproject.toml", "Root project configuration"),
        ("README.md", "Project README"),
        ("src/mail_client_interface/pyproject.toml", "Interface package config"),
        ("src/gmail_implementation/pyproject.toml", "Gmail package config"),
        ("src/mail_client_interface/src/mail_client_interface/models.py", "Interface models"),
        ("src/mail_client_interface/src/mail_client_interface/protocols.py", "Interface protocols"),
        ("src/mail_client_interface/src/mail_client_interface/exceptions.py", "Interface exceptions"),
        ("src/gmail_implementation/src/gmail_implementation/client.py", "Gmail client"),
        ("src/gmail_implementation/src/gmail_implementation/auth.py", "Gmail auth"),
        ("src/gmail_implementation/src/gmail_implementation/transformer.py", "Gmail transformer"),
        (".circleci/config.yml", "CI/CD configuration"),
        ("docs/index.md", "Documentation"),
        ("ruff.toml", "Ruff configuration"),
        ("mypy.ini", "Mypy configuration"),
        ("mkdocs.yml", "MkDocs configuration"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check tool commands
    print("\n🛠️  Checking tool availability...")
    tools_to_check = [
        ("uv --version", "uv package manager"),
        ("uv run ruff --version", "ruff formatter/linter"),
        ("uv run mypy --version", "mypy type checker"),
        ("uv run pytest --version", "pytest testing framework"),
        ("uv run mkdocs --version", "mkdocs documentation"),
    ]
    
    for command, description in tools_to_check:
        if not run_command(command, description):
            all_good = False
    
    # Check code quality
    print("\n📝 Checking code quality...")
    quality_checks = [
        ("uv run ruff check . --quiet", "Ruff linting"),
        ("uv run ruff format --check . --quiet", "Ruff formatting"),
        ("uv run mypy src/ --quiet", "Mypy type checking"),
    ]
    
    for command, description in quality_checks:
        if not run_command(command, description):
            all_good = False
    
    # Check tests can run
    print("\n🧪 Checking test execution...")
    if not run_command("uv run pytest --collect-only -q", "Test collection"):
        all_good = False
    
    # Check documentation build
    print("\n📚 Checking documentation build...")
    if not run_command("uv run mkdocs build --quiet", "Documentation build"):
        all_good = False
    
    # Final report
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 Setup validation PASSED!")
        print("✨ Your Smart Email Client is ready for development!")
        print("\n💡 Next steps:")
        print("   1. Add your Gmail credentials.json file")
        print("   2. Run: uv run python example_cli.py")
        print("   3. Start developing your features!")
    else:
        print("⚠️  Setup validation FAILED!")
        print("🔧 Please fix the issues above before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
