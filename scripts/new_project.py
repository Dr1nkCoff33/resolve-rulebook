#!/usr/bin/env python3
"""Create the project folder for one project from the template skeleton.

Step 1 of _TEMPLATE/NEW_PROJECT_ROUTINE.md: copy `_TEMPLATE/_folder_skeleton/`
and the template's `assets/` into `<projects root>/<ID>_<name>/`. The skeleton
is the only definition of the lanes; this script carries no list of its own.

Create and copy only. It never overwrites, renames or deletes anything, and
it stops if the episode folder already exists (the rules say stop and ask).

No network, no paid APIs, no media touched.

    python3 scripts/new_project.py EP012 my-first-project
    python3 scripts/new_project.py EP012 my-first-project --dry-run

Set PROJECTS_ROOT to your media drive (required). ID_PATTERN is a regex for
the project ID; the default accepts EP### or an ISO week like 2026-W41.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

DEFAULT_PROJECTS_ROOT = os.environ.get("PROJECTS_ROOT", "")
TEMPLATE_DIR = "_TEMPLATE"
SKELETON_DIR = "_folder_skeleton"

EP_RE = re.compile(os.environ.get("ID_PATTERN", r"^(EP\d{3}|\d{4}-W\d{2})$"))
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TEMPLATE_VERSION_RE = re.compile(r"^RESOLVE_TEMPLATE_v(\d{2})$")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the project folder for one project from the template skeleton."
    )
    parser.add_argument("episode", help="project ID, e.g. EP012 or 2026-W41")
    parser.add_argument("name", help="the packet slug: lowercase, hyphenated, e.g. resolve-use-case")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print what would be created and change nothing",
    )
    return parser.parse_args(argv)


def validate(episode: str, name: str) -> list[str]:
    errors: list[str] = []
    if not EP_RE.match(episode):
        errors.append(f"ID does not match ID_PATTERN, got {episode!r}")
    if not NAME_RE.match(name):
        errors.append(f"name must be lowercase, hyphenated, no spaces, got {name!r}")
    return errors


def newest_template(template_home: Path) -> Path | None:
    """The highest-numbered RESOLVE_TEMPLATE_v## folder with its own assets/, else the shared _TEMPLATE/assets/."""
    best: tuple[int, Path] | None = None
    for child in template_home.iterdir():
        m = TEMPLATE_VERSION_RE.match(child.name)
        if m and (child / "assets").is_dir():
            n = int(m.group(1))
            if best is None or n > best[0]:
                best = (n, child)
    if best:
        return best[1]
    shared = template_home / "assets"
    return template_home if shared.is_dir() else None


def copy_tree_no_overwrite(src: Path, dst: Path, dry_run: bool) -> list[str]:
    """Copy src into dst, creating only what is missing. Returns the paths created."""
    created: list[str] = []
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        target = dst / rel
        if target.exists():
            continue
        created.append(str(rel))
        if dry_run:
            continue
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    return created


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    episode, name = args.episode, args.name

    errors = validate(episode, name)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 2

    if not DEFAULT_PROJECTS_ROOT:
        print("error: set PROJECTS_ROOT to your media drive, e.g. /Volumes/video/Projects", file=sys.stderr)
        return 1
    root = Path(DEFAULT_PROJECTS_ROOT)
    if not root.is_dir():
        print(f"error: projects root not found: {root}. Is the drive mounted?", file=sys.stderr)
        return 1

    template_home = root / TEMPLATE_DIR
    skeleton = template_home / SKELETON_DIR
    if not skeleton.is_dir():
        print(f"error: skeleton not found: {skeleton}", file=sys.stderr)
        return 1
    template = newest_template(template_home)
    if template is None:
        print(f"error: no assets/ folder under {template_home}", file=sys.stderr)
        return 1

    project = root / f"{episode}_{name}"
    if project.exists():
        print(f"error: {project} already exists. Stop and ask; nothing was changed.", file=sys.stderr)
        return 1

    prefix = "would create" if args.dry_run else "created"
    print(f"project: {project}")
    print(f"assets from: {template}")
    if not args.dry_run:
        project.mkdir(parents=True)
    for rel in copy_tree_no_overwrite(skeleton, project, args.dry_run):
        print(f"  {prefix}: {rel}")
    for rel in copy_tree_no_overwrite(template / "assets", project / "assets", args.dry_run):
        print(f"  {prefix}: assets/{rel}")

    print()
    print("Next: copy originals into 01_CAMERA_A and 02_AUDIO, verify playback from the")
    print("drive, make a second copy, then continue with step 2 of NEW_PROJECT_ROUTINE.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
