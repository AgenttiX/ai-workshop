# Exercise 03: PTtools spectrum (15 min, bonus)
[PTtools](https://github.com/CFT-HY/pttools) computes gravitational wave spectra of first-order phase transitions
in the early universe. It's installed in your virtualenv, so the agent can *read its source code and documentation*
instead of hallucinating an API.

## Task
1. `spectrum.py` has a stub `compute_spectrum()` and `test_spectrum.py` tests it. Ask Claude Code to implement it:
   > Implement compute_spectrum() in exercises/03_pttools/spectrum.py with PTtools (installed in venv).
   > Use the bag model, an exponential nucleation type and the given r_star. Read the PTtools source and examples
   > to find the right API before writing code. Then run pytest exercises/03_pttools.

   The first run takes 1–3 minutes, as PTtools compiles its numerical code with Numba. If Claude's command times out,
   ask it to run the tests again. The NumbaLSODA and TBB messages printed on import are harmless.
2. Then ask it to implement `plot_spectra()` for several wall velocities, e.g. 0.4, 0.6 and 0.8, and run the script.
3. Ask a physics question about the result, e.g. why the peak frequency moves with the wall velocity,
   and check the answer against what you know. Being able to check is the point.

## What to look for
- Did it look at `venv/lib/python3.*/site-packages/pttools/` (`venv\Lib\site-packages\pttools\` on Windows)
  or the examples? An agent that reads the library is doing what you'd do — faster.
- If it gets stuck on the API, point it to `pttools.bubble.Bubble`, `pttools.models.BagModel` and `pttools.omgw0.Spectrum`.
