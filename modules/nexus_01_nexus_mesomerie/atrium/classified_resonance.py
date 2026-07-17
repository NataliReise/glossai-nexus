"""Truthful placeholder entry adapters for classified Resonance modes."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .resonance_mode import ResonanceMode
from .runtime import ChamberRunResult


OutputWriter = Callable[[str], None]


DOOR_LABELS = {
    ResonanceMode.COMPOSE: "begin/send a resonance",
    ResonanceMode.ANSWER: "answer the carried resonance",
    ResonanceMode.BLOCKED_ANSWER_RECOVERY: "the carried invitation needs attention",
}


def resonance_door_label(mode: ResonanceMode) -> str:
    """Return mode-specific wording without changing Chamber identity."""

    return DOOR_LABELS[mode]


@dataclass(frozen=True)
class ClassifiedResonanceController:
    """Keep corrected modes away from the legacy one-person controller."""

    mode: ResonanceMode
    output_writer: OutputWriter = print

    def __call__(self) -> ChamberRunResult:
        if self.mode is ResonanceMode.COMPOSE:
            self.output_writer("Resonance Chamber — begin/send a resonance")
            self.output_writer(
                "Compose mode is ready, but invitation publication is not yet "
                "connected to this Atrium door."
            )
            self.output_writer("No invitation or Return Artifact was created.")
        elif self.mode is ResonanceMode.ANSWER:
            self.output_writer("Resonance Chamber — answer the carried resonance")
            self.output_writer(
                "The selected invitation is valid and ready. The answer form is "
                "not implemented yet."
            )
            self.output_writer("No response choices were collected or saved.")
        else:
            self.output_writer(
                "Resonance Chamber — the carried invitation needs attention"
            )
            self.output_writer(
                "This activation expects its original selected Token V2 context, "
                "but that package-relative context is missing, invalid, altered, "
                "or mismatched."
            )
            self.output_writer(
                "Restore the selected activation context and Token copy from a "
                "trusted backup, or prepare a fresh Nexus activation. Nearby Tokens "
                "will not be selected automatically."
            )
            self.output_writer("Compose and legacy Resonance flows remain unavailable.")
        return ChamberRunResult(completed=False)
