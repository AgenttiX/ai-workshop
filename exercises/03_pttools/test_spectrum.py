import numpy as np
import pytest

import spectrum


@pytest.fixture(scope="module")
def bag_spectrum():
    return spectrum.compute_spectrum(v_wall=0.5, alpha_n=0.2)


def test_shapes(bag_spectrum):
    f, omgw0 = bag_spectrum
    assert f.ndim == 1
    assert f.shape == omgw0.shape
    assert f.size >= 100


def test_frequencies_are_positive_and_increasing(bag_spectrum):
    f, _ = bag_spectrum
    assert np.all(f > 0)
    assert np.all(np.diff(f) > 0)


def test_spectrum_has_a_peak(bag_spectrum):
    _, omgw0 = bag_spectrum
    assert np.all(omgw0 > 0)
    peak = int(np.argmax(omgw0))
    assert 0 < peak < omgw0.size - 1
