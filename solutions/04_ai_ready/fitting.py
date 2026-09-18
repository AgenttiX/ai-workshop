"""Weighted linear least squares and the gravitational acceleration from pendulum measurements.

Reference solution of exercise 04.
"""

import numpy as np

from workshop.type_hints import FloatArr


def weighted_linear_fit(
    x: FloatArr, y: FloatArr, sigma: FloatArr | None = None
) -> tuple[float, float, float, float]:
    r"""Fit $y = a x + b$ by weighted least squares with weights $1 / \sigma^2$.

    The formulas are the standard ones, e.g. Bevington & Robinson, Data Reduction and Error Analysis, ch. 6.

    :param x: independent variable
    :param y: dependent variable
    :param sigma: standard deviations of ``y``, or None for equal weights
    :return: slope $a$, intercept $b$, and their standard errors
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.ones_like(x) if sigma is None else 1 / np.asarray(sigma, dtype=float) ** 2
    s = np.sum(w)
    sx = np.sum(w * x)
    sy = np.sum(w * y)
    sxx = np.sum(w * x * x)
    sxy = np.sum(w * x * y)
    delta = s * sxx - sx**2
    slope = (s * sxy - sx * sy) / delta
    intercept = (sxx * sy - sx * sxy) / delta
    slope_err = np.sqrt(s / delta)
    intercept_err = np.sqrt(sxx / delta)
    return float(slope), float(intercept), float(slope_err), float(intercept_err)


def chi_squared(x: FloatArr, y: FloatArr, sigma: FloatArr, slope: float, intercept: float) -> float:
    r"""$\chi^2$ of the line $y = a x + b$ with respect to the data."""
    return float(np.sum(((np.asarray(y) - (slope * np.asarray(x) + intercept)) / np.asarray(sigma)) ** 2))


def pendulum_g(lengths: FloatArr, periods: FloatArr, period_errors: FloatArr) -> tuple[float, float]:
    r"""$g$, the gravitational acceleration from pendulum measurements, and its standard error.

    Uses $T^2 = 4 \pi^2 L / g$, with $\sigma_{T^2} = 2 T \sigma_T$ by linear error propagation.

    :param lengths: $L$, pendulum lengths in m
    :param periods: $T$, measured periods in s
    :param period_errors: $\sigma_T$, standard deviations of the periods in s
    :return: $g$ in m/s^2 and its standard error
    """
    periods = np.asarray(periods, dtype=float)
    t2 = periods**2
    t2_err = 2 * periods * np.asarray(period_errors, dtype=float)
    slope, _, slope_err, _ = weighted_linear_fit(np.asarray(lengths, dtype=float), t2, t2_err)
    g = 4 * np.pi**2 / slope
    g_err = 4 * np.pi**2 * slope_err / slope**2
    return g, g_err
