# AGENTS.md

## Project description
This repository is for organizing an AI workshop for scientists
at the Kumpula Campus of the University of Helsinki in autumn 2026.

## Workshop description
- Structure: 2 h session + 15 min break + 2 h session
- Language: English
- Coordination: [Mattermost](https://cftgroup.chat/main/channels/ai-workshop)
- Exercise platform: Claude Code with Claude Team plan for scientists
  - Backup option for those without Claude: GitHub Copilot with GitHub Student Developer Pack
- Primary IDE: Visual Studio Code and VSCodium

## Workshop organizers
- [Aaron Haarti](https://github.com/haaaaron): PhD student in computational field theory
- [Antti "Hippe" Hippeläinen](https://github.com/ahippelainen): PhD student in holography
- [Mika Mäki](https://github.com/AgenttiX): PhD student in first-order cosmological phase transitions

## Project structure
- `./dev/` contains temporary files (Markdown etc.) that are not tracked in Git.
- `./plan/` contains documents for planning the workshop.
- `./slides.html` is the reveal.js presentations slides.

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
  - [Manifolder](https://github.com/AgenttiX/manifolder): Calabi-Yau manifold plotter Mika
  - [vote_for_lunch_online](https://github.com/ahippelainen/vote_for_lunch_online): restaurant voting app by Hippe
