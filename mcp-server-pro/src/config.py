"""
config.py - Loads and validates environment variables.
All other server modules import from here.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "IA-Agent-MCP")
    LOG_LEVEL: str = os.getenv("MCP_LOG_LEVEL", "INFO")
    WORKSPACE_ROOT: str = os.getenv("WORKSPACE_ROOT", ".")


config = Config()
