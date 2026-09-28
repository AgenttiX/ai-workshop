"""PostToolUse hook: lint a Python file that Claude has just edited and report the problems back to Claude.

Claude Code passes the tool call to the hook as JSON on stdin. If the edited file is a Python file
and ruff finds problems in it, the hook prints them to stderr and exits with code 2.
For a PostToolUse hook, exit code 2 shows stderr to Claude, so that it can fix the problems.
Any other non-zero exit code only shows a short error notice to you.
See https://code.claude.com/docs/en/hooks

The hook uses only the standard library, so it runs with any Python 3.12. Ruff is run as ``python -m ruff``
with the same interpreter that runs the hook, which is the one in the workshop's venv.
"""

import json
from pathlib import Path
import subprocess
import sys

#: Exit code that shows the hook's stderr to Claude
EXIT_FEEDBACK_TO_CLAUDE = 2
#: Exit code that shows an error notice to you but not to Claude
EXIT_HOOK_ERROR = 1


def edited_python_file(hook_input: object) -> Path | None:
    """Return the edited file if it is an existing Python file, otherwise None.

    :param hook_input: the JSON that Claude Code passed to the hook
    """
    if not isinstance(hook_input, dict):
        return None
    tool_input = hook_input.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    file_path = tool_input.get("file_path")
    if not isinstance(file_path, str):
        return None
    path = Path(file_path)
    return path if path.suffix == ".py" and path.is_file() else None


def main() -> int:
    """Run ruff on the edited file and return the exit code of the hook."""
    path = edited_python_file(json.load(sys.stdin))
    if path is None:
        return 0
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", str(path)], capture_output=True, text=True, check=False
    )
    if result.returncode == 0:
        return 0
    # Ruff exits with 1 when it finds problems. Anything else (e.g. "No module named ruff") is a problem
    # of the setup, which Claude can't fix by editing the file.
    if result.returncode == 1 and result.stdout:
        print(f"ruff found problems in {path}:\n{result.stdout}", file=sys.stderr)
        return EXIT_FEEDBACK_TO_CLAUDE
    print(f"Running ruff failed: {result.stderr or result.stdout}", file=sys.stderr)
    return EXIT_HOOK_ERROR


if __name__ == "__main__":
    sys.exit(main())
