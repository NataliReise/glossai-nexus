#!/usr/bin/env python3
"""Build a local personal gift package for Nexus 01 - First Spark.

The gift package builder creates a small standalone folder that may include a real
local activation file. It is intentionally local-only: it does not commit, upload,
send, sync, or track anything.
"""

from __future__ import annotations

import argparse
import json
from json import JSONDecodeError
import re
import shutil
import stat
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = SCRIPT_PATH.parents[3]
FIRST_SPARK_ROOT = NEXUS_ROOT / "first_spark"
DEFAULT_DIST_ROOT = REPO_ROOT / "dist"
DEFAULT_GIFT_LABEL = "personal-gift"
PACKAGE_NAME_PREFIX = "nexus-01-first-spark-gift"
LOCAL_ACTIVATION_FILENAME = "activation.local.json"
EXAMPLE_ACTIVATION_FILENAME = "activation.example.json"

COPY_PUBLIC_FILES = (
    "run_first_spark.py",
    EXAMPLE_ACTIVATION_FILENAME,
)

COPY_DIRS = (
    "first_spark",
)

LOCAL_OR_GENERATED_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    LOCAL_ACTIVATION_FILENAME,
    "return_slot.local.json",
    "return_artifact.local.txt",
    "local_result.md",
}

LOCAL_OR_GENERATED_SUFFIXES = (
    ".pyc",
    ".pyo",
    ".local.md",
    ".local.json",
    ".local.txt",
)

README_FOR_RECIPIENT = """# Nexus 01 - First Spark

Welcome to **Nexus 01 - First Spark**.

This is a small local terminal experience from the public **glossai-nexus** project.
This package was created as a personal gift package.

## Start

Open a terminal in this folder and run:

```bash
./START_HERE.sh
```

If that does not work, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 run_first_spark.py
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

## Local activation

This package includes:

```text
activation.local.json
```

That file carries the local activation layer for this copy.

You do not need to edit it in order to play.

## Project

Public repository:

```text
https://github.com/NataliReise/glossai-nexus
```
"""

GIFT_NOTE = """# Personal Gift Package Note

This folder was built locally as a personal First Spark gift package.

It is not an automatically delivered message and it does not track anything.

Working rule:

```text
The artifact may travel digitally.
The resonance should be carried socially.
```
"""

START_HERE = """#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
PYTHONDONTWRITEBYTECODE=1 python3 run_first_spark.py
"""


class GiftPackageError(RuntimeError):
    """Raised when a gift package cannot be built safely."""


def normalize_label(label: str) -> str:
    """Return a filesystem-friendly package label."""
    normalized = label.strip().lower()
    normalized = re.sub(r"[^a-z0-9._-]+", "-", normalized)
    normalized = normalized.strip("-._")
    if not normalized:
        raise GiftPackageError("Gift label must contain at least one letter or number.")
    return normalized


def package_name_from_label(label: str) -> str:
    """Return the default gift package name for a label."""
    return f"{PACKAGE_NAME_PREFIX}-{normalize_label(label)}"


def should_ignore(path: Path) -> bool:
    """Return whether a file or directory should be excluded from the copied tree."""
    if path.name in LOCAL_OR_GENERATED_NAMES:
        return True
    return any(path.name.endswith(suffix) for suffix in LOCAL_OR_GENERATED_SUFFIXES)


def copy_public_tree(source: Path, target: Path) -> None:
    """Copy a public-safe tree while excluding local and generated files."""
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


def validate_local_activation(path: Path) -> None:
    """Require a readable JSON object as local activation data."""
    if not path.exists():
        raise GiftPackageError(
            f"Local activation file not found: {path}\n"
            "Create it first with:\n"
            "python3 modules/nexus_01_nexus_mesomerie/first_spark/create_local_activation.py"
        )

    if not path.is_file():
        raise GiftPackageError(f"Local activation path is not a file: {path}")

    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except JSONDecodeError as error:
        raise GiftPackageError(
            f"Local activation file is not valid JSON near line {error.lineno}, "
            f"column {error.colno}: {error.msg}."
        ) from error

    if not isinstance(data, dict):
        raise GiftPackageError(
            "Local activation file must contain a JSON object at the top level."
        )


def prepare_output_paths(package_name: str, dist_root: Path, overwrite: bool) -> tuple[Path, Path]:
    """Prepare output folder and ZIP path, respecting the overwrite flag."""
    package_dir = dist_root / package_name
    zip_path = (dist_root / package_name).with_suffix(".zip")

    if package_dir.exists():
        if not overwrite:
            raise GiftPackageError(
                f"Gift package folder already exists: {package_dir}\n"
                "Use --overwrite to rebuild it."
            )
        shutil.rmtree(package_dir)

    if zip_path.exists():
        if not overwrite:
            raise GiftPackageError(
                f"Gift package ZIP already exists: {zip_path}\n"
                "Use --overwrite to rebuild it."
            )
        zip_path.unlink()

    dist_root.mkdir(parents=True, exist_ok=True)
    package_dir.mkdir(parents=True)
    return package_dir, zip_path


def copy_gift_files(package_dir: Path, local_activation_path: Path) -> None:
    """Copy the public structure plus the one required local activation file."""
    for filename in COPY_PUBLIC_FILES:
        source = FIRST_SPARK_ROOT / filename
        if not source.exists():
            raise FileNotFoundError(f"Required package file not found: {source}")
        shutil.copy2(source, package_dir / filename)

    for dirname in COPY_DIRS:
        source = FIRST_SPARK_ROOT / dirname
        if not source.exists():
            raise FileNotFoundError(f"Required package directory not found: {source}")
        copy_public_tree(source, package_dir / dirname)

    shutil.copy2(local_activation_path, package_dir / LOCAL_ACTIVATION_FILENAME)


def build_gift_package(
    package_name: str,
    dist_root: Path,
    local_activation_path: Path,
    overwrite: bool = False,
    zip_package: bool = False,
) -> Path:
    """Build the First Spark personal gift package and return its folder path."""
    if not FIRST_SPARK_ROOT.exists():
        raise FileNotFoundError(f"First Spark root not found: {FIRST_SPARK_ROOT}")

    validate_local_activation(local_activation_path)
    package_dir, zip_path = prepare_output_paths(package_name, dist_root, overwrite)
    copy_gift_files(package_dir, local_activation_path)

    write_text_file(package_dir / "README_FOR_RECIPIENT.md", README_FOR_RECIPIENT)
    write_text_file(package_dir / "GIFT_NOTE.md", GIFT_NOTE)
    write_text_file(package_dir / "START_HERE.sh", START_HERE)
    make_executable(package_dir / "START_HERE.sh")

    if zip_package:
        shutil.make_archive(
            str(zip_path.with_suffix("")),
            "zip",
            root_dir=dist_root,
            base_dir=package_name,
        )

    return package_dir


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Build a local Nexus 01 - First Spark personal gift package."
    )
    parser.add_argument(
        "--gift-label",
        default=DEFAULT_GIFT_LABEL,
        help=f"Local gift label for the package name. Default: {DEFAULT_GIFT_LABEL}",
    )
    parser.add_argument(
        "--package-name",
        default=None,
        help="Explicit package folder name. Overrides --gift-label if set.",
    )
    parser.add_argument(
        "--dist-root",
        type=Path,
        default=DEFAULT_DIST_ROOT,
        help=f"Output folder. Default: {DEFAULT_DIST_ROOT}",
    )
    parser.add_argument(
        "--local-activation",
        type=Path,
        default=FIRST_SPARK_ROOT / LOCAL_ACTIVATION_FILENAME,
        help="Path to activation.local.json. Default: First Spark local activation path.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing gift package folder or ZIP with the same name.",
    )
    parser.add_argument(
        "--zip",
        action="store_true",
        help="Also create a ZIP archive next to the gift package folder.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the gift package builder."""
    args = parse_args()
    package_name = args.package_name or package_name_from_label(args.gift_label)

    try:
        package_dir = build_gift_package(
            package_name=package_name,
            dist_root=args.dist_root,
            local_activation_path=args.local_activation,
            overwrite=args.overwrite,
            zip_package=args.zip,
        )
    except (GiftPackageError, OSError) as error:
        print("First Spark gift package could not be created.")
        print()
        print(error)
        return 1

    print("First Spark gift package created.")
    print()
    print(f"Folder: {package_dir}")
    if args.zip:
        print(f"ZIP:    {(args.dist_root / package_name).with_suffix('.zip')}")
    print()
    print("Manual next steps:")
    print(f"cd {package_dir}")
    print("./START_HERE.sh")
    print()
    print("Share the folder or ZIP manually only after reviewing it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
