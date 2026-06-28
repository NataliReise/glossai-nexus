"""Spark chamber module for Nexus 0.1 - First Spark."""

from __future__ import annotations

from first_spark.module_response import ModuleResponse
from first_spark.state import GameState


VISIBLE_TRACES = {
    "welcome.log": """[first-spark / welcome.log]

The chamber is small on purpose.
A spark does not need to become a system before it can glow.

Visible instruction:
  Try: read spark.note
""",
    "spark.note": """[first-spark / spark.note]

This Nexus has been activated as a gift.
The private message is present, but still locked.

Next trace:
  Fragment logic has not been installed yet.
""",
}


HELP_TEXT = """Available commands:
  help                 Show this help text.
  look                 Look around the First Spark chamber.
  read <trace-name>    Read a visible trace.
  quit                 Exit First Spark.
"""


LOOK_TEXT = """You are inside the First Spark chamber.

Visible traces:
  welcome.log
  spark.note

The private message is still locked.
"""


def handle_command(command: str, state: GameState) -> ModuleResponse:
    """Handle commands inside the First Spark chamber."""
    if command == "help":
        return ModuleResponse(HELP_TEXT.strip())

    if command == "look":
        return ModuleResponse(LOOK_TEXT.strip())

    if command.startswith("read "):
        trace_name = command.removeprefix("read ").strip()
        if not trace_name:
            return ModuleResponse("Usage: read <trace-name>\nType 'look' to see visible traces.")
        return read_trace(trace_name, state)

    if command == "read":
        return ModuleResponse("Usage: read <trace-name>\nType 'look' to see visible traces.")

    if command == "quit":
        return ModuleResponse("First Spark closed.", should_quit=True)

    return ModuleResponse(
        f"Unknown command: {command}\nType 'help' for available commands."
    )


def read_trace(trace_name: str, state: GameState) -> ModuleResponse:
    """Read a visible trace by name."""
    trace_text = VISIBLE_TRACES.get(trace_name)

    if trace_text is None:
        return ModuleResponse(
            f"Trace not found: {trace_name}\nType 'look' to see visible traces."
        )

    state.read_traces.add(trace_name)
    return ModuleResponse(trace_text.strip())
