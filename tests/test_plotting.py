import os.path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from workshop import plotting


def test_apply_style_sets_rcparams():
    plotting.apply_style()
    for key, value in plotting.STYLE.items():
        assert plt.rcParams[key] == value


def test_save_fig_writes_files(tmp_path):
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    paths = plotting.save_fig(fig, "line", fig_dir=str(tmp_path), formats=("png", "svg"))
    plt.close(fig)
    assert paths == [os.path.join(tmp_path, "line.png"), os.path.join(tmp_path, "line.svg")]
    for path in paths:
        assert os.path.getsize(path) > 0
