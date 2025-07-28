"""Test Gmail authentication."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

from gmail_implementation.auth import GmailAuthenticator
from mail_client_interface.exceptions import AuthenticationError, ConfigurationError


@pytest.fixture
def temp_credentials_file():
    """Create a temporary credentials file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('''{
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }''')
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def authenticator(temp_credentials_file):
    """Create authenticator with temporary credentials."""
    return GmailAuthenticator(credentials_path=temp_credentials_file)


def test_init_default_path():
    """Test authenticator initialization with default path."""
    auth = GmailAuthenticator()
    assert auth.credentials_path == 'credentials.json'


def test_init_custom_path():
    """Test authenticator initialization with custom path."""
    custom_path = 'custom_credentials.json'
    auth = GmailAuthenticator(credentials_path=custom_path)
    assert auth.credentials_path == custom_path


def test_authenticate_missing_credentials():
    """Test authentication with missing credentials file."""
    auth = GmailAuthenticator(credentials_path='nonexistent.json')
    
    with pytest.raises(ConfigurationError, match="Credentials file not found"):
        auth.authenticate()


@patch('gmail_implementation.auth.build')
@patch('gmail_implementation.auth.Credentials')
def test_authenticate_success(mock_credentials, mock_build, authenticator):
    """Test successful authentication."""
    # Mock credentials
    mock_creds = Mock()
    mock_creds.valid = True
    authenticator._get_credentials = Mock(return_value=mock_creds)
    
    # Mock service
    mock_service = Mock()
    mock_build.return_value = mock_service
    
    # Test
    service = authenticator.authenticate()
    
    # Verify
    assert service == mock_service
    mock_build.assert_called_once_with('gmail', 'v1', credentials=mock_creds)


@patch('gmail_implementation.auth.build')
def test_authenticate_build_failure(mock_build, authenticator):
    """Test authentication failure during service build."""
    authenticator._get_credentials = Mock(return_value=Mock())
    mock_build.side_effect = Exception("Build failed")
    
    with pytest.raises(AuthenticationError, match="Failed to build Gmail service"):
        authenticator.authenticate()


def test_is_authenticated_false_initially(authenticator):
    """Test is_authenticated returns False initially."""
    assert not authenticator.is_authenticated()


def test_is_authenticated_true_after_success(authenticator):
    """Test is_authenticated returns True after successful auth."""
    # Mock successful authentication
    mock_creds = Mock()
    mock_creds.valid = True
    authenticator._credentials = mock_creds
    authenticator._service = Mock()
    
    assert authenticator.is_authenticated()


def test_logout_clears_credentials(authenticator, temp_credentials_file):
    """Test logout clears credentials and removes token."""
    # Setup authenticated state
    authenticator._credentials = Mock()
    authenticator._service = Mock()
    
    # Create fake token file
    token_path = Path(authenticator.TOKEN_FILE)
    token_path.write_text('{"fake": "token"}')
    
    # Test logout
    authenticator.logout()
    
    # Verify state cleared
    assert authenticator._credentials is None
    assert authenticator._service is None
    assert not token_path.exists()


def test_service_property_authenticated(authenticator):
    """Test service property when authenticated."""
    mock_service = Mock()
    authenticator._service = mock_service
    
    assert authenticator.service == mock_service


def test_service_property_not_authenticated(authenticator):
    """Test service property when not authenticated."""
    with pytest.raises(AuthenticationError, match="Not authenticated"):
        _ = authenticator.service
