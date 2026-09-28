---
name: plot-style
description: The plotting conventions of the workshop. Use whenever creating, editing or saving a Matplotlib figure.
---

# Plotting conventions of the workshop

When making a plot with Matplotlib:

1. Call `workshop.plotting.apply_style()` once before creating figures. Do not set `rcParams` by hand.
2. Save figures with `workshop.plotting.save_fig(fig, name)`, which writes both PNG and PDF into `fig/`.
   Do not call `fig.savefig()` directly.
3. Label every axis with the quantity and its unit in parentheses, e.g. `Length (m)`.
   Use LaTeX for symbols: `r"$T^2$ (s$^2$)"`.
4. Use a logarithmic scale for quantities that span more than two orders of magnitude.
5. Add a legend when there is more than one line. Do not add a title; the caption goes in the paper.
6. Return the `Figure` object from plotting functions so that they can be tested and reused.
7. Use colour-blind-friendly colours: take them from the Okabe–Ito palette,
   `matplotlib.color_sequences["okabe_ito"]`, and pass them explicitly with `color=`.
   When lines must also be told apart in greyscale print, vary the line style or marker as well.

Example:

```python
import matplotlib as mpl
import matplotlib.pyplot as plt
from workshop.plotting import apply_style, save_fig

colors = mpl.color_sequences["okabe_ito"]
apply_style()
fig, ax = plt.subplots()
ax.plot(x, y, color=colors[5], label="data")
ax.set_xlabel("Length (m)")
ax.set_ylabel("Period (s)")
ax.legend()
save_fig(fig, "pendulum")
```
