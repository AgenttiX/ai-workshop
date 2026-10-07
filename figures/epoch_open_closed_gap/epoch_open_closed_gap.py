"""Plot the Epoch Capabilities Index (ECI) of the best closed, open and consumer-GPU models against their release dates.

This is our own version of Epoch AI's chart *Open models lag state-of-the-art closed models by 4 months*
(https://epoch.ai/data-insights/open-closed-eci-gap), made from Epoch AI's newer ECI data (``eci_scores.csv``).
We have added a third curve for open-weights models that fit on a consumer-grade GPU with 32 GB of VRAM,
using the parameter counts of ``model_parameters.py``.

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
from figures.epoch_open_closed_gap.model_parameters import PARAMETERS, Parameters

DATA_DIR = Path(__file__).resolve().parent
ECI_DATA = DATA_DIR / "eci_scores.csv"
OUTPUT = DATA_DIR / "epoch_open_closed_gap.html"
#: When the ECI data was downloaded, for the footnote of the figure
DATA_DATE = "October 2026"

#: The largest model that fits on a 32 GB GPU (billions of parameters).
#: Quantized to 4 bits (0.5 bytes per parameter), its weights take about 20 GB,
#: which leaves room for the context (KV cache) and the rest of the inference software.
MAX_CONSUMER_PARAMS = 40

#: The plotted range of the x-axis
X_MIN = datetime.date(2022, 12, 1)
X_MAX = datetime.date(2027, 1, 15)

#: The colors of Epoch AI's chart, and a third one for our curve
COLOR_CLOSED = "#00a5a6"
COLOR_OPEN = "#e1418f"
COLOR_CONSUMER = "#7b5cd6"
#: The color of the highlighted models
COLOR_HIGHLIGHT = "#a16207"

#: The models to label in the plot on each curve, as in Epoch AI's chart, and their labels.
#: The other models are shown without a label. The keys are the "Model" column of eci_scores.csv.
CLOSED_LABELS: dict[str, str] = {
    "GPT-4 (Mar 2023)": "GPT-4 (Mar 2023)",
    "Claude 3.5 Sonnet": "Claude 3.5 Sonnet",
    "o1-mini": "o1-mini",
    "o1": "o1",
    "Gemini 2.5 Pro (Mar 2025)": "Gemini 2.5 Pro",
    "o3": "o3",
    "GPT-5": "GPT-5",
    "GPT-5.3 Codex": "GPT-5.3 Codex",
    "GPT-5.5 Pro": "GPT-5.5 Pro",
    "Claude Fable 5.1": "Claude Fable 5.1",
    "GPT-6 Astra": "GPT-6 Astra",
    "Claude Opus 5.5": "Claude Opus 5.5",
}
OPEN_LABELS: dict[str, str] = {
    "Llama 2-70B": "Llama 2-70B",
    "Mixtral 8x7B": "Mixtral 8x7B",
    "Yi-34B": "Yi-34B",
    "Mixtral 8x22B": "Mixtral 8x22B",
    "Llama 3.1-405B": "Llama 3.1-405B",
    "DeepSeek-V3": "DeepSeek-V3",
    "Qwen3-235B-A22B-Thinking (Jul 2025)": "Qwen3-235B-A22B",
    "Kimi K2.6": "Kimi K2.6",
    "Kimi K3": "Kimi K3",
}
CONSUMER_LABELS: dict[str, str] = {
    "Qwen3-32B": "Qwen3-32B",
    "Gemma 4 31B IT": "Gemma 4 31B",
    "Gemma 4 26B A4B": "Gemma 4 26B A4B",
    "Qwen3.6 27B": "Qwen3.6-27B",
    "Qwen 3.8 27B": "Qwen3.8-27B",
}

#: Models that fit on a consumer GPU that are shown as points even though they are not on the curve.
#: Gemma 4 E2B, E4B and 12B would belong here too, but they have no ECI score in Epoch AI's data of October 2026.
CONSUMER_EXTRA_MODELS = ("Gemma 4 26B A4B",)

#: Models whose markers and labels are shown in :data:`COLOR_HIGHLIGHT`, e.g. the ones discussed in the slides
HIGHLIGHTED_MODELS = ("Gemma 4 31B IT", "Gemma 4 26B A4B", "Qwen 3.8 27B")

#: Models with a horizontal line at their ECI from the left edge of the plot to their marker,
#: to show when the closed and open models reached the same level
REFERENCE_LINE_MODELS = ("Qwen 3.8 27B", "Gemma 4 26B A4B")
#: Labels that a reference line crosses. They get a white background, so that the line passes behind them.
LABELS_ON_REFERENCE_LINES = ("Qwen3-235B-A22B",)

#: Label positions that differ from the default (above the marker, to its left): (xanchor, yanchor, xshift, yshift).
#: The keys are the labels.
LABEL_POSITIONS: dict[str, tuple[str, str, int, int]] = {
    "GPT-4 (Mar 2023)": ("left", "bottom", 8, 2),
    "o3": ("right", "bottom", -4, -1),
    "DeepSeek-V3": ("right", "bottom", 4, 4),
    "Claude Fable 5.1": ("left", "top", 8, -4),
    "GPT-6 Astra": ("right", "middle", -8, 0),
    "Llama 2-70B": ("right", "middle", -8, 0),
    "Yi-34B": ("left", "top", 8, -4),
    "Mixtral 8x22B": ("left", "top", 8, -4),
    "Llama 3.1-405B": ("left", "top", 4, -4),
    "Qwen3-235B-A22B": ("left", "top", 8, -4),
    "Qwen3-32B": ("left", "top", 8, -4),
    "Gemma 4 31B": ("left", "middle", 28, 0),
    "Gemma 4 26B A4B": ("left", "middle", 28, -10),
    "Qwen3.6-27B": ("left", "top", 8, -4),
    "Qwen3.8-27B": ("left", "middle", 8, 0),
}


@dataclass(frozen=True)
class Model:
    """The ECI of one model.

    :param name: name of the model
    :param release_date: release date of the model
    :param eci: Epoch Capabilities Index
    :param ci_low: lower limit of the 90 % confidence interval of the ECI.
        ``None`` for the two models that anchor the scale (Claude 3.5 Sonnet at 130 and GPT-5 at 150).
    :param ci_high: upper limit of the 90 % confidence interval of the ECI, or ``None``
    :param open_weights: whether the weights of the model can be downloaded
    :param parameters: the number of parameters of the model, if known
    """

    name: str
    release_date: datetime.date
    eci: float
    ci_low: float | None
    ci_high: float | None
    open_weights: bool
    parameters: Parameters | None = None


def load_models(path: Path) -> list[Model]:
    """Load the models from Epoch AI's ``eci_scores.csv``.

    As in Epoch AI's chart, a model counts as closed unless it has open weights,
    i.e. also when its accessibility is unknown ("Other").

    :param path: path to the CSV file
    :return: the models
    """
    with path.open(encoding="utf-8", newline="") as file:
        return [
            Model(
                name=row["Model"],
                release_date=datetime.date.fromisoformat(row["date"]),
                eci=float(row["eci"]),
                ci_low=float(row["eci_ci_low"]) if row["eci_ci_low"] else None,
                ci_high=float(row["eci_ci_high"]) if row["eci_ci_high"] else None,
                open_weights=row["Accessibility group"] == "Open weights",
                parameters=PARAMETERS.get(row["Model"]),
            )
            for row in csv.DictReader(file)
        ]


def fits_consumer_gpu(model: Model, max_params: float = MAX_CONSUMER_PARAMS) -> bool:
    """Check whether a model can be run on a consumer GPU.

    :param model: the model
    :param max_params: the largest total number of parameters (billions)
    :return: whether the model has open weights and at most ``max_params`` parameters
    """
    return model.open_weights and model.parameters is not None and model.parameters.total <= max_params


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


def hover_details(model: Model) -> str:
    """Format the confidence interval and the parameters of a model for its hover label.

    :param model: the model
    :return: the details as HTML, starting after the ECI
    """
    if model.ci_low is None or model.ci_high is None:
        details = " (anchor of the scale)"
    else:
        details = f" (90 % CI: {model.ci_low:.1f} \u2013 {model.ci_high:.1f})"
    if model.parameters is not None:
        details += f"<br>Parameters: {model.parameters}"
    return details


def step_trace(
    models: list[Model], name: str, color: str, symbol: str, lines: bool = True, show_legend: bool = True
) -> go.Scatter:
    """Create a trace of a frontier as a step line: each level holds until a better model is released.

    :param models: the frontier models, sorted by release date
    :param name: name of the trace in the legend.
        Traces with the same name are shown and hidden together by clicking the legend.
    :param color: color of the line and the markers, except the markers of :data:`HIGHLIGHTED_MODELS`
    :param symbol: Plotly marker symbol, so that the curves can be told apart without color
    :param lines: whether to connect the markers with a step line. Without it, the models are shown as points.
    :param show_legend: whether to show the trace in the legend
    :return: the trace
    """
    return go.Scatter(
        x=[model.release_date for model in models],
        y=[model.eci for model in models],
        mode="lines+markers" if lines else "markers",
        legendgroup=name,
        showlegend=show_legend,
        line={"color": color, "width": 3, "shape": "hv"},
        marker={
            "color": [COLOR_HIGHLIGHT if model.name in HIGHLIGHTED_MODELS else color for model in models],
            "size": 11,
            "symbol": symbol,
            "line": {"color": "white", "width": 2},
        },
        name=name,
        customdata=[[model.name, hover_details(model)] for model in models],
        hovertemplate="<b>%{customdata[0]}</b><br>"
        "Released %{x|%-d %b %Y}<br>"
        "ECI: %{y:.1f}%{customdata[1]}"
        "<extra></extra>",
    )


def add_labels(fig: go.Figure, models: list[Model], labels: dict[str, str], color: str) -> None:
    """Label the models of a curve next to their markers.

    :param fig: the figure
    :param models: the models of the curve
    :param labels: the models to label and their labels
    :param color: color of the labels, except those of :data:`HIGHLIGHTED_MODELS`
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
            font={"size": FONT_SIZE - 3, "color": COLOR_HIGHLIGHT if model.name in HIGHLIGHTED_MODELS else color},
            bgcolor="white" if label in LABELS_ON_REFERENCE_LINES else None,
        )


def make_figure(
    closed: list[Model], open_: list[Model], consumer: list[Model], consumer_extra: list[Model]
) -> go.Figure:
    """Create the figure.

    :param closed: the frontier of the closed-weights models
    :param open_: the frontier of the open-weights models
    :param consumer: the frontier of the open-weights models that fit on a consumer GPU
    :param consumer_extra: other open-weights models that fit on a consumer GPU, shown as points
    :return: the figure
    """
    consumer_name = "Open weights, fits on a 32 GB GPU<br>(or smaller with CPU offload)"
    fig = go.Figure()
    fig.add_trace(step_trace(closed, "Closed weights", COLOR_CLOSED, "circle"))
    fig.add_trace(step_trace(open_, "Open weights", COLOR_OPEN, "square"))
    fig.add_trace(step_trace(consumer, consumer_name, COLOR_CONSUMER, "diamond"))
    fig.add_trace(step_trace(consumer_extra, consumer_name, COLOR_CONSUMER, "diamond", lines=False, show_legend=False))
    for model in consumer + consumer_extra:
        if model.name in REFERENCE_LINE_MODELS:
            fig.add_shape(
                type="line",
                x0=X_MIN,
                x1=model.release_date,
                y0=model.eci,
                y1=model.eci,
                line={"color": COLOR_HIGHLIGHT, "width": 1.5, "dash": "dot"},
                layer="below",
            )
    add_labels(fig, closed, CLOSED_LABELS, COLOR_CLOSED)
    add_labels(fig, open_, OPEN_LABELS, COLOR_OPEN)
    add_labels(fig, consumer + consumer_extra, CONSUMER_LABELS, COLOR_CONSUMER)

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
        range=[104, 172],
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
        text=f"Data: Epoch AI's ECI data (CC BY 4.0, epoch.ai/benchmarks), {DATA_DATE}. "
        "After Epoch AI's chart at epoch.ai/data-insights/open-closed-eci-gap.<br>"
        f"32 GB GPU: models with \u2264 {MAX_CONSUMER_PARAMS} B parameters (4-bit quantized), "
        "parameter counts from the model cards.",
        font={"size": FONT_SIZE - 5, "color": "#666666"},
    )
    return fig


def main() -> None:
    """Create the figure and save it as an HTML file."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=OUTPUT, help="the HTML file to write")
    args = parser.parse_args()

    models = load_models(ECI_DATA)
    closed = frontier([model for model in models if not model.open_weights])
    open_ = frontier([model for model in models if model.open_weights])
    consumer_models = [model for model in models if fits_consumer_gpu(model)]
    consumer = frontier(consumer_models)
    consumer_extra = [
        model for model in consumer_models if model.name in CONSUMER_EXTRA_MODELS and model not in consumer
    ]
    groups = {"Closed": closed, "Open": open_, "32 GB GPU": consumer, "32 GB GPU, not on the curve": consumer_extra}
    for name, group in groups.items():
        print(f"{name}: " + ", ".join(f"{model.name} ({model.eci:.1f})" for model in group))

    fig = make_figure(closed, open_, consumer, consumer_extra)
    write_html(fig, args.output, div_id="epoch-open-closed-gap")
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
