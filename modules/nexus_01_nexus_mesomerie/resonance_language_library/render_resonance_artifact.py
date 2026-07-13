"""Render a Resonance Artifact from a slim Return Artifact and local library.

The renderer performs no grammar generation and uses no AI. It resolves approved
render-ready lines by stable ID and assembles them in a fixed stanza structure.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

EXPECTED_ARTIFACT_VERSION = "0.1"
EXPECTED_LIBRARY_VERSION = "resonance-en-v0.1"


class ResonanceArtifactRenderError(ValueError):
    """Raised when a Return Artifact cannot be rendered safely."""


@dataclass(frozen=True)
class RenderedResonanceArtifact:
    text: str
    library_version: str


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ResonanceArtifactRenderError(f"Missing library file: {path}") from error
    except json.JSONDecodeError as error:
        raise ResonanceArtifactRenderError(f"Invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ResonanceArtifactRenderError(f"Library document must be an object: {path}")
    return value


def _entries_by_id(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ResonanceArtifactRenderError("Library entries must be an array")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise ResonanceArtifactRenderError("Invalid library entry")
        result[entry["id"]] = entry
    return result


def _nested_responses_by_id(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ResonanceArtifactRenderError("Response groups must be an array")
    for group in entries:
        if not isinstance(group, dict) or not isinstance(group.get("responses"), list):
            raise ResonanceArtifactRenderError("Invalid response group")
        for response in group["responses"]:
            if not isinstance(response, dict) or not isinstance(response.get("id"), str):
                raise ResonanceArtifactRenderError("Invalid response entry")
            result[response["id"]] = response
    return result


def _scent_responses_by_id(document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for key in ("universal", "scene_compatible"):
        entries = document.get(key)
        if not isinstance(entries, list):
            raise ResonanceArtifactRenderError(f"scent_responses.{key} must be an array")
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
                raise ResonanceArtifactRenderError("Invalid scent response entry")
            result[entry["id"]] = entry
    return result


def _artifact_lines(entry: dict[str, Any], entry_id: str) -> list[str]:
    artifact = entry.get("resonance_artifact")
    if not isinstance(artifact, dict) or not isinstance(artifact.get("lines"), list):
        raise ResonanceArtifactRenderError(
            f"No approved Resonance Artifact form for {entry_id!r}"
        )
    lines = artifact["lines"]
    if not lines or any(not isinstance(line, str) or not line.strip() for line in lines):
        raise ResonanceArtifactRenderError(f"Invalid render lines for {entry_id!r}")
    return list(lines)


def _lookup(mapping: dict[str, dict[str, Any]], entry_id: Any, field: str) -> dict[str, Any]:
    if not isinstance(entry_id, str) or not entry_id:
        raise ResonanceArtifactRenderError(f"{field} must be a non-empty string")
    try:
        return mapping[entry_id]
    except KeyError as error:
        raise ResonanceArtifactRenderError(f"Unknown {field}: {entry_id!r}") from error


def _validate_word(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value or any(character.isspace() for character in value):
        raise ResonanceArtifactRenderError(f"{field} must be exactly one non-empty word")
    return value


def _capitalise_word(word: str) -> str:
    return word[:1].upper() + word[1:]


def render_resonance_artifact(
    return_artifact: dict[str, Any],
    library_dir: Path,
) -> RenderedResonanceArtifact:
    """Render one approved long-form Resonance Artifact."""
    if not isinstance(return_artifact, dict):
        raise ResonanceArtifactRenderError("Return Artifact must be a JSON object")
    if return_artifact.get("artifact_version") != EXPECTED_ARTIFACT_VERSION:
        raise ResonanceArtifactRenderError(
            f"Unsupported artifact_version: {return_artifact.get('artifact_version')!r}"
        )
    if return_artifact.get("language_library") != EXPECTED_LIBRARY_VERSION:
        raise ResonanceArtifactRenderError(
            f"Unsupported language_library: {return_artifact.get('language_library')!r}"
        )

    images = _entries_by_id(_load_json(library_dir / "images.json"))
    image_responses = _nested_responses_by_id(
        _load_json(library_dir / "image_responses.json")
    )
    scents = _entries_by_id(_load_json(library_dir / "scents.json"))
    scent_responses = _scent_responses_by_id(
        _load_json(library_dir / "scent_responses.json")
    )
    movements = _entries_by_id(_load_json(library_dir / "movements.json"))
    movement_responses = _nested_responses_by_id(
        _load_json(library_dir / "movement_responses.json")
    )

    image_id = return_artifact.get("image_id")
    image_response_id = return_artifact.get("image_response_id")
    scent_id = return_artifact.get("scent_id")
    scent_response_id = return_artifact.get("scent_response_id")
    movement_id = return_artifact.get("movement_id")
    movement_response_id = return_artifact.get("movement_response_id")

    image = _lookup(images, image_id, "image_id")
    image_response = _lookup(image_responses, image_response_id, "image_response_id")
    scent = _lookup(scents, scent_id, "scent_id")
    scent_response = _lookup(scent_responses, scent_response_id, "scent_response_id")
    movement = _lookup(movements, movement_id, "movement_id")
    movement_response = _lookup(
        movement_responses, movement_response_id, "movement_response_id"
    )

    if isinstance(image_response_id, str):
        valid_for_image = any(
            group.get("image_id") == image_id
            and any(
                isinstance(response, dict) and response.get("id") == image_response_id
                for response in group.get("responses", [])
            )
            for group in _load_json(library_dir / "image_responses.json").get("entries", [])
            if isinstance(group, dict)
        )
        if not valid_for_image:
            raise ResonanceArtifactRenderError(
                f"image_response_id {image_response_id!r} is not compatible with image_id {image_id!r}"
            )

    if isinstance(movement_response_id, str):
        valid_for_movement = any(
            group.get("movement_id") == movement_id
            and any(
                isinstance(response, dict) and response.get("id") == movement_response_id
                for response in group.get("responses", [])
            )
            for group in _load_json(library_dir / "movement_responses.json").get("entries", [])
            if isinstance(group, dict)
        )
        if not valid_for_movement:
            raise ResonanceArtifactRenderError(
                f"movement_response_id {movement_response_id!r} is not compatible with movement_id {movement_id!r}"
            )

    compatible_scents = scent_response.get("compatible_scent_ids")
    if isinstance(compatible_scents, list) and scent_id not in compatible_scents:
        raise ResonanceArtifactRenderError(
            f"scent_response_id {scent_response_id!r} is not compatible with scent_id {scent_id!r}"
        )

    wish_word = _capitalise_word(_validate_word(return_artifact.get("wish_word"), "wish_word"))
    return_word = _capitalise_word(
        _validate_word(return_artifact.get("return_word"), "return_word")
    )

    stanzas = [
        _artifact_lines(image, str(image_id)),
        ["Around it,"] + _artifact_lines(image_response, str(image_response_id)),
        _artifact_lines(scent, str(scent_id))
        + _artifact_lines(scent_response, str(scent_response_id)),
        _artifact_lines(movement, str(movement_id))
        + _artifact_lines(movement_response, str(movement_response_id)),
        [f"{wish_word} was left here.", f"{return_word} answered."],
    ]

    text = "\n\n".join("\n".join(stanza) for stanza in stanzas)
    return RenderedResonanceArtifact(text=text, library_version=EXPECTED_LIBRARY_VERSION)


def default_library_dir() -> Path:
    return Path(__file__).resolve().parent / "v0_1"
