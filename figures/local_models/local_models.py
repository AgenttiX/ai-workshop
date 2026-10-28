"""Flow chart of an agent harness with a local model, as a self-contained 1600x800 SVG.

The white background lets it sit on any slide theme. The style follows Antti's research flow charts
(``research-physics.svg``, ``research-math.svg``): the same palette, cards and arrows.
A PNG preview is rendered with Inkscape when it is installed.

Run with ``python -m figures.local_models.local_models`` in the root directory of the repository.
"""

from pathlib import Path
import shutil
import subprocess
from xml.sax.saxutils import escape

DIR = Path(__file__).resolve().parent
OUTPUT = DIR / "local_models.svg"
W, H = 1600, 800
FONT = "Inter, 'Source Sans Pro', 'Source Sans 3', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'DejaVu Sans Mono', monospace"

INK = "#1f2933"
MUTED = "#52606d"
LINE = "#52606d"
#: Fill and stroke of each kind of box
PALETTE = {
    "you": ("#fdf3ea", "#e0a36f"),
    "harness": ("#eef4fb", "#7b9cc4"),
    "check": ("#f3eefb", "#9b85c9"),
    "yours": ("#f1f7ee", "#8fb67f"),
    "machine": ("#f4f5f7", "#9aa5b1"),
}


class Svg:
    """An SVG drawing built from text, boxes, cards and arrows."""

    def __init__(self, title: str):
        """:param title: the title of the drawing, read by screen readers"""
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'font-family="{FONT}">',
            f"<title>{escape(title)}</title>",
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            'orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 Z" fill="{LINE}"/></marker></defs>',
            f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        ]

    def add(self, s: str) -> None:
        """Add raw SVG markup."""
        self.parts.append(s)

    def text(self, x: float, y: float, s: str, size: int = 20, weight: int = 400, color: str = INK,
             anchor: str = "start", mono: bool = False, italic: bool = False) -> None:
        """Add one line of text with its baseline at ``y``."""
        fam = f' font-family="{MONO}"' if mono else ""
        sty = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x:g}" y="{y:g}" font-size="{size}" font-weight="{weight}" fill="{color}" '
                 f'text-anchor="{anchor}" xml:space="preserve"{fam}{sty}>{escape(s)}</text>')

    def box(self, x: float, y: float, w: float, h: float, kind: str, dash: bool = False, rx: int = 16) -> None:
        """Add a rounded rectangle in the colors of ``kind``."""
        fill, stroke = PALETTE[kind]
        d = ' stroke-dasharray="8 6"' if dash else ""
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="2"{d}/>')

    def card(self, x: float, y: float, w: float, h: float, kind: str, title: str, lines: list[str],
             size: int = 18, title_size: int = 21, icon: str | None = None, dash: bool = False) -> None:
        """Add a box with a bold title and body lines; a line starting with a backtick is set in monospace."""
        self.box(x, y, w, h, kind, dash=dash)
        tx = x + 18
        if icon == "you":
            self.person(x + 34, y + 30)
            tx = x + 62
        self.text(tx, y + 34, title, title_size, 700)
        yy = y + 34 + title_size * 0.5 + size * 1.25
        for line in lines:
            mono = line.startswith("`")
            self.text(x + 18, yy, line.strip("`"), size - 1 if mono else size, color=INK if mono else MUTED, mono=mono)
            yy += size * 1.35

    def person(self, cx: float, cy: float) -> None:
        """Add a person icon centered at (cx, cy)."""
        stroke = PALETTE["you"][1]
        self.add(f'<circle cx="{cx:g}" cy="{cy - 7:g}" r="7" fill="{stroke}"/>'
                 f'<path d="M{cx - 13:g},{cy + 15:g} a13,11 0 0 1 26,0 z" fill="{stroke}"/>')

    def arrow(self, pts: list[tuple[float, float]], label: str = "", lx: float | None = None,
              ly: float | None = None, anchor: str = "middle") -> None:
        """Add a polyline arrow through ``pts``, optionally labeled at (lx, ly) or above its first segment."""
        d = " ".join(f"{'M' if i == 0 else 'L'}{x:g},{y:g}" for i, (x, y) in enumerate(pts))
        self.add(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="2.4" marker-end="url(#arrow)"/>')
        if label:
            if lx is None or ly is None:
                (x0, y0), (x1, y1) = pts[0], pts[1]
                lx, ly = (x0 + x1) / 2, (y0 + y1) / 2 - 10
            self.text(lx, ly, label, 17, color=MUTED, anchor=anchor, italic=True)

    def save(self, path: Path) -> None:
        """Write the drawing to ``path``."""
        path.write_text("\n".join([*self.parts, "</svg>"]) + "\n", encoding="utf-8")


def local_models() -> Svg:
    """Draw the chain from the harness through the model server to the weights, and the tool loop."""
    s = Svg("An agent harness with a local model: the harness sends the conversation over HTTP to a model server "
            "on the same computer, "
            "where a chat template turns it into one string, the inference engine computes the next tokens "
            "from the weights, and the reply comes back as text or a tool call that the harness runs")

    s.box(30, 30, 1540, 560, "machine", dash=True)
    s.text(52, 66, "Your computer", 24, 700)

    s.card(60, 100, 230, 110, "you", "You", ["Type a task"], icon="you")
    s.arrow([(290, 155), (360, 155)])

    s.card(360, 90, 440, 200, "harness", "Harness (e.g. OpenCode)", [
        "Sends the whole conversation, every turn:",
        "instructions, tool list, your messages,",
        "earlier tool results",
    ])
    s.card(360, 380, 440, 180, "harness", "Runs the tools on your files", [
        "`Bash  Read  Edit  Write  …",
        "The model only writes text;",
        "the harness does the acting,",
        "with your permission",
    ])
    s.arrow([(540, 290), (540, 380)], "tool call", 528, 342, anchor="end")
    s.arrow([(620, 380), (620, 290)], "result", 632, 342, anchor="start")

    s.box(940, 60, 610, 510, "check")
    s.text(962, 96, "Model server: LM Studio / llama-server / vLLM", 22, 700)
    s.text(962, 124, "Port 1234 (LM Studio), 9931 (llama-server) or 8000 (vLLM)", 18, color=MUTED)
    s.arrow([(800, 165), (940, 165)], "request", 870, 153)
    s.arrow([(940, 240), (800, 240)], "reply:", 870, 268)
    s.text(870, 290, "text or tool call", 17, color=MUTED, anchor="middle", italic=True)

    s.card(965, 140, 560, 110, "yours", "Chat template", [
        "Messages → one string with markers:",
        "`<|im_start|>user …<|im_end|>",
    ])
    s.arrow([(1245, 250), (1245, 275)])
    s.card(965, 275, 560, 140, "yours", "Inference engine: llama.cpp / vLLM", [
        "Prefill: reads the whole prompt at once",
        "Decode: writes one token at a time,",
        "each one reads all the weights again",
    ])
    s.arrow([(1245, 415), (1245, 440)])
    s.card(965, 440, 560, 110, "yours", "Weights + KV cache, in RAM", [
        "`gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf  14.2 GB",
        "KV cache: the context, 20 KiB per token",
    ])

    s.card(30, 620, 760, 150, "machine", "Optional: LiteLLM, a translator+proxy", [
        "Converts between API formats, e.g. Anthropic vs. OpenAI,",
        "and combines multiple model servers to one API endpoint",
    ], dash=True)
    s.card(810, 620, 760, 150, "you", "In the cloud: the same chain, far away", [
        "A harness works the same way with cloud and local models,",
        "and can be pointed to either:",
        "`ANTHROPIC_BASE_URL=http://localhost:1234",
    ])
    return s


def main() -> None:
    """Save the SVG and, if Inkscape is installed, a PNG preview next to it."""
    local_models().save(OUTPUT)
    if shutil.which("inkscape"):
        subprocess.run(["timeout", "-s", "KILL", "120", "inkscape", str(OUTPUT), "--export-type=png",
                        f"--export-filename={OUTPUT.with_suffix('.png')}", "--export-width=1600"],
                       check=True, capture_output=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
