#!/usr/bin/env bash

sudo apt update
sudo apt install curl git python3 python3-venv
sudo snap install code --classic  # or: codium

# Claude desktop app from Anthropic's apt repository
sudo curl -fsSLo /usr/share/keyrings/claude-desktop-archive-keyring.asc https://downloads.claude.ai/claude-desktop/key.asc
echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/claude-desktop-archive-keyring.asc] https://downloads.claude.ai/claude-desktop/apt/stable stable main" | sudo tee /etc/apt/sources.list.d/claude-desktop.list
sudo apt update
sudo apt install claude-desktop
# Alternatively, install the command-line Claude Code. This is included in Claude Desktop.
# curl -fsSL https://claude.ai/install.sh | bash

# The workshop repository and its packages
git clone https://github.com/AgenttiX/ai-workshop.git
cd ai-workshop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m workshop.check
