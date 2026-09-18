r"""Synthetic measurement data for the exercises.

The exercises 02 and 04 analyse pendulum measurements: the period $T$ of a pendulum of length $L$ is
$T = 2 \pi \sqrt{L / g}$, so a linear fit of $T^2$ against $L$ gives the gravitational acceleration $g$.
"""

import csv

import numpy as np

from workshop.type_hints import FloatArr

#: Standard gravity, m/s^2
G_STANDARD: float = 9.80665


def pendulum_period(length: FloatArr | float, g: float = G_STANDARD) -> FloatArr | float:
    """$T$, the period of a simple pendulum in s.

    :param length: $L$, the length of the pendulum in m
    :param g: $g$, the gravitational acceleration in m/s^2
    """
    return 2 * np.pi * np.sqrt(length / g)


def pendulum_measurements(
    n: int = 10,
    seed: int = 2026,
    g: float = G_STANDARD,
    period_err: float = 0.01,
    length_min: float = 0.1,
    length_max: float = 1.0,
) -> tuple[FloatArr, FloatArr, FloatArr]:
    r"""Simulate measurements of the period of a pendulum for a range of lengths.

    :param n: number of measurements
    :param seed: seed of the random number generator
    :param g: $g$, the gravitational acceleration in m/s^2
    :param period_err: $\sigma_T$, the standard deviation of the measured periods in s
    :param length_min: shortest pendulum in m
    :param length_max: longest pendulum in m
    :return: lengths in m, measured periods in s, and the uncertainties of the periods in s
    """
    rng = np.random.default_rng(seed)
    lengths = np.linspace(length_min, length_max, n)
    periods = pendulum_period(lengths, g) + rng.normal(0, period_err, n)
    errors = np.full(n, period_err)
    return lengths, periods, errors


def write_pendulum_csv(path: str, lengths: FloatArr, periods: FloatArr, errors: FloatArr) -> None:
    """Write pendulum measurements to a CSV file.

    The units are in the column names, as is the convention in the lab: lengths in cm, periods in s.
    """
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["length_cm", "period_s", "period_err_s"])
        for length, period, error in zip(lengths, periods, errors, strict=True):
            writer.writerow([f"{100 * length:.1f}", f"{period:.4f}", f"{error:.4f}"])


def read_pendulum_csv(path: str) -> tuple[FloatArr, FloatArr, FloatArr]:
    """Read pendulum measurements from a CSV file written by :func:`write_pendulum_csv`.

    :return: lengths in m, periods in s, and the uncertainties of the periods in s
    """
    data = np.genfromtxt(path, delimiter=",", names=True)
    return data["length_cm"] / 100, data["period_s"], data["period_err_s"]
