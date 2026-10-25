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
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m workshop.check
