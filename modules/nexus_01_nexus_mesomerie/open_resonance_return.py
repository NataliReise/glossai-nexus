#!/usr/bin/env python3
"""Open one matched Resonance Return Artifact into a stable local result.

The command loads the shared JSON artifact and local slot document, verifies the
route through the existing matcher, preserves an existing result or generates one
compact production result, writes it once, and marks the matching slot as opened.
Nothing is transported or published.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import TYPE_CHECKING, Any, Protocol
import unicodedata

NEXUS_01_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(NEXUS_01_ROOT))

from return_resonance.matching import MatchResult, match_return_artifact
from return_resonance.resonance_render_bridge import (
    ResonanceReturnArtifact,
    ResonanceRenderBridgeError,
    load_resonance_return_artifact,
)
from return_resonance.slots import (
    ReturnSlot,
    ReturnSlotLoadError,
    ReturnSlotState,
    load_return_slots,
)

if TYPE_CHECKING:
    from return_resonance.compact_generator import CompactGenerationResult


class LocalResonanceOpenError(ValueError):
    """Raised when a matched return cannot be opened safely on disk."""


class CompactGenerator(Protocol):
    def __call__(
        self,
        artifact: ResonanceReturnArtifact,
        *,
        seed: str,
    ) -> CompactGenerationResult: ...


class SlotStateUpdater(Protocol):
    def __call__(self, path: Path, origin_trace_id: str, return_slot_id: str) -> bool: ...


@dataclass(frozen=True)
class LocalResonanceResult:
    path: Path
    content: str
    created: bool
    slot_state_changed: bool
    artifact: ResonanceReturnArtifact
    match: MatchResult
    generation: CompactGenerationResult | None


_SAFE_RESULT_FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}")
_WINDOWS_RESERVED_STEMS = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
_TRACE_START = "<!-- nexus-01-result-trace-start -->"
_TRACE_END = "<!-- nexus-01-result-trace-end -->"
_SEED_DERIVATION_ID = "nexus-01-compact-opening-seed-v1"


def open_resonance_return_files(
    artifact_path: str | Path,
    slots_path: str | Path,
    output_dir: str | Path,
    library_dir: str | Path | None = None,
    *,
    generator: CompactGenerator | None = None,
    slot_state_updater: SlotStateUpdater | None = None,
) -> LocalResonanceResult:
    """Open a shared artifact locally with generate-once, revisit-often behavior."""

    artifact_file = Path(artifact_path)
    slot_file = Path(slots_path)
    result_dir = Path(output_dir)
    # Accepted for CLI/API compatibility. The production compact path has no
    # external library directory and never invokes the legacy renderer.
    _ = library_dir
    active_slot_updater = (
        slot_state_updater if slot_state_updater is not None else _mark_slot_opened
    )

    artifact = load_resonance_return_artifact(artifact_file)
    slots = load_return_slots(slot_file)
    match = _match_artifact(artifact, slots)
    slot = match.slot
    if slot is None:
        raise LocalResonanceOpenError("Matched Resonance Return has no slot data.")
    result_name = _validate_result_target(slot, slots)
    result_path = _result_path_beneath(result_dir, result_name)

    if result_path.exists():
        content = _read_existing_result(result_path)
        if slot.status is ReturnSlotState.WAITING:
            _require_result_identity(content, artifact, slot)
            state_changed = _update_slot_after_result(
                active_slot_updater, slot_file, artifact
            )
        else:
            state_changed = False
        return LocalResonanceResult(
            path=result_path,
            content=content,
            created=False,
            slot_state_changed=state_changed,
            artifact=artifact,
            match=match,
            generation=None,
        )

    if slot.status is ReturnSlotState.OPENED:
        raise LocalResonanceOpenError(
            "The matching slot is marked as opened, but its local result file is missing. "
            "Restore the saved result or deliberately repair the slot state; it will not be regenerated."
        )

    seed, seed_trace = _derive_seed(artifact, slot)
    if generator is None:
        try:
            from return_resonance.compact_generator import generate_compact_resonance
        except ImportError as error:
            raise LocalResonanceOpenError(
                "Compact generator is unavailable for this first opening."
            ) from error
        active_generator = generate_compact_resonance
    else:
        active_generator = generator
    try:
        generation = active_generator(artifact, seed=seed)
    except ValueError as error:
        raise LocalResonanceOpenError(f"Compact generation failed: {error}") from error
    content = _compose_local_result(artifact, slot, generation, seed, seed_trace)
    _write_new_file(result_path, content)
    state_changed = _update_slot_after_result(
        active_slot_updater, slot_file, artifact
    )

    return LocalResonanceResult(
        path=result_path,
        content=content,
        created=True,
        slot_state_changed=state_changed,
        artifact=artifact,
        match=match,
        generation=generation,
    )


def _compose_local_result(
    artifact: ResonanceReturnArtifact,
    slot: ReturnSlot,
    generation: CompactGenerationResult,
    seed: str,
    seed_trace: dict[str, str],
) -> str:
    artifact_identity = _structural_identity(artifact)
    slot_identity = _structural_identity(slot)
    trace = {
        "trace_format": "nexus-01-compact-result-trace-v1",
        "generator_id": generation.generator_id,
        "generator_version": generation.generator_version,
        "deterministic_seed": seed,
        "seed_derivation": {
            "derivation_id": _SEED_DERIVATION_ID,
            "algorithm": "SHA-256",
            "inputs": seed_trace,
        },
        "composition_plan": generation.composition_plan,
        "artifact_identity": artifact_identity,
        "slot_identity": slot_identity,
        "result_file": slot.result_file,
    }
    return "\n".join(
        [
            "# Resonance Return",
            "",
            "## Compact Resonance",
            "",
            "```text",
            generation.text,
            "```",
            "",
            _TRACE_START,
            "<details>",
            "<summary>Technical trace</summary>",
            "",
            "```json",
            json.dumps(trace, indent=2, ensure_ascii=False, sort_keys=True),
            "```",
            "",
            "</details>",
            _TRACE_END,
            "",
            "---",
            "",
            "This result remains local unless you deliberately transfer it.",
            "",
        ]
    )


def _write_new_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary_path, path)
    except FileExistsError as error:
        raise LocalResonanceOpenError(
            f"Refusing to overwrite existing local result: {path}. Reopen to inspect it safely."
        ) from error
    except OSError as error:
        raise LocalResonanceOpenError(f"Could not write local result: {path}") from error
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def _match_artifact(
    artifact: ResonanceReturnArtifact,
    slots: list[ReturnSlot],
) -> MatchResult:
    match = match_return_artifact(artifact.to_matching_artifact(), slots)
    if not match.is_match:
        raise LocalResonanceOpenError(
            f"Resonance Return Artifact cannot open: {match.status.value}: {match.message}"
        )
    if match.slot is None:
        raise LocalResonanceOpenError("Matched Resonance Return has no slot data.")
    if artifact.module_id != match.slot.module_id:
        raise LocalResonanceOpenError(
            "Resonance Return Artifact cannot open: module_mismatch: "
            "the artifact does not match the module for this slot."
        )
    return match


def _validate_result_target(slot: ReturnSlot, slots: list[ReturnSlot]) -> str:
    value = slot.result_file
    candidate = Path(value)
    stem = candidate.name.split(".", 1)[0].upper()
    if (
        not value
        or candidate.is_absolute()
        or candidate.name != value
        or "/" in value
        or "\\" in value
        or ".." in value
        or _SAFE_RESULT_FILENAME.fullmatch(value) is None
        or value.endswith((".", " "))
        or stem in _WINDOWS_RESERVED_STEMS
    ):
        raise LocalResonanceOpenError(
            "Return Slot result_file must be one unambiguous ASCII filename without paths, "
            "traversal, reserved names, or unsafe characters."
        )

    normalized_target = _normalized_filename(value)
    collisions = [
        candidate_slot
        for candidate_slot in slots
        if _normalized_filename(candidate_slot.result_file) == normalized_target
    ]
    if len(collisions) != 1:
        raise LocalResonanceOpenError(
            f"Multiple Return Slots target the same result filename: {value!r}. "
            "Choose a unique filename before opening."
        )
    return value


def _result_path_beneath(output_dir: Path, result_name: str) -> Path:
    result_path = output_dir / result_name
    if result_path.is_symlink():
        raise LocalResonanceOpenError("Refusing a symbolic-link result target.")
    if result_path.resolve(strict=False).parent != output_dir.resolve(strict=False):
        raise LocalResonanceOpenError("Return result must remain beneath the selected output directory.")
    return result_path


def _read_existing_result(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise LocalResonanceOpenError("Existing result target is not a safe regular file.")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise LocalResonanceOpenError(
            "Existing local result could not be read as exact UTF-8 content."
        ) from error


def _update_slot_after_result(
    updater: SlotStateUpdater,
    slot_file: Path,
    artifact: ResonanceReturnArtifact,
) -> bool:
    try:
        return bool(updater(slot_file, artifact.origin_trace_id, artifact.return_slot_id))
    except Exception as error:
        raise LocalResonanceOpenError(
            "The local result was preserved successfully, but the Return Slot could not be "
            "marked opened. Do not delete or overwrite the result; retry this opening to "
            "repair the waiting slot without regeneration."
        ) from error


def _derive_seed(
    artifact: ResonanceReturnArtifact,
    slot: ReturnSlot,
) -> tuple[str, dict[str, str]]:
    inputs = _structural_identity(artifact)
    if inputs != _structural_identity(slot):
        raise LocalResonanceOpenError("Artifact and Return Slot structural identities disagree.")
    payload = json.dumps(
        {"derivation_id": _SEED_DERIVATION_ID, "inputs": inputs},
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    return f"n01-open-v1-{digest}", inputs


def _structural_identity(value: ResonanceReturnArtifact | ReturnSlot) -> dict[str, str]:
    return {
        "module_id": value.module_id,
        "layer_id": value.layer_id,
        "origin_trace_id": value.origin_trace_id,
        "return_slot_id": value.return_slot_id,
        "package_id": value.package_id,
    }


def _require_result_identity(
    content: str,
    artifact: ResonanceReturnArtifact,
    slot: ReturnSlot,
) -> None:
    try:
        marked = content.split(_TRACE_START, 1)[1].split(_TRACE_END, 1)[0]
        json_text = marked.split("```json", 1)[1].split("```", 1)[0]
        trace = json.loads(json_text)
    except (IndexError, json.JSONDecodeError) as error:
        raise LocalResonanceOpenError(
            "A result exists for a waiting slot, but its structural trace cannot be verified. "
            "It was preserved and not reused or overwritten."
        ) from error
    if not isinstance(trace, dict):
        raise LocalResonanceOpenError(
            "A result exists for a waiting slot, but its structural trace is not an object. "
            "It was preserved and not reused or overwritten."
        )
    expected = _structural_identity(artifact)
    if trace.get("artifact_identity") != expected or trace.get("slot_identity") != _structural_identity(slot):
        raise LocalResonanceOpenError(
            "An existing result belongs to different structural identifiers. "
            "It was preserved and not reused or overwritten."
        )


def _normalized_filename(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


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
    parser.add_argument(
        "--library-dir",
        type=Path,
        default=None,
        help="Accepted for legacy CLI compatibility; ignored by the compact production generator.",
    )
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
