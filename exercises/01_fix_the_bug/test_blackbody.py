import pytest

import blackbody

#: Wien's displacement constant, m K
WIEN_B = 2.897771955e-3


def test_wien_displacement_law():
    temperature = 5778.0  # The Sun
    assert blackbody.peak_wavelength(temperature) * temperature == pytest.approx(WIEN_B, rel=1e-3)
