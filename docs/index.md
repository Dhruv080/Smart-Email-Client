# Smart Email Client

Welcome to the Smart Email Client documentation! This system demonstrates clean architecture principles through a component-based mail client that separates interface definitions from implementation details.

## Overview

The Smart Email Client is designed around the principle of separating "what you can do" from "how you do it." This creates a system that passes the "forklift test" - you can replace the Gmail implementation with any other email provider without changing the interface code.

## Key Features

- **Clean Architecture**: Clear separation between interface and implementation
- **Type Safety**: Comprehensive type hints throughout the codebase
- **Modern Tooling**: Uses uv, ruff, mypy, pytest, and mkdocs
- **Robust Testing**: High test coverage with meaningful tests
- **Professional Documentation**: Complete setup and usage guides

## Quick Start

1. [Set up the project](setup.md)
2. [Learn how to use it](usage.md)
3. [Understand the architecture](architecture.md)

## Components

### Mail Client Interface
Defines the contract for mail client operations without any provider-specific dependencies.

### Gmail Implementation
Provides Gmail-specific functionality that fulfills the mail client interface contract.
