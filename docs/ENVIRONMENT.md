# Python environment

Use Python 3.10 or newer for the project-creation utility. The lab programs may have their own requirements once imported.

The root `requirements.txt` contains a suggested toolkit for future projects. For the included labs, use `projects/gaussian-beam-analysis/requirements.txt` (Lab 02) and `projects/rubidium-spectroscopy/requirements.txt` (Lab 06). Both were tested on Python 3.12.14. Lab 02 adds openpyxl for Excel input; the shared NumPy, SciPy and Matplotlib pins match.

## Windows PowerShell

Open PowerShell inside the extracted repository folder. These commands use the environment directly, so activation is unnecessary:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r projects/gaussian-beam-analysis/requirements.txt -r projects/rubidium-spectroscopy/requirements.txt
.\.venv\Scripts\python.exe -m pip install jupyterlab
.\.venv\Scripts\python.exe -m jupyterlab
```

## macOS or Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r projects/gaussian-beam-analysis/requirements.txt -r projects/rubidium-spectroscopy/requirements.txt
.venv/bin/python -m pip install jupyterlab
.venv/bin/python -m jupyterlab
```

Open `projects/gaussian-beam-analysis/notebooks/analysis.ipynb` for the runnable Lab 02 workflow. Archived notebooks preserve historical code and cached output; consult their opening notes before running them. The generic template notebook contains instructions and empty cells for future projects.

## Once a real project runs

Record the Python version, required packages, exact input files, and launch command in its README. Save tested dependencies in that project's `requirements.txt` when it needs a specific environment.

For an existing Anaconda workflow, start by documenting the working environment before changing package versions. The project-folder utility uses only Python's standard library and does not require installing the scientific toolkit.

References: [Python virtual environments](https://docs.python.org/3/library/venv.html), [JupyterLab installation](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html).
