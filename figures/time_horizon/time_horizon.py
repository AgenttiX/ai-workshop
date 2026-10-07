"""Plot the 50 % time horizons of AI models against their release dates.

This is our own version of the chart at https://metr.org/time-horizons/.
It combines METR's Time Horizon 1.1 data (``benchmark_results_1_1.yaml``)
with newer measurements that are not yet in it (``additional_results.yaml``).

The result is an interactive HTML page: hover over a point to see its values, drag to zoom, double-click to reset.

Run with ``python -m figures.time_horizon.time_horizon`` in the root directory of the repository.
The requirements are in ``figures/requirements.txt``.
"""

import argparse
from dataclasses import dataclass
import datetime
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import yaml

from figures.common import COLOR_GRID, COLOR_TEXT, FONT, FONT_SIZE, write_html

DATA_DIR = Path(__file__).resolve().parent
METR_DATA = DATA_DIR / "benchmark_results_1_1.yaml"
ADDITIONAL_DATA = DATA_DIR / "additional_results.yaml"
OUTPUT = DATA_DIR / "time_horizon.html"

#: METR considers horizons above this unreliable with its current task suite (minutes)
RELIABLE_LIMIT = 16 * 60
#: The trend is fitted to the state-of-the-art models released from this date on, as in METR's "from_2023_on" fit
TREND_START = datetime.date(2023, 1, 1)
#: The trend line is drawn until this date
TREND_END = datetime.date(2026, 12, 31)
#: The plotted range of the x-axis
X_MIN = datetime.date(2018, 12, 1)
X_MAX = datetime.date(2027, 4, 1)

COLOR_SOTA = "#2e7d32"
COLOR_OTHER = "#a5d6a7"
COLOR_NOT_ROBUST = "#888888"

#: Display names of the models in METR's data file, shown when hovering over a point.
#: The models of additional_results.yaml have their names in the file.
NAMES: dict[str, str] = {
    "gpt2": "GPT-2",
    "davinci_002": "GPT-3 (davinci-002)",
    "gpt_3_5_turbo_instruct": "GPT-3.5 Turbo Instruct",
    "gpt_4": "GPT-4",
    "gpt_4_1106_inspect": "GPT-4 (Nov 2023)",
    "claude_3_opus_inspect": "Claude 3 Opus",
    "gpt_4_turbo_inspect": "GPT-4 Turbo",
    "gpt_4o_inspect": "GPT-4o",
    "claude_3_5_sonnet_20240620_inspect": "Claude 3.5 Sonnet (Jun 2024)",
    "o1_preview": "o1-preview",
    "claude_3_5_sonnet_20241022_inspect": "Claude 3.5 Sonnet (Oct 2024)",
    "o1_inspect": "o1",
    "claude_3_7_sonnet_inspect": "Claude 3.7 Sonnet",
    "o3_inspect": "o3",
    "claude_4_opus_inspect": "Claude Opus 4",
    "claude_4_1_opus_inspect": "Claude Opus 4.1",
    "gpt_5_2025_08_07_inspect": "GPT-5",
    "gemini_3_pro": "Gemini 3 Pro",
    "gpt_5_1_codex_max_inspect": "GPT-5.1-Codex-Max",
    "claude_opus_4_5_inspect": "Claude Opus 4.5",
    "gpt_5_2": "GPT-5.2",
    "claude_opus_4_6_inspect": "Claude Opus 4.6",
    "gpt_5_3_codex": "GPT-5.3-Codex",
    "gemini_3_1_pro": "Gemini 3.1 Pro",
    "gpt_5_4": "GPT-5.4",
    "claude_mythos_preview_early_inspect": "Claude Mythos Preview (early)",
}

#: Labels of the models to label in the plot. The other models are shown without a label.
LABELS: dict[str, str] = {
    "gpt2": "GPT-2",
    "davinci_002": "GPT-3",
    "gpt_3_5_turbo_instruct": "GPT-3.5",
    "gpt_4": "GPT-4",
    "gpt_4o_inspect": "GPT-4o",
    "claude_3_7_sonnet_inspect": "Claude 3.7 Sonnet",
    "o3_inspect": "o3",
    "claude_opus_4_6_inspect": "Claude Opus 4.6",
    "claude_mythos_preview_early_inspect": "Claude Mythos<br>Preview",
    "gpt_5_6_sol": "GPT-5.6 Sol",
}

#: Label positions that differ from the default (left of the marker): (xanchor, xshift, yshift) in pixels
LABEL_POSITIONS: dict[str, tuple[str, int, int]] = {
    "davinci_002": ("left", 10, -10),
    "claude_mythos_preview_early_inspect": ("left", 10, 18),
    "gpt_5_6_sol": ("left", 12, -10),
}

#: Example tasks and how long they take a human expert (minutes), shown along the y-axis as in METR's chart.
#: From the 50 % chart of https://metr.org/assets/js/time-horizon-chart.js
EXAMPLE_TASKS: dict[float, str] = {
    12 * 60: "Optimally reduce the size of a language model",
    4 * 60: "Train adversarially robust image model",
    0.82 * 60: "Train classifier",
    0.17 * 60: "Find fact on web",
    0.03 * 60: "Count words in passage",
    0.00417 * 60: "Answer question",
}

#: Tick positions of the y-axis (minutes) and their labels
Y_TICKS: dict[float, str] = {
    1 / 60: "1 s",
    15 / 60: "15 s",
    1: "1 min",
    4: "4 min",
    15: "15 min",
    60: "1 h",
    4 * 60: "4 h",
    16 * 60: "16 h",
    64 * 60: "64 h",
}
#: The plotted range of the y-axis (minutes)
Y_MIN = 1 / 60 / 2
Y_MAX = 64 * 60 * 1.5


@dataclass(frozen=True)
class Result:
    """The 50 % time horizon of one model.

    :param key: identifier of the model in the data file
    :param name: display name
    :param label: label in the plot, or an empty string for no label
    :param release_date: release date of the model
    :param estimate: point estimate of the 50 % time horizon (minutes)
    :param ci_low: lower limit of the 95 % confidence interval (minutes)
    :param ci_high: upper limit of the 95 % confidence interval (minutes)
    :param is_sota: whether the model was the state of the art when released
    :param robust: whether METR considers the measurement robust
    """

    key: str
    name: str
    label: str
    release_date: datetime.date
    estimate: float
    ci_low: float
    ci_high: float
    is_sota: bool = True
    robust: bool = True


def load_results(path: Path) -> list[Result]:
    """Load the results from a YAML file in the format of METR's ``benchmark_results_1_1.yaml``.

    :param path: path to the YAML file
    :return: the results, sorted by release date
    """
    with path.open(encoding="utf-8") as file:
        data = yaml.safe_load(file)
    results = []
    for key, entry in data["results"].items():
        horizon = entry["metrics"]["p50_horizon_length"]
        results.append(
            Result(
                key=key,
                name=entry.get("name", NAMES.get(key, key)),
                label=LABELS.get(key, ""),
                release_date=entry["release_date"],
                estimate=horizon["estimate"],
                ci_low=horizon["ci_low"],
                ci_high=horizon["ci_high"],
                is_sota=entry["metrics"].get("is_sota", True),
                robust=entry.get("robust", True),
            )
        )
    return sorted(results, key=lambda result: result.release_date)


def fit_doubling_time(results: list[Result]) -> tuple[float, float]:
    """Fit an exponential trend to the reliable state-of-the-art results since :data:`TREND_START`.

    This reproduces the "from_2023_on" doubling time of METR's data file.

    :param results: all the results
    :return: the doubling time (days) and the base-2 logarithm of the horizon (minutes) at day 0 (``date.toordinal()``)
    """
    selected = [
        result
        for result in results
        if result.is_sota and result.robust and result.release_date >= TREND_START and result.estimate <= RELIABLE_LIMIT
    ]
    days = np.array([result.release_date.toordinal() for result in selected], dtype=float)
    log2_horizon = np.log2([result.estimate for result in selected])
    slope, intercept = np.polyfit(days, log2_horizon, 1)
    return 1 / slope, intercept


def format_duration(minutes: float) -> str:
    """Format a duration for humans, e.g. "36 s", "4.2 min" or "11.3 h".

    :param minutes: the duration (minutes)
    :return: the formatted duration
    """
    if minutes < 1:
        return f"{minutes * 60:.0f} s"
    if minutes < 60:  # noqa: PLR2004
        return f"{minutes:.1f} min"
    return f"{minutes / 60:.1f} h"


def scatter(results: list[Result], name: str, color: str, symbol: str = "circle") -> go.Scatter:
    """Create a scatter trace with the 95 % confidence intervals as error bars.

    :param results: the results to plot
    :param name: name of the trace in the legend
    :param color: color of the markers
    :param symbol: Plotly marker symbol
    :return: the trace
    """
    return go.Scatter(
        x=[result.release_date for result in results],
        y=[result.estimate for result in results],
        error_y={
            "type": "data",
            "symmetric": False,
            "array": [result.ci_high - result.estimate for result in results],
            "arrayminus": [result.estimate - result.ci_low for result in results],
            "color": color,
            "thickness": 1.5,
            "width": 0,
        },
        mode="markers",
        marker={"color": color, "size": 12, "symbol": symbol, "line": {"color": "white", "width": 1}},
        name=name,
        customdata=[
            [result.name, *(format_duration(value) for value in (result.estimate, result.ci_low, result.ci_high))]
            for result in results
        ],
        hovertemplate="<b>%{customdata[0]}</b><br>"
        "Released %{x|%-d %b %Y}<br>"
        "50 % time horizon: %{customdata[1]}<br>"
        "95 % CI: %{customdata[2]} \u2013 %{customdata[3]}"
        "<extra></extra>",
    )


def make_figure(results: list[Result], doubling_time: float, intercept: float, show_legend: bool = True) -> go.Figure:
    """Create the figure.

    :param results: all the results
    :param doubling_time: doubling time of the trend (days)
    :param intercept: base-2 logarithm of the trend at day 0 (minutes)
    :param show_legend: whether to show the legend.
        Without it, the trend line is labeled directly, and the gray color marks the non-robust results.
    :return: the figure
    """
    fig = go.Figure()

    # Example tasks along the y-axis, with short ticks
    for minutes, task in EXAMPLE_TASKS.items():
        fig.add_shape(
            type="line", xref="paper", x0=0, x1=0.008, y0=minutes, y1=minutes, line={"color": "#999999", "width": 1}
        )
        fig.add_annotation(
            xref="paper",
            x=0.01,
            y=np.log10(minutes),
            xanchor="left",
            text=task,
            showarrow=False,
            font={"size": FONT_SIZE - 4, "color": "#777777"},
        )

    # The region that the task suite cannot measure reliably.
    # Note that annotations on a logarithmic axis are positioned with the base-10 logarithm, but shapes are not.
    fig.add_hrect(y0=RELIABLE_LIMIT, y1=Y_MAX, fillcolor="#bbbbbb", opacity=0.25, line_width=0, layer="below")
    fig.add_annotation(
        x=datetime.date(2021, 1, 1),
        y=np.log10(RELIABLE_LIMIT * 2.5),
        text="<i>Above 16 h: beyond what the task suite can measure reliably</i>",
        showarrow=False,
        font={"size": FONT_SIZE - 4, "color": "#666666"},
    )

    # Trend line
    trend_name = f"Fit to 2023\u20132026: doubling every {doubling_time:.0f} days"
    trend_days = np.array([TREND_START.toordinal(), TREND_END.toordinal()], dtype=float)
    fig.add_trace(
        go.Scatter(
            x=[datetime.date.fromordinal(int(day)) for day in trend_days],
            y=2 ** (intercept + trend_days / doubling_time),
            mode="lines",
            line={"color": COLOR_SOTA, "dash": "dash", "width": 2},
            name=trend_name,
            hoverinfo="skip",
        )
    )
    if not show_legend:
        # Label the trend line itself, below the line
        label_date = datetime.date(2024, 7, 1)
        fig.add_annotation(
            x=label_date,
            y=np.log10(2 ** (intercept + label_date.toordinal() / doubling_time)),
            text=trend_name.replace(": ", ":<br>"),
            showarrow=False,
            xanchor="left",
            yanchor="top",
            xshift=10,
            yshift=-10,
            font={"size": FONT_SIZE - 4, "color": COLOR_SOTA},
        )

    fig.add_trace(scatter([r for r in results if r.robust and r.is_sota], "State of the art at release", COLOR_SOTA))
    fig.add_trace(scatter([r for r in results if r.robust and not r.is_sota], "Other models", COLOR_OTHER))
    fig.add_trace(
        scatter(
            [r for r in results if not r.robust],
            "Not a robust measurement (METR)",
            COLOR_NOT_ROBUST,
            symbol="diamond",
        )
    )

    for result in results:
        if not result.label:
            continue
        xanchor, xshift, yshift = LABEL_POSITIONS.get(result.key, ("right", -12, 10))
        fig.add_annotation(
            x=result.release_date,
            y=np.log10(result.estimate),
            text=result.label,
            showarrow=False,
            xanchor=xanchor,
            xshift=xshift,
            yshift=yshift,
            font={"size": FONT_SIZE - 4, "color": COLOR_NOT_ROBUST if not result.robust else COLOR_TEXT},
            bgcolor="rgba(255, 255, 255, 0.7)",
        )

    fig.update_layout(
        autosize=True,
        margin={"l": 90, "r": 20, "t": 15, "b": 105},
        font={"family": f"{FONT}, sans-serif", "size": FONT_SIZE, "color": COLOR_TEXT},
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=show_legend,
        # In the lower right corner, which has no data
        legend={"x": 0.99, "y": 0.03, "xanchor": "right", "yanchor": "bottom", "bgcolor": "rgba(255, 255, 255, 0.8)",
                "font": {"size": FONT_SIZE - 2}},
        hoverlabel={"font": {"family": f"{FONT}, sans-serif", "size": FONT_SIZE - 2}},
    )
    fig.update_xaxes(
        title="LLM release date",
        range=[X_MIN, X_MAX],
        dtick="M12",
        tickformat="%Y",
        showgrid=True,
        gridcolor=COLOR_GRID,
        linecolor=COLOR_TEXT,
        ticks="outside",
    )
    fig.update_yaxes(
        title="Task length for a human expert<br>(AI succeeds 50 % of the time)",
        type="log",
        range=[np.log10(Y_MIN), np.log10(Y_MAX)],
        tickvals=list(Y_TICKS),
        ticktext=list(Y_TICKS.values()),
        showgrid=True,
        gridcolor=COLOR_GRID,
        linecolor=COLOR_TEXT,
        ticks="outside",
    )
    fig.add_annotation(
        x=0,
        y=-0.25,
        xref="paper",
        yref="paper",
        xanchor="left",
        showarrow=False,
        text="Data: METR, Time Horizon 1.1 (metr.org/time-horizons, May 2026); "
        "GPT-5.6 Sol: METR, 26 June 2026. Error bars: 95 % confidence intervals.",
        font={"size": FONT_SIZE - 5, "color": "#666666"},
    )
    return fig



def main() -> None:
    """Create the figure and save it as an HTML file."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=OUTPUT, help="the HTML file to write")
    parser.add_argument("--hide-legend", action="store_true", help="hide the legend and label the lines instead")
    args = parser.parse_args()

    results = load_results(METR_DATA) + load_results(ADDITIONAL_DATA)
    doubling_time, intercept = fit_doubling_time(results)
    print(f"Doubling time since {TREND_START}: {doubling_time:.1f} days")

    results.sort(key=lambda result: result.release_date)
    fig = make_figure(results, doubling_time, intercept, show_legend=not args.hide_legend)
    write_html(fig, args.output, div_id="time-horizon")
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
