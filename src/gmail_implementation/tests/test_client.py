"""Test Gmail client."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from googleapiclient.errors import HttpError

from gmail_implementation.client import GmailClient
from mail_client_interface.exceptions import (
    AuthenticationError, ServiceError, EmailNotFoundError
)


@pytest.fixture
def mock_gmail_client():
    """Create a Gmail client with mocked authenticator."""
    client = GmailClient()
    client.authenticator = Mock()
    client.transformer = Mock()
    return client


def test_authenticate_success(mock_gmail_client):
    """Test successful authentication."""
    mock_gmail_client.authenticator.authenticate.return_value = Mock()
    
    mock_gmail_client.authenticate()
    mock_gmail_client.authenticator.authenticate.assert_called_once()


def test_authenticate_failure(mock_gmail_client):
    """Test authentication failure."""
    mock_gmail_client.authenticator.authenticate.side_effect = Exception("Auth failed")
    
    with pytest.raises(AuthenticationError, match="Gmail authentication failed"):
        mock_gmail_client.authenticate()


def test_get_email_list_not_authenticated(mock_gmail_client):
    """Test get_email_list when not authenticated."""
    mock_gmail_client.authenticator.is_authenticated.return_value = False
    
    with pytest.raises(AuthenticationError, match="Not authenticated with Gmail"):
        mock_gmail_client.get_email_list()


def test_get_email_list_success(mock_gmail_client):
    """Test successful email list retrieval."""
    # Setup mocks
    mock_gmail_client.authenticator.is_authenticated.return_value = True
    mock_service = Mock()
    mock_gmail_client.authenticator.service = mock_service
    
    # Mock Gmail API response
    mock_messages_result = {
        'messages': [{'id': '123'}, {'id': '456'}],
        'nextPageToken': 'next_token'
    }
    mock_service.users().messages().list().execute.return_value = mock_messages_result
    
    # Mock individual message details
    mock_message_detail = {'id': '123', 'payload': {'headers': []}}
    mock_service.users().messages().get().execute.return_value = mock_message_detail
    
    # Mock transformer
    mock_summary = Mock()
    mock_gmail_client.transformer.to_email_summary.return_value = mock_summary
    
    # Test
    emails, next_token = mock_gmail_client.get_email_list(max_results=5)
    
    # Verify calls
    mock_service.users().messages().list.assert_called_once()
    assert next_token == 'next_token'


def test_get_email_detail_not_found(mock_gmail_client):
    """Test get_email_detail with non-existent email."""
    mock_gmail_client.authenticator.is_authenticated.return_value = True
    mock_service = Mock()
    mock_gmail_client.authenticator.service = mock_service
    
    # Mock 404 error
    http_error = HttpError(
        resp=Mock(status=404),
        content=b'Not found'
    )
    mock_service.users().messages().get().execute.side_effect = http_error
    
    with pytest.raises(EmailNotFoundError):
        mock_gmail_client.get_email_detail('nonexistent')


def test_is_authenticated(mock_gmail_client):
    """Test is_authenticated method."""
    mock_gmail_client.authenticator.is_authenticated.return_value = True
    assert mock_gmail_client.is_authenticated() is True
    
    mock_gmail_client.authenticator.is_authenticated.return_value = False
    assert mock_gmail_client.is_authenticated() is False


def test_logout(mock_gmail_client):
    """Test logout method."""
    mock_gmail_client.logout()
    mock_gmail_client.authenticator.logout.assert_called_once()


def test_http_error_handling(mock_gmail_client):
    """Test various HTTP error status codes."""
    mock_gmail_client.authenticator.is_authenticated.return_value = True
    mock_service = Mock()
    mock_gmail_client.authenticator.service = mock_service
    
    # Test 401 (unauthorized)
    http_error_401 = HttpError(resp=Mock(status=401), content=b'Unauthorized')
    mock_service.users().messages().get().execute.side_effect = http_error_401
    
    with pytest.raises(AuthenticationError):
        mock_gmail_client.get_email_detail('some_id')

    # Test 500 (server error)
    http_error_500 = HttpError(resp=Mock(status=500), content=b'Server Error')
    mock_service.users().messages().get().execute.side_effect = http_error_500
    
    with pytest.raises(ServiceError):
        mock_gmail_client.get_email_detail('some_id')
