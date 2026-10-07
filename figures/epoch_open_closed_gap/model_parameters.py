"""The number of parameters of the small open-weights models in Epoch AI's ECI data.

Epoch AI's ``eci_scores.csv`` does not have the number of parameters of the models,
so we list them here to find the models that fit on a consumer GPU.
The counts are from the model names and the model cards on Hugging Face.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Parameters:
    """The number of parameters of a model.

    :param total: total number of parameters (billions)
    :param active: number of parameters active per token (billions).
        Smaller than ``total`` for mixture-of-experts (MoE) models. ``None`` for a dense model, where all are active.
    """

    total: float
    active: float | None = None

    def __str__(self) -> str:
        """Format the parameters for humans, e.g. "30.5 B (3.3 B active)"."""
        if self.active is None:
            return f"{self.total:.1f} B"
        return f"{self.total:.1f} B ({self.active:.1f} B active)"


#: The open-weights models with at most about 40 B parameters, by their name in Epoch AI's data (the "Model" column).
#: These include the best ones of each time, which make up the curve in the plot, and some others for comparison.
#: When Epoch AI adds new small models, add them here.
PARAMETERS: dict[str, Parameters] = {
    "LLaMA-33B": Parameters(32.5),
    "LLaMA-13B": Parameters(13.0),
    "Llama 2-13B": Parameters(13.0),
    "Qwen-14B": Parameters(14.2),
    "Mistral 7B v0.1": Parameters(7.2),
    "Yi-34B": Parameters(34.4),
    "Phi-2": Parameters(2.7),
    "Gemma 7B": Parameters(8.5),
    "Llama 3-8B": Parameters(8.0),
    "phi-3-small 7.4B": Parameters(7.4),
    "phi-3-medium 14B": Parameters(14.0),
    "Gemma 2 27B": Parameters(27.2),
    "Gemma 2 9B": Parameters(9.2),
    "Mistral NeMo": Parameters(12.2),
    "Qwen2.5-32B": Parameters(32.5),
    "Phi-4": Parameters(14.7),
    "DeepSeek-R1-Distill-Qwen-32B": Parameters(32.8),
    "DeepSeek-R1-Distill-Qwen-14B": Parameters(14.8),
    "Mistral Small 3": Parameters(24.0),
    "QwQ-32B": Parameters(32.5),
    "Gemma 3 27B": Parameters(27.4),
    "Qwen3-8B": Parameters(8.2),
    "Qwen3-32B": Parameters(32.8),
    "Qwen3-14B": Parameters(14.8),
    "Qwen3-30B-A3B": Parameters(30.5, 3.3),
    "Magistral Small 1.0": Parameters(24.0),
    "Qwen3-30B-A3B-Thinking (Jul 2025)": Parameters(30.5, 3.3),
    "gpt-oss-20b": Parameters(20.9, 3.6),
    "Qwen3.5-9B": Parameters(9.0),
    "Qwen3.5-35B-A3B": Parameters(35.0, 3.0),
    "Gemma 4 31B IT": Parameters(30.7),
    "Gemma 4 26B A4B": Parameters(25.2, 3.8),
    "Qwen 3.6 35B-A3B": Parameters(35.0, 3.0),
    "Qwen3.6 27B": Parameters(27.0),
    "Qwen 3.8 27B": Parameters(27.0),
}
