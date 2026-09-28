# Pendulum lab
Determines the gravitational acceleration g by fitting T² = 4π² L / g to pendulum measurements.

## Commands
- Run the analysis in this folder with `python run.py`, on Linux, macOS and Windows alike.
  It runs `analyse.py` with the Python of the workshop's virtual environment (`../../../venv`),
  which has the `workshop` package that `analyse.py` imports.

## Data
- `data/pendulum.csv` holds the raw measurements. Don't edit it.
- The unit of each column is in its name: `length_cm` is in cm, `period_s` and `period_err_s` are in s.
- `period_err_s` is the 1σ (one standard deviation) uncertainty of the period.
- Read the file with `workshop.data.read_pendulum_csv`, which converts the lengths to m. Compute in SI units.

## Results
- The analysis writes `g.txt` and the figure `pendulum.png`/`.pdf` into `results/`.
- `results/` is not tracked in Git. Regenerate the results instead of committing them.

## Plots
- Use the workshop style: call `workshop.plotting.apply_style()` before plotting,
  and save with `workshop.plotting.save_fig(fig, name, fig_dir=RESULTS_DIR)`.
