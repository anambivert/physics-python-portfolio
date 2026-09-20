# Add another project

From the repository folder:

```bash
python scripts/new_project.py pid-control-analysis --title "PID Control Analysis"
```

On Windows, `py` can replace `python` if that is how Python is installed.

Use a short folder name made from lowercase letters, numbers, and hyphens. The utility copies [the project template](../templates/project/) into `projects/` and refuses to replace an existing project.

You can also copy the template folder manually and rename it.

## Finish the new project

1. Replace the notebook's instruction cells with your original code and explanations.
2. Put scripts in `src/`, suitable sample inputs in `data/sample/`, and selected plots in `figures/`.
3. Edit the project README: question, method, actual result, exact run instructions, and limitations.
4. Add a row linking the new README in [the main project index](../README.md).
5. Review the changed files, then commit with a descriptive message.

A compact entry is enough: one reproducible analysis, one useful figure, and a clear result. Additional investigations can follow later.

## Reuse the standard

For a fit, show the model assumptions, parameter units, and residuals. For a simulation, state the model, numerical settings, and a meaningful verification. For image analysis, explain the detector data, ROI, and background treatment.

Record the origin of code and data, including collaborators and any assistance. Distinguish work reproduced from the lab from new extensions.

The folder utility has been smoke-tested on Python 3.12. Lab 6 has its own numerical tests and a reproduced experimental run. Each future program needs its own validation after import.
