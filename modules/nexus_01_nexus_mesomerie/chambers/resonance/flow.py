"""UI-independent deterministic flow for the Resonance Chamber."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from return_resonance.resonance_render_bridge import ChamberSelections

from .choices import ChoiceCatalog, ChoiceCatalogError


class ResonanceChamberFlowError(ValueError):
    """Raised when the Chamber cannot complete its own mechanical grammar."""


class ChamberIO(Protocol):
    """Small interaction boundary used by terminal and scripted adapters."""

    def choose(self, step: str, option_ids: tuple[str, ...]) -> str:
        ...

    def enter_word(self, step: str) -> str:
        ...


@dataclass
class ScriptedChamberIO:
    """Deterministic adapter for tests and non-interactive demonstrations."""

    choices: dict[str, str]
    words: dict[str, str]

    def choose(self, step: str, option_ids: tuple[str, ...]) -> str:
        try:
            value = self.choices[step]
        except KeyError as error:
            raise ResonanceChamberFlowError(
                f"No scripted choice was provided for step {step!r}."
            ) from error
        if value not in option_ids:
            raise ResonanceChamberFlowError(
                f"Scripted choice {value!r} is not available at step {step!r}."
            )
        return value

    def enter_word(self, step: str) -> str:
        try:
            value = self.words[step]
        except KeyError as error:
            raise ResonanceChamberFlowError(
                f"No scripted word was provided for step {step!r}."
            ) from error
        value = value.strip()
        if not value or len(value.split()) != 1:
            raise ResonanceChamberFlowError(
                f"The word at step {step!r} must contain exactly one word."
            )
        return value


@dataclass(frozen=True)
class ResonanceChamberFlow:
    catalog: ChoiceCatalog

    def run(self, io: ChamberIO) -> ChamberSelections:
        """Run the Chamber's fixed V0.1 grammar and return only its typed result."""

        try:
            image_id = io.choose("image", self.catalog.option_ids("images"))
            self.catalog.require_choice("images", image_id)

            image_response_id = io.choose(
                "image_response",
                self.catalog.image_compatibility.get(image_id, ()),
            )
            self.catalog.require_response("image", image_id, image_response_id)

            scent_id = io.choose("scent", self.catalog.option_ids("scents"))
            self.catalog.require_choice("scents", scent_id)

            scent_response_id = io.choose(
                "scent_response",
                self.catalog.scent_compatibility.get(scent_id, ()),
            )
            self.catalog.require_response("scent", scent_id, scent_response_id)

            movement_id = io.choose("movement", self.catalog.option_ids("movements"))
            self.catalog.require_choice("movements", movement_id)

            movement_response_id = io.choose(
                "movement_response",
                self.catalog.movement_compatibility.get(movement_id, ()),
            )
            self.catalog.require_response(
                "movement", movement_id, movement_response_id
            )

            wish_word = io.enter_word("wish_word")
            return_word = io.enter_word("return_word")
        except ChoiceCatalogError as error:
            raise ResonanceChamberFlowError(str(error)) from error

        return ChamberSelections(
            image_id=image_id,
            image_response_id=image_response_id,
            scent_id=scent_id,
            scent_response_id=scent_response_id,
            movement_id=movement_id,
            movement_response_id=movement_response_id,
            wish_word=wish_word,
            return_word=return_word,
        )
