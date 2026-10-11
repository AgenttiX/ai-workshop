# Extra: doing the exercises with another agent
The exercises are written for Claude Code, the workshop's main tool. Most of them work with any coding agent, for
example GitHub Copilot in VS Code (the backup option, see the [setup guide](../README.md)), OpenAI Codex or
Google Antigravity. The ideas are the same everywhere; the file names and commands differ.
This page says where. It was checked against each vendor's documentation on 11 October 2026; these tools change
fast, so follow the links when something doesn't match.

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
| GitHub Copilot in VS Code | [Customization overview](https://code.visualstudio.com/docs/copilot/customization/overview): instructions, skills, custom agents, hooks, MCP servers |
| OpenAI Codex | [Customization overview](https://learn.chatgpt.com/docs/customization/overview): `AGENTS.md`, skills, MCP; [subagents](https://developers.openai.com/codex/subagents) |
| Google Antigravity | [Rules](https://antigravity.google/docs/rules/) (`AGENTS.md`, `GEMINI.md`, `.agents/rules/`); skills, hooks, subagents and MCP are in the [agent docs](https://antigravity.google/docs/agent/) |
