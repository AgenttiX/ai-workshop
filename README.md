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
- **Language:** English.
- **Bring your laptop**, set up as described below.
- **Contact:** antti.hippelainen@helsinki.fi, mika.x.maki@helsinki.fi, joonas.nattila@helsinki.fi
- Slides: [`slides.html`](./slides.html) (download it to your computer and then open it in a browser; press `S` for the speaker notes, `F` for full screen)

**Contents:** [Setup](#set-up-your-laptop-before-the-workshop) ·
[Troubleshooting](#troubleshooting) · [Exercises](#exercises)

---

## Set up your laptop before the workshop
Please do this at home **before** the workshop. It takes 30–60 minutes, most of it waiting for downloads.
Every step is explained, so you don't need any previous experience. If you get stuck, see
[Troubleshooting](#troubleshooting), or paste the error message into any AI chatbot and ask what it means.
That's a skill we'll be using a lot. You can also email us.

The instructions are written for **Linux**, **Windows** and **macOS**. Follow the parts for your system.

<details>
<summary><b>Already comfortable with the terminal? The quick setup</b></summary>

These commands do steps 3, 4, 7 and 8 below.
Run them one line at a time. Before them, do step 1, and after them, steps 5, 6 and 9.
They are tested on fresh machines in CI (the files are in [`setup/`](./setup/)).

**Ubuntu and Cubbli 24.04 and newer**
<!-- source: setup/ubuntu.sh -->
```bash
#!/usr/bin/env bash

sudo apt update
sudo apt install curl git python3 python3-venv
sudo snap install code --classic  # or: codium

# Claude desktop app from Anthropic's apt repository
sudo curl -fsSLo /usr/share/keyrings/claude-desktop-archive-keyring.asc https://downloads.claude.ai/claude-desktop/key.asc
echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/claude-desktop-archive-keyring.asc] https://downloads.claude.ai/claude-desktop/apt/stable stable main" | sudo tee /etc/apt/sources.list.d/claude-desktop.list
sudo apt update
sudo apt install claude-desktop
# Claude Desktop may also install the command-line Claude Code. Check with:
# claude --version
# If it's missing, install it with:
# curl -fsSL https://claude.ai/install.sh | bash

# The workshop repository and its packages
mkdir -p ~/Git
cd ~/Git
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m workshop.check
```

**macOS** with [Homebrew](https://brew.sh/). Run the *"Next steps"* that the Homebrew installer prints at the end.
<!-- source: setup/macos.sh -->
```bash
# After installing Homebrew from brew.sh
brew install git python@3.14
brew install --cask visual-studio-code   # or: vscodium

# Claude desktop app
brew install --cask claude
# Claude Desktop may also install the command-line Claude Code. Check with:
# claude --version
# If it's missing, install it with:
# curl -fsSL https://claude.ai/install.sh | bash

# The workshop repository and its packages
mkdir -p ~/Git
cd ~/Git
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m workshop.check
```

**Windows 11** in PowerShell
<!-- source: setup/windows.ps1 -->
```powershell
# In PowerShell. Anthropic.Claude is the Claude desktop app.
winget install Python.Python.3.14 Git.Git Microsoft.VisualStudioCode Anthropic.Claude
# Claude Desktop may also install the command-line Claude Code. Check with:
# claude --version
# If it's missing, install it with:
# irm https://claude.ai/install.ps1 | iex

# Close and reopen PowerShell, then:
New-Item -ItemType Directory -Force ~\Git
cd ~\Git
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
py -3.14 -m venv .venv
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m workshop.check
```
</details>


### What you'll install, and why
| What | Which | Why |
|---|---|---|
| Code editor | **VS Code or VSCodium** | A program for writing and running code. It has a built-in terminal and extensions, e.g. for Python. |
| Programming language | **Python 3.12 or later** | The programming language of the exercises. The instructions below default to Python 3.14 where applicable. |
| Version control | **Git** | It records every change to your files so that you can see and undo them. It's also how you download the workshop materials. |
| AI harness | **Claude Code, GitHub Copilot or OpenCode** | A harness is a program that enables an AI agent to interact with your computer and files. |
| Account | **A paid Claude plan, GitHub Education, or an AI provider of your choice** | Claude Code needs Claude Pro, Max or Team. The free plan doesn't include Claude Code. Students and researchers can use GitHub Copilot through GitHub Education instead. See [step 1](#step-1-an-account-for-an-ai-provider). |

You can also use other tools of your choice if you prefer.
These are simply the ones with which we are familiar enough that we can provide support.


### Step 1: An account for an AI provider

<details open>
<summary><b>Claude</b></summary>

Claude Code needs a paid Claude plan: **Pro, Max or Team**.
The free Claude plan doesn't include Claude Code.
See [claude.com/pricing](https://claude.com/pricing).
[Claude Team plan for scientists](https://support.claude.com/en/articles/16634237-claude-team-plan-for-scientists)
is available for research groups.
If you're a principal investigator of a research group, you can apply for it
[here](https://claude.com/programs/team-plan-for-scientists).
</details>

<details open>
<summary><b>GitHub Education</b></summary>

[GitHub Education](https://github.com/education) gives verified students free access to GitHub Copilot
([Copilot Student](https://docs.github.com/en/copilot/how-tos/manage-your-account/free-access-with-copilot-student)).
**Apply with your university email address well before the workshop,
as the verification and the activation of the benefit can take a few days.** Then, in VS Code, hover over the
Copilot icon in the Status Bar at the bottom, select **Use AI Features** and sign in with your GitHub account.
The exercises are written for Claude Code, but most of them work with Copilot too: see [doing the exercises with another agent](./exercises/other_agents.md).
</details>

<details open>
<summary><b>A provider of your choice</b></summary>

You may also use an AI provider of your choice. Some notable ones include:

- [Google Gemini](https://gemini.google/subscriptions/)
  - [Provides free agentic access to some models](https://antigravity.google/docs/models)
- [Mistral](https://mistral.ai/pricing/)
  - Provides limited free agentic access
  - The European alternative
- [OpenAI ChatGPT](https://chatgpt.com/pricing/)
  - Provides limited free agentic access

One option is to run the AI model locally on your own computer.
</details>

### Step 2: Open a terminal
A **terminal** (also called the command line or shell) is a window where you type commands instead of clicking.
Type or paste a command and press Enter to run it. Commands are case-sensitive.
Copy them from this page exactly, one line at a time.

- **Linux:** press Ctrl+Alt+T, or search for "Terminal" in your applications.
- **Windows:** press the Windows key, type **PowerShell** and open "Windows PowerShell".
  The prompt looks like `PS C:\Users\yourname>`. All Windows commands on this page are for PowerShell.
- **macOS:** press Cmd+Space, type **Terminal** and press Enter.

Once VS Code is installed, you can also use its built-in terminal: menu **Terminal → New Terminal**.


### Step 3: Install Python, Git and VS Code or VSCodium

<details open>
<summary><b>Linux (Ubuntu or Cubbli)</b></summary>

1. Install Python, its virtual-environment module and Git.
   `sudo` runs the command as an administrator and asks for your password.
   Nothing appears on the screen while you type the password; that's normal.
   ```bash
   sudo apt update
   sudo apt install python3 python3-venv git
   python3 --version
   ```
   The last command should output `Python 3.12` or later.
   If not, please update your operating system,
   or install Python with alternative methods such as
   [uv](https://docs.astral.sh/uv/) or [Miniconda](https://www.anaconda.com/download/success?reg=skipped-miniconda).
   On Fedora, use `sudo dnf install python3.14 git`.
   If you're using the Cubbli Linux of the University of Helsinki and don't yet have sudo access, you may be able to request it with this command:
   ```bash
   i-want-sudo-access
   ```
   If that command doesn't work for you, then please see the
   [sudo instructions on University of Helsinki wiki](https://wiki.helsinki.fi/xwiki/bin/view/Cubbli/User%20documentation/Administrator%20%28sudo%29%20rights%20in%20Cubbli%20Linux/).
2. Install Visual Studio Code or VSCodium:
   ```bash
   # Visual Studio Code
   sudo snap install code --classic
   # VSCodium
   sudo snap install codium --classic
   ```
   Alternatively, download the `.deb` file from [code.visualstudio.com](https://code.visualstudio.com/) or [VSCodium releases](https://github.com/VSCodium/vscodium/releases)
   and install it with
   ```bash
   sudo apt install ~/Downloads/cod*.deb
   ```
3. Check that everything works. Each command should print a version number:
   ```bash
   python3 --version
   git --version
   # Visual Studio Code
   code --version
   # VSCodium
   codium --version
   ```
</details>

<details>
<summary><b>Windows</b></summary>

1. **Python.** Download the **Windows installer (64-bit)** from
   [python.org/downloads/release/python-3149](https://www.python.org/downloads/release/python-3149/).
   Run it and on the first screen:
   - tick **Add python.exe to PATH** at the bottom,
   - if you don't have administrator rights on the computer, also untick the option about admin privileges
     for installing `py.exe` (the Python launcher),
   - click **Install Now**. It doesn't need administrator rights.
2. **Git.** Download and run the installer from [git-scm.com/downloads/win](https://git-scm.com/downloads/win).
   The default choices on every screen are fine. Git also installs *Git Bash*, which Claude Code uses to run commands.
3. **VS Code.** Download the **User Installer** from [code.visualstudio.com](https://code.visualstudio.com/)
   (it doesn't need administrator rights) and keep the option **Add to PATH** ticked.
   For VSCodium, download the **user installer** (`VSCodiumUserSetup-x64-….exe`) from
   [VSCodium releases](https://github.com/VSCodium/vscodium/releases) and keep the option **Add to PATH** ticked.
4. **Close all PowerShell windows and open a new one**, so that it finds the new programs.
   Then check that everything works. Each command should print a version number:
   ```powershell
   py -3 --version
   git --version
   # Visual Studio Code
   code --version
   # VSCodium
   codium --version
   ```
   `py` is the Python launcher for Windows; `py -3` means "the newest Python 3 installed".
   Use it instead of `python` until the virtual environment is set up in step 8.

If you already use [winget](https://learn.microsoft.com/windows/package-manager/winget/), you can install the same
three programs with `winget install Python.Python.3.14`, `winget install Git.Git` and
`winget install Microsoft.VisualStudioCode` (VSCodium: `winget install VSCodium.VSCodium`).
</details>

<details>
<summary><b>macOS</b></summary>

1. **Python.** Download the **macOS 64-bit universal2 installer** from
   [python.org/downloads/release/python-3149](https://www.python.org/downloads/release/python-3149/) and run it.
   (If you use Homebrew: `brew install python@3.14`.)
2. **Git.** Run `git --version` in the terminal. If Git is missing, macOS offers to install the
   *Command Line Tools*, which include Git. Accept and wait until it's done.
3. **VS Code.** Download it from [code.visualstudio.com](https://code.visualstudio.com/), open the downloaded file
   and drag Visual Studio Code to Applications. Start VS Code, press Cmd+Shift+P, type
   **Shell Command: Install 'code' command in PATH** and press Enter.
   For VSCodium, download the `.dmg` file from [VSCodium releases](https://github.com/VSCodium/vscodium/releases)
   (or with Homebrew: `brew install --cask vscodium`), drag VSCodium to Applications, and use the command
   **Shell Command: Install 'codium' command in PATH** in the same way.
4. **Close the Terminal window and open a new one**, so that it finds the new programs.
   Then check that everything works. Each command should print a version number, and Python should be 3.12 or newer:
   ```bash
   python3 --version
   git --version
   # Visual Studio Code
   code --version
   # VSCodium
   codium --version
   ```
</details>


### Step 4: Install an AI desktop client (optional, but useful)
A desktop client is an app in which you chat with an AI agent that works on the files of a folder on your computer.

<details open>
<summary><b>Claude Desktop</b></summary>

- **Windows** and **macOS:** download the installer from [claude.com/download](https://claude.com/download) and run it.
  On macOS, drag Claude to Applications. (Or in the terminal: `winget install Anthropic.Claude` on Windows,
  `brew install --cask claude` with Homebrew on macOS.)
- **Linux** (Ubuntu 22.04 or later and Debian 12 or later; the Linux version is in beta): add Anthropic's software
  source and install the app from it. These commands are from the
  [official guide](https://code.claude.com/docs/en/desktop-linux):
  ```bash
  sudo apt install curl gnupg
  sudo curl -fsSLo /usr/share/keyrings/claude-desktop-archive-keyring.asc https://downloads.claude.ai/claude-desktop/key.asc
  echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/claude-desktop-archive-keyring.asc] https://downloads.claude.ai/claude-desktop/apt/stable stable main" | sudo tee /etc/apt/sources.list.d/claude-desktop.list
  sudo apt update
  sudo apt install claude-desktop
  ```
  On Fedora and other Linux distributions, the desktop app isn't available yet: use a command-line tool of [step 5](#step-5-install-a-command-line-ai-harness).

Start **Claude** from your applications. Sign in with the account of [step 1](#step-1-an-account-for-an-ai-provider).
</details>

<details>
<summary><b>GitHub Copilot app</b></summary>

The [GitHub Copilot app](https://docs.github.com/en/copilot/concepts/agents/github-copilot-app) is GitHub's
desktop client for Copilot, for Windows, macOS and Linux. It works with every Copilot plan,
including Copilot Free and GitHub Education.
1. Download it for your system from [github.com/features/ai/github-app](https://github.com/features/ai/github-app)
   and install it.
2. Open it, click **Sign in to GitHub** and follow the prompts.
3. When it asks for repositories, add the `~/Git/ai-workshop` folder as a local folder after [step 7](#step-7-download-the-workshop-materials),
   or skip this and add it later.

See the [official quickstart](https://docs.github.com/en/copilot/get-started/quickstart-copilot-app).
</details>

<details>
<summary><b>OpenCode Desktop</b></summary>

[OpenCode](https://opencode.ai/) is an open-source AI harness that works with many model providers.
1. Download the desktop app for your system from [opencode.ai/download](https://opencode.ai/download) and install it
   (`.deb` for Ubuntu and Debian, `.rpm` for Fedora). With Homebrew on macOS: `brew install --cask opencode-desktop`.
2. Open it and connect a model provider, e.g. your GitHub Copilot account (`/connect`, then **GitHub Copilot**).
   See the [providers documentation](https://opencode.ai/docs/providers/).
   Note that a Claude subscription can't be used in OpenCode without some trickery.
3. Test whether the `opencode` command is now available in your terminal.
   If not, on Linux, you can make it available with a symbolic link by running this command:
   ```bash
   ln -s /opt/OpenCode/resources/opencode-cli "${HOME}/.local/bin/opencode"
   ```
</details>


### Step 5: Install a command-line AI harness
A command-line (CLI) harness runs the AI agent in a terminal.
This is the primary tool used in this workshop.

<details open>
<summary><b>Claude Code</b></summary>

Claude Desktop may also install the command-line version. If you installed it, check with `claude --version`
in a new terminal. If the command is not found, install it with the commands below.

- Linux and macOS: `curl -fsSL https://claude.ai/install.sh | bash`
- Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`

Check with `claude --version`. These commands are from the
[official setup guide](https://code.claude.com/docs/en/setup).
</details>

<details>
<summary><b>GitHub Copilot CLI</b></summary>

- Linux and macOS: `curl -fsSL https://gh.io/copilot-install | bash`
  (or on macOS with Homebrew: `brew install --cask copilot-cli`)
- Windows PowerShell: `winget install GitHub.Copilot`

Check with `copilot --version`. Start it with `copilot`; on the first start, log in with the `/login` command.
It needs a Copilot plan, e.g. through GitHub Education. See the
[official installation guide](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli).
</details>

<details>
<summary><b>OpenCode</b></summary>

OpenCode Desktop (instructions above) already includes the command-line version, at least on Linux.
- Linux and macOS: `curl -fsSL https://opencode.ai/install | bash`
  (or on macOS with Homebrew: `brew install anomalyco/tap/opencode`)
- Windows
  - OpenCode recommends on Windows: [OpenCode WSL instructions](https://opencode.ai/docs/windows-wsl/)
  - Chocolatey: [`choco install opencode`](https://community.chocolatey.org/packages/opencode) (third-party package)
  - Node.js: `npm install -g @opencode/cli`

Check with `opencode --version`. Start it with `opencode` and connect a model provider with `/connect`.
See the [official documentation](https://opencode.ai/docs/).
</details>


### Step 6: Install the IDE extensions
Start VS Code or VSCodium and open the **Extensions** view: the icon of four squares on the left, or Ctrl+Shift+X
(Cmd+Shift+X on a Mac). Search for and install:
1. **Python**: for running Python and choosing the virtual environment.
   [VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python),
   [VSCodium](https://open-vsx.org/vscode/item?itemName=ms-python.python)
2. A plugin for your AI harness
   - **Claude Code**:
     [VS Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code),
     [VSCodium](https://open-vsx.org/vscode/item?itemName=Anthropic.claude-code)
   - **GitHub Copilot Chat**:
     [VS Code](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
   - **opencode**:
     [VS Code](https://marketplace.visualstudio.com/items?itemName=sst-dev.opencode),
     [VSCodium](https://open-vsx.org/vscode/item?itemName=sst-dev.opencode)

Claude Code is marked by the **Spark icon**, a small orange star. To open its panel, open any file (e.g. `README.md`) and click
the Spark icon in the top-right corner of the editor (it appears when a file is open), or click the Spark icon in the Activity Bar on the left.


### Step 7: Download the workshop materials
In the terminal, go to your home folder and download (*clone*) this repository. A **repository** is a folder
whose history Git tracks.
```bash
mkdir -p ~/Git
cd ~/Git
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
```
On Windows, in PowerShell:
```powershell
New-Item -ItemType Directory -Force ~\Git
cd ~\Git
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
```
This creates the folder `Git/ai-workshop` in your home folder (`~`), and `cd` ("change directory") moves the terminal into it.


### Step 8: Create the Python environment and check everything
A **virtual environment** ("venv") is a folder with its own copy of Python and its own packages, separate from the
rest of your computer, so that the workshop can't break anything else and vice versa.
The workshop's check script creates it for you. In the terminal, inside the `~/Git/ai-workshop` folder, run:

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
| Linux, macOS | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |

The start of the prompt changes to `(.venv)`. From now on, `python` means the Python of the workshop.
On Windows, if PowerShell says that "running scripts is disabled on this system", run this once and try again:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```


### Step 9: Open the workshop in VS Code and say hello to the AI
1. In VS Code: **File → Open Folder…** and choose the `ai-workshop` folder in the `Git` folder of your home folder.
   If VS Code asks whether you trust the authors of the files, answer yes.
2. Choose the virtual environment: press Ctrl+Shift+P (Cmd+Shift+P on a Mac), type **Python: Select Interpreter**
   and pick the one that mentions `.venv`.
3. Open a terminal in VS Code (**Terminal → New Terminal**). The prompt should start with `(.venv)`. Run
   ```bash
   python -m workshop.check
   ```
   once more. Everything should be `OK` or `WARN`.
4. Open your AI plugin. E.g. for Claude Code, click the orange spark icon. Then ask:
   > What is this repository about?

   It reads the files of the repository and answers. If it does, you're ready. See you at the workshop!

---

### Step 10: Local models (optional)
Local AI models are a viable alternative to cloud-hosted models.
They are not as capable as frontier-level cloud models, but they are sufficient for many kinds of useful work.
As long as you have enough free memory (RAM or VRAM), you can run a useful AI agent even on a laptop without any internet access.
**The setup instructions below are provided already in this readme before the workshop, as downloading the multi-gigabyte LLM models can take several hours.**

As an example of recent local LLMs, the memory requirements for Google's Gemma 4 QAT are available
[here](https://ai.google.dev/gemma/docs/core#gemma-4-inference-memory-requirements).
For most use, 4-bit quantization is sufficient. The E2B and E4B versions are useful for testing,
but for actual work the versions from 12B onwards are preferred.
If you have enough memory, the 26B A4B is preferable over the 12B,
since the former is significantly faster due to its mixture-of-experts (MoE) architecture despite its larger size.
In model names, B refers to how many billions of parameters it has, which determines the memory use.
E refers to an effective number of parameters.
A means how many parameters are activated during the generation of each output token, which determines the output speed (tokens/s).
For example, the Gemma 4 26B A4B has 26 billion parameters, of which 4 billion are activated when generating each output token.

Therefore, for testing you should have at least 3 GB of free memory (RAM or VRAM),
and for multipurpose work at least 7 GB, preferably 16 GB.
On Linux, you can check your free RAM with `free -h`, and free VRAM with `nvtop` or `nvidia-smi`, if you have them installed.
On Windows, you can check these in Task Manager.

There are several backends for running LLMs locally.
These can be connected to any compatible client or harness, such as OpenCode or [Open WebUI](https://openwebui.com/).

**One of the easiest ways to get started with local LLMs is [LM Studio](https://lmstudio.ai/)**,
as it bundles the LLM backend, chat interface and agent harness in one package.
You can just download it, select an LLM that fits on your computer, and get started.

However, LM Studio is not very optimized, and with other backends it's possible to fit much larger models and run them much faster on the same hardware.
Perhaps the most popular LLM backend for consumer hardware is [llama.cpp](https://llama.app/),
as it works on a variety of platforms and is capable of splitting an LLM between a GPU and a CPU,
if the LLM doesn't fit entirely in the VRAM of the GPU. This is known as CPU offloading.
This way, even a GPU with 4 GB of VRAM can be highly useful.
An example laptop config for llama.cpp is available [here](https://github.com/AgenttiX/agx-ai/tree/main/llama-cpp-agx-l14).

The highest performance is often achieved with [vLLM](https://vllm.ai/).
However, it often requires more memory than llama.cpp for the same models,
and its support for CPU offloading is more limited.
It also requires extensive configuration for optimal performance,
and has limited support of model formats.

For advanced users interested in local models, our recommendation is to install llama.cpp in a Docker container if on Linux, and natively if on Windows.
(Docker has some overhead on Windows. For macOS, we haven't tested.)
Once you have llama.cpp working, you can start experimenting with vLLM.
Both of these provide an OpenAI-compatible HTTP endpoint, to which you can connect your client or harness of choice.
An example OpenCode config is available [here](https://github.com/AgenttiX/agx-ai/blob/main/opencode/opencode.jsonc).

---

## Troubleshooting
When something fails, the error message usually says why. Paste it into any AI chatbot and ask
"I'm new to this. What does this error mean and how do I fix it?" If that doesn't help, email us.

| Problem | Fix |
|---|---|
| Linux: `python3: command not found` | `sudo apt install python3 python3-venv`. On older Ubuntu releases it's older than 3.12; see [step 3](#step-3-install-python-git-and-vs-code-or-vscodium). |
| Linux: `ensurepip is not available` or "The virtual environment was not created successfully" | `sudo apt install python3-venv`, then run the check again. |
| Windows: `py` is not recognized | Close and reopen PowerShell. If that doesn't help, run the Python installer again and make sure the py launcher is included. |
| Windows: typing `python` opens the Microsoft Store | Use `py -3` instead, or activate the virtual environment first. |
| Windows: "running scripts is disabled on this system" | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then activate again. |
| `git`, `code` or `codium` is not recognized / not found | Close and reopen the terminal (or VS Code) after installing. On macOS, see step 3 for the `code` and `codium` commands. |
| The check says `FAIL` for a package | Run the check again with `--setup` added, e.g. `python3 -m workshop.check --setup`. |
| The terminal in VS Code doesn't show `(.venv)` | Select the interpreter (step 9), then open a new terminal. Or activate it by hand (step 8). |
| You can't install programs on a university-managed laptop | Tell us well before the workshop. The Python and VS Code installers above work without administrator rights. |
| `claude` is not found in the terminal | Install the command-line version ([step 5](#step-5-install-a-command-line-ai-harness)), then open a new terminal. Claude Desktop may not add the command, and the VS Code extension doesn't. |
| `git pull` says your local changes would be overwritten | You have edited files in the exercises. Keep a copy of your work with `git stash`, then `git pull` again; `git stash pop` brings your changes back. |
| Claude Code says that your plan doesn't include it | The free Claude plan doesn't include Claude Code; see [step 1](#step-1-an-account-for-an-ai-provider). |

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
