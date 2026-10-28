# Exercise 00: Setup check (10 min)

## 1. Open the workshop
Open this repository in VS Code and activate the virtual environment in the terminal (the commands are in [step 8 of the setup guide](../../README.md#step-8-create-the-python-environment-and-check-everything)).

## 2. Run the environment check

```bash
python -m workshop.check
```

Everything marked `FAIL` has to be fixed. `WARN` is fine for `code`/`codium` if VS Code is not on your PATH.

## 3. Start Claude Code
Start Claude Code (the Spark icon in VS Code, or `claude` in the terminal) and log in.

Using [OpenCode](../other_agents.md#opencode) instead: start `opencode` in the terminal and log in, then continue with step 4. It reads `AGENTS.md` and `README.md` the same way.

## 4. Ask about the repository
Ask it:

> What is this repository about, and how do I run its tests?

It should read `AGENTS.md` and `README.md` and answer without you telling it where to look.

## 5. Look at what it did
Which files did it read? That's the "file access" that makes a harness different from a chat.

If something doesn't work, ask an organizer or pair up with your neighbour. The coffee break is reserved for debugging.
