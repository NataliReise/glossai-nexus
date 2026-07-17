"""State-dependent behavior for the one canonical Resonance Chamber."""

from __future__ import annotations

from enum import StrEnum


class ResonanceMode(StrEnum):
    COMPOSE = "COMPOSE"
    ANSWER = "ANSWER"
    BLOCKED_ANSWER_RECOVERY = "BLOCKED_ANSWER_RECOVERY"
