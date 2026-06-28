"""Arrival module for Nexus 0.1 - First Spark."""

from __future__ import annotations

from first_spark.config import MODULE_TITLE, RECIPIENT_ALIAS
from first_spark.module_response import ModuleResponse
from first_spark.state import GameState


HELP_TEXT = """Available commands:
  help                 Show this help text.
  look                 Enter the First Spark chamber.
  quit                 Exit First Spark.
"""


def boot_text() -> str:
    """Return the first visible boot sequence."""
    return f"""
================================================
{MODULE_TITLE}
================================================

Activation detected.
Recipient: {RECIPIENT_ALIAS}
Private message: locked.

Refactoring running unit online.
Type 'help' for available commands.
""".strip()


def handle_command(command: str, state: GameState) -> ModuleResponse:
    """Handle commands in the arrival module."""
    if command == "help":
        return ModuleResponse(HELP_TEXT.strip())

    if command == "look":
        return ModuleResponse("Entering the First Spark chamber.", next_module="spark_chamber")

    if command == "quit":
        return ModuleResponse("First Spark closed.", should_quit=True)

    return ModuleResponse(
        f"Unknown command: {command}\nType 'help' for available commands."
    )
