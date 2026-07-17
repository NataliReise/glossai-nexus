"""Resonance Chamber mechanical module for Nexus 01."""

from .choices import ChoiceCatalog, ChoiceOption, build_v0_1_catalog
from .composer import ComposedResonanceReturn, compose_resonance_return
from .compose import (
    OriginatingResonanceContribution,
    ResonanceComposeError,
    ResonanceComposeFlow,
    build_resonance_token_v2,
    compose_originating_resonance,
    compose_originating_resonance_terminal,
)
from .flow import (
    ResonanceChamberFlow,
    ResonanceChamberFlowError,
    ScriptedChamberIO,
)
from .terminal_io import TerminalChamberIO

__all__ = [
    "ChoiceCatalog",
    "ChoiceOption",
    "ComposedResonanceReturn",
    "OriginatingResonanceContribution",
    "ResonanceComposeError",
    "ResonanceComposeFlow",
    "ResonanceChamberFlow",
    "ResonanceChamberFlowError",
    "ScriptedChamberIO",
    "TerminalChamberIO",
    "build_v0_1_catalog",
    "build_resonance_token_v2",
    "compose_originating_resonance",
    "compose_originating_resonance_terminal",
    "compose_resonance_return",
]
