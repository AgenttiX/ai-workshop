# Exercise 08: MCP (10 min, optional)
The [Model Context Protocol](https://modelcontextprotocol.io/) is a standard for connecting tools and data sources
to an agent: paper databases, reference managers, lab instruments, databases, your group's wiki.
The agent sees the server's tools and decides when to call them.

## Task
1. List the servers already configured: `claude mcp list` (or `/mcp` inside a session).
2. Add an arXiv server. The exact command depends on the server; for example, with the
   [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) package (needs [`uv`](https://docs.astral.sh/uv/)):
   ```bash
   claude mcp add arxiv -- uvx arxiv-mcp-server
   ```
   Check the server's README for the current install command before running it.
3. Start a session and ask:
   > Find the abstract of arXiv:1909.10040 and summarize the sound shell model in three sentences.

   Watch the tool calls: the agent picks the server's `search`/`download` tools by itself.
4. If you use Zotero, try [zotero-mcp](https://github.com/54yyyu/zotero-mcp), which gives the agent access to your library:
   ask it to find the papers in your library related to what you're working on.

## What to look for
- **Trust.** An MCP server runs code on your machine and its output goes into the agent's context.
  A malicious paper abstract could contain instructions for the agent (prompt injection). Only add servers you trust,
  and keep the permission prompts on for anything that writes.
- Scopes: `claude mcp add --scope project` writes to `.mcp.json` in the repository, so the whole group shares the server.
- [Documentation](https://code.claude.com/docs/en/mcp).
