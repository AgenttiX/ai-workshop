#!/usr/bin/env python3
"""Copy the setup scripts of this directory into the code blocks of the slides.

The code blocks to fill are marked in ``slides.html`` with the path of their source file, e.g.
``<code class="language-bash" data-trim data-source-file="setup/ubuntu.sh">``.
The paths are relative to the root of the repository.

Usage: ``./setup/sync_slides.py`` to update ``slides.html``,
or ``./setup/sync_slides.py --check`` to only check that it is up to date (e.g. in CI).
"""

import argparse
import html
from pathlib import Path
import re
import sys

REPO_DIR: Path = Path(__file__).resolve().parent.parent
SLIDES_PATH: Path = REPO_DIR / "slides.html"

#: A code block with a source file: the opening tag, the current content and the indentation of the closing tag
CODE_BLOCK: re.Pattern[str] = re.compile(
    r'(?P<open><code\b[^>]*\bdata-source-file="(?P<path>[^"]+)"[^>]*>\n)'
    r"(?P<content>.*?)"
    r"(?P<close>\n[ \t]*</code>)",
    re.DOTALL,
)


def sync(slides: str, repo_dir: Path = REPO_DIR) -> tuple[str, list[str]]:
    """Replace the content of each marked code block with its source file.

    :param slides: the HTML of the slides
    :param repo_dir: the directory that the paths of the source files are relative to
    :return: the updated HTML and the paths of the source files whose blocks changed
    """
    changed: list[str] = []

    def replace(match: re.Match[str]) -> str:
        path = match["path"]
        content = html.escape((repo_dir / path).read_text(encoding="utf-8").rstrip("\n"), quote=False)
        if content != match["content"]:
            changed.append(path)
        return match["open"] + content + match["close"]

    return CODE_BLOCK.sub(replace, slides), changed


def main() -> int:
    """Update the slides, or with ``--check`` only report whether they are out of date.

    :return: the exit code
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="only check that the slides are up to date")
    args = parser.parse_args()

    slides = SLIDES_PATH.read_text(encoding="utf-8")
    if not CODE_BLOCK.search(slides):
        print(f"No code blocks with data-source-file found in {SLIDES_PATH}")
        return 1
    updated, changed = sync(slides)
    if not changed:
        print("The slides are up to date.")
        return 0
    if args.check:
        print("The slides are out of date for: " + ", ".join(changed))
        print("Run: ./setup/sync_slides.py")
        return 1
    SLIDES_PATH.write_text(updated, encoding="utf-8")
    print("Updated the slides for: " + ", ".join(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
