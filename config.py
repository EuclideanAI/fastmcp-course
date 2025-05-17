import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class ConfluenceConfig:
    """Configuration for the Confluence API client"""

    url: str
    username: Optional[str] = None
    personal_access_token: Optional[str] = None

    @classmethod
    def from_env(cls) -> "ConfluenceConfig":
        """Load configuration from environment variables"""
        url = os.environ.get("CONFLUENCE_URL")
        username = os.environ.get("CONFLUENCE_USERNAME")
        personal_access_token = os.environ.get("CONFLUENCE_PAT")

        if not url:
            raise ValueError("CONFLUENCE_URL environment variable is required")

        # Validate we have username and PAT authentication
        if not username:
            raise ValueError("CONFLUENCE_USERNAME environment variable is required")

        if not personal_access_token:
            raise ValueError(
                "CONFLUENCE_PAT (Personal Access Token) environment variable is required"
            )

        return cls(
            url=url, username=username, personal_access_token=personal_access_token
        )


def get_confluence_config() -> ConfluenceConfig:
    """
    Get the Confluence configuration from environment variables.

    Returns:
        ConfluenceConfig: The Confluence configuration.

    Raises:
        ValueError: If required configuration values are missing or invalid.
    """
    return ConfluenceConfig.from_env()
