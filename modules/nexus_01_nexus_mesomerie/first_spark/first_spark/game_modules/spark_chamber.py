"""Spark chamber module for Nexus 0.1 - First Spark."""

from __future__ import annotations

from first_spark.module_response import ModuleResponse
from first_spark.state import GameState


REQUIRED_TRACES_FOR_LINK = {"welcome.log", "spark.note"}


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


PUBLIC_DEMO_MESSAGE = """[public demo message]

This is a public demo message.
Real gift messages belong to the private activation layer.
"""


HELP_TEXT = """Available commands:
  help                 Show this help text.
  look                 Look around the First Spark chamber.
  read <trace-name>    Read a visible trace.
  link spark           Link the first spark fragments.
  unlock               Open the public demo message after linking the spark.
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

    if command == "link spark":
        return link_spark(state)

    if command.startswith("link "):
        return ModuleResponse("Unknown link target.\nTry: link spark")

    if command == "link":
        return ModuleResponse("Usage: link spark")

    if command == "unlock":
        return unlock_message(state)

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


def link_spark(state: GameState) -> ModuleResponse:
    """Link the first spark fragments after the visible traces were read."""
    if state.spark_linked:
        return ModuleResponse(
            "The spark fragments are already linked.\n"
            "The private message is still locked."
        )

    missing_traces = REQUIRED_TRACES_FOR_LINK - state.read_traces
    if missing_traces:
        return ModuleResponse(
            "The spark is not ready to link.\n"
            "Read the visible traces first."
        )

    state.spark_linked = True
    return ModuleResponse(
        "Fragment connection detected.\n"
        "Linked fragments:\n"
        "  welcome.log\n"
        "  spark.note\n\n"
        "The private message reacts, but remains locked.\n"
        "Next unit: unlock command."
    )


def unlock_message(state: GameState) -> ModuleResponse:
    """Unlock the public demo message after the spark was linked."""
    if state.message_unlocked:
        return ModuleResponse(
            "The private message is already open.\n\n"
            f"{PUBLIC_DEMO_MESSAGE.strip()}"
        )

    if not state.spark_linked:
        return ModuleResponse(
            "The private message does not open yet.\n"
            "Link the spark first."
        )

    state.message_unlocked = True
    return ModuleResponse(
        "The private message opens.\n\n"
        f"{PUBLIC_DEMO_MESSAGE.strip()}"
    )
