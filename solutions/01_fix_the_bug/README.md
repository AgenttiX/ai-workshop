# Solution of exercise 01: Fix the bug

## The fix
In `blackbody.py`, Planck's law divided by the fourth power of the wavelength instead of the fifth:

```diff
-        return 2 * H * C**2 / wavelength**4 / np.expm1(x)
+        return 2 * H * C**2 / wavelength**5 / np.expm1(x)
```

After this change, `pytest exercises/01_fix_the_bug` should report `1 passed`.

## What was going on
Planck's law per unit wavelength is

$$B_\lambda(\lambda, T) = \frac{2 h c^2}{\lambda^5} \frac{1}{e^{hc / (\lambda k_B T)} - 1}.$$

With $\lambda^4$ instead of $\lambda^5$ the code computes $\lambda B_\lambda$, which peaks at a longer wavelength. For the Sun ($T = 5778$ K) the peak moves from 502 nm to 635 nm, so $\lambda_\text{max} T$ comes out as $3.67 \times 10^{-3}$ m K instead of Wien's $2.898 \times 10^{-3}$ m K: 27 % too large. The test allows a relative error of 0.1 %, so it fails.

This kind of bug is typical of AI-written code too: the program runs, the plot looks like a black-body spectrum, and nothing crashes. Only a check against known physics reveals it. That's why the test exists.

## What the agent typically does
1. Reads `test_blackbody.py` to see what is being tested, and `blackbody.py` to see the code.
2. Runs `pytest` to see the failure (you're asked for permission, unless it's allowed in the settings).
3. Compares the formula with Planck's law and changes the exponent.
4. Runs `pytest` again to confirm that the test passes.

Warning signs: it edits the test instead of the code, loosens the tolerance, or says "fixed" without running the tests.

## Step 4: the Stefan–Boltzmann test
The test in [`test_blackbody.py`](./test_blackbody.py) checks that the total power radiated per unit area, $\pi \int_0^\infty B_\lambda \thinspace d\lambda$, equals $\sigma T^4$ for three temperatures. The integral is computed numerically from 1 nm to 1 cm with the trapezoid rule on a logarithmic grid, which is wide and fine enough for a relative error below 0.1 %. Your version may look different. What matters is that it tests physics with a known answer.

## Step 5: the plot
`main()` in [`blackbody.py`](./blackbody.py) marks the Sun's peak wavelength with a dashed vertical line.

## What to take away about prompting
1. Say **where** the problem is, **what** is wrong and **how to check** the result ("run the tests").
2. Ask the agent to **explain** its change. You learn something, and a wrong fix is easier to spot.
3. Consider using **plan mode** for bigger fixes.
