"""Terminal adapter for the Resonance Chamber interaction boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .choices import ChoiceCatalog, ChoiceCatalogError


InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]


class ChamberInteractionCancelled(RuntimeError):
    """Raised only when an interaction explicitly enables cancellation."""


STEP_TITLES = {
    "image": "Choose an image",
    "image_response": "Choose what answers the image",
    "scent": "Choose a scent",
    "scent_response": "Choose what the scent carries",
    "movement": "Choose a movement",
    "movement_response": "Choose what answers the movement",
    "wish_word": "Leave one wish word",
    "return_word": "Leave one return word",
}


@dataclass
class TerminalChamberIO:
    """Human-facing terminal adapter that keeps internal IDs out of sight."""

    catalog: ChoiceCatalog
    input_fn: InputFunction = input
    output_fn: OutputFunction = print
    allow_cancel: bool = False

    def choose(self, step: str, option_ids: tuple[str, ...]) -> str:
        if not option_ids:
            raise ChoiceCatalogError(f"No options are available at step {step!r}.")

        labels = tuple(self._label_for(option_id) for option_id in option_ids)
        self.output_fn("")
        self.output_fn(STEP_TITLES.get(step, "Choose one path"))
        self.output_fn("-" * len(STEP_TITLES.get(step, "Choose one path")))
        for index, label in enumerate(labels, start=1):
            self.output_fn(f"{index}. {label}")

        while True:
            raw_value = self.input_fn("Enter a number: ").strip()
            if self.allow_cancel and raw_value.casefold() == "/cancel":
                raise ChamberInteractionCancelled("Chamber interaction cancelled.")
            try:
                index = int(raw_value)
            except ValueError:
                self.output_fn("Please enter one of the numbers shown above.")
                continue

            if 1 <= index <= len(option_ids):
                return option_ids[index - 1]

            self.output_fn("Please enter one of the numbers shown above.")

    def enter_word(self, step: str) -> str:
        self.output_fn("")
        self.output_fn(STEP_TITLES.get(step, "Leave one word"))
        self.output_fn("-" * len(STEP_TITLES.get(step, "Leave one word")))

        while True:
            value = self.input_fn("Enter exactly one word: ").strip()
            if self.allow_cancel and value.casefold() == "/cancel":
                raise ChamberInteractionCancelled("Chamber interaction cancelled.")
            if value and len(value.split()) == 1:
                return value
            self.output_fn("Please enter exactly one non-empty word.")

    def _label_for(self, option_id: str) -> str:
        for kind in (
            "images",
            "image_responses",
            "scents",
            "scent_responses",
            "movements",
            "movement_responses",
        ):
            for option in getattr(self.catalog, kind):
                if option.id == option_id:
                    return option.label
        raise ChoiceCatalogError(f"No player-facing label exists for option {option_id!r}.")
