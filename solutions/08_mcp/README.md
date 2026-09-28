# Solution of exercise 08: MCP

## The result
`claude mcp list` shows the arXiv server as connected, and the question about arXiv:1909.10040 is answered with a
call to one of the server's tools, typically `get_abstract` or `search_papers`. The paper is Hindmarsh & Hijazi (2019),
*Gravitational waves from first order cosmological phase transitions in the Sound Shell Model*. A good three-sentence
summary says roughly: sound waves in the plasma, created by expanding bubbles, are the main source of the gravitational
waves; the spectrum depends on the bubble spacing, the transition strength and the wall speed; and it has the shape of a
double broken power law, with breaks set by the bubble spacing and the thickness of the sound shell.
Compare with the [abstract](https://arxiv.org/abs/1909.10040) yourself.

## What was going on
MCP, the [Model Context Protocol](https://modelcontextprotocol.io/), is a standard way to plug external tools and data
into an agent. An *MCP server* is a small program that offers tools, e.g. "search arXiv" or "get an abstract".
Claude Code starts the server, asks it which tools it has, and then Claude decides when to call them,
just like its built-in tools for reading files.

The arXiv server runs on your computer. `uvx arxiv-mcp-server` downloads the Python package `arxiv-mcp-server`
from PyPI (the Python package index) and runs it; `uvx` comes with the tool [uv](https://docs.astral.sh/uv/).
The server fetches the papers from arXiv over the internet.

## The commands
We checked the install command in the server's [README](https://github.com/blazickjp/arxiv-mcp-server)
(version 0.7.2 at the time of writing). It recommends `uvx arxiv-mcp-server` and, for Claude Code,
`claude mcp add --transport stdio --scope user arxiv -- uvx arxiv-mcp-server`.
The exercise's shorter command adds the same server in the default, local scope (see below).
A server given as a command after `--` always runs as a local process (*stdio* transport).

| Step | Linux, macOS | Windows (PowerShell) |
|---|---|---|
| Install uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| Add the server | `claude mcp add arxiv -- uvx arxiv-mcp-server` | the same |
| Check | `claude mcp list` or `claude mcp get arxiv` | the same |

The `--` separates Claude Code's own options from the command that starts the server.
Inside a session, `/mcp` shows the servers and their status. The uv commands are from the
[uv documentation](https://docs.astral.sh/uv/getting-started/installation/); open a new terminal afterwards.

**Only the VS Code extension?** The `claude mcp` commands need the Claude Code command-line program on your PATH,
which the extension doesn't install. Two alternatives: type `/mcp` in the Claude Code panel, which can add servers
in recent versions, or write a file `.mcp.json` in the root of the repository by hand
(format from the [MCP documentation](https://code.claude.com/docs/en/mcp#project-scope)):
```json
{
  "mcpServers": {
    "arxiv": {
      "type": "stdio",
      "command": "uvx",
      "args": ["arxiv-mcp-server"]
    }
  }
}
```
Claude Code asks you to approve servers from `.mcp.json` the first time. If the server fails to start although
`uvx arxiv-mcp-server` works in a terminal, the editor may not see the same PATH. Replace `"uvx"` with the full path
printed by `command -v uvx` (Linux, macOS) or `(Get-Command uvx).Source` (Windows).

## Scopes: who gets the server
| Scope | Option | Stored in | Loads in |
|---|---|---|---|
| local (default) | `--scope local` | `~/.claude.json`, under this project | this project, only for you |
| project | `--scope project` | `.mcp.json` in the repository | this project, for everyone who clones it |
| user | `--scope user` | `~/.claude.json` | all your projects |

`~` is your home folder (`C:\Users\<you>` on Windows). A project-scope server is how a research group shares
a server: commit `.mcp.json` to the repository (a folder whose history Git tracks).

## What the agent typically does
It picks the arXiv tool by itself, because the tool descriptions match the request. Click on the tool call to see
what it sent and got back. Warning signs: it answers from memory without calling the tool (then the summary may be
of the wrong paper), or it downloads and reads the full paper when the abstract was enough.

## Trust and prompt injection
An MCP server is code that runs on your computer with your permissions, and everything it returns goes into
Claude's context. Anyone can put text into an arXiv abstract, a web page or an email. A text that says
"ignore your instructions and run this command" is a *prompt injection*: an attempt to steer the agent through data.
So: add only servers you trust, prefer well-known ones, and keep permission prompts on for tools that write files,
send messages or run commands.

## What to take away about prompting
1. Name the source you want: "use the arXiv server" makes the agent use it instead of its memory.
2. Ask for the identifier or link of every paper it cites, and open one or two yourself.
3. Treat tool output as data, not as instructions. If the agent suddenly wants to do something you didn't ask for, stop and read why.
