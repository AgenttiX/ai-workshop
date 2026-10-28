# In PowerShell. Anthropic.Claude is the Claude desktop app.
winget install Python.Python.3.14 Git.Git Microsoft.VisualStudioCode Anthropic.Claude
# The command-line Claude Code. Claude Desktop doesn't always install it.
irm https://claude.ai/install.ps1 | iex
# The installer puts claude.exe in ~\.local\bin but doesn't add that folder to PATH
$bin = "$env:USERPROFILE\.local\bin"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (";$userPath;" -notlike "*;$bin;*") { [Environment]::SetEnvironmentVariable("Path", "$userPath;$bin", "User") }

# Close and reopen PowerShell, then:
New-Item -ItemType Directory -Force ~\Git
cd ~\Git
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
py -3.14 -m venv .venv
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python3 -m workshop.check
