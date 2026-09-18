"""Gravitational wave spectra of a first-order phase transition with PTtools."""

from workshop.type_hints import FloatArr


def compute_spectrum(v_wall: float, alpha_n: float, r_star: float = 0.1) -> tuple[FloatArr, FloatArr]:
    r"""Compute the gravitational wave power spectrum today for a bubble in the bag model.

    :param v_wall: $v_\text{wall}$, wall speed of the bubble
    :param alpha_n: $\alpha_n$, transition strength at the nucleation temperature
    :param r_star: $r_*$, mean bubble spacing in units of the Hubble length
    :return: frequencies in Hz, and $\Omega_\text{gw} h^2$ at those frequencies
    """
    raise NotImplementedError


def plot_spectra(v_walls: tuple[float, ...] = (0.4, 0.6, 0.8), alpha_n: float = 0.2) -> None:
    """Plot the spectra for several wall velocities in one figure."""
    raise NotImplementedError


if __name__ == "__main__":
    plot_spectra()
