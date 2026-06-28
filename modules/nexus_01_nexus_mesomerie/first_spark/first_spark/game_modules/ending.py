"""Ending module for Nexus 0.1 - First Spark."""

from __future__ import annotations

from first_spark.module_response import ModuleResponse
from first_spark.state import GameState


PUBLIC_DEMO_MESSAGE = """[public demo message]

This is a public demo message.
Real gift messages belong to the private activation layer.
"""


HELP_TEXT = """Available commands:
  help     Show this help text.
  look     Look at the opened public demo message.
  unlock   Show the already opened public demo message again.
  trace    Reveal a gentle next trace.
  quit     Exit First Spark.
"""


ENDING_TEXT = f"""The private message opens.

{PUBLIC_DEMO_MESSAGE.strip()}"""


ALREADY_OPEN_TEXT = f"""The private message is already open.

{PUBLIC_DEMO_MESSAGE.strip()}"""


def handle_command(command: str, state: GameState) -> ModuleResponse:
    """Handle commands after the public demo message was opened."""
    if command == "help":
        return ModuleResponse(HELP_TEXT.strip())

    if command == "look":
        return ModuleResponse(ALREADY_OPEN_TEXT)

    if command == "unlock":
        return ModuleResponse(ALREADY_OPEN_TEXT)

    if command == "trace":
        return ModuleResponse("Next trace:\n  The First Spark is complete.")

    if command == "quit":
        return ModuleResponse("First Spark closed.", should_quit=True)

    return ModuleResponse(
        f"Unknown command: {command}\nType 'help' for available commands."
    )


def open_ending(state: GameState) -> ModuleResponse:
    """Open the public demo ending and move into the ending module."""
    state.message_unlocked = True
    return ModuleResponse(ENDING_TEXT, next_module="ending")
