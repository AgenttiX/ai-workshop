# Exercise 05: A skill (10 min)
A *skill* is a Markdown file with instructions that the agent loads when the task matches its description (or when you invoke it with `/name`). It's how you teach the agent a workflow once instead of in every prompt.

## Task

### 1. Copy the skill
Copy the template into the skills directory of this repository. In the terminal, in the workshop folder, run the commands for your system:

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

`.claude/skills/plot-style/SKILL.md` now defines a project skill. (`~/.claude/skills/` would make it personal.)

### 2. Read it
The frontmatter `description` decides *when* the skill fires — that's the important part.

### 3. Test it
In Claude Code, type these two commands, one at a time:

```text
/reload-skills
/clear
```

`/reload-skills` is needed once, because `.claude/skills/` didn't exist when the session started, and `/clear` starts a new conversation. Then ask for a plot without mentioning the style:

> Plot the period of a pendulum as a function of its length from 0.1 m to 2 m and save the figure.

Did it call `apply_style()` and `save_fig()`? Did it label the axes with units?

### 4. Add a rule of your own
Edit the skill to add one rule of your own (e.g. "always use colorblind-friendly colours" or "use SI units only") and test again.

## What to look for
- Skills vs. `AGENTS.md`: `AGENTS.md` is *always* in the context; a skill is loaded *when relevant*. Put the permanent rules in `AGENTS.md` and the workflows in skills.
- Skills can include scripts and reference files next to `SKILL.md`. See [the documentation](https://code.claude.com/docs/en/skills).
