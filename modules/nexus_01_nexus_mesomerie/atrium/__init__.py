"""Shared Nexus 01 Atrium state model.

The Atrium is one player-facing place with several states.  The current
First Spark ``arrival`` and ``ending`` modules may remain separate
implementations while both are interpreted through this small model.
"""

from .state import (
    AtriumPhase,
    AtriumState,
    AtriumStateError,
    FIRST_SPARK_CHAMBER,
    RESONANCE_CHAMBER,
)

__all__ = [
    "AtriumPhase",
    "AtriumState",
    "AtriumStateError",
    "FIRST_SPARK_CHAMBER",
    "RESONANCE_CHAMBER",
]
