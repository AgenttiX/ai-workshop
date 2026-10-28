# Kumpula AI workshop for scientists 2026
A hands-on workshop on how AI is actually used in research today: not chat windows, but AI agents that read your files, run your code and check their own work. Organized at the Kumpula campus of the University of Helsinki by [Antti "Hippe" Hippeläinen](https://github.com/ahippelainen) and [Mika Mäki](https://github.com/AgenttiX).

- **When and where:** Friday 30 October 2026, 12:00–16:30 (coffee break 14:00–14:30), Chemicum A129, Kumpula campus
- **Who:** researchers and students of the Faculty of Science. No experience needed; advanced topics are included too.
- **Programme:**
    - *12:00 Foundations:* AI in 2026, chat windows vs. AI agents, the caveats, a live demo, hands-on exercises.
    - *14:30 Advanced:* extending the agent with your own instructions, automatic checks, helper agents and tools, making your project AI-ready (tests, automatic code checks, continuous integration), and three showcases: two research setups (attended physics and an autonomous mathematics program) and running models on your own computer.
- **Language:** English.
- **Bring your laptop**, set up as described below.
- **Contact:** antti.hippelainen@helsinki.fi, mika.x.maki@helsinki.fi, joonas.nattila@helsinki.fi
- Slides: [`slides.html`](./slides.html) (download it to your computer and then open it in a browser; press `S` for the speaker notes, `F` for full screen)

**Contents:** [Setup](#set-up-your-laptop-before-the-workshop) · [Troubleshooting](#troubleshooting) · [Exercises](#exercises)

---

## Set up your laptop before the workshop
Please do this at home **before** the workshop. It takes 30–60 minutes, most of it waiting for downloads. Every step is explained, so you don't need any previous experience. **If you get stuck, see [Troubleshooting](#troubleshooting), or paste the error message into any AI chatbot and ask what it means. That's a skill we'll be using a lot.** You can also email us. **It's important that you download the software beforehand, as Wi-Fi will be congested during the workshop due to the number of participants.**

The instructions are written for **Linux**, **Windows** and **macOS**. Follow the parts for your system. Steps 1–9 take you from nothing to a working setup; step 10 (local models) is optional.

### The short version
If you know how to install programs on your system, this is all you need, installed in any way you like:

**1.** **Python 3.12 or newer** and **Git**. Git is also needed for installing one of the Python packages.

**2.** **VS Code** with the **Claude Code** extension, signed in with a paid Claude plan ([step 1](#step-1-an-account-for-an-ai-provider)). Or alternatively, an IDE, AI harness and AI provider of your choice, including the free options.

**3.** This repository and its Python packages. In a terminal, run:

```bash
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
python3 -m workshop.check
```

On Windows, the last command is `py -3 -m workshop.check`. It creates a virtual environment in `.venv`, installs the packages of [`requirements.txt`](./requirements.txt) into it and checks your setup.

The rest of this section explains each of these step by step.

<details>
<summary><b>Already comfortable with the terminal? The quick setup</b></summary>

These commands do steps 3, 4, 7 and 8 below. Run them one line at a time. Before them, do step 1, and after them, steps 5, 6 and 9. They are tested on fresh machines in CI (the files are in [`setup/`](./setup/)).

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
# The command-line Claude Code. Claude Desktop doesn't always install it.
curl -fsSL https://claude.ai/install.sh | bash

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
# The command-line Claude Code. Claude Desktop doesn't always install it.
curl -fsSL https://claude.ai/install.sh | bash

# The workshop repository and its packages
mkdir -p ~/Git
cd ~/Git
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m workshop.check
```

**Windows 11** in PowerShell
<!-- source: setup/windows.ps1 -->
```powershell
# In PowerShell. Anthropic.Claude is the Claude desktop app.
winget install Python.Python.3.14 Git.Git Microsoft.VisualStudioCode Anthropic.Claude
# The command-line Claude Code. Claude Desktop doesn't always install it.
irm https://claude.ai/install.ps1 | iex

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

You can also use other tools of your choice if you prefer. These are simply the ones with which we are familiar enough that we can provide support.


### Step 1: An account for an AI provider
Choose an AI provider, and create an account. If you don't already have a paid subscription for one of the providers, then we recommend creating a free account with more than one provider to ensure that you don't hit the free usage limits during the workshop.

Then, in the following steps of these instructions, install either the provider's own client software (aka. harness) or OpenCode, which is compatible with multiple providers. If you choose to use OpenCode, you need to create an API key for your provider, and then input that into OpenCode once you have installed it. (A password that one software uses to access another is called an API key. In this case, the API key is the password that your local AI client/harness uses to access the cloud AI provider.)

<details open>
<summary><b>Claude</b></summary>

Claude is the provider that the workshop organizers are the most familiar with, and can therefore provide the most support for.

However, the use of Claude as an AI agent, aka. Claude Code, needs a paid Claude plan: **Pro, Max or Team**. The free Claude plan doesn't include Claude Code. See [claude.com/pricing](https://claude.com/pricing). [Claude Team plan for scientists](https://support.claude.com/en/articles/16634237-claude-team-plan-for-scientists) is available for research groups. If you're a principal investigator of a research group, you can apply for it [here](https://claude.com/programs/team-plan-for-scientists).

With Claude, API access (which is required for using a third-party harness such as OpenCode) is not included in the usage limits of the subscription, but is paid-per-use. You can check from [Claude Console](https://platform.claude.com/settings/billing) whether your plan includes API credits.
</details>

<details open>
<summary><b>GitHub Education</b></summary>

[GitHub Education](https://github.com/education) gives verified students and teachers free access to GitHub Copilot ([Copilot Student](https://docs.github.com/en/copilot/how-tos/manage-your-account/free-access-with-copilot-student), [Copilot Pro for teachers](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-teachers-and-os-maintainers)). **Apply with your university email address well before the workshop, as the verification and the activation of the benefit can take a few days.** You'll sign in to Copilot in VS Code in [step 6](#step-6-install-the-ide-extensions). The exercises are written for Claude Code, but most of them work with Copilot too: see [doing the exercises with another agent](./exercises/other_agents.md).
</details>

<details open>
<summary><b>OpenAI ChatGPT</b></summary>

[OpenAI ChatGPT](https://chatgpt.com/pricing/) provides limited free agentic access with their [Codex](https://openai.com/codex/) desktop client. API access requires paid tokens or a subscription. You can create an API key [here](https://platform.openai.com/settings/organization/api-keys).
</details>

<details open>
<summary><b>Google Gemini</b></summary>

[Google Gemini](https://gemini.google/subscriptions/) provides limited free agentic access to [some models](https://antigravity.google/docs/models). It can be used with Google's own Antigravity IDE, Antigravity CLI or editor plugins (including VS Code), all of which are available [here](https://antigravity.google/docs/ide/extensions/vscode). You can create an API key [here](https://aistudio.google.com/app/api-keys).
</details>

<details open>
<summary><b>Mistral</b></summary>

[Mistral](https://mistral.ai/pricing/) is the European option. It provides limited free agentic access. You can download their Vibe CLI and VS Code extension [here](https://chat.mistral.ai/code/extensions). You can create an API key [here](https://admin.mistral.ai/organization/api-keys).
</details>

<details open>
<summary><b>A provider of your choice</b></summary>

You can also use an AI provider of your choice. The list above is merely of the ones we have tried.
</details>

<details open>
<summary><b>Local models</b></summary>

Local models are a viable option to cloud-hosted ones. The ones that fit on consumer hardware aren't as fast or intelligent as the cloud-hosted frontier models, but they are sufficient for many kinds of work. For instructions on how to set up local models, please see [Step 10: Local models](#step-10-local-models-optional).

</details>


### Step 2: Open a terminal
A **terminal** (also called the command line or shell) is a window where you type commands instead of clicking. Type or paste a command and press Enter to run it. Commands are case-sensitive. Copy them from this page exactly, one line at a time.

- **Linux:** press Ctrl+Alt+T, or search for "Terminal" in your applications.
- **Windows:** press the Windows key, type **PowerShell** and open "Windows PowerShell". The prompt looks like `PS C:\Users\yourname>`. All Windows commands on this page are for PowerShell.
- **macOS:** press Cmd+Space, type **Terminal** and press Enter.

Once VS Code is installed, you can also use its built-in terminal: menu **Terminal → New Terminal**.


### Step 3: Install Python, Git and VS Code or VSCodium
You need **one** code editor: VS Code or VSCodium. They are the same editor. **VS Code** is Microsoft's build, and **VSCodium** is a fully open-source build of it without Microsoft's telemetry. If you're unsure, or if you'll use GitHub Copilot, pick **VS Code**. From here on, "VS Code" means whichever of the two you installed. If you chose VSCodium, type `codium` wherever a command says `code`.

<details open>
<summary><b>Linux (Ubuntu or Cubbli)</b></summary>

**1.** **Cubbli only:** the commands below start with `sudo`, which needs administrator (sudo) rights. On the Cubbli Linux of the University of Helsinki, if you don't have them yet, you may be able to request them with

```bash
i-want-sudo-access
```

If that doesn't work, see the [sudo instructions on the University of Helsinki wiki](https://wiki.helsinki.fi/xwiki/bin/view/Cubbli/User%20documentation/Administrator%20%28sudo%29%20rights%20in%20Cubbli%20Linux/).

**2.** **Python and Git.** Install Python, its virtual-environment module and Git. `sudo` runs the command as an administrator and asks for your password. Nothing appears on the screen while you type the password; that's normal.

```bash
sudo apt update
sudo apt install python3 python3-venv git
python3 --version
```

The last command should output `Python 3.12` or later. If not, please update your operating system, or install Python with alternative methods such as [uv](https://docs.astral.sh/uv/) or [Miniconda](https://www.anaconda.com/download/success?reg=skipped-miniconda). On Fedora, use `sudo dnf install python3.14 git` instead.

**3.** **VS Code.** Install it with

```bash
sudo snap install code --classic
```

or, for VSCodium, `sudo snap install codium --classic`. Run only one of the two. If `snap` isn't available, download the `.deb` file from [code.visualstudio.com](https://code.visualstudio.com/) (VSCodium: the `…amd64.deb` file from [VSCodium releases](https://github.com/VSCodium/vscodium/releases)) and install it with `sudo apt install ~/Downloads/` followed by the name of the downloaded file.

**4.** **Check** that everything works. Each command should print a version number (VSCodium: `codium --version` instead of `code --version`):

```bash
python3 --version
git --version
code --version
```

</details>

<details>
<summary><b>Windows</b></summary>

**1.** **Python.** Download the **Windows installer (64-bit)** from [python.org/downloads/release/python-3149](https://www.python.org/downloads/release/python-3149/). Run it and on the first screen:

- tick **Add python.exe to PATH** at the bottom,
- if you don't have administrator rights on the computer, also untick the option about admin privileges for installing `py.exe` (the Python launcher),
- click **Install Now**. It doesn't need administrator rights.

**2.** **Git.** Download and run the installer from [git-scm.com/downloads/win](https://git-scm.com/downloads/win). The default choices on every screen are fine. Git also installs *Git Bash*, which Claude Code uses to run commands.

**3.** **VS Code.** Download the **User Installer** from [code.visualstudio.com](https://code.visualstudio.com/) (it doesn't need administrator rights) and keep the option **Add to PATH** ticked. For VSCodium instead, download the **user installer** (`VSCodiumUserSetup-x64-….exe`) from [VSCodium releases](https://github.com/VSCodium/vscodium/releases) and keep the option **Add to PATH** ticked.

**4.** **Close all PowerShell windows and open a new one**, so that it finds the new programs. Then check that everything works. Each command should print a version number (VSCodium: `codium --version` instead of `code --version`):

```powershell
py -3 --version
git --version
code --version
```

`py` is the Python launcher for Windows; `py -3` means "the newest Python 3 installed". Use it instead of `python` until the virtual environment is set up in step 8.

If you already use [winget](https://learn.microsoft.com/windows/package-manager/winget/), you can install the same three programs with these commands instead (for VSCodium, replace the last one with `winget install VSCodium.VSCodium`):

```powershell
winget install Python.Python.3.14
winget install Git.Git
winget install Microsoft.VisualStudioCode
```

</details>

<details>
<summary><b>macOS</b></summary>

**1.** **Python.** Download the **macOS 64-bit universal2 installer** from [python.org/downloads/release/python-3149](https://www.python.org/downloads/release/python-3149/) and run it. (If you use Homebrew: `brew install python@3.14`.)

**2.** **Git.** Run `git --version` in the terminal. If Git is missing, macOS offers to install the *Command Line Tools*, which include Git. Accept and wait until it's done.

**3.** **VS Code.** Download it from [code.visualstudio.com](https://code.visualstudio.com/), open the downloaded file and drag Visual Studio Code to Applications. Start VS Code, press Cmd+Shift+P, type **Shell Command: Install 'code' command in PATH** and press Enter. For VSCodium instead, download the `.dmg` file from [VSCodium releases](https://github.com/VSCodium/vscodium/releases) (or with Homebrew: `brew install --cask vscodium`), drag VSCodium to Applications, and use the command **Shell Command: Install 'codium' command in PATH** in the same way.

**4.** **Close the Terminal window and open a new one**, so that it finds the new programs. Then check that everything works. Each command should print a version number, and Python should be 3.12 or newer (VSCodium: `codium --version` instead of `code --version`):

```bash
python3 --version
git --version
code --version
```

</details>


### Step 4: Install an AI desktop client (optional, but useful)
A desktop client is an app in which you chat with an AI agent that works on the files of a folder on your computer.

<details open>
<summary><b>Claude Desktop</b></summary>

**Windows** and **macOS:** download the installer from [claude.com/download](https://claude.com/download) and run it. On macOS, drag Claude to Applications. (Or in the terminal: `winget install Anthropic.Claude` on Windows, `brew install --cask claude` with Homebrew on macOS.)

**Linux** (Ubuntu 22.04 or later and Debian 12 or later; the Linux version is in beta): add Anthropic's software source and install the app from it. These commands are from the [official guide](https://code.claude.com/docs/en/desktop-linux):

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

The [GitHub Copilot app](https://docs.github.com/en/copilot/concepts/agents/github-copilot-app) is GitHub's desktop client for Copilot, for Windows, macOS and Linux. It works with every Copilot plan, including Copilot Free and GitHub Education.

1. Download it for your system from [github.com/features/ai/github-app](https://github.com/features/ai/github-app) and install it.
2. Open it, click **Sign in to GitHub** and follow the prompts.
3. When it asks for repositories, add the `~/Git/ai-workshop` folder as a local folder after [step 7](#step-7-download-the-workshop-materials), or skip this and add it later.

See the [official quickstart](https://docs.github.com/en/copilot/get-started/quickstart-copilot-app).
</details>

<details>
<summary><b>ChatGPT Codex</b></summary>

OpenAI's ChatGPT Codex is available for download [here](https://chatgpt.com/codex/).
</details>

<details>
<summary><b>OpenCode Desktop: for both cloud & local models</b></summary>

[OpenCode](https://opencode.ai/) is an open-source AI harness that works with many model providers.

**1.** Download the desktop app for your system from [opencode.ai/download](https://opencode.ai/download) and install it (`.deb` for Ubuntu and Debian, `.rpm` for Fedora). With Homebrew on macOS: `brew install --cask opencode-desktop`.

**2.** Open it and connect a model provider. In the desktop version, click ≡ at top-left corner, go to File &rarr; Settings &rarr; Providers &rarr; Show more providers, and input the API key you have generated for your provider. In command-line version, write `/connect`, and select your provider. For further information, see the [OpenCode providers documentation](https://opencode.ai/docs/providers/).

**3.** Test whether the `opencode` command is now available in your terminal. If not, on Linux, you can make it available with a symbolic link by running this command:

```bash
ln -s /opt/OpenCode/resources/opencode-cli "${HOME}/.local/bin/opencode"
```

On other platforms, you may have to install the `opencode` command-line harness separately.
</details>

<details>
<summary><b>LM Studio & Bionic: local models</b></summary>

Download and run the LM Studio installer [here](https://lmstudio.ai/download).
On Ubuntu and Cubbli, you can run the .deb installer with:
```bash
sudo apt install ./LM-Studio*.deb
```
LM Studio is compatible with both their own Bionic harness and OpenCode. If you choose to use Bionic, download it from the same downloads page as LM Studio.

You will also need to download an LLM model. For this, see [step 10](#step-10-local-models-optional).
</details>


### Step 5: Install a command-line AI harness
A command-line (CLI) harness runs the AI agent in a terminal.

<details open>
<summary><b>Claude Code</b></summary>

Claude Desktop may also install the command-line version. If you installed it, check with `claude --version` in a new terminal. If the command is not found, install it with the commands below.

- Linux and macOS: `curl -fsSL https://claude.ai/install.sh | bash`
- Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`

Check with `claude --version`. These commands are from the [official setup guide](https://code.claude.com/docs/en/setup).
</details>

<details>
<summary><b>GitHub Copilot CLI</b></summary>

- Linux and macOS: `curl -fsSL https://gh.io/copilot-install | bash` (or on macOS with Homebrew: `brew install --cask copilot-cli`)
- Windows PowerShell: `winget install GitHub.Copilot`

Check with `copilot --version`. Start it with `copilot`; on the first start, log in with the `/login` command. It needs a Copilot plan, e.g. through GitHub Education. See the [official installation guide](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli).
</details>

<details>
<summary><b>ChatGPT Codex</b></summary>

- Linux and macOS: `curl -fsSL https://chatgpt.com/codex/install.sh | sh`
- macOS with Homebrew: `brew install --cask codex`
- Windows: `powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"`
Official documentation is available [here](https://learn.chatgpt.com/docs/codex/cli).
</details>

<details>
<summary><b>Mistral Vibe CLI</b></summary>

- Linux and macOS: `curl -LsSf https://mistral.ai/vibe/install.sh | bash`
- Windows
  - First install [`uv`](https://docs.astral.sh/uv/), e.g. with: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
  - Then install Vibe CLI with uv: `uv tool install mistral-vibe`
</details>

<details>
<summary><b>OpenCode: for both cloud & local models</b></summary>

OpenCode Desktop (instructions above) already includes the command-line version, at least on Linux. If it's not already available with the instructions above, then you can install it manually:

- Linux and macOS: `curl -fsSL https://opencode.ai/install | bash` (or on macOS with Homebrew: `brew install anomalyco/tap/opencode`)
- Windows
    - OpenCode recommends on Windows: [OpenCode WSL instructions](https://opencode.ai/docs/windows-wsl/)
    - Chocolatey: [`choco install opencode`](https://community.chocolatey.org/packages/opencode) (third-party package)
    - Node.js: `npm install -g @opencode/cli`

Check with `opencode --version`. Start it with `opencode` and connect a model provider with `/connect`. See the [official documentation](https://opencode.ai/docs/).
</details>


### Step 6: Install the IDE extensions
An **extension** (also called a plugin) adds features to VS Code. Start VS Code and open the **Extensions** view: the icon of four squares on the left, or Ctrl+Shift+X (Cmd+Shift+X on a Mac). Search for and install the two extensions below. The links show each extension's page, for VS Code and for VSCodium.

1. **Python**: for running Python and choosing the virtual environment. [VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python), [VSCodium](https://open-vsx.org/vscode/item?itemName=ms-python.python)
2. The extension of the AI harness you installed in step 5 (only one is needed):
    - **Claude Code**: [VS Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code), [VSCodium](https://open-vsx.org/vscode/item?itemName=Anthropic.claude-code)
      - Once installed, Claude Code is marked by the **Spark icon**, a small orange star. To open its panel, open any file (e.g. `README.md`) and click the Spark icon in the top-right corner of the editor (it appears when a file is open), or click the Spark icon in the Activity Bar on the left.
    - **GitHub Copilot Chat**: [VS Code](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
      - Once installed, hover over the Copilot icon in the Status Bar at the bottom, select **Use AI Features** and sign in with your GitHub account.
    - **ChatGPT Codex**: [VS Code](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt), [VSCodium](https://open-vsx.org/extension/openai/chatgpt)
    - **Google Antigravity**: [VS Code](https://marketplace.visualstudio.com/items?itemName=Google.google-antigravity), [VSCodium](https://open-vsx.org/extension/Google/google-antigravity)
    - **Mistral Vibe**: [VS Code](https://marketplace.visualstudio.com/items?itemName=mistralai.mistral-vibe-code), [VSCodium](https://open-vsx.org/extension/mistralai/mistral-vibe-code)
    - **OpenCode**: [VS Code](https://marketplace.visualstudio.com/items?itemName=sst-dev.opencode), [VSCodium](https://open-vsx.org/vscode/item?itemName=sst-dev.opencode)


### Step 7: Download the workshop materials
In the terminal, go to your home folder and download (*clone*) this repository. A **repository** is simply a folder whose history Git tracks.

```bash
# Create a directory for Git repositories under your home directory (abbreviated by ~)
mkdir -p ~/Git
# Go to the newly created directory
cd ~/Git
# Clone the workshop materials
git clone https://github.com/AgenttiX/ai-workshop.git
# Go to the workshop directory
cd ai-workshop
```

On Windows, in PowerShell:

```powershell
New-Item -ItemType Directory -Force ~\Git
cd ~\Git
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
```


### Step 8: Create the Python environment and check everything
A **virtual environment** ("venv") is a fancy name for a folder with its own copy of Python and its own packages, separate from the rest of your computer, so that the workshop can't break anything else and vice versa. This keeps dependencies on different packages separate between projects. The workshop's check script creates it for you. In the terminal, inside the `~/Git/ai-workshop` folder, run:

| System | Command |
|---|---|
| Linux, macOS | `python3 -m workshop.check` |
| Windows | `py -3 -m workshop.check` |

It asks whether to create the virtual environment. Press Enter to answer yes. It then installs the packages the exercises need (this may take a few minutes) and checks your setup. It should end with **"All required checks passed. You're ready for the workshop!"** Lines marked `WARN` are fine: they're optional.

Finally, **activate** the virtual environment, i.e. tell the terminal to use its Python:

| System | Command |
|---|---|
| Linux, macOS | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |

The start of the prompt changes to `(.venv)`. From now on, `python` means the Python of the workshops virtual environment. On Windows, if PowerShell says that "running scripts is disabled on this system", run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```


### Step 9: Open the workshop in VS Code and say hello to the AI
**1.** In VS Code: **File → Open Folder…** and choose the `ai-workshop` folder in the `Git` folder of your home folder. If VS Code asks whether you trust the authors of the files, answer yes.

**2.** Choose the virtual environment: press Ctrl+Shift+P (Cmd+Shift+P on a Mac), type **Python: Select Interpreter** and pick the one that mentions `.venv`. If the bottom-right corner of VS Code already shows `.venv`, you can skip this.

**3.** Open a terminal in VS Code (**Terminal → New Terminal**). The prompt should start with `(.venv)`. Run

```bash
python -m workshop.check
```

once more. Everything should be `OK` or `WARN`.

**4.** Open your AI extension. E.g. for Claude Code, click the orange Spark icon. If it asks you to sign in, use the account of [step 1](#step-1-an-account-for-an-ai-provider). Then ask:

> What is this repository about?

It reads the files of the repository and answers. If it does, you're ready. See you at the workshop!

### Step 10: Local models (optional)
Local AI models are a viable alternative to cloud-hosted models. The ones that fit on consumer hardware are not as capable as frontier-level cloud models, but they are sufficient for many kinds of useful work. As long as you have enough free system memory (RAM) or GPU memory (VRAM), you can run a useful AI agent even on a laptop without any internet access. **The setup instructions below are provided already in this readme before the workshop, as downloading a multi-gigabyte LLM model can take several hours.**

There are several backends for running LLMs locally. These can be connected to any compatible client or harness, such as OpenCode or [Open WebUI](https://openwebui.com/).

<details open>
<summary><b>LM Studio</b></summary>

**One of the easiest ways to get started with local LLMs is [LM Studio](https://lmstudio.ai/)**, as it bundles the LLM backend, chat interface and agent harness in one package. You can just download it, select an LLM that fits on your computer, and get started. See the [step 2](#step-4-install-an-ai-desktop-client-optional-but-useful) for the installation instructions.

Once you have installed LM Studio, select *Model Search* from the menu on the left. Then, select a model that fits on your computer. If you have a GPU, prefer models for which LM Studio says *Full GPU Offload Possible*.

However, LM Studio is not very optimized, and with other backends it's possible to fit much larger models and run them much faster on the same hardware. For this, please see the llama.cpp and vLLM instructions below.

</details>

<details>
<summary><b>llama.cpp</b></summary>

[llama.cpp](https://llama.app/) is perhaps the most popular LLM backend for consumer hardware, as it works on a variety of platforms and is capable of splitting an LLM between a GPU and a CPU, if the LLM doesn't fit entirely in the VRAM of the GPU. This is known as CPU offloading. This way, even a GPU with 4 GB of VRAM can be highly useful. Some example configurations:
- [Laptop with integrated GPU only](https://github.com/AgenttiX/agx-ai/blob/main/llama-cpp-l14/preset.ini)
- [Laptop with NVIDIA GPU (4 GB VRAM)](https://github.com/AgenttiX/agx-ai/blob/main/llama-cpp-t550/preset.ini)
- [NVIDIA RTX 3070](https://github.com/AgenttiX/agx-ai/blob/main/llama-cpp-rtx3070/preset.ini)

On Linux, installing llama.cpp in Docker keeps it nicely contained. On Windows it's preferred to install natively, since on Windows, Docker and WSL have significant overhead for RAM use and accessing the filesystem.
</details>

<details>
<summary><b>vLLM</b></summary>

The highest performance is often achieved with [vLLM](https://vllm.ai/). However, it often requires more memory than llama.cpp for the same models, and its support for CPU offloading is limited. It also requires extensive configuration for optimal performance, and has limited support of model formats.
</details>

<details open>
<summary><b>Selecting a local LLM model</b></summary>

The optimal choice of a local LLM model depends on the amount of system memory (RAM) and GPU memory (VRAM) available on the computer, as the model must be loaded entirely in RAM+VRAM to work efficiently. Below are some examples of openly available (=open-weight) LLM models suitable for various hardware. The RAM and VRAM numbers are for the memory that is free after your operating system and other programs. On Linux, you can check your free RAM with `free -h`, and free VRAM with `nvtop` or `nvidia-smi`, if you have them installed. On Windows, you can check these in Task Manager.
- GPU, >= 16 GB: Qwen 3.8-27B, [Gemma 4 26B A4B QAT](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-qat-GGUF), [Gemma 4 31B QAT](https://huggingface.co/unsloth/gemma-4-31B-it-qat-GGUF)
- GPU/CPU, >= 16 GB total (VRAM+RAM): [Gemma 4 26B A4B QAT](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-qat-GGUF) (e.g. 8 GB GPU + 8 GB CPU)
- GPU/CPU, >= 8 GB total (VRAM+RAM): [Gemma 4 12B QAT](https://huggingface.co/unsloth/gemma-4-12B-it-qat-GGUF)
- GPU/CPU, >= 6 GB total (VRAM+RAM): [Gemma 4 E4B QAT](https://huggingface.co/unsloth/gemma-4-E4B-it-qat-GGUF)
- GPU/CPU, >= 4 GB total (VRAM+RAM): [Gemma 4 E2B QAT](https://huggingface.co/unsloth/gemma-4-E2B-it-qat-GGUF)

Further information on Google's Gemma 4 series is available in its [official documentation](https://ai.google.dev/gemma/docs/core). For most use, 4-bit quantization is a good trade-off between size and quality. The E2B and E4B versions are useful for testing and as generic assistants, but for actual work the versions from 12B onwards are preferred. If you have enough memory, the 26B A4B is preferable over the smaller variants, since the former is significantly faster due to its mixture-of-experts (MoE) architecture despite its larger size. In model names, B refers to how many billions of parameters it has, which determines the memory use. E refers to an effective number of parameters. A means how many parameters are activated during the generation of each output token, which determines the output speed (tokens/s). For example, the Gemma 4 26B A4B has 26 billion parameters, of which 4 billion are activated when generating each output token.
</details>


---

## Troubleshooting
When something fails, the error message usually says why. Paste it into any AI chatbot and ask "I'm new to this. What does this error mean and how do I fix it?" If that doesn't help, email us.

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
| You can't install programs on a university-managed laptop | On Cubbli, request sudo rights with `i-want-sudo-access`. The Python and VS Code installers above work without administrator rights. |
| `claude` is not found in the terminal | Install the command-line version ([step 5](#step-5-install-a-command-line-ai-harness)), then open a new terminal. Claude Desktop may not add the command, and the VS Code extension doesn't. |
| `git pull` says your local changes would be overwritten | You have edited files in the exercises. Run these three commands one at a time: <br>`git stash` (puts your changes aside)<br>`git pull`<br>`git stash pop` (brings your changes back)<br> You can also ask your AI agent to do this for you.|
| Claude Code says that your plan doesn't include it | The free Claude plan doesn't include Claude Code; see [step 1](#step-1-an-account-for-an-ai-provider). |

---


## Exercises
The exercises are in [`exercises/`](./exercises/). Each has a `README.md` with the task, the prompts to try and explanations for those who want to know more. The solutions, with an explanation of what happened, are in [`solutions/`](./solutions/). Try first, then peek.
