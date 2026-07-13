"""Render the complete local Resonance output from one slim Return Artifact.

This module combines the approved long-form Resonance Artifact and the approved
five-line Nexus Echo. It performs no free generation and uses no AI.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import sys
from typing import Any

from resonance_language_library.render_nexus_echo import (
    NexusEchoRenderError,
    RenderedNexusEcho,
    render_nexus_echo,
)
from resonance_language_library.render_resonance_artifact import (
    RenderedResonanceArtifact,
    ResonanceArtifactRenderError,
    render_resonance_artifact,
)


class ResonanceOutputRenderError(ValueError):
    """Raised when the complete Resonance output cannot be rendered safely."""


@dataclass(frozen=True)
class RenderedResonanceOutput:
    resonance_artifact: RenderedResonanceArtifact
    nexus_echo: RenderedNexusEcho
    text: str


def render_resonance_output(
    return_artifact: dict[str, Any],
    library_dir: Path,
) -> RenderedResonanceOutput:
    """Render both approved outputs from the same Return Artifact."""
    try:
        resonance_artifact = render_resonance_artifact(return_artifact, library_dir)
        nexus_echo = render_nexus_echo(return_artifact, library_dir)
    except (ResonanceArtifactRenderError, NexusEchoRenderError) as error:
        raise ResonanceOutputRenderError(str(error)) from error

    text = (
        "Resonance Artifact\n"
        "==================\n\n"
        f"{resonance_artifact.text}\n\n"
        "Nexus Echo\n"
        "==========\n\n"
        f"{nexus_echo.text}"
    )
    return RenderedResonanceOutput(
        resonance_artifact=resonance_artifact,
        nexus_echo=nexus_echo,
        text=text,
    )


def default_library_dir() -> Path:
    return Path(__file__).resolve().parent / "v0_1"


def _load_return_artifact(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ResonanceOutputRenderError(f"Return Artifact file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ResonanceOutputRenderError(f"Invalid Return Artifact JSON: {error}") from error
    if not isinstance(value, dict):
        raise ResonanceOutputRenderError("Return Artifact must be a JSON object")
    return value


def main(argv: list[str] | None = None) -> int:
    arguments = list(argv if argv is not None else sys.argv[1:])
    if not arguments:
        print("Usage: python3 render_resonance_output.py RETURN_ARTIFACT.json [LIBRARY_DIR]", file=sys.stderr)
        return 2

    artifact_path = Path(arguments[0]).resolve()
    library_dir = Path(arguments[1]).resolve() if len(arguments) > 1 else default_library_dir()

    try:
        artifact = _load_return_artifact(artifact_path)
        result = render_resonance_output(artifact, library_dir)
    except ResonanceOutputRenderError as error:
        print(f"Resonance output rendering failed: {error}", file=sys.stderr)
        return 1

    print(result.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
