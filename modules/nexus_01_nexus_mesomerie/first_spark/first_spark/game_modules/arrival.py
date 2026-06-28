"""Arrival module for Nexus 0.1 - First Spark."""

from __future__ import annotations

from first_spark.command_feedback import unknown_command_text
from first_spark.config import MODULE_TITLE, RECIPIENT_ALIAS
from first_spark.guidance import WALKTHROUGH_TEXT
from first_spark.module_response import ModuleResponse
from first_spark.state import GameState


HELP_TEXT = """Available commands:
  help                 Show this help text.
  look                 Enter the First Spark chamber.
  trace                Reveal a gentle next trace.
  walkthrough          Show the full solution path with a spoiler warning.
  quit                 Exit First Spark and return to your terminal.
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

First Spark online.
Type 'help' for available commands.
""".strip()


def handle_command(command: str, state: GameState) -> ModuleResponse:
    """Handle commands in the arrival module."""
    if command == "help":
        return ModuleResponse(HELP_TEXT.strip())

    if command == "look":
        return ModuleResponse("Entering the First Spark chamber.", next_module="spark_chamber")

    if command == "trace":
        return ModuleResponse("Next trace:\n  Look for the entrance.")

    if command == "walkthrough":
        return ModuleResponse(WALKTHROUGH_TEXT.strip())

    if command == "quit":
        return ModuleResponse("First Spark closed.", should_quit=True)

    return ModuleResponse(unknown_command_text(command))
