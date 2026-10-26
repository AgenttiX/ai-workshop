# Exercise 02: Write an AGENTS.md (10 min)
`pendulum_lab/` is a small analysis project of the kind that lives in every research group:
a script, a data file, a run script, and conventions that exist only in someone's head.
It has no `AGENTS.md`, so an agent working on it has to guess.

## Task
1. Open a Claude Code session *in `exercises/02_agents_md/pendulum_lab/`*. In the terminal, from the repository folder:
   `cd exercises/02_agents_md/pendulum_lab` and then `claude` (the same in PowerShell). Run `/init`. It reads the project and writes a draft `CLAUDE.md`.
2. Read the draft critically. Which of the unwritten conventions did it find, and which did it miss?
   - The units are in the column names of the data file.
   - The analysis is run with `python run.py`, which uses the Python of the virtual environment.
   - The results go to `results/`, which is not tracked in Git.
   - The uncertainties in the data are 1σ.
   - The plots should use the workshop style (`workshop.plotting`).
3. Fix and complete the file by hand. Keep it short: an `AGENTS.md` is read by the agent on *every* session, so it costs context.
4. Verify: start a new session (`/clear`) and ask
   > How do I run the analysis, what are the units in the data, and where do the results go?

   A good `AGENTS.md` makes the answer correct without any file reads beyond it.
5. Rename `CLAUDE.md` to `AGENTS.md` and create a `CLAUDE.md` containing only `@AGENTS.md`, like the root of this repository does.
   `AGENTS.md` is the tool-agnostic convention; `CLAUDE.md` is what Claude Code reads.

## What to look for
- `/init` is a starting point, not an answer. The valuable part is what only you know.
- Claude Code also loads the `CLAUDE.md` files of the folders above the one you started it in, here the workshop's own.
  That's why the session in `pendulum_lab/` may already know a few things about the workshop.
- What belongs in `AGENTS.md`: commands, structure, conventions, what *not* to do.
  What doesn't: anything the agent can read from the code itself.
