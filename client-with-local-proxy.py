import asyncio

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

# Create transport with authentication headers
transport = StreamableHttpTransport(
    url="http://127.0.0.1:3000/mcp-server/mcp",
)

client = Client(transport)


async def main():
    async with client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")


asyncio.run(main())
