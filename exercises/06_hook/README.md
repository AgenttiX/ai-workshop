# Exercise 06: A hook (10 min)
A *hook* is a shell command that the harness runs on an event — before or after a tool call, when the session
starts, when the agent wants to stop, and so on. Unlike a skill, the model can't forget or skip it.

## Task
1. Look at `hooks/ruff_on_edit.py`. It receives the tool call as JSON on stdin, and if the edited file is Python,
   it runs `ruff check` on it. If ruff finds problems, the hook exits with code 2, which sends its output back to the agent.
2. Install it as a `PostToolUse` hook for `Edit` and `Write`: copy the `hooks` block into `.claude/settings.json`
   of this repository (or into `~/.claude/settings.json` to make it personal).
   On Linux and macOS, copy it from `settings.snippet.json`; on Windows, from `settings.windows.snippet.json`.
   The two differ only in the path of the Python of the virtualenv.
   Restart Claude Code, as the settings are read at startup. `/hooks` shows the active hooks.
3. Test it by asking for deliberately sloppy code:
   > Write a script exercises/06_hook/sloppy.py that imports os, sys and json but uses only one of them.

   The hook complains about the unused imports, and the agent should fix them without being asked.
4. Bonus: add a `Stop` hook that runs `pytest` and blocks stopping if the tests fail. This is the idea behind
   Hippe's "Ralph loop" shown in the showcase: an agent that can't stop until the task is done.

## What to look for
- Hooks are deterministic. Use them for things that must *always* happen (formatting, linting, secrets scanning,
  notifications); use skills for things that need judgement.
- Exit code 2 = "block and tell the agent". Other non-zero codes only show the output to you.
- The [hooks documentation](https://code.claude.com/docs/en/hooks) lists all the events and the JSON they receive.
