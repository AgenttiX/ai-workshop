r"""The period of a simple pendulum as a function of its length.

Reference solution of exercise 05: a plot that follows every rule of the plot-style skill.
The period of a simple pendulum at small amplitudes is $T = 2 \pi \sqrt{L / g}$.
"""

import matplotlib as mpl
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from workshop import data
from workshop.plotting import apply_style, save_fig


def plot_period(length_min: float = 0.1, length_max: float = 2.0, n: int = 200) -> Figure:
    """Plot the period of a pendulum against its length, with simulated measurements.

    :param length_min: shortest pendulum in m
    :param length_max: longest pendulum in m
    :param n: number of points on the curve
    :return: the figure
    """
    colors = mpl.color_sequences["okabe_ito"]
    lengths = np.linspace(length_min, length_max, n)
    meas_lengths, meas_periods, meas_errors = data.pendulum_measurements()

    fig, ax = plt.subplots()
    ax.plot(lengths, data.pendulum_period(lengths), color=colors[5], label=r"$T = 2 \pi \sqrt{L / g}$")
    ax.errorbar(
        meas_lengths,
        meas_periods,
        yerr=meas_errors,
        fmt="o",
        color=colors[6],
        label=r"simulated measurements ($1 \sigma$)",
    )
    # The lengths span a factor of 20, less than two orders of magnitude, so the axes stay linear.
    ax.set_xlabel("Length $L$ (m)")
    ax.set_ylabel("Period $T$ (s)")
    ax.legend()
    return fig


def main() -> None:
    """Plot the period, save the figure into fig/ and show it."""
    apply_style()
    fig = plot_period()
    print(save_fig(fig, "pendulum_period"))
    plt.show()


if __name__ == "__main__":
    main()
