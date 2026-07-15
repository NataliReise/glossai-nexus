"""Canonical activation profiles for the Nexus 01 Atrium.

Profiles describe which Chamber paths a validated activation opens.  They do
not load private files, render player-facing text, or start a Chamber.

A missing validated profile is represented by ``None`` at this boundary and
therefore produces a sealed Atrium.  Development fixtures may use the same
profile objects, but they are not a third canonical activation type.
"""

from __future__ import annotations

from dataclasses import dataclass

from .state import (
    AtriumState,
    FIRST_SPARK_CHAMBER,
    KNOWN_CHAMBERS,
    RESONANCE_CHAMBER,
)


FIRST_SPARK_PROFILE_ID = "first-spark"
RETURN_RESONANCE_PROFILE_ID = "return-resonance"


class ActivationProfileError(ValueError):
    """Raised when an activation profile contradicts the Nexus structure."""


@dataclass(frozen=True)
class ActivationProfile:
    """Describe the Chamber paths opened by one validated activation."""

    profile_id: str
    enabled_chambers: frozenset[str]

    def __post_init__(self) -> None:
        if not self.profile_id.strip():
            raise ActivationProfileError("Activation profile ID cannot be empty.")

        if not self.enabled_chambers:
            raise ActivationProfileError(
                "An activation profile must enable at least one Chamber."
            )

        unknown = self.enabled_chambers - KNOWN_CHAMBERS
        if unknown:
            raise ActivationProfileError(
                "Activation profile contains unknown Chamber(s): "
                + ", ".join(sorted(unknown))
            )

        if FIRST_SPARK_CHAMBER not in self.enabled_chambers:
            raise ActivationProfileError(
                "Every Nexus 01 activation profile must enable First Spark."
            )


FIRST_SPARK_PROFILE = ActivationProfile(
    profile_id=FIRST_SPARK_PROFILE_ID,
    enabled_chambers=frozenset({FIRST_SPARK_CHAMBER}),
)

RETURN_RESONANCE_PROFILE = ActivationProfile(
    profile_id=RETURN_RESONANCE_PROFILE_ID,
    enabled_chambers=frozenset({FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER}),
)

CANONICAL_PROFILES = {
    FIRST_SPARK_PROFILE.profile_id: FIRST_SPARK_PROFILE,
    RETURN_RESONANCE_PROFILE.profile_id: RETURN_RESONANCE_PROFILE,
}


def profile_from_id(profile_id: str) -> ActivationProfile:
    """Return one canonical profile by exact public ID."""

    try:
        return CANONICAL_PROFILES[profile_id]
    except KeyError as error:
        raise ActivationProfileError(
            f"Unknown Nexus 01 activation profile: {profile_id!r}"
        ) from error


def atrium_state_from_profile(
    profile: ActivationProfile | None,
) -> AtriumState:
    """Translate one validated profile into the initial Atrium state.

    ``None`` means that no valid activation has crossed this boundary.  The
    Nexus is therefore present but sealed.
    """

    if profile is None:
        return AtriumState.sealed()

    return AtriumState.activated(profile.enabled_chambers)
