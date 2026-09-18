# Exercise 01: Fix the bug (10 min)
`blackbody.py` implements Planck's law, and `test_blackbody.py` checks it against Wien's displacement law.
The test fails:
```bash
pytest exercises/01_fix_the_bug
```

## Task
1. Ask Claude Code to find and fix the bug, and to run the tests. Suggested prompt:
   > The Wien displacement test in exercises/01_fix_the_bug fails. Find the bug, fix it and run the tests.
2. **Read the diff before you accept it.** Does the fix make physical sense? Ask:
   > Explain what was wrong and why the test caught it.
3. Ask for a second test based on the Stefan–Boltzmann law: the integral of $\pi B_\lambda$ over all wavelengths
   should be $\sigma T^4$. Try *plan mode* (`Shift+Tab` in the terminal) so that it first proposes the test and you approve.
4. Run `python exercises/01_fix_the_bug/blackbody.py` to plot the spectra. Ask it to add the Sun's peak wavelength to the plot.

## What to look for
- The agent reads the test *and* the code before editing. If it guesses, ask it to run the tests first.
- The permission prompts: what it wants to run and why. You're the one accepting them.
- `/context` in the terminal shows what's in the context window now.
