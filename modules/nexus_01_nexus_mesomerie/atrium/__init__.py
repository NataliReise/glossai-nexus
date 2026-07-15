"""Shared Nexus 01 Atrium state, activation, and runtime models.

The Atrium is one player-facing place with several states.  The current
First Spark ``arrival`` and ``ending`` modules may remain separate
implementations while both are interpreted through these small models.
"""

from .activation_bridge import (
    ActivationBridgeError,
    ActivationProfileSource,
    atrium_state_from_activation,
    profile_from_activation,
)
from .profiles import (
    ActivationProfile,
    ActivationProfileError,
    FIRST_SPARK_PROFILE,
    FIRST_SPARK_PROFILE_ID,
    RETURN_RESONANCE_PROFILE,
    RETURN_RESONANCE_PROFILE_ID,
    atrium_state_from_profile,
    profile_from_id,
)
from .runtime import (
    AtriumRuntimeError,
    ChamberRunResult,
    ChamberRunner,
    NexusAtriumRuntime,
)
from .state import (
    AtriumPhase,
    AtriumState,
    AtriumStateError,
    FIRST_SPARK_CHAMBER,
    RESONANCE_CHAMBER,
)

__all__ = [
    "ActivationBridgeError",
    "ActivationProfile",
    "ActivationProfileError",
    "ActivationProfileSource",
    "AtriumPhase",
    "AtriumRuntimeError",
    "AtriumState",
    "AtriumStateError",
    "ChamberRunResult",
    "ChamberRunner",
    "FIRST_SPARK_CHAMBER",
    "FIRST_SPARK_PROFILE",
    "FIRST_SPARK_PROFILE_ID",
    "NexusAtriumRuntime",
    "RESONANCE_CHAMBER",
    "RETURN_RESONANCE_PROFILE",
    "RETURN_RESONANCE_PROFILE_ID",
    "atrium_state_from_activation",
    "atrium_state_from_profile",
    "profile_from_activation",
    "profile_from_id",
]
