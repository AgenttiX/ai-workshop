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
