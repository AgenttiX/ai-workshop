"""Determine the gravitational acceleration from the pendulum measurements."""

import os

import matplotlib.pyplot as plt
import numpy as np

from workshop.data import read_pendulum_csv
from workshop.plotting import apply_style, save_fig

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "pendulum.csv")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


def main() -> None:
    r"""Fit $T^2 = 4 \pi^2 L / g$ and save the result."""
    apply_style()
    lengths, periods, errors = read_pendulum_csv(DATA_PATH)
    slope, intercept = np.polyfit(lengths, periods**2, 1)
    g = 4 * np.pi**2 / slope

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "g.txt"), "w") as file:
        file.write(f"g = {g:.3f} m/s^2\n")

    fig, ax = plt.subplots()
    ax.errorbar(lengths, periods**2, yerr=2 * periods * errors, fmt="o", label="measurements")
    ax.plot(lengths, slope * lengths + intercept, label=f"fit: $g$ = {g:.3f} m/s$^2$")
    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Period$^2$ (s$^2$)")
    ax.legend()
    save_fig(fig, "pendulum", fig_dir=RESULTS_DIR)
    print(f"g = {g:.3f} m/s^2")


if __name__ == "__main__":
    main()
