"""Gravitational wave spectra of a first-order phase transition with PTtools.

Reference solution of exercise 03.
"""

import matplotlib.pyplot as plt
import numpy as np
from pttools.bubble import Bubble
from pttools.models import BagModel
from pttools.omgw0 import Spectrum
from pttools.ssm import NucType

from workshop.plotting import apply_style, save_fig
from workshop.type_hints import FloatArr


def compute_spectrum(v_wall: float, alpha_n: float, r_star: float = 0.1) -> tuple[FloatArr, FloatArr]:
    r"""Compute the gravitational wave power spectrum today for a bubble in the bag model.

    :param v_wall: $v_\text{wall}$, wall speed of the bubble
    :param alpha_n: $\alpha_n$, transition strength at the nucleation temperature
    :param r_star: $r_*$, mean bubble spacing in units of the Hubble length
    :return: frequencies in Hz, and $\Omega_\text{gw} h^2$ at those frequencies
    """
    model = BagModel(alpha_n_min=min(alpha_n, 0.01))
    bubble = Bubble(model, v_wall=v_wall, alpha_n=alpha_n)
    spectrum = Spectrum(bubble, nuc_type=NucType.EXPONENTIAL, r_star=r_star)
    return np.asarray(spectrum.f(), dtype=float), np.asarray(spectrum.omgw0(), dtype=float)


def plot_spectra(v_walls: tuple[float, ...] = (0.4, 0.6, 0.8), alpha_n: float = 0.2) -> None:
    """Plot the spectra for several wall velocities in one figure."""
    apply_style()
    fig, ax = plt.subplots()
    for v_wall in v_walls:
        f, omgw0 = compute_spectrum(v_wall, alpha_n)
        ax.plot(f, omgw0, label=rf"$v_\text{{wall}} = {v_wall}$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("$f$ (Hz)")
    ax.set_ylabel(r"$\Omega_\text{gw} h^2$")
    ax.set_title(rf"Bag model, $\alpha_n = {alpha_n}$")
    ax.legend()
    print(save_fig(fig, "spectra"))
    plt.show()


if __name__ == "__main__":
    plot_spectra()
