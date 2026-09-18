#!/usr/bin/env python3
"""Render a reveal.js presentation into a PDF.

The whole presentation is exported in one go with the print view of reveal.js (?print-pdf)
and the PDF printer of headless Chromium/Chrome, so the deck is loaded only once and the
text of the slides stays as selectable and searchable text instead of being rasterised.

The browser is driven over the Chrome DevTools Protocol, which makes it possible to wait
for the "pdf-ready" event of reveal.js, i.e. until MathJax, the fonts and the images are
done, before printing. Printing without waiting for that event tends to produce PDFs with
missing or even completely blank slides.

Usage: ./render.py [options] <presentation.html|URL>
Run "./render.py --help" for the available options.

Requirements: Chromium or Chrome, Python 3 (no third-party packages),
              and poppler-utils (pdftoppm) for --png.
"""

import argparse
import base64
import glob
import json
import os
import secrets
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

BROWSER_CANDIDATES = ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome")
NOTE_MODES = ("inline", "separate-page")


class RenderError(Exception):
    """An error that is reported to the user without a Python stack trace."""


def log(message):
    print(message, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------- the browser


class WebSocket:
    """A minimal WebSocket client for talking to the browser."""

    def __init__(self, url, timeout):
        host_port, _, path = url.removeprefix("ws://").partition("/")
        host, _, port = host_port.partition(":")
        self.sock = socket.create_connection((host, int(port or 80)), timeout=timeout)
        self.sock.settimeout(timeout)
        key = base64.b64encode(secrets.token_bytes(16)).decode()
        self.sock.sendall(
            f"GET /{path} HTTP/1.1\r\nHost: {host_port}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n".encode()
        )
        self.buffer = b""
        while b"\r\n\r\n" not in self.buffer:
            self.buffer += self._recv()
        head, _, self.buffer = self.buffer.partition(b"\r\n\r\n")
        if b" 101 " not in head.split(b"\r\n")[0]:
            raise ConnectionError(f"the browser rejected the DevTools connection: {head[:80]!r}")

    def _recv(self):
        chunk = self.sock.recv(1 << 16)
        if not chunk:
            raise ConnectionError("the browser closed the DevTools connection")
        return chunk

    def _read(self, count):
        while len(self.buffer) < count:
            self.buffer += self._recv()
        data, self.buffer = self.buffer[:count], self.buffer[count:]
        return data

    def send(self, text):
        data = text.encode()
        mask = secrets.token_bytes(4)
        header = b"\x81"
        if len(data) < 126:
            header += bytes([0x80 | len(data)])
        elif len(data) < 1 << 16:
            header += b"\xfe" + struct.pack(">H", len(data))
        else:
            header += b"\xff" + struct.pack(">Q", len(data))
        self.sock.sendall(header + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def receive(self):
        """Returns the next text message, reassembling fragmented frames."""
        payload = b""
        while True:
            first, second = self._read(2)
            final, opcode, length = first & 0x80, first & 0x0F, second & 0x7F
            if length == 126:
                length = struct.unpack(">H", self._read(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self._read(8))[0]
            data = self._read(length)
            if opcode == 0x8:
                raise ConnectionError("the browser closed the DevTools connection")
            if opcode in (0x9, 0xA):  # Ping and pong
                continue
            payload += data
            if final:
                return payload.decode("utf-8", "replace")

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


class Browser:
    """A headless browser controlled over the Chrome DevTools Protocol."""

    def __init__(self, binary, profile, timeout):
        arguments = [
            binary, "--headless", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
            "--no-first-run", "--no-default-browser-check", "--disable-extensions",
            "--disable-sync", "--disable-background-networking", "--disable-component-update",
            "--force-color-profile=srgb", "--force-device-scale-factor=1",
            "--window-size=1920,1080", f"--user-data-dir={profile}",
            # Port 0 makes the browser pick a free port and write it into the profile.
            "--remote-debugging-port=0", "about:blank",
        ]
        # Chromium refuses to run as root without disabling its sandbox.
        if os.geteuid() == 0:
            arguments.insert(1, "--no-sandbox")
        self.process = subprocess.Popen(arguments, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.connection = None
        self.message_id = 0
        # A browser that has been started but cannot be connected to has to be killed here,
        # because there is nothing left to close it with.
        try:
            port = self._wait_for_port(profile, timeout)
            targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=timeout))
            pages = [target for target in targets if target["type"] == "page"]
            if not pages:
                raise RenderError("the browser did not open a page to render into")
            # The presentation and its resources may take a while to load, and printing a
            # large deck takes a moment as well, so the connection gets a generous timeout.
            self.connection = WebSocket(pages[0]["webSocketDebuggerUrl"], timeout=timeout + 120)
        except BaseException:
            self.process.kill()
            raise

    def _wait_for_port(self, profile, timeout):
        path = Path(profile, "DevToolsActivePort")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                raise RenderError(f"the browser exited with the status {self.process.returncode}")
            # The file is complete once it has both the port and the WebSocket path.
            if path.exists():
                lines = path.read_text().split("\n")
                if len(lines) >= 2 and lines[0].isdigit():
                    return lines[0]
            time.sleep(0.05)
        raise RenderError("the browser did not start up")

    def call(self, method, **params):
        self.message_id += 1
        self.connection.send(json.dumps({"id": self.message_id, "method": method, "params": params}))
        while True:
            message = json.loads(self.connection.receive())
            if message.get("id") == self.message_id:
                if "error" in message:
                    raise RenderError(f"{method}: {message['error'].get('message')}")
                return message.get("result", {})

    def evaluate(self, expression):
        result = self.call("Runtime.evaluate", expression=expression, returnByValue=True)
        if "exceptionDetails" in result:
            raise RenderError(result["exceptionDetails"].get("text", "JavaScript error"))
        return result["result"].get("value")

    def close(self):
        if self.connection is not None:
            try:
                self.call("Browser.close")
            except (OSError, RenderError):
                pass
            self.connection.close()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()


# ------------------------------------------------------------------------------- scripts

# reveal.js dispatches "pdf-ready" once it has laid the slides out into pages for printing,
# which happens after the plugins, such as MathJax, are done. The listener is installed
# before the presentation is loaded, so that the event cannot be missed.
INIT_SCRIPT = """
window.__renderReady = false;
document.addEventListener('pdf-ready', () => { window.__renderReady = true; });
"""

# The images and the fonts are waited for separately, because reveal.js does not do so.
READY_SCRIPT = """
(() => {
    if (!window.__renderReady) return false;
    if (document.fonts && document.fonts.status !== 'loaded') return false;
    for (const image of document.images) if (!image.complete) return false;
    return true;
})()
"""

# The print view of reveal.js shows every fragment of a slide, unless the fragments are
# printed as separate steps. Hiding them again gives the slides without any fragments.
HIDE_FRAGMENTS_SCRIPT = """
(() => {
    const fragments = document.querySelectorAll('.pdf-page .fragment.visible');
    fragments.forEach(fragment => fragment.classList.remove('visible', 'current-fragment'));
    return fragments.length;
})()
"""

PAGE_COUNT_SCRIPT = "document.querySelectorAll('.pdf-page').length"


# ----------------------------------------------------------------------------- arguments


EPILOG = """\
The rendering time is dominated by loading the presentation and its external resources
such as reveal.js, MathJax and the figures, which is a matter of tens of seconds for the
entire deck, since the presentation is loaded only once.

Notes:
- The slides are printed as vector graphics and text, so the PDF has no resolution and
  the file stays small. Only bitmap figures are embedded as images.
- Background videos are not painted by headless browsers and therefore show up as the
  background colour of the slide.

Examples:
  ./render.py 2026_sewm/sewm.html
  ./render.py --fragments steps --notes 2026_sewm/sewm.html
  ./render.py -o /tmp/sewm.pdf --png https://example.com/sewm.html
"""


def positive_int(minimum):
    """Returns an argparse type for an integer of at least the given value."""

    def parse(text):
        try:
            value = int(text)
        except ValueError:
            raise argparse.ArgumentTypeError(f"invalid number: {text}")
        if value < minimum:
            raise argparse.ArgumentTypeError(f"the value has to be at least {minimum}: {text}")
        return value

    return parse


def config_option(text):
    if "=" not in text:
        raise argparse.ArgumentTypeError(f"invalid config override: {text} (expected KEY=VALUE)")
    return text


def normalize_notes(arguments):
    """Makes the mode of --notes optional, e.g. "--notes deck.html" means "--notes=inline".

    argparse would otherwise swallow the presentation as the mode of the option.
    """
    normalized = []
    for index, argument in enumerate(arguments):
        if argument in ("-n", "--notes"):
            following = arguments[index + 1] if index + 1 < len(arguments) else None
            normalized.append("--notes" if following in NOTE_MODES else "--notes=inline")
        else:
            normalized.append(argument)
    return normalized


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(
        prog="./render.py",
        description="Render a reveal.js presentation into a PDF with headless Chromium/Chrome.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("presentation", metavar="presentation.html|URL",
                        help="the presentation to render, as a local file or a URL")
    parser.add_argument("-o", "--output", metavar="FILE",
                        help="path of the PDF (default: render/<presentation>.pdf)")
    parser.add_argument("-f", "--fragments", metavar="MODE", default="all",
                        choices=("all", "none", "steps"),
                        help="how to handle fragments (incremental content): "
                             "all (one page per slide with all fragments shown, the default), "
                             "none (one page per slide with no fragments shown), "
                             "steps (one page per fragment step, like the reveal.js PDF export)")
    parser.add_argument("-n", "--notes", metavar="MODE", nargs="?", const="inline", choices=NOTE_MODES,
                        help="include the speaker notes in the PDF: "
                             "inline (at the bottom of the slide, the default) or "
                             "separate-page (on a page of their own)")
    parser.add_argument("-w", "--wait", metavar="MS", type=positive_int(0), default=0,
                        help="extra wait after the presentation is ready, in milliseconds; "
                             "only needed for content that reveal.js does not wait for")
    parser.add_argument("-t", "--timeout", metavar="SEC", type=positive_int(1), default=180,
                        help="how long to wait for the presentation to become ready "
                             "(default: 180); the PDF is printed anyway once this runs out")
    parser.add_argument("--png", action="store_true",
                        help="also export the pages as PNG images next to the PDF")
    parser.add_argument("--png-width", metavar="PX", type=positive_int(1),
                        help="width of the PNG images (default: 1920)")
    parser.add_argument("--png-dir", metavar="DIR",
                        help="directory for the PNG images (default: next to the PDF)")
    parser.add_argument("--config", metavar="KEY=VAL", action="append", default=[], type=config_option,
                        help="override a reveal.js config option, e.g. --config slideNumber=false "
                             "(repeatable; the values are passed in the URL query string)")
    parser.add_argument("--browser", metavar="BIN", default=os.environ.get("BROWSER_BIN"),
                        help="browser binary (default: chromium, chrome or google-chrome)")
    parser.add_argument("--keep-temp", action="store_true", help="keep the temporary browser profile")

    parsed = parser.parse_args(normalize_notes(arguments))
    # The PNG options imply --png.
    parsed.png = parsed.png or parsed.png_width is not None or parsed.png_dir is not None
    parsed.png_width = parsed.png_width or 1920
    return parsed


# --------------------------------------------------------------------------------- inputs


def build_url(presentation, fragments, notes, config):
    """Returns the URL of the print view of the presentation, and the name of the deck."""
    if presentation.startswith(("http://", "https://", "file://")):
        url = presentation
        name = Path(url.split("?")[0].split("#")[0]).name.removesuffix(".html")
    else:
        path = Path(presentation)
        if not path.is_file():
            raise RenderError(f"no such file: {presentation}")
        # as_uri percent-encodes the characters that are not allowed in a URL as such.
        url = path.resolve().as_uri()
        name = path.name.removesuffix(".html")

    # reveal.js switches to its print view based on the query string, and reads the rest of
    # its configuration from there as well.
    query = ["print-pdf", f"pdfSeparateFragments={str(fragments == 'steps').lower()}"]
    if notes:
        query.append(f"showNotes={notes}")
    query.extend(config)

    if "#" in url:
        raise RenderError("the presentation URL must not contain a hash (#)")
    url += ("&" if "?" in url else "?") + "&".join(query)
    return url, name or "presentation"


def find_browser(binary):
    if binary:
        if not shutil.which(binary):
            raise RenderError(f"browser not found: {binary}")
        return binary
    for candidate in BROWSER_CANDIDATES:
        if shutil.which(candidate):
            return candidate
    raise RenderError("no Chromium/Chrome found, install one or use --browser")


# -------------------------------------------------------------------------------- output


def print_to_pdf(url, output, browser_binary, profile, timeout, wait, fragments):
    """Loads the presentation in the browser and writes its print view into the PDF."""
    started = time.monotonic()
    browser = Browser(browser_binary, profile, timeout)
    try:
        browser.call("Page.enable")
        browser.call("Runtime.enable")
        browser.call("Page.addScriptToEvaluateOnNewDocument", source=INIT_SCRIPT)
        browser.call("Page.navigate", url=url)

        deadline = time.monotonic() + timeout
        ready = False
        while time.monotonic() < deadline:
            try:
                ready = bool(browser.evaluate(READY_SCRIPT))
            except RenderError:
                # The evaluation fails while the page is being navigated to.
                ready = False
            if ready:
                break
            time.sleep(0.2)

        if ready:
            log(f"The presentation is ready after {time.monotonic() - started:.1f} s")
        else:
            log(f"Warning: the presentation was not ready in {timeout} s, printing it anyway. "
                "Is it a reveal.js presentation, and does it load its resources?")

        if fragments == "none":
            browser.evaluate(HIDE_FRAGMENTS_SCRIPT)
        if wait:
            time.sleep(wait / 1000)

        pages = browser.evaluate(PAGE_COUNT_SCRIPT) or 0
        if pages:
            log(f"Printing {pages} slides...")

        # The page size is set by reveal.js with an @page rule based on the size of the slides.
        result = browser.call(
            "Page.printToPDF", printBackground=True, preferCSSPageSize=True,
            marginTop=0, marginBottom=0, marginLeft=0, marginRight=0,
        )
        pdf = base64.b64decode(result["data"])
    finally:
        browser.close()

    if not pdf.startswith(b"%PDF"):
        raise RenderError("the browser did not return a PDF")
    output.write_bytes(pdf)
    log(f"Wrote {len(pdf) / 1e6:.1f} MB to {output} in {time.monotonic() - started:.1f} s")


def export_pngs(output, png_dir, png_width):
    png_dir.mkdir(parents=True, exist_ok=True)
    for old in png_dir.glob("slide-[0-9]*.png"):
        old.unlink()
    # -scale-to-y -1 keeps the aspect ratio of the slides.
    subprocess.run(
        ["pdftoppm", "-png", "-scale-to-x", str(png_width), "-scale-to-y", "-1",
         str(output), str(png_dir / "slide")],
        check=True,
    )
    count = len(glob.glob(str(png_dir / "slide-[0-9]*.png")))
    log(f"Wrote {count} PNG images to {png_dir}")


def main(arguments):
    options = parse_arguments(arguments)
    url, name = build_url(options.presentation, options.fragments, options.notes, options.config)
    browser_binary = find_browser(options.browser)
    if options.png and not shutil.which("pdftoppm"):
        raise RenderError("pdftoppm (poppler-utils) is required for --png")

    output = Path(options.output or f"render/{name}.pdf")
    png_dir = Path(options.png_dir) if options.png_dir else output.parent
    output.parent.mkdir(parents=True, exist_ok=True)

    log(f"Presentation: {url}")
    log(f"Browser:      {browser_binary}")

    profile = tempfile.mkdtemp(prefix="revealjs-render-")
    try:
        print_to_pdf(url, output, browser_binary, profile, options.timeout, options.wait, options.fragments)
    finally:
        if options.keep_temp:
            log(f"Browser profile: {profile}")
        else:
            shutil.rmtree(profile, ignore_errors=True)

    if options.png:
        export_pngs(output, png_dir, options.png_width)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (RenderError, ConnectionError, OSError, subprocess.SubprocessError) as error:
        log(f"Error: {error}")
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)
