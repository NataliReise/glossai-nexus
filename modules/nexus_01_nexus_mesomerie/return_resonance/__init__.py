"""Return Resonance extension layer for Nexus 01.

This package belongs to the Nexus 01 extension layer, not to the
First Spark core.
"""

from .artifact import ReturnArtifact, ReturnArtifactParseError, parse_return_artifact
from .artifact_store import (
    ResonanceArtifactStoreError,
    write_resonance_return_artifact,
)
from .local_opening import (
    LocalResonanceOpening,
    LocalResonanceOpeningError,
    open_local_resonance_return,
)
from .slots import ReturnSlot, ReturnSlotState, load_return_slots
from .matching import MatchResult, MatchStatus, match_return_artifact
from .result import ReturnResult, ReturnResultError, compose_return_result, open_return_result
from .token import (
    LANGUAGE_LIBRARY,
    TOKEN_VERSION_V1,
    TOKEN_VERSION_V2,
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
    "LocalResonanceOpening",
    "LocalResonanceOpeningError",
    "LANGUAGE_LIBRARY",
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
    "TOKEN_VERSION_V1",
    "TOKEN_VERSION_V2",
    "compose_return_artifact",
    "compose_return_result",
    "load_resonance_token",
    "load_return_slots",
    "match_return_artifact",
    "open_local_resonance_return",
    "open_return_result",
    "parse_resonance_token",
    "parse_return_artifact",
    "write_resonance_return_artifact",
]
