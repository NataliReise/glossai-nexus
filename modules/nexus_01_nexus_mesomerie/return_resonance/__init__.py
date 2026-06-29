"""Return Resonance extension layer for Nexus 01.

This package belongs to the Nexus 01 extension layer, not to the
First Spark core.
"""

from .artifact import ReturnArtifact, ReturnArtifactParseError, parse_return_artifact
from .slots import ReturnSlot, ReturnSlotState, load_return_slots
from .matching import MatchResult, MatchStatus, match_return_artifact
from .result import ReturnResult, ReturnResultError, compose_return_result, open_return_result

__all__ = [
    "MatchResult",
    "MatchStatus",
    "ReturnArtifact",
    "ReturnArtifactParseError",
    "ReturnResult",
    "ReturnResultError",
    "ReturnSlot",
    "ReturnSlotState",
    "compose_return_result",
    "load_return_slots",
    "match_return_artifact",
    "open_return_result",
    "parse_return_artifact",
]
