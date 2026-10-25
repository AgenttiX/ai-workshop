# In PowerShell. Anthropic.Claude is the Claude desktop app.
winget install Python.Python.3.14 Git.Git Microsoft.VisualStudioCode Anthropic.Claude
# Alternatively, install the command-line Claude Code. This is included in Claude Desktop.
# irm https://claude.ai/install.ps1 | iex

# Close and reopen PowerShell, then:
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
py -3.14 -m venv venv
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m workshop.check
