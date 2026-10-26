# Exercise 01: Fix the bug (10 min)
**You will practise:** giving Claude Code a task, and checking its work before you accept it.

`blackbody.py` computes how much light a hot object emits at each wavelength (Planck's law). `test_blackbody.py` is a *test*: a small program that checks the code against a known fact, Wien's displacement law, which says that the Sun's spectrum peaks at about 500 nm. The test fails, so the code has a bug. Your job is to get Claude to find and fix it, and to make sure the fix is right.

**Before you start:** the workshop repository is open in VS Code, the virtual environment is active and a terminal is open (see [exercise 00](../00_setup/)).

## 1. See the test fail
Type this in the VS Code terminal and press Enter:

```bash
pytest exercises/01_fix_the_bug
```

The last line should say `1 failed` in red.

<details>
<summary>What is a test, and what is pytest?</summary>

A test is a function that runs your code and checks the result against something you know to be true, here that the peak wavelength times the temperature equals Wien's constant $b = 2.898 \times 10^{-3}$ m K. `pytest` finds all the files called `test_*.py`, runs the test functions in them and reports which ones fail. Tests matter even more with AI: they are how the agent (and you) can *check* that code is correct instead of just believing it.
</details>

## 2. Give Claude the task
Open the Claude Code panel (the Spark icon in the top-right corner of the editor when a file is open, or in the Activity Bar on the left).

**Before you type anything, switch to *Manual* mode.** Claude Code starts in *Auto* mode, where it acts without asking. Click the mode indicator at the bottom of the prompt box and choose **Manual** (in the terminal: press Shift+Tab until the status line says `manual mode on`). Then it asks you before editing a file or running a command.

Now describe the problem. Try to use your own words. If you're stuck, copy this:

> The test in exercises/01_fix_the_bug fails. Find the bug, fix it and run the tests to check that they pass.

Claude now reads the files, thinks, and asks before it edits or runs commands. Read what it wants to do before you click *Yes*.

<details>
<summary>Why this prompt works</summary>

A good task tells the agent three things:

1. **Where:** `exercises/01_fix_the_bug`, so it doesn't have to search the whole repository.
2. **What is wrong:** the test fails. It can run the test itself to see how.
3. **How to check the result:** "run the tests". Without this, the agent may stop after editing and only *claim* that the fix works.

Try it yourself: start a new conversation with `/clear`, undo the fix, and ask only "fix my code". Compare what it does. To undo the fix, restore the file to the version in Git:

```bash
git restore exercises/01_fix_the_bug/blackbody.py
```

</details>

## 3. Check the change before you accept it
When Claude edits a file, VS Code shows the change as a *diff*: red lines were removed, green lines were added. Look at it and ask yourself whether it makes physical sense. Then ask Claude:

> Explain what was wrong and why the test caught it.

<details>
<summary>Why read the change if the test passes?</summary>

A passing test only proves what the test checks. An agent can also make a test pass the wrong way, for example by loosening the tolerance of the test instead of fixing the formula. Check *which file* it changed: here the fix belongs in `blackbody.py`, not in `test_blackbody.py`.
</details>

## 4. Plan first, then act
For bigger changes it's better to see the plan before anything is edited. Switch to *plan mode*:

- In the VS Code panel: click the mode indicator below the prompt box and choose plan mode, or type `/plan`.
- In the terminal (`claude`): press `Shift+Tab` until the status line says plan mode.

Then ask:

> Add a second test based on the Stefan–Boltzmann law: π times the integral of the spectral radiance over all wavelengths should equal σT⁴.

Read the plan. If it looks right, approve it; if not, tell Claude what to change.

<details>
<summary>What is plan mode for?</summary>

In plan mode Claude only reads and thinks; it doesn't edit files or run commands that change anything. You get a proposal you can correct while it's still cheap to do so. Use it whenever the task is more than a one-line fix, or when you're not sure the agent understood what you meant.
</details>

## 5. Make a plot (optional)

```bash
python exercises/01_fix_the_bug/blackbody.py
```

A window with the spectra opens (close it to finish), and the figure is saved to `fig/blackbody.png`. Then ask:

> Mark the peak wavelength of the Sun (5778 K) in the plot.

## Useful while you work
- `/context` shows what is currently in Claude's context window, i.e. everything it "knows" in this conversation.
- `/clear` starts a new conversation with an empty context.

## Finished or stuck?
The solution and an explanation of what happened are in [`solutions/01_fix_the_bug/`](../../solutions/01_fix_the_bug/). Try on your own first. You can run the tests of the solution with `pytest solutions/01_fix_the_bug`.
