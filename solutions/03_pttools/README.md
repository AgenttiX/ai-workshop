# Solution of exercise 03: PTtools spectrum

## The result
The core of [`spectrum.py`](./spectrum.py) is four lines:
```python
model = BagModel(alpha_n_min=min(alpha_n, 0.01))
bubble = Bubble(model, v_wall=v_wall, alpha_n=alpha_n)
spectrum = Spectrum(bubble, nuc_type=NucType.EXPONENTIAL, r_star=r_star)
return np.asarray(spectrum.f(), dtype=float), np.asarray(spectrum.omgw0_h2(), dtype=float)
```
`pytest exercises/03_pttools` should report `3 passed`. `plot_spectra()` draws the spectra for
$v_\text{wall} = 0.4, 0.6, 0.8$ on log-log axes and saves them to `fig/spectra.png`.

## What was going on
Shortly after the Big Bang, the universe may have gone through a *first-order phase transition*:
like water boiling, bubbles of a new phase appear in the hot plasma and grow until they fill space.
The expanding bubbles push the plasma and create sound waves, and the sound waves produce gravitational waves
that might be detectable today, e.g. by the planned LISA space observatory.
PTtools computes that gravitational wave spectrum. What the four lines mean:

- **`BagModel`**: the simplest *equation of state* (the relation between pressure, energy and temperature) for the two phases.
  The phases differ by a constant vacuum energy, and sound travels at $c_s = 1/\sqrt{3} \approx 0.577$ times the speed of light in both.
  `alpha_n_min` sets up the model so that transition strengths down to that value are allowed.
- **`Bubble`**: solves the flow of the plasma around one expanding bubble, the *sound shell*, for a given wall speed
  $v_\text{wall}$ (in units of the speed of light) and transition strength $\alpha_n$
  (roughly: the energy the transition releases relative to the thermal energy of the plasma).
- **`Spectrum`**: adds up many such bubbles with the *sound shell model* and computes the gravitational wave power spectrum.
  - `NucType.EXPONENTIAL`: new bubbles appear at a rate that grows exponentially in time (the other option is all at once).
  - `r_star` $= r_* = H_* R_*$: the mean distance between bubbles $R_*$ in units of the Hubble length $1/H_*$ at the time of the transition.
    $r_* = 0.1$ means the bubbles are about a tenth of a Hubble length apart, and the Hubble length is roughly
    the size of a causally connected region at that time.
- **`spectrum.f()`**: the frequencies today in Hz. PTtools computes the spectrum as a function of $z = k R_*$
  (the wavenumber times the bubble spacing, from 0.1 to 1000 by default) and converts it to today's frequency
  $f = z f_{*,0} / r_*$ with the redshift since the transition. For the bag model it assumes the transition happened
  at $T_* = 100$ GeV with $g_* = 100$ relativistic degrees of freedom, which gives $f_{*,0} = 2.6$ μHz.
- **`spectrum.omgw0_h2()`**: $\Omega_\text{gw,0} h^2$, the energy density of gravitational waves today per logarithmic
  frequency interval, as a fraction of the critical density (the density of a spatially flat universe).
  It is multiplied by $h^2$, where the Hubble constant is $H_0 = 100\,h$ km/s/Mpc. The critical density is
  proportional to $H_0^2$, so $\Omega_\text{gw,0} h^2$ doesn't depend on the measured value of $H_0$.
  This is the quantity usually compared with detector sensitivities.

Note: `spectrum.omgw0()` without `_h2` is $\Omega_\text{gw,0}$ itself, i.e. $\Omega_\text{gw,0} h^2$ divided by
PTtools' $h^2 = 0.458$: a factor of 2.18 larger. An earlier version of this reference solution used it by mistake.
The names differ by three characters, the tests only check the shape of the spectrum, and the plot looks fine either way.
Only the docstring tells them apart. Agents make exactly this kind of mistake, so ask them to quote the docstring.

## How the agent should find the API
The library is installed in the virtual environment, so the agent can read its source code and docstrings:

| System | Location |
|---|---|
| Linux, macOS | `venv/lib/python3.12/site-packages/pttools/` |
| Windows | `venv\Lib\site-packages\pttools\` |

Good behaviour looks like: searching for `class Spectrum`, reading the `__init__` docstrings of `Bubble` and `Spectrum`,
or running `python -c "from pttools.omgw0 import Spectrum; help(Spectrum)"`.
The worked examples are in the [GitHub repository](https://github.com/CFT-HY/pttools/tree/main/examples),
not in the installed package, so an agent can only read them from the web.

Warning signs: it writes `import pttools` and calls functions without having opened any PTtools file;
it invents parameters such as `Spectrum(v_wall=..., alpha=...)`; or it changes `test_spectrum.py` when the API doesn't fit.

## The slow first run
PTtools uses Numba, which compiles the numerical functions to machine code the first time they are called
and stores the result on disk. On an 8-thread laptop (Intel i5-1145G7) the first `compute_spectrum()` took 55 s
with an empty cache and 5 s afterwards. If the agent's command times out during the first run, tell it to run the tests again.

## Step 3: why the peak frequency moves with the wall speed
What we got with $\alpha_n = 0.2$, $r_* = 0.1$ and exponential nucleation:

| $v_\text{wall}$ | 0.4 | 0.5 | 0.6 | 0.65 | 0.7 | 0.8 | 0.9 |
|---|---|---|---|---|---|---|---|
| Type of solution | deflagration | deflagration | hybrid | hybrid | hybrid | hybrid | detonation |
| Peak frequency (μHz) | 71 | 96 | 234 | 326 | 89 | 87 | 89 |

A reasonable explanation, based on the sound shell model
([Hindmarsh & Hijazi 2019, arXiv:1909.10040](https://arxiv.org/abs/1909.10040)):
the spectrum has two length scales, the bubble spacing $R_*$ and the thickness of the sound shell.
For small $\alpha_n$ the shell thickness is about $R_* |v_\text{wall} - c_s| / v_\text{wall}$.
Here $R_*$ is fixed by `r_star`, so the wall speed changes only the shell. Near $c_s \approx 0.577$ the shell is thin,
and the peak moves to higher frequencies. For wall speeds far from $c_s$ the shell is thick and the peak sits near
the scale of the bubble spacing ($z = k R_* \approx 3$).
So of 0.4, 0.6 and 0.8, the spectrum for 0.6 peaks highest.

Caveats, and what to check rather than believe:
- The thin-shell estimate is for weak transitions. At $\alpha_n = 0.2$ the hybrid shells are thicker, and the peak
  jumps back between 0.65 and 0.7 instead of moving smoothly. At $v_\text{wall} = 0.675$ we found two local maxima
  of almost equal height. With $\alpha_n = 0.05$ the peak moved smoothly, highest at 0.6.
- Here the bubble spacing is fixed. If you fix the nucleation rate $\beta$ instead, $R_* \propto v_\text{wall}/\beta$
  (for detonations; see the docstring of `pttools.ssm.nucleation.R_star`), which moves the whole spectrum as well.
- The absolute frequency scale depends on the assumed $T_*$ and $g_*$.

If the agent's answer mentions the shell thickness and $c_s$, it's on the right track.
If it says "faster walls give higher frequencies" without qualification, ask it to compute the peak for a few wall speeds.

## What to take away about prompting
1. Tell the agent *where the truth is*: "read the PTtools source in venv before writing code".
2. Ask for evidence: which file and which docstring did it base the call on?
3. For physics questions, ask the agent to *compute* something you can check (here: the peak frequency against $v_\text{wall}$), not only to explain.
