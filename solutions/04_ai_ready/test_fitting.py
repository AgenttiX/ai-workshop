import numpy as np
import pytest

import fitting
from workshop.data import G_STANDARD, pendulum_measurements


def test_exact_line_is_recovered():
    x = np.linspace(0, 10, 11)
    y = 3 * x - 2
    slope, intercept, slope_err, intercept_err = fitting.weighted_linear_fit(x, y)
    assert slope == pytest.approx(3)
    assert intercept == pytest.approx(-2)
    # With unit weights the standard errors are those for sigma = 1.
    assert slope_err == pytest.approx(np.sqrt(1 / np.sum((x - x.mean()) ** 2)))
    assert intercept_err > 0


def test_weights_pull_the_fit_towards_precise_points():
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 10.0])  # The last point is an outlier...
    sigma = np.array([0.01, 0.01, 10.0])  # ...with a huge uncertainty.
    slope, intercept, _, _ = fitting.weighted_linear_fit(x, y, sigma)
    assert slope == pytest.approx(1, abs=1e-3)
    assert intercept == pytest.approx(0, abs=1e-3)


def test_chi_squared_of_a_perfect_fit_is_zero():
    x = np.array([1.0, 2.0, 3.0])
    assert fitting.chi_squared(x, 2 * x + 1, np.ones(3), 2, 1) == 0


def test_chi_squared_counts_deviations_in_sigmas():
    x = np.array([1.0, 2.0])
    y = np.array([1.0, 2.0]) + np.array([0.5, -1.0])
    assert fitting.chi_squared(x, y, np.array([0.5, 0.5]), 1, 0) == pytest.approx(1 + 4)


def test_pendulum_g_from_simulated_data():
    lengths, periods, errors = pendulum_measurements(n=20, seed=3)
    g, g_err = fitting.pendulum_g(lengths, periods, errors)
    assert g_err > 0
    assert abs(g - G_STANDARD) < 3 * g_err
    assert g == pytest.approx(G_STANDARD, rel=0.02)
