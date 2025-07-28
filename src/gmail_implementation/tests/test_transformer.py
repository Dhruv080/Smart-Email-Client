"""Test Gmail data transformer."""

import pytest
from datetime import datetime
from gmail_implementation.transformer import GmailTransformer
from mail_client_interface.models import EmailStatus


@pytest.fixture
def sample_gmail_message():
    """Sample Gmail API message response."""
    return {
        'id': 'message123',
        'threadId': 'thread456',
        'labelIds': ['INBOX', 'UNREAD'],
        'snippet': 'This is a test email snippet...',
        'internalDate': '1640995200000',  # 2022-01-01 00:00:00 UTC
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'Test Sender <sender@example.com>'},
                {'name': 'To', 'value': 'recipient@example.com'},
                {'name': 'Subject', 'value': 'Test Subject'},
                {'name': 'Date', 'value': 'Sat, 1 Jan 2022 00:00:00 +0000'},
                {'name': 'Cc', 'value': 'cc@example.com'},
            ],
            'mimeType': 'text/plain',
            'body': {
                'data': 'VGhpcyBpcyBhIHRlc3QgZW1haWwgYm9keS4='  # base64: "This is a test email body."
            }
        }
    }


def test_to_email_summary_basic(sample_gmail_message):
    """Test basic email summary conversion."""
    summary = GmailTransformer.to_email_summary(sample_gmail_message)
    
    assert summary.message_id == 'message123'
    assert summary.sender.email == 'sender@example.com'
    assert summary.sender.name == 'Test Sender'
    assert summary.subject == 'Test Subject'
    assert summary.status == EmailStatus.UNREAD
    assert summary.has_attachments is False
    assert summary.snippet == 'This is a test email snippet...'


def test_to_email_detail_basic(sample_gmail_message):
    """Test basic email detail conversion."""
    detail = GmailTransformer.to_email_detail(sample_gmail_message)
    
    assert detail.message_id == 'message123'
    assert detail.sender.email == 'sender@example.com'
    assert detail.sender.name == 'Test Sender'
    assert len(detail.recipients) == 1
    assert detail.recipients[0].email == 'recipient@example.com'
    assert len(detail.cc) == 1
    assert detail.cc[0].email == 'cc@example.com'
    assert detail.subject == 'Test Subject'
    assert detail.thread_id == 'thread456'
    assert 'INBOX' in detail.labels
    assert detail.body_text == 'This is a test email body.'


def test_parse_email_address_with_name():
    """Test parsing email address with display name."""
    addr = GmailTransformer._parse_email_address('John Doe <john@example.com>')
    assert addr.email == 'john@example.com'
    assert addr.name == 'John Doe'


def test_parse_email_address_without_name():
    """Test parsing email address without display name."""
    addr = GmailTransformer._parse_email_address('jane@example.com')
    assert addr.email == 'jane@example.com'
    assert addr.name is None


def test_parse_email_addresses_multiple():
    """Test parsing multiple email addresses."""
    addresses = GmailTransformer._parse_email_addresses(
        'John Doe <john@example.com>, jane@example.com, Bob <bob@example.com>'
    )
    
    assert len(addresses) == 3
    assert addresses[0].email == 'john@example.com'
    assert addresses[0].name == 'John Doe'
    assert addresses[1].email == 'jane@example.com'
    assert addresses[1].name is None
    assert addresses[2].email == 'bob@example.com'
    assert addresses[2].name == 'Bob'


def test_has_attachments_true():
    """Test has_attachments detection with attachments."""
    payload = {
        'parts': [
            {'body': {'attachmentId': 'att123'}}
        ]
    }
    assert GmailTransformer._has_attachments(payload) is True


def test_has_attachments_false():
    """Test has_attachments detection without attachments."""
    payload = {
        'parts': [
            {'body': {'data': 'some_data'}}
        ]
    }
    assert GmailTransformer._has_attachments(payload) is False
