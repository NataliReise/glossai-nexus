#!/usr/bin/env python3
"""Tests for the Resonance Chamber integration composer."""

from __future__ import annotations

from pathlib import Path
import sys

NEXUS_01_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NEXUS_01_ROOT))

from chambers.resonance.composer import compose_resonance_return
from chambers.resonance.flow import ScriptedChamberIO
from return_resonance.resonance_render_bridge import ResonanceRenderBridgeError
from return_resonance.token import (
    LAYER_ID,
    MODULE_ID,
    TOKEN_TYPE,
    TOKEN_VERSION,
    ResonanceToken,
)


def _token(*, enabled_chambers: tuple[str, ...] = ("resonance",)) -> ResonanceToken:
    return ResonanceToken(
        token_version=TOKEN_VERSION,
        token_type=TOKEN_TYPE,
        module_id=MODULE_ID,
        layer_id=LAYER_ID,
        origin_trace_id="n01-composer-test-origin-001",
        return_slot_id="composer-slot-001",
        package_id="composer-package-001",
        enabled_chambers=enabled_chambers,
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


def test_composer_preserves_selections_and_builds_transport_artifact() -> None:
    result = compose_resonance_return(_token(), _clear_meeting_io())

    assert result.selections.image_id == "waiting-lantern"
    assert result.selections.return_word == "trust"
    assert result.artifact.to_dict() == {
        "artifact_version": "0.1",
        "artifact_type": "resonance-return",
        "module_id": "N01",
        "layer_id": "return-resonance-1",
        "origin_trace_id": "n01-composer-test-origin-001",
        "return_slot_id": "composer-slot-001",
        "package_id": "composer-package-001",
        "language_library": "resonance-en-v0.1",
        "image_id": "waiting-lantern",
        "image_response_id": "appearing-path",
        "scent_id": "summer-rain",
        "scent_response_id": "possibility-of-encounter",
        "movement_id": "falling-feather",
        "movement_response_id": "crossing-feather",
        "wish_word": "courage",
        "return_word": "trust",
    }


def test_composer_uses_bridge_validation_for_route_identity() -> None:
    try:
        compose_resonance_return(_token(enabled_chambers=("spark",)), _clear_meeting_io())
    except ResonanceRenderBridgeError as error:
        assert "does not enable" in str(error)
    else:
        raise AssertionError("Composer accepted a token without Resonance activation.")


def test_composer_does_not_write_or_render() -> None:
    result = compose_resonance_return(_token(), _clear_meeting_io())

    assert not hasattr(result, "output")
    assert not hasattr(result, "path")


def main() -> int:
    test_composer_preserves_selections_and_builds_transport_artifact()
    test_composer_uses_bridge_validation_for_route_identity()
    test_composer_does_not_write_or_render()
    print("Resonance Chamber composer tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
