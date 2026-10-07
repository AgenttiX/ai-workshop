# Figures
The figures of the slides, and the data and scripts for the plots made by us.

The directory is a Python package, so the plotting scripts are run as modules in the root directory of the repository,
e.g. `python -m figures.time_horizon.time_horizon`.
Each plot has its own subdirectory (a subpackage) with its data, script and HTML page.
`common.py` has the code shared by the scripts: the font and colors of the slides,
and saving a figure as an HTML page that fills its iframe in the slides.

## `time_horizon/time_horizon.html`: the task horizon of AI models
Our own interactive Plotly plot of the 50 % time horizon of AI models against their release dates,
in the style of [METR's chart](https://metr.org/time-horizons/), with newer data points added.

- `benchmark_results_1_1.yaml`: METR's Time Horizon 1.1 data, as downloaded from
  <https://metr.org/assets/benchmark_results_1_1.yaml> on 2026-09-28 (last updated by METR on 2026-05-08).
  The horizon lengths are in minutes.
- `additional_results.yaml`: newer results in the same format, with their sources:
  - GPT-5.6 Sol: [METR, 2026-06-26](https://metr.org/blog/2026-06-26-gpt-5-6-sol/).
    METR does not consider this a robust measurement, so it's shown with a separate marker and not used for the trend.
- `time_horizon.py`: the plotting script. The trend line is a least-squares fit of the base-2 logarithm
  of the horizon for the state-of-the-art models released since 2023 with horizons up to 16 h.
  This reproduces METR's doubling time of 128.7 days.

All of these files are in `time_horizon/`.

To regenerate the figure:
```bash
pip install -r figures/requirements.txt
python -m figures.time_horizon.time_horizon --hide-legend
```
The slides use the version without the legend, where the trend line is labeled directly and the non-robust result is gray.
Leave out `--hide-legend` to show the legend.
Open `time_horizon.html` in a browser: hover over a point to see its values, drag to zoom and double-click to reset.
The page loads Plotly from its CDN and the Open Sans font of the slides from Google Fonts, so it needs an internet connection.
In the slides, it's shown in an `<iframe>` with `data-src`, so that reveal.js loads it only when its slide is shown:
Plotly can't measure its text in a hidden iframe, which would break the legend and the labels.

## `epoch_open_closed_gap/epoch_open_closed_gap.html`: closed, open and consumer-GPU models
Our own interactive Plotly version of Epoch AI's chart
[*Open models lag state-of-the-art closed models by 4 months*](https://epoch.ai/data-insights/open-closed-eci-gap)
(`epoch_open_closed_gap.png`), with a third curve for the open-weights models
that fit on a consumer-grade GPU with 32 GB of VRAM.
Each curve shows the models that had a higher Epoch Capabilities Index (ECI) than any earlier model of their group.
Gemma 4 26B A4B is also shown as a point of the 32 GB GPU curve, although it's below the curve.
Gemma 4 E2B, E4B and 12B are not shown, as Epoch AI's data of October 2026 has no ECI score for them.

- `benchmarked_models.csv`: the data of Epoch AI's chart (CC BY 4.0), May 2026.
  As in their chart, the models without an "Open weights" accessibility count as closed.
- `consumer_gpu_models.csv`: open-weights models with at most 40 B parameters,
  whose 4-bit quantized weights (about 20 GB) fit in 32 GB of VRAM with room for the context.
  The ECI scores, their 90 % confidence intervals, the release dates and the accessibility are from
  Epoch AI's ECI data (`epoch_capabilities_index/eci_scores.csv` of <https://epoch.ai/data/benchmark_data.zip>,
  CC BY 4.0), downloaded on 2026-10-07. The parameter counts are from the model names and model cards.
  The ECI has been refitted since May 2026, which changes the scores of the same models by about ±1 (standard deviation),
  so the curves can be compared to within about that accuracy.
- `extract_consumer_models.py`: the script that makes `consumer_gpu_models.csv` from `benchmark_data.zip`.
  The models and their parameter counts are listed in the script.
- `benchmark_data.zip`: Epoch AI's benchmark data, downloaded on 2026-10-07.
  It's not in Git (`*.zip` is in `.gitignore`), so download it with the `--download` option of the script.
- `epoch_open_closed_gap.py`: the plotting script.

All of these files are in `epoch_open_closed_gap/`.

To regenerate the figure:
```bash
pip install -r figures/requirements.txt
python -m figures.epoch_open_closed_gap.epoch_open_closed_gap
```
To update the 32 GB GPU curve with the newest data of Epoch AI, add any new models to `MODELS`
in `extract_consumer_models.py`, then run before the plotting script:
```bash
python -m figures.epoch_open_closed_gap.extract_consumer_models --download
```

## Third-party figures
Used unchanged unless marked as cropped. The captions in the slides carry the same attribution.

| File | Source | Licence |
|---|---|---|
| `lost_in_the_middle.png` | N. F. Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, TACL 12, 157 (2024), [doi:10.1162/tacl_a_00638](https://doi.org/10.1162/tacl_a_00638), Fig. 1 | CC BY 4.0 (the TACL version; the arXiv version is not CC-licensed) |
| `hallucinated_references_arxiv.png` | Z. Zhao et al., *LLM hallucinations in the wild: Large-scale evidence from non-existent citations*, [arXiv:2605.07723](https://arxiv.org/abs/2605.07723), Fig. 1a, cropped to the arXiv panel | CC BY 4.0 |
| `epoch_open_closed_gap/epoch_open_closed_gap.png` | J. Edwards & L. Emberson, Epoch AI, [*Open models lag state-of-the-art closed models by 4 months*](https://epoch.ai/data-insights/open-closed-eci-gap), May 2026 | CC BY 4.0 |
| `hep_agent_timings.png` | E. A. Moreno et al., *AI Agents Can Already Autonomously Perform Experimental High Energy Physics*, [arXiv:2603.20179](https://arxiv.org/abs/2603.20179) | CC BY 4.0 |
| `mistral_logo.svg` | Mistral AI logo, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Mistral_AI_logo_(2025%E2%80%93).svg) | Public domain (text logo); a trademark of Mistral AI |
| `metr_forecast_vs_observed.png` | METR (J. Becker, N. Rush et al.), *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*, [arXiv:2507.09089](https://arxiv.org/abs/2507.09089) | CC BY 4.0 |

## Backup-slide plots: `training_compute.html`, `benchmarks.html`, `session_tokens.html`
Our own interactive Plotly plots. They load Plotly from its CDN, so they need an internet connection.
- `training_compute.html`: training compute of notable models vs. publication date, with our least-squares fit
  to Epoch AI's frontier models since 2020 (×4.6 per year). Data: Epoch AI, *Data on AI Models*
  (<https://epoch.ai/data/notable_ai_models.csv>, CC BY 4.0), downloaded on 2026-10-07.
- `benchmarks.html`: the best score so far on MMLU, GPQA Diamond, SWE-bench Verified, FrontierMath,
  Humanity's Last Exam and CritPt. Data: Epoch AI's benchmark data (CC BY 4.0), downloaded on 2026-10-07.
- `ai_race.html`: notable AI models per year by region (United States, China, EU, United Kingdom, other,
  multinational), our count from the same Epoch AI data.
- `session_tokens.html`: the tokens in the context of each request during one of our own Claude Code sessions
  (token counts from the session log only, no message content).

## `blackbody_bug.png`
Our own plot: the normalised Planck spectrum of the Sun (T = 5778 K) with the correct \(1/\lambda^5\)
and the buggy \(1/\lambda^4\) of exercise 01. The peaks are at 501.5 nm and 635.1 nm (+26.6 %).

## Citations
- METR, *Task-Completion Time Horizons of Frontier AI Models*, <https://metr.org/time-horizons/>, 2026.
- T. Kwa et al., *Measuring AI Ability to Complete Long Tasks*,
  [arXiv:2503.14499](https://arxiv.org/abs/2503.14499) (CC BY 4.0).
- METR, *Summary of METR's predeployment evaluation of GPT-5.6 Sol*,
  <https://metr.org/blog/2026-06-26-gpt-5-6-sol/>, 2026.
