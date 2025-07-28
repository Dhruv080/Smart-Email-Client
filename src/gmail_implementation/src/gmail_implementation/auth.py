"""Gmail OAuth2 authentication handler."""

import json
import os
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

from mail_client_interface.exceptions import AuthenticationError, ConfigurationError


class GmailAuthenticator:
    """Handles Gmail OAuth2 authentication."""

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    TOKEN_FILE = 'token.json'
    CREDENTIALS_FILE = 'credentials.json'

    def __init__(self, credentials_path: Optional[str] = None) -> None:
        """Initialize the authenticator.
        
        Args:
            credentials_path: Path to credentials.json file
        """
        self.credentials_path = credentials_path or self.CREDENTIALS_FILE
        self._credentials: Optional[Credentials] = None
        self._service: Optional[Resource] = None

    def authenticate(self) -> Resource:
        """Authenticate and return Gmail service.
        
        Returns:
            Authenticated Gmail service
            
        Raises:
            AuthenticationError: If authentication fails
            ConfigurationError: If credentials file is missing
        """
        if not Path(self.credentials_path).exists():
            raise ConfigurationError(
                f"Credentials file not found: {self.credentials_path}. "
                "Please download from Google Cloud Console."
            )

        self._credentials = self._get_credentials()
        
        try:
            self._service = build('gmail', 'v1', credentials=self._credentials)
            return self._service
        except Exception as e:
            raise AuthenticationError(f"Failed to build Gmail service: {e}") from e

    def _get_credentials(self) -> Credentials:
        """Get valid credentials, refreshing if necessary."""
        creds = None
        
        # Load existing token
        if Path(self.TOKEN_FILE).exists():
            creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    raise AuthenticationError(f"Failed to refresh token: {e}") from e
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    raise AuthenticationError(f"OAuth flow failed: {e}") from e
            
            # Save credentials for next run
            try:
                with open(self.TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                # Not critical, just means user will need to re-auth next time
                print(f"Warning: Could not save token: {e}")
        
        return creds

    def is_authenticated(self) -> bool:
        """Check if currently authenticated."""
        return (
            self._credentials is not None 
            and self._credentials.valid 
            and self._service is not None
        )

    def logout(self) -> None:
        """Clear authentication and remove token file."""
        self._credentials = None
        self._service = None
        
        if Path(self.TOKEN_FILE).exists():
            try:
                os.remove(self.TOKEN_FILE)
            except Exception as e:
                print(f"Warning: Could not remove token file: {e}")

    @property
    def service(self) -> Resource:
        """Get the Gmail service.
        
        Returns:
            Gmail service
            
        Raises:
            AuthenticationError: If not authenticated
        """
        if not self._service:
            raise AuthenticationError("Not authenticated. Call authenticate() first.")
        return self._service
