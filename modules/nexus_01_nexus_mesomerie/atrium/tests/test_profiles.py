"""Tests for canonical Nexus 01 activation profiles."""

from __future__ import annotations

from pathlib import Path
import sys


MODULE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE_ROOT))

from atrium.profiles import (
    ActivationProfile,
    ActivationProfileError,
    FIRST_SPARK_PROFILE,
    FIRST_SPARK_PROFILE_ID,
    RETURN_RESONANCE_PROFILE,
    RETURN_RESONANCE_PROFILE_ID,
    atrium_state_from_profile,
    profile_from_id,
)
from atrium.state import (
    AtriumPhase,
    FIRST_SPARK_CHAMBER,
    RESONANCE_CHAMBER,
)


def assert_raises(expected_exception, callback) -> str:
    try:
        callback()
    except expected_exception as error:
        return str(error)
    raise AssertionError(f"Expected {expected_exception.__name__}.")


def test_first_spark_profile() -> None:
    assert FIRST_SPARK_PROFILE.profile_id == FIRST_SPARK_PROFILE_ID
    assert FIRST_SPARK_PROFILE.enabled_chambers == frozenset(
        {FIRST_SPARK_CHAMBER}
    )

    state = atrium_state_from_profile(FIRST_SPARK_PROFILE)
    assert state.phase is AtriumPhase.ARRIVAL
    assert state.visible_paths == (FIRST_SPARK_CHAMBER,)
    assert state.unfinished_paths == (FIRST_SPARK_CHAMBER,)


def test_return_resonance_profile() -> None:
    assert RETURN_RESONANCE_PROFILE.profile_id == RETURN_RESONANCE_PROFILE_ID
    assert RETURN_RESONANCE_PROFILE.enabled_chambers == frozenset(
        {FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER}
    )

    state = atrium_state_from_profile(RETURN_RESONANCE_PROFILE)
    assert state.phase is AtriumPhase.ARRIVAL
    assert state.visible_paths == (FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER)
    assert state.unfinished_paths == (FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER)


def test_missing_profile_seals_atrium() -> None:
    state = atrium_state_from_profile(None)
    assert state.phase is AtriumPhase.SEALED
    assert state.visible_paths == ()
    assert state.unfinished_paths == ()


def test_profile_lookup() -> None:
    assert profile_from_id(FIRST_SPARK_PROFILE_ID) is FIRST_SPARK_PROFILE
    assert profile_from_id(RETURN_RESONANCE_PROFILE_ID) is RETURN_RESONANCE_PROFILE

    message = assert_raises(
        ActivationProfileError,
        lambda: profile_from_id("neutral-demo"),
    )
    assert "Unknown Nexus 01 activation profile" in message


def test_invalid_profiles() -> None:
    message = assert_raises(
        ActivationProfileError,
        lambda: ActivationProfile("", frozenset({FIRST_SPARK_CHAMBER})),
    )
    assert "cannot be empty" in message

    message = assert_raises(
        ActivationProfileError,
        lambda: ActivationProfile("empty", frozenset()),
    )
    assert "at least one Chamber" in message

    message = assert_raises(
        ActivationProfileError,
        lambda: ActivationProfile("unknown", frozenset({FIRST_SPARK_CHAMBER, "x"})),
    )
    assert "unknown Chamber" in message

    message = assert_raises(
        ActivationProfileError,
        lambda: ActivationProfile("resonance-only", frozenset({RESONANCE_CHAMBER})),
    )
    assert "must enable First Spark" in message


if __name__ == "__main__":
    test_first_spark_profile()
    test_return_resonance_profile()
    test_missing_profile_seals_atrium()
    test_profile_lookup()
    test_invalid_profiles()
    print("Nexus Atrium activation profile tests passed.")
