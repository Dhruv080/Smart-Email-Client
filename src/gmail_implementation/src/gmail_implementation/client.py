"""Gmail client implementation."""

from typing import List, Optional, Dict, Any

from googleapiclient.errors import HttpError

from mail_client_interface.protocols import MailClientProtocol
from mail_client_interface.models import EmailSummary, EmailDetail
from mail_client_interface.exceptions import (
    AuthenticationError, ConnectionError, ServiceError, EmailNotFoundError
)

from .auth import GmailAuthenticator
from .transformer import GmailTransformer


class GmailClient:
    """Gmail implementation of the mail client protocol."""

    def __init__(self, credentials_path: Optional[str] = None) -> None:
        """Initialize the Gmail client.
        
        Args:
            credentials_path: Path to Gmail credentials file
        """
        self.authenticator = GmailAuthenticator(credentials_path)
        self.transformer = GmailTransformer()

    def authenticate(self) -> None:
        """Authenticate with Gmail."""
        try:
            self.authenticator.authenticate()
        except Exception as e:
            raise AuthenticationError(f"Gmail authentication failed: {e}") from e

    def get_email_list(
        self, 
        max_results: int = 10,
        page_token: Optional[str] = None
    ) -> tuple[List[EmailSummary], Optional[str]]:
        """Get a list of emails from Gmail inbox."""
        if not self.is_authenticated():
            raise AuthenticationError("Not authenticated with Gmail")

        try:
            service = self.authenticator.service
            
            # Get message list
            request_params: Dict[str, Any] = {
                'userId': 'me',
                'labelIds': ['INBOX'],
                'maxResults': max_results
            }
            
            if page_token:
                request_params['pageToken'] = page_token

            messages_result = service.users().messages().list(**request_params).execute()
            
            messages = messages_result.get('messages', [])
            next_page_token = messages_result.get('nextPageToken')
            
            # Get detailed info for each message
            email_summaries = []
            for message in messages:
                try:
                    msg_detail = service.users().messages().get(
                        userId='me', 
                        id=message['id'],
                        format='metadata',
                        metadataHeaders=['From', 'Subject', 'Date', 'To']
                    ).execute()
                    
                    summary = self.transformer.to_email_summary(msg_detail)
                    email_summaries.append(summary)
                    
                except HttpError as e:
                    if e.resp.status == 404:
                        continue  # Skip deleted messages
                    raise
            
            return email_summaries, next_page_token
            
        except HttpError as e:
            if e.resp.status == 401:
                raise AuthenticationError("Gmail authentication expired")
            elif e.resp.status >= 500:
                raise ServiceError(f"Gmail service error: {e}")
            else:
                raise ConnectionError(f"Gmail connection error: {e}")
        except Exception as e:
            raise ServiceError(f"Unexpected Gmail error: {e}") from e

    def get_email_detail(self, message_id: str) -> EmailDetail:
        """Get complete details for a specific Gmail message."""
        if not self.is_authenticated():
            raise AuthenticationError("Not authenticated with Gmail")

        try:
            service = self.authenticator.service
            
            message = service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            return self.transformer.to_email_detail(message)
            
        except HttpError as e:
            if e.resp.status == 404:
                raise EmailNotFoundError(f"Email not found: {message_id}")
            elif e.resp.status == 401:
                raise AuthenticationError("Gmail authentication expired")
            elif e.resp.status >= 500:
                raise ServiceError(f"Gmail service error: {e}")
            else:
                raise ConnectionError(f"Gmail connection error: {e}")
        except Exception as e:
            raise ServiceError(f"Unexpected Gmail error: {e}") from e

    def is_authenticated(self) -> bool:
        """Check if authenticated with Gmail."""
        return self.authenticator.is_authenticated()

    def logout(self) -> None:
        """Log out from Gmail."""
        self.authenticator.logout()
