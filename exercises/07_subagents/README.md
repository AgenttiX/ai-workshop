# Exercise 07: A subagent (10 min)
A *subagent* is a separate agent with its own context window, its own instructions and its own tool permissions, that the main agent can delegate to. Use them for parallel work, for specialists, and to keep noisy tasks (reading many files, running long tests) out of the main context.

## Task

### 1. Copy the agent
Copy the template into the agents directory of this repository. In the terminal, in the workshop folder, run the commands for your system:

**Linux and macOS:**

```bash
mkdir -p .claude/agents
cp exercises/07_subagents/agents/physics-reviewer.md .claude/agents/
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force .claude\agents
Copy-Item exercises\07_subagents\agents\physics-reviewer.md .claude\agents\
```

Read it: the frontmatter defines the name, when to use it, the tools it may use and the model; the body is its system prompt.

### 2. Restart Claude Code and ask for a review
Restart Claude Code so that it finds the agent: a running session doesn't notice a `.claude/agents/` folder that didn't exist when it started, and `/clear` isn't enough. In the terminal, quit Claude Code and start it again with these two commands, one at a time:

```text
/exit
claude
```

In VS Code, press Ctrl+Shift+P (Cmd+Shift+P on a Mac), run **Developer: Reload Window** and open Claude Code again. Then ask for a review:

> Use the physics-reviewer agent to review exercises/04_ai_ready/fitting.py (or your solution of exercise 04).

The main agent launches the reviewer, which reads the code and reports back. Note that you only see the report, not the reviewer's file reads — that's the point: its context is separate.

### 3. Two reviews in parallel
Ask for two reviews in parallel, e.g. the physics reviewer and a general code reviewer, and compare.

### 4. Bonus: a checklist of your own
Give the reviewer a checklist of your own field's common mistakes (units, signs, conventions, limits).

## What to look for
- The built-in `Explore` and `Plan` agents already exist; custom ones add domain knowledge.
- Subagents cost tokens: each starts fresh and re-reads what it needs. Use them for tasks that produce a *short* result from a *long* investigation.
- [Documentation](https://code.claude.com/docs/en/sub-agents).
