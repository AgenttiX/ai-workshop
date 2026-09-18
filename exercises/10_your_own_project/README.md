# Exercise 10: Your own project (25 min)
Everything above, on the code base you actually work with. Bring a small one if you can.

## Checklist
1. **Version control first.** If the project is not in Git, `git init` and commit. The agent's edits are then
   always reviewable and reversible. Never let an agent loose on the only copy of anything.
2. **Open it in Claude Code and run `/init`.** Read the draft and fix it (exercise 02). Add the commands
   for running, testing and linting, the structure, the conventions, and what it must not touch (data, results).
3. **Permissions.** Decide what it may run without asking: `pytest`, `ruff`, `git status` are safe; `rm`, `pip install`
   and anything with network access deserve a prompt. Write the allow-list in `.claude/settings.json` (see this repository's).
4. **Give it a feedback signal.** If there are no tests, ask it to write regression tests from the current output
   (exercise 04): "Write tests that pin the current results of X, so that we notice if they change."
   Add `ruff` and, if the code is typed, `pyrefly`.
5. **A first real task.** Something small and verifiable: fix a warning, add a CLI option, document a function,
   port a script to a function with a test. Review the diff. Commit.
6. **A first real *research* task.** Something you'd do by hand this week: reproduce a plot from a paper, check
   a derivation numerically, scan a parameter. Use plan mode, and keep the task small enough that you can check the result.
7. **Write down what you learned in `AGENTS.md`.** Every correction you had to make twice is a rule for the file.

## Ask the organizers
This is what we're here for. If you'd like, we'll look at your project together.
