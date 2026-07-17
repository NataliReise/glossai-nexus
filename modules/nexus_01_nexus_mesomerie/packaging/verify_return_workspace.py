#!/usr/bin/env python3
"""Independently verify a private Nexus 01 giver-side Return Workspace."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from return_resonance.slots import (  # noqa: E402
    ReturnSlotLoadError,
    load_return_slots,
)
from return_resonance.token import (  # noqa: E402
    LAYER_ID,
    MODULE_ID,
    ResonanceTokenLoadError,
    load_resonance_token,
)
from return_workspace import OPEN_RETURN_SCRIPT, RUNTIME_FILES, SLOT_PATH  # noqa: E402
from verify_resonance_gift_package import TOKEN_PATH, verify_package  # noqa: E402


EXPECTED_ROOT_ENTRIES = frozenset(
    {Path("OPEN_RETURN.sh"), Path("README.md"), Path("incoming"), Path("results"), Path("private"), Path("runtime")}
)
EXPECTED_PRIVATE_FILES = frozenset({SLOT_PATH})
FORBIDDEN_PARTS = frozenset(
    {
        ".git", "__pycache__", ".pytest_cache", "activation", "archive", "atrium",
        "chambers", "demos", "demo", "examples", "experiments", "first_spark",
        "packaging", "tests",
    }
)
FORBIDDEN_NAMES = frozenset(
    {
        "activation.local.json",
        "resonance_token.local.json",
        "COMPACT_GENERATOR_REVIEW_CORPUS.md",
    }
)
_SAFE_RESULT_FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}")
_WINDOWS_RESERVED_STEMS = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


@dataclass
class VerificationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def add_error(self, message: str) -> None:
        self.errors.append(message)


def is_safe_result_filename(value: str) -> bool:
    path = Path(value)
    stem = path.name.split(".", 1)[0].upper()
    return bool(
        value
        and not path.is_absolute()
        and path.name == value
        and "/" not in value
        and "\\" not in value
        and ".." not in value
        and _SAFE_RESULT_FILENAME.fullmatch(value)
        and not value.endswith((".", " "))
        and stem not in _WINDOWS_RESERVED_STEMS
    )


def verify_workspace(
    workspace_dir: Path,
    expected_identity: dict[str, str] | None = None,
    gift_dir: Path | None = None,
) -> VerificationResult:
    result = VerificationResult()
    if not workspace_dir.is_dir():
        result.add_error(f"Return Workspace does not exist or is not a directory: {workspace_dir}")
        return result

    _verify_no_symlinks(workspace_dir, result)
    actual_root = {path.relative_to(workspace_dir) for path in workspace_dir.iterdir()}
    for missing in sorted(EXPECTED_ROOT_ENTRIES - actual_root, key=str):
        result.add_error(f"Missing workspace entry: {missing}")
    for unexpected in sorted(actual_root - EXPECTED_ROOT_ENTRIES, key=str):
        result.add_error(f"Unexpected workspace root entry: {unexpected}")

    _verify_static_files(workspace_dir, result)
    slots = _verify_slot(workspace_dir, expected_identity, result)
    _verify_incoming(workspace_dir, result)
    _verify_results(workspace_dir, slots, result)
    _verify_runtime(workspace_dir, result)
    _verify_forbidden_content(workspace_dir, result)
    if gift_dir is not None:
        _verify_gift_separation(gift_dir, slots, result)
    return result


def _verify_gift_separation(
    gift_dir: Path,
    slots: list[object],
    result: VerificationResult,
) -> None:
    gift_verification = verify_package(gift_dir)
    for error in gift_verification.errors:
        result.add_error(f"Travelling/private separation failed: {error}")
    if len(slots) != 1:
        return
    try:
        token = load_resonance_token(gift_dir / TOKEN_PATH)
    except ResonanceTokenLoadError:
        return
    slot = slots[0]
    for field_name in (
        "module_id", "layer_id", "origin_trace_id", "return_slot_id", "package_id"
    ):
        if getattr(token, field_name) != getattr(slot, field_name, None):
            result.add_error(
                f"Travelling gift and retained slot disagree on {field_name}"
            )


def _verify_no_symlinks(workspace_dir: Path, result: VerificationResult) -> None:
    for path in (workspace_dir, *workspace_dir.rglob("*")):
        if path.is_symlink():
            result.add_error(f"Symbolic links are not allowed in a Return Workspace: {path.relative_to(workspace_dir)}")


def _verify_static_files(workspace_dir: Path, result: VerificationResult) -> None:
    launcher = workspace_dir / "OPEN_RETURN.sh"
    readme = workspace_dir / "README.md"
    if not launcher.is_file():
        result.add_error("OPEN_RETURN.sh is missing")
    else:
        if not launcher.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
            result.add_error("OPEN_RETURN.sh is not executable")
        try:
            content = launcher.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            result.add_error(f"OPEN_RETURN.sh is not readable UTF-8 text: {error}")
            content = ""
        required_fragments = (
            'BASH_SOURCE[0]',
            'cd "$WORKSPACE_ROOT"',
            "sys.version_info >= (3, 11)",
            "incoming/*.json",
            "private/return_slots.local.json",
            '--artifact "$ARTIFACT_PATH"',
            "--slots private/return_slots.local.json",
            "--output-dir results",
        )
        for fragment in required_fragments:
            if fragment not in content:
                result.add_error(f"OPEN_RETURN.sh is missing required relative launcher logic: {fragment}")
        if re.search(r"(?:/home/|/Users/|[A-Za-z]:\\\\)", content):
            result.add_error("OPEN_RETURN.sh contains a machine-specific absolute path")
        if content.rstrip() != OPEN_RETURN_SCRIPT.rstrip():
            result.add_error("OPEN_RETURN.sh differs from the verified package-relative launcher")

    if not readme.is_file():
        result.add_error("README.md is missing")
    else:
        try:
            content = readme.read_text(encoding="utf-8").casefold()
        except (OSError, UnicodeError) as error:
            result.add_error(f"README.md is not readable UTF-8 text: {error}")
            content = ""
        for phrase in (
            "do not send it with the travelling gift",
            "incoming/",
            "manual edits",
            "private/return_slots.local.json",
            "back up",
            "no automatic communication",
        ):
            if phrase not in content:
                result.add_error(f"README.md is missing giver guidance: {phrase}")


def _verify_slot(
    workspace_dir: Path,
    expected_identity: dict[str, str] | None,
    result: VerificationResult,
) -> list[object]:
    private_dir = workspace_dir / "private"
    if private_dir.is_dir():
        actual = {path.relative_to(workspace_dir) for path in private_dir.rglob("*") if path.is_file()}
        for unexpected in sorted(actual - EXPECTED_PRIVATE_FILES, key=str):
            result.add_error(f"Unexpected private workspace file: {unexpected}")
    slot_path = workspace_dir / SLOT_PATH
    try:
        slots = load_return_slots(slot_path)
    except (ReturnSlotLoadError, OSError, UnicodeError) as error:
        result.add_error(f"Retained Return Slot failed validation: {error}")
        return []
    if len(slots) != 1:
        result.add_error("Return Workspace must contain exactly one retained slot")
        return slots
    slot = slots[0]
    if slot.module_id != MODULE_ID or slot.layer_id != LAYER_ID:
        result.add_error("Retained slot uses an unsupported module_id or layer_id")
    if not is_safe_result_filename(slot.result_file):
        result.add_error("Retained slot result_file is not one plain safe relative filename")
    if expected_identity is not None:
        for field_name, expected in expected_identity.items():
            if getattr(slot, field_name, None) != expected:
                result.add_error(f"Retained slot disagrees with expected {field_name}")
    return slots


def _verify_incoming(workspace_dir: Path, result: VerificationResult) -> None:
    incoming = workspace_dir / "incoming"
    if not incoming.is_dir():
        return
    for path in incoming.iterdir():
        if not path.is_file() or path.is_symlink() or path.suffix.casefold() != ".json":
            result.add_error(f"incoming/ contains a non-Artifact candidate: {path.name}")


def _verify_results(workspace_dir: Path, slots: list[object], result: VerificationResult) -> None:
    results_dir = workspace_dir / "results"
    if not results_dir.is_dir():
        return
    allowed = {getattr(slot, "result_file", "") for slot in slots}
    for path in results_dir.iterdir():
        if not path.is_file() or path.is_symlink() or path.name not in allowed:
            result.add_error(f"results/ contains an unrelated result target: {path.name}")


def _verify_runtime(workspace_dir: Path, result: VerificationResult) -> None:
    runtime = workspace_dir / "runtime"
    if not runtime.is_dir():
        return
    actual = {path.relative_to(workspace_dir) for path in runtime.rglob("*") if path.is_file()}
    for missing in sorted(RUNTIME_FILES - actual, key=str):
        result.add_error(f"Missing opening runtime file: {missing}")
    for unexpected in sorted(actual - RUNTIME_FILES, key=str):
        result.add_error(f"Unexpected file outside opening runtime allowlist: {unexpected}")
    if RUNTIME_FILES - actual or actual - RUNTIME_FILES:
        return
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        check = subprocess.run(
            [
                sys.executable,
                "-I",
                "-c",
                (
                    "import sys; "
                    "sys.dont_write_bytecode = True; "
                    "sys.path.insert(0, '.'); "
                    "import open_resonance_return"
                ),
            ],
            cwd=runtime,
            env=environment,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        result.add_error(f"Opening runtime import preflight could not run: {error}")
        return
    if check.returncode != 0:
        detail = (check.stderr or check.stdout).strip().splitlines()[-1:]
        result.add_error(
            "Opening runtime cannot be imported in isolation"
            + (f": {detail[0]}" if detail else "")
        )


def _verify_forbidden_content(workspace_dir: Path, result: VerificationResult) -> None:
    for path in workspace_dir.rglob("*"):
        relative = path.relative_to(workspace_dir)
        folded_parts = {part.casefold() for part in relative.parts}
        if path.name in FORBIDDEN_NAMES:
            result.add_error(f"Forbidden travelling or development file found: {relative}")
        if FORBIDDEN_PARTS.intersection(folded_parts):
            result.add_error(f"Forbidden development path found: {relative}")
        if path.suffix.casefold() in {".pyc", ".pyo"}:
            result.add_error(f"Python cache file found: {relative}")
        if "corpus" in path.name.casefold():
            result.add_error(f"Review corpus file found: {relative}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify a Nexus 01 private Return Workspace.")
    parser.add_argument("workspace_dir", type=Path)
    parser.add_argument(
        "--gift",
        type=Path,
        help="Also verify route consistency and private-data separation from this gift.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = verify_workspace(args.workspace_dir, gift_dir=args.gift)
    if result.passed:
        print("Private Return Workspace verification passed.")
        print(f"Workspace: {args.workspace_dir}")
        return 0
    print("Private Return Workspace verification failed.")
    for error in result.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
