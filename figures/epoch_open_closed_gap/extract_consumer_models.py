"""Extract the ECI scores of the open-weights models that fit on a consumer GPU from Epoch AI's benchmark data.

Epoch AI publishes its benchmark data, including the Epoch Capabilities Index (ECI), as a zip file at
https://epoch.ai/data/benchmark_data.zip (CC BY 4.0). This script reads ``epoch_capabilities_index/eci_scores.csv``
from it and writes the models of :data:`MODELS` to ``consumer_gpu_models.csv``,
which ``epoch_open_closed_gap.py`` plots.

The data does not have the number of parameters of the models, so it's given in :data:`MODELS`.
The counts are from the model names and the model cards on Hugging Face.

Run with ``python -m figures.epoch_open_closed_gap.extract_consumer_models`` in the root directory of the repository.
Add ``--download`` to download the newest version of the zip file first.
"""

import argparse
import csv
from dataclasses import dataclass
import io
from pathlib import Path
import urllib.request
import zipfile

DATA_DIR = Path(__file__).resolve().parent
ZIP_URL = "https://epoch.ai/data/benchmark_data.zip"
ZIP_PATH = DATA_DIR / "benchmark_data.zip"
ECI_FILE = "epoch_capabilities_index/eci_scores.csv"
OUTPUT = DATA_DIR / "consumer_gpu_models.csv"


@dataclass(frozen=True)
class ModelInfo:
    """What we know about a model in addition to Epoch AI's data.

    :param params: total number of parameters (billions)
    :param active_params: number of parameters active per token (billions).
        Smaller than ``params`` for mixture-of-experts (MoE) models.
        Defaults to ``params``, i.e. a dense model.
    :param name: our name of the model, if it differs from Epoch AI's
    """

    params: float
    active_params: float | None = None
    name: str | None = None


#: The open-weights models with at most about 40 B parameters, by their name in Epoch AI's data (the "Model" column).
#: These include the best ones of each time, which make up the curve in the plot,
#: and some others for comparison.
MODELS: dict[str, ModelInfo] = {
    "LLaMA-33B": ModelInfo(32.5),
    "LLaMA-13B": ModelInfo(13.0),
    "Llama 2-13B": ModelInfo(13.0),
    "Qwen-14B": ModelInfo(14.2),
    "Mistral 7B v0.1": ModelInfo(7.2),
    "Yi-34B": ModelInfo(34.4),
    "Phi-2": ModelInfo(2.7),
    "Gemma 7B": ModelInfo(8.5),
    "Llama 3-8B": ModelInfo(8.0),
    "phi-3-small 7.4B": ModelInfo(7.4),
    "phi-3-medium 14B": ModelInfo(14.0),
    "Gemma 2 27B": ModelInfo(27.2),
    "Gemma 2 9B": ModelInfo(9.2),
    "Mistral NeMo": ModelInfo(12.2),
    "Qwen2.5-32B": ModelInfo(32.5),
    "Phi-4": ModelInfo(14.7),
    "DeepSeek-R1-Distill-Qwen-32B": ModelInfo(32.8),
    "DeepSeek-R1-Distill-Qwen-14B": ModelInfo(14.8),
    "Mistral Small 3": ModelInfo(24.0),
    "QwQ-32B": ModelInfo(32.5),
    "Gemma 3 27B": ModelInfo(27.4),
    "Qwen3-8B": ModelInfo(8.2),
    "Qwen3-32B": ModelInfo(32.8),
    "Qwen3-14B": ModelInfo(14.8),
    "Qwen3-30B-A3B": ModelInfo(30.5, 3.3),
    "Magistral Small 1.0": ModelInfo(24.0),
    "Qwen3-30B-A3B-Thinking (Jul 2025)": ModelInfo(30.5, 3.3),
    "gpt-oss-20b": ModelInfo(20.9, 3.6),
    "Qwen3.5-9B": ModelInfo(9.0),
    "Qwen3.5-35B-A3B": ModelInfo(35.0, 3.0),
    "Gemma 4 31B IT": ModelInfo(30.7, name="Gemma 4 31B"),
    "Gemma 4 26B A4B": ModelInfo(25.2, 3.8),
    "Qwen 3.6 35B-A3B": ModelInfo(35.0, 3.0, name="Qwen3.6-35B-A3B"),
    "Qwen3.6 27B": ModelInfo(27.0, name="Qwen3.6-27B"),
    "Qwen 3.8 27B": ModelInfo(27.0, name="Qwen3.8-27B"),
}

#: The columns of the output file
COLUMNS = [
    "Model",
    "Organization",
    "Release date",
    "Total parameters (B)",
    "Active parameters (B)",
    "Model accessibility",
    "ECI",
    "ECI CI low",
    "ECI CI high",
]


def read_eci_scores(zip_path: Path) -> dict[str, dict[str, str]]:
    """Read the ECI scores from Epoch AI's zip file without extracting it.

    :param zip_path: path to the zip file
    :return: the rows of ``eci_scores.csv`` by the name of the model
    """
    with zipfile.ZipFile(zip_path) as archive, archive.open(ECI_FILE) as file:
        reader = csv.DictReader(io.TextIOWrapper(file, encoding="utf-8"))
        return {row["Model"]: row for row in reader}


def extract(scores: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    """Collect the models of :data:`MODELS` from the ECI scores.

    :param scores: the rows of ``eci_scores.csv`` by the name of the model
    :return: the rows of the output file, sorted by release date and then by ECI from the highest
    :raises KeyError: if a model is missing from the data, e.g. because Epoch AI renamed it
    :raises ValueError: if a model does not have open weights
    """
    rows = []
    for epoch_name, info in MODELS.items():
        if epoch_name not in scores:
            raise KeyError(f"The model {epoch_name!r} is not in {ECI_FILE}.")
        score = scores[epoch_name]
        if not score["Model accessibility"].startswith("Open weights"):
            raise ValueError(f"The model {epoch_name!r} does not have open weights: {score['Model accessibility']}")
        active_params = info.params if info.active_params is None else info.active_params
        rows.append({
            "Model": info.name or epoch_name,
            "Organization": score["Organization"],
            "Release date": score["date"],
            "Total parameters (B)": f"{info.params:.1f}",
            "Active parameters (B)": f"{active_params:.1f}",
            "Model accessibility": score["Model accessibility"],
            "ECI": score["eci"],
            "ECI CI low": score["eci_ci_low"],
            "ECI CI high": score["eci_ci_high"],
        })
    return sorted(rows, key=lambda row: (row["Release date"], -float(row["ECI"])))


def main() -> None:
    """Extract the models and save them as a CSV file."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--download", action="store_true", help=f"download the zip file from {ZIP_URL} first")
    parser.add_argument("--output", type=Path, default=OUTPUT, help="the CSV file to write")
    args = parser.parse_args()

    if args.download:
        print(f"Downloading {ZIP_URL}")
        urllib.request.urlretrieve(ZIP_URL, ZIP_PATH)
    rows = extract(read_eci_scores(ZIP_PATH))
    with args.output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} models to {args.output}")


if __name__ == "__main__":
    main()
