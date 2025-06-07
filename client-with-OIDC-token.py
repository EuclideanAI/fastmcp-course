import asyncio
import os
import time

import dotenv
import jwt
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from google.auth.transport.requests import Request
from google.oauth2.service_account import IDTokenCredentials

dotenv.load_dotenv()


class TokenManager:
    def __init__(self, target_audience):
        self.target_audience = target_audience
        self.token = None
        self.expires_at = 0

    def get_token(self):
        # Check if token is expired or will expire in next 5 minutes
        if not self.token or time.time() > (self.expires_at - 300):
            self._refresh_token()
        return self.token

    def _refresh_token(self):
        # Get service account key file path
        key_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not key_file:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        # Create ID token credentials for service account
        id_token_credentials = IDTokenCredentials.from_service_account_file(
            key_file, target_audience=self.target_audience
        )

        # Refresh the token
        request = Request()
        id_token_credentials.refresh(request)
        self.token = id_token_credentials.token

        # Decode to get expiration time
        decoded = jwt.decode(self.token, options={"verify_signature": False})
        self.expires_at = decoded["exp"]
        print(f"Token refreshed, expires at: {time.ctime(self.expires_at)}")


async def main():
    cloud_run_url = "https://confluence-fastmcp-529297080659.us-central1.run.app"

    token_manager = TokenManager(cloud_run_url)
    token = token_manager.get_token()

    if not token:
        raise ValueError("Failed to obtain authentication token")

    transport = StreamableHttpTransport(
        url=f"{cloud_run_url}/mcp-server/mcp/",
        headers={"Authorization": f"Bearer {token}"},
    )

    client = Client(transport)

    async with client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")


asyncio.run(main())
