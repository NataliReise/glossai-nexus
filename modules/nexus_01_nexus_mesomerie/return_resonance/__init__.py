"""Return Resonance extension layer for Nexus 01.

This package belongs to the Nexus 01 extension layer, not to the
First Spark core.
"""

from .artifact import ReturnArtifact, ReturnArtifactParseError, parse_return_artifact
from .slots import ReturnSlot, ReturnSlotState, load_return_slots
from .matching import MatchResult, MatchStatus, match_return_artifact

__all__ = [
    "MatchResult",
    "MatchStatus",
    "ReturnArtifact",
    "ReturnArtifactParseError",
    "ReturnSlot",
    "ReturnSlotState",
    "load_return_slots",
    "match_return_artifact",
    "parse_return_artifact",
]
