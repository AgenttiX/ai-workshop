"""Check that the environment of the workshop is set up correctly, and set it up if it isn't.

Run in the root directory of the repository::

    python3 -m workshop.check    # Linux and macOS
    py -3 -m workshop.check      # Windows

If you run it outside a virtual environment, it offers to create one in ``.venv/``,
installs the requirements into it, runs the checks there and tells you how to activate it.
Run it again inside the activated virtual environment to confirm that everything works.
"""

# Postponed annotations: an old Python (e.g. 3.9) must get as far as the friendly version check.
from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib.metadata
import os
from pathlib import Path
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
#: VS Code extensions that the workshop uses
VSCODE_EXTENSIONS: tuple[str, ...] = ("anthropic.claude-code", "ms-python.python")
MIN_PYTHON: tuple[int, int] = (3, 12)
#: How to run the setup on this system (Ubuntu has no `python` outside a virtual environment)
SETUP_COMMAND: str = ("py -3" if os.name == "nt" else "python3") + " -m workshop.check --setup"

REPO_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = REPO_DIR / ".venv"
IS_WINDOWS = os.name == "nt"


@dataclass(frozen=True)
class CheckResult:
    """The result of a single check."""

    name: str
    ok: bool
    detail: str
    required: bool = True

    def __str__(self) -> str:
        """Format the result as one line for the terminal."""
        mark = "OK  " if self.ok else ("FAIL" if self.required else "WARN")
        return f"[{mark}] {self.name}: {self.detail}"


# ---------------------------------------------------------------------------- virtual environment


def in_virtual_environment() -> bool:
    """Tell whether Python runs in a virtual environment (venv) or a conda environment."""
    return sys.prefix != sys.base_prefix or (Path(sys.prefix) / "conda-meta").is_dir()


def venv_python(venv_dir: Path = VENV_DIR, windows: bool = IS_WINDOWS) -> Path:
    """Return the path of the Python interpreter of a virtual environment.

    :param venv_dir: the directory of the virtual environment
    :param windows: whether the paths are those of Windows
    """
    return venv_dir / "Scripts" / "python.exe" if windows else venv_dir / "bin" / "python"


def activation_instructions(windows: bool = IS_WINDOWS) -> str:
    """Explain how to activate the virtual environment in ``.venv/``, as text for the terminal.

    :param windows: whether to give the commands for Windows
    """
    if windows:
        commands = (
            "  PowerShell (the default terminal of VS Code):  .venv\\Scripts\\Activate.ps1\n"
            "  Command Prompt:                                .venv\\Scripts\\activate.bat\n"
            "  Git Bash:                                      source .venv/Scripts/activate\n"
            "If PowerShell says that running scripts is disabled, run this once and try again:\n"
            "  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned\n"
        )
    else:
        commands = "  source .venv/bin/activate\n"
    return (
        "To activate the virtual environment in a terminal, run in the workshop directory:\n"
        f"{commands}"
        "When it's active, the prompt of the terminal starts with (.venv).\n"
        "In VS Code: press Ctrl+Shift+P (Cmd+Shift+P on a Mac), choose 'Python: Select Interpreter' and pick\n"
        "the one in venv. New terminals in VS Code then activate it automatically."
    )


def check_environment() -> CheckResult:
    """Check that Python runs in a virtual environment."""
    if in_virtual_environment():
        return CheckResult("Virtual environment", True, sys.prefix, required=False)
    return CheckResult("Virtual environment", False, "not active (see the instructions below)", required=False)


def ask(question: str) -> bool:
    """Ask a yes/no question in the terminal. The default answer is yes.

    Returns False without asking if there is nobody to answer, e.g. in CI.
    """
    if sys.stdin is None or not sys.stdin.isatty():
        print(f"{question} Not asking, as this is not an interactive terminal. To do it, run: {SETUP_COMMAND}")
        return False
    try:
        answer = input(f"{question} [Y/n] ")
    except EOFError:
        return False
    return answer.strip().lower() in ("", "y", "yes")


def create_venv(venv_dir: Path = VENV_DIR) -> bool:
    """Create a virtual environment with the Python that runs this script.

    :return: whether it succeeded
    """
    print(f"Creating a virtual environment in {venv_dir} ...", flush=True)
    result = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=False)
    if result.returncode == 0:
        return True
    # A failed attempt leaves a broken venv behind, which would confuse the next run.
    shutil.rmtree(venv_dir, ignore_errors=True)
    if sys.platform.startswith("linux"):
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f"\nOn Debian and Ubuntu, the venv module is a separate package: sudo apt install python{version}-venv")
    return False


def install_requirements(python: Path) -> bool:
    """Install the requirements of the workshop with the given Python interpreter.

    :return: whether it succeeded
    """
    print("Installing the requirements. This takes a few minutes ...", flush=True)
    command = [str(python), "-m", "pip", "install", "-r", str(REPO_DIR / "requirements.txt")]
    return subprocess.run(command, cwd=REPO_DIR, check=False).returncode == 0


def set_up_venv(force: bool) -> int | None:
    """Create the virtual environment if needed, and run the checks in it.

    :param force: create the environment and install the requirements without asking
    :return: the exit code of the checks run in the virtual environment,
        or None if the checks should be run here instead
    """
    python = venv_python()
    print("You are not in a virtual environment.")
    if not python.exists():
        if not check_python().ok:
            print(check_python())
            print("Please install Python 3.12 or later (see README.md) and run this script with it.")
            return 1
        print("A virtual environment is a folder with its own Python and packages, separate from the rest of")
        print("your computer. The workshop uses one in the folder .venv/.")
        if not (force or ask("Create it and install the requirements into it now?")):
            return None
        if not create_venv() or not install_requirements(python):
            print("\nSetting up the virtual environment failed. The error message is above.")
            return 1
    elif force and not install_requirements(python):
        return 1
    print("\nRunning the checks in the virtual environment ...\n", flush=True)
    code = subprocess.run([str(python), "-m", "workshop.check", "--no-setup"], cwd=REPO_DIR, check=False).returncode
    print()
    print(activation_instructions())
    return code


# ---------------------------------------------------------------------------- checks


def check_python(min_version: tuple[int, int] = MIN_PYTHON) -> CheckResult:
    """Check the Python version."""
    version = sys.version_info[:2]
    detail = f"{platform.python_version()} at {sys.executable}"
    if version < min_version:
        detail += f". Python {min_version[0]}.{min_version[1]} or newer is needed."
    return CheckResult("Python", version >= min_version, detail)


def check_package(name: str) -> CheckResult:
    """Check that a Python package is installed."""
    try:
        version = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return CheckResult(name, False, f"not installed. Run: {SETUP_COMMAND}")
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


def check_vscode_extensions(editor: str | None = None) -> list[CheckResult]:
    """Check that the VS Code extensions of the workshop are installed.

    :param editor: the command of the editor, by default ``code`` or ``codium``, whichever is found first
    :return: one result per extension, or nothing if the editor is not on PATH
    """
    path = shutil.which(editor) if editor else (shutil.which("code") or shutil.which("codium"))
    if path is None:
        return []
    try:
        output = subprocess.run([path, "--list-extensions"], capture_output=True, text=True, timeout=60, check=False)
    except (OSError, subprocess.SubprocessError):
        return []
    installed = {line.strip().lower() for line in output.stdout.splitlines()}
    return [
        CheckResult(
            f"VS Code extension {ext}",
            ext in installed,
            "installed" if ext in installed else "not installed. Install it from the Extensions view of VS Code",
            required=False,
        )
        for ext in VSCODE_EXTENSIONS
    ]


def run_checks() -> list[CheckResult]:
    """Run all the checks."""
    results = [check_python(), check_environment()]
    results.extend(check_package(name) for name in REQUIRED_PACKAGES)
    results.extend(check_command(name) for name in REQUIRED_COMMANDS)
    results.extend(check_command(name, required=False) for name in OPTIONAL_COMMANDS)
    results.extend(check_vscode_extensions())
    return results


def parse_arguments(argv: list[str] | None) -> argparse.Namespace:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--setup",
        action="store_true",
        help="create the virtual environment and install the requirements without asking",
    )
    group.add_argument(
        "--no-setup",
        action="store_true",
        help="only run the checks, even outside a virtual environment",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Set up the virtual environment if needed, print the results of the checks and return the exit code."""
    args = parse_arguments(argv)
    if in_virtual_environment():
        if args.setup and not install_requirements(Path(sys.executable)):
            return 1
    elif not args.no_setup:
        code = set_up_venv(force=args.setup)
        if code is not None:
            return code

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
