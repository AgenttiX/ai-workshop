"""Check that the environment of the workshop is set up correctly.

Run with ``python -m workshop.check``.
"""

from dataclasses import dataclass
import importlib.metadata
import platform
import shutil
import subprocess
import sys

#: Python packages that the exercises need
REQUIRED_PACKAGES: tuple[str, ...] = ("matplotlib", "numpy", "scipy", "pttools-gw", "pytest", "ruff", "pyrefly")
#: Command-line tools that the exercises need
REQUIRED_COMMANDS: tuple[str, ...] = ("git",)
#: Command-line tools that are useful but not strictly necessary,
#: e.g. because the VS Code extension may be used instead of the CLI
OPTIONAL_COMMANDS: tuple[str, ...] = ("claude", "code", "codium")
MIN_PYTHON: tuple[int, int] = (3, 12)


@dataclass(frozen=True)
class CheckResult:
    """The result of a single check."""

    name: str
    ok: bool
    detail: str
    required: bool = True

    def __str__(self) -> str:
        """Format the result as one line for the terminal."""
        mark = "OK  " if self.ok else ("FAIL" if self.required else "MISS")
        return f"[{mark}] {self.name}: {self.detail}"


def check_python(min_version: tuple[int, int] = MIN_PYTHON) -> CheckResult:
    """Check the Python version."""
    version = sys.version_info[:2]
    return CheckResult(
        "Python",
        version >= min_version,
        f"{platform.python_version()} at {sys.executable}",
    )


def check_package(name: str) -> CheckResult:
    """Check that a Python package is installed."""
    try:
        version = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return CheckResult(name, False, "not installed. Run: pip install -r requirements.txt")
    return CheckResult(name, True, version)


def check_command(name: str, required: bool = True) -> CheckResult:
    """Check that a command-line tool is available, and ask it for its version."""
    path = shutil.which(name)
    if path is None:
        return CheckResult(name, False, "not found on PATH", required)
    try:
        output = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=30, check=False)
        version = (output.stdout or output.stderr).strip().splitlines()[0] if (output.stdout or output.stderr) else ""
    except (OSError, subprocess.SubprocessError):
        version = ""
    return CheckResult(name, True, f"{version} at {path}".strip(), required)


def run_checks() -> list[CheckResult]:
    """Run all the checks."""
    results = [check_python()]
    results.extend(check_package(name) for name in REQUIRED_PACKAGES)
    results.extend(check_command(name) for name in REQUIRED_COMMANDS)
    results.extend(check_command(name, required=False) for name in OPTIONAL_COMMANDS)
    return results


def main() -> int:
    """Print the results and return the exit code."""
    results = run_checks()
    for result in results:
        print(result)
    failed = [result for result in results if result.required and not result.ok]
    if failed:
        print(f"\n{len(failed)} required check(s) failed. Please see the setup instructions in README.md.")
        return 1
    if not any(result.ok for result in results if result.name == "claude"):
        print("\nThe Claude Code CLI was not found. That's fine if you use the VS Code extension.")
    print("\nAll required checks passed. You're ready for the workshop!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
