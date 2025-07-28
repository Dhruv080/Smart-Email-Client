"""Test mail client models."""

from datetime import datetime
from mail_client_interface.models import (
    EmailAddress, EmailStatus, EmailSummary, EmailDetail, Attachment
)


def test_email_address_with_name():
    """Test EmailAddress with name."""
    addr = EmailAddress(email="test@example.com", name="Test User")
    assert str(addr) == "Test User <test@example.com>"


def test_email_address_without_name():
    """Test EmailAddress without name."""
    addr = EmailAddress(email="test@example.com")
    assert str(addr) == "test@example.com"


def test_email_summary_creation():
    """Test EmailSummary creation."""
    sender = EmailAddress(email="sender@example.com", name="Sender")
    date = datetime.now()
    
    summary = EmailSummary(
        message_id="123",
        sender=sender,
        subject="Test Subject",
        date=date,
        status=EmailStatus.UNREAD,
        has_attachments=True,
        snippet="Test snippet"
    )
    
    assert summary.message_id == "123"
    assert summary.sender == sender
    assert summary.subject == "Test Subject"
    assert summary.status == EmailStatus.UNREAD
    assert summary.has_attachments is True


def test_attachment_creation():
    """Test Attachment creation."""
    attachment = Attachment(
        filename="test.pdf",
        mime_type="application/pdf",
        size_bytes=1024,
        attachment_id="att123"
    )
    
    assert attachment.filename == "test.pdf"
    assert attachment.mime_type == "application/pdf"
    assert attachment.size_bytes == 1024
    assert attachment.attachment_id == "att123"


def test_email_detail_creation():
    """Test EmailDetail creation."""
    sender = EmailAddress(email="sender@example.com", name="Sender")
    recipient = EmailAddress(email="recipient@example.com")
    date = datetime.now()
    
    detail = EmailDetail(
        message_id="456",
        sender=sender,
        recipients=[recipient],
        cc=[],
        bcc=[],
        subject="Test Detail",
        date=date,
        status=EmailStatus.READ,
        body_text="Test body",
        body_html="<p>Test body</p>",
        attachments=[],
        thread_id="thread123",
        labels=["INBOX"]
    )
    
    assert detail.message_id == "456"
    assert detail.sender == sender
    assert len(detail.recipients) == 1
    assert detail.recipients[0] == recipient
