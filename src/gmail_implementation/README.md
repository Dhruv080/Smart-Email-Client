# Gmail Implementation

This package provides a Gmail-specific implementation of the Mail Client Interface, handling all the complexities of Google's APIs while presenting a clean, standardized interface.

## Purpose

The Gmail Implementation fulfills the Mail Client Interface contract using Google's Gmail API. It handles:

- **OAuth2 Authentication**: Secure login flow with token management
- **API Integration**: Gmail API calls and response handling
- **Data Transformation**: Converting Gmail data to interface models
- **Error Mapping**: Translating Gmail errors to interface exceptions

## Components

### Client (`client.py`)
- `GmailClient`: Main class implementing `MailClientProtocol`
- Orchestrates authentication, API calls, and data transformation
- Maps Gmail-specific errors to interface exceptions

### Authentication (`auth.py`)
- `GmailAuthenticator`: Handles OAuth2 flow with Gmail
- Manages token storage and refresh
- Provides authenticated Gmail service instance

### Transformer (`transformer.py`)
- `GmailTransformer`: Converts Gmail API responses to interface models
- Handles various email formats (text/HTML, multipart)
- Extracts attachments and metadata

## Setup

1. **Enable Gmail API**:
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create project and enable Gmail API
   - Create OAuth2 credentials for desktop application

2. **Install Dependencies**:
   ```bash
   uv add google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

3. **Add Credentials**:
   - Download credentials file as `credentials.json`
   - Place in project root

## Usage

```python
from gmail_implementation.client import GmailClient

# Create client
client = GmailClient()

# Authenticate (opens browser for OAuth)
client.authenticate()

# Use standard interface
emails, next_token = client.get_email_list(max_results=10)
for email in emails:
    print(f"{email.sender}: {email.subject}")

# Read specific email
detail = client.get_email_detail(emails[0].message_id)
print(detail.body_text)

# Clean logout
client.logout()
```

## Features

- **Automatic Token Refresh**: Handles expired authentication seamlessly
- **Pagination Support**: Efficiently handles large inboxes
- **Rich Data Extraction**: Supports text, HTML, and attachments
- **Robust Error Handling**: Maps Gmail errors to interface exceptions
- **Type Safety**: Full type hints throughout

## Dependencies

- `mail-client-interface`: The interface this package implements
- `google-api-python-client`: Google's API client library
- `google-auth-httplib2`: HTTP library for Google authentication
- `google-auth-oauthlib`: OAuth2 flow implementation
