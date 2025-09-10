"""
Tests for configuration management
"""
import pytest
import os
from unittest.mock import patch

from app.config import Settings


class TestSettings:
    """Test configuration settings"""

    def test_default_settings(self):
        """Test default settings values"""
        # Clear environment to test defaults and disable .env file loading
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings(_env_file=None)
        
            assert settings.smtp_host == "smtp.gmail.com"
            assert settings.smtp_port == 587
            assert settings.secret_key == "your-secret-key-change-this"
            assert settings.debug is True
            assert settings.github_username is None
            assert settings.github_token is None

    def test_settings_from_env_vars(self):
        """Test settings loading from environment variables"""
        env_vars = {
            "GITHUB_USERNAME": "testuser",
            "GITHUB_TOKEN": "token123",
            "SMTP_USERNAME": "test@example.com",
            "SMTP_PASSWORD": "password123",
            "CONTACT_EMAIL": "contact@example.com",
            "SECRET_KEY": "super-secret-key",
            "DEBUG": "false"
        }
        
        with patch.dict(os.environ, env_vars):
            settings = Settings()
            
            assert settings.github_username == "testuser"
            assert settings.github_token == "token123"
            assert settings.smtp_username == "test@example.com"
            assert settings.smtp_password == "password123"
            assert settings.contact_email == "contact@example.com"
            assert settings.secret_key == "super-secret-key"
            assert settings.debug is False

    def test_settings_case_insensitive(self):
        """Test that settings are case insensitive"""
        env_vars = {
            "github_username": "testuser",  # lowercase
            "GITHUB_TOKEN": "token123",     # uppercase
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            
            assert settings.github_username == "testuser"
            assert settings.github_token == "token123"

    def test_settings_with_custom_values(self):
        """Test settings with custom initialization values"""
        custom_settings = Settings(
            github_username="custom_user",
            smtp_port=2525,
            debug=False
        )
        
        assert custom_settings.github_username == "custom_user"
        assert custom_settings.smtp_port == 2525
        assert custom_settings.debug is False
        # Other values should use defaults
        assert custom_settings.smtp_host == "smtp.gmail.com"

    def test_smtp_configuration_validation(self):
        """Test SMTP configuration scenarios"""
        # Test Gmail configuration
        gmail_settings = Settings(
            smtp_host="smtp.gmail.com",
            smtp_port=587
        )
        assert gmail_settings.smtp_host == "smtp.gmail.com"
        assert gmail_settings.smtp_port == 587
        
        # Test custom SMTP configuration
        custom_settings = Settings(
            smtp_host="mail.example.com",
            smtp_port=465
        )
        assert custom_settings.smtp_host == "mail.example.com"
        assert custom_settings.smtp_port == 465

    def test_email_configuration_completeness(self):
        """Test email configuration completeness scenarios"""
        # Complete configuration
        complete_config = Settings(
            smtp_username="user@example.com",
            smtp_password="password",
            contact_email="contact@example.com"
        )
        
        assert complete_config.smtp_username is not None
        assert complete_config.smtp_password is not None
        assert complete_config.contact_email is not None
        
        # Incomplete configuration - clear env to test defaults
        with patch.dict(os.environ, {}, clear=True):
            incomplete_config = Settings(_env_file=None)
            assert incomplete_config.smtp_username is None
            assert incomplete_config.smtp_password is None
            assert incomplete_config.contact_email is None
