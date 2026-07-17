"""Pure compose/initiate boundary for the single Resonance Chamber."""

from __future__ import annotations

from dataclasses import dataclass

from return_resonance.token import (
    IMAGE_IDS,
    LANGUAGE_LIBRARY,
    MOVEMENT_IDS,
    RESONANCE_CHAMBER,
    SCENT_IDS,
    TOKEN_TYPE,
    TOKEN_VERSION_V2,
    ResonanceToken,
    ResonanceTokenLoadError,
    parse_resonance_token,
    validate_originating_wish_word,
)

from .choices import ChoiceCatalog, ChoiceCatalogError, build_v0_1_catalog
from .flow import ChamberIO
from .terminal_io import InputFunction, OutputFunction, TerminalChamberIO


class ResonanceComposeError(ValueError):
    """Raised when an originating contribution cannot be composed safely."""


@dataclass(frozen=True)
class OriginatingResonanceContribution:
    """The originating person's complete, immutable contribution."""

    image_id: str
    scent_id: str
    movement_id: str
    wish_word: str

    def __post_init__(self) -> None:
        _require_source_id(self.image_id, "image_id", IMAGE_IDS)
        _require_source_id(self.scent_id, "scent_id", SCENT_IDS)
        _require_source_id(self.movement_id, "movement_id", MOVEMENT_IDS)
        try:
            cleaned = validate_originating_wish_word(self.wish_word)
        except ResonanceTokenLoadError as error:
            raise ResonanceComposeError(str(error)) from error
        object.__setattr__(self, "wish_word", cleaned)


@dataclass(frozen=True)
class ResonanceComposeFlow:
    """Collect only source choices and one wish word through a Chamber IO."""

    catalog: ChoiceCatalog

    def run(self, io: ChamberIO) -> OriginatingResonanceContribution:
        try:
            image_id = io.choose("image", self.catalog.option_ids("images"))
            self.catalog.require_choice("images", image_id)
            scent_id = io.choose("scent", self.catalog.option_ids("scents"))
            self.catalog.require_choice("scents", scent_id)
            movement_id = io.choose("movement", self.catalog.option_ids("movements"))
            self.catalog.require_choice("movements", movement_id)
            wish_word = io.enter_word("wish_word")
            return OriginatingResonanceContribution(
                image_id=image_id,
                scent_id=scent_id,
                movement_id=movement_id,
                wish_word=wish_word,
            )
        except (ChoiceCatalogError, ResonanceTokenLoadError) as error:
            raise ResonanceComposeError(str(error)) from error


def compose_originating_resonance(
    io: ChamberIO,
    catalog: ChoiceCatalog | None = None,
) -> OriginatingResonanceContribution:
    """Run the compose core with an injected interaction adapter."""

    return ResonanceComposeFlow(catalog or build_v0_1_catalog()).run(io)


def compose_originating_resonance_terminal(
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
    catalog: ChoiceCatalog | None = None,
) -> OriginatingResonanceContribution:
    """Run the compose core using the existing terminal presentation style."""

    selected_catalog = catalog or build_v0_1_catalog()
    return compose_originating_resonance(
        TerminalChamberIO(selected_catalog, input_fn, output_fn),
        selected_catalog,
    )


def build_resonance_token_v2(
    contribution: OriginatingResonanceContribution,
    *,
    module_id: str,
    layer_id: str,
    origin_trace_id: str,
    return_slot_id: str,
    package_id: str,
    public_safe_label: str = "",
) -> ResonanceToken:
    """Combine validated compose data with an externally supplied route."""

    if not isinstance(contribution, OriginatingResonanceContribution):
        raise ResonanceComposeError(
            "Token V2 construction requires a validated originating contribution."
        )
    mapping: dict[str, object] = {
        "token_version": TOKEN_VERSION_V2,
        "token_type": TOKEN_TYPE,
        "module_id": module_id,
        "layer_id": layer_id,
        "origin_trace_id": origin_trace_id,
        "return_slot_id": return_slot_id,
        "package_id": package_id,
        "language_library": LANGUAGE_LIBRARY,
        "enabled_chambers": [RESONANCE_CHAMBER],
        "image_id": contribution.image_id,
        "scent_id": contribution.scent_id,
        "movement_id": contribution.movement_id,
        "wish_word": contribution.wish_word,
    }
    if public_safe_label:
        mapping["public_safe_label"] = public_safe_label
    try:
        return parse_resonance_token(mapping)
    except ResonanceTokenLoadError as error:
        raise ResonanceComposeError(str(error)) from error


def _require_source_id(
    value: object,
    field_name: str,
    supported_ids: frozenset[str],
) -> None:
    if not isinstance(value, str) or value not in supported_ids:
        raise ResonanceComposeError(f"Unsupported originating {field_name}: {value!r}.")
