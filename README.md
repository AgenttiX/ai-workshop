# Kumpula AI workshop for scientists 2026
A hands-on workshop on how AI is actually used in research today: not chat windows, but AI agents
that read your files, run your code and check their own work. Organized at the Kumpula campus of the
University of Helsinki by
[Antti "Hippe" Hippeläinen](https://github.com/ahippelainen) and
[Mika Mäki](https://github.com/AgenttiX).

- **When and where:** Friday 30 October 2026, 12:00–16:30 (coffee break 14:00–14:30),
  Physicum E207, Kumpula campus
- **Who:** researchers and students of the Faculty of Science. No experience needed; advanced topics are included too.
- **Programme:**
  - *12:00 Foundations:* AI in 2026, chat windows vs. AI agents, the caveats, a live demo, hands-on exercises.
  - *14:30 Advanced:* extending the agent with your own instructions, automatic checks, helper agents and tools,
    making your project AI-ready (tests, automatic code checks, continuous integration), and three showcases: two research setups (attended physics and an autonomous mathematics program)
    and running models on your own computer.
- **Language:** English. **Bring your laptop**, set up as described below.
- **Contact:** antti.hippelainen@helsinki.fi, mika.x.maki@helsinki.fi, joonas.nattila@helsinki.fi
- Slides: [`slides.html`](./slides.html) (open it in a browser; press `S` for the speaker notes, `F` for full screen)

**Contents:** [Setup](#set-up-your-laptop-before-the-workshop) ·
[Troubleshooting](#troubleshooting) · [Exercises](#exercises) · [For the organizers](#for-the-organizers)

---

## Set up your laptop before the workshop
Please do this at home **before** the workshop. It takes 30–60 minutes, most of it waiting for downloads.
Every step is explained, so you don't need any previous experience. If you get stuck, see
[Troubleshooting](#troubleshooting), or paste the error message into any AI chatbot and ask what it means.
That's a skill we'll use all day. You can also email us.

The instructions are written for **Linux**, **Windows** and **macOS**. Follow the parts for your system.

<details>
<summary><b>Already comfortable with the terminal? The quick setup</b></summary>

These commands do steps 1, 3 and 5 below, and install the Claude Code command-line tool.
Run them one line at a time. After them, do steps 2, 4 and 6.
They are tested on fresh machines in CI (the files are in [`setup/`](./setup/)).

**Ubuntu 24.04 and newer**
<!-- source: setup/ubuntu.sh -->
```bash
# Ubuntu 24.04 comes with Python 3.12 and 26.04 with 3.14
sudo apt update
sudo apt install git python3 python3-pip python3-venv
sudo snap install code --classic   # or: codium

# Claude Code command-line tool
curl -fsSL https://claude.ai/install.sh | bash

# The workshop repository and its packages
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m workshop.check
```

**macOS** with [Homebrew](https://brew.sh/). Run the *"Next steps"* that the Homebrew installer prints at the end.
<!-- source: setup/macos.sh -->
```bash
# After installing Homebrew from brew.sh
brew install git python@3.14
brew install --cask visual-studio-code   # or: vscodium

# Claude Code command-line tool
curl -fsSL https://claude.ai/install.sh | bash

# The workshop repository and its packages
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m workshop.check
```

**Windows 11** in PowerShell
<!-- source: setup/windows.ps1 -->
```powershell
# In PowerShell
winget install Python.Python.3.14 Git.Git Microsoft.VisualStudioCode
# Close and reopen PowerShell, then:
irm https://claude.ai/install.ps1 | iex

git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
py -3.14 -m venv venv
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m workshop.check
```
</details>

### What you'll install, and why
| What | Why |
|---|---|
| **VS Code** | A code editor: a program for writing and running code. It has a built-in terminal and the Claude Code extension. [VSCodium](https://vscodium.com/) works too. |
| **Python 3.12 or later** | The programming language of the exercises. |
| **Git** | Version control: it records every change to your files so that you can see and undo them. It's also how you download the workshop materials. |
| **Claude Code** | The AI agent we use. It runs inside VS Code as an extension. |
| **A Claude account** | Claude Code needs a paid Claude plan: Pro, Max or Team. The free plan doesn't include Claude Code. See [step 4](#step-4-a-claude-account). |

### Step 0: Open a terminal
A **terminal** (also called the command line or shell) is a window where you type commands instead of clicking.
Type or paste a command and press Enter to run it. Commands are case-sensitive.
Copy them from this page exactly, one line at a time.

- **Linux:** press Ctrl+Alt+T, or search for "Terminal" in your applications.
- **Windows:** press the Windows key, type **PowerShell** and open "Windows PowerShell".
  The prompt looks like `PS C:\Users\yourname>`. All Windows commands on this page are for PowerShell.
- **macOS:** press Cmd+Space, type **Terminal** and press Enter.

Once VS Code is installed, you can also use its built-in terminal: menu **Terminal → New Terminal**.

### Step 1: Install Python, Git and VS Code

<details open>
<summary><b>Linux (Ubuntu or Debian)</b></summary>

1. Install Python, its virtual-environment module and Git.
   `sudo` runs the command as an administrator and asks for your password.
   Nothing appears on the screen while you type the password; that's normal.
   ```bash
   sudo apt update
   sudo apt install python3 python3-venv git
   ```
   Ubuntu 24.04 comes with Python 3.12 and newer releases with a later one. On older releases, `python3` is older than 3.12;
   contact us in that case.
   On Fedora, use `sudo dnf install python3 git`.
2. Install VS Code: download the `.deb` file from [code.visualstudio.com](https://code.visualstudio.com/)
   and install it with
   ```bash
   sudo apt install ./Downloads/code_*.deb
   ```
   (or with `sudo snap install code --classic`).
3. Check that everything works. Each command should print a version number:
   ```bash
   python3 --version
   git --version
   code --version
   ```
   Python should be 3.12 or later.
</details>

<details>
<summary><b>Windows</b></summary>

1. **Python 3.12.** Download the **Windows installer (64-bit)** from
   [python.org/downloads/release/python-31210](https://www.python.org/downloads/release/python-31210/)
   (3.12.10 is the last 3.12 release with a Windows installer). Run it and on the first screen:
   - tick **Add python.exe to PATH** at the bottom,
   - if you don't have administrator rights on the computer, also untick the option about admin privileges
     for installing `py.exe` (the Python launcher),
   - click **Install Now**. It doesn't need administrator rights.
2. **Git.** Download and run the installer from [git-scm.com/downloads/win](https://git-scm.com/downloads/win).
   The default choices on every screen are fine. Git also installs *Git Bash*, which Claude Code uses to run commands.
3. **VS Code.** Download the **User Installer** from [code.visualstudio.com](https://code.visualstudio.com/)
   (it doesn't need administrator rights) and keep the option **Add to PATH** ticked.
4. **Close all PowerShell windows and open a new one**, so that it finds the new programs.
   Then check that everything works. Each command should print a version number:
   ```powershell
   py -3 --version
   git --version
   code --version
   ```
   `py` is the Python launcher for Windows; `py -3` means "the newest Python 3 installed".
   Use it instead of `python` until the virtual environment is set up in step 5.

If you already use [winget](https://learn.microsoft.com/windows/package-manager/winget/), you can install the same
three programs with `winget install Python.Python.3.12`, `winget install Git.Git` and
`winget install Microsoft.VisualStudioCode`.
</details>

<details>
<summary><b>macOS</b></summary>

1. **Python 3.12.** Download the **macOS 64-bit universal2 installer** from
   [python.org/downloads/release/python-31210](https://www.python.org/downloads/release/python-31210/) and run it.
   (If you use Homebrew: `brew install python@3.12`.)
2. **Git.** Run `git --version` in the terminal. If Git is missing, macOS offers to install the
   *Command Line Tools*, which include Git. Accept and wait until it's done.
3. **VS Code.** Download it from [code.visualstudio.com](https://code.visualstudio.com/), open the downloaded file
   and drag Visual Studio Code to Applications. Start VS Code, press Cmd+Shift+P, type
   **Shell Command: Install 'code' command in PATH** and press Enter.
4. **Close the Terminal window and open a new one**, so that it finds the new programs.
   Then check that everything works. Each command should print a version number, and Python should be 3.12 or newer:
   ```bash
   python3 --version
   git --version
   code --version
   ```
</details>

### Step 2: Install the VS Code extensions
Start VS Code and open the **Extensions** view: the icon of four squares on the left, or Ctrl+Shift+X
(Cmd+Shift+X on a Mac). Search for and install:
1. **Python** by Microsoft: running Python and choosing the virtual environment.
2. **Claude Code** by Anthropic: the AI agent.

Claude Code is marked by the **Spark icon**, a small orange star. To open its panel, open any file (e.g. `README.md`) and click
the Spark icon in the top-right corner of the editor (it appears when a file is open), or click the Spark icon in the Activity Bar on the left.

**Also install Claude Code for the terminal.** Several exercises run `claude` in a terminal, and the extension does not
make that command available there. (The quick setup above already did this.)
- Linux and macOS: `curl -fsSL https://claude.ai/install.sh | bash`
- Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`

Open a new terminal and check with `claude --version`. These commands are from the
[official setup guide](https://code.claude.com/docs/en/setup).

### Step 3: Download the workshop materials
In the terminal, go to your home folder and download (*clone*) this repository. A **repository** is a folder
whose history Git tracks.
```bash
cd ~
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
```
This creates the folder `ai-workshop` in your home folder, and `cd` ("change directory") moves the terminal into it.
The same commands work in PowerShell on Windows.

### Step 4: A Claude account
You don't need to buy anything for the workshop: we arrange access to Claude Code through existing subscriptions
and send the details to everyone who signs up. If you already have Claude Pro, Max or Team, you can use your own account.
(The free Claude plan doesn't include Claude Code.)

To log in, open the Claude Code panel (the Spark icon) and choose to sign in. A browser window opens; log in there.

### Step 5: Create the Python environment and check everything
A **virtual environment** ("venv") is a folder with its own copy of Python and its own packages, separate from the
rest of your computer, so that the workshop can't break anything else and vice versa.
The workshop's check script creates it for you. In the terminal, inside the `ai-workshop` folder, run:

| System | Command |
|---|---|
| Linux, macOS | `python3 -m workshop.check` |
| Windows | `py -3 -m workshop.check` |

It asks whether to create the virtual environment. Press Enter to answer yes. It then installs the packages the
exercises need (this takes several minutes) and checks your setup. It should end with
**"All required checks passed. You're ready for the workshop!"**
Lines marked `WARN` are fine: they're optional.

Finally, **activate** the virtual environment, i.e. tell the terminal to use its Python:

| System | Command |
|---|---|
| Linux, macOS | `source venv/bin/activate` |
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |

The start of the prompt changes to `(venv)`. From now on, `python` means the Python of the workshop.
On Windows, if PowerShell says that "running scripts is disabled on this system", run this once and try again:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Step 6: Open the workshop in VS Code and say hello to Claude
1. In VS Code: **File → Open Folder…** and choose the `ai-workshop` folder.
   If VS Code asks whether you trust the authors of the files, answer yes.
2. Choose the virtual environment: press Ctrl+Shift+P (Cmd+Shift+P on a Mac), type **Python: Select Interpreter**
   and pick the one that mentions `venv`.
3. Open a terminal in VS Code (**Terminal → New Terminal**). The prompt should start with `(venv)`. Run
   ```bash
   python -m workshop.check
   ```
   once more. Everything should be `OK` or `WARN`.
4. Click the Spark icon to open Claude Code and ask:
   > What is this repository about?

   It reads the files of the repository and answers. If it does, you're ready. See you at the workshop!

---

## Troubleshooting
When something fails, the error message usually says why. Paste it into any AI chatbot and ask
"I'm new to this. What does this error mean and how do I fix it?" If that doesn't help, email us.

| Problem | Fix |
|---|---|
| Linux: `python3: command not found` | `sudo apt install python3 python3-venv`. On older Ubuntu releases it's older than 3.12; contact us. |
| Linux: `ensurepip is not available` or "The virtual environment was not created successfully" | `sudo apt install python3-venv`, then run the check again. |
| Windows: `py` is not recognized | Close and reopen PowerShell. If that doesn't help, run the Python installer again and make sure the py launcher is included. |
| Windows: typing `python` opens the Microsoft Store | Use `py -3` instead, or activate the virtual environment first. |
| Windows: "running scripts is disabled on this system" | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then activate again. |
| `git` or `code` is not recognized / not found | Close and reopen the terminal (or VS Code) after installing. On macOS, see step 1 for the `code` command. |
| The check says `FAIL` for a package | Run the check again with `--setup` added, e.g. `python3 -m workshop.check --setup`. |
| The terminal in VS Code doesn't show `(venv)` | Select the interpreter (step 6), then open a new terminal. Or activate it by hand (step 5). |
| You can't install programs on a university-managed laptop | Tell us well before the workshop. The Python and VS Code installers above work without administrator rights. |
| `claude` is not found in the terminal | Install the terminal version ([step 2](#step-2-install-the-vs-code-extensions)), then open a new terminal. The VS Code extension alone doesn't add the command. |
| `git pull` says your local changes would be overwritten | You have edited files in the exercises. Keep a copy of your work with `git stash`, then `git pull` again; `git stash pop` brings your changes back. |
| Claude Code says that your plan doesn't include it | The free Claude plan doesn't include Claude Code; see [step 4](#step-4-a-claude-account). |

---

## Exercises
The exercises are in [`exercises/`](./exercises/). Each has a `README.md` with the task, the prompts to try and
explanations for those who want to know more. The solutions, with an explanation of what happened, are in
[`solutions/`](./solutions/). Try first, then peek.

## For the organizers
- Plan: [`plan/`](./plan/). Coordination: [Mattermost](https://cftgroup.chat/main/channels/ai-workshop).
- Run the tests: `pytest`. Lint: `ruff check`. Type check: `pyrefly check`.
- Render the slides to a PDF: `./render.py slides.html` (requires Chromium or Chrome).
- The poster is in [`poster/`](./poster/): `poster.svg`, previewed with `poster/preview.sh`
  and exported for print with `inkscape poster.svg --export-type=pdf --export-text-to-path --export-filename=poster.pdf`.
