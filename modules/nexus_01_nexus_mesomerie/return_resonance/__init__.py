"""Return Resonance extension layer for Nexus 01.

This package belongs to the Nexus 01 extension layer, not to the
First Spark core.
"""

from .artifact import ReturnArtifact, ReturnArtifactParseError, parse_return_artifact
from .artifact_store import (
    ResonanceArtifactStoreError,
    write_resonance_return_artifact,
)
from .slots import ReturnSlot, ReturnSlotState, load_return_slots
from .matching import MatchResult, MatchStatus, match_return_artifact
from .result import ReturnResult, ReturnResultError, compose_return_result, open_return_result
from .token import (
    ResonanceToken,
    ResonanceTokenLoadError,
    load_resonance_token,
    parse_resonance_token,
)
from .writer import (
    ResonanceExpression,
    ReturnArtifactWriteError,
    compose_return_artifact,
)

__all__ = [
    "MatchResult",
    "MatchStatus",
    "ResonanceArtifactStoreError",
    "ResonanceExpression",
    "ResonanceToken",
    "ResonanceTokenLoadError",
    "ReturnArtifact",
    "ReturnArtifactParseError",
    "ReturnArtifactWriteError",
    "ReturnResult",
    "ReturnResultError",
    "ReturnSlot",
    "ReturnSlotState",
    "compose_return_artifact",
    "compose_return_result",
    "load_resonance_token",
    "load_return_slots",
    "match_return_artifact",
    "open_return_result",
    "parse_resonance_token",
    "parse_return_artifact",
    "write_resonance_return_artifact",
]
