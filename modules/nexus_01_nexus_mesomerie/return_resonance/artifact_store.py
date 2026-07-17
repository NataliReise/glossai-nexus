"""Safe local persistence for shared Resonance Return Artifacts."""

from __future__ import annotations

import os
from pathlib import Path
import tempfile

from .resonance_render_bridge import ResonanceReturnArtifact


class ResonanceArtifactStoreError(OSError):
    """Raised when a Resonance Return Artifact cannot be stored safely."""


def write_resonance_return_artifact(
    artifact: ResonanceReturnArtifact,
    path: str | Path,
) -> Path:
    """Write one artifact locally without overwriting an existing file.

    Parent directories are not created implicitly. The caller must choose an
    existing destination deliberately. A complete staged file is linked into
    place atomically, so an existing or partially written artifact is never
    exposed at the selected destination.
    """

    artifact_path = Path(path).expanduser()
    staged_path: Path | None = None
    try:
        descriptor, raw_staged_path = tempfile.mkstemp(
            prefix=f".{artifact_path.name}.",
            suffix=".staged",
            dir=artifact_path.parent,
        )
        staged_path = Path(raw_staged_path)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(artifact.to_json())
            handle.flush()
            os.fsync(handle.fileno())
        os.link(staged_path, artifact_path)
    except FileExistsError as error:
        raise ResonanceArtifactStoreError(
            f"Refusing to overwrite existing file: {artifact_path}"
        ) from error
    except OSError as error:
        raise ResonanceArtifactStoreError(
            f"Could not write Resonance Return Artifact: {artifact_path}"
        ) from error
    finally:
        if staged_path is not None:
            try:
                staged_path.unlink()
            except FileNotFoundError:
                pass

    return artifact_path
