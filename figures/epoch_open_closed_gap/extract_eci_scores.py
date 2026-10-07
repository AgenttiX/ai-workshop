"""Extract the Epoch Capabilities Index (ECI) scores from Epoch AI's benchmark data.

Epoch AI publishes its benchmark data, including the ECI, as a zip file at
https://epoch.ai/data/benchmark_data.zip (CC BY 4.0). This script extracts ``epoch_capabilities_index/eci_scores.csv``
from it to ``eci_scores.csv``, which ``epoch_open_closed_gap.py`` plots.

Run with ``python -m figures.epoch_open_closed_gap.extract_eci_scores`` in the root directory of the repository.
Add ``--download`` to download the newest version of the zip file first.
"""

import argparse
from pathlib import Path
import urllib.request
import zipfile

DATA_DIR = Path(__file__).resolve().parent
ZIP_URL = "https://epoch.ai/data/benchmark_data.zip"
ZIP_PATH = DATA_DIR / "benchmark_data.zip"
ECI_FILE = "epoch_capabilities_index/eci_scores.csv"
OUTPUT = DATA_DIR / "eci_scores.csv"


def main() -> None:
    """Extract the ECI scores from the zip file."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--download", action="store_true", help=f"download the zip file from {ZIP_URL} first")
    parser.add_argument("--output", type=Path, default=OUTPUT, help="the CSV file to write")
    args = parser.parse_args()

    if args.download:
        print(f"Downloading {ZIP_URL}")
        urllib.request.urlretrieve(ZIP_URL, ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH) as archive:
        args.output.write_bytes(archive.read(ECI_FILE))
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
