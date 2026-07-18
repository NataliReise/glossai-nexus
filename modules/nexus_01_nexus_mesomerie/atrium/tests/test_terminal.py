"""Tests for the player-facing Nexus 01 terminal launcher."""

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
    ResonanceMode,
)
from atrium.terminal import help_text, render_atrium, run_nexus_terminal


@dataclass(frozen=True)
class ActivationStub:
    profile_id: str
    activation_purpose: str = "gift"


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
        input_reader=scripted_input(["/first-spark", "/quit"]),
        output_writer=output.append,
    )

    assert calls == [FIRST_SPARK_CHAMBER]
    assert runtime.state.phase is AtriumPhase.RETURN
    assert runtime.state.is_completed(FIRST_SPARK_CHAMBER)
    assert runtime.state.is_enabled(RESONANCE_CHAMBER)
    assert "You return to the Atrium" in "\n".join(output)


def test_gift_progression_hides_then_reveals_mode_aware_resonance() -> None:
    output: list[str] = []
    resonance_calls: list[str] = []

    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        first_spark_runner=lambda: ChamberRunResult(completed=True),
        classified_resonance_runner=lambda: (
            resonance_calls.append(RESONANCE_CHAMBER)
            or ChamberRunResult(completed=False)
        ),
        resonance_mode=ResonanceMode.COMPOSE,
        input_reader=scripted_input(
            ["/look", "/resonance", "/first-spark", "/look", "/resonance", "/quit"]
        ),
        output_writer=output.append,
    )

    first_render = output[0]
    assert "first-spark: open" in first_render
    assert "resonance" not in first_render.lower()
    assert "not opened by this activation" in "\n".join(output)
    assert runtime.state.is_completed(FIRST_SPARK_CHAMBER)
    assert "resonance — shape a resonance invitation: open" in "\n".join(output)
    assert resonance_calls == [RESONANCE_CHAMBER]


def test_interrupted_first_spark_does_not_change_atrium() -> None:
    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        first_spark_runner=lambda: ChamberRunResult(completed=False),
        input_reader=scripted_input(["/first-spark", "/quit"]),
        output_writer=lambda _: None,
    )

    assert runtime.state.phase is AtriumPhase.ARRIVAL
    assert not runtime.state.is_completed(FIRST_SPARK_CHAMBER)


def test_return_resonance_profile_shows_both_connected_paths() -> None:
    output: list[str] = []

    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("return-resonance"),
        first_spark_runner=lambda: ChamberRunResult(completed=False),
        input_reader=scripted_input(["/look", "/quit"]),
        output_writer=output.append,
    )

    assert runtime.state.visible_paths == (FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER)
    rendered = "\n".join(output)
    assert "resonance: open" in rendered
    assert "terminal passage not connected" not in rendered


def test_resonance_command_completes_and_returns_to_atrium() -> None:
    calls: list[str] = []

    def run_resonance() -> ChamberRunResult:
        calls.append(RESONANCE_CHAMBER)
        return ChamberRunResult(completed=True)

    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("return-resonance"),
        resonance_runner=run_resonance,
        input_reader=scripted_input(["/resonance", "/quit"]),
        output_writer=lambda _: None,
    )

    assert calls == [RESONANCE_CHAMBER]
    assert runtime.state.phase is AtriumPhase.RETURN
    assert runtime.state.is_completed(RESONANCE_CHAMBER)


def test_unavailable_resonance_does_not_call_runner() -> None:
    calls: list[str] = []

    def run_resonance() -> ChamberRunResult:
        calls.append(RESONANCE_CHAMBER)
        return ChamberRunResult(completed=True)

    output: list[str] = []
    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        resonance_runner=run_resonance,
        input_reader=scripted_input(["/resonance", "/quit"]),
        output_writer=output.append,
    )

    assert calls == []
    assert not runtime.state.is_completed(RESONANCE_CHAMBER)
    assert "not opened by this activation" in "\n".join(output)


def test_help_is_state_dependent_and_unknown_command_is_local() -> None:
    from atrium import NexusAtriumRuntime

    first_spark_runtime = NexusAtriumRuntime.from_activation(ActivationStub("first-spark"))
    resonance_runtime = NexusAtriumRuntime.from_activation(ActivationStub("return-resonance"))

    assert "enter the First Spark Chamber" in help_text(first_spark_runtime)
    assert "enter the Resonance Chamber" not in help_text(first_spark_runtime)
    assert "enter the Resonance Chamber" in help_text(resonance_runtime)

    output: list[str] = []
    run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        input_reader=scripted_input(["something", "/quit"]),
        output_writer=output.append,
    )
    assert "Unknown Atrium command" in "\n".join(output)
    assert "Use /help" in "\n".join(output)


def test_atrium_points_to_help_without_listing_commands() -> None:
    from atrium import NexusAtriumRuntime

    runtime = NexusAtriumRuntime.from_activation(ActivationStub("first-spark"))
    rendered = render_atrium(runtime)

    assert "Available commands: /look, /first-spark, /quit" in rendered
    assert "Use /help for command details." in rendered
    assert "/resonance" not in rendered


def test_rendered_return_state_keeps_unfinished_resonance_visible() -> None:
    from atrium import NexusAtriumRuntime

    runtime = NexusAtriumRuntime.from_activation(ActivationStub("return-resonance"))
    runtime.enter_chamber(
        FIRST_SPARK_CHAMBER,
        lambda: ChamberRunResult(completed=True),
    )

    rendered = render_atrium(runtime)
    assert "first-spark: completed" in rendered
    assert "resonance: open" in rendered


def test_help_and_rendering_use_only_canonical_visible_grammar() -> None:
    from atrium import NexusAtriumRuntime

    first_spark_runtime = NexusAtriumRuntime.from_activation(ActivationStub("first-spark"))
    resonance_runtime = NexusAtriumRuntime.from_activation(ActivationStub("return-resonance"))

    first_help = help_text(first_spark_runtime)
    resonance_help = help_text(resonance_runtime)
    assert "/look         show the current Atrium" in first_help
    assert "/help         show the current Atrium grammar" in first_help
    assert "/first-spark  enter the First Spark Chamber" in first_help
    assert "/quit         leave Nexus 01" in first_help
    assert "/resonance" not in first_help
    assert "/resonance" in resonance_help
    assert all(line.startswith("/") for line in resonance_help.splitlines())

    first_render = render_atrium(first_spark_runtime)
    resonance_render = render_atrium(resonance_runtime)
    assert "Available commands: /look, /first-spark, /quit" in first_render
    assert "/resonance" not in first_render
    assert "Available commands: /look, /first-spark, /resonance, /quit" in resonance_render
    assert "Type 'help'" not in first_render


def test_bare_help_is_an_unadvertised_rescue_alias() -> None:
    output: list[str] = []
    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        input_reader=scripted_input(["/help", "help", "/quit"]),
        output_writer=output.append,
    )

    visible_help = help_text(runtime)
    assert output.count(visible_help) == 2
    assert all(not line.startswith("help ") for line in visible_help.splitlines())
    assert "Available commands: /look, /first-spark, /quit" in output[0]


def test_slash_commands_are_stripped_and_case_normalized() -> None:
    calls: list[str] = []
    output: list[str] = []
    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        first_spark_runner=lambda: (
            calls.append(FIRST_SPARK_CHAMBER) or ChamberRunResult(completed=False)
        ),
        input_reader=scripted_input(
            ["  /LOOK  ", " /HeLp ", "  /First-Spark ", " /QuIt "]
        ),
        output_writer=output.append,
    )

    assert calls == [FIRST_SPARK_CHAMBER]
    assert runtime.state.phase is AtriumPhase.ARRIVAL
    assert output.count(render_atrium(runtime)) >= 2
    assert help_text(runtime) in output
    assert output[-1] == "Leaving Nexus 01."


def test_unknown_slash_is_neutral_and_nonmutating() -> None:
    calls: list[str] = []
    output: list[str] = []
    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        first_spark_runner=lambda: (
            calls.append(FIRST_SPARK_CHAMBER) or ChamberRunResult(completed=True)
        ),
        resonance_runner=lambda: (
            calls.append(RESONANCE_CHAMBER) or ChamberRunResult(completed=True)
        ),
        input_reader=scripted_input(["/unknown", "/quit"]),
        output_writer=output.append,
    )

    unknown = "Unknown Atrium command.\nUse /help to see the commands available here."
    assert calls == []
    assert runtime.state.phase is AtriumPhase.ARRIVAL
    assert runtime.state.completed_chambers == frozenset()
    assert unknown in output
    assert "/unknown" not in unknown


def test_former_bare_commands_are_unknown_and_do_not_dispatch_or_exit() -> None:
    unknown = "Unknown Atrium command.\nUse /help to see the commands available here."
    for former in (
        "look",
        "first-spark",
        "first spark",
        "resonance",
        "resonance-chamber",
        "quit",
        "exit",
    ):
        calls: list[str] = []
        output: list[str] = []
        runtime = run_nexus_terminal(
            activation_loader=lambda: ActivationStub("first-spark"),
            first_spark_runner=lambda: (
                calls.append(FIRST_SPARK_CHAMBER)
                or ChamberRunResult(completed=True)
            ),
            resonance_runner=lambda: (
                calls.append(RESONANCE_CHAMBER)
                or ChamberRunResult(completed=True)
            ),
            input_reader=scripted_input([former, "/quit"]),
            output_writer=output.append,
        )

        assert calls == []
        assert runtime.state.phase is AtriumPhase.ARRIVAL
        assert runtime.state.completed_chambers == frozenset()
        assert output.count(unknown) == 1
        assert output[-1] == "Leaving Nexus 01."
        assert former not in unknown


def test_blank_input_and_ctrl_c_behavior_are_unchanged() -> None:
    blank_output: list[str] = []
    run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        input_reader=scripted_input(["   ", "/quit"]),
        output_writer=blank_output.append,
    )
    assert not any("Unknown Atrium command" in line for line in blank_output)

    interrupted_output: list[str] = []

    def interrupt(_prompt: str) -> str:
        raise KeyboardInterrupt

    runtime = run_nexus_terminal(
        activation_loader=lambda: ActivationStub("first-spark"),
        input_reader=interrupt,
        output_writer=interrupted_output.append,
    )
    assert runtime.state.phase is AtriumPhase.ARRIVAL
    assert "Nexus 01 interrupted. Returning to your terminal." in interrupted_output
    assert "Leaving Nexus 01." not in interrupted_output


if __name__ == "__main__":
    test_first_spark_path_completes_and_returns_to_atrium()
    test_gift_progression_hides_then_reveals_mode_aware_resonance()
    test_interrupted_first_spark_does_not_change_atrium()
    test_return_resonance_profile_shows_both_connected_paths()
    test_resonance_command_completes_and_returns_to_atrium()
    test_unavailable_resonance_does_not_call_runner()
    test_help_is_state_dependent_and_unknown_command_is_local()
    test_atrium_points_to_help_without_listing_commands()
    test_rendered_return_state_keeps_unfinished_resonance_visible()
    test_help_and_rendering_use_only_canonical_visible_grammar()
    test_bare_help_is_an_unadvertised_rescue_alias()
    test_slash_commands_are_stripped_and_case_normalized()
    test_unknown_slash_is_neutral_and_nonmutating()
    test_former_bare_commands_are_unknown_and_do_not_dispatch_or_exit()
    test_blank_input_and_ctrl_c_behavior_are_unchanged()
    print("Nexus Atrium terminal launcher tests passed.")
