"""Render a Nexus Echo from a slim Return Artifact and approved echo paths.

The renderer performs no free text generation and uses no AI. It first selects an
exact known-valid path. If no exact path exists, it combines one approved image,
scent, and movement component, then validates the 2-4-6-4-1 Nachhall pattern.
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


def _matches(requirements: Any, artifact: dict[str, Any], location: str) -> bool:
    if not isinstance(requirements, dict):
        raise NexusEchoRenderError(f"{location} has invalid requires block")
    return all(artifact.get(key) == value for key, value in requirements.items())


def _find_exact_path(document: dict[str, Any], artifact: dict[str, Any]) -> dict[str, Any] | None:
    paths = document.get("paths")
    if not isinstance(paths, list):
        raise NexusEchoRenderError("echo_paths.json.paths must be an array")

    for index, path in enumerate(paths):
        if not isinstance(path, dict):
            raise NexusEchoRenderError(f"Invalid echo path at index {index}")
        if _matches(path.get("requires"), artifact, f"Echo path {index}"):
            return path
    return None


def _find_component(
    document: dict[str, Any],
    family: str,
    artifact: dict[str, Any],
) -> dict[str, Any]:
    components = document.get("components")
    if not isinstance(components, dict):
        raise NexusEchoRenderError("echo_paths.json.components must be an object")

    entries = components.get(family)
    if not isinstance(entries, list):
        raise NexusEchoRenderError(f"echo_paths.json.components.{family} must be an array")

    matches: list[dict[str, Any]] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise NexusEchoRenderError(f"Invalid {family} component at index {index}")
        if _matches(entry.get("requires"), artifact, f"{family} component {index}"):
            matches.append(entry)

    if len(matches) != 1:
        raise NexusEchoRenderError(
            f"Expected exactly one approved {family} component, found {len(matches)}."
        )
    return matches[0]


def _fallback_message(document: dict[str, Any]) -> str:
    fallback = document.get("fallback")
    if isinstance(fallback, dict) and isinstance(fallback.get("message"), str):
        return fallback["message"]
    return "No approved Nexus Echo path or component composition is available for this composition."


def _render_exact_path(
    path: dict[str, Any],
    slots: dict[str, str],
) -> tuple[str, list[str]]:
    path_id = path.get("id")
    if not isinstance(path_id, str) or not path_id:
        raise NexusEchoRenderError("Matched echo path has no valid id")

    lines = path.get("lines")
    if not isinstance(lines, list) or len(lines) != 5:
        raise NexusEchoRenderError(f"Echo path {path_id!r} must contain exactly five lines")

    rendered = [
        _render_line(line, slots, f"echo path {path_id!r} line {index + 1}")
        for index, line in enumerate(lines)
    ]
    return path_id, rendered


def _render_component_path(
    document: dict[str, Any],
    artifact: dict[str, Any],
    slots: dict[str, str],
) -> tuple[str, list[str]]:
    try:
        image = _find_component(document, "image", artifact)
        scent = _find_component(document, "scent", artifact)
        movement = _find_component(document, "movement", artifact)
    except NexusEchoRenderError as error:
        raise NexusEchoRenderError(_fallback_message(document)) from error

    component_ids: list[str] = []
    for family, component in (("image", image), ("scent", scent), ("movement", movement)):
        component_id = component.get("id")
        if not isinstance(component_id, str) or not component_id:
            raise NexusEchoRenderError(f"Matched {family} component has no valid id")
        component_ids.append(component_id)

    templates = [
        image.get("line_1"),
        scent.get("line_2"),
        movement.get("line_3"),
        image.get("line_4"),
        "{return_word}",
    ]
    rendered = [
        _render_line(template, slots, f"component composition line {index + 1}")
        for index, template in enumerate(templates)
    ]
    return "mixed:" + "+".join(component_ids), rendered


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
    slots = {"wish_word": wish_word, "return_word": return_word}

    document = _load_json(library_dir / "echo_paths.json")
    if document.get("library_version") != EXPECTED_LIBRARY_VERSION:
        raise NexusEchoRenderError(
            f"Unsupported echo path library_version: {document.get('library_version')!r}"
        )

    exact_path = _find_exact_path(document, return_artifact)
    if exact_path is not None:
        path_id, rendered_lines = _render_exact_path(exact_path, slots)
    else:
        path_id, rendered_lines = _render_component_path(document, return_artifact, slots)

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
