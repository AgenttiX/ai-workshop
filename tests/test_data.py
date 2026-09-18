import numpy as np
import pytest

from workshop import data


def test_pendulum_period_one_second():
    # A "seconds pendulum" has a period of 2 s and a length of about 0.994 m.
    assert data.pendulum_period(0.994) == pytest.approx(2.0, abs=1e-3)


def test_measurements_are_reproducible():
    a = data.pendulum_measurements(seed=1)
    b = data.pendulum_measurements(seed=1)
    for x, y in zip(a, b, strict=True):
        np.testing.assert_array_equal(x, y)


def test_measurements_follow_the_pendulum_law():
    lengths, periods, errors = data.pendulum_measurements(n=50, period_err=0.001)
    assert lengths.shape == periods.shape == errors.shape == (50,)
    np.testing.assert_allclose(periods, data.pendulum_period(lengths), atol=5 * 0.001)


def test_csv_roundtrip(tmp_path):
    lengths, periods, errors = data.pendulum_measurements(n=5)
    path = str(tmp_path / "pendulum.csv")
    data.write_pendulum_csv(path, lengths, periods, errors)
    lengths2, periods2, errors2 = data.read_pendulum_csv(path)
    np.testing.assert_allclose(lengths2, lengths, atol=1e-3)
    np.testing.assert_allclose(periods2, periods, atol=1e-4)
    np.testing.assert_allclose(errors2, errors, atol=1e-4)
