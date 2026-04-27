"""
db_connector.py - MCP tool for executing SQL queries.

Basic security implemented:
- Blocks DROP, TRUNCATE, ALTER, CREATE DATABASE, GRANT, REVOKE by default.
- SELECT returns rows; other statements return affected row count.
"""
import re
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

from src.config import config
from src.utils.logging_config import logger

_BLOCKED = re.compile(
    r"\b(DROP|TRUNCATE|ALTER|CREATE\s+DATABASE|GRANT|REVOKE)\b",
    re.IGNORECASE,
)

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(config.DATABASE_URL)
        logger.info("SQLAlchemy engine created for %s", config.DATABASE_URL)
    return _engine


def register(mcp):

    @mcp.tool()
    def run_db_query(sql: str) -> str:
        """
        Execute a SQL query against the project database.

        Args:
            sql: SQL statement to execute (SELECT, INSERT, UPDATE, DELETE).

        Returns:
            List of dicts for SELECT queries, or affected row count for writes.

        Security:
            DROP, TRUNCATE, ALTER and similar statements are blocked.
        """
        if _BLOCKED.search(sql):
            logger.warning("Query blocked by security policy: %s", sql[:120])
            return "Operation blocked by security policy."

        try:
            engine = _get_engine()
            with engine.begin() as conn:
                result = conn.execute(text(sql))

                if sql.strip().upper().startswith("SELECT"):
                    rows = [dict(row._mapping) for row in result]
                    logger.info("SELECT returned %d rows.", len(rows))
                    return str(rows)
                else:
                    count = result.rowcount
                    logger.info("Write query affected %d rows.", count)
                    return f"OK - {count} row(s) affected."

        except SQLAlchemyError as exc:
            logger.error("SQL error: %s", exc)
            return f"Database error: {exc}"

    @mcp.tool()
    def list_db_tables() -> str:
        """
        List all available tables in the database.

        Returns:
            List of table names.
        """
        try:
            engine = _get_engine()
            tables = inspect(engine).get_table_names()
            logger.info("Tables found: %s", tables)
            return str(tables)
        except SQLAlchemyError as exc:
            logger.error("Error listing tables: %s", exc)
            return f"Database error: {exc}"
