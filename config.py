"""Configuration management for the Confluence MCP server."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class ConfluenceConfig:
    """Configuration for Confluence API connection."""

    url: str
    username: str
    api_token: str


@dataclass
class Config:
    """Global configuration for the application."""

    confluence: ConfluenceConfig
    log_level: str = "INFO"
    debug: bool = False


def load_config() -> Config:
    """
    Load configuration from environment variables.

    Returns:
        Config: Application configuration
    """
    load_dotenv()

    # Required Confluence settings
    confluence_url = os.getenv("CONFLUENCE_URL")
    confluence_username = os.getenv("CONFLUENCE_USERNAME")
    confluence_api_token = os.getenv("CONFLUENCE_PAT")

    # Validate required settings
    missing = []
    if not confluence_url:
        missing.append("CONFLUENCE_URL")
    if not confluence_username:
        missing.append("CONFLUENCE_USERNAME")
    if not confluence_api_token:
        missing.append("CONFLUENCE_PAT")

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    # Optional settings
    log_level = os.getenv("LOG_LEVEL", "INFO")
    debug = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes", "y")

    confluence_config = ConfluenceConfig(
        url=str(confluence_url),
        username=str(confluence_username),
        api_token=str(confluence_api_token),
    )

    return Config(confluence=confluence_config, log_level=log_level, debug=debug)
