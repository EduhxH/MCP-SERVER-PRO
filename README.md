<div align="center">

<br>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-000000?style=for-the-badge&logo=pinecone&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Server-orange?style=for-the-badge)
![FastMCP](https://img.shields.io/badge/FastMCP-Backend-009688?style=for-the-badge)
![UV](https://img.shields.io/badge/UV-Package%20Manager-646CFF?style=for-the-badge)
![Status](https://img.shields.io/badge/status-in%20development-yellow?style=for-the-badge)
[![SafeSkill 50/100](https://img.shields.io/badge/SafeSkill-50%2F100_Use%20with%20Caution-orange)](https://safeskill.dev/scan/eduhxh-mcp-server-pro)

<br>

# 🚀 MCP-SERVER-PRO

### A Professional Model Context Protocol (MCP) Server for AI Agents.
### Empowering local AI agents with enterprise-grade tool integration.

<br>

> 🇺🇸 This project is documented and implemented entirely in **American English**.

<br>

**[About](#-about-the-project)** &nbsp;•&nbsp; **[Features](#-features)** &nbsp;•&nbsp; **[Tech Stack](#%EF%B8%8F-tech-stack)** &nbsp;•&nbsp; **[Getting Started](#-getting-started)** &nbsp;•&nbsp; **[Configuration](#%EF%B8%8F-configuration)** &nbsp;•&nbsp; **[Structure](#-project-structure)**

<br>

</div>

---

<br>

## 🧩 &nbsp;About the Project

**MCP-SERVER-PRO** is a high-performance server built on the **Model Context Protocol (MCP)**. It acts as a bridge between LLMs (like Claude, GPT, or local models) and a suite of professional tools, enabling agents to interact with databases, spreadsheets, emails, and development environments seamlessly.

Designed to complement the [IA-agent-with-tools---](https://github.com/EduhxH/IA-agent-with-tools---) ecosystem, this server provides a robust, standardized interface for tool execution, ensuring reliability and security in agentic workflows.

<br>

---

<br>

## ✨ &nbsp;Features

<br>

<div align="center">

| Icon | Tool | Description |
|:---:|:---|:---|
| 🌲 | **Pinecone Connector** | Vector database integration for long-term memory and RAG |
| 📊 | **Excel Connector** | Direct manipulation of Excel spreadsheets for data analysis |
| 📧 | **Gmail Connector** | Secure interaction with Google Mail for communication automation |
| 💻 | **IDE Connector** | Deep integration with development environments for coding tasks |
| 🤖 | **Autonomy Tools** | Specialized tools for agent self-management and advanced logic |
| ⚡ | **FastMCP Core** | Built on FastMCP for high-speed, asynchronous tool handling |

</div>

<br>

---

<br>

## 🛠️ &nbsp;Tech Stack

<br>

<div align="center">

| Technology | Role |
|:---:|:---|
| [Python 3.11+](https://www.python.org/) | Core Programming Language |
| [FastMCP](https://github.com/jlowin/fastmcp) | MCP Server Framework |
| [UV](https://github.com/astral-sh/uv) | Ultra-fast Python package manager |
| [Pinecone](https://www.pinecone.io/) | Vector Database |
| [Google Cloud / Gmail](https://developers.google.com/gmail/api) | Email & Cloud Services Integration |
| [Microsoft Excel](https://www.microsoft.com/excel) | Spreadsheet Automation |

</div>

<br>

---

<br>

## 📦 &nbsp;Prerequisites

Before getting started, make sure you have the following installed:

- [Python 3.11+](https://www.python.org/)
- [UV](https://github.com/astral-sh/uv) — Ultra-fast Python package manager

<br>

---

<br>

## 🚀 &nbsp;Getting Started

<br>

**1 — Install UV (if not already installed)**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

<br>

**2 — Clone the repository**

```bash
git clone https://github.com/EduhxH/MCP-SERVER-PRO.git
cd MCP-SERVER-PRO/mcp-server-pro
```

<br>

**3 — Install dependencies**

```bash
uv sync
```

<br>

**4 — Run the server**

```bash
# Run on stdio transport (default for MCP clients)
uv run mcp-server
```

<br>

---

<br>

## ⚙️ &nbsp;Configuration

The server is configured via environment variables. Create a `.env` file in the root directory:

```env
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=your_env
GOOGLE_CLOUD_CREDENTIALS=path_to_json
# Add other service credentials as needed
```

<br>

---

<br>

## 📁 &nbsp;Project Structure

```
mcp-server-pro/
│
├── src/
│   ├── tools/              # Tool implementations (Pinecone, Excel, Gmail, etc.)
│   │   ├── autonomy_tools.py
│   │   ├── db_connector.py
│   │   ├── excel_connector.py
│   │   ├── gmail_connector.py
│   │   ├── ide_connector.py
│   │   └── pinecone_connector.py
│   ├── utils/              # Shared utilities and logging
│   ├── config.py           # Configuration management
│   └── server.py           # FastMCP server entry point
│
├── pyproject.toml          # Project metadata and dependencies
└── uv.lock                 # Deterministic lockfile
```

<br>

---

<br>

## 🧠 &nbsp;What I Learned

- Implementation of the **Model Context Protocol (MCP)** for standardized AI tool use.
- Building scalable **asynchronous connectors** for third-party APIs (Google Cloud, Pinecone).
- Managing complex tool registries using the **FastMCP** framework.
- Professional project structure and dependency management with **UV**.

<br>

---

<br>

<div align="center">

Made with 💜 by [EduhxH](https://github.com/EduhxH)

</div>

