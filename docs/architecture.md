# Architecture Guide

## Design Principles

The Smart Email Client is built around several key architectural principles:

### 1. Interface Segregation
The system separates "what you can do" (interface) from "how you do it" (implementation). This allows for:
- Easy testing with mocks
- Swapping implementations without changing client code
- Clear contracts between components

### 2. Dependency Injection
The Gmail implementation injects itself into the interface at runtime, allowing for flexible configuration and testing.

### 3. Type Safety
Comprehensive type hints throughout the codebase provide:
- Better IDE support
- Early error detection
- Self-documenting code

## Component Overview

```
┌─────────────────────────────────────┐
│           Client Code               │
│  (Uses MailClientProtocol)          │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│      Mail Client Interface          │
│  • EmailSummary, EmailDetail        │
│  • MailClientProtocol               │
│  • Exceptions                       │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│      Gmail Implementation           │
│  • GmailClient                      │
│  • GmailAuthenticator               │
│  • GmailTransformer                 │
└─────────────────────────────────────┘
```

## The Forklift Test

The architecture passes the "forklift test" - you can replace Gmail with another provider:

```python
# Current implementation
client = GmailClient()

# Hypothetical future implementation
client = OutlookClient()  # Same interface!

# Client code remains unchanged
client.authenticate()
emails, _ = client.get_email_list()
```

This is achieved through:
- Zero Gmail dependencies in the interface
- Protocol-based design
- Consistent error handling
- Standard data models
