"""
excel_connector.py - MCP tool for interacting with Excel via xlwings.

Requires Excel to be installed and a workbook open on the host machine.
xlwings is an optional dependency: install with `pip install mcp-server[excel]`.
"""
from src.utils.logging_config import logger


def register(mcp):

    @mcp.tool()
    def read_excel_cell(cell: str, sheet: str = "") -> str:
        """
        Read the value of a cell from the currently active Excel workbook.

        Args:
            cell:  Cell address in A1 notation, e.g. "B4".
            sheet: Sheet name. Defaults to the active sheet if not provided.

        Returns:
            Cell value as a string, or an error message.
        """
        try:
            import xlwings as xw
            wb = xw.apps.active.books.active
            ws = wb.sheets[sheet] if sheet else wb.sheets.active
            value = ws.range(cell).value
            logger.info("Read cell %s from sheet '%s': %s", cell, ws.name, value)
            return str(value)
        except ImportError:
            return "xlwings is not installed. Run: pip install mcp-server[excel]"
        except Exception as exc:
            logger.error("Error reading cell %s: %s", cell, exc)
            return f"Error reading cell: {exc}"

    @mcp.tool()
    def update_excel_cell(cell: str, value: str, sheet: str = "") -> str:
        """
        Write a value to a cell in the currently active Excel workbook.

        Args:
            cell:  Cell address in A1 notation, e.g. "B4".
            value: Value to write (will be cast to the appropriate type by Excel).
            sheet: Sheet name. Defaults to the active sheet if not provided.

        Returns:
            Confirmation string or an error message.
        """
        try:
            import xlwings as xw
            wb = xw.apps.active.books.active
            ws = wb.sheets[sheet] if sheet else wb.sheets.active
            ws.range(cell).value = value
            logger.info("Updated cell %s on sheet '%s' to '%s'.", cell, ws.name, value)
            return f"Cell {cell} on sheet '{ws.name}' updated to '{value}'."
        except ImportError:
            return "xlwings is not installed. Run: pip install mcp-server[excel]"
        except Exception as exc:
            logger.error("Error updating cell %s: %s", cell, exc)
            return f"Error updating cell: {exc}"

    @mcp.tool()
    def list_excel_sheets() -> str:
        """
        List all sheet names in the currently active Excel workbook.

        Returns:
            List of sheet names, or an error message.
        """
        try:
            import xlwings as xw
            wb = xw.apps.active.books.active
            sheets = [s.name for s in wb.sheets]
            logger.info("Sheets in workbook: %s", sheets)
            return str(sheets)
        except ImportError:
            return "xlwings is not installed. Run: pip install mcp-server[excel]"
        except Exception as exc:
            logger.error("Error listing sheets: %s", exc)
            return f"Error listing sheets: {exc}"
