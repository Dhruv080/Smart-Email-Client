"""Transform Gmail API responses to interface models."""

from datetime import datetime
from typing import List, Optional, Dict, Any
import base64
import email
from email.mime.text import MIMEText

from mail_client_interface.models import (
    EmailSummary, EmailDetail, EmailAddress, Attachment, EmailStatus
)


class GmailTransformer:
    """Transforms Gmail API responses to interface models."""

    @staticmethod
    def to_email_summary(gmail_message: Dict[str, Any]) -> EmailSummary:
        """Convert Gmail message to EmailSummary."""
        headers = {h['name']: h['value'] for h in gmail_message['payload']['headers']}
        
        # Parse sender
        sender_str = headers.get('From', 'Unknown')
        sender = GmailTransformer._parse_email_address(sender_str)
        
        # Parse date
        date = datetime.fromtimestamp(int(gmail_message['internalDate']) / 1000)
        
        # Determine status
        labels = gmail_message.get('labelIds', [])
        status = EmailStatus.READ if 'UNREAD' not in labels else EmailStatus.UNREAD
        
        # Check for attachments
        has_attachments = GmailTransformer._has_attachments(gmail_message['payload'])
        
        # Get snippet
        snippet = gmail_message.get('snippet', '')
        
        return EmailSummary(
            message_id=gmail_message['id'],
            sender=sender,
            subject=headers.get('Subject', '(No Subject)'),
            date=date,
            status=status,
            has_attachments=has_attachments,
            snippet=snippet
        )

    @staticmethod
    def to_email_detail(gmail_message: Dict[str, Any]) -> EmailDetail:
        """Convert Gmail message to EmailDetail."""
        headers = {h['name']: h['value'] for h in gmail_message['payload']['headers']}
        
        # Parse addresses
        sender = GmailTransformer._parse_email_address(headers.get('From', 'Unknown'))
        recipients = GmailTransformer._parse_email_addresses(headers.get('To', ''))
        cc = GmailTransformer._parse_email_addresses(headers.get('Cc', ''))
        bcc = GmailTransformer._parse_email_addresses(headers.get('Bcc', ''))
        
        # Parse date
        date = datetime.fromtimestamp(int(gmail_message['internalDate']) / 1000)
        
        # Determine status
        labels = gmail_message.get('labelIds', [])
        status = EmailStatus.READ if 'UNREAD' not in labels else EmailStatus.UNREAD
        
        # Extract body content
        body_text, body_html = GmailTransformer._extract_body(gmail_message['payload'])
        
        # Extract attachments
        attachments = GmailTransformer._extract_attachments(gmail_message['payload'])
        
        return EmailDetail(
            message_id=gmail_message['id'],
            sender=sender,
            recipients=recipients,
            cc=cc,
            bcc=bcc,
            subject=headers.get('Subject', '(No Subject)'),
            date=date,
            status=status,
            body_text=body_text,
            body_html=body_html,
            attachments=attachments,
            thread_id=gmail_message['threadId'],
            labels=labels
        )

    @staticmethod
    def _parse_email_address(address_str: str) -> EmailAddress:
        """Parse a single email address string."""
        try:
            parsed = email.utils.parseaddr(address_str)
            name = parsed[0] if parsed[0] else None
            email_addr = parsed[1]
            return EmailAddress(email=email_addr, name=name)
        except Exception:
            return EmailAddress(email=address_str)

    @staticmethod
    def _parse_email_addresses(addresses_str: str) -> List[EmailAddress]:
        """Parse multiple email addresses from a string."""
        if not addresses_str:
            return []
        
        addresses = []
        for addr in email.utils.getaddresses([addresses_str]):
            name = addr[0] if addr[0] else None
            email_addr = addr[1]
            if email_addr:
                addresses.append(EmailAddress(email=email_addr, name=name))
        
        return addresses

    @staticmethod
    def _has_attachments(payload: Dict[str, Any]) -> bool:
        """Check if message has attachments."""
        if payload.get('parts'):
            for part in payload['parts']:
                if part.get('body', {}).get('attachmentId'):
                    return True
                if GmailTransformer._has_attachments(part):
                    return True
        return False

    @staticmethod
    def _extract_body(payload: Dict[str, Any]) -> tuple[Optional[str], Optional[str]]:
        """Extract text and HTML body from message payload."""
        text_body = None
        html_body = None
        
        def extract_from_part(part: Dict[str, Any]) -> None:
            nonlocal text_body, html_body
            
            mime_type = part.get('mimeType', '')
            
            if mime_type == 'text/plain' and not text_body:
                data = part.get('body', {}).get('data')
                if data:
                    text_body = base64.urlsafe_b64decode(data).decode('utf-8')
            elif mime_type == 'text/html' and not html_body:
                data = part.get('body', {}).get('data')
                if data:
                    html_body = base64.urlsafe_b64decode(data).decode('utf-8')
            elif part.get('parts'):
                for subpart in part['parts']:
                    extract_from_part(subpart)
        
        if payload.get('parts'):
            for part in payload['parts']:
                extract_from_part(part)
        else:
            extract_from_part(payload)
        
        return text_body, html_body

    @staticmethod
    def _extract_attachments(payload: Dict[str, Any]) -> List[Attachment]:
        """Extract attachment information from message payload."""
        attachments = []
        
        def extract_from_part(part: Dict[str, Any]) -> None:
            if part.get('body', {}).get('attachmentId'):
                filename = part.get('filename', 'unnamed')
                mime_type = part.get('mimeType', 'application/octet-stream')
                size = part.get('body', {}).get('size', 0)
                attachment_id = part['body']['attachmentId']
                
                attachments.append(Attachment(
                    filename=filename,
                    mime_type=mime_type,
                    size_bytes=size,
                    attachment_id=attachment_id
                ))
            
            if part.get('parts'):
                for subpart in part['parts']:
                    extract_from_part(subpart)
        
        if payload.get('parts'):
            for part in payload['parts']:
                extract_from_part(part)
        
        return attachments
