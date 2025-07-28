"""Exception classes for the mail client interface."""


class MailClientError(Exception):
    """Base exception for mail client errors."""
    pass


class AuthenticationError(MailClientError):
    """Raised when authentication fails or is required."""
    pass


class ConnectionError(MailClientError):
    """Raised when unable to connect to the email service."""
    pass


class ServiceError(MailClientError):
    """Raised when the email service returns an error."""
    pass


class EmailNotFoundError(MailClientError):
    """Raised when a requested email cannot be found."""
    pass


class ConfigurationError(MailClientError):
    """Raised when there's a configuration problem."""
    pass
