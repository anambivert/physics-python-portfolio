"""Create a portfolio project from the bundled template.

Run from any directory with Python 3.10+:
    python scripts/new_project.py project-name --title "Project Title"

This utility prepares folders and instructions; it does not generate lab code.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RESERVED_NAMES = {"con", "prn", "aux", "nul"} | {
    f"{prefix}{number}"
    for prefix in ("com", "lpt")
    for number in range(1, 10)
}


def create_project(slug: str, title: str) -> Path:
    """Copy the template into projects, refusing invalid or existing targets."""
    if (
        not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug)
        or len(slug) > 64
        or slug in RESERVED_NAMES
    ):
        raise ValueError(
            "Use a name of at most 64 lowercase letters, numbers and hyphens "
            "(not a reserved Windows device name)."
        )
    title = title.strip()
    if not title or any(character in title for character in "\r\n"):
        raise ValueError("The project title must be a non-empty single line.")

    template = REPOSITORY_ROOT / "templates" / "project"
    target = REPOSITORY_ROOT / "projects" / slug
    if not template.is_dir():
        raise FileNotFoundError("The bundled templates/project folder is missing.")
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Project already exists: {slug}")

    shutil.copytree(template, target)
    readme = target / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace("{{PROJECT_TITLE}}", title),
        encoding="utf-8",
    )
    notebook_path = target / "notebooks" / "analysis.ipynb"
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        cell["source"] = [
            line.replace("{{PROJECT_TITLE}}", title) for line in cell["source"]
        ]
    notebook_path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Project folder name, e.g. pid-control-analysis")
    parser.add_argument("--title", help="Readable project title")
    args = parser.parse_args()
    title = args.title if args.title is not None else args.name.replace("-", " ").title()
    try:
        target = create_project(args.name, title)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Could not create project: {error}\n")
    print(f"Created {target.relative_to(REPOSITORY_ROOT).as_posix()}")
    print("Add your original code and data, then update the main README project index.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
