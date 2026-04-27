"""
mcp_client.py - Reusable async client for calling MCP server tools.

Usage:
    result = await call_mcp_tool("run_db_query", {"sql": "SELECT * FROM users"})
"""
import asyncio
from contextlib import asynccontextmanager
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


_SERVER_PARAMS = StdioServerParameters(
    command="uv",
    args=["run", "mcp-server"],
)


@asynccontextmanager
async def _mcp_session():
    """Context manager that yields an initialized MCP ClientSession."""
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


async def call_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> str:
    """
    Call a single tool on the MCP server and return its text output.

    Args:
        tool_name:  Name of the registered MCP tool to invoke.
        arguments:  Dict of arguments matching the tool's signature.

    Returns:
        The tool's text response as a string.

    Raises:
        ValueError: If the tool response contains no text content.
        Exception:  Propagates any transport or server-side errors.
    """
    async with _mcp_session() as session:
        result = await session.call_tool(tool_name, arguments)

    if not result.content:
        raise ValueError(f"Tool '{tool_name}' returned an empty response.")

    return result.content[0].text


async def list_available_tools() -> list[str]:
    """
    Return the names of all tools registered on the MCP server.

    Returns:
        List of tool name strings.
    """
    async with _mcp_session() as session:
        tools = await session.list_tools()
    return [t.name for t in tools.tools]


# ---------------------------------------------------------------------------
# Quick smoke-test - run this file directly to verify the connection.
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    async def _smoke_test():
        print("Available tools:", await list_available_tools())
        result = await call_mcp_tool("list_db_tables", {})
        print("list_db_tables result:", result)

    asyncio.run(_smoke_test())
