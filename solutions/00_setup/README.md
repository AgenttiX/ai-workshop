# Solution of exercise 00: Setup check

## What a finished setup looks like
In a terminal (a window where you type commands) inside the workshop folder, with the virtual environment active,
the check ends with:
```text
All required checks passed. You're ready for the workshop!
```
Every line above it is `[OK  ]` or `[WARN]`, and none is `[FAIL]`.
Claude Code answers "What is this repository about, and how do I run its tests?" with something like
"a workshop on AI agents for scientists; run the tests with `pytest`".

## What `python -m workshop.check` does
It is a small Python program, [`workshop/check.py`](../../workshop/check.py). `-m workshop.check` means
"run the module `check` of the package `workshop`". It does two things: it sets up the virtual environment
if needed, and it checks that everything the exercises need is installed.

A *virtual environment* ("venv") is a folder, here `venv/`, with its own Python and its own packages,
separate from the rest of your computer.

**Outside a virtual environment** (the first time you run it):
1. It checks that the Python running it is 3.12 or newer. If not, it stops and asks you to install Python 3.12 or later.
2. If `venv/` doesn't exist, it asks `Create it and install the requirements into it now? [Y/n]`. Enter means yes.
   It then creates `venv/` with the Python you ran it with and installs the packages of `requirements.txt` into it.
   This takes several minutes. If you answer no, it only runs the checks with your current Python,
   so the packages show `FAIL`.
3. It runs the checks again *with the Python of `venv/`* and prints how to activate the environment.

**Inside an active virtual environment** it only runs the checks.

Two options change this:
- `--setup` creates the environment and (re)installs the packages without asking.
  Use it when a package shows `FAIL`.
- `--no-setup` only runs the checks, even outside a virtual environment.

| Mark | Meaning |
|---|---|
| `[OK  ]` | Found, with its version and location. |
| `[FAIL]` | Required and missing: Python 3.12+, the Python packages (matplotlib, numpy, scipy, pttools-gw, pytest, ruff, pyrefly) or Git. Fix these. |
| `[WARN]` | Optional and missing. The `claude`, `code` and `codium` commands are optional: the VS Code extension works without the `claude` command, and VS Code works without `code` on your PATH. "Virtual environment: not active" is also a warning: activate it before the exercises. |

The PATH is the list of folders where the terminal looks for commands.

## Common problems
| Problem | Fix |
|---|---|
| Linux/macOS: `python3: command not found` | Install Python 3.12 or later (see the [README](../../README.md#step-1-install-python-git-and-vs-code)). On Ubuntu 24.04: `sudo apt install python3 python3-venv`. |
| Windows: `py` is not recognized | Close and reopen PowerShell. If that doesn't help, rerun the Python installer and include the `py` launcher. |
| Windows: typing `python` opens the Microsoft Store | Python isn't installed or isn't on the PATH. Use `py -3` until the venv is active. |
| Debian/Ubuntu: `ensurepip is not available` or "The virtual environment was not created successfully" | The `venv` module is a separate package: `sudo apt install python3-venv`. Then run the check again. |
| Windows PowerShell: "running scripts is disabled on this system" when activating | Run once: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`. This lets you run local scripts such as `Activate.ps1`, for your user only. |
| The VS Code terminal doesn't show `(venv)` | Ctrl+Shift+P (Cmd+Shift+P on a Mac) → **Python: Select Interpreter** → pick the one in `venv`. Then open a *new* terminal. |
| Claude Code says your plan doesn't include it | Claude Code needs a Pro, Max, Team, Enterprise or Console account. The free claude.ai plan doesn't include Claude Code ([setup docs](https://code.claude.com/docs/en/setup#authenticate)). |

To run the check by hand:

| System | First time (creates `venv/`) | Activate `venv/` | Afterwards |
|---|---|---|---|
| Linux, macOS | `python3 -m workshop.check` | `source venv/bin/activate` | `python -m workshop.check` |
| Windows (PowerShell) | `py -3 -m workshop.check` | `venv\Scripts\Activate.ps1` | `python -m workshop.check` |

## What the agent typically does in step 4
Claude Code loads `CLAUDE.md` into its context (its working memory for the conversation) at the start of every session.
In this repository `CLAUDE.md` contains only `@AGENTS.md`, which pulls in the whole of `AGENTS.md`.
So Claude often *already knows* what the repository is about and that the tests run with `pytest`,
before it opens any file. It typically still reads `README.md` or lists the folders to fill in details.

This is why you may not see `AGENTS.md` in the list of files it read. Type `/context` to see what is loaded:
`CLAUDE.md` and `AGENTS.md` appear under the memory files.

Warning signs: it invents commands that don't exist in the repository (e.g. `make test`), or it answers
without reading anything and without mentioning `pytest`. Then check that you opened the workshop folder
itself, not a folder above or below it.

## Step 5: file access
A chat window only sees what you paste into it. Claude Code is a *harness*: a program around the model that lets it
read files, run commands and edit code on your computer, with your permission. The list of file reads and
commands in the conversation is that access at work. Click on them to see exactly what it did.

## What to take away about prompting
1. The agent reads what's in the repository. A good `AGENTS.md` saves you from explaining the project in every prompt.
2. Ask questions whose answers you can check. "How do I run its tests?" has a checkable answer: run the command.
3. Look at what the agent read before you trust what it says.
