"""Thin integration boundary from Chamber flow to transport artifact."""

from __future__ import annotations

from dataclasses import dataclass

from return_resonance.resonance_render_bridge import (
    ChamberSelections,
    ResonanceReturnArtifact,
    build_resonance_return_artifact,
)
from return_resonance.token import ResonanceToken

from .choices import ChoiceCatalog, build_v0_1_catalog
from .flow import ChamberIO, ResonanceChamberFlow


@dataclass(frozen=True)
class ComposedResonanceReturn:
    """Explicitly preserve both sides of the Chamber boundary."""

    selections: ChamberSelections
    artifact: ResonanceReturnArtifact


def compose_resonance_return(
    token: ResonanceToken,
    io: ChamberIO,
    catalog: ChoiceCatalog | None = None,
) -> ComposedResonanceReturn:
    """Run the Chamber grammar, then join its result to validated route identity.

    This function deliberately does not read or write files, render poetry, match a
    Return Slot, or manage Atrium state. It is only the narrow integration seam
    between the Chamber-owned flow and the shared transport contract.
    """

    active_catalog = catalog if catalog is not None else build_v0_1_catalog()
    selections = ResonanceChamberFlow(active_catalog).run(io)
    artifact = build_resonance_return_artifact(token, selections)
    return ComposedResonanceReturn(selections=selections, artifact=artifact)
