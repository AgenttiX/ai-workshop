# Solution of exercise 02: Write an AGENTS.md

## The result
Two files in `pendulum_lab/`:
- [`pendulum_lab/AGENTS.md`](./pendulum_lab/AGENTS.md): about 20 lines covering the commands, the data, the results and the plots.
- [`pendulum_lab/CLAUDE.md`](./pendulum_lab/CLAUDE.md): only the line `@AGENTS.md`. The `@` imports the other file,
  so Claude Code reads `AGENTS.md` through it.

The files describe `exercises/02_agents_md/pendulum_lab/`; copy them there to try them.

`AGENTS.md` is a plain Markdown file that many coding agents read. `CLAUDE.md` is the file Claude Code looks for.
Keeping the content in `AGENTS.md` means that other tools and your colleagues read the same file.

Step 5 on the command line, inside `pendulum_lab/`:

| System | Commands |
|---|---|
| Linux, macOS | `mv CLAUDE.md AGENTS.md` and then `echo "@AGENTS.md" > CLAUDE.md` |
| Windows (PowerShell) | `Rename-Item CLAUDE.md AGENTS.md` and then `Set-Content CLAUDE.md "@AGENTS.md"` |

## What was going on
The five conventions differ in how visible they are in the files:

| Convention | Where it can be found | What `/init` typically does |
|---|---|---|
| Units in the column names | The header of `data/pendulum.csv` (`length_cm`, `period_s`, `period_err_s`) | Often finds it if it opens the CSV file. |
| How to run the analysis | `run.py` | Usually finds it: a run script is an obvious thing to document. |
| Results go to `results/`, not tracked in Git | `RESULTS_DIR` in `analyse.py`. The "not in Git" part is in the `.gitignore` of the workshop root, outside the folder | Often finds the folder, often misses that it is ignored by Git. |
| Uncertainties are 1σ | Nowhere in `pendulum_lab/` | Can't find it. It may guess, or not mention the uncertainties at all. |
| Plots use `workshop.plotting` | The imports in `analyse.py` | May describe it as a fact about the code rather than as a rule for new plots. |

You can check the Git part yourself: `git check-ignore -v results/g.txt` prints the `.gitignore` rule that ignores it
(after you have run the analysis once). The command is the same on all systems.

**Why 1σ can't be found.** The column `period_err_s` says 0.0100 s. That number could be one standard deviation,
two standard deviations, a 95 % confidence interval, half the resolution of the stopwatch, or the standard error
of a mean over several swings. The file doesn't say which, and the code doesn't either. Only the person who
measured knows. That's exactly the kind of fact an `AGENTS.md` is for.
(In this workshop the data are simulated by `workshop/data.py`, whose docstring calls the value a standard deviation.
An agent that follows the import could find it there, but a real lab has no such file.)
One more trap: `analyse.py` plots error bars of `2 * periods * errors`. That is the propagated uncertainty of $T^2$,
$\sigma_{T^2} = 2 T \sigma_T$, not "2σ". Humans and agents both misread this kind of line.

## What the agent typically does
1. Lists the folder and reads `analyse.py`, `run.py` and often the first lines of the CSV file.
2. Writes a `CLAUDE.md` with an overview, the run command and the file layout.
   Drafts are often longer than needed, e.g. they describe the fit that anyone can read from `analyse.py`.

Warning signs: it states a convention you never told it (e.g. "uncertainties are 95 % confidence intervals")
as if it were a fact, or it documents what the code does line by line instead of what the code can't tell.

## The workshop's own CLAUDE.md is also loaded
Claude Code loads `CLAUDE.md` from the folder where you start it *and from every folder above it*
([documentation](https://code.claude.com/docs/en/memory#how-claude-md-files-load)).
`pendulum_lab/` is inside the workshop repository, so a session started there, in the terminal or with the folder
opened as the VS Code workspace, also sees the workshop's root `CLAUDE.md`, and through it the workshop's `AGENTS.md`.
This affects the exercise in three ways:
- `/init` and the answers in step 4 may use facts from the workshop's file, e.g. that there is a `venv/`.
  A correct answer in step 4 is therefore not proof that *your* file is complete. Read your file and compare.
- Type `/context` to see which memory files are loaded, and in which order.
- By default, Claude Code reads an `AGENTS.md` on its own only if there is no `CLAUDE.md` in the folder or any folder
  above it ([documentation](https://code.claude.com/docs/en/memory#when-claude-code-reads-agents-md)).
  The workshop root has a `CLAUDE.md`, so a lone `pendulum_lab/AGENTS.md` would be ignored.
  The one-line `CLAUDE.md` of step 5 is what makes it load here.

## Step 4: a correct answer
"Run `python run.py` in `pendulum_lab/`. The lengths are in cm in the file (converted to m when read),
the periods and their 1σ uncertainties in s. The results go to `results/`, which is not tracked in Git."
If the answer is right but the agent had to open `analyse.py` or the CSV file to get it, your `AGENTS.md` is missing something.

## What to take away about prompting
1. Write down what the agent can't read from the files: conventions, units, what not to touch.
   Leave out what it can read from the code.
2. Keep the file short. It is loaded into every session and costs context each time.
   The [documentation](https://code.claude.com/docs/en/memory) suggests under 200 lines.
3. Test the file the way the agent uses it: a fresh session (`/clear`) and a question whose answer you know.
