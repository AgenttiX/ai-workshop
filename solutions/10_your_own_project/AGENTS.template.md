# <Project name>
<One sentence: what the code computes or analyses, and for which paper or thesis chapter.>

## Commands
- Set up: `<e.g. python -m venv .venv && pip install -r requirements.txt>`
- Run: `<e.g. python simulate.py --config configs/default.toml>`
- Test: `<e.g. pytest>` (takes <time>; run `<fast subset>` while iterating)
- Lint and type check: `<e.g. ruff check && pyrefly check>`

## Structure
- `<src/ or the main script>`: <what it does>
- `<data/raw/>`: raw data. Read-only; never edit, move or delete.
- `<results/>`: generated output, not in Git. Regenerate with `<command>`.
- `<notebooks/>`: exploration only; the code that produces results lives in `<src/>`.

## Conventions
- Units: <e.g. SI throughout; lengths in the input files are in cm (the unit is in the column name)>.
- Uncertainties: <e.g. 1σ standard deviations; systematic and statistical errors kept separate>.
- Physics conventions: <e.g. metric signature (-,+,+,+), ħ = c = k_B = 1, Fourier convention>.
- Random numbers: <e.g. always seeded; seeds are in the config file>.
- Style: <e.g. type hints and Sphinx docstrings; plots with plotting.apply_style()>.

## How results are verified
- <e.g. test_*.py compare against analytic limits: free field, T → 0, known literature values (cite them)>.
- <e.g. regression tests pin the numbers in Table 2 of the paper; if they change, explain why before updating them>.
- A change is done when <e.g. pytest, ruff and pyrefly pass and the affected plot has been looked at>.

## Don't
- <e.g. edit data/raw/, commit results/, change a tolerance to make a test pass, install packages without asking>.
