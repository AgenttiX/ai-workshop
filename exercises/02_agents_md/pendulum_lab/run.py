"""Run the analysis with the Python of the workshop's virtual environment.

Usage, on Linux, macOS and Windows alike: ``python run.py``
"""

from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
VENV_DIR = HERE.parents[2] / "venv"
PYTHON = VENV_DIR / "Scripts" / "python.exe" if sys.platform == "win32" else VENV_DIR / "bin" / "python"

if __name__ == "__main__":
    sys.exit(subprocess.run([str(PYTHON), str(HERE / "analyse.py")], check=False).returncode)
