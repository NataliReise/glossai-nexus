"""Local orchestration for opening one Resonance Return Artifact.

This module loads a saved Return Artifact and local Return Slot file, validates
both contracts, matches route identity, and renders the approved local outputs.
It does not mutate slot state, write result files, or perform any transmission.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from resonance_language_library.render_resonance_output import default_library_dir

from .resonance_render_bridge import (
    OpenedResonanceReturn,
    ResonanceRenderBridgeError,
    load_resonance_return_artifact,
    open_resonance_return,
)
from .slots import ReturnSlotLoadError, load_return_slots


class LocalResonanceOpeningError(ValueError):
    """Raised when a local Resonance return cannot be opened safely."""


@dataclass(frozen=True)
class LocalResonanceOpening:
    """Validated in-memory result of one local opening attempt."""

    artifact_path: Path
    slot_path: Path
    opened: OpenedResonanceReturn


def open_local_resonance_return(
    artifact_path: str | Path,
    slot_path: str | Path,
    library_dir: str | Path | None = None,
) -> LocalResonanceOpening:
    """Load, match, and render one local Resonance Return Artifact.

    The function performs no persistence beyond reading the supplied files.
    In particular, it does not mark a Return Slot as opened and does not write
    the rendered Resonance Artifact or Nexus Echo to disk.
    """

    resolved_artifact_path = Path(artifact_path).expanduser()
    resolved_slot_path = Path(slot_path).expanduser()
    resolved_library_dir = (
        Path(library_dir).expanduser() if library_dir is not None else default_library_dir()
    )

    try:
        artifact = load_resonance_return_artifact(resolved_artifact_path)
        slots = load_return_slots(resolved_slot_path)
        opened = open_resonance_return(artifact, slots, resolved_library_dir)
    except (ResonanceRenderBridgeError, ReturnSlotLoadError) as error:
        raise LocalResonanceOpeningError(str(error)) from error

    return LocalResonanceOpening(
        artifact_path=resolved_artifact_path,
        slot_path=resolved_slot_path,
        opened=opened,
    )
