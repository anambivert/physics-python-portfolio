# Python environment

Use Python 3.10 or newer for the project-creation utility. The lab programs may have their own requirements once imported.

The root `requirements.txt` contains a suggested toolkit for future projects. For the included Lab 6 analysis, use `projects/rubidium-spectroscopy/requirements.txt`; its versions were tested on Python 3.12.14.

## Windows PowerShell

Open PowerShell inside the extracted repository folder. These commands use the environment directly, so activation is unnecessary:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab
```

## macOS or Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyterlab
```

Open a project notebook in JupyterLab. The template notebook contains instructions and empty analysis cells; it does not contain an experimental analysis.

## Once a real project runs

Record the Python version, required packages, exact input files, and launch command in its README. Save tested dependencies in that project's `requirements.txt` when it needs a specific environment.

For an existing Anaconda workflow, start by documenting the working environment before changing package versions. The project-folder utility uses only Python's standard library and does not require installing the scientific toolkit.

References: [Python virtual environments](https://docs.python.org/3/library/venv.html), [JupyterLab installation](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html).
