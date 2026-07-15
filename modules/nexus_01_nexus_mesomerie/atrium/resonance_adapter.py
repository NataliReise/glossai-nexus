"""Adapter from the Resonance Chamber composer to the Nexus Atrium runtime.

The Resonance Chamber produces a rich composition result that must remain
available to later local save, matching, and rendering steps. The Atrium,
however, needs only the small ``ChamberRunResult`` completion signal. This
module preserves both sides without moving persistence or route logic into the
Chamber.
"""

from __future__ import annotations

from dataclasses import dataclass

from chambers.resonance.composer import (
    ComposedResonanceReturn,
    compose_resonance_return,
)
from chambers.resonance.flow import ChamberIO
from return_resonance.token import ResonanceToken

from .runtime import ChamberRunResult


@dataclass(frozen=True)
class ResonanceChamberRun:
    """Complete in-memory result of one successful Resonance Chamber visit."""

    chamber_result: ChamberRunResult
    composition: ComposedResonanceReturn


def run_resonance_chamber(
    token: ResonanceToken,
    io: ChamberIO,
) -> ResonanceChamberRun:
    """Run the Chamber composer and preserve its complete in-memory result.

    This adapter does not load or save files, choose output paths, match return
    slots, render artifacts, or change Atrium state. Successful composition is
    the Chamber's completion condition at this boundary.
    """

    composition = compose_resonance_return(token, io)
    return ResonanceChamberRun(
        chamber_result=ChamberRunResult(completed=True),
        composition=composition,
    )


@dataclass
class ResonanceAtriumRunner:
    """Callable Atrium runner that retains the rich Resonance result locally."""

    token: ResonanceToken
    io: ChamberIO
    last_run: ResonanceChamberRun | None = None

    def __call__(self) -> ChamberRunResult:
        """Run Resonance once and expose only completion to the Atrium runtime."""

        self.last_run = run_resonance_chamber(self.token, self.io)
        return self.last_run.chamber_result
