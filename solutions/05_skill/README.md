# Solution of exercise 05: A skill

## The result
- [`plot-style/SKILL.md`](./plot-style/SKILL.md): the skill of the exercise with one added rule, number 7: colour-blind-friendly colours from the Okabe–Ito palette.
- [`pendulum_period.py`](./pendulum_period.py): a plot that follows every rule. Run it with `python solutions/05_skill/pendulum_period.py`; it saves `fig/pendulum_period.png` and `.pdf`.
- [`test_pendulum_period.py`](./test_pendulum_period.py): tests that check the rules, e.g. units in the axis labels, no title, a returned `Figure`, only Okabe–Ito colours. Run them with `pytest solutions/05_skill`.

The commands are the same on every system once the virtual environment is active. To copy the skill in step 1, use the commands for your system:

**Linux and macOS:**

```bash
mkdir -p .claude/skills
cp -r exercises/05_skill/plot-style .claude/skills/
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force .claude\skills
Copy-Item -Recurse exercises\05_skill\plot-style .claude\skills\
```

## What was going on
A *skill* is a folder with a `SKILL.md` file: instructions that Claude Code loads when they are relevant. The file starts with *frontmatter*, a block of settings between two `---` lines at the top. At the start of a session, only the `description` from the frontmatter is loaded into the context. The rest of the file is loaded when Claude decides that the task matches the description, or when you type `/plot-style` ([documentation](https://code.claude.com/docs/en/skills)). That is why the description matters most: "Use whenever creating, editing or saving a Matplotlib figure" tells Claude *when*.

Claude Code notices new and edited skills in `.claude/skills/` during a session, without a restart. If the folder `.claude/skills/` didn't exist when the session started, type `/reload-skills` once.

## The added rule
Matplotlib's default colours (`tab10`) were not designed for colour-vision deficiencies. In a simulation of deuteranopia (a form of red-green colour blindness; Machado et al. 2009 model, full severity) that we ran, the default green and red became almost the same colour: a colour difference of ΔE ≈ 7, against ΔE ≥ 17 for every pair of the eight Okabe–Ito colours. The [Okabe–Ito palette](https://jfly.uni-koeln.de/color/) was designed to stay distinguishable for the common forms of colour blindness. Matplotlib has it built in since version 3.11 as `matplotlib.color_sequences["okabe_ito"]` (the workshop uses 3.11.2). Another accessible option is the `petroff10` style of Matplotlib 3.10 and newer. The rule passes the colours explicitly with `color=`, because rule 1 forbids setting `rcParams` by hand. Colour alone is never fully safe, so the rule also asks for different line styles or markers when needed.

## What the agent typically does
With the skill installed, a request such as "plot the period of a pendulum" typically makes Claude load the skill (you see a line saying that it used `plot-style`) and then call `apply_style()` and `save_fig()`. Without the skill, agents often call `plt.savefig()` directly, add a title, and label an axis without the unit.

Warning signs:

- The skill doesn't load at all. The description may not match the request, or the file is in the wrong place: it must be `.claude/skills/plot-style/SKILL.md`.
- It loads the skill but ignores a rule. Rules that are short, concrete and checkable are followed more reliably.

## Step 3: checking the plot
Check the plot, not the agent's summary of it: open the PNG, read the axis labels, look for a title. The tests in `test_pendulum_period.py` do the same checks automatically, which is how you would enforce a style in a real project. The curve test also checks physics: a pendulum of length $g/\pi^2 \approx 0.994$ m has a period of exactly 2 s.

## What to take away about prompting
1. Write a workflow down once as a skill instead of repeating it in every prompt.
2. The description is the trigger. Say *when* to use the skill, in the words you'd use in a request.
3. Skills vs. `AGENTS.md`: `AGENTS.md` is always loaded; a skill only when relevant. Permanent rules go in `AGENTS.md`, task-specific workflows in skills.
