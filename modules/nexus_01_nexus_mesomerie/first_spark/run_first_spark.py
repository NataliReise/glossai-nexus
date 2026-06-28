#!/usr/bin/env python3
"""Nexus 0.1 - First Spark.

Fourth running unit: print a boot sequence and accept simple commands.

This file is still intentionally tiny. It proves that the first playable slice
can start locally, accept a minimal command loop, show a first view into the
Nexus space, and read visible traces before puzzle logic is added.
"""

from __future__ import annotations


MODULE_TITLE = "Nexus 0.1 - First Spark"
RECIPIENT_ALIAS = "recipient_name"
PROMPT = "nexus> "


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
    print("Fourth running unit online.")
    print("Type 'help' for available commands.")
    print()


def print_help() -> None:
    """Print available commands."""
    print()
    print(HELP_TEXT)


def print_look() -> None:
    """Print the first view into the First Spark chamber."""
    print()
    print(LOOK_TEXT)


def read_trace(trace_name: str) -> None:
    """Read a visible trace by name."""
    trace_text = VISIBLE_TRACES.get(trace_name)

    print()
    if trace_text is None:
        print(f"Trace not found: {trace_name}")
        print("Type 'look' to see visible traces.")
    else:
        print(trace_text)
    print()


def command_loop() -> None:
    """Run the minimal command loop."""
    while True:
        command = input(PROMPT).strip().lower()

        if command == "help":
            print_help()
        elif command == "look":
            print_look()
        elif command.startswith("read "):
            trace_name = command.removeprefix("read ").strip()
            if trace_name:
                read_trace(trace_name)
            else:
                print()
                print("Usage: read <trace-name>")
                print("Type 'look' to see visible traces.")
                print()
        elif command == "read":
            print()
            print("Usage: read <trace-name>")
            print("Type 'look' to see visible traces.")
            print()
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
