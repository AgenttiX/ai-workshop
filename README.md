# Kumpula AI workshop for scientists 2026
A hands-on workshop on using AI harnesses (Claude Code and friends) effectively in research,
organized at the Kumpula Campus of the University of Helsinki in autumn 2026 by
[Aaron Haarti](https://github.com/haaaaron),
[Antti "Hippe" Hippeläinen](https://github.com/ahippelainen) and
[Mika Mäki](https://github.com/AgenttiX).

- Structure: 2 h foundations + 15 min break + 2 h advanced topics, in English
- Coordination: [Mattermost](https://cftgroup.chat/main/channels/ai-workshop)
- Slides: [`slides.html`](./slides.html) (reveal.js; press `S` for the speaker notes, `F` for full screen)
- Plan: [`plan/`](./plan/)

## Setup for the participants
1. Install [VS Code](https://code.visualstudio.com/) (or [VSCodium](https://vscodium.com/)), Git and Python 3.12.
2. Install [Claude Code](https://code.claude.com/docs/en/overview): the VS Code extension and/or the CLI,
   and log in with your Claude account.
   Backup: [GitHub Copilot](https://github.com/features/copilot) with the
   [GitHub Student Developer Pack](https://education.github.com/pack).
3. Clone this repository and install the requirements:
   ```bash
   git clone https://github.com/AgenttiX/ai-workshop.git
   cd ai-workshop
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m workshop.check
   ```
   The last command checks that everything is installed. It should end with "All required checks passed".
4. Open the repository in VS Code and start Claude Code. Ask it: "What is this repository about?"

## Exercises
The exercises are in [`exercises/`](./exercises/), and each of them has a `README.md` with the task and suggested prompts.
Reference solutions for the code exercises are in [`solutions/`](./solutions/).

## Development
- Run the tests: `pytest`
- Lint: `ruff check`
- Type check: `pyrefly check`
- Render the slides to a PDF: `./render.py slides.html` (requires Chromium or Chrome)
