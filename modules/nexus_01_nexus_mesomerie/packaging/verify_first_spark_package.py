#!/usr/bin/env python3
"""Verify a standalone Nexus 01 - First Spark preview package.

The verifier checks that a built preview package contains the expected public
handoff files and does not contain private local files, generated result files,
Git metadata, Python bytecode, or cache folders.
"""

from __future__ import annotations

import argparse
import fnmatch
import stat
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[3]
DEFAULT_PACKAGE_NAME = "nexus-01-first-spark-preview"
DEFAULT_PACKAGE_DIR = REPO_ROOT / "dist" / DEFAULT_PACKAGE_NAME

REQUIRED_FILES = (
    "START_HERE.sh",
    "README_FOR_PLAYER.md",
    "SHORT_NOTE_FOR_TESTER.md",
    "run_first_spark.py",
    "create_local_activation.py",
    "activation.example.json",
)

REQUIRED_DIRS = (
    "first_spark",
)

FORBIDDEN_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "activation.local.json",
    "return_slot.local.json",
    "return_artifact.local.txt",
    "local_result.md",
}

FORBIDDEN_PATTERNS = (
    "*.pyc",
    "*.pyo",
    "*.local.json",
    "*.local.txt",
    "*.local.md",
)


class VerificationResult:
    """Collect package verification errors."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    def add_error(self, message: str) -> None:
        """Record one verification error."""
        self.errors.append(message)

    @property
    def passed(self) -> bool:
        """Return whether no verification errors were found."""
        return not self.errors


def is_forbidden(path: Path) -> bool:
    """Return whether a path is private, generated, or otherwise unsafe."""
    if path.name in FORBIDDEN_NAMES:
        return True
    return any(fnmatch.fnmatch(path.name, pattern) for pattern in FORBIDDEN_PATTERNS)


def is_executable(path: Path) -> bool:
    """Return whether at least one execute bit is set on a file."""
    mode = path.stat().st_mode
    execute_bits = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    return bool(mode & execute_bits)


def verify_required_items(package_dir: Path, result: VerificationResult) -> None:
    """Check that required package files and folders exist."""
    for relative_path in REQUIRED_FILES:
        path = package_dir / relative_path
        if not path.is_file():
            result.add_error(f"Missing required file: {relative_path}")

    for relative_path in REQUIRED_DIRS:
        path = package_dir / relative_path
        if not path.is_dir():
            result.add_error(f"Missing required directory: {relative_path}/")


def verify_forbidden_items(package_dir: Path, result: VerificationResult) -> None:
    """Check that private or generated files are not present."""
    for path in package_dir.rglob("*"):
        if is_forbidden(path):
            result.add_error(f"Forbidden item found: {path.relative_to(package_dir)}")


def verify_start_script(package_dir: Path, result: VerificationResult) -> None:
    """Check that START_HERE.sh is present and executable."""
    start_script = package_dir / "START_HERE.sh"
    if not start_script.exists():
        return
    if not start_script.is_file():
        result.add_error("START_HERE.sh exists but is not a regular file")
        return
    if not is_executable(start_script):
        result.add_error("START_HERE.sh is not executable")


def verify_package(package_dir: Path) -> VerificationResult:
    """Verify a First Spark preview package folder."""
    result = VerificationResult()

    if not package_dir.exists():
        result.add_error(f"Package directory does not exist: {package_dir}")
        return result

    if not package_dir.is_dir():
        result.add_error(f"Package path is not a directory: {package_dir}")
        return result

    verify_required_items(package_dir, result)
    verify_forbidden_items(package_dir, result)
    verify_start_script(package_dir, result)
    return result


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Verify a standalone Nexus 01 - First Spark preview package."
    )
    parser.add_argument(
        "package_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_PACKAGE_DIR,
        help=f"Package folder to verify. Default: {DEFAULT_PACKAGE_DIR}",
    )
    return parser.parse_args()


def main() -> int:
    """Run the package verifier."""
    args = parse_args()
    package_dir = args.package_dir
    result = verify_package(package_dir)

    if result.passed:
        print("First Spark package verification passed.")
        print(f"Checked: {package_dir}")
        return 0

    print("First Spark package verification failed.")
    print(f"Checked: {package_dir}")
    print()
    for error in result.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
