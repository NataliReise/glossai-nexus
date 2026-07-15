"""Shared Nexus 01 Atrium state, activation, runtime, and Chamber adapters.

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
from .first_spark_adapter import (
    FirstSparkStateSource,
    FirstSparkTerminalRunner,
    load_first_spark_terminal_runner,
    run_first_spark_chamber,
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
from .terminal import (
    help_text,
    load_nexus_activation,
    render_atrium,
    run_nexus_terminal,
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
    "FirstSparkStateSource",
    "FirstSparkTerminalRunner",
    "NexusAtriumRuntime",
    "RESONANCE_CHAMBER",
    "RETURN_RESONANCE_PROFILE",
    "RETURN_RESONANCE_PROFILE_ID",
    "atrium_state_from_activation",
    "atrium_state_from_profile",
    "help_text",
    "load_first_spark_terminal_runner",
    "load_nexus_activation",
    "profile_from_activation",
    "profile_from_id",
    "render_atrium",
    "run_first_spark_chamber",
    "run_nexus_terminal",
]
