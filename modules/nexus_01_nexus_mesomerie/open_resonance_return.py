#!/usr/bin/env python3
"""Open one matched Resonance Return Artifact into a stable local result.

The command loads the shared JSON artifact and local slot document, verifies the
route through the existing matcher, renders both approved poetic outputs, writes
the result once, and marks the matching slot as opened. Nothing is published.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from typing import Any

NEXUS_01_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(NEXUS_01_ROOT))

from resonance_language_library.render_resonance_output import default_library_dir
from return_resonance.matching import MatchStatus
from return_resonance.resonance_render_bridge import (
    OpenedResonanceReturn,
    ResonanceRenderBridgeError,
    load_resonance_return_artifact,
    open_resonance_return,
)
from return_resonance.slots import ReturnSlotLoadError, load_return_slots


class LocalResonanceOpenError(ValueError):
    """Raised when a matched return cannot be opened safely on disk."""


@dataclass(frozen=True)
class LocalResonanceResult:
    path: Path
    content: str
    created: bool
    slot_state_changed: bool
    opened: OpenedResonanceReturn


def open_resonance_return_files(
    artifact_path: str | Path,
    slots_path: str | Path,
    output_dir: str | Path,
    library_dir: str | Path | None = None,
) -> LocalResonanceResult:
    """Open a shared artifact locally with generate-once, revisit-often behavior."""

    artifact_file = Path(artifact_path)
    slot_file = Path(slots_path)
    result_dir = Path(output_dir)
    library = Path(library_dir) if library_dir is not None else default_library_dir()

    artifact = load_resonance_return_artifact(artifact_file)
    slots = load_return_slots(slot_file)
    opened = open_resonance_return(artifact, slots, library)

    if opened.match.slot is None:
        raise LocalResonanceOpenError("Matched Resonance Return has no slot data.")

    result_path = result_dir / opened.match.slot.result_file
    if result_path.exists():
        try:
            content = result_path.read_text(encoding="utf-8")
        except OSError as error:
            raise LocalResonanceOpenError(
                f"Could not read existing local result: {result_path}"
            ) from error
        state_changed = _mark_slot_opened(slot_file, artifact.origin_trace_id, artifact.return_slot_id)
        return LocalResonanceResult(
            path=result_path,
            content=content,
            created=False,
            slot_state_changed=state_changed,
            opened=opened,
        )

    if opened.match.status == MatchStatus.MATCH_OPENED:
        raise LocalResonanceOpenError(
            "The matching slot is marked as opened, but its local result file is missing."
        )

    content = _compose_local_result(opened)
    _write_new_file(result_path, content)
    state_changed = _mark_slot_opened(slot_file, artifact.origin_trace_id, artifact.return_slot_id)

    return LocalResonanceResult(
        path=result_path,
        content=content,
        created=True,
        slot_state_changed=state_changed,
        opened=opened,
    )


def _compose_local_result(opened: OpenedResonanceReturn) -> str:
    slot = opened.match.slot
    if slot is None:
        raise LocalResonanceOpenError("Cannot compose a local result without slot data.")

    return "\n".join(
        [
            f"# Resonance Return: {slot.return_slot_id}",
            "",
            "Status: opened",
            f"Module: {slot.module_id}",
            f"Layer: {slot.layer_id}",
            f"Origin trace: {slot.origin_trace_id}",
            f"Language library: {opened.artifact.language_library}",
            "",
            "---",
            "",
            opened.output.text,
            "",
            "---",
            "",
            "## Privacy reminder",
            "",
            "This is a local Resonance Return result.",
            "",
            "Do not publish it unless it has been reviewed carefully and intentionally made public-safe.",
            "",
        ]
    )


def _write_new_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise LocalResonanceOpenError(f"Refusing to overwrite existing local result: {path}")

    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(content, encoding="utf-8")
        if path.exists():
            raise LocalResonanceOpenError(
                f"Refusing to overwrite existing local result: {path}"
            )
        temporary.replace(path)
    except OSError as error:
        raise LocalResonanceOpenError(f"Could not write local result: {path}") from error
    finally:
        if temporary.exists():
            temporary.unlink()


def _mark_slot_opened(path: Path, origin_trace_id: str, return_slot_id: str) -> bool:
    document = _load_slot_document(path)
    slots = document.get("slots")
    if not isinstance(slots, list):
        raise LocalResonanceOpenError("Return slot document must contain a slots list.")

    matching: list[dict[str, Any]] = []
    for item in slots:
        if not isinstance(item, dict):
            continue
        if (
            item.get("origin_trace_id") == origin_trace_id
            and item.get("return_slot_id") == return_slot_id
        ):
            matching.append(item)

    if len(matching) != 1:
        raise LocalResonanceOpenError(
            "Expected exactly one matching slot while updating local state."
        )

    slot = matching[0]
    if slot.get("status") == "opened":
        return False
    if slot.get("status") != "waiting":
        raise LocalResonanceOpenError(
            f"Cannot mark slot opened from unsupported state: {slot.get('status')!r}"
        )

    slot["status"] = "opened"
    _replace_json_file(path, document)
    return True


def _load_slot_document(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise LocalResonanceOpenError(f"Could not read return slot document: {path}") from error
    except json.JSONDecodeError as error:
        raise LocalResonanceOpenError(
            f"Return slot document is not valid JSON: {error.msg}"
        ) from error
    if not isinstance(value, dict):
        raise LocalResonanceOpenError("Return slot document must be a JSON object.")
    return value


def _replace_json_file(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
    except OSError as error:
        raise LocalResonanceOpenError(f"Could not update return slot document: {path}") from error
    finally:
        if temporary.exists():
            temporary.unlink()


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open a matched Nexus 01 Resonance Return locally.",
    )
    parser.add_argument("--artifact", required=True, type=Path)
    parser.add_argument("--slots", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--library-dir", type=Path, default=None)
    return parser.parse_args(argv)


def _display_path(path: Path) -> Path:
    try:
        return path.relative_to(Path.cwd())
    except ValueError:
        return path


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    print("Nexus 01 - Open Resonance Return")
    print("================================")
    print()
    print("This command opens a matched return locally. It does not publish anything.")
    print()

    try:
        result = open_resonance_return_files(
            artifact_path=args.artifact.expanduser().resolve(),
            slots_path=args.slots.expanduser().resolve(),
            output_dir=args.output_dir.expanduser().resolve(),
            library_dir=(
                args.library_dir.expanduser().resolve() if args.library_dir is not None else None
            ),
        )
    except (
        LocalResonanceOpenError,
        ResonanceRenderBridgeError,
        ReturnSlotLoadError,
    ) as error:
        print("Error:", error)
        return 2

    if result.created:
        print("Local result created:", _display_path(result.path))
    else:
        print("Local result reused:", _display_path(result.path))

    print("Slot state:", "opened now" if result.slot_state_changed else "already opened")
    print()
    print("Privacy reminder:")
    print("Do not publish the artifact or local result unless reviewed carefully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
