# Exercises
Each exercise has a `README.md` with the task, suggested prompts and what to look for.
Use your own words for the prompts: the suggested ones are only there in case you're stuck.
Reference solutions for the code exercises are in [`../solutions/`](../solutions/) — try before you peek.
The exercises are written for Claude Code. Using GitHub Copilot, Codex or Antigravity instead? See [the extra guide](./other_agents.md).

| # | Exercise | Session | Time | What you practise |
|---|---|---|---|---|
| 00 | [Setup check](./00_setup/) | 1 | 10 min | The environment and the first prompt |
| 01 | [Fix the bug](./01_fix_the_bug/) | 1 | 10 min | Giving a task, reviewing a diff, running tests |
| 02 | [Write an AGENTS.md](./02_agents_md/) | 1 | 10 min | Project instructions for the agent |
| 03 | [PTtools spectrum](./03_pttools/) | 1 (bonus) | 15 min | Making the agent learn a research library from its source |
| 04 | [AI-ready code](./04_ai_ready/) | 1 | 15 min | Tests, types and lint as the agent's feedback loop |
| 05 | [A skill](./05_skill/) | 1 | 10 min | Reusable instructions the agent loads when relevant |
| 06 | [A hook](./06_hook/) | 2 | 10 min | Deterministic automation on tool events |
| 07 | [A subagent](./07_subagents/) | 2 | 10 min | Specialist agents with their own context |
| 08 | [MCP](./08_mcp/) | 2 (optional) | 10 min | Connecting external tools and data |
| 09 | [Local models](./09_local_models/) | 2 (optional) | 15 min | Running the harness on a model on your own hardware |
| 10 | [Your own project](./10_your_own_project/) | 2 | 25 min | Making your own code base agent-ready |

## Before you start
- **Claude Code starts in *Auto* mode**, where it edits files and runs commands without asking.
  Exercise 01 shows how to switch to *Manual*, where it asks you first. Use Manual whenever you want to see each step.
- **Do the exercises in order.** Some build on earlier ones: exercise 07 reviews the code of exercise 04,
  and the hook of exercise 06 stays active in the later ones.
- **Start each exercise in a new conversation** with `/clear`, so that the previous one doesn't confuse the agent.
- **Undoing changes.** Git keeps the original files. `git status` lists what has changed, `git diff` shows how,
  and `git restore <file>` puts a file back the way it was. To reset all the exercises, run `git restore .` and then
  `git clean -fd`, which also deletes the new files you created (your virtual environment and settings stay).

## Running the tests
The exercise starters are deliberately imperfect, so their tests are not part of the repository's `pytest` run.
Run the tests of an exercise with e.g. `pytest exercises/01_fix_the_bug`.
