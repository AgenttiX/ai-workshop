"""The plotting style of the workshop.

This is what the "plot-style" skill of exercise 05 makes the agent use.
"""

import os.path

import matplotlib.pyplot as plt

#: Directory for the figures, relative to the current working directory
FIG_DIR = "fig"

#: Matplotlib settings shared by all the plots of the workshop
STYLE: dict[str, object] = {
    "axes.grid": True,
    "axes.labelsize": "large",
    "figure.constrained_layout.use": True,
    "figure.dpi": 100,
    "font.size": 12,
    "grid.alpha": 0.3,
    "legend.frameon": False,
    "lines.linewidth": 2,
    "savefig.bbox": "tight",
    "savefig.dpi": 200,
}


def apply_style() -> None:
    """Apply the workshop plotting style to Matplotlib."""
    plt.rcParams.update(STYLE)


def save_fig(
    fig: plt.Figure, name: str, fig_dir: str = FIG_DIR, formats: tuple[str, ...] = ("png", "pdf")
) -> list[str]:
    """Save a figure in the given formats and return the paths.

    :param fig: the figure
    :param name: the file name without the extension
    :param fig_dir: the directory, which is created if it does not exist
    :param formats: the file formats
    """
    os.makedirs(fig_dir, exist_ok=True)
    paths = [os.path.join(fig_dir, f"{name}.{fmt}") for fmt in formats]
    for path in paths:
        fig.savefig(path)
    return paths
