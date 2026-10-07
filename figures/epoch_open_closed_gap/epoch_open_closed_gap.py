"""Plot the Epoch Capabilities Index (ECI) of the best closed, open and consumer-GPU models against their release dates.

This is our own version of Epoch AI's chart *Open models lag state-of-the-art closed models by 4 months*
(https://epoch.ai/data-insights/open-closed-eci-gap), made from the same data (``benchmarked_models.csv``).
We have added a third curve for open-weights models that fit on a consumer-grade GPU with 32 GB of VRAM
(``consumer_gpu_models.csv``).

Each curve is a "frontier": a model is shown only if its ECI is higher than that of every earlier model of its group.

The result is an interactive HTML page: hover over a point to see its values, drag to zoom, double-click to reset.

Run with ``python -m figures.epoch_open_closed_gap.epoch_open_closed_gap`` in the root directory of the repository.
The requirements are in ``figures/requirements.txt``.
"""

import argparse
import csv
from dataclasses import dataclass
import datetime
from pathlib import Path

import plotly.graph_objects as go

from figures.common import COLOR_GRID, COLOR_TEXT, FONT, FONT_SIZE, write_html

DATA_DIR = Path(__file__).resolve().parent
EPOCH_DATA = DATA_DIR / "benchmarked_models.csv"
CONSUMER_DATA = DATA_DIR / "consumer_gpu_models.csv"
OUTPUT = DATA_DIR / "epoch_open_closed_gap.html"

#: The largest model that fits on a 32 GB GPU (billions of parameters).
#: Quantized to 4 bits (0.5 bytes per parameter), its weights take about 20 GB,
#: which leaves room for the context (KV cache) and the rest of the inference software.
MAX_CONSUMER_PARAMS = 40

#: The plotted range of the x-axis
X_MIN = datetime.date(2022, 12, 1)
X_MAX = datetime.date(2026, 9, 30)

#: The colors of Epoch AI's chart, and a third one for our curve
COLOR_CLOSED = "#00a5a6"
COLOR_OPEN = "#e1418f"
COLOR_CONSUMER = "#7b5cd6"

#: The models to label in the plot on each curve, as in Epoch AI's chart, and their labels.
#: The other models are shown without a label. The keys are the "Model group" column of benchmarked_models.csv
#: and the "Model" column of consumer_gpu_models.csv.
CLOSED_LABELS: dict[str, str] = {
    "GPT-4 (Mar 2023)": "GPT-4 (Mar 2023)",
    "Claude 3.5 Sonnet": "Claude 3.5 Sonnet",
    "o1-mini": "o1-mini",
    "o1": "o1",
    "o3": "o3",
    "GPT-5 Pro": "GPT-5 Pro",
    "GPT-5.3 Codex": "GPT-5.3 Codex",
    "GPT-5.5 Pro": "GPT-5.5 Pro",
}
OPEN_LABELS: dict[str, str] = {
    "Llama 2-70B": "Llama 2-70B",
    "Mixtral 8x7B": "Mixtral 8x7B",
    "Yi-34B": "Yi-34B",
    "Mixtral 8x22B": "Mixtral 8x22B",
    "Llama 3.1-405B": "Llama 3.1-405B",
    "DeepSeek-V3": "DeepSeek-V3",
    "DeepSeek-R1": "DeepSeek-R1",
    "Qwen3-235B-A22B-Thinking (Jul 2025)": "Qwen3-235B-A22B",
    "Kimi K2.6": "Kimi K2.6",
}
CONSUMER_LABELS: dict[str, str] = {
    "Qwen3-32B": "Qwen3-32B",
    "Gemma 4 31B": "Gemma 4 31B",
    "Qwen3.6-27B": "Qwen3.6-27B",
    "Qwen3.8-27B": "Qwen3.8-27B",
}

#: Label positions that differ from the default (above the marker, to its left): (xanchor, yanchor, xshift, yshift).
#: The keys are the labels.
LABEL_POSITIONS: dict[str, tuple[str, str, int, int]] = {
    "GPT-4 (Mar 2023)": ("left", "bottom", 8, 2),
    "Llama 2-70B": ("left", "top", 8, -4),
    "Yi-34B": ("left", "top", 8, -4),
    "Mixtral 8x22B": ("left", "top", 8, -4),
    "Llama 3.1-405B": ("left", "top", 8, -4),
    "DeepSeek-R1": ("left", "bottom", 8, 1),
    "Qwen3-235B-A22B": ("left", "top", 8, -4),
    "Qwen3-32B": ("left", "top", 8, -4),
    "Gemma 4 31B": ("right", "top", -6, -4),
    "Qwen3.6-27B": ("left", "top", 8, -4),
    "Qwen3.8-27B": ("right", "top", -8, -2),
}


@dataclass(frozen=True)
class Model:
    """The ECI of one model.

    :param name: name of the model
    :param release_date: release date of the model
    :param eci: Epoch Capabilities Index
    :param ci_low: lower limit of the 90 % confidence interval of the ECI
    :param ci_high: upper limit of the 90 % confidence interval of the ECI
    :param open_weights: whether the weights of the model can be downloaded
    """

    name: str
    release_date: datetime.date
    eci: float
    ci_low: float
    ci_high: float
    open_weights: bool


def load_epoch_models(path: Path) -> list[Model]:
    """Load the models that have an ECI score from Epoch AI's ``benchmarked_models.csv``.

    The file has one row per model version (e.g. different reasoning settings), but they share the ECI of the model.
    As in Epoch AI's chart, a model without an "Open weights" accessibility counts as closed.

    :param path: path to the CSV file
    :return: the models
    """
    models = []
    with path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            if not row["ECI"]:
                continue
            models.append(
                Model(
                    name=row["Model group"],
                    release_date=datetime.date.fromisoformat(row["Version release date"] or row["Publication date"]),
                    eci=float(row["ECI"]),
                    ci_low=float(row["ECI CI low"]),
                    ci_high=float(row["ECI CI high"]),
                    open_weights=row["Model accessibility"].startswith("Open weights"),
                )
            )
    return models


def load_consumer_models(path: Path, max_params: float = MAX_CONSUMER_PARAMS) -> list[Model]:
    """Load the open-weights models that fit on a consumer GPU from ``consumer_gpu_models.csv``.

    :param path: path to the CSV file
    :param max_params: the largest total number of parameters to include (billions)
    :return: the models
    """
    with path.open(encoding="utf-8", newline="") as file:
        return [
            Model(
                name=row["Model"],
                release_date=datetime.date.fromisoformat(row["Release date"]),
                eci=float(row["ECI"]),
                ci_low=float(row["ECI CI low"]),
                ci_high=float(row["ECI CI high"]),
                open_weights=True,
            )
            for row in csv.DictReader(file)
            if float(row["Total parameters (B)"]) <= max_params
        ]


def frontier(models: list[Model]) -> list[Model]:
    """Find the models that were better than every earlier model when they were released.

    Of the models released on the same day, only the best one is kept.

    :param models: the models
    :return: the frontier models, sorted by release date
    """
    best_of_day: dict[datetime.date, Model] = {}
    for model in models:
        if model.release_date not in best_of_day or model.eci > best_of_day[model.release_date].eci:
            best_of_day[model.release_date] = model
    result: list[Model] = []
    for model in sorted(best_of_day.values(), key=lambda model: model.release_date):
        if not result or model.eci > result[-1].eci:
            result.append(model)
    return result


def step_trace(models: list[Model], name: str, color: str, symbol: str) -> go.Scatter:
    """Create a trace of a frontier as a step line: each level holds until a better model is released.

    :param models: the frontier models, sorted by release date
    :param name: name of the trace in the legend
    :param color: color of the line and the markers
    :param symbol: Plotly marker symbol, so that the curves can be told apart without color
    :return: the trace
    """
    return go.Scatter(
        x=[model.release_date for model in models],
        y=[model.eci for model in models],
        mode="lines+markers",
        line={"color": color, "width": 3, "shape": "hv"},
        marker={"color": color, "size": 11, "symbol": symbol, "line": {"color": "white", "width": 2}},
        name=name,
        customdata=[[model.name, model.ci_low, model.ci_high] for model in models],
        hovertemplate="<b>%{customdata[0]}</b><br>"
        "Released %{x|%-d %b %Y}<br>"
        "ECI: %{y:.1f} (90 % CI: %{customdata[1]:.1f} \u2013 %{customdata[2]:.1f})"
        "<extra></extra>",
    )


def add_labels(fig: go.Figure, models: list[Model], labels: dict[str, str], color: str) -> None:
    """Label the models of a curve next to their markers.

    :param fig: the figure
    :param models: the models of the curve
    :param labels: the models to label and their labels
    :param color: color of the labels
    """
    for model in models:
        if model.name not in labels:
            continue
        label = labels[model.name]
        xanchor, yanchor, xshift, yshift = LABEL_POSITIONS.get(label, ("right", "bottom", -4, 4))
        fig.add_annotation(
            x=model.release_date,
            y=model.eci,
            text=label,
            showarrow=False,
            xanchor=xanchor,
            yanchor=yanchor,
            xshift=xshift,
            yshift=yshift,
            font={"size": FONT_SIZE - 3, "color": color},
        )


def make_figure(closed: list[Model], open_: list[Model], consumer: list[Model]) -> go.Figure:
    """Create the figure.

    :param closed: the frontier of the closed-weights models
    :param open_: the frontier of the open-weights models
    :param consumer: the frontier of the open-weights models that fit on a consumer GPU
    :return: the figure
    """
    fig = go.Figure()
    fig.add_trace(step_trace(closed, "Closed weights", COLOR_CLOSED, "circle"))
    fig.add_trace(step_trace(open_, "Open weights", COLOR_OPEN, "square"))
    fig.add_trace(
        step_trace(consumer, "Open weights, fits on a 32 GB GPU", COLOR_CONSUMER, "diamond")
    )
    add_labels(fig, closed, CLOSED_LABELS, COLOR_CLOSED)
    add_labels(fig, open_, OPEN_LABELS, COLOR_OPEN)
    add_labels(fig, consumer, CONSUMER_LABELS, COLOR_CONSUMER)

    fig.update_layout(
        autosize=True,
        margin={"l": 80, "r": 20, "t": 15, "b": 115},
        font={"family": f"{FONT}, sans-serif", "size": FONT_SIZE, "color": COLOR_TEXT},
        plot_bgcolor="white",
        paper_bgcolor="white",
        # In the upper left corner, which has no data
        legend={"x": 0.01, "y": 0.99, "xanchor": "left", "yanchor": "top", "bgcolor": "rgba(255, 255, 255, 0.8)",
                "font": {"size": FONT_SIZE - 2}},
        hoverlabel={"font": {"family": f"{FONT}, sans-serif", "size": FONT_SIZE - 2}},
    )
    fig.update_xaxes(
        title="Release date",
        range=[X_MIN, X_MAX],
        dtick="M6",
        tickformat="%b %Y",
        showgrid=True,
        gridcolor=COLOR_GRID,
        linecolor=COLOR_TEXT,
        ticks="outside",
    )
    fig.update_yaxes(
        title="Epoch Capabilities Index (ECI)",
        range=[104, 164],
        dtick=10,
        showgrid=True,
        gridcolor=COLOR_GRID,
        linecolor=COLOR_TEXT,
        ticks="outside",
    )
    fig.add_annotation(
        x=0,
        y=0,
        xref="paper",
        yref="paper",
        xanchor="left",
        yanchor="top",
        # In pixels below the x-axis, so that the position does not depend on the size of the figure
        yshift=-75,
        align="left",
        showarrow=False,
        text="Data: Epoch AI (CC BY 4.0). Closed and open weights: epoch.ai/data-insights/open-closed-eci-gap, "
        "May 2026.<br>32 GB GPU: Epoch AI's ECI data of October 2026 (epoch.ai/benchmarks), "
        f"models with \u2264 {MAX_CONSUMER_PARAMS} B parameters (4-bit quantized).",
        font={"size": FONT_SIZE - 5, "color": "#666666"},
    )
    return fig


def main() -> None:
    """Create the figure and save it as an HTML file."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=OUTPUT, help="the HTML file to write")
    args = parser.parse_args()

    models = load_epoch_models(EPOCH_DATA)
    closed = frontier([model for model in models if not model.open_weights])
    open_ = frontier([model for model in models if model.open_weights])
    consumer = frontier(load_consumer_models(CONSUMER_DATA))
    for name, curve in (("Closed", closed), ("Open", open_), ("32 GB GPU", consumer)):
        print(f"{name}: " + ", ".join(f"{model.name} ({model.eci:.1f})" for model in curve))

    fig = make_figure(closed, open_, consumer)
    write_html(fig, args.output, div_id="epoch-open-closed-gap")
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
