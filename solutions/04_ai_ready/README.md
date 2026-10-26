# Solution of exercise 04: AI-ready code

## The result
[`fitting.py`](./fitting.py) with type hints and docstrings, and [`test_fitting.py`](./test_fitting.py) with five tests. All three tools are clean:

The commands are the same on Linux, macOS and Windows, with the virtual environment active:

```bash
ruff check solutions/04_ai_ready
pyrefly check solutions/04_ai_ready/fitting.py
pytest solutions/04_ai_ready
```

For your own version, replace `solutions` with `exercises`. The exercise folder is excluded from the repository-wide checks, so always pass the path explicitly.

## What was going on
*Lint* is automatic checking of code for likely bugs and style problems; `ruff` is the linter here. *Type checking* checks that values match the declared *type hints* (e.g. `x: float`); `pyrefly` is the type checker. Ruff finds 22 problems in the starter:

| Rule | Where | Problem | Fix in the solution |
|---|---|---|---|
| D100, D103 | module, 3 functions | No docstrings | Docstrings that give the formula, the units and the reference. |
| I001, F401 | imports | Unsorted imports; `os` is imported but never used | Removed. |
| F403, F405 ×4 | `from math import *` | A star import hides where `sqrt` and `pi` come from, so ruff can't tell whether they exist | `np.sqrt` and `np.pi`. |
| B006 | `result={}` | A mutable default argument is created once and shared by all calls, so each call silently adds to the same dict | Parameter removed; the function returns its results. |
| SIM108 | `if sigma is None:` | Four lines where one expression does | `w = np.ones_like(x) if sigma is None else 1 / np.asarray(sigma) ** 2` |
| N806 ×6 | `S`, `Sx`, …, `D` | Upper-case local variables (PEP 8, the Python style guide, wants lower case) | `s`, `sx`, …, `delta`. |
| E722 | `chi_squared` | A bare `except:` catches *every* error, even a typo or Ctrl+C, and returns `None` | The `try` is gone. Errors now surface where they happen. |
| RUF059 ×2 | `pendulum_g` | `intercept` and `intercept_err` are unpacked but never used | `_`. |

`pyrefly check exercises/04_ai_ready/fitting.py` reports **0 errors** on the starter (pyrefly 1.3.1). Code without type hints gives a type checker almost nothing to check. It starts to pay off once the hints are there: then every later change is checked against them.

**The physics was right.** The fit uses the standard weighted least-squares formulas (Bevington & Robinson, *Data Reduction and Error Analysis for the Physical Sciences*, ch. 6): with weights $w_i = 1/\sigma_i^2$, $\Delta = S S_{xx} - S_x^2$, the slope is $(S S_{xy} - S_x S_y)/\Delta$ with standard error $\sqrt{S/\Delta}$, where $S = \sum w_i$, $S_x = \sum w_i x_i$ and so on. We checked `weighted_linear_fit` against `numpy.polyfit(x, y, 1, w=1/sigma, cov="unscaled")`: slopes, intercepts and errors agree to about $10^{-15}$. The propagation $\sigma_{T^2} = 2 T \sigma_T$ and $\sigma_g = 4 \pi^2 \sigma_a / a^2$ for $g = 4 \pi^2 / a$ is correct to first order. One subtlety: with `sigma=None`, the errors are those for $\sigma = 1$, not estimated from the scatter of the data. The solution's test says so; the docstring could say it more clearly.

## What the tests check physically
1. **An exact line is recovered**: $y = 3x - 2$ gives slope 3 and intercept −2, and the slope error equals $1/\sqrt{\sum (x_i - \bar{x})^2}$, the textbook value for $\sigma = 1$.
2. **Weights matter**: an outlier with a huge uncertainty barely moves the fit.
3. **$\chi^2$ of a perfect fit is 0.**
4. **$\chi^2$ counts deviations in units of σ**: deviations of 0.5 and −1 with σ = 0.5 give $1^2 + 2^2 = 5$.
5. **The pendulum gives $g$**: 20 simulated measurements with $g = 9.80665$ m/s² give $g = 9.809 \pm 0.051$ m/s², which must be within 3σ and 2 % of the true value.

Each test has an answer known *independently* of the code. "The function runs without errors" is not such a test.

## What the agent typically does
1. Runs the three tools, adds hints and docstrings, fixes the lint, writes tests, runs them again.
2. Loops until everything is clean. This loop, run → read the error → fix → rerun, is the agent checking its own work.

Warning signs:

- It silences the tools instead of fixing the code: `# noqa`, `# type: ignore`, or new `ignore` entries in `pyproject.toml`.
- It "fixes" the bare `except` with `except Exception: return None`, which still hides errors.
- Its tests compare the function with a copy of the same formula. That tests nothing.
- It changes the physics while fixing style, e.g. drops the weights. Read the diff: the formulas must stay the same.

## Step 4: coverage
*Coverage* measures which lines the tests actually run. `pytest --cov=exercises/04_ai_ready --cov-report=term-missing exercises/04_ai_ready` lists the missed lines of `fitting.py` under `Missing` (the same command on every system). The repository's settings also add the `workshop` package to the report; ignore those lines. The solution reaches 100 % of `fitting.py`. 100 % coverage means every line ran, not that every result was checked.

## What to take away about prompting
1. Give the agent a way to check its work and ask it to use it: "run ruff, pyrefly and pytest and fix everything they report".
2. Say what *not* to do: "don't silence warnings; don't change the formulas".
3. Ask for tests with known answers, and read them. Weak tests make the loop worthless.
