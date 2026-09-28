# Solution of exercise 07: A subagent

## The result
`.claude/agents/physics-reviewer.md` exists, and asking "Use the physics-reviewer agent to review
exercises/04_ai_ready/fitting.py" makes the main agent launch the reviewer and show you its report.
To copy the file in step 1:

| System | Commands |
|---|---|
| Linux, macOS | `mkdir -p .claude/agents` and then `cp exercises/07_subagents/agents/physics-reviewer.md .claude/agents/` |
| Windows (PowerShell) | `New-Item -ItemType Directory -Force .claude\agents` and then `Copy-Item exercises\07_subagents\agents\physics-reviewer.md .claude\agents\` |

Claude Code notices new files in `.claude/agents/` within a few seconds; no restart is needed
([documentation](https://code.claude.com/docs/en/sub-agents)).

## What was going on
A *subagent* is a second agent that the main agent starts for one task. It has its own *context window*
(the text the model can see at once: instructions, files read, command output), so the files it reads don't fill yours.

The file has two parts. The *frontmatter*, the settings between the two `---` lines:

| Field | In the template | Meaning |
|---|---|---|
| `name` | `physics-reviewer` | The identifier you and the main agent use. |
| `description` | "Reviews scientific Python code … Use after writing or changing code that implements equations …" | When the main agent should delegate to it. Like a skill's description, it is the trigger. |
| `tools` | `Read, Grep, Glob, Bash` | The only tools it gets. No `Edit` or `Write`, so it can't edit files with the editing tools. |
| `model` | `sonnet` | Which Claude model runs it. Without it, Claude Code chooses. |

The body, below the frontmatter, is the subagent's system prompt: the instructions it starts with.
It replaces Claude Code's default system prompt for that subagent. The `CLAUDE.md` files are still loaded.

**How delegation works.** The main agent calls a tool (named `Agent`) with a task description.
The subagent starts fresh: it sees its system prompt, the project's `CLAUDE.md` and the task, but not your conversation.
It works with its own tools and returns one final message. Only that message enters the main conversation.
That's why you see the report but not the file reads.

## An illustration of a report
*This is an illustration we wrote to show the kind of report to expect. It is not a recorded run; your report will differ.*

> **Verdict:** probably correct. The formulas are right; the robustness problems can hide errors.
>
> **Findings:**
> 1. `fitting.py:6`: `result={}` is a mutable default argument. The same dict is shared by all calls and
>    overwritten on each one. Remove the parameter and return the values.
> 2. `fitting.py:31`: the bare `except:` returns `None` for any error, e.g. arrays of different lengths.
>    A wrong input then fails far away from its cause, or not at all. Let the exception propagate.
> 3. `fitting.py:21–22`: the standard errors $\sqrt{S/\Delta}$ and $\sqrt{S_{xx}/\Delta}$ are the standard
>    weighted least-squares results (Bevington & Robinson, ch. 6) *when σ is given*. With `sigma=None` they
>    assume σ = 1, which is wrong unless the data happen to have unit variance. Require `sigma`, or scale
>    the errors by $\sqrt{\chi^2/(N-2)}$ and document it.
> 4. `fitting.py:35`: no units anywhere. `pendulum_g` expects lengths in m. Fed the lab's `length_cm` column
>    directly, it returns $g \approx 981$ instead of $9.81$ m/s².
> 5. `fitting.py:38, 41`: $\sigma_{T^2} = 2 T \sigma_T$ and $\sigma_g = 4 \pi^2 \sigma_a / a^2$ are correct first-order
>    propagation, valid for $\sigma_T \ll T$. The intercept is fitted but not used, which is fine.
>
> **Missing tests:** an exact line $y = 3x - 2$ is recovered; $\chi^2 = 0$ for a perfect fit;
> the slope error for unit weights is $1/\sqrt{\sum (x_i - \bar{x})^2}$; simulated pendulum data give
> $g = 9.807$ m/s² within 3σ.

We checked the claims in it: the formulas against `numpy.polyfit(..., w=1/sigma, cov="unscaled")` (they agree to about $10^{-15}$),
and the 981 by fitting the exercise 02 data with the lengths left in cm. A real report may be wrong in places:
check each finding before acting on it, the same way you'd check a colleague's review.

## What the agent typically does
1. Recognises that you asked for the physics-reviewer and delegates. It often delegates on its own when a request
   matches the description, e.g. "check the physics of my fit".
2. Shows the subagent's report, sometimes with its own summary on top.
3. In step 3, it launches two subagents at the same time and waits for both.

Warning signs:
- It does the review itself instead of delegating. Name the agent explicitly, or check the file location and name.
- The report praises the code or stays vague ("consider adding tests"). The system prompt asks for file, line and fix.
- `Bash` can still change files, e.g. with `sed`. "You do not edit files" is an instruction, not a guarantee.
  The permission prompts are what actually protect you.

## Step 4: a checklist for your field
Add the mistakes you see most often, e.g. for field theory: metric signature, factors of $2\pi$ in Fourier transforms,
lattice spacing units. Short and concrete items work best.

## What to take away about prompting
1. Use a subagent when a long investigation should produce a *short* answer: reviews, searches, test runs.
2. The subagent sees only the task you (or the main agent) give it. Say what to review and what matters.
3. Each subagent re-reads what it needs and uses its own tokens (a token is a piece of text, a word or part of a word;
   usage is counted in tokens). Don't delegate what takes one file read.
