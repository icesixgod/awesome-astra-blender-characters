#!/usr/bin/env python3
"""Validate metadata and inline local Markdown links; no Blender or network use."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    raise SystemExit("Install development dependencies: python3 -m pip install -r requirements-dev.txt")


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "blender-character-workflow"


def headings(text: str) -> set[str]:
    """Anchors for the simple ATX headings used by this repository."""
    anchors = set()
    counts: dict[str, int] = {}
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        anchors.add(f"{slug}-{count}" if count else slug)
        counts[slug] = count + 1
    return anchors


def check_links(path: Path, boundary: Path) -> list[str]:
    errors = []
    for link in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
        parts = urlsplit(link)
        if parts.scheme in {"https", "http", "mailto"}:
            continue
        if parts.scheme or parts.netloc or parts.path.startswith("/"):
            errors.append(f"{path.name}: non-portable link {link}")
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path.resolve()
        if not target.is_relative_to(boundary.resolve()):
            errors.append(f"{path.name}: link escapes package boundary: {link}")
        elif not target.exists():
            errors.append(f"{path.name}: missing link target: {link}")
        elif parts.fragment and target.suffix == ".md":
            if unquote(parts.fragment) not in headings(target.read_text(encoding="utf-8")):
                errors.append(f"{path.name}: missing heading: {link}")
    return errors


def validate(root: Path = ROOT) -> list[str]:
    errors = []
    skill = root / "skills" / SKILL_NAME
    try:
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            raise ValueError("SKILL.md requires YAML frontmatter")
        metadata = yaml.safe_load(match.group(1))
        if not isinstance(metadata, dict):
            raise ValueError("SKILL.md frontmatter must be a mapping")
        if metadata.get("name") != SKILL_NAME:
            errors.append("Skill name must match its distributable folder")
        description = metadata.get("description")
        if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
            errors.append("Skill description must be a nonempty string of at most 1024 characters")
        if metadata.get("license") != "MIT":
            errors.append("Skill license metadata must match the repository license")
        interface = yaml.safe_load((skill / "agents/openai.yaml").read_text(encoding="utf-8"))["interface"]
        for field in ("display_name", "short_description", "default_prompt"):
            if not isinstance(interface.get(field), str) or not interface[field].strip():
                errors.append(f"Missing UI string: {field}")
        if not 25 <= len(interface.get("short_description", "")) <= 64:
            errors.append("UI short_description must be 25–64 characters")
        if f"${SKILL_NAME}" not in interface.get("default_prompt", ""):
            errors.append("UI default_prompt must invoke the skill")
        if (root / "LICENSE").read_bytes() != (skill / "LICENSE").read_bytes():
            errors.append("The distributable license differs from the root license")
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        errors.append(f"Package metadata: {error}")

    for path in skill.rglob("*"):
        if path.is_symlink():
            errors.append(f"Distributable skill contains a symlink: {path.relative_to(root)}")
    documents = list(root.glob("*.md"))
    documents += list((root / "docs").rglob("*.md"))
    documents += list((root / ".github").rglob("*.md"))
    documents += list(skill.rglob("*.md"))
    for path in documents:
        errors.extend(check_links(path, skill if path.is_relative_to(skill) else root))
    for path in (root / ".github").rglob("*.yml"):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            errors.append(f"{path.relative_to(root)}: invalid YAML: {error}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("Validated skill metadata, package-local links and anchors, license copies, and GitHub YAML.")
