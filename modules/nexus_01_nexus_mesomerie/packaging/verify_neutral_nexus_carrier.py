#!/usr/bin/env python3
"""Independently verify a corrected activation-ready Nexus 01 carrier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import zipfile


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from return_resonance.token import (  # noqa: E402
    ResonanceTokenLoadError,
    parse_resonance_token,
)


SIDECAR_PATH = Path("invitation/resonance_token.v2.json")
START_PATH = Path("START_HERE.sh")
README_PATH = Path("README_FOR_RECIPIENT.md")

START_SCRIPT = r'''#!/usr/bin/env bash
set -euo pipefail

CARRIER_ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$CARRIER_ROOT"

PYTHON_BIN="${NEXUS_PYTHON:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python 3.11 or newer is required, but '$PYTHON_BIN' was not found." >&2
  exit 2
fi
if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
  echo "Python 3.11 or newer is required." >&2
  exit 2
fi

PYTHONDONTWRITEBYTECODE=1 "$PYTHON_BIN" run_nexus.py
'''

NEUTRAL_RUNTIME_FILES = frozenset(
    {
        Path("run_nexus.py"),
        Path("recipient_activation.py"),
        Path("resonance_invitation_runtime.py"),
        Path("open_resonance_return.py"),
        *(Path("atrium") / name for name in (
            "__init__.py", "activation_bridge.py", "classified_resonance.py",
            "first_spark_adapter.py", "known_source.py", "profiles.py",
            "resonance_adapter.py", "resonance_mode.py", "resonance_terminal.py",
            "runtime.py", "stable_result.py", "state.py", "terminal.py",
        )),
        *(Path("chambers/resonance") / name for name in (
            "__init__.py", "choices.py", "compose.py", "composer.py", "flow.py",
            "terminal_io.py",
        )),
        Path("first_spark/run_first_spark.py"),
        Path("first_spark/activation.example.json"),
        *(Path("first_spark/first_spark") / name for name in (
            "__init__.py", "activation.py", "command_feedback.py", "config.py",
            "guidance.py", "module_response.py", "runtime.py", "state.py",
        )),
        *(Path("first_spark/first_spark/game_modules") / name for name in (
            "__init__.py", "arrival.py", "ending.py", "spark_chamber.py",
        )),
        *(Path("return_resonance") / name for name in (
            "__init__.py", "artifact.py", "artifact_store.py",
            "compact_generator.py", "local_opening.py",
            "matching.py", "resonance_render_bridge.py", "result.py", "slots.py",
            "token.py", "writer.py",
        )),
        *(Path("resonance_language_library") / name for name in (
            "render_nexus_echo.py", "render_resonance_artifact.py",
            "render_resonance_output.py",
        )),
        *(Path("resonance_language_library/v0_1") / name for name in (
            "echo_paths.json", "image_responses.json", "images.json",
            "movement_responses.json", "movements.json", "scent_responses.json",
            "scents.json",
        )),
    }
)
GENERATED_FILES = frozenset({START_PATH, README_PATH})

FORBIDDEN_NAMES = frozenset(
    {
        "activation.local.json",
        "activation.local.resonance-context.json",
        "resonance_token.local.json",
        "return_slots.local.json",
        "return_slot.local.json",
        "resonance_return.local.json",
        "return_artifact.local.json",
        "return_artifact.local.txt",
        "return_result.local.md",
        "local_result.md",
        "OPEN_RETURN.sh",
    }
)
FORBIDDEN_PARTS = frozenset(
    {
        ".git", "__pycache__", ".pytest_cache", "archive", "demos",
        "examples", "experiments", "incoming", "packaging", "private",
        "results", "tests",
    }
)
MACHINE_PATH_PATTERN = re.compile(r"(?:/home/|/Users/|[A-Za-z]:\\\\)")


@dataclass
class CarrierVerificationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def add_error(self, message: str) -> None:
        self.errors.append(message)


def verify_carrier(
    carrier_dir: Path,
    expected_token_source: Path | None = None,
) -> CarrierVerificationResult:
    """Verify one directory carrier without changing it."""

    result = CarrierVerificationResult()
    if not carrier_dir.is_dir():
        result.add_error(f"Neutral Nexus Carrier is not a directory: {carrier_dir}")
        return result

    for path in (carrier_dir, *carrier_dir.rglob("*")):
        if path.is_symlink():
            result.add_error(
                f"Symbolic links are not allowed: {path.relative_to(carrier_dir)}"
            )

    sidecar_present = (carrier_dir / SIDECAR_PATH).is_file()
    allowed_files = NEUTRAL_RUNTIME_FILES | GENERATED_FILES
    if sidecar_present:
        allowed_files |= {SIDECAR_PATH}
    actual_files = {
        path.relative_to(carrier_dir)
        for path in carrier_dir.rglob("*")
        if path.is_file()
    }
    for missing in sorted(allowed_files - actual_files, key=str):
        result.add_error(f"Missing carrier file: {missing}")
    for unexpected in sorted(actual_files - allowed_files, key=str):
        result.add_error(f"Unexpected file outside carrier allowlist: {unexpected}")

    allowed_dirs = {
        parent
        for path in allowed_files
        for parent in path.parents
        if parent != Path(".")
    }
    actual_dirs = {
        path.relative_to(carrier_dir)
        for path in carrier_dir.rglob("*")
        if path.is_dir()
    }
    for unexpected in sorted(actual_dirs - allowed_dirs, key=str):
        result.add_error(f"Unexpected directory outside carrier allowlist: {unexpected}")

    _verify_forbidden_content(carrier_dir, result)
    _verify_launcher(carrier_dir, result)
    _verify_readme(carrier_dir, result)
    _verify_sidecar(carrier_dir, expected_token_source, result)
    _verify_runtime_import(carrier_dir, result)
    return result


def verify_carrier_zip(
    zip_path: Path,
    expected_token_source: Path | None = None,
) -> CarrierVerificationResult:
    """Verify a ZIP by checking safe members and its extracted carrier."""

    result = CarrierVerificationResult()
    if not zip_path.is_file():
        result.add_error(f"Neutral Nexus Carrier ZIP is missing: {zip_path}")
        return result
    try:
        with zipfile.ZipFile(zip_path) as archive:
            members = [name for name in archive.namelist() if not name.endswith("/")]
            unsafe = [
                name
                for name in members
                if (
                    Path(name).is_absolute()
                    or ".." in Path(name).parts
                    or "\\" in name
                    or re.match(r"[A-Za-z]:", name)
                )
            ]
            roots = {Path(name).parts[0] for name in members if Path(name).parts}
            if unsafe:
                result.add_error("Carrier ZIP contains an unsafe member path")
                return result
            if len(roots) != 1:
                result.add_error("Carrier ZIP must contain exactly one top-level folder")
                return result
            root_name = next(iter(roots))
            if any(
                stat.S_ISLNK(info.external_attr >> 16)
                for info in archive.infolist()
            ):
                result.add_error("Carrier ZIP must not contain symbolic links")
                return result
            launcher_member = f"{root_name}/{START_PATH.as_posix()}"
            try:
                launcher_info = archive.getinfo(launcher_member)
            except KeyError:
                result.add_error("Carrier ZIP is missing START_HERE.sh")
                return result
            archived_mode = launcher_info.external_attr >> 16
            if not archived_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                result.add_error("Carrier ZIP does not preserve launcher execute permission")
                return result
            with tempfile.TemporaryDirectory() as directory:
                archive.extractall(directory)
                extracted = Path(directory) / root_name
                extracted_launcher = extracted / START_PATH
                extracted_launcher.chmod(
                    extracted_launcher.stat().st_mode
                    | stat.S_IXUSR
                    | stat.S_IXGRP
                    | stat.S_IXOTH
                )
                nested = verify_carrier(extracted, expected_token_source)
    except (OSError, zipfile.BadZipFile) as error:
        result.add_error(f"Carrier ZIP could not be read: {error}")
        return result
    result.errors.extend(nested.errors)
    return result


def _verify_forbidden_content(
    carrier_dir: Path, result: CarrierVerificationResult
) -> None:
    for path in carrier_dir.rglob("*"):
        relative = path.relative_to(carrier_dir)
        folded_parts = {part.casefold() for part in relative.parts}
        if path.name in FORBIDDEN_NAMES:
            result.add_error(f"Forbidden local or private file found: {relative}")
        if FORBIDDEN_PARTS.intersection(folded_parts):
            result.add_error(f"Forbidden private or development path found: {relative}")
        if path.suffix.casefold() in {".pyc", ".pyo"}:
            result.add_error(f"Python cache file found: {relative}")
        if path.is_file() and path.suffix.casefold() in {".py", ".sh", ".json"}:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                result.add_error(f"Carrier text file is not readable UTF-8: {relative}: {error}")
                continue
            if MACHINE_PATH_PATTERN.search(text):
                result.add_error(f"Machine-specific absolute path found: {relative}")


def _verify_launcher(carrier_dir: Path, result: CarrierVerificationResult) -> None:
    launcher = carrier_dir / START_PATH
    if not launcher.is_file():
        return
    if not launcher.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
        result.add_error("START_HERE.sh is not executable")
    try:
        text = launcher.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return
    for fragment in (
        'BASH_SOURCE[0]',
        'cd "$CARRIER_ROOT"',
        "sys.version_info >= (3, 11)",
        '"$PYTHON_BIN" run_nexus.py',
    ):
        if fragment not in text:
            result.add_error(f"START_HERE.sh is missing corrected launcher logic: {fragment}")
    if "--legacy-preactivated" in text:
        result.add_error("Neutral carrier launcher must not request legacy activation")
    if text.rstrip() != START_SCRIPT.rstrip():
        result.add_error("START_HERE.sh differs from the verified neutral launcher")


def _verify_readme(carrier_dir: Path, result: CarrierVerificationResult) -> None:
    readme = carrier_dir / README_PATH
    if not readme.is_file():
        return
    try:
        text = readme.read_text(encoding="utf-8").casefold()
    except (OSError, UnicodeError) as error:
        result.add_error(f"Carrier README is not readable UTF-8: {error}")
        return
    for phrase in (
        "activation-ready",
        "recipient chooses",
        "only an invitation",
        "normal activation leaves",
        "deliberately select",
        "private return workspace",
        "manual",
    ):
        if phrase not in text:
            result.add_error(f"Carrier README is missing recipient guidance: {phrase}")


def _verify_sidecar(
    carrier_dir: Path,
    expected_token_source: Path | None,
    result: CarrierVerificationResult,
) -> None:
    sidecar = carrier_dir / SIDECAR_PATH
    if not sidecar.exists():
        if expected_token_source is not None:
            result.add_error("Expected Token V2 sidecar is missing")
        return
    try:
        sidecar_bytes = sidecar.read_bytes()
        data = json.loads(sidecar_bytes.decode("utf-8"))
        token = parse_resonance_token(data)
    except (OSError, UnicodeError, ValueError, ResonanceTokenLoadError) as error:
        result.add_error(f"Optional Token sidecar failed strict validation: {error}")
        return
    if token.is_legacy or not token.has_originating_contribution:
        result.add_error("Optional carrier invitation must be Resonance Token V2")
    if expected_token_source is not None:
        try:
            expected_bytes = expected_token_source.read_bytes()
        except OSError as error:
            result.add_error(f"Expected Token source could not be read: {error}")
        else:
            if sidecar_bytes != expected_bytes:
                result.add_error("Optional Token sidecar is not byte-identical to its source")


def _verify_runtime_import(
    carrier_dir: Path, result: CarrierVerificationResult
) -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        check = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                "-c",
                (
                    "import sys; sys.path.insert(0, '.'); "
                    "import run_nexus; run_nexus.main(['--help'])"
                ),
            ],
            cwd=carrier_dir,
            env=environment,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        result.add_error(f"Carrier runtime import preflight could not run: {error}")
        return
    if check.returncode != 0:
        detail = (check.stderr or check.stdout).strip().splitlines()[-1:]
        result.add_error(
            "Corrected carrier runtime cannot import in isolation"
            + (f": {detail[0]}" if detail else "")
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify a Neutral Nexus Carrier.")
    parser.add_argument("carrier", type=Path)
    parser.add_argument("--zip", action="store_true", dest="is_zip")
    parser.add_argument("--token-source", type=Path)
    args = parser.parse_args(argv)
    result = (
        verify_carrier_zip(args.carrier, args.token_source)
        if args.is_zip
        else verify_carrier(args.carrier, args.token_source)
    )
    if result.passed:
        print("Neutral Nexus Carrier verification passed.")
        print(f"Carrier: {args.carrier}")
        return 0
    print("Neutral Nexus Carrier verification failed.")
    for error in result.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
