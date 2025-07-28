"""System tests for end-to-end functionality."""

import pytest
from gmail_implementation.client import GmailClient
from mail_client_interface.exceptions import ConfigurationError


@pytest.mark.slow
@pytest.mark.skipif(
    True,  # Skip by default - requires real Gmail setup
    reason="Requires Gmail credentials and real API access"
)
def test_real_gmail_authentication():
    """Test authentication with real Gmail API."""
    client = GmailClient()
    
    try:
        client.authenticate()
        assert client.is_authenticated()
        
        # Test basic functionality
        emails, _ = client.get_email_list(max_results=5)
        assert isinstance(emails, list)
        
        if emails:
            detail = client.get_email_detail(emails[0].message_id)
            assert detail.message_id == emails[0].message_id
            
    finally:
        client.logout()


def test_missing_credentials_error():
    """Test error handling when credentials are missing."""
    client = GmailClient(credentials_path='nonexistent_credentials.json')
    
    with pytest.raises(ConfigurationError):
        client.authenticate()


def test_system_components_integration():
    """Test that all system components work together."""
    # This test verifies that all components can be imported and instantiated
    from mail_client_interface.models import EmailAddress, EmailSummary, EmailDetail, EmailStatus, Attachment
    from mail_client_interface.protocols import MailClientProtocol
    from mail_client_interface.exceptions import MailClientError, AuthenticationError
    from gmail_implementation.client import GmailClient
    from gmail_implementation.auth import GmailAuthenticator
    from gmail_implementation.transformer import GmailTransformer
    
    # Test that all imports work
    assert EmailAddress is not None
    assert EmailSummary is not None
    assert EmailDetail is not None
    assert EmailStatus is not None
    assert Attachment is not None
    assert MailClientProtocol is not None
    assert MailClientError is not None
    assert AuthenticationError is not None
    assert GmailClient is not None
    assert GmailAuthenticator is not None
    assert GmailTransformer is not None
    
    # Test that components can be instantiated
    client = GmailClient()
    assert client is not None
    
    # Test that the client implements the protocol interface
    assert hasattr(client, 'authenticate')
    assert hasattr(client, 'get_email_list')
    assert hasattr(client, 'get_email_detail')
    assert hasattr(client, 'is_authenticated')
    assert hasattr(client, 'logout')
