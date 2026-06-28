"""Command feedback helpers for Nexus 0.1 - First Spark."""

from __future__ import annotations


def unknown_command_text(command: str) -> str:
    """Return a helpful unknown-command message.

    The additional note explains a common terminal copy-and-paste situation
    without trying to interpret or repair the user's input automatically.
    """
    return (
        f"Unknown command: {command}\n\n"
        "This may include pasted input that was still waiting in the terminal.\n"
        "Type 'help' for available commands.\n"
        "Type 'quit' on a fresh prompt to leave First Spark."
    )
