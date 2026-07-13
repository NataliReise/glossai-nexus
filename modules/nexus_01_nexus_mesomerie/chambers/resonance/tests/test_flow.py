#!/usr/bin/env python3
"""Tests for the first deterministic Resonance Chamber flow."""

from __future__ import annotations

from pathlib import Path
import sys

NEXUS_01_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NEXUS_01_ROOT))

from chambers.resonance import (
    ResonanceChamberFlow,
    ResonanceChamberFlowError,
    ScriptedChamberIO,
    build_v0_1_catalog,
)


def _clear_meeting_io() -> ScriptedChamberIO:
    return ScriptedChamberIO(
        choices={
            "image": "waiting-lantern",
            "image_response": "appearing-path",
            "scent": "summer-rain",
            "scent_response": "possibility-of-encounter",
            "movement": "falling-feather",
            "movement_response": "crossing-feather",
        },
        words={
            "wish_word": "courage",
            "return_word": "trust",
        },
    )


def test_complete_flow_returns_shared_selection_contract() -> None:
    result = ResonanceChamberFlow(build_v0_1_catalog()).run(_clear_meeting_io())

    assert result.image_id == "waiting-lantern"
    assert result.image_response_id == "appearing-path"
    assert result.scent_id == "summer-rain"
    assert result.scent_response_id == "possibility-of-encounter"
    assert result.movement_id == "falling-feather"
    assert result.movement_response_id == "crossing-feather"
    assert result.wish_word == "courage"
    assert result.return_word == "trust"


def test_response_options_depend_on_previous_choice() -> None:
    io = _clear_meeting_io()
    io.choices["image_response"] = "shared-silence"

    try:
        ResonanceChamberFlow(build_v0_1_catalog()).run(io)
    except ResonanceChamberFlowError as error:
        assert "not available" in str(error)
    else:
        raise AssertionError("Incompatible image response was accepted.")


def test_unknown_source_choice_is_rejected() -> None:
    io = _clear_meeting_io()
    io.choices["image"] = "unknown-image"

    try:
        ResonanceChamberFlow(build_v0_1_catalog()).run(io)
    except ResonanceChamberFlowError as error:
        assert "not available" in str(error)
    else:
        raise AssertionError("Unknown image choice was accepted.")


def test_words_must_be_single_words() -> None:
    io = _clear_meeting_io()
    io.words["return_word"] = "quiet trust"

    try:
        ResonanceChamberFlow(build_v0_1_catalog()).run(io)
    except ResonanceChamberFlowError as error:
        assert "exactly one word" in str(error)
    else:
        raise AssertionError("Multiple return words were accepted.")


def test_missing_scripted_step_is_explicit() -> None:
    io = _clear_meeting_io()
    del io.choices["movement_response"]

    try:
        ResonanceChamberFlow(build_v0_1_catalog()).run(io)
    except ResonanceChamberFlowError as error:
        assert "movement_response" in str(error)
    else:
        raise AssertionError("Missing scripted step was accepted.")


def main() -> int:
    test_complete_flow_returns_shared_selection_contract()
    test_response_options_depend_on_previous_choice()
    test_unknown_source_choice_is_rejected()
    test_words_must_be_single_words()
    test_missing_scripted_step_is_explicit()
    print("Resonance Chamber flow tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
