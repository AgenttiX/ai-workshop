# Figures
The figures of the slides, and the data and scripts for the plots made by us.

## `time_horizon.html`: the task horizon of AI models
Our own interactive Plotly plot of the 50 % time horizon of AI models against their release dates,
in the style of [METR's chart](https://metr.org/time-horizons/), with newer data points added.

- `benchmark_results_1_1.yaml`: METR's Time Horizon 1.1 data, as downloaded from
  <https://metr.org/assets/benchmark_results_1_1.yaml> on 2026-09-28 (last updated by METR on 2026-05-08).
  The horizon lengths are in minutes.
- `additional_results.yaml`: newer results in the same format, with their sources:
  - GPT-5.6 Sol: [METR, 2026-06-26](https://metr.org/blog/2026-06-26-gpt-5-6-sol/).
    METR does not consider this a robust measurement, so it's shown with a separate marker and not used for the trend.
- `plot_time_horizon.py`: the plotting script. The trend line is a least-squares fit of the base-2 logarithm
  of the horizon for the state-of-the-art models released since 2023 with horizons up to 16 h.
  This reproduces METR's doubling time of 128.7 days.

To regenerate the figure:
```bash
pip install -r figures/requirements.txt
python figures/plot_time_horizon.py --hide-legend
```
The slides use the version without the legend, where the trend line is labeled directly and the non-robust result is gray.
Leave out `--hide-legend` to show the legend.
Open `time_horizon.html` in a browser: hover over a point to see its values, drag to zoom and double-click to reset.
The page loads Plotly from its CDN and the Open Sans font of the slides from Google Fonts, so it needs an internet connection.
In the slides, it's shown in an `<iframe>` with `data-src`, so that reveal.js loads it only when its slide is shown:
Plotly can't measure its text in a hidden iframe, which would break the legend and the labels.

## `metr_time_horizon.svg`
METR's own chart, extracted from the D3 chart of <https://metr.org/time-horizons/> (updated 2026-05-08) on 2026-09-28,
with the Montserrat font (SIL Open Font License) embedded.

## Third-party figures
Used unchanged unless marked as cropped. The captions in the slides carry the same attribution.

| File | Source | Licence |
|---|---|---|
| `lost_in_the_middle.png` | N. F. Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, TACL 12, 157 (2024), [doi:10.1162/tacl_a_00638](https://doi.org/10.1162/tacl_a_00638), Fig. 1 | CC BY 4.0 (the TACL version; the arXiv version is not CC-licensed) |
| `hallucinated_references_arxiv.png` | Z. Zhao et al., *LLM hallucinations in the wild: Large-scale evidence from non-existent citations*, [arXiv:2605.07723](https://arxiv.org/abs/2605.07723), Fig. 1a, cropped to the arXiv panel | CC BY 4.0 |
| `epoch_open_closed_gap.png` | J. Edwards & L. Emberson, Epoch AI, [*Open models lag state-of-the-art closed models by 4 months*](https://epoch.ai/data-insights/open-closed-eci-gap), May 2026 | CC BY 4.0 |
| `hep_agent_timings.png` | E. A. Moreno et al., *AI Agents Can Already Autonomously Perform Experimental High Energy Physics*, [arXiv:2603.20179](https://arxiv.org/abs/2603.20179) | CC BY 4.0 |
| `metr_forecast_vs_observed.png` | METR (J. Becker, N. Rush et al.), *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*, [arXiv:2507.09089](https://arxiv.org/abs/2507.09089) | CC BY 4.0 |

## `blackbody_bug.png`
Our own plot: the normalised Planck spectrum of the Sun (T = 5778 K) with the correct \(1/\lambda^5\)
and the buggy \(1/\lambda^4\) of exercise 01. The peaks are at 501.5 nm and 635.1 nm (+26.6 %).

## Citations
- METR, *Task-Completion Time Horizons of Frontier AI Models*, <https://metr.org/time-horizons/>, 2026.
- T. Kwa et al., *Measuring AI Ability to Complete Long Tasks*,
  [arXiv:2503.14499](https://arxiv.org/abs/2503.14499) (CC BY 4.0).
- METR, *Summary of METR's predeployment evaluation of GPT-5.6 Sol*,
  <https://metr.org/blog/2026-06-26-gpt-5-6-sol/>, 2026.
