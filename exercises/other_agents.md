# Extra: doing the exercises with another agent
The exercises are written primarily for Claude Code. Most of them work with any coding agent, for example OpenCode (which this repository is developed with; see [its section](#opencode)), GitHub Copilot in VS Code (the backup option, see the [setup guide](../README.md)), OpenAI Codex or Google Antigravity. The ideas are the same everywhere; the file names and commands differ. This page says where. It was checked against each vendor's documentation on 11 October 2026 (OpenCode on 28 October 2026); these tools change fast, so follow the links when something doesn't match.

## OpenCode
[OpenCode](https://opencode.ai/) is one of the harnesses that this workshop was developed with. Start it in the terminal with `opencode`, or from its [VS Code extension](https://marketplace.visualstudio.com/items?itemName=sst-dev.opencode). OpenCode reads `AGENTS.md` by itself (no `CLAUDE.md` needed), and it accepts several of the same files as Claude Code: the project skills of `.claude/skills/` and `.agents/skills/`, locally installed plugins from `.opencode/plugins/`, and MCP servers. The slash commands differ: a new conversation is `/new`, not `/clear`.

| Exercise | With OpenCode |
|---|---|
| 00, 01, 03, 04 | Work as written: give the task in the agent's chat and read every change before you accept it. Planning first: run `/agents` and switch to the `plan` agent. To undo the latest change, `/undo`. |
| 02 AGENTS.md | OpenCode reads `AGENTS.md` natively, so skip the rename step and skip the `CLAUDE.md` shim. There is no `/init`: ask the agent to write a draft `AGENTS.md`, then edit it by hand. |
| 05 Skill | The `.claude/skills/` copy of the exercise works as it is: OpenCode reads that folder as a compatibility source. Don't run `/reload-skills`: OpenCode rereads skills from the files after a save (`/reload` forces it). Start a new session with `/new`. |
| 06 Hook | Hooks are plugins: copy `exercises/06_hook/opencode_ruff_on_edit/` to `.opencode/plugins/` (run `mkdir -p .opencode/plugins` first). There is no exit code 2 and no blocking; instead the plugin appends ruff's findings to the edit's result, so the agent reads them and fixes the file. |
| 07 Subagent | Copy `exercises/07_subagents/agents/opencode/physics-reviewer.md` to `.opencode/agents/`. The frontmatter differs: `mode: subagent` and `permissions` rules instead of a `tools` list, and no `model` line (it inherits the main agent's model). No restart is needed: OpenCode rereads agents from the files. |
| 08 MCP | The same steps with `opencode mcp list` and `opencode mcp add arxiv -- uvx arxiv-mcp-server` (`--global` to make it personal instead of project-local). `/mcps` shows the connection state. |
| 09 Local models | Skip the environment-variable block of step 3: add a provider to `opencode.json(c)` instead, then select the model with `/models`. That's a separate section in the [exercise README](./09_local_models/README.md). |
| 10 Your own project | The checklist works as written: OpenCode reads `AGENTS.md`, plan mode is the `plan` agent (`/agents`), `.claude/settings.json` becomes `permissions` rules in `opencode.json(c)`, and this repository has one as a starting point. |

## Exercise by exercise
| Exercise | With another agent |
|---|---|
| 00, 01, 03, 04, 10 | Work as written: give the task in the agent's chat and read every change before you accept it. |
| 02 AGENTS.md | Codex, Copilot and Antigravity all read an `AGENTS.md` in the project. `/init` is Claude Code's command; elsewhere, ask the agent to write an `AGENTS.md` for the project. |
| 05 Skill | Codex and Copilot use the same idea, a folder with a `SKILL.md`; Codex reads project skills from `.agents/skills/`. Antigravity has skills too. For Copilot and Antigravity, see their skills pages below. |
| 06 Hook | Copilot, Codex and Antigravity have hooks too, with their own configuration formats: see their hooks pages. The hook script itself (`ruff_on_edit.py`) can stay as it is. |
| 07 Subagent | Copilot has custom agents in `.github/agents/<name>.agent.md`; Codex and Antigravity have subagents: see their pages. |
| 08 MCP | All of them can use MCP servers; only the configuration differs. |
| 09 Local models | Specific to Claude Code. The other tools have their own ways to use a local or custom model. |

## Where to read more
| Tool | Documentation |
|---|---|
| Claude Code | [code.claude.com/docs](https://code.claude.com/docs) |
| OpenCode | [opencode.ai/v2/docs](https://opencode.ai/v2/docs/): `AGENTS.md`, skills, agents, plugins (hooks), MCP servers, providers |
| GitHub Copilot in VS Code | [Customization overview](https://code.visualstudio.com/docs/copilot/customization/overview): instructions, skills, custom agents, hooks, MCP servers |
| OpenAI Codex | [Customization overview](https://learn.chatgpt.com/docs/customization/overview): `AGENTS.md`, skills, MCP; [subagents](https://developers.openai.com/codex/subagents) |
| Google Antigravity | [Rules](https://antigravity.google/docs/rules/) (`AGENTS.md`, `GEMINI.md`, `.agents/rules/`); skills, hooks, subagents and MCP are in the [agent docs](https://antigravity.google/docs/agent/) |
