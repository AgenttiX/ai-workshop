"""Planck's law of black-body radiation.

Reference solution of exercise 01: the exponent of the wavelength was 4 instead of 5.
"""

import matplotlib.pyplot as plt
import numpy as np

from workshop.plotting import apply_style, save_fig
from workshop.type_hints import FloatArr

#: Planck constant, J s
H = 6.62607015e-34
#: Speed of light, m/s
C = 299792458.0
#: Boltzmann constant, J/K
K_B = 1.380649e-23


def spectral_radiance(wavelength: FloatArr, temperature: float) -> FloatArr:
    r"""$B_\lambda(\lambda, T)$, the spectral radiance of a black body per unit wavelength, W sr^-1 m^-3.

    :param wavelength: $\lambda$, wavelength in m
    :param temperature: $T$, temperature in K
    """
    x = H * C / (wavelength * K_B * temperature)
    with np.errstate(over="ignore"):
        return 2 * H * C**2 / wavelength**5 / np.expm1(x)


def peak_wavelength(temperature: float) -> float:
    r"""$\lambda_\text{max}$, the wavelength of the maximum spectral radiance, found numerically, in m.

    :param temperature: $T$, temperature in K
    """
    wavelengths = np.geomspace(1e-8, 1e-3, 100_000)
    return float(wavelengths[np.argmax(spectral_radiance(wavelengths, temperature))])


def main() -> None:
    """Plot the spectra of a few black bodies."""
    apply_style()
    wavelengths = np.geomspace(1e-7, 1e-5, 500)
    fig, ax = plt.subplots()
    for temperature in (3000.0, 5778.0, 10000.0):
        ax.plot(wavelengths * 1e9, spectral_radiance(wavelengths, temperature), label=f"{temperature:.0f} K")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel(r"$B_\lambda$ (W sr$^{-1}$ m$^{-3}$)")
    ax.legend()
    print(save_fig(fig, "blackbody"))
    plt.show()


if __name__ == "__main__":
    main()
