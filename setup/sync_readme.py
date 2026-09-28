#!/usr/bin/env python3
"""Copy the setup scripts of this directory into the code blocks of the README.

The code blocks to fill are marked in ``README.md`` with a comment on the line before them, e.g.
``<!-- source: setup/ubuntu.sh -->`` followed by a fenced code block.
The paths are relative to the root of the repository.

Usage: ``./setup/sync_readme.py`` to update ``README.md``,
or ``./setup/sync_readme.py --check`` to only check that it is up to date (e.g. in CI).
"""

import argparse
from pathlib import Path
import re
import sys

REPO_DIR: Path = Path(__file__).resolve().parent.parent
README_PATH: Path = REPO_DIR / "README.md"

#: A code block with a source file: the marker and the opening fence, the current content and the closing fence
CODE_BLOCK: re.Pattern[str] = re.compile(
    r"(?P<open>^<!-- source: (?P<path>\S+) -->\n```[\w-]*\n)"
    r"(?P<content>.*?)"
    r"(?P<close>^```$)",
    re.DOTALL | re.MULTILINE,
)


def sync(readme: str, repo_dir: Path = REPO_DIR) -> tuple[str, list[str]]:
    """Replace the content of each marked code block with its source file.

    :param readme: the Markdown of the README
    :param repo_dir: the directory that the paths of the source files are relative to
    :return: the updated Markdown and the paths of the source files whose blocks changed
    """
    changed: list[str] = []

    def replace(match: re.Match[str]) -> str:
        path = match["path"]
        content = (repo_dir / path).read_text(encoding="utf-8").rstrip("\n") + "\n"
        if content != match["content"]:
            changed.append(path)
        return match["open"] + content + match["close"]

    return CODE_BLOCK.sub(replace, readme), changed


def main() -> int:
    """Update the README, or with ``--check`` only report whether it is out of date.

    :return: the exit code
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="only check that the README is up to date")
    args = parser.parse_args()

    readme = README_PATH.read_text(encoding="utf-8")
    if not CODE_BLOCK.search(readme):
        print(f"No code blocks marked with <!-- source: ... --> found in {README_PATH}")
        return 1
    updated, changed = sync(readme)
    if not changed:
        print("The README is up to date.")
        return 0
    if args.check:
        print("The README is out of date for: " + ", ".join(changed))
        print("Run: ./setup/sync_readme.py")
        return 1
    README_PATH.write_text(updated, encoding="utf-8")
    print("Updated the README for: " + ", ".join(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
