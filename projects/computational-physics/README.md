# Computational Physics

**Status:** collection outline; original scripts and notebooks pending import.

A home for my numerical computing work, including Fourier analysis, nonlinear equations, differential equations, and statistical simulation.

## Analyses to organize

| Area | Work to locate | Useful verification when documenting it |
| --- | --- | --- |
| Fourier and spectral analysis | Recursive FFT implementation and spectral-analysis notebooks | Compare with a trusted transform and a signal with known frequencies |
| Differential equations | Existing ODE and oscillator simulations, including work with `solve_ivp` | Check solver success, tolerances, and an appropriate limiting case |
| Nonlinear equations | Existing root-finding work with `fsolve` | Report equation residuals and dependence on starting guesses |
| Monte Carlo methods | Existing sampling and simulation notebooks | State the random seed, estimator, convergence behaviour, and uncertainty |

These are topics from previous coding work. Implementations and results are not bundled in this initial repository.

## Organization

Small related notebooks can remain in this folder. Give larger analyses their own project using `scripts/new_project.py` so each has a clear question and reproduction instructions.

## What to include

Start with an original notebook that demonstrates a substantial piece of your work. Explain the model, numerical method, main result, and a meaningful check. Include an animation only when it helps explain the behaviour.

## Reproduction

Add the source, any required inputs, tested dependencies, and exact run instructions during import.

## Authorship

The outline reflects Siddharth Prajapati's previously discussed coding topics. This documentation was prepared with AI assistance. Identify the original code authors and any later assistance for each added analysis.
