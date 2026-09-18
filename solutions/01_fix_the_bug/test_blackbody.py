import numpy as np
import pytest

import blackbody

#: Wien's displacement constant, m K
WIEN_B = 2.897771955e-3
#: Stefan-Boltzmann constant, W m^-2 K^-4
SIGMA = 5.670374419e-8


def test_wien_displacement_law():
    temperature = 5778.0  # The Sun
    assert blackbody.peak_wavelength(temperature) * temperature == pytest.approx(WIEN_B, rel=1e-3)


@pytest.mark.parametrize("temperature", [300.0, 5778.0, 20000.0])
def test_stefan_boltzmann_law(temperature: float):
    # The radiant exitance is pi times the integral of the spectral radiance over all wavelengths.
    wavelengths = np.geomspace(1e-9, 1e-2, 100_000)
    exitance = np.pi * np.trapezoid(blackbody.spectral_radiance(wavelengths, temperature), wavelengths)
    assert exitance == pytest.approx(SIGMA * temperature**4, rel=1e-3)
