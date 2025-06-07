"""Tests for server lifecycle and integration."""

from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio

from confluence.client import ConfluenceClient
from server import AppContext, app_lifespan, register_tools


class TestAppContext:
    """Test the AppContext dataclass."""

    def test_app_context_creation(self) -> None:
        """Test AppContext can be created with confluence client."""
        mock_confluence = MagicMock(spec=ConfluenceClient)
        context = AppContext(confluence=mock_confluence)

        assert context.confluence is mock_confluence


class TestAppLifespan:
    """Test the application lifespan management."""

    @pytest_asyncio.fixture
    async def mock_fastmcp_server(self) -> MagicMock:
        """Mock FastMCP server for testing."""
        return MagicMock()

    @pytest.mark.asyncio
    async def test_app_lifespan_success(
        self, mock_fastmcp_server: MagicMock, mock_config: MagicMock
    ) -> None:
        """Test successful app lifespan setup and teardown."""
        with (
            patch("server.load_config", return_value=mock_config),
            patch("server.ConfluenceClient") as mock_client_class,
        ):
            mock_client = MagicMock(spec=ConfluenceClient)
            mock_client_class.return_value = mock_client

            # Test the async context manager
            async with app_lifespan(mock_fastmcp_server) as context:
                # Verify context is properly created
                assert isinstance(context, AppContext)
                assert context.confluence is mock_client

                # Verify client was initialized with correct config
                mock_client_class.assert_called_once_with(
                    url=mock_config.confluence.url,
                    username=mock_config.confluence.username,
                    api_token=mock_config.confluence.api_token,
                )

    @pytest.mark.asyncio
    async def test_app_lifespan_config_error(
        self, mock_fastmcp_server: MagicMock
    ) -> None:
        """Test app lifespan handles configuration errors."""
        with patch("server.load_config", side_effect=ValueError("Invalid config")):
            with pytest.raises(ValueError, match="Invalid config"):
                async with app_lifespan(mock_fastmcp_server):
                    pass

    @pytest.mark.asyncio
    async def test_app_lifespan_client_error(
        self, mock_fastmcp_server: MagicMock, mock_config: MagicMock
    ) -> None:
        """Test app lifespan handles client initialization errors."""
        with (
            patch("server.load_config", return_value=mock_config),
            patch(
                "server.ConfluenceClient", side_effect=ConnectionError("Can't connect")
            ),
        ):
            with pytest.raises(ConnectionError, match="Can't connect"):
                async with app_lifespan(mock_fastmcp_server):
                    pass

    @pytest.mark.asyncio
    @patch("server.logger")
    async def test_app_lifespan_logging(
        self,
        mock_logger: MagicMock,
        mock_fastmcp_server: MagicMock,
        mock_config: MagicMock,
    ) -> None:
        """Test that app lifespan logs appropriately."""
        with (
            patch("server.load_config", return_value=mock_config),
            patch("server.ConfluenceClient"),
        ):
            async with app_lifespan(mock_fastmcp_server):
                pass

            # Verify logging calls
            mock_logger.info.assert_any_call("Configuration loaded successfully")
            mock_logger.info.assert_any_call("Confluence client initialized")
            mock_logger.info.assert_any_call("Shutting down Confluence MCP server")


class TestToolRegistration:
    """Test tool registration functionality."""

    @patch("server.mcp")
    @patch("server.logger")
    def test_register_tools(self, mock_logger: MagicMock, mock_mcp: MagicMock) -> None:
        """Test that all tools are registered correctly."""
        register_tools()

        # Verify logger was called
        mock_logger.info.assert_called_with("All tools registered successfully")
