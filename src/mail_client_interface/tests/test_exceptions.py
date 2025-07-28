"""Test mail client exceptions."""

import pytest
from mail_client_interface.exceptions import (
    MailClientError, AuthenticationError, ConnectionError, 
    ServiceError, EmailNotFoundError, ConfigurationError
)


def test_base_exception():
    """Test base MailClientError."""
    error = MailClientError("Base error")
    assert str(error) == "Base error"
    assert isinstance(error, Exception)


def test_authentication_error():
    """Test AuthenticationError inheritance."""
    error = AuthenticationError("Auth failed")
    assert str(error) == "Auth failed"
    assert isinstance(error, MailClientError)
    assert isinstance(error, Exception)


def test_connection_error():
    """Test ConnectionError inheritance."""
    error = ConnectionError("Connection failed")
    assert str(error) == "Connection failed"
    assert isinstance(error, MailClientError)


def test_service_error():
    """Test ServiceError inheritance."""
    error = ServiceError("Service failed")
    assert str(error) == "Service failed"
    assert isinstance(error, MailClientError)


def test_email_not_found_error():
    """Test EmailNotFoundError inheritance."""
    error = EmailNotFoundError("Email not found")
    assert str(error) == "Email not found"
    assert isinstance(error, MailClientError)


def test_configuration_error():
    """Test ConfigurationError inheritance."""
    error = ConfigurationError("Config error")
    assert str(error) == "Config error"
    assert isinstance(error, MailClientError)


def test_exception_raising():
    """Test that exceptions can be raised and caught."""
    with pytest.raises(AuthenticationError):
        raise AuthenticationError("Test auth error")
    
    with pytest.raises(MailClientError):
        raise AuthenticationError("Test as base error")
