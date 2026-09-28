# Exercise 00: Setup check (10 min)
1. Open this repository in VS Code and activate the virtualenv in the terminal.
2. Run the environment check:
   ```bash
   python -m workshop.check
   ```
   Everything marked `FAIL` has to be fixed. `MISS` is fine for `claude` if you use the VS Code extension,
   and for `code`/`codium` if VS Code is not on your PATH.
3. Start Claude Code (the extension's icon in VS Code, or `claude` in the terminal) and log in.
4. Ask it:
   > What is this repository about, and how do I run its tests?

   It should read `AGENTS.md` and `README.md` and answer without you telling it where to look.
5. Look at what it did: which files did it read? That's the "file access" that makes a harness different from a chat.

If something doesn't work, ask an organizer or pair up with your neighbour. The lunch break is reserved for debugging.
