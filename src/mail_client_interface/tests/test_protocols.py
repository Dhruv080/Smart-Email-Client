"""Test mail client protocols."""

from typing import List, Optional
from unittest.mock import Mock

from mail_client_interface.protocols import MailClientProtocol
from mail_client_interface.models import EmailSummary, EmailDetail


def test_mail_client_protocol():
    """Test that a mock client implements the protocol."""
    mock_client = Mock(spec=MailClientProtocol)
    
    # Test protocol methods exist
    assert hasattr(mock_client, 'authenticate')
    assert hasattr(mock_client, 'get_email_list')
    assert hasattr(mock_client, 'get_email_detail')
    assert hasattr(mock_client, 'is_authenticated')
    assert hasattr(mock_client, 'logout')


class MockMailClient:
    """Mock implementation of MailClientProtocol for testing."""
    
    def __init__(self):
        self._authenticated = False
    
    def authenticate(self) -> None:
        self._authenticated = True
    
    def get_email_list(
        self, 
        max_results: int = 10,
        page_token: Optional[str] = None
    ) -> tuple[List[EmailSummary], Optional[str]]:
        return [], None
    
    def get_email_detail(self, message_id: str) -> EmailDetail:
        raise NotImplementedError("Mock implementation")
    
    def is_authenticated(self) -> bool:
        return self._authenticated
    
    def logout(self) -> None:
        self._authenticated = False


def test_mock_client_implements_protocol():
    """Test that MockMailClient properly implements the protocol."""
    client = MockMailClient()
    
    # Test authentication flow
    assert not client.is_authenticated()
    client.authenticate()
    assert client.is_authenticated()
    client.logout()
    assert not client.is_authenticated()
    
    # Test email list method exists and returns correct type
    emails, token = client.get_email_list()
    assert isinstance(emails, list)
    assert token is None
