"""Translate validated activation identity into the shared Nexus Atrium state.

This boundary does not load activation files and does not start Chambers.  It
accepts only a small object exposing ``profile_id`` so the standalone First
Spark package does not need to import the shared Atrium implementation.
"""

from __future__ import annotations

from typing import Protocol

from .profiles import (
    ActivationProfile,
    ActivationProfileError,
    atrium_state_from_profile,
    profile_from_id,
)
from .state import AtriumState


class ActivationProfileSource(Protocol):
    """Minimal activation shape required at the Nexus boundary."""

    profile_id: str


class ActivationBridgeError(ValueError):
    """Raised when validated activation identity cannot cross the boundary."""


def profile_from_activation(
    activation: ActivationProfileSource,
) -> ActivationProfile:
    """Resolve one canonical Atrium profile from an activation object."""

    try:
        return profile_from_id(activation.profile_id)
    except ActivationProfileError as error:
        raise ActivationBridgeError(
            "Activation could not be translated into a Nexus 01 profile: "
            f"{activation.profile_id!r}"
        ) from error


def atrium_state_from_activation(
    activation: ActivationProfileSource | None,
) -> AtriumState:
    """Return the initial Atrium state for one activation boundary value.

    ``None`` represents a Nexus for which no validated activation crossed the
    boundary.  The Nexus remains present but sealed.
    """

    if activation is None:
        return atrium_state_from_profile(None)

    return atrium_state_from_profile(profile_from_activation(activation))
