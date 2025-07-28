# Usage Guide

## Basic Usage

The Smart Email Client provides a clean interface for reading Gmail messages. Here's how to use it:

### Authentication

```python
from gmail_implementation.client import GmailClient

# Create client (credentials.json must be in project root)
client = GmailClient()

# Authenticate with Gmail
client.authenticate()  # Opens browser for OAuth flow
```

### Reading Email List

```python
# Get recent emails
emails, next_token = client.get_email_list(max_results=10)

# Display email summaries
for email in emails:
    print(f"From: {email.sender}")
    print(f"Subject: {email.subject}")
    print(f"Date: {email.date}")
    print(f"Status: {email.status.value}")
    print("-" * 40)
```

### Reading Individual Emails

```python
# Get detailed email content
email_detail = client.get_email_detail(emails[0].message_id)

print(f"From: {email_detail.sender}")
print(f"To: {', '.join(str(addr) for addr in email_detail.recipients)}")
print(f"Subject: {email_detail.subject}")
print(f"Date: {email_detail.date}")
print("\nBody:")
print(email_detail.body_text or email_detail.body_html)

# Check for attachments
if email_detail.attachments:
    print(f"\nAttachments ({len(email_detail.attachments)}):")
    for attachment in email_detail.attachments:
        print(f"  - {attachment.filename} ({attachment.size_bytes} bytes)")
```

### Error Handling

```python
from mail_client_interface.exceptions import (
    AuthenticationError, ConnectionError, ServiceError, EmailNotFoundError
)

try:
    client.authenticate()
    emails, _ = client.get_email_list()
    
except AuthenticationError:
    print("Authentication failed. Check credentials.json")
except ConnectionError:
    print("Network connection problem")
except ServiceError as e:
    print(f"Gmail service error: {e}")
```

## Command Line Interface

Create a simple CLI script:

```python
#!/usr/bin/env python3
"""Simple Gmail reader CLI."""

import sys
from gmail_implementation.client import GmailClient

def main():
    client = GmailClient()
    
    try:
        print("Authenticating with Gmail...")
        client.authenticate()
        
        print("Fetching recent emails...")
        emails, _ = client.get_email_list(max_results=5)
        
        for i, email in enumerate(emails, 1):
            print(f"\n{i}. {email.subject}")
            print(f"   From: {email.sender}")
            print(f"   Date: {email.date.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Preview: {email.snippet[:100]}...")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Testing Your Implementation

```bash
# Run all tests
uv run pytest

# Run specific test files
uv run pytest src/mail_client_interface/tests/
uv run pytest src/gmail_implementation/tests/

# Generate coverage report
uv run pytest --cov=src --cov-report=html
```
