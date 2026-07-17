"""Tests for the minimal Nexus 01 Atrium runtime wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


MODULE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE_ROOT))

from atrium import (
    AtriumPhase,
    AtriumRuntimeError,
    ChamberRunResult,
    FIRST_SPARK_CHAMBER,
    NexusAtriumRuntime,
    RESONANCE_CHAMBER,
)


@dataclass(frozen=True)
class ActivationStub:
    profile_id: str
    activation_purpose: str = "gift"


def test_first_spark_activation_opens_only_first_spark() -> None:
    runtime = NexusAtriumRuntime.from_activation(ActivationStub("first-spark"))

    assert runtime.state.phase is AtriumPhase.ARRIVAL
    assert runtime.state.visible_paths == (FIRST_SPARK_CHAMBER,)

    calls: list[str] = []

    def run_first_spark() -> ChamberRunResult:
        calls.append("first-spark")
        return ChamberRunResult(completed=True)

    result = runtime.enter_chamber(FIRST_SPARK_CHAMBER, run_first_spark)

    assert result.completed
    assert calls == ["first-spark"]
    assert runtime.state.phase is AtriumPhase.RETURN
    assert runtime.state.is_completed(FIRST_SPARK_CHAMBER)
    assert runtime.state.is_enabled(RESONANCE_CHAMBER)


def test_non_gift_first_spark_completion_does_not_add_resonance() -> None:
    runtime = NexusAtriumRuntime.from_activation(
        ActivationStub("first-spark", activation_purpose="development")
    )

    runtime.enter_chamber(
        FIRST_SPARK_CHAMBER,
        lambda: ChamberRunResult(completed=True),
    )

    assert not runtime.state.is_enabled(RESONANCE_CHAMBER)


def test_unfinished_visit_leaves_atrium_unchanged() -> None:
    runtime = NexusAtriumRuntime.from_activation(ActivationStub("first-spark"))
    original_state = runtime.state

    result = runtime.enter_chamber(
        FIRST_SPARK_CHAMBER,
        lambda: ChamberRunResult(completed=False),
    )

    assert not result.completed
    assert runtime.state == original_state
    assert runtime.state.phase is AtriumPhase.ARRIVAL


def test_return_resonance_activation_exposes_both_paths() -> None:
    runtime = NexusAtriumRuntime.from_activation(
        ActivationStub("return-resonance")
    )

    assert runtime.state.visible_paths == (
        FIRST_SPARK_CHAMBER,
        RESONANCE_CHAMBER,
    )

    runtime.enter_chamber(
        FIRST_SPARK_CHAMBER,
        lambda: ChamberRunResult(completed=True),
    )

    assert runtime.state.is_completed(FIRST_SPARK_CHAMBER)
    assert runtime.state.unfinished_paths == (RESONANCE_CHAMBER,)


def test_disabled_and_unknown_paths_are_rejected_before_runner_call() -> None:
    runtime = NexusAtriumRuntime.from_activation(ActivationStub("first-spark"))
    called = False

    def runner() -> ChamberRunResult:
        nonlocal called
        called = True
        return ChamberRunResult(completed=True)

    try:
        runtime.enter_chamber(RESONANCE_CHAMBER, runner)
    except AtriumRuntimeError as error:
        assert "not enabled" in str(error)
    else:
        raise AssertionError("Expected disabled Resonance path to be rejected.")

    assert not called

    try:
        runtime.enter_chamber("unknown-room", runner)
    except AtriumRuntimeError as error:
        assert "Unknown Nexus 01 Chamber" in str(error)
    else:
        raise AssertionError("Expected unknown Chamber to be rejected.")

    assert not called


def test_runner_contract_is_checked() -> None:
    runtime = NexusAtriumRuntime.from_activation(ActivationStub("first-spark"))

    try:
        runtime.enter_chamber(FIRST_SPARK_CHAMBER, lambda: True)  # type: ignore[arg-type,return-value]
    except AtriumRuntimeError as error:
        assert "must return ChamberRunResult" in str(error)
    else:
        raise AssertionError("Expected invalid runner result to be rejected.")


def test_missing_activation_creates_sealed_runtime() -> None:
    runtime = NexusAtriumRuntime.from_activation(None)

    assert runtime.state.phase is AtriumPhase.SEALED
    assert runtime.state.visible_paths == ()

    try:
        runtime.enter_chamber(
            FIRST_SPARK_CHAMBER,
            lambda: ChamberRunResult(completed=True),
        )
    except AtriumRuntimeError as error:
        assert "not enabled" in str(error)
    else:
        raise AssertionError("Expected sealed Atrium to reject Chamber entry.")


if __name__ == "__main__":
    test_first_spark_activation_opens_only_first_spark()
    test_non_gift_first_spark_completion_does_not_add_resonance()
    test_unfinished_visit_leaves_atrium_unchanged()
    test_return_resonance_activation_exposes_both_paths()
    test_disabled_and_unknown_paths_are_rejected_before_runner_call()
    test_runner_contract_is_checked()
    test_missing_activation_creates_sealed_runtime()
    print("Nexus Atrium runtime wrapper tests passed.")
