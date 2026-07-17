"""Bridge Return Resonance transport identity to the local rendering pipeline.

The bridge keeps the existing human-readable Return Artifact implementation intact.
It defines a parallel JSON contract for stable Chamber selections, verifies Return
Slot matching through the existing matcher, and only then opens both poetic outputs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any
import unicodedata

from resonance_language_library.render_resonance_output import (
    RenderedResonanceOutput,
    ResonanceOutputRenderError,
    render_resonance_output,
)

from .artifact import ReturnArtifact
from .matching import MatchResult, match_return_artifact
from .slots import ReturnSlot
from .token import (
    LAYER_ID,
    MODULE_ID,
    ResonanceToken,
    ResonanceTokenLoadError,
    validate_originating_wish_word,
)

ARTIFACT_VERSION = "0.1"
ARTIFACT_TYPE = "resonance-return"
LANGUAGE_LIBRARY = "resonance-en-v0.1"


class ResonanceRenderBridgeError(ValueError):
    """Raised when the shared Resonance Return Artifact is invalid or cannot open."""


@dataclass(frozen=True)
class ChamberSelections:
    """Stable, public-safe Chamber selections used by the local renderers."""

    image_id: str
    image_response_id: str
    scent_id: str
    scent_response_id: str
    movement_id: str
    movement_response_id: str
    wish_word: str
    return_word: str

    def __post_init__(self) -> None:
        for field_name, value in asdict(self).items():
            if not isinstance(value, str) or not value.strip():
                raise ResonanceRenderBridgeError(
                    f"Chamber selection field {field_name!r} must be non-empty text."
                )
            object.__setattr__(self, field_name, value.strip())


@dataclass(frozen=True)
class ResonanceReturnArtifact:
    """Shared V0.1 transport artifact joining route and Chamber selections."""

    artifact_version: str
    artifact_type: str
    module_id: str
    layer_id: str
    origin_trace_id: str
    return_slot_id: str
    package_id: str
    language_library: str
    image_id: str
    image_response_id: str
    scent_id: str
    scent_response_id: str
    movement_id: str
    movement_response_id: str
    wish_word: str
    return_word: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n"

    def to_matching_artifact(self) -> ReturnArtifact:
        """Adapt only route identity to the existing slot matcher."""

        return ReturnArtifact(
            version=self.artifact_version,
            module=self.module_id,
            origin_trace_id=self.origin_trace_id,
            return_slot_id=self.return_slot_id,
            package_id=self.package_id,
            layer_id=self.layer_id,
            return_word=self.return_word,
        )


@dataclass(frozen=True)
class OpenedResonanceReturn:
    artifact: ResonanceReturnArtifact
    match: MatchResult
    output: RenderedResonanceOutput


def build_resonance_return_artifact(
    token: ResonanceToken,
    selections: ChamberSelections,
) -> ResonanceReturnArtifact:
    """Join validated route identity from a token with stable Chamber selections."""

    if not token.enables_resonance:
        raise ResonanceRenderBridgeError(
            "The Resonance Token does not enable the Resonance Chamber."
        )
    if token.module_id != MODULE_ID:
        raise ResonanceRenderBridgeError(
            f"Unsupported module_id {token.module_id!r}; expected {MODULE_ID!r}."
        )
    if token.layer_id != LAYER_ID:
        raise ResonanceRenderBridgeError(
            f"Unsupported layer_id {token.layer_id!r}; expected {LAYER_ID!r}."
        )

    return ResonanceReturnArtifact(
        artifact_version=ARTIFACT_VERSION,
        artifact_type=ARTIFACT_TYPE,
        module_id=token.module_id,
        layer_id=token.layer_id,
        origin_trace_id=token.origin_trace_id,
        return_slot_id=token.return_slot_id,
        package_id=token.package_id,
        language_library=LANGUAGE_LIBRARY,
        **asdict(selections),
    )


def parse_resonance_return_artifact(value: Any) -> ResonanceReturnArtifact:
    """Validate a decoded shared artifact without inferring or rewriting meaning."""

    if not isinstance(value, dict):
        raise ResonanceRenderBridgeError("Resonance Return Artifact must be a JSON object.")

    field_names = tuple(ResonanceReturnArtifact.__dataclass_fields__)
    missing = [name for name in field_names if name not in value]
    if missing:
        raise ResonanceRenderBridgeError(
            "Resonance Return Artifact is missing required field(s): " + ", ".join(missing)
        )

    unknown = sorted(set(value) - set(field_names))
    if unknown:
        raise ResonanceRenderBridgeError(
            "Resonance Return Artifact contains unknown field(s): " + ", ".join(unknown)
        )

    cleaned: dict[str, str] = {}
    for field_name in field_names:
        field_value = value[field_name]
        if not isinstance(field_value, str) or not field_value.strip():
            raise ResonanceRenderBridgeError(
                f"Resonance Return Artifact field {field_name!r} must be non-empty text."
            )
        cleaned[field_name] = field_value.strip()

    _require_exact(cleaned["artifact_version"], ARTIFACT_VERSION, "artifact_version")
    _require_exact(cleaned["artifact_type"], ARTIFACT_TYPE, "artifact_type")
    _require_exact(cleaned["module_id"], MODULE_ID, "module_id")
    _require_exact(cleaned["layer_id"], LAYER_ID, "layer_id")
    _require_exact(cleaned["language_library"], LANGUAGE_LIBRARY, "language_library")
    cleaned["wish_word"] = _require_free_word(cleaned["wish_word"], "wish_word")
    cleaned["return_word"] = _require_free_word(cleaned["return_word"], "return_word")

    return ResonanceReturnArtifact(**cleaned)


def load_resonance_return_artifact(path: str | Path) -> ResonanceReturnArtifact:
    artifact_path = Path(path)
    try:
        data = json.loads(artifact_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ResonanceRenderBridgeError(
            f"Could not read Resonance Return Artifact: {artifact_path}"
        ) from error
    except json.JSONDecodeError as error:
        raise ResonanceRenderBridgeError(
            f"Resonance Return Artifact is not valid JSON: {error.msg}"
        ) from error
    return parse_resonance_return_artifact(data)


def open_resonance_return(
    artifact: ResonanceReturnArtifact,
    slots: list[ReturnSlot],
    library_dir: Path,
) -> OpenedResonanceReturn:
    """Match the route first, then render both local poetic outputs."""

    match = match_return_artifact(artifact.to_matching_artifact(), slots)
    if not match.is_match:
        raise ResonanceRenderBridgeError(
            f"Resonance Return Artifact cannot open: {match.status.value}: {match.message}"
        )
    if match.slot is None:
        raise ResonanceRenderBridgeError(
            "Resonance Return Artifact matched without a local Return Slot."
        )
    if artifact.module_id != match.slot.module_id:
        raise ResonanceRenderBridgeError(
            "Resonance Return Artifact cannot open: module_mismatch: "
            "the artifact does not match the module for this slot."
        )

    try:
        output = render_resonance_output(artifact.to_dict(), library_dir)
    except ResonanceOutputRenderError as error:
        raise ResonanceRenderBridgeError(
            f"Resonance Return Artifact matched but could not render: {error}"
        ) from error

    return OpenedResonanceReturn(artifact=artifact, match=match, output=output)


def _require_exact(actual: str, expected: str, field_name: str) -> None:
    if actual != expected:
        raise ResonanceRenderBridgeError(
            f"Unsupported {field_name} {actual!r}; expected {expected!r}."
        )


def _require_free_word(value: str, field_name: str) -> str:
    """Apply the established Token/answer word contract to untrusted artifacts."""

    try:
        cleaned = validate_originating_wish_word(value)
    except ResonanceTokenLoadError as error:
        raise ResonanceRenderBridgeError(
            str(error).replace("wish_word", field_name)
        ) from error
    if any(unicodedata.category(character) == "Cc" for character in cleaned):
        raise ResonanceRenderBridgeError(
            f"Resonance Return Artifact field {field_name!r} contains a control character."
        )
    return cleaned
