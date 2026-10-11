# Solution of exercise 06: A hook

## The result
[`settings.json`](./settings.json) is a complete `.claude/settings.json` for this repository on Linux and macOS:
the existing permission allow-list plus the `PostToolUse` hook. On Windows, the only difference is the Python path:
`${CLAUDE_PROJECT_DIR}/venv/Scripts/python.exe` instead of `${CLAUDE_PROJECT_DIR}/venv/bin/python`,
as in [`settings.windows.snippet.json`](../../exercises/06_hook/settings.windows.snippet.json).

When it works, asking for `exercises/06_hook/sloppy.py` goes like this: Claude writes the file, the hook reports
`F401 'sys' imported but unused` (and usually a missing docstring), and Claude edits the file again without being asked.
The second edit triggers the hook again, which now stays silent.

## What was going on
A *hook* is a command that Claude Code itself runs when an event happens. The model doesn't decide whether it runs.
Here the event is `PostToolUse`, i.e. right after a tool call, and the `matcher` `Edit|Write` limits it to the two
file-editing tools. A *tool* is an action the agent can take, such as reading a file, editing a file or running a command.

How [`ruff_on_edit.py`](../../exercises/06_hook/hooks/ruff_on_edit.py) works:
1. Claude Code sends the tool call as JSON on the hook's standard input (stdin). The path of the edited file is in
   `tool_input.file_path`, always absolute ([documentation](https://code.claude.com/docs/en/hooks#posttooluse-input)).
2. If the file isn't an existing `.py` file, the hook exits with 0: nothing happens.
3. Otherwise it runs `python -m ruff check <file>` with the same Python that runs the hook, i.e. the one in `venv/`.
4. If ruff finds problems, the hook prints them to its error output (stderr) and exits with code 2.

The exit code decides what happens ([documentation](https://code.claude.com/docs/en/hooks#exit-code-2-behavior-per-event)):

| Exit code | Effect for `PostToolUse` |
|---|---|
| 0 | Nothing is shown. |
| 2 | stderr is shown to Claude. The edit has already happened, so Claude sees the problems and can fix them. |
| anything else | A short "hook error" notice is shown to you, not to Claude. The script uses 1 when ruff itself can't run. |

The settings use the *exec form*: `command` is the program and `args` its arguments. Claude Code starts the program
directly, without a shell, so the same configuration works on Linux, macOS and Windows.
`${CLAUDE_PROJECT_DIR}` is replaced by the folder where the session started, so the hook works from any subfolder.

## Installing it
The simplest way is to copy the snippet to `.claude/settings.local.json`, as in the exercise: Claude Code combines it with
the shared `.claude/settings.json`. Alternatively, merge the `hooks` block into `.claude/settings.json` next to `"permissions"`. According to the current [documentation](https://code.claude.com/docs/en/settings),
Claude Code reloads settings files while it runs, so a restart shouldn't be needed; restarting doesn't hurt.
`/hooks` lists the active hooks (in the VS Code extension also the **Hooks** entry of the Customize section).

To test the hook without Claude, create a file with an unused import and pipe JSON into the script, from the workshop folder:

| System | Command |
|---|---|
| Linux, macOS | `echo '{"tool_input": {"file_path": "exercises/06_hook/sloppy.py"}}' \| venv/bin/python exercises/06_hook/hooks/ruff_on_edit.py; echo $?` |
| Windows (PowerShell) | `'{"tool_input": {"file_path": "exercises/06_hook/sloppy.py"}}' \| venv\Scripts\python.exe exercises\06_hook\hooks\ruff_on_edit.py; $LASTEXITCODE` |

It should print the ruff output and `2`. A clean file or a `.txt` file prints only `0`.

## Things to know
- The hook lints every Python file Claude edits, with the repository's ruff settings. That includes files you didn't
  ask about: editing `exercises/04_ai_ready/fitting.py` triggers its 22 lint problems, and Claude will want to fix them.
- `~/.claude/settings.json` applies to all your projects. The paths above point into this repository, so as a personal
  hook they would fail in other projects. For personal use, put the script in `~/.claude/hooks/` and use absolute paths.

## Bonus: a Stop hook that runs the tests
[`hooks/pytest_on_stop.py`](./hooks/pytest_on_stop.py) runs `pytest` on one directory when Claude is about to stop.
If tests fail, it prints the last lines of the pytest output to stderr and exits with 2, which for `Stop` means
"don't stop, continue with this message". Add it to `"hooks"` in `.claude/settings.json` (Linux/macOS shown;
on Windows use `venv/Scripts/python.exe`):
```json
"Stop": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "${CLAUDE_PROJECT_DIR}/venv/bin/python",
        "args": [
          "${CLAUDE_PROJECT_DIR}/solutions/06_hook/hooks/pytest_on_stop.py",
          "${CLAUDE_PROJECT_DIR}/exercises/01_fix_the_bug"
        ]
      }
    ]
  }
]
```
- It tests one directory, not the whole repository: the full `pytest` run takes minutes because of PTtools.
- Endless loops: we checked the [hooks documentation](https://code.claude.com/docs/en/hooks#stop-input). The Stop input
  has a field `stop_hook_active`, which is `true` when Claude is already continuing because of a Stop hook.
  The script lets Claude stop in that case, so Claude gets one extra attempt. Without the check, Claude Code itself
  ends the turn after eight blocks in a row (adjustable with `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`).
- While exercise 01 is unsolved, this hook blocks *every* stop once, whatever you asked. Enable it only while you work on that exercise.
- The tests of the scripts are in [`test_hooks.py`](./test_hooks.py).

## What the agent typically does
It usually treats hook output like any other error message: reads it, fixes the file, moves on.
Warning signs: it disables the hook or edits `.claude/settings.json` to get rid of it, or it adds `# noqa` comments
instead of fixing the code. Keep permission prompts on for edits to `.claude/`.

## What to take away about prompting
1. A hook replaces a prompt you would otherwise repeat forever ("run ruff after every edit"), and it never forgets.
2. Use hooks for what must *always* happen, and prompts or skills for what needs judgement.
3. The message a hook sends is a prompt too: make it say what to do ("Fix the code, not the tests").
