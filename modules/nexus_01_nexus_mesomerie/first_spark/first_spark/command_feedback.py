"""Command feedback helpers for Nexus 0.1 - First Spark."""

from __future__ import annotations


def unknown_command_text() -> str:
    """Return neutral feedback for input outside the public grammar."""
    return (
        "Unknown First Spark command.\n"
        "Use /help to see the commands available here."
    )
