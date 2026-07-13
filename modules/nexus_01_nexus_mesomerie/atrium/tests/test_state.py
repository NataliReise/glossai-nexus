#!/usr/bin/env python3
"""Tests for the minimal Nexus 01 Atrium state model."""

from __future__ import annotations

from pathlib import Path
import sys

NEXUS_01_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_01_ROOT))

from atrium import (
    AtriumPhase,
    AtriumState,
    AtriumStateError,
    FIRST_SPARK_CHAMBER,
    RESONANCE_CHAMBER,
)


def test_sealed_atrium_exposes_no_paths() -> None:
    state = AtriumState.sealed()

    assert state.phase is AtriumPhase.SEALED
    assert state.visible_paths == ()
    assert state.unfinished_paths == ()


def test_first_spark_activation_exposes_one_path() -> None:
    state = AtriumState.activated(frozenset({FIRST_SPARK_CHAMBER}))

    assert state.phase is AtriumPhase.ARRIVAL
    assert state.visible_paths == (FIRST_SPARK_CHAMBER,)
    assert state.unfinished_paths == (FIRST_SPARK_CHAMBER,)
    assert state.is_enabled(FIRST_SPARK_CHAMBER)
    assert not state.is_enabled(RESONANCE_CHAMBER)


def test_resonance_activation_can_expose_two_paths() -> None:
    state = AtriumState.activated(
        frozenset({FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER})
    )

    assert state.visible_paths == (FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER)
    assert state.unfinished_paths == (FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER)


def test_completion_returns_to_changed_atrium() -> None:
    state = AtriumState.activated(
        frozenset({FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER})
    )

    returned = state.after_completion(FIRST_SPARK_CHAMBER)

    assert returned.phase is AtriumPhase.RETURN
    assert returned.visible_paths == (FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER)
    assert returned.unfinished_paths == (RESONANCE_CHAMBER,)
    assert returned.is_completed(FIRST_SPARK_CHAMBER)
    assert not returned.is_completed(RESONANCE_CHAMBER)


def test_unknown_chamber_is_rejected() -> None:
    try:
        AtriumState.activated(frozenset({"unknown"}))
    except AtriumStateError as error:
        assert "unknown enabled Chamber" in str(error)
    else:
        raise AssertionError("Unknown Chamber was accepted.")


def test_completed_chamber_must_be_enabled() -> None:
    try:
        AtriumState(
            phase=AtriumPhase.RETURN,
            enabled_chambers=frozenset({FIRST_SPARK_CHAMBER}),
            completed_chambers=frozenset({RESONANCE_CHAMBER}),
        )
    except AtriumStateError as error:
        assert "cannot be completed unless it is enabled" in str(error)
    else:
        raise AssertionError("Completion outside the activation was accepted.")


def test_sealed_atrium_cannot_expose_paths() -> None:
    try:
        AtriumState(
            phase=AtriumPhase.SEALED,
            enabled_chambers=frozenset({FIRST_SPARK_CHAMBER}),
        )
    except AtriumStateError as error:
        assert "sealed Atrium" in str(error)
    else:
        raise AssertionError("Sealed Atrium exposed an enabled path.")


def main() -> int:
    test_sealed_atrium_exposes_no_paths()
    test_first_spark_activation_exposes_one_path()
    test_resonance_activation_can_expose_two_paths()
    test_completion_returns_to_changed_atrium()
    test_unknown_chamber_is_rejected()
    test_completed_chamber_must_be_enabled()
    test_sealed_atrium_cannot_expose_paths()
    print("Nexus Atrium state tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
