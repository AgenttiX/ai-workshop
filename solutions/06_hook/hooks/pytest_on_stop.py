"""Stop hook: keep Claude working while the tests of one directory fail.

Usage in the hook configuration: ``python pytest_on_stop.py <directory with tests>``.
Claude Code runs the hook when Claude is about to finish its answer, and passes JSON on stdin.
If the tests fail, the hook prints a short summary to stderr and exits with code 2,
which makes Claude continue with the summary as its next instruction.
See https://code.claude.com/docs/en/hooks

To avoid an endless loop, the hook lets Claude stop when the input field ``stop_hook_active`` is true,
i.e. when Claude is already continuing because of a Stop hook. Claude therefore gets one extra attempt.
"""

import json
from pathlib import Path
import subprocess
import sys

#: Exit code that prevents Claude from stopping and shows it the hook's stderr
EXIT_KEEP_WORKING = 2
#: Exit code that shows an error notice to you but lets Claude stop
EXIT_HOOK_ERROR = 1
#: Exit codes of pytest, see https://docs.pytest.org/en/stable/reference/exit-codes.html
PYTEST_TESTS_FAILED = 1
PYTEST_NO_TESTS = 5
#: Number of lines of the pytest output that are shown to Claude
SUMMARY_LINES = 15


def main(argv: list[str]) -> int:
    """Run pytest on the directory given as the first argument and return the exit code of the hook."""
    if len(argv) != 1:
        print("Usage: pytest_on_stop.py <directory with tests>", file=sys.stderr)
        return EXIT_HOOK_ERROR
    hook_input = json.load(sys.stdin)
    if isinstance(hook_input, dict) and hook_input.get("stop_hook_active"):
        return 0
    test_dir = Path(argv[0])
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--tb=short", "--no-cov", "-p", "no:cacheprovider", str(test_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode in (0, PYTEST_NO_TESTS):
        return 0
    if result.returncode == PYTEST_TESTS_FAILED:
        summary = "\n".join(result.stdout.strip().splitlines()[-SUMMARY_LINES:])
        print(
            f"The tests in {test_dir} fail. Fix the code, not the tests, and run pytest again before you stop.\n"
            f"{summary}",
            file=sys.stderr,
        )
        return EXIT_KEEP_WORKING
    print(f"Running pytest failed:\n{result.stderr or result.stdout}", file=sys.stderr)
    return EXIT_HOOK_ERROR


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
