"""Tests for the thin activation-to-Atrium boundary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


MODULE_ROOT = Path(__file__).resolve().parents[2]
FIRST_SPARK_ROOT = MODULE_ROOT / "first_spark"
sys.path.insert(0, str(MODULE_ROOT))
sys.path.insert(0, str(FIRST_SPARK_ROOT))

from atrium.activation_bridge import (
    ActivationBridgeError,
    atrium_state_from_activation,
    profile_from_activation,
)
from atrium.profiles import (
    FIRST_SPARK_PROFILE,
    RETURN_RESONANCE_PROFILE,
)
from atrium.state import (
    AtriumPhase,
    FIRST_SPARK_CHAMBER,
    RESONANCE_CHAMBER,
)
from first_spark.activation import activation_from_mapping


@dataclass(frozen=True)
class ProfileSource:
    profile_id: str


def test_legacy_first_spark_activation_crosses_boundary() -> None:
    activation = activation_from_mapping(
        {
            "recipient_alias": "legacy-recipient",
            "activation_purpose": "gift",
            "private_message": "A private legacy message.",
        }
    )

    profile = profile_from_activation(activation)
    state = atrium_state_from_activation(activation)

    assert profile is FIRST_SPARK_PROFILE
    assert state.phase is AtriumPhase.ARRIVAL
    assert state.visible_paths == (FIRST_SPARK_CHAMBER,)


def test_return_resonance_activation_opens_both_paths() -> None:
    activation = activation_from_mapping(
        {
            "profile_id": "return-resonance",
            "recipient_alias": "returning-recipient",
            "activation_purpose": "return",
            "private_message": "A private return message.",
        }
    )

    profile = profile_from_activation(activation)
    state = atrium_state_from_activation(activation)

    assert profile is RETURN_RESONANCE_PROFILE
    assert state.phase is AtriumPhase.ARRIVAL
    assert state.visible_paths == (FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER)


def test_missing_activation_keeps_nexus_sealed() -> None:
    state = atrium_state_from_activation(None)

    assert state.phase is AtriumPhase.SEALED
    assert state.visible_paths == ()
    assert state.unfinished_paths == ()


def test_boundary_rejects_unknown_profile_defensively() -> None:
    activation = ProfileSource(profile_id="unknown-profile")

    try:
        profile_from_activation(activation)
    except ActivationBridgeError as error:
        message = str(error)
        assert "could not be translated" in message
        assert "unknown-profile" in message
    else:
        raise AssertionError("Expected ActivationBridgeError for unknown profile.")


if __name__ == "__main__":
    test_legacy_first_spark_activation_crosses_boundary()
    test_return_resonance_activation_opens_both_paths()
    test_missing_activation_keeps_nexus_sealed()
    test_boundary_rejects_unknown_profile_defensively()
    print("Nexus activation bridge tests passed.")
