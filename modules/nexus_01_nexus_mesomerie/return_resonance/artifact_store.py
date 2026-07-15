"""Safe local persistence for shared Resonance Return Artifacts."""

from __future__ import annotations

from pathlib import Path

from .resonance_render_bridge import ResonanceReturnArtifact


class ResonanceArtifactStoreError(OSError):
    """Raised when a Resonance Return Artifact cannot be stored safely."""


def write_resonance_return_artifact(
    artifact: ResonanceReturnArtifact,
    path: str | Path,
) -> Path:
    """Write one artifact locally without overwriting an existing file.

    Parent directories are not created implicitly. The caller must choose an
    existing destination deliberately. Exclusive creation keeps an existing
    artifact safe from accidental replacement.
    """

    artifact_path = Path(path).expanduser()
    try:
        with artifact_path.open("x", encoding="utf-8") as handle:
            handle.write(artifact.to_json())
    except FileExistsError as error:
        raise ResonanceArtifactStoreError(
            f"Refusing to overwrite existing file: {artifact_path}"
        ) from error
    except OSError as error:
        raise ResonanceArtifactStoreError(
            f"Could not write Resonance Return Artifact: {artifact_path}"
        ) from error

    return artifact_path
