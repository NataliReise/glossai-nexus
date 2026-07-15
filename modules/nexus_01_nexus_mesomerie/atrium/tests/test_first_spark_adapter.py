"""Tests for the First Spark adapter at the Nexus Atrium boundary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


MODULE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE_ROOT))

from atrium import ChamberRunResult, run_first_spark_chamber


@dataclass(frozen=True)
class FinalStateStub:
    message_unlocked: bool


def test_completed_first_spark_becomes_completed_chamber_result() -> None:
    def runner() -> FinalStateStub:
        return FinalStateStub(message_unlocked=True)

    result = run_first_spark_chamber(runner)

    assert result == ChamberRunResult(completed=True)


def test_interrupted_first_spark_remains_incomplete() -> None:
    def runner() -> FinalStateStub:
        return FinalStateStub(message_unlocked=False)

    result = run_first_spark_chamber(runner)

    assert result == ChamberRunResult(completed=False)


def test_adapter_uses_only_message_unlocked_as_completion_signal() -> None:
    @dataclass(frozen=True)
    class RichStateStub:
        current_module: str = "ending"
        spark_linked: bool = True
        should_quit: bool = True
        message_unlocked: bool = False

    result = run_first_spark_chamber(lambda: RichStateStub())

    assert result.completed is False


def test_runner_must_return_observable_first_spark_state() -> None:
    try:
        run_first_spark_chamber(lambda: object())
    except TypeError as error:
        assert "message_unlocked" in str(error)
    else:
        raise AssertionError("Expected TypeError for a runner without message_unlocked.")


def main() -> None:
    test_completed_first_spark_becomes_completed_chamber_result()
    test_interrupted_first_spark_remains_incomplete()
    test_adapter_uses_only_message_unlocked_as_completion_signal()
    test_runner_must_return_observable_first_spark_state()
    print("Nexus First Spark adapter tests passed.")


if __name__ == "__main__":
    main()
