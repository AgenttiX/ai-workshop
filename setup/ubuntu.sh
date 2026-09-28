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
