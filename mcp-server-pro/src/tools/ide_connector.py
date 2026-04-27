"""
ide_connector.py - MCP tools for interacting with the local filesystem.

Provides read/write access to project files so the agent can inspect
source code, apply patches, and list directory contents.
"""
import os
from pathlib import Path

from src.utils.logging_config import logger

# Safety guard: restrict all file operations to this root.
# Override via the WORKSPACE_ROOT environment variable if needed.
_WORKSPACE = Path(os.getenv("WORKSPACE_ROOT", ".")).resolve()


def _safe_path(relative: str) -> Path:
    """Resolve a relative path and ensure it stays inside the workspace."""
    resolved = (_WORKSPACE / relative).resolve()
    if not resolved.is_relative_to(_WORKSPACE):
        raise PermissionError(f"Path '{relative}' is outside the workspace root.")
    return resolved


def register(mcp):

    @mcp.tool()
    def read_file(path: str) -> str:
        """
        Read the contents of a file inside the workspace.

        Args:
            path: Relative path to the file from the workspace root.

        Returns:
            File contents as a UTF-8 string, or an error message.
        """
        try:
            target = _safe_path(path)
            content = target.read_text(encoding="utf-8")
            logger.info("Read file: %s (%d chars)", target, len(content))
            return content
        except PermissionError as exc:
            logger.warning("Path traversal blocked: %s", exc)
            return f"Access denied: {exc}"
        except FileNotFoundError:
            return f"File not found: {path}"
        except Exception as exc:
            logger.error("Error reading file %s: %s", path, exc)
            return f"Error reading file: {exc}"

    @mcp.tool()
    def write_file(path: str, content: str) -> str:
        """
        Write content to a file inside the workspace.
        Creates the file and any missing parent directories if needed.

        Args:
            path:    Relative path to the file from the workspace root.
            content: UTF-8 string content to write.

        Returns:
            Confirmation string or an error message.
        """
        try:
            target = _safe_path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            logger.info("Wrote file: %s (%d chars)", target, len(content))
            return f"File written successfully: {path}"
        except PermissionError as exc:
            logger.warning("Path traversal blocked: %s", exc)
            return f"Access denied: {exc}"
        except Exception as exc:
            logger.error("Error writing file %s: %s", path, exc)
            return f"Error writing file: {exc}"

    @mcp.tool()
    def list_directory(path: str = ".") -> str:
        """
        List the contents of a directory inside the workspace.

        Args:
            path: Relative path to the directory. Defaults to workspace root.

        Returns:
            Newline-separated list of entries, or an error message.
        """
        try:
            target = _safe_path(path)
            if not target.is_dir():
                return f"Not a directory: {path}"
            entries = sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name))
            lines = [f"{'DIR ' if e.is_dir() else 'FILE'} {e.name}" for e in entries]
            logger.info("Listed directory: %s (%d entries)", target, len(lines))
            return "\n".join(lines) if lines else "Empty directory."
        except PermissionError as exc:
            logger.warning("Path traversal blocked: %s", exc)
            return f"Access denied: {exc}"
        except Exception as exc:
            logger.error("Error listing directory %s: %s", path, exc)
            return f"Error listing directory: {exc}"
