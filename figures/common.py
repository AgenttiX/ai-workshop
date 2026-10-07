"""Code shared by the plotting scripts of the figures: the style of the slides and saving the figures as HTML."""

from pathlib import Path

import plotly.graph_objects as go

#: The font of the reveal.js "sky" theme of the slides
FONT = "Open Sans"
#: Font size (pixels) in the iframe of the slides
FONT_SIZE = 18

COLOR_TEXT = "#333333"
COLOR_GRID = "#e5e5e5"


def write_html(fig: go.Figure, path: Path, div_id: str) -> None:
    """Save the figure as an HTML page that fills its window, e.g. an iframe in the slides.

    :param fig: the figure
    :param path: the HTML file to write
    :param div_id: ID of the HTML element of the figure
    """
    page = fig.to_html(
        include_plotlyjs="cdn",
        full_html=True,
        # A fixed ID instead of a random one, so that regenerating the figure does not change the file needlessly
        div_id=div_id,
        default_width="100%",
        default_height="100%",
        # Zooming by dragging and resetting by double-clicking work without the toolbar.
        config={"responsive": True, "displayModeBar": False},
    )
    # The font of the slides, and no margins or scroll bars around the figure
    head = (
        f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={FONT.replace(" ", "+")}'
        ':ital,wght@0,400;0,700;1,400&display=swap">\n'
        "<style>html, body { height: 100%; margin: 0; overflow: hidden; }</style>\n"
    )
    # Plotly measures the text when drawing it, so the figure is redrawn once the font has loaded.
    # (In the slides, the iframe must also be loaded only when it's visible, which is why it uses data-src.)
    redraw = (
        f"<script>document.fonts.ready.then(() => {{ const plot = document.getElementById('{div_id}'); "
        "Plotly.newPlot(plot, plot.data, plot.layout, plot._context); });</script>\n"
    )
    page = page.replace("<head>", "<head>\n" + head, 1).replace("</body>", redraw + "</body>", 1)
    path.write_text(page, encoding="utf-8")
