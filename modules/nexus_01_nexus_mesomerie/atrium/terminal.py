"""First player-facing terminal launcher for Nexus 01.

The launcher owns only Nexus-level navigation.  Chamber mechanics stay inside
Chamber adapters.  Resonance may already be visible through an activation
profile while remaining intentionally unavailable until its terminal adapter is
connected.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import sys
from typing import Protocol

from .activation_bridge import ActivationProfileSource
from .first_spark_adapter import run_first_spark_chamber
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
        if chamber_id == RESONANCE_CHAMBER:
            marker += ", terminal passage not connected yet"
        lines.append(f"- {chamber_id}: {marker}")

    lines.append("")
    lines.append("Type 'help' for available commands.")
    return "\n".join(lines)


def help_text() -> str:
    return (
        "look         show the current Atrium\n"
        "first-spark  enter the First Spark Chamber\n"
        "quit         leave Nexus 01"
    )


def run_nexus_terminal(
    activation_loader: ActivationLoader = load_nexus_activation,
    first_spark_runner: ChamberRunner = run_first_spark_chamber,
    input_reader: InputReader = input,
    output_writer: OutputWriter = print,
) -> NexusAtriumRuntime:
    """Run the first Nexus terminal path and return its final Atrium runtime."""

    activation = activation_loader()
    runtime = NexusAtriumRuntime.from_activation(activation)
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
        if command == "look":
            output_writer(render_atrium(runtime))
            continue
        if command == "help":
            output_writer(help_text())
            continue
        if command in {"quit", "exit"}:
            output_writer("Leaving Nexus 01.")
            break
        if command in {"first-spark", "first spark"}:
            runtime.enter_chamber(FIRST_SPARK_CHAMBER, first_spark_runner)
            output_writer(render_atrium(runtime))
            continue
        if command in {"resonance", "resonance-chamber"}:
            output_writer(
                "The Resonance path is visible, but its terminal passage is not connected yet."
            )
            continue

        output_writer("Unknown command. Type help to see the current Atrium grammar.")

    return runtime
