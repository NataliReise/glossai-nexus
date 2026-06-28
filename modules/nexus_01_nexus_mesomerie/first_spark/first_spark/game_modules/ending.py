"""Ending module for Nexus 0.1 - First Spark."""

from __future__ import annotations

from first_spark.command_feedback import unknown_command_text
from first_spark.config import PRIVATE_MESSAGE
from first_spark.guidance import WALKTHROUGH_TEXT
from first_spark.module_response import ModuleResponse
from first_spark.state import GameState


PUBLIC_REPOSITORY_URL = "https://github.com/NataliReise/glossai-nexus.git"


ACTIVATION_MESSAGE = f"""[activation message]

{PRIVATE_MESSAGE}"""


AFTER_PLAY_MESSAGE = f"""[after-play]

The First Spark is complete.

You may keep this as a finished gift.
Nothing else is required.

If you want, you may let the spark travel further.
Give a clean public copy of First Spark or the Git link to someone you choose.
Add a private activation package only through a private channel.

Public project:
  {PUBLIC_REPOSITORY_URL}

Never post private activation data, private gift messages, or return artifacts publicly.

Later, you may also share a public-safe resonance node to show that a spark was seen.
A resonance node must not include private messages, activation files, or return artifacts."""


HELP_TEXT = """Available commands:
  help         Show this help text.
  look         Look at the opened activation message.
  unlock       Show the already opened activation message again.
  trace        Reveal a gentle next trace.
  walkthrough  Show the full solution path with a spoiler warning.
  quit         Exit First Spark and return to your terminal.
"""


ENDING_TEXT = f"""The private message opens.

{ACTIVATION_MESSAGE.strip()}

{AFTER_PLAY_MESSAGE.strip()}"""


ALREADY_OPEN_TEXT = f"""The private message is already open.

{ACTIVATION_MESSAGE.strip()}

{AFTER_PLAY_MESSAGE.strip()}"""


def handle_command(command: str, state: GameState) -> ModuleResponse:
    """Handle commands after the activation message was opened."""
    if command == "help":
        return ModuleResponse(HELP_TEXT.strip())

    if command == "look":
        return ModuleResponse(ALREADY_OPEN_TEXT)

    if command == "unlock":
        return ModuleResponse(ALREADY_OPEN_TEXT)

    if command == "trace":
        return ModuleResponse("Next trace:\n  The First Spark is complete.")

    if command == "walkthrough":
        return ModuleResponse(WALKTHROUGH_TEXT.strip())

    if command == "quit":
        return ModuleResponse("First Spark closed.", should_quit=True)

    return ModuleResponse(unknown_command_text(command))


def open_ending(state: GameState) -> ModuleResponse:
    """Open the activation message and move into the ending module."""
    state.message_unlocked = True
    return ModuleResponse(ENDING_TEXT, next_module="ending")
