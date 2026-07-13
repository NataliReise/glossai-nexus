"""Render a Nexus Echo from a slim Return Artifact and approved echo paths.

The renderer performs no free text generation and uses no AI. It selects one
known-valid path, inserts approved one-word slots, and validates the 2-4-6-4-1
Nachhall pattern at runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

EXPECTED_ARTIFACT_VERSION = "0.1"
EXPECTED_LIBRARY_VERSION = "resonance-en-v0.1"
EXPECTED_WORD_COUNTS = (2, 4, 6, 4, 1)
ALLOWED_PLACEHOLDERS = {"wish_word", "return_word"}


class NexusEchoRenderError(ValueError):
    """Raised when a Return Artifact cannot be rendered safely as a Nexus Echo."""


@dataclass(frozen=True)
class RenderedNexusEcho:
    text: str
    path_id: str
    word_counts: tuple[int, int, int, int, int]
    library_version: str


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise NexusEchoRenderError(f"Missing library file: {path}") from error
    except json.JSONDecodeError as error:
        raise NexusEchoRenderError(f"Invalid JSON in {path}: {error}") from error

    if not isinstance(value, dict):
        raise NexusEchoRenderError(f"Library document must be an object: {path}")
    return value


def _validate_word(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value or any(char.isspace() for char in value):
        raise NexusEchoRenderError(f"{field} must be exactly one non-empty word")
    return value


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def _render_line(template: Any, slots: dict[str, str], location: str) -> str:
    if not isinstance(template, str) or not template.strip():
        raise NexusEchoRenderError(f"Invalid line template at {location}")

    placeholders = set(re.findall(r"\{([^{}]+)\}", template))
    unknown = placeholders - ALLOWED_PLACEHOLDERS
    if unknown:
        names = ", ".join(sorted(unknown))
        raise NexusEchoRenderError(f"Unknown placeholder at {location}: {names}")

    rendered = template
    for name in ALLOWED_PLACEHOLDERS:
        rendered = rendered.replace("{" + name + "}", slots[name])

    if "{" in rendered or "}" in rendered:
        raise NexusEchoRenderError(f"Unresolved placeholder at {location}")
    return rendered


def _find_matching_path(document: dict[str, Any], artifact: dict[str, Any]) -> dict[str, Any]:
    paths = document.get("paths")
    if not isinstance(paths, list):
        raise NexusEchoRenderError("echo_paths.json.paths must be an array")

    for index, path in enumerate(paths):
        if not isinstance(path, dict):
            raise NexusEchoRenderError(f"Invalid echo path at index {index}")
        requires = path.get("requires")
        if not isinstance(requires, dict):
            raise NexusEchoRenderError(f"Echo path {index} has invalid requires block")
        if all(artifact.get(key) == value for key, value in requires.items()):
            return path

    fallback = document.get("fallback")
    message = None
    if isinstance(fallback, dict) and isinstance(fallback.get("message"), str):
        message = fallback["message"]
    raise NexusEchoRenderError(
        message or "No approved Nexus Echo path is available for this composition."
    )


def render_nexus_echo(
    return_artifact: dict[str, Any],
    library_dir: Path,
) -> RenderedNexusEcho:
    """Render one approved Nexus Echo from a slim Return Artifact."""
    if not isinstance(return_artifact, dict):
        raise NexusEchoRenderError("Return Artifact must be a JSON object")

    if return_artifact.get("artifact_version") != EXPECTED_ARTIFACT_VERSION:
        raise NexusEchoRenderError(
            f"Unsupported artifact_version: {return_artifact.get('artifact_version')!r}"
        )
    if return_artifact.get("language_library") != EXPECTED_LIBRARY_VERSION:
        raise NexusEchoRenderError(
            f"Unsupported language_library: {return_artifact.get('language_library')!r}"
        )

    wish_word = _validate_word(return_artifact.get("wish_word"), "wish_word")
    return_word = _validate_word(return_artifact.get("return_word"), "return_word")

    document = _load_json(library_dir / "echo_paths.json")
    if document.get("library_version") != EXPECTED_LIBRARY_VERSION:
        raise NexusEchoRenderError(
            f"Unsupported echo path library_version: {document.get('library_version')!r}"
        )

    path = _find_matching_path(document, return_artifact)
    path_id = path.get("id")
    if not isinstance(path_id, str) or not path_id:
        raise NexusEchoRenderError("Matched echo path has no valid id")

    lines = path.get("lines")
    if not isinstance(lines, list) or len(lines) != 5:
        raise NexusEchoRenderError(f"Echo path {path_id!r} must contain exactly five lines")

    slots = {"wish_word": wish_word, "return_word": return_word}
    rendered_lines = [
        _render_line(line, slots, f"echo path {path_id!r} line {index + 1}")
        for index, line in enumerate(lines)
    ]

    counts = tuple(_word_count(line) for line in rendered_lines)
    for index, (actual, expected) in enumerate(zip(counts, EXPECTED_WORD_COUNTS, strict=True)):
        if actual != expected:
            raise NexusEchoRenderError(
                f"Echo path {path_id!r} line {index + 1}: expected {expected} words, found {actual}"
            )

    return RenderedNexusEcho(
        text="\n".join(rendered_lines),
        path_id=path_id,
        word_counts=counts,
        library_version=EXPECTED_LIBRARY_VERSION,
    )


def default_library_dir() -> Path:
    return Path(__file__).resolve().parent / "v0_1"
