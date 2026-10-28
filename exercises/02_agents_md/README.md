# Exercise 02: Write an AGENTS.md (10 min)
`pendulum_lab/` is a small analysis project of the kind that lives in every research group: a script, a data file, a run script, and conventions that exist only in someone's head. It has no `AGENTS.md`, so an agent working on it has to guess.

## Task

### 1. Let Claude write a draft
Open a Claude Code session *in `exercises/02_agents_md/pendulum_lab/`*. In the terminal, from the repository folder, run (the same in PowerShell):

```bash
cd exercises/02_agents_md/pendulum_lab
claude
```

In Claude Code, type `/init`. It reads the project and writes a draft `CLAUDE.md`.

(With OpenCode there is no `/init`: instead, ask the agent to "write a draft AGENTS.md for this project". OpenCode reads `AGENTS.md` natively, so in step 5 you skip the rename and the `CLAUDE.md` shim.)

You can also run `/init` in the Claude Code extension of VS Code. The extension works in the folder that is open in VS Code, so first open `pendulum_lab` in a new window: **File → New Window**, then **File → Open Folder…** and choose `exercises/02_agents_md/pendulum_lab` in the workshop folder. Then open Claude Code in that window and type `/init`.

### 2. Read the draft critically
Which of the unwritten conventions did it find, and which did it miss?

- The units are in the column names of the data file.
- The analysis is run with `python run.py`, which uses the Python of the virtual environment.
- The results go to `results/`, which is not tracked in Git.
- The uncertainties in the data are 1σ.
- The plots should use the workshop style (`workshop.plotting`).

### 3. Fix it by hand
Fix and complete the file by hand. Keep it short: an `AGENTS.md` is read by the agent on *every* session, so it costs context.

### 4. Verify
Start a new session (`/clear`) and ask

> How do I run the analysis, what are the units in the data, and where do the results go?

A good `AGENTS.md` makes the answer correct without any file reads beyond it.

### 5. Rename it to AGENTS.md
Rename `CLAUDE.md` to `AGENTS.md` (in the VS Code Explorer: right-click the file → **Rename**), then create a new file `CLAUDE.md` containing only the line `@AGENTS.md`, like the root of this repository does. `AGENTS.md` is the tool-agnostic convention that other coding agents (Copilot, Codex, OpenCode, Antigravity) read directly. Recent versions of Claude Code read `AGENTS.md` directly too; the `@AGENTS.md` line imports it into `CLAUDE.md`, so that it works in every version.

(If you started with OpenCode you already wrote `AGENTS.md` and need none of this.)

## What to look for
- `/init` is a starting point, not an answer. The valuable part is what only you know.
- Claude Code also loads the `CLAUDE.md` files of the folders above the one you started it in, here the workshop's own. That's why the session in `pendulum_lab/` may already know a few things about the workshop.
- What belongs in `AGENTS.md`: commands, structure, conventions, what *not* to do. What doesn't: anything the agent can read from the code itself.
