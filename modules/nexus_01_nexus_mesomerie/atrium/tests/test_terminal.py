"""Tests for the first player-facing Nexus 01 terminal launcher."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


MODULE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE_ROOT))

from atrium import (
    AtriumPhase,
    ChamberRunResult,
    FIRST_SPARK_CHAMBER,
    RESONANCE_CHAMBER,
)
from atrium.terminal import render_atrium, run_nexus_terminal


@dataclass(frozen=True)
class ActivationStub:
    profile_id: str


def scripted_input(commands: list[str]):
    remaining = iter(commands)

    def read(_: str) -> str:
        return next(remaining)

    return read


def test_first_spark_path_completes_and_returns_to_atrium() -> None:
    output: list[str] = []
    calls: list[str] = []

    def run_first_spark() -> ChamberRunResult:
        calls.append(FIRST_SPARK_CHAMBER)
        return ChamberRunResult(completed=True)

    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        first_spark_runner=run_first_spark,
        input_reader=scripted_input(["first-spark", "quit"]),
        output_writer=output.append,
    )

    assert calls == [FIRST_SPARK_CHAMBER]
    assert runtime.state.phase is AtriumPhase.RETURN
    assert runtime.state.is_completed(FIRST_SPARK_CHAMBER)
    assert "You return to the Atrium" in "\n".join(output)


def test_interrupted_first_spark_does_not_change_atrium() -> None:
    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        first_spark_runner=lambda: ChamberRunResult(completed=False),
        input_reader=scripted_input(["first-spark", "quit"]),
        output_writer=lambda _: None,
    )

    assert runtime.state.phase is AtriumPhase.ARRIVAL
    assert not runtime.state.is_completed(FIRST_SPARK_CHAMBER)


def test_return_resonance_profile_shows_both_paths() -> None:
    output: list[str] = []

    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("return-resonance"),
        first_spark_runner=lambda: ChamberRunResult(completed=False),
        input_reader=scripted_input(["look", "quit"]),
        output_writer=output.append,
    )

    assert runtime.state.visible_paths == (FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER)
    rendered = "\n".join(output)
    assert "resonance: open, terminal passage not connected yet" in rendered


def test_help_and_unknown_command_are_handled_locally() -> None:
    output: list[str] = []

    run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        input_reader=scripted_input(["help", "something", "quit"]),
        output_writer=output.append,
    )

    rendered = "\n".join(output)
    assert "enter the First Spark Chamber" in rendered
    assert "Unknown command" in rendered


def test_rendered_return_state_keeps_unfinished_resonance_visible() -> None:
    from atrium import NexusAtriumRuntime

    runtime = NexusAtriumRuntime.from_activation(ActivationStub("return-resonance"))
    runtime.enter_chamber(
        FIRST_SPARK_CHAMBER,
        lambda: ChamberRunResult(completed=True),
    )

    rendered = render_atrium(runtime)
    assert "first-spark: completed" in rendered
    assert "resonance: open, terminal passage not connected yet" in rendered


if __name__ == "__main__":
    test_first_spark_path_completes_and_returns_to_atrium()
    test_interrupted_first_spark_does_not_change_atrium()
    test_return_resonance_profile_shows_both_paths()
    test_help_and_unknown_command_are_handled_locally()
    test_rendered_return_state_keeps_unfinished_resonance_visible()
    print("Nexus Atrium terminal launcher tests passed.")
