"""Immutable Resonance Token V1/V2 parsing and validation for Nexus 01.

A Token is inert invitation data. Loading or parsing it never activates a Nexus,
modifies a file, consumes the Token, or changes any runtime state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
from typing import Any


TOKEN_VERSION_V1 = "N01-RT-1"
TOKEN_VERSION_V2 = "N01-RT-2"
# Compatibility alias for the current one-person Chamber and gift builder. Those
# callers remain V1 until the later compose/answer and preparation changes.
TOKEN_VERSION = TOKEN_VERSION_V1
TOKEN_TYPE = "resonance-activation"
MODULE_ID = "N01"
LAYER_ID = "return-resonance-1"
LANGUAGE_LIBRARY = "resonance-en-v0.1"
RESONANCE_CHAMBER = "resonance"

IMAGE_IDS = frozenset(
    {
        "waiting-lantern",
        "book-bench",
        "open-starry-window",
        "stone-in-water",
        "bridge-in-mist",
    }
)
SCENT_IDS = frozenset(
    {
        "summer-rain",
        "books-and-cedar",
        "evening-salt",
        "first-snow",
        "warm-bread",
    }
)
MOVEMENT_IDS = frozenset(
    {
        "falling-feather",
        "loosening-knot",
        "returning-tide",
        "opening-circle",
        "crossing-light",
    }
)

_V1_REQUIRED_FIELDS = frozenset(
    {
        "token_version",
        "token_type",
        "module_id",
        "layer_id",
        "origin_trace_id",
        "return_slot_id",
        "package_id",
        "enabled_chambers",
    }
)
_V2_ORIGIN_FIELDS = frozenset(
    {"language_library", "image_id", "scent_id", "movement_id", "wish_word"}
)
_V1_OPTIONAL_FIELDS = frozenset({"public_safe_label", "note"})
_V2_OPTIONAL_FIELDS = frozenset({"public_safe_label"})
_V2_REQUIRED_FIELDS = _V1_REQUIRED_FIELDS | _V2_ORIGIN_FIELDS
_V2_ALLOWED_FIELDS = _V2_REQUIRED_FIELDS | _V2_OPTIONAL_FIELDS
_ANSWER_SIDE_FIELDS = frozenset(
    {"image_response_id", "scent_response_id", "movement_response_id", "return_word"}
)
_SAFE_STRUCTURAL_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}")
_SENTINEL_FRAGMENTS = (
    "CHANGE-ME",
    "CHANGE_ME",
    "CHANGEME",
    "REPLACE-ME",
    "REPLACE_ME",
    "TODO",
    "TBD",
)


class ResonanceTokenLoadError(ValueError):
    """Raised when a resonance token cannot be loaded or validated."""


@dataclass(frozen=True)
class ResonanceToken:
    """Validated immutable invitation data for one Resonance route.

    V1 Tokens contain only structural invitation data. V2 Tokens additionally
    contain the originating person's image, scent, movement, and wish word.
    The V2 fields remain empty only for a successfully parsed legacy V1 Token.
    """

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
    language_library: str = ""
    image_id: str = ""
    scent_id: str = ""
    movement_id: str = ""
    wish_word: str = ""

    @property
    def enables_resonance(self) -> bool:
        return RESONANCE_CHAMBER in self.enabled_chambers

    @property
    def is_legacy(self) -> bool:
        return self.token_version == TOKEN_VERSION_V1

    @property
    def has_originating_contribution(self) -> bool:
        return self.token_version == TOKEN_VERSION_V2

    def to_dict(self) -> dict[str, object]:
        """Return the validated version-specific transport representation."""

        value = asdict(self)
        value["enabled_chambers"] = list(self.enabled_chambers)
        if self.is_legacy:
            for field_name in _V2_ORIGIN_FIELDS:
                value.pop(field_name)
        else:
            value.pop("note")
        for field_name in _V1_OPTIONAL_FIELDS:
            if field_name not in value:
                continue
            if not value[field_name]:
                value.pop(field_name)
        return value

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n"


def load_resonance_token(path: str | Path) -> ResonanceToken:
    """Read one Token without moving, rewriting, consuming, or activating it."""

    token_path = Path(path)
    try:
        raw_text = token_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ResonanceTokenLoadError(
            f"Could not read resonance token as UTF-8: {token_path}"
        ) from error

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise ResonanceTokenLoadError(
            f"Resonance token is not valid JSON: {error.msg}"
        ) from error

    return parse_resonance_token(data)


def parse_resonance_token(data: Any) -> ResonanceToken:
    """Validate a decoded V1 or V2 Token without causing runtime effects."""

    if not isinstance(data, dict):
        raise ResonanceTokenLoadError("Resonance token must be a JSON object.")
    version = _require_non_empty_text(data.get("token_version"), "token_version")
    if version == TOKEN_VERSION_V1:
        return _parse_v1(data)
    if version == TOKEN_VERSION_V2:
        return _parse_v2(data)
    raise ResonanceTokenLoadError(
        f"Unsupported token_version {version!r}; expected "
        f"{TOKEN_VERSION_V1!r} or {TOKEN_VERSION_V2!r}."
    )


def _parse_v1(data: dict[str, Any]) -> ResonanceToken:
    """Read the existing structural Token as an explicit legacy value."""

    _require_fields(data, _V1_REQUIRED_FIELDS)
    common = _parse_common(data)
    return ResonanceToken(
        **common,
        public_safe_label=_optional_text(data.get("public_safe_label", ""), "public_safe_label"),
        note=_optional_text(data.get("note", ""), "note"),
    )


def _parse_v2(data: dict[str, Any]) -> ResonanceToken:
    """Strictly validate a Token containing only the originating contribution."""

    _require_fields(data, _V2_REQUIRED_FIELDS)
    unknown = sorted(set(data) - _V2_ALLOWED_FIELDS)
    if unknown:
        answer_fields = sorted(set(unknown) & _ANSWER_SIDE_FIELDS)
        if answer_fields:
            raise ResonanceTokenLoadError(
                "Resonance Token V2 must not contain answer-side field(s): "
                + ", ".join(answer_fields)
            )
        raise ResonanceTokenLoadError(
            "Resonance Token V2 contains unknown field(s): " + ", ".join(unknown)
        )

    common = _parse_common(data)
    if common["enabled_chambers"] != (RESONANCE_CHAMBER,):
        raise ResonanceTokenLoadError(
            "Resonance Token V2 enabled_chambers must contain only 'resonance'."
        )
    language_library = _require_non_empty_text(
        data["language_library"], "language_library"
    )
    _require_exact(language_library, LANGUAGE_LIBRARY, "language_library")
    image_id = _require_source_id(data["image_id"], "image_id", IMAGE_IDS)
    scent_id = _require_source_id(data["scent_id"], "scent_id", SCENT_IDS)
    movement_id = _require_source_id(
        data["movement_id"], "movement_id", MOVEMENT_IDS
    )
    wish_word = _require_word(data["wish_word"], "wish_word")
    public_safe_label = _optional_text(
        data.get("public_safe_label", ""), "public_safe_label", maximum=80
    )
    for field_name, value in (
        ("language_library", language_library),
        ("image_id", image_id),
        ("scent_id", scent_id),
        ("movement_id", movement_id),
        ("wish_word", wish_word),
        ("public_safe_label", public_safe_label),
    ):
        _reject_template_sentinel(value, field_name)

    return ResonanceToken(
        **common,
        public_safe_label=public_safe_label,
        language_library=language_library,
        image_id=image_id,
        scent_id=scent_id,
        movement_id=movement_id,
        wish_word=wish_word,
    )


def _parse_common(data: dict[str, Any]) -> dict[str, object]:
    text_fields = (
        "token_version",
        "token_type",
        "module_id",
        "layer_id",
        "origin_trace_id",
        "return_slot_id",
        "package_id",
    )
    values = {name: _require_non_empty_text(data[name], name) for name in text_fields}
    enabled_chambers = _require_chamber_list(data["enabled_chambers"])
    _require_exact(values["token_type"], TOKEN_TYPE, "token_type")
    _require_exact(values["module_id"], MODULE_ID, "module_id")
    _require_exact(values["layer_id"], LAYER_ID, "layer_id")
    if RESONANCE_CHAMBER not in enabled_chambers:
        raise ResonanceTokenLoadError(
            "Resonance token must enable the 'resonance' Chamber."
        )
    for field_name in ("origin_trace_id", "return_slot_id", "package_id"):
        _require_route_id(values[field_name], field_name)
    return {**values, "enabled_chambers": enabled_chambers}


def _require_fields(data: dict[str, Any], required: frozenset[str]) -> None:
    missing = sorted(field_name for field_name in required if field_name not in data)
    if missing:
        raise ResonanceTokenLoadError(
            "Resonance token is missing required field(s): " + ", ".join(missing)
        )


def _require_non_empty_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ResonanceTokenLoadError(
            f"Resonance token field {field_name!r} must be non-empty text."
        )
    return value.strip()


def _optional_text(value: Any, field_name: str, maximum: int | None = None) -> str:
    if not isinstance(value, str):
        raise ResonanceTokenLoadError(
            f"Resonance token field {field_name!r} must be text when present."
        )
    cleaned = value.strip()
    if maximum is not None and len(cleaned) > maximum:
        raise ResonanceTokenLoadError(
            f"Resonance token field {field_name!r} must be {maximum} characters or fewer."
        )
    return cleaned


def _require_chamber_list(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ResonanceTokenLoadError(
            "Resonance token field 'enabled_chambers' must be a non-empty list."
        )
    chambers = tuple(
        _require_non_empty_text(chamber, "enabled_chambers") for chamber in value
    )
    if len(chambers) != len(set(chambers)):
        raise ResonanceTokenLoadError(
            "Resonance token field 'enabled_chambers' must not contain duplicates."
        )
    return chambers


def _require_route_id(value: str, field_name: str) -> None:
    if _SAFE_STRUCTURAL_ID.fullmatch(value) is None:
        raise ResonanceTokenLoadError(
            f"Resonance token field {field_name!r} must be one public-safe structural ID."
        )
    _reject_template_sentinel(value, field_name)


def _require_source_id(
    value: Any, field_name: str, supported_ids: frozenset[str]
) -> str:
    cleaned = _require_non_empty_text(value, field_name)
    if cleaned not in supported_ids:
        raise ResonanceTokenLoadError(
            f"Unsupported Resonance Token V2 {field_name}: {cleaned!r}."
        )
    return cleaned


def _require_word(value: Any, field_name: str) -> str:
    cleaned = _require_non_empty_text(value, field_name)
    if any(character.isspace() for character in cleaned):
        raise ResonanceTokenLoadError(
            f"Resonance Token V2 field {field_name!r} must be exactly one word."
        )
    if any(ord(character) < 32 or ord(character) == 127 for character in cleaned):
        raise ResonanceTokenLoadError(
            f"Resonance Token V2 field {field_name!r} contains a control character."
        )
    if len(cleaned) > 80:
        raise ResonanceTokenLoadError(
            f"Resonance Token V2 field {field_name!r} must be 80 characters or fewer."
        )
    return cleaned


def _reject_template_sentinel(value: str, field_name: str) -> None:
    folded = value.upper()
    if any(fragment in folded for fragment in _SENTINEL_FRAGMENTS):
        raise ResonanceTokenLoadError(
            f"Resonance token field {field_name!r} contains a template sentinel."
        )


def _require_exact(actual: str, expected: str, field_name: str) -> None:
    if actual != expected:
        raise ResonanceTokenLoadError(
            f"Unsupported {field_name} {actual!r}; expected {expected!r}."
        )
