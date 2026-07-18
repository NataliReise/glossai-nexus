"""Player-facing terminal launcher for Nexus 01.

The launcher owns only Nexus-level navigation. Chamber mechanics stay inside
Chamber adapters and their own terminal controllers.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import sys
from typing import Protocol

from .activation_bridge import ActivationProfileSource
from .classified_resonance import (
    ClassifiedResonanceController,
    resonance_door_label,
)
from .first_spark_adapter import run_first_spark_chamber
from .resonance_mode import ResonanceMode
from .resonance_terminal import ResonanceTerminalController
from .runtime import ChamberRunner, NexusAtriumRuntime
from .state import AtriumPhase, FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER


PROMPT = "nexus> "


class ActivationLoader(Protocol):
    def __call__(self) -> ActivationProfileSource: ...


InputReader = Callable[[str], str]
OutputWriter = Callable[[str], None]


def load_nexus_activation() -> ActivationProfileSource:
    """Load the existing local activation through the standalone seed package."""

    package_root = Path(__file__).resolve().parents[1] / "first_spark"
    package_root_text = str(package_root)
    if package_root_text not in sys.path:
        sys.path.insert(0, package_root_text)

    from first_spark.activation import load_activation

    return load_activation()


def render_atrium(runtime: NexusAtriumRuntime) -> str:
    """Render the current Atrium state without interpreting Chamber mechanics."""

    state = runtime.state
    if state.phase is AtriumPhase.SEALED:
        return (
            "Nexus 01 is present, but its paths are sealed.\n"
            "A valid activation is required."
        )

    lines = ["Nexus Atrium"]
    if state.phase is AtriumPhase.ARRIVAL:
        lines.append("The paths opened by this activation are waiting.")
    else:
        lines.append("You return to the Atrium. Its paths now carry your progress.")

    lines.append("")
    lines.append("Visible paths:")
    for chamber_id in state.visible_paths:
        marker = "completed" if state.is_completed(chamber_id) else "open"
        if chamber_id == RESONANCE_CHAMBER and runtime.resonance_mode is not None:
            if runtime.resonance_mode is ResonanceMode.BLOCKED_ANSWER_RECOVERY:
                marker = "blocked — recovery guidance available"
            label = resonance_door_label(runtime.resonance_mode)
            lines.append(f"- {chamber_id} — {label}: {marker}")
        else:
            lines.append(f"- {chamber_id}: {marker}")

    commands = ["/look", "/first-spark"]
    if state.is_enabled(RESONANCE_CHAMBER):
        commands.append("/resonance")
    commands.append("/quit")
    lines.append("")
    lines.append("Available commands: " + ", ".join(commands))
    lines.append("Use /help for command details.")
    return "\n".join(lines)


def help_text(runtime: NexusAtriumRuntime | None = None) -> str:
    lines = [
        "/look         show the current Atrium",
        "/help         show the current Atrium grammar",
        "/first-spark  enter the First Spark Chamber",
    ]
    if runtime is not None and runtime.state.is_enabled(RESONANCE_CHAMBER):
        if runtime.resonance_mode is None:
            lines.append("/resonance     enter the Resonance Chamber")
        else:
            lines.append(
                "/resonance     " + resonance_door_label(runtime.resonance_mode)
            )
    lines.append("/quit         leave Nexus 01")
    return "\n".join(lines)


def run_nexus_terminal(
    activation_loader: ActivationLoader = load_nexus_activation,
    first_spark_runner: ChamberRunner = run_first_spark_chamber,
    resonance_runner: ChamberRunner | None = None,
    input_reader: InputReader = input,
    output_writer: OutputWriter = print,
    resonance_mode: ResonanceMode | None = None,
    classified_resonance_runner: ChamberRunner | None = None,
) -> NexusAtriumRuntime:
    """Run Nexus 01 and return its final Atrium runtime."""

    activation = activation_loader()
    runtime = NexusAtriumRuntime.from_activation(
        activation,
        resonance_mode=resonance_mode,
    )
    if resonance_mode is None:
        active_resonance_runner = resonance_runner or ResonanceTerminalController(
            input_reader=input_reader,
            output_writer=output_writer,
        )
    else:
        active_resonance_runner = (
            classified_resonance_runner
            or ClassifiedResonanceController(
                resonance_mode,
                output_writer=output_writer,
                input_reader=input_reader,
            )
        )
    output_writer(render_atrium(runtime))

    while True:
        try:
            command = input_reader(PROMPT).strip().lower()
        except KeyboardInterrupt:
            output_writer("")
            output_writer("Nexus 01 interrupted. Returning to your terminal.")
            break

        if command == "":
            continue
        if command == "/look":
            output_writer(render_atrium(runtime))
            continue
        if command in {"/help", "help"}:
            output_writer(help_text(runtime))
            continue
        if command == "/quit":
            output_writer("Leaving Nexus 01.")
            break
        if command == "/first-spark":
            runtime.enter_chamber(FIRST_SPARK_CHAMBER, first_spark_runner)
            output_writer(render_atrium(runtime))
            continue
        if command == "/resonance":
            if not runtime.state.is_enabled(RESONANCE_CHAMBER):
                output_writer("The Resonance path is not opened by this activation.")
                continue
            output_writer("")
            output_writer("The Resonance Chamber opens from the Atrium.")
            runtime.enter_chamber(RESONANCE_CHAMBER, active_resonance_runner)
            output_writer(render_atrium(runtime))
            continue

        output_writer(
            "Unknown Atrium command.\n"
            "Use /help to see the commands available here."
        )

    return runtime
