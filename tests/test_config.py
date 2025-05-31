"""Tests for configuration management."""

import os
from typing import Any
from unittest.mock import patch

import pytest

from config import Config, ConfluenceConfig, load_config


class TestConfluenceConfig:
    """Test ConfluenceConfig dataclass."""

    def test_confluence_config_creation(self) -> None:
        """Test creating a ConfluenceConfig instance."""
        config = ConfluenceConfig(
            url="https://test.atlassian.net",
            username="test@example.com",
            api_token="test-token",
        )

        assert config.url == "https://test.atlassian.net"
        assert config.username == "test@example.com"
        assert config.api_token == "test-token"


class TestConfig:
    """Test Config dataclass."""

    def test_config_creation_with_defaults(self) -> None:
        """Test creating a Config instance with default values."""
        confluence_config = ConfluenceConfig(
            url="https://test.atlassian.net",
            username="test@example.com",
            api_token="test-token",
        )
        config = Config(confluence=confluence_config)

        assert config.confluence == confluence_config
        assert config.log_level == "INFO"
        assert config.debug is False

    def test_config_creation_with_custom_values(self) -> None:
        """Test creating a Config instance with custom values."""
        confluence_config = ConfluenceConfig(
            url="https://test.atlassian.net",
            username="test@example.com",
            api_token="test-token",
        )
        config = Config(
            confluence=confluence_config,
            log_level="DEBUG",
            debug=True,
        )

        assert config.confluence == confluence_config
        assert config.log_level == "DEBUG"
        assert config.debug is True


class TestLoadConfig:
    """Test load_config function."""

    @patch.dict(os.environ, {}, clear=True)
    @patch("config.load_dotenv")
    def test_load_config_missing_all_required(self, mock_load_dotenv: Any) -> None:
        """Test load_config raises error when all required variables are missing."""
        with pytest.raises(ValueError) as exc_info:
            load_config()

        error_message = str(exc_info.value)
        assert "Missing required environment variables:" in error_message
        assert "CONFLUENCE_URL" in error_message
        assert "CONFLUENCE_USERNAME" in error_message
        assert "CONFLUENCE_PAT" in error_message
        mock_load_dotenv.assert_called_once()

    @patch.dict(
        os.environ,
        {
            "CONFLUENCE_URL": "https://test.atlassian.net",
            # Missing USERNAME and PAT
        },
        clear=True,
    )
    @patch("config.load_dotenv")
    def test_load_config_missing_some_required(self, mock_load_dotenv: Any) -> None:
        """Test load_config raises error when some required variables are missing."""
        with pytest.raises(ValueError) as exc_info:
            load_config()

        error_message = str(exc_info.value)
        assert "Missing required environment variables:" in error_message
        assert "CONFLUENCE_USERNAME" in error_message
        assert "CONFLUENCE_PAT" in error_message
        assert "CONFLUENCE_URL" not in error_message  # This one is present
        mock_load_dotenv.assert_called_once()

    @patch.dict(
        os.environ,
        {
            "CONFLUENCE_URL": "https://test.atlassian.net",
            "CONFLUENCE_USERNAME": "test@example.com",
            "CONFLUENCE_PAT": "test-token",
        },
        clear=True,
    )
    @patch("config.load_dotenv")
    def test_load_config_success_with_defaults(self, mock_load_dotenv: Any) -> None:
        """Test load_config success with only required variables (using defaults)."""
        config = load_config()

        assert config.confluence.url == "https://test.atlassian.net"
        assert config.confluence.username == "test@example.com"
        assert config.confluence.api_token == "test-token"
        assert config.log_level == "INFO"  # Default
        assert config.debug is False  # Default
        mock_load_dotenv.assert_called_once()

    @patch.dict(
        os.environ,
        {
            "CONFLUENCE_URL": "https://test.atlassian.net",
            "CONFLUENCE_USERNAME": "test@example.com",
            "CONFLUENCE_PAT": "test-token",
            "LOG_LEVEL": "DEBUG",
            "DEBUG": "true",
        },
        clear=True,
    )
    @patch("config.load_dotenv")
    def test_load_config_success_with_custom_values(
        self, mock_load_dotenv: Any
    ) -> None:
        """Test load_config success with custom optional values."""
        config = load_config()

        assert config.confluence.url == "https://test.atlassian.net"
        assert config.confluence.username == "test@example.com"
        assert config.confluence.api_token == "test-token"
        assert config.log_level == "DEBUG"
        assert config.debug is True
        mock_load_dotenv.assert_called_once()

    @pytest.mark.parametrize(
        "debug_value,expected",
        [
            ("true", True),
            ("TRUE", True),
            ("1", True),
            ("yes", True),
            ("y", True),
            ("false", False),
            ("FALSE", False),
            ("0", False),
            ("no", False),
            ("n", False),
            ("invalid", False),
            ("", False),
        ],
    )
    @patch.dict(
        os.environ,
        {
            "CONFLUENCE_URL": "https://test.atlassian.net",
            "CONFLUENCE_USERNAME": "test@example.com",
            "CONFLUENCE_PAT": "test-token",
        },
        clear=True,
    )
    @patch("config.load_dotenv")
    def test_load_config_debug_flag_parsing(
        self, mock_load_dotenv: Any, debug_value: str, expected: bool
    ) -> None:
        """Test that debug flag is parsed correctly from various string values."""
        with patch.dict(os.environ, {"DEBUG": debug_value}):
            config = load_config()
            assert config.debug is expected
            mock_load_dotenv.assert_called_once()
