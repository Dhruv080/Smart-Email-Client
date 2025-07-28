"""Protocol definitions for the mail client interface."""

from typing import Protocol, List, Optional
from .models import EmailSummary, EmailDetail


class MailClientProtocol(Protocol):
    """Protocol defining mail client capabilities."""

    def authenticate(self) -> None:
        """Authenticate with the email service.
        
        Raises:
            AuthenticationError: If authentication fails
            ConnectionError: If unable to connect to service
        """
        ...

    def get_email_list(
        self, 
        max_results: int = 10,
        page_token: Optional[str] = None
    ) -> tuple[List[EmailSummary], Optional[str]]:
        """Get a list of emails from the inbox.
        
        Args:
            max_results: Maximum number of emails to retrieve
            page_token: Token for pagination (None for first page)
            
        Returns:
            Tuple of (email_list, next_page_token)
            
        Raises:
            AuthenticationError: If not authenticated
            ConnectionError: If unable to connect to service
            ServiceError: If the email service returns an error
        """
        ...

    def get_email_detail(self, message_id: str) -> EmailDetail:
        """Get complete details for a specific email.
        
        Args:
            message_id: Unique identifier for the email
            
        Returns:
            Complete email details
            
        Raises:
            AuthenticationError: If not authenticated
            EmailNotFoundError: If email doesn't exist
            ConnectionError: If unable to connect to service
            ServiceError: If the email service returns an error
        """
        ...

    def is_authenticated(self) -> bool:
        """Check if currently authenticated with the service."""
        ...

    def logout(self) -> None:
        """Log out from the email service."""
        ...
