# Exercise 06: A hook (10 min)
A *hook* is a shell command that the harness runs on an event — before or after a tool call, when the session starts, when the agent wants to stop, and so on. Unlike a skill, the model can't forget or skip it.

## Task

### 1. Read the hook
Look at `hooks/ruff_on_edit.py`. It receives the tool call as JSON on stdin, and if the edited file is Python, it runs `ruff check` on it. If ruff finds problems, the hook exits with code 2, which sends its output back to the agent.

### 2. Install it
Install it as a `PostToolUse` hook for `Edit` and `Write`, i.e. a hook that runs after every file edit. The easiest place is your own local settings file `.claude/settings.local.json`, which Claude Code combines with the shared `.claude/settings.json` and which Git ignores. The snippets `settings.snippet.json` (Linux and macOS) and `settings.windows.snippet.json` (Windows) contain the hook; they differ only in the path of the Python of the virtual environment.

**a. Check whether you already have the file.** If you answered "Yes, and don't ask again" to a permission prompt in an earlier exercise, Claude Code saved that choice there, and copying the snippet over it would erase it. In the terminal, in the workshop folder, run `ls .claude` (the same on every system) and look for `settings.local.json`.

**b. If it's not there, copy the snippet** with the command for your system:

| System | Command |
|---|---|
| Linux and macOS | `cp exercises/06_hook/settings.snippet.json .claude/settings.local.json` |
| Windows (PowerShell) | `Copy-Item exercises\06_hook\settings.windows.snippet.json .claude\settings.local.json` |

**If it's already there,** don't copy anything. Ask Claude instead:

> Merge the hooks block of exercises/06_hook/settings.snippet.json into .claude/settings.local.json and keep everything that's already there.

(On Windows, say `settings.windows.snippet.json`.) Claude Code reloads settings while it runs, so no restart is needed. `/hooks` shows the active hooks.

### 3. Test it
Ask for deliberately sloppy code:

> Write a script exercises/06_hook/sloppy.py that imports os, sys and json but uses only one of them.

The hook complains about the unused imports, and the agent should fix them without being asked.

### 4. Bonus: a Stop hook
Add a `Stop` hook that runs `pytest` and blocks stopping if the tests fail: an agent that can't stop until the task is done (the idea behind the so-called Ralph loop).

## What to look for
- Hooks are deterministic. Use them for things that must *always* happen (formatting, linting, secrets scanning, notifications); use skills for things that need judgement.
- Exit code 2 = "block and tell the agent". Other non-zero codes only show the output to you.
- The [hooks documentation](https://code.claude.com/docs/en/hooks) lists all the events and the JSON they receive.
