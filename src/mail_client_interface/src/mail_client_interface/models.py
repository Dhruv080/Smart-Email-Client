"""Data models for the mail client interface."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class EmailStatus(Enum):
    """Email read status."""
    READ = "read"
    UNREAD = "unread"


@dataclass(frozen=True)
class EmailAddress:
    """Represents an email address with optional display name."""
    email: str
    name: Optional[str] = None

    def __str__(self) -> str:
        """Return formatted email address."""
        if self.name:
            return f"{self.name} <{self.email}>"
        return self.email


@dataclass(frozen=True)
class Attachment:
    """Represents an email attachment."""
    filename: str
    mime_type: str
    size_bytes: int
    attachment_id: str


@dataclass(frozen=True)
class EmailSummary:
    """Summary information for an email in a list."""
    message_id: str
    sender: EmailAddress
    subject: str
    date: datetime
    status: EmailStatus
    has_attachments: bool
    snippet: str  # Brief preview of email content


@dataclass(frozen=True)
class EmailDetail:
    """Complete email information."""
    message_id: str
    sender: EmailAddress
    recipients: List[EmailAddress]
    cc: List[EmailAddress]
    bcc: List[EmailAddress]
    subject: str
    date: datetime
    status: EmailStatus
    body_text: Optional[str]
    body_html: Optional[str]
    attachments: List[Attachment]
    thread_id: str
    labels: List[str]
