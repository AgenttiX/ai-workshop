# Solution of exercise 10: Your own project

## The result
Your project is in Git, has an `AGENTS.md` (and a one-line `CLAUDE.md` with `@AGENTS.md`), a permission allow-list,
at least one test that checks a result, and one or two small changes made with the agent, reviewed and committed.
[`AGENTS.template.md`](./AGENTS.template.md) is a fill-in template for the `AGENTS.md`: copy it into your project,
replace everything in `<...>` and delete what doesn't apply.

## A worked example
Imagine a typical small research repository, `ising/`: a Monte Carlo script `simulate.py`, a notebook `analysis.ipynb`
that makes the plots, measured or generated data in `data/`, figures in `plots/`, no tests, not in Git.

**1. Version control first.** Git records every change, so every edit of the agent can be seen and undone.
A *commit* is a saved snapshot. The commands are the same in every terminal, including PowerShell:
```bash
git init
git add .
git commit -m "State before using an agent"
```
Before `git add .`, create a file `.gitignore` listing what shouldn't be tracked: large data, `plots/`, `.venv/`.
If Git asks who you are, run `git config --global user.name "Your Name"` and
`git config --global user.email "you@helsinki.fi"` once.

**2. `/init`, then fix the draft.** Start Claude Code in `ising/` and type `/init`. The draft usually gets the file
layout and the run command right. Typically missing, and only you know: that `data/` holds a month of cluster time
and must never be touched; that the temperature is in units of $J/k_B$; that `analysis.ipynb` expects the output files
of `simulate.py` under a particular name. Rename the file to `AGENTS.md`, add a `CLAUDE.md` with `@AGENTS.md`, and fill
in the gaps from the template.

**3. Permissions.** In `.claude/settings.json`, allow what is safe and deny what must not happen:
```json
{
  "permissions": {
    "allow": ["Bash(pytest:*)", "Bash(ruff check:*)", "Bash(git status:*)", "Bash(git diff:*)"],
    "deny": ["Edit(/data/**)"]
  }
}
```
`Edit(/data/**)` blocks Claude's file-editing tools, and recognised shell commands such as `sed` or `> file`,
in `data/` ([documentation](https://code.claude.com/docs/en/permissions#read-and-edit)).
It does not stop a Python script that opens files by itself. Backups are still your job.

**4. A feedback signal.** There are no tests, so pin the current behaviour first. A *regression test* checks that a
result doesn't change unnoticed:
> Write pytest tests that run simulate.py for an 8×8 lattice with a fixed seed and check the energy and magnetisation
> against the current output. Put them in tests/. Don't change simulate.py.

Then add at least one test with a known answer, e.g. the exact energy per spin of the 2D Ising model at
low temperature ($-2J$ in the ground state). A regression test pins bugs as well as correct results; a physics test doesn't.

**5. A first real task.** Small and checkable, e.g.
> Add a command-line option --seed to simulate.py. Run the tests afterwards.

Read the diff (the list of removed and added lines) and commit.

**6. A first research task.** Use plan mode, e.g.
> Plan how to compute the specific heat from the energy fluctuations, $C = (\langle E^2 \rangle - \langle E \rangle^2)/T^2$,
> and plot it against T around $T_c = 2/\ln(1 + \sqrt{2}) \approx 2.269$.

Read the plan before approving it. Is the formula right, and in which units? Check the result against something you
know: here the peak should be near $T_c$ and grow with the lattice size.

**7. Write down what you learned.** Every correction you made twice becomes a line in `AGENTS.md`,
e.g. "Always run the 8×8 test before the 64×64 production run."

## What the agent typically does
On an unfamiliar project it reads a lot before acting, and it tends to "improve" things you didn't ask about.
Warning signs: edits outside the files you named, new dependencies, reformatting of whole files, or "all tests pass"
when there are no tests. Keep tasks small and review every diff before committing.

## What to take away about prompting
1. Say *where*, *what* and *how to check* in every task.
2. Put what you'd otherwise repeat into `AGENTS.md`, what must always happen into hooks or permissions,
   and recurring workflows into skills.
3. Commit before each task and review after it. With Git, a bad attempt costs one `git restore .`
   (it discards the uncommitted changes to tracked files; new files stay).
