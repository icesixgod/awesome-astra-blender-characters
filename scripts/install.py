#!/usr/bin/env python3
"""Copy the distributable skill without overwriting an existing installation."""

import argparse
from pathlib import Path
import shutil
import sys
import tempfile


SKILL_NAME = "blender-character-workflow"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / SKILL_NAME
PACKAGE_FILES = (
    "SKILL.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/production-workflow.md",
    "references/blender-reliability.md",
    "references/static-illustration-finish.md",
)


def check_source() -> None:
    """Reject linked sources and require every file in the distribution manifest."""
    if SOURCE.is_symlink() or any(path.is_symlink() for path in SOURCE.rglob("*")):
        raise ValueError("Source skill must not contain symbolic links.")
    for name in PACKAGE_FILES:
        if not (SOURCE / name).is_file():
            raise FileNotFoundError(f"Incomplete source package: {name}")


def install(destination: Path) -> Path:
    """Install below a skill parent directory. Never merge or replace files."""
    parent = destination.expanduser().resolve()
    target = parent / SKILL_NAME
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Refusing to overwrite {target}. Back up and move it first.")
    if target.is_relative_to(SOURCE.resolve()):
        raise ValueError("The destination must be outside the source skill directory.")
    check_source()
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{SKILL_NAME}-", dir=parent) as directory:
        staged = Path(directory) / SKILL_NAME
        staged.mkdir()
        for name in PACKAGE_FILES:
            output = staged / name
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / name, output)
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Refusing to overwrite {target}.")
        staged.rename(target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--destination", type=Path, default=Path.home() / ".agents" / "skills",
        help="Skill parent directory (default: ~/.agents/skills). Existing installs are preserved.",
    )
    args = parser.parse_args()
    try:
        target = install(args.destination)
    except (OSError, ValueError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        return 1
    print(f"Installed: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
