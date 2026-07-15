#!/usr/bin/env python3
"""Tests for the Resonance Chamber to Atrium adapter."""

from __future__ import annotations

from pathlib import Path
import sys

MODULE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE_ROOT))

from atrium import (
    AtriumPhase,
    NexusAtriumRuntime,
    RESONANCE_CHAMBER,
    ResonanceAtriumRunner,
    run_resonance_chamber,
)
from chambers.resonance.flow import ScriptedChamberIO
from return_resonance.token import (
    LAYER_ID,
    MODULE_ID,
    TOKEN_TYPE,
    TOKEN_VERSION,
    ResonanceToken,
)


class ActivationStub:
    profile_id = "return-resonance"


def token() -> ResonanceToken:
    return ResonanceToken(
        token_version=TOKEN_VERSION,
        token_type=TOKEN_TYPE,
        module_id=MODULE_ID,
        layer_id=LAYER_ID,
        origin_trace_id="n01-adapter-test-origin-001",
        return_slot_id="adapter-slot-001",
        package_id="adapter-package-001",
        enabled_chambers=("resonance",),
    )


def scripted_io() -> ScriptedChamberIO:
    return ScriptedChamberIO(
        choices={
            "image": "waiting-lantern",
            "image_response": "appearing-path",
            "scent": "summer-rain",
            "scent_response": "possibility-of-encounter",
            "movement": "falling-feather",
            "movement_response": "crossing-feather",
        },
        words={"wish_word": "courage", "return_word": "trust"},
    )


def test_adapter_preserves_composition_in_memory() -> None:
    result = run_resonance_chamber(token(), scripted_io())

    assert result.chamber_result.completed
    assert result.composition.selections.return_word == "trust"
    assert result.composition.artifact.return_slot_id == "adapter-slot-001"
    assert not hasattr(result, "path")
    assert not hasattr(result, "output")


def test_atrium_runner_exposes_completion_and_retains_rich_result() -> None:
    runtime = NexusAtriumRuntime.from_activation(ActivationStub())
    runner = ResonanceAtriumRunner(token(), scripted_io())

    chamber_result = runtime.enter_chamber(RESONANCE_CHAMBER, runner)

    assert chamber_result.completed
    assert runtime.state.phase is AtriumPhase.RETURN
    assert runtime.state.is_completed(RESONANCE_CHAMBER)
    assert runner.last_run is not None
    assert runner.last_run.composition.artifact.package_id == "adapter-package-001"


def test_runner_starts_without_a_stored_result() -> None:
    runner = ResonanceAtriumRunner(token(), scripted_io())
    assert runner.last_run is None


if __name__ == "__main__":
    test_adapter_preserves_composition_in_memory()
    test_atrium_runner_exposes_completion_and_retains_rich_result()
    test_runner_starts_without_a_stored_result()
    print("Nexus Resonance adapter tests passed.")
