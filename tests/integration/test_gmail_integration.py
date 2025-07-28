"""Integration tests for Gmail implementation with mail client interface."""

import pytest
from unittest.mock import Mock, patch
from typing import List

from mail_client_interface.protocols import MailClientProtocol
from mail_client_interface.models import EmailSummary, EmailDetail
from mail_client_interface.exceptions import AuthenticationError

from gmail_implementation.client import GmailClient


def test_gmail_client_implements_protocol():
    """Test that GmailClient properly implements MailClientProtocol."""
    client = GmailClient()
    
    # Check that all protocol methods exist
    assert hasattr(client, 'authenticate')
    assert hasattr(client, 'get_email_list')
    assert hasattr(client, 'get_email_detail')
    assert hasattr(client, 'is_authenticated')
    assert hasattr(client, 'logout')


def test_forklift_test_simulation():
    """Simulate the forklift test - swapping implementations."""
    
    class MockEmailClient:
        """Mock implementation that could replace Gmail."""
        
        def __init__(self):
            self._authenticated = False
        
        def authenticate(self) -> None:
            self._authenticated = True
        
        def get_email_list(self, max_results: int = 10, page_token=None):
            if not self._authenticated:
                raise AuthenticationError("Not authenticated")
            return [], None
        
        def get_email_detail(self, message_id: str):
            if not self._authenticated:
                raise AuthenticationError("Not authenticated")
            # Return mock detail
            from mail_client_interface.models import EmailDetail, EmailAddress, EmailStatus
            from datetime import datetime
            
            return EmailDetail(
                message_id=message_id,
                sender=EmailAddress(email="test@example.com"),
                recipients=[],
                cc=[],
                bcc=[],
                subject="Mock Email",
                date=datetime.now(),
                status=EmailStatus.READ,
                body_text="Mock body",
                body_html=None,
                attachments=[],
                thread_id="mock_thread",
                labels=[]
            )
        
        def is_authenticated(self) -> bool:
            return self._authenticated
        
        def logout(self) -> None:
            self._authenticated = False
    
    def use_mail_client(client: MailClientProtocol) -> None:
        """Function that works with any mail client implementation."""
        client.authenticate()
        emails, _ = client.get_email_list(max_results=5)
        
        if emails:
            detail = client.get_email_detail(emails[0].message_id)
            assert detail.message_id is not None
    
    # Test that mock implementation works with the same client code
    mock_client = MockEmailClient()
    use_mail_client(mock_client)
