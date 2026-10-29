# Exercise 10: Your own project (25 min)
Everything above, on the research code you actually work with. Bring a small project if you can.

## Checklist
1. **Version control first.** Code, notes and small inputs go in Git; large data stays outside the repository, and the agent reads it but doesn't write to it. The agent's edits are then always reviewable and reversible. Never let an agent loose on the only copy of anything.
2. **Open it in Claude Code and run `/init`** (OpenCode: there is no `/init`; it reads `AGENTS.md` natively, so just ask the agent to write a draft `AGENTS.md`). Read the draft and fix it (exercise 02). Add the research context the agent can't guess: what the code computes and why, the conventions (units, signs, metric signature, notation), where the raw data and the results live, and what it must never change (raw data, published numbers).
3. **Permissions.** Decide what it may run without asking: tests, linters and your analysis scripts are usually safe. Keep the prompt for anything that writes to the data or results folders, installs packages, uses the network or submits jobs to a cluster. Write the allow-list in `.claude/settings.json` (see this repository's); with OpenCode it's the `permissions` rules of `opencode.json(c)` (see this repository's [`opencode.jsonc`](../../opencode.jsonc)).
4. **Give it a feedback signal from the physics.** If there are no tests, ask it to write regression tests from the current output: "Write tests that pin the current results of X, so that we notice if they change." Better still are checks against known physics: a limit with an analytic solution, a conservation law, a sum rule, a value from a paper (exercise 01). Add `ruff` and, if the code is typed, `pyrefly` (exercise 04).
5. **Make it reproducible.** Pin the environment (`requirements.txt` in a venv, or preferably [uv](https://docs.astral.sh/uv/)), fix the random seeds, and have one script per figure that regenerates it from the data. Then "reproduce figure 3" is a task the agent can check.
6. **A first research task.** Something you'd do by hand this week, small enough that you can check the result: reproduce a figure from your paper, check a derivation numerically, run a parameter scan, compare to a known limit. Start in plan mode, and ask for the check against known physics in the same prompt.
7. **Write down what you learned in `AGENTS.md`.** Every correction you had to make twice is a rule for the file.

## Ask the organizers
This is what we're here for. If you'd like, we'll look at your project together.
