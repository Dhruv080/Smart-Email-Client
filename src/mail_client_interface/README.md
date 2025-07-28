# Mail Client Interface

This package defines the core interface for a mail client system, providing clean contracts that any email provider can implement.

## Purpose

The Mail Client Interface establishes the boundary between "what you can do" and "how you do it" in email operations. It defines:

- **Data Models**: Standard structures for emails, addresses, and attachments
- **Protocols**: Interface contracts that implementations must fulfill
- **Exceptions**: Standardized error handling

## Key Principle

This interface has **zero dependencies** on any specific email provider (Gmail, Outlook, etc.). This enables the "forklift test" - you can swap email providers without changing interface code.

## Components

### Models (`models.py`)
- `EmailAddress`: Email address with optional display name
- `EmailSummary`: Brief email information for lists
- `EmailDetail`: Complete email content
- `Attachment`: File attachment metadata
- `EmailStatus`: Read/unread enumeration

### Protocols (`protocols.py`)
- `MailClientProtocol`: Interface contract for mail client operations

### Exceptions (`exceptions.py`)
- Hierarchical exception structure for clean error handling
- Maps provider-specific errors to standard interface exceptions

## Usage

```python
from mail_client_interface.models import EmailSummary, EmailDetail
from mail_client_interface.protocols import MailClientProtocol
from mail_client_interface.exceptions import AuthenticationError

# Your code works with any implementation of MailClientProtocol
def read_recent_emails(client: MailClientProtocol):
    client.authenticate()
    emails, _ = client.get_email_list(max_results=10)
    for email in emails:
        print(f"{email.sender}: {email.subject}")
```

## Design Goals

- **Provider Agnostic**: Works with any email service
- **Type Safe**: Comprehensive type hints throughout
- **Error Resistant**: Clear exception hierarchy
- **Future Proof**: Stable interface for long-term use
