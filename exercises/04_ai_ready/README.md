# Exercise 04: AI-ready code (15 min)
`fitting.py` does a weighted linear fit and determines $g$ from pendulum data. It works — probably. It has no tests, no type hints, no docstrings, and the linter has opinions about it:

```bash
ruff check exercises/04_ai_ready/fitting.py
pyrefly check exercises/04_ai_ready/fitting.py
```

(This directory is excluded from the repository-wide checks on purpose, so pass the file explicitly.)

## Task

### 1. Ask for AI-ready code
Ask your AI agent to make the module AI-ready:

> Add type hints, docstrings and unit tests to exercises/04_ai_ready/fitting.py. Then run ruff check, pyrefly check and pytest on it and fix everything they report. Repeat until all are clean. Put the tests in exercises/04_ai_ready/test_fitting.py.

### 2. Watch the loop
Run the tool → read the error → fix → re-run. This is the agent *verifying its own work*. Without the tools it could only believe the code works.

### 3. Read the tests
Read the tests it wrote. Are they testing physics (e.g. an exact line is recovered, χ² of a perfect fit is 0, the pendulum data give $g \approx 9.8$ m/s²), or just that the function runs? Ask for better ones if needed.

### 4. Bonus: coverage
Ask it to add `--cov` coverage reporting and to show which lines aren't covered.

## What to look for
- The tools give the agent a *feedback signal*. That's why tests, linting, typing and CI matter more with AI, not less.
- `AGENTS.md` should tell the agent which commands to run. Check that this repository's does.
- The reference solution in `solutions/04_ai_ready/` shows one way to do it.
