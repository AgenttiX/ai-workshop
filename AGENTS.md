# AGENTS.md

## Project description
This repository is for organizing an AI workshop for scientists
at the Kumpula Campus of the University of Helsinki in autumn 2026.

## Workshop description
- Participants: BSc, MSc and PhD students and researchers of the Faculty of Science (voluntary participation)
- Structure: 2 h session + 15 min break + 2 h session
- Language: English
- Coordination: [Mattermost](https://cftgroup.chat/main/channels/ai-workshop)
- Exercise platform: Claude Code with Claude Team plan for scientists
  - Backup option for those without Claude: GitHub Copilot with GitHub Student Developer Pack
- Primary IDE: Visual Studio Code and VSCodium
- Programming language for exercises: Python 3.12

## Workshop organizers
- [Aaron Haarti](https://github.com/haaaaron): PhD student in computational field theory
- [Antti "Hippe" Hippeläinen](https://github.com/ahippelainen): PhD student in holography
- [Mika Mäki](https://github.com/AgenttiX): PhD student in first-order cosmological phase transitions

## Commands
- Install dependencies: `pip install -r requirements.txt` (use the virtualenv at `./venv`)
- Check the environment: `python -m workshop.check`
- Run tests: `pytest` (runs `tests/` and `solutions/`; run the tests of an exercise with e.g. `pytest exercises/01_fix_the_bug`)
- Lint: `ruff check`
- Type checking: `pyrefly check`
- Render the slides to a PDF: `./render.py slides.html`

## Project structure
- `./dev/` contains temporary files (Markdown etc.) that are not tracked in Git.
- `./exercises/` contains the exercises for the participants, one directory per exercise with a `README.md`.
  The starters are deliberately imperfect (e.g. `01_fix_the_bug` has a physics bug and `04_ai_ready` has lint errors),
  so their tests are not run by the default `pytest`, and `04_ai_ready` is excluded from the linter and type checker.
- `./plan/` contains documents for planning the workshop.
- `./slides.html` is the reveal.js presentation slides. Speaker notes are in `<aside class="notes">` elements.
- `./solutions/` contains the reference solutions of the exercises. These are tested in CI.
- `./tests/` contains the tests of the `workshop` package.
- `./workshop/` is a small Python package with helpers shared by the exercises (environment check, plotting style, data generation).

## Code style
- Python 3.12 type hints everywhere except in the deliberately messy exercise starters.
- Sphinx-style docstrings. The code is read by workshop participants, so prefer clarity over cleverness.

## Commands for developing the examples
- Run Python tests: `pytest`
- Lint: `ruff check`
- Type checking: `pyrefly check`

## General instructions
- When producing a long response, also output it as a Markdown file in `./dev/`.

## Relevant sources
The repositories below may also be available locally in the same parent directory as this repository.
If you need them, you may `git clone` them there.

- [Hippe's Claude configs](https://github.com/ahippelainen/claude-loadout)
- [Mika's Claude & local AI server configs](https://github.com/AgenttiX/agx-ai)
- [Mika's lecture on unit testing & CI/CD for scientific Python](https://github.com/CFT-HY/unit-testing-ci-cd): created with reveal.js
- [Mika's PhD presentations](https://github.com/AgenttiX/phd-presentations): created with reveal.js
- [PTPlot](https://github.com/CFT-HY/PTPlot/tree/mika-dev): Mika's research software for plotting first-order cosmological phase transitions
- [PTtools](https://github.com/CFT-HY/pttools/tree/dev): Mika's research software for modeling first-order cosmological phase transitions
- Vibe-coded projects
  - [Bubble simulation](https://github.com/AgenttiX/bubble-simulation):
    lattice simulation of a first-order phase transition by Mika
  - [Manifolder](https://github.com/AgenttiX/manifolder): Calabi-Yau manifold plotter by Mika
  - [vote_for_lunch_online](https://github.com/ahippelainen/vote_for_lunch_online): restaurant voting app by Hippe
