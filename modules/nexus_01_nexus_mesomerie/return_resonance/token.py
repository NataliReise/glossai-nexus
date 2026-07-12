"""Resonance token loading and validation for Nexus 01."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

TOKEN_VERSION = "N01-RT-1"
TOKEN_TYPE = "resonance-activation"
MODULE_ID = "N01"
LAYER_ID = "return-resonance-1"
RESONANCE_CHAMBER = "resonance"


class ResonanceTokenLoadError(ValueError):
    """Raised when a resonance token cannot be loaded or validated."""


@dataclass(frozen=True)
class ResonanceToken:
    """Validated structural token that can make a resonance path available."""

    token_version: str
    token_type: str
    module_id: str
    layer_id: str
    origin_trace_id: str
    return_slot_id: str
    package_id: str
    enabled_chambers: tuple[str, ...]
    public_safe_label: str = ""
    note: str = ""

    @property
    def enables_resonance(self) -> bool:
        """Return True when the token enables the Resonance Chamber."""

        return RESONANCE_CHAMBER in self.enabled_chambers


def load_resonance_token(path: str | Path) -> ResonanceToken:
    """Load and validate one resonance token from a JSON file."""

    token_path = Path(path)
    try:
        raw_text = token_path.read_text(encoding="utf-8")
    except OSError as error:
        raise ResonanceTokenLoadError(
            f"Could not read resonance token: {token_path}"
        ) from error

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise ResonanceTokenLoadError(
            f"Resonance token is not valid JSON: {error.msg}"
        ) from error

    return parse_resonance_token(data)


def parse_resonance_token(data: Any) -> ResonanceToken:
    """Validate a decoded JSON value and return a ResonanceToken."""

    if not isinstance(data, dict):
        raise ResonanceTokenLoadError("Resonance token must be a JSON object.")

    required_text_fields = (
        "token_version",
        "token_type",
        "module_id",
        "layer_id",
        "origin_trace_id",
        "return_slot_id",
        "package_id",
    )
    missing = [name for name in required_text_fields if name not in data]
    if "enabled_chambers" not in data:
        missing.append("enabled_chambers")
    if missing:
        raise ResonanceTokenLoadError(
            "Resonance token is missing required field(s): " + ", ".join(missing)
        )

    values = {
        name: _require_non_empty_text(data[name], name) for name in required_text_fields
    }
    enabled_chambers = _require_chamber_list(data["enabled_chambers"])

    _require_exact(values["token_version"], TOKEN_VERSION, "token_version")
    _require_exact(values["token_type"], TOKEN_TYPE, "token_type")
    _require_exact(values["module_id"], MODULE_ID, "module_id")
    _require_exact(values["layer_id"], LAYER_ID, "layer_id")

    if RESONANCE_CHAMBER not in enabled_chambers:
        raise ResonanceTokenLoadError(
            "Resonance token must enable the 'resonance' Chamber."
        )

    public_safe_label = _optional_text(data.get("public_safe_label", ""), "public_safe_label")
    note = _optional_text(data.get("note", ""), "note")

    return ResonanceToken(
        token_version=values["token_version"],
        token_type=values["token_type"],
        module_id=values["module_id"],
        layer_id=values["layer_id"],
        origin_trace_id=values["origin_trace_id"],
        return_slot_id=values["return_slot_id"],
        package_id=values["package_id"],
        enabled_chambers=enabled_chambers,
        public_safe_label=public_safe_label,
        note=note,
    )


def _require_non_empty_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ResonanceTokenLoadError(
            f"Resonance token field '{field_name}' must be non-empty text."
        )
    return value.strip()


def _optional_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ResonanceTokenLoadError(
            f"Resonance token field '{field_name}' must be text when present."
        )
    return value.strip()


def _require_chamber_list(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ResonanceTokenLoadError(
            "Resonance token field 'enabled_chambers' must be a non-empty list."
        )

    chambers: list[str] = []
    for chamber in value:
        chambers.append(_require_non_empty_text(chamber, "enabled_chambers"))

    if len(chambers) != len(set(chambers)):
        raise ResonanceTokenLoadError(
            "Resonance token field 'enabled_chambers' must not contain duplicates."
        )

    return tuple(chambers)


def _require_exact(actual: str, expected: str, field_name: str) -> None:
    if actual != expected:
        raise ResonanceTokenLoadError(
            f"Unsupported {field_name} {actual!r}; expected {expected!r}."
        )
