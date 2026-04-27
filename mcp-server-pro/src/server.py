"""
server.py - MCP server entry point.

Registers all tool modules onto the FastMCP instance and starts
the server using the stdio transport (required for mcp_client.py).
"""
from mcp.server.fastmcp import FastMCP

from src.config import config
from src.utils.logging_config import logger
from src.tools import pinecone_connector, excel_connector, ide_connector, autonomy_tools
from src.tools import pinecone_connector, excel_connector, ide_connector, autonomy_tools, gmail_connector

mcp = FastMCP(config.SERVER_NAME)


def main() -> None:
    logger.info("Starting MCP server '%s'.", config.SERVER_NAME)

    pinecone_connector.register(mcp)
    excel_connector.register(mcp)
    ide_connector.register(mcp)
    autonomy_tools.register(mcp)
    gmail_connector.register(mcp)

    logger.info("All tools registered. Running on stdio transport.")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
