# Exercise 08: MCP (10 min, optional)
The [Model Context Protocol](https://modelcontextprotocol.io/) is a standard for connecting tools and data sources to an agent: paper databases, reference managers, lab instruments, databases, your group's wiki. The agent sees the server's tools and decides when to call them.

## Task

### 1. List the configured servers
Run `claude mcp list` in the terminal (or type `/mcp` inside a session).

(With OpenCode: `opencode mcp list`, or `/mcps` inside a session — it shows the connection state.)

### 2. Add an arXiv server
The exact command depends on the server; here we use the [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) package. Check its README for the current install command before you run the one below, as these change.

**a. Install `uv`** if `uv --version` doesn't print a version. [`uv`](https://docs.astral.sh/uv/) is a Python package runner that starts the server. Run the command for your system, then close the terminal and open a new one.

**Linux and macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**b. Add the server** (the same command on every system):

```bash
claude mcp add arxiv -- uvx arxiv-mcp-server
```

(With OpenCode: `opencode mcp add arxiv -- uvx arxiv-mcp-server`. Project scope is the default; add `--global` to make it personal instead. The stored config lives in `opencode.json(c)`, whose `mcp.servers` section you can also edit by hand.)

### 3. Use it
Start a session and ask:

> Find the abstract of arXiv:1909.10040 and summarize the sound shell model in three sentences.

Watch the tool calls: the agent picks the server's tools (e.g. `search_papers`, `get_abstract`, `download_paper`) by itself.

### 4. Bonus: Zotero
If you use Zotero, try [zotero-mcp](https://github.com/54yyyu/zotero-mcp), which gives the agent access to your library: ask it to find the papers in your library related to what you're working on.

## What to look for
- **Trust.** An MCP server runs code on your machine and its output goes into the agent's context. A malicious paper abstract could contain instructions for the agent (prompt injection). Only add servers you trust, and keep the permission prompts on for anything that writes.
- Scopes: `claude mcp add --scope project` writes to `.mcp.json` in the repository, so the whole group shares the server.
- [Documentation](https://code.claude.com/docs/en/mcp).
