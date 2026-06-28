#!/usr/bin/env python3
"""Nexus 0.1 - First Spark.

Second running unit: print a boot sequence and accept two commands.

This file is still intentionally tiny. It proves that the first playable slice
can start locally and accept a minimal command loop before file inspection or
puzzle logic is added.
"""

from __future__ import annotations


MODULE_TITLE = "Nexus 0.1 - First Spark"
RECIPIENT_ALIAS = "recipient_name"
PROMPT = "nexus> "


HELP_TEXT = """Available commands:
  help   Show this help text.
  quit   Exit First Spark.
"""


def print_boot_sequence() -> None:
    """Print the first visible boot sequence for First Spark."""
    print()
    print("=" * 48)
    print(MODULE_TITLE)
    print("=" * 48)
    print()
    print("Activation detected.")
    print(f"Recipient: {RECIPIENT_ALIAS}")
    print("Private message: locked.")
    print()
    print("Second running unit online.")
    print("Type 'help' for available commands.")
    print()


def print_help() -> None:
    """Print available commands."""
    print()
    print(HELP_TEXT)


def command_loop() -> None:
    """Run the minimal command loop."""
    while True:
        command = input(PROMPT).strip().lower()

        if command == "help":
            print_help()
        elif command == "quit":
            print()
            print("First Spark closed.")
            print()
            break
        elif command == "":
            continue
        else:
            print()
            print(f"Unknown command: {command}")
            print("Type 'help' for available commands.")
            print()


def main() -> None:
    """Run the first tiny First Spark prototype."""
    print_boot_sequence()
    command_loop()


if __name__ == "__main__":
    main()
