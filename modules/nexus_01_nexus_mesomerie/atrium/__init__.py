"""Shared Nexus 01 Atrium state and activation profile models.

The Atrium is one player-facing place with several states.  The current
First Spark ``arrival`` and ``ending`` modules may remain separate
implementations while both are interpreted through these small models.
"""

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
from .state import (
    AtriumPhase,
    AtriumState,
    AtriumStateError,
    FIRST_SPARK_CHAMBER,
    RESONANCE_CHAMBER,
)

__all__ = [
    "ActivationProfile",
    "ActivationProfileError",
    "AtriumPhase",
    "AtriumState",
    "AtriumStateError",
    "FIRST_SPARK_CHAMBER",
    "FIRST_SPARK_PROFILE",
    "FIRST_SPARK_PROFILE_ID",
    "RESONANCE_CHAMBER",
    "RETURN_RESONANCE_PROFILE",
    "RETURN_RESONANCE_PROFILE_ID",
    "atrium_state_from_profile",
    "profile_from_id",
]
