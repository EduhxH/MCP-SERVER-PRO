"""
logging_config.py - Global logger configuration for the MCP server.

All logs are written to stderr because the stdio transport
uses stdout for MCP message framing.
"""
import logging
import sys

from src.config import config


def setup_logging() -> logging.Logger:
    level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr,
    )

    return logging.getLogger("mcp-server")


logger = setup_logging()
