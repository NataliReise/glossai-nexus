"""Ending module for Nexus 0.1 - First Spark."""

from __future__ import annotations

from first_spark.command_feedback import unknown_command_text
from first_spark.config import PRIVATE_MESSAGE
from first_spark.guidance import WALKTHROUGH_TEXT
from first_spark.module_response import ModuleResponse
from first_spark.state import GameState


PUBLIC_REPOSITORY_URL = "https://github.com/NataliReise/glossai-nexus.git"
WHAT_NEXT_GUIDE_URL = (
    "https://github.com/NataliReise/glossai-nexus/blob/main/"
    "modules/nexus_01_nexus_mesomerie/first_spark/WHAT_NEXT.md"
)
PERSONAL_DIVIDER = "︵‿︵‿୨ ☾𓋹☽ ୧‿︵‿︵"
TECHNICAL_SECTION_DIVIDER = "┈┈┈✧┈┈┈◈┈┈┈✧┈┈┈"


ACTIVATION_MESSAGE = f"""[activation message]

{PRIVATE_MESSAGE}"""

AFTER_PLAY_MESSAGE = f"""[after-play]

The First Spark is complete.

You may keep this as a finished gift.
Nothing else is required.


{TECHNICAL_SECTION_DIVIDER}

If you want, you may let the spark travel further.
Give a clean public copy of First Spark or the Git link to someone you choose.
Add a private activation package only through a private channel.


{TECHNICAL_SECTION_DIVIDER}

Public project:
  {PUBLIC_REPOSITORY_URL}

Short guide:
  {WHAT_NEXT_GUIDE_URL}


Never post private activation data, private gift messages, or return artifacts publicly.


{TECHNICAL_SECTION_DIVIDER}

Later, you may also share a public-safe resonance node to show that a spark was seen.
A resonance node must not include private messages, activation files, or return artifacts.

Use /resonance-node to show an optional public-safe draft.
You can copy that draft, edit only the public alias and public note, and share it manually if you choose."""


RESONANCE_NODE_TEXT = f"""[public-safe resonance node draft]

This is an optional public-safe note.
Copy it only if you want to leave a visible trace.
Do not add private activation data, private gift messages, or return artifacts.

---
Resonance Node: N01-RN-draft
Module: Nexus 01 - First Spark
Run type: private gift / neutral / carried spark
Status: completed
Trace visibility: public-safe summary only
Forwarded: optional / yes / no / not shared
Return: optional / received / not shared
Public project: {PUBLIC_REPOSITORY_URL}

Public alias:
Public note:

Consent:
I choose to share this public trace.
No private activation data, private gift text, or return artifact is included.
---"""


HELP_TEXT = """Available commands:
  /help            Show this help text.
  /look            Look at the opened activation message.
  /unlock          Show the already opened activation message again.
  /trace           Reveal a gentle next trace.
  /resonance-node  Show a public-safe resonance node draft.
  /walkthrough     Show the full solution path with a spoiler warning.
  /quit            Leave First Spark.
"""


ENDING_TEXT = f"""The private message opens.

{AFTER_PLAY_MESSAGE.strip()}

{PERSONAL_DIVIDER}

{ACTIVATION_MESSAGE.strip()}

{PERSONAL_DIVIDER}"""


ALREADY_OPEN_TEXT = f"""The private message is already open.

{AFTER_PLAY_MESSAGE.strip()}

{PERSONAL_DIVIDER}

{ACTIVATION_MESSAGE.strip()}

{PERSONAL_DIVIDER}"""


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

    if command == "resonance-node":
        return ModuleResponse(RESONANCE_NODE_TEXT)

    if command == "walkthrough":
        return ModuleResponse(WALKTHROUGH_TEXT.strip())

    if command == "quit":
        return ModuleResponse("First Spark closed.", should_quit=True)

    return ModuleResponse(unknown_command_text())


def open_ending(state: GameState) -> ModuleResponse:
    """Open the activation message and move into the ending module."""
    state.message_unlocked = True
    return ModuleResponse(ENDING_TEXT, next_module="ending")
