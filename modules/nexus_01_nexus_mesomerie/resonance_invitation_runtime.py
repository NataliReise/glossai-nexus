"""Packageable publication boundary for one inert Resonance invitation.

This module creates two strictly separate local outputs after explicit caller
confirmation: a travelling Token V2 invitation and a private Return Workspace.
It never activates a Nexus, creates a Return Artifact, or transports files.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile

from return_resonance.slots import load_return_slots
from return_resonance.token import (
    LAYER_ID,
    MODULE_ID,
    ResonanceToken,
    ResonanceTokenLoadError,
    load_resonance_token,
    parse_resonance_token,
)


NEXUS_ROOT = Path(__file__).resolve().parent
TOKEN_PATH = Path("resonance_token.local.json")
INVITATION_README_PATH = Path("README.md")
WORKSPACE_SLOT_PATH = Path("private/return_slots.local.json")
SLOT_NOTE = "origin_trace_id identifies a local resonance arc, not a person"

WORKSPACE_RUNTIME_SOURCE_FILES = frozenset(
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
WORKSPACE_RUNTIME_FILES = frozenset(
    Path("runtime") / path for path in WORKSPACE_RUNTIME_SOURCE_FILES
)

INVITATION_README = """# Nexus 01 Resonance Invitation

This folder carries an **optional invitation** created in the shared Resonance
Chamber. It does not activate a Nexus merely by being present.

Pass this folder manually alongside a Nexus 01 module. The recipient chooses
whether to activate normally or deliberately accept this Token later. Nothing
is uploaded, sent, synchronized, consumed, or changed automatically.
"""

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

_SAFE_RESULT_FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}")
_WINDOWS_RESERVED_STEMS = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


class InvitationPublicationError(RuntimeError):
    """Raised when both outputs cannot be safely validated and published."""


@dataclass(frozen=True)
class RouteIdentity:
    module_id: str
    layer_id: str
    origin_trace_id: str
    return_slot_id: str
    package_id: str


@dataclass(frozen=True)
class InvitationPreparationResult:
    invitation_path: Path
    private_workspace_path: Path
    private_slot_path: Path
    token: ResonanceToken


def generate_route_identity() -> RouteIdentity:
    """Generate one opaque public-safe route without personal input."""

    route_key = secrets.token_hex(12)
    return RouteIdentity(
        module_id=MODULE_ID,
        layer_id=LAYER_ID,
        origin_trace_id=f"n01-origin-{route_key}",
        return_slot_id=f"n01-slot-{route_key}",
        package_id=f"n01-package-{route_key}",
    )


def invitation_name(return_slot_id: str) -> str:
    return workspace_name(return_slot_id).replace(
        "n01-return-workspace-", "n01-resonance-invitation-", 1
    )


def workspace_name(return_slot_id: str) -> str:
    opaque_id = return_slot_id.removeprefix("n01-slot-")
    if not opaque_id or not all(
        character.isascii() and (character.isalnum() or character in "._-")
        for character in opaque_id
    ):
        raise InvitationPublicationError(
            "Return Slot ID cannot form a safe workspace name."
        )
    return f"n01-return-workspace-{opaque_id}"


def prepare_resonance_invitation(
    token: ResonanceToken,
    *,
    invitation_root: Path,
    private_root: Path,
    result_file: str | None = None,
    _workspace_builder=None,
    _publisher=None,
) -> InvitationPreparationResult:
    """Stage, verify, and atomically publish travelling and private outputs."""

    workspace_builder = _workspace_builder or _build_return_workspace
    publisher = _publisher or _publish
    validated_token = _validated_token_v2(token)
    invitation_root = invitation_root.expanduser().resolve()
    private_root = private_root.expanduser().resolve()
    final_invitation = invitation_root / invitation_name(
        validated_token.return_slot_id
    )
    final_workspace = private_root / workspace_name(validated_token.return_slot_id)
    final_slot = final_workspace / WORKSPACE_SLOT_PATH
    if final_workspace.is_relative_to(final_invitation) or final_invitation.is_relative_to(
        final_workspace
    ):
        raise InvitationPublicationError(
            "The private Return Workspace and travelling invitation must be separate paths."
        )
    _require_absent(final_invitation, final_workspace)

    result_target_key = hashlib.sha256(
        validated_token.return_slot_id.encode("ascii")
    ).hexdigest()[:24]
    safe_result_file = _validate_result_filename(
        result_file or f"return_resonance_{result_target_key}.local.md"
    )
    identity = _identity_from_token(validated_token)
    slot_document = _build_slot_document(
        validated_token,
        safe_result_file,
        validated_token.public_safe_label or "resonance invitation",
    )

    invitation_root.parent.mkdir(parents=True, exist_ok=True)
    private_root.parent.mkdir(parents=True, exist_ok=True)
    invitation_stage_root = Path(
        tempfile.mkdtemp(
            prefix=".nexus-invitation-stage-", dir=invitation_root.parent
        )
    )
    workspace_stage_root = Path(
        tempfile.mkdtemp(
            prefix=".nexus-return-workspace-stage-", dir=private_root.parent
        )
    )
    published: list[Path] = []
    try:
        staged_invitation = invitation_stage_root / final_invitation.name
        staged_workspace = workspace_stage_root / final_workspace.name
        _build_invitation(staged_invitation, validated_token)
        workspace_builder(staged_workspace, slot_document)
        _verify_invitation(staged_invitation, identity)
        _verify_workspace(staged_workspace, identity, safe_result_file)

        publisher(staged_invitation, final_invitation)
        published.append(final_invitation)
        publisher(staged_workspace, final_workspace)
        published.append(final_workspace)
        return InvitationPreparationResult(
            invitation_path=final_invitation,
            private_workspace_path=final_workspace,
            private_slot_path=final_slot,
            token=validated_token,
        )
    except Exception:
        _rollback_publication(*published)
        raise
    finally:
        shutil.rmtree(invitation_stage_root, ignore_errors=True)
        shutil.rmtree(workspace_stage_root, ignore_errors=True)


def _validated_token_v2(token: ResonanceToken) -> ResonanceToken:
    try:
        validated = parse_resonance_token(token.to_dict())
    except (AttributeError, ResonanceTokenLoadError) as error:
        raise InvitationPublicationError(
            "Invitation preparation requires a validated Resonance Token V2."
        ) from error
    if validated.is_legacy or not validated.has_originating_contribution:
        raise InvitationPublicationError(
            "Invitation preparation requires a Resonance Token V2 with originating data."
        )
    return validated


def _identity_from_token(token: ResonanceToken) -> dict[str, str]:
    return {
        field_name: getattr(token, field_name)
        for field_name in (
            "module_id", "layer_id", "origin_trace_id", "return_slot_id", "package_id"
        )
    }


def _validate_result_filename(value: str) -> str:
    path = Path(value)
    stem = path.name.split(".", 1)[0].upper()
    if not (
        value
        and not path.is_absolute()
        and path.name == value
        and "/" not in value
        and "\\" not in value
        and ".." not in value
        and _SAFE_RESULT_FILENAME.fullmatch(value)
        and not value.endswith((".", " "))
        and stem not in _WINDOWS_RESERVED_STEMS
    ):
        raise InvitationPublicationError(
            "result_file must be one plain safe relative filename."
        )
    return value


def _build_slot_document(
    token: ResonanceToken,
    result_file: str,
    public_safe_label: str,
) -> dict[str, object]:
    return {
        "document_status": "private local return slots",
        "slots": [
            {
                **_identity_from_token(token),
                "status": "waiting",
                "result_file": result_file,
                "public_safe_label": public_safe_label,
                "note": SLOT_NOTE,
            }
        ],
    }


def _build_invitation(path: Path, token: ResonanceToken) -> None:
    path.mkdir()
    _write_text(path / INVITATION_README_PATH, INVITATION_README)
    (path / TOKEN_PATH).write_text(token.to_json(), encoding="utf-8")


def _build_return_workspace(
    workspace_dir: Path,
    slot_document: dict[str, object],
) -> Path:
    if workspace_dir.exists():
        raise InvitationPublicationError(
            f"Refusing to replace existing staged workspace: {workspace_dir}"
        )
    workspace_dir.mkdir()
    for directory in ("incoming", "results", "private", "runtime"):
        (workspace_dir / directory).mkdir()
    for relative in sorted(WORKSPACE_RUNTIME_SOURCE_FILES, key=str):
        source = NEXUS_ROOT / relative
        if not source.is_file():
            raise InvitationPublicationError(
                f"Required opening runtime file is missing: {relative}"
            )
        target = workspace_dir / "runtime" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    _write_text(workspace_dir / "OPEN_RETURN.sh", OPEN_RETURN_SCRIPT)
    _make_executable(workspace_dir / "OPEN_RETURN.sh")
    _write_text(workspace_dir / "README.md", WORKSPACE_README)
    (workspace_dir / WORKSPACE_SLOT_PATH).write_text(
        json.dumps(slot_document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return workspace_dir


def _verify_invitation(path: Path, identity: dict[str, str]) -> None:
    actual = {entry.relative_to(path) for entry in path.rglob("*")}
    expected = {INVITATION_README_PATH, TOKEN_PATH}
    if actual != expected or any(entry.is_symlink() for entry in path.rglob("*")):
        raise InvitationPublicationError(
            "Staged Resonance invitation failed its strict file allowlist."
        )
    token = load_resonance_token(path / TOKEN_PATH)
    if token.is_legacy or not token.has_originating_contribution:
        raise InvitationPublicationError(
            "Staged Resonance invitation does not contain Token V2."
        )
    if any(getattr(token, name) != expected for name, expected in identity.items()):
        raise InvitationPublicationError(
            "Staged Resonance invitation route identity changed."
        )
    readme = (path / INVITATION_README_PATH).read_text(encoding="utf-8").casefold()
    for phrase in ("optional invitation", "does not activate", "manually", "recipient chooses"):
        if phrase not in readme:
            raise InvitationPublicationError(
                "Staged Resonance invitation README failed validation."
            )


def _verify_workspace(
    path: Path,
    identity: dict[str, str],
    result_file: str,
) -> None:
    expected_root = {"OPEN_RETURN.sh", "README.md", "incoming", "results", "private", "runtime"}
    if {entry.name for entry in path.iterdir()} != expected_root:
        raise InvitationPublicationError(
            "Staged private Return Workspace has an invalid root structure."
        )
    if any(entry.is_symlink() for entry in path.rglob("*")):
        raise InvitationPublicationError(
            "Staged private Return Workspace contains a symbolic link."
        )
    actual_runtime = {
        entry.relative_to(path)
        for entry in (path / "runtime").rglob("*")
        if entry.is_file()
    }
    if actual_runtime != WORKSPACE_RUNTIME_FILES:
        raise InvitationPublicationError(
            "Staged private Return Workspace runtime failed its allowlist."
        )
    slots = load_return_slots(path / WORKSPACE_SLOT_PATH)
    if len(slots) != 1:
        raise InvitationPublicationError(
            "Staged private Return Workspace must contain exactly one Return Slot."
        )
    slot = slots[0]
    if slot.result_file != result_file or any(
        getattr(slot, name) != expected for name, expected in identity.items()
    ):
        raise InvitationPublicationError(
            "Staged private Return Workspace route identity changed."
        )
    forbidden = {
        "activation.local.json",
        "resonance_token.local.json",
        "return_artifact.local.json",
    }
    if any(entry.name in forbidden for entry in path.rglob("*")):
        raise InvitationPublicationError(
            "Staged private Return Workspace contains travelling or activation data."
        )
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        check = subprocess.run(
            [
                sys.executable,
                "-I",
                "-c",
                (
                    "import sys; sys.dont_write_bytecode=True; "
                    "sys.path.insert(0,'.'); import open_resonance_return"
                ),
            ],
            cwd=path / "runtime",
            env=environment,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise InvitationPublicationError(
            "Staged private Return Workspace import preflight could not run."
        ) from error
    if check.returncode != 0:
        detail = (check.stderr or check.stdout).strip().splitlines()[-1:]
        raise InvitationPublicationError(
            "Staged private Return Workspace opening runtime cannot import in isolation"
            + (f": {detail[0]}" if detail else ".")
        )


def _require_absent(*paths: Path) -> None:
    for path in paths:
        if path.exists():
            raise InvitationPublicationError(
                f"Refusing to overwrite existing output: {path}"
            )


def _publish(staged: Path, final: Path) -> None:
    final.parent.mkdir(parents=True, exist_ok=True)
    if final.exists():
        raise InvitationPublicationError(
            f"Refusing to overwrite existing output: {final}"
        )
    try:
        os.rename(staged, final)
    except OSError as error:
        raise InvitationPublicationError(
            f"Could not publish prepared output: {final}"
        ) from error


def _rollback_publication(*paths: Path) -> None:
    for path in reversed(paths):
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def _write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
