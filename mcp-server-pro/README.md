# MCP Server — IA Agent with Tools

MCP server for [IA Agent with Tools](https://github.com/EduhxH/IA-agent-with-tools---).  
Exposes database, filesystem, Excel, and autonomous goal management as MCP tools.

## Structure

```
mcp-server/
├── src/
│   ├── server.py              # Entry point - registers all tools and starts server
│   ├── config.py              # Environment variable loader
│   ├── tools/
│   │   ├── db_connector.py    # SQL query execution (SQLAlchemy)
│   │   ├── excel_connector.py # Live Excel read/write (xlwings, optional)
│   │   ├── ide_connector.py   # Filesystem read/write inside workspace
│   │   ├── autonomy_tools.py  # Goal registration and self-correction
│   │   └── mcp_client.py      # Async client used by the AI agent
│   └── utils/
│       └── logging_config.py  # Structured stderr logging
├── .env.example
├── .gitignore
└── pyproject.toml
```

## Setup

```bash
cp .env.example .env
# Edit .env with your DATABASE_URL and other settings

uv sync
# For Excel support:
uv sync --extra excel
```

## Running

```bash
uv run mcp-server
```

## Tools

| Tool | Module | Description |
|---|---|---|
| `run_db_query` | db_connector | Execute SELECT / INSERT / UPDATE / DELETE |
| `list_db_tables` | db_connector | List all tables in the database |
| `read_excel_cell` | excel_connector | Read a cell from the active workbook |
| `update_excel_cell` | excel_connector | Write a value to a cell |
| `list_excel_sheets` | excel_connector | List all sheets in the active workbook |
| `read_file` | ide_connector | Read a file inside the workspace |
| `write_file` | ide_connector | Write a file inside the workspace |
| `list_directory` | ide_connector | List directory contents |
| `register_autonomous_goal` | autonomy_tools | Register a long-term goal |
| `list_autonomous_goals` | autonomy_tools | List all registered goals |
| `complete_goal` | autonomy_tools | Mark a goal as completed |
| `run_self_correction` | autonomy_tools | Analyze an error and suggest a fix |

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./database.db` | SQLAlchemy connection string |
| `MCP_SERVER_NAME` | `IA-Agent-MCP` | Server name shown to the client |
| `MCP_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `WORKSPACE_ROOT` | `.` | Root directory the IDE connector can access |
