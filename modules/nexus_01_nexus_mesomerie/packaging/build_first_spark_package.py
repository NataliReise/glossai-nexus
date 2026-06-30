#!/usr/bin/env python3
"""Build a standalone Nexus 01 - First Spark preview package.

The package builder creates a small, public-safe folder that can be shared
manually for feedback or demonstration. It intentionally does not copy private
activation files, local results, Git metadata, caches, or development-only
artifacts.
"""

from __future__ import annotations

import argparse
import shutil
import stat
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = SCRIPT_PATH.parents[3]
FIRST_SPARK_ROOT = NEXUS_ROOT / "first_spark"
DEFAULT_PACKAGE_NAME = "nexus-01-first-spark-preview"
DEFAULT_DIST_ROOT = REPO_ROOT / "dist"

COPY_FILES = (
    "run_first_spark.py",
    "create_local_activation.py",
    "activation.example.json",
)

COPY_DIRS = (
    "first_spark",
)

PRIVATE_OR_GENERATED_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "activation.local.json",
    "return_slot.local.json",
    "return_artifact.local.txt",
    "local_result.md",
}

PRIVATE_OR_GENERATED_SUFFIXES = (
    ".pyc",
    ".pyo",
    ".local.md",
    ".local.json",
    ".local.txt",
)

README_FOR_PLAYER = """# Nexus 01 - First Spark Preview Package

Welcome to **Nexus 01 - First Spark**.

This is a small local terminal experience from the public **glossai-nexus** project.

It can be played as a neutral public demo. A private gift version may later use a private `activation.local.json` file, but this preview package does not contain real private gift data.

## Start

Open a terminal in this folder and run:

```bash
./START_HERE.sh
```

If that does not work, run:

```bash
python3 run_first_spark.py
```

You need Python 3 and a Linux terminal.

## Useful commands inside First Spark

Try these commands during play:

```text
help
look
read welcome.log
read spark.note
link spark
unlock
resonance-node
quit
```

You can also type:

```text
walkthrough
```

for the full solution path.

## Public / private boundary

This preview package is public-safe.

It contains only demo activation data.

Real private messages belong in:

```text
activation.local.json
```

A real `activation.local.json` file should stay private and should not be posted, committed, or shared accidentally.

## Optional local activation test

To create a local activation file from the safe public example, run:

```bash
python3 create_local_activation.py
```

This creates `activation.local.json` only if it does not already exist.

For this preview package, editing that file is optional.

## Feedback focus

If you received this package for testing, useful feedback includes:

```text
Could you unpack it easily?
Was it clear how to start?
Did the terminal flow make sense?
Did it feel like a small gift artifact rather than a developer folder?
Was the public/private boundary understandable?
Did anything feel confusing, fragile, or too obscure?
```

## Project

Public repository:

```text
https://github.com/NataliReise/glossai-nexus
```
"""

SHORT_NOTE_FOR_TESTER = """# Short Note for Tester

Thank you for looking at this early First Spark preview package.

This is not a finished large game. It is a small local prototype and the first seed of a possible Nexus gift module.

The current test question is simple:

```text
Can a person receive this as a small standalone Linux-friendly package,
unpack it, start it, understand the flow, and give feedback?
```

Please do not post any private activation data if you create or edit `activation.local.json` while testing.

Useful things to check:

```text
- Does ./START_HERE.sh work?
- Does python3 run_first_spark.py work?
- Is the player README understandable?
- Does the small terminal flow feel coherent?
- Is the public/private boundary clear enough?
- What should be simpler before this becomes a real gift package?
```

The package should remain social-analog:

```text
The artifact may travel digitally.
The resonance should be carried socially.
```
"""

START_HERE = """#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 run_first_spark.py
"""


def should_ignore(path: Path) -> bool:
    """Return whether a file or directory should be excluded from the package."""
    if path.name in PRIVATE_OR_GENERATED_NAMES:
        return True
    return any(path.name.endswith(suffix) for suffix in PRIVATE_OR_GENERATED_SUFFIXES)


def copy_public_tree(source: Path, target: Path) -> None:
    """Copy a public-safe tree while excluding private and generated files."""
    def ignore(directory: str, names: list[str]) -> set[str]:
        directory_path = Path(directory)
        ignored: set[str] = set()
        for name in names:
            if should_ignore(directory_path / name):
                ignored.add(name)
        return ignored

    shutil.copytree(source, target, ignore=ignore)


def write_text_file(path: Path, content: str) -> None:
    """Write UTF-8 text content with a trailing newline."""
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def make_executable(path: Path) -> None:
    """Add user/group/other execute bits to a generated script."""
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def build_package(package_name: str, dist_root: Path, overwrite: bool = False, zip_package: bool = False) -> Path:
    """Build the First Spark standalone package and return its folder path."""
    if not FIRST_SPARK_ROOT.exists():
        raise FileNotFoundError(f"First Spark root not found: {FIRST_SPARK_ROOT}")

    package_dir = dist_root / package_name
    zip_base = dist_root / package_name
    zip_path = zip_base.with_suffix(".zip")

    if package_dir.exists():
        if not overwrite:
            raise FileExistsError(
                f"Package folder already exists: {package_dir}\n"
                "Use --overwrite to rebuild it."
            )
        shutil.rmtree(package_dir)

    if zip_path.exists():
        if not overwrite:
            raise FileExistsError(
                f"Package ZIP already exists: {zip_path}\n"
                "Use --overwrite to rebuild it."
            )
        zip_path.unlink()

    dist_root.mkdir(parents=True, exist_ok=True)
    package_dir.mkdir(parents=True)

    for filename in COPY_FILES:
        source = FIRST_SPARK_ROOT / filename
        if not source.exists():
            raise FileNotFoundError(f"Required package file not found: {source}")
        shutil.copy2(source, package_dir / filename)

    for dirname in COPY_DIRS:
        source = FIRST_SPARK_ROOT / dirname
        if not source.exists():
            raise FileNotFoundError(f"Required package directory not found: {source}")
        copy_public_tree(source, package_dir / dirname)

    write_text_file(package_dir / "README_FOR_PLAYER.md", README_FOR_PLAYER)
    write_text_file(package_dir / "SHORT_NOTE_FOR_TESTER.md", SHORT_NOTE_FOR_TESTER)
    write_text_file(package_dir / "START_HERE.sh", START_HERE)
    make_executable(package_dir / "START_HERE.sh")

    if zip_package:
        shutil.make_archive(str(zip_base), "zip", root_dir=dist_root, base_dir=package_name)

    return package_dir


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Build a standalone Nexus 01 - First Spark preview package."
    )
    parser.add_argument(
        "--package-name",
        default=DEFAULT_PACKAGE_NAME,
        help=f"Package folder name. Default: {DEFAULT_PACKAGE_NAME}",
    )
    parser.add_argument(
        "--dist-root",
        type=Path,
        default=DEFAULT_DIST_ROOT,
        help=f"Output folder. Default: {DEFAULT_DIST_ROOT}",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing package folder or ZIP with the same name.",
    )
    parser.add_argument(
        "--zip",
        action="store_true",
        help="Also create a ZIP archive next to the package folder.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the package builder."""
    args = parse_args()
    package_dir = build_package(
        package_name=args.package_name,
        dist_root=args.dist_root,
        overwrite=args.overwrite,
        zip_package=args.zip,
    )

    print("First Spark preview package created.")
    print()
    print(f"Folder: {package_dir}")
    if args.zip:
        print(f"ZIP:    {(args.dist_root / args.package_name).with_suffix('.zip')}")
    print()
    print("Next test:")
    print(f"cd {package_dir}")
    print("./START_HERE.sh")


if __name__ == "__main__":
    main()
