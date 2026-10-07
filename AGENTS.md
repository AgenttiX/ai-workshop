# AGENTS.md

## Project description
This repository is for organizing an AI workshop for scientists
at the Kumpula Campus of the University of Helsinki in autumn 2026.

## Workshop description
- Participants: BSc, MSc and PhD students and researchers of the Faculty of Science (voluntary participation)
- Structure: 2 h session (10:00–12:00) + 1 h lunch break + 2 h session (13:00–15:00)
- Language: English
- Coordination: [Mattermost](https://cftgroup.chat/main/channels/ai-workshop)
- Exercise platform: Claude Code with Claude Team plan for scientists
  - Backup option for those without Claude: GitHub Copilot with GitHub Student Developer Pack
- Primary IDE: Visual Studio Code and VSCodium
- Programming language for exercises: Python 3.12 or newer

## Workshop organizers
- [Aaron Haarti](https://github.com/haaaaron): PhD student in computational field theory
- [Antti "Hippe" Hippeläinen](https://github.com/ahippelainen): PhD student in holography
- [Mika Mäki](https://github.com/AgenttiX): PhD student in first-order cosmological phase transitions

## Commands
- Set up the virtualenv at `./venv` and check the environment: `python3 -m workshop.check` (Windows: `py -3 -m workshop.check`).
  It creates the venv and installs `requirements.txt` if needed.
- Run tests: `pytest` (runs `tests/` and `solutions/`; run the tests of an exercise with e.g. `pytest exercises/01_fix_the_bug`)
- Lint: `ruff check`
- Type checking: `pyrefly check`
- Render the slides to a PDF: `./render.py slides.html`
- Copy the setup scripts to the README: `./setup/sync_readme.py`

## Project structure
- `./dev/` contains temporary files (Markdown etc.) that are not tracked in Git.
- `./figures/` contains the figures of the slides, and the data and Plotly scripts for the plots made by us
  (requirements in `figures/requirements.txt`).
- `./exercises/` contains the exercises for the participants, one directory per exercise with a `README.md`.
  The starters are deliberately imperfect (e.g. `01_fix_the_bug` has a physics bug and `04_ai_ready` has lint errors),
  so their tests are not run by the default `pytest`, and `04_ai_ready` is excluded from the linter and type checker.
- `./plan/` contains documents for planning the workshop.
- `./poster/` contains the A3 poster (`poster.svg`, Inkscape-compatible); `preview.sh` renders it to `poster/build/`.
- `./setup/` contains the quick-setup commands of the README for each operating system. These are the source of truth:
  edit them and run `./setup/sync_readme.py`, not the code blocks in `README.md`. Tested in CI by `.github/workflows/setup.yml`.
- `./slides.html` is the reveal.js presentation slides. Speaker notes are in `<aside class="notes">` elements.
- `./solutions/` contains the reference solutions of the exercises, each with a `README.md` explaining what happened.
  The code is tested in CI.
- `./themes/` contains custom reveal.js themes for the slides (`_base.css` + one file of variables per theme, see `themes/README.md`).
- `./tests/` contains the tests of the `workshop` package.
- `./workshop/` is a small Python package with helpers shared by the exercises (environment check, plotting style, data generation).

## Participant-facing text
- The audience ranges from complete beginners (no VS Code, terminal or venv experience) to advanced users.
  Define every term at first use, and give commands for Linux (primary), native Windows (PowerShell) and macOS.

## Code style
- Type hints that work on Python 3.12 and newer everywhere except in the deliberately messy exercise starters.
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
