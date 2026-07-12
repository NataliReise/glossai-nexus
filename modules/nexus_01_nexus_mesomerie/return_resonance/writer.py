"""Compose human-readable Nexus 01 return artifacts."""

from __future__ import annotations

from dataclasses import dataclass

from .token import ResonanceToken

ARTIFACT_VERSION = "N01-RA-GEN-1"
MODULE_NAME = "Nexus 01 - First Spark"


class ReturnArtifactWriteError(ValueError):
    """Raised when chamber output cannot form a valid return artifact."""


@dataclass(frozen=True)
class ResonanceExpression:
    """The five expression values discovered in the Resonance Chamber."""

    carrier_image: str
    carrier_movement: str
    return_word: str
    return_image: str
    return_tone: str

    def __post_init__(self) -> None:
        for field_name in (
            "carrier_image",
            "carrier_movement",
            "return_word",
            "return_image",
            "return_tone",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ReturnArtifactWriteError(
                    f"Resonance expression field '{field_name}' must be non-empty text."
                )
            object.__setattr__(self, field_name, value.strip())


def compose_return_artifact(
    token: ResonanceToken,
    expression: ResonanceExpression,
) -> str:
    """Compose a parseable return artifact from a token and chamber expression."""

    if not token.enables_resonance:
        raise ReturnArtifactWriteError(
            "The resonance token does not enable the Resonance Chamber."
        )

    return f"""NEXUS RETURN ARTIFACT
Version: {ARTIFACT_VERSION}
Module: {MODULE_NAME}
Origin Trace: {token.origin_trace_id}
Return Slot: {token.return_slot_id}
Package: {token.package_id}
Layer: {token.layer_id}

Carrier image:
{expression.carrier_image}

Carrier movement:
{expression.carrier_movement}

Return word:
{expression.return_word}

Return image:
{expression.return_image}

Return tone:
{expression.return_tone}

Privacy:
Do not post this return artifact publicly.
Send it only through the intended private human channel.
"""
