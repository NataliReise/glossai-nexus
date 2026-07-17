"""Build one private giver-side Return Workspace from explicit local data."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import stat


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
SLOT_PATH = Path("private/return_slots.local.json")

RUNTIME_SOURCE_FILES = frozenset(
    {
        Path("open_resonance_return.py"),
        *(Path("return_resonance") / name for name in (
            "__init__.py",
            "artifact.py",
            "artifact_store.py",
            "compact_generator.py",
            "local_opening.py",
            "matching.py",
            "resonance_render_bridge.py",
            "result.py",
            "slots.py",
            "token.py",
            "writer.py",
        )),
        *(Path("resonance_language_library") / name for name in (
            "render_nexus_echo.py",
            "render_resonance_artifact.py",
            "render_resonance_output.py",
        )),
    }
)
RUNTIME_FILES = frozenset(Path("runtime") / path for path in RUNTIME_SOURCE_FILES)

OPEN_RETURN_SCRIPT = r'''#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$WORKSPACE_ROOT"

PYTHON_BIN="${NEXUS_PYTHON:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python 3.11 or newer is required, but '$PYTHON_BIN' was not found." >&2
  exit 2
fi
if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
  PYTHON_VERSION="$($PYTHON_BIN -c 'import sys; print(".".join(map(str, sys.version_info[:3])))' 2>/dev/null || true)"
  echo "Python 3.11 or newer is required. Found: ${PYTHON_VERSION:-unknown}." >&2
  exit 2
fi

if (( $# > 1 )); then
  echo "Usage: ./OPEN_RETURN.sh [ARTIFACT.json]" >&2
  exit 2
fi

if (( $# == 1 )); then
  ARTIFACT_PATH="$1"
else
  shopt -s nullglob
  ARTIFACTS=(incoming/*.json)
  shopt -u nullglob
  if (( ${#ARTIFACTS[@]} == 0 )); then
    echo "No Return Artifact JSON file was found in incoming/." >&2
    echo "Copy the manually returned Artifact into incoming/ and run this command again." >&2
    exit 1
  fi
  if (( ${#ARTIFACTS[@]} > 1 )); then
    echo "Multiple Return Artifact JSON files were found in incoming/:" >&2
    printf '  %s\n' "${ARTIFACTS[@]}" >&2
    echo "Refusing ambiguous automatic selection. Pass one Artifact path explicitly." >&2
    exit 1
  fi
  ARTIFACT_PATH="${ARTIFACTS[0]}"
fi

if [[ ! -f "$ARTIFACT_PATH" || -L "$ARTIFACT_PATH" ]]; then
  echo "Return Artifact is not a safe regular file: $ARTIFACT_PATH" >&2
  exit 1
fi

PYTHONDONTWRITEBYTECODE=1 "$PYTHON_BIN" runtime/open_resonance_return.py \
  --artifact "$ARTIFACT_PATH" \
  --slots private/return_slots.local.json \
  --output-dir results
'''

WORKSPACE_README = """# Nexus 01 Private Return Workspace

This folder is private. **Do not send it with the travelling gift.**

1. Wait for the Return Artifact to be transferred back manually, for example by
   USB drive, email attachment, or another deliberate file handoff.
2. Copy the returned JSON file into `incoming/`.
3. Run `./OPEN_RETURN.sh`. You may instead pass one Artifact path explicitly.
4. The compact result is created once in `results/` and reused unchanged later.
5. Manual edits to the saved result are preserved when it is reopened.

Do not edit or share `private/return_slots.local.json`. It is the private waiting
place that matches this gift. Back up this whole workspace if the return matters.

No automatic communication, upload, cloud transport, sending, or synchronization
occurs. The Artifact must always be transferred by a person deliberately.

Python 3.11 or newer and a Bash-compatible terminal are required.
"""


class ReturnWorkspaceBuildError(RuntimeError):
    """Raised when a staged private Return Workspace cannot be built safely."""


def workspace_name(return_slot_id: str) -> str:
    prefix = "n01-slot-"
    opaque_id = return_slot_id.removeprefix(prefix)
    if not opaque_id or not all(
        character.isascii() and (character.isalnum() or character in "._-")
        for character in opaque_id
    ):
        raise ReturnWorkspaceBuildError("Return Slot ID cannot form a safe workspace name")
    return f"n01-return-workspace-{opaque_id}"


def build_return_workspace(
    workspace_dir: Path,
    slot_document: dict[str, object],
) -> Path:
    """Build a new staged workspace without reading private activation data."""

    if workspace_dir.exists():
        raise ReturnWorkspaceBuildError(
            f"Refusing to replace existing staged workspace: {workspace_dir}"
        )
    workspace_dir.mkdir(parents=True)
    for directory in ("incoming", "results", "private", "runtime"):
        (workspace_dir / directory).mkdir()

    for source_relative in sorted(RUNTIME_SOURCE_FILES, key=str):
        source = NEXUS_ROOT / source_relative
        if not source.is_file():
            raise ReturnWorkspaceBuildError(f"Required opening runtime file is missing: {source}")
        target = workspace_dir / "runtime" / source_relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    _write_text(workspace_dir / "OPEN_RETURN.sh", OPEN_RETURN_SCRIPT)
    _make_executable(workspace_dir / "OPEN_RETURN.sh")
    _write_text(workspace_dir / "README.md", WORKSPACE_README)
    (workspace_dir / SLOT_PATH).write_text(
        json.dumps(slot_document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return workspace_dir


def _write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
