import matplotlib as mpl

mpl.use("Agg")
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pytest

import pendulum_period
from workshop.data import G_STANDARD


@pytest.fixture
def fig():
    fig = pendulum_period.plot_period()
    yield fig
    plt.close(fig)


def test_returns_a_figure(fig):
    assert isinstance(fig, Figure)


def test_axis_labels_have_units(fig):
    ax = fig.axes[0]
    assert ax.get_xlabel().endswith("(m)")
    assert ax.get_ylabel().endswith("(s)")


def test_legend_and_no_title(fig):
    ax = fig.axes[0]
    assert ax.get_legend() is not None
    assert ax.get_title() == ""
    assert fig.get_suptitle() == ""


def test_curve_is_the_pendulum_period(fig):
    line = fig.axes[0].get_lines()[0]
    lengths, periods = np.asarray(line.get_xdata()), np.asarray(line.get_ydata())
    assert lengths[0] == pytest.approx(0.1)
    assert lengths[-1] == pytest.approx(2.0)
    # A pendulum of length g / pi^2 (almost exactly 1 m) has a period of 2 s.
    assert np.interp(G_STANDARD / np.pi**2, lengths, periods) == pytest.approx(2.0, rel=1e-4)


def test_colours_are_okabe_ito(fig):
    okabe_ito = {mcolors.to_hex(color) for color in mpl.color_sequences["okabe_ito"]}
    for line in fig.axes[0].get_lines():
        assert mcolors.to_hex(line.get_color()) in okabe_ito


def test_main_saves_png_and_pdf(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(plt, "show", lambda: None)
    pendulum_period.main()
    plt.close("all")
    for ext in ("png", "pdf"):
        assert (tmp_path / "fig" / f"pendulum_period.{ext}").stat().st_size > 0
